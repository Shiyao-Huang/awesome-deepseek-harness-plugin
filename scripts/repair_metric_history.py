#!/usr/bin/env python3
"""Replay baseline-missing Listing metrics from a full database's raw snapshots."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

import collect
import monitor_sources
from validate_append_only import MetricKey, MetricProvenance, append_only_errors, metric_history


INTEGER_FIELDS = (
    "likes", "replies", "reposts", "comments", "bookmarks", "views", "points",
    "stars", "forks", "open_issues", "subscribers", "favorites", "shares", "coins",
    "danmaku",
)


def metric_values(path: Path) -> dict[MetricKey, tuple[Any, ...]]:
    """Return normalized metric values keyed by their immutable identity."""

    connection = sqlite3.connect(f"file:{path.resolve()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            """
            SELECT
                i.canonical_url, m.observed_at, m.metric_source,
                m.likes, m.replies, m.reposts, m.comments, m.bookmarks, m.views, m.points,
                m.stars, m.forks, m.open_issues, m.subscribers, m.favorites, m.shares,
                m.coins, m.danmaku, m.upvote_ratio
            FROM metrics AS m
            JOIN items AS i ON i.id = m.item_id
            """
        ).fetchall()
    finally:
        connection.close()
    return {
        (str(row[0]), str(row[1]), str(row[2])): tuple(row[index] for index in range(3, len(row)))
        for row in rows
    }


def replay_missing_metrics(baseline: Path, database: Path) -> tuple[int, int]:
    """Restore only metric keys previously present in the authoritative baseline."""

    baseline_history = metric_history(baseline)
    baseline_values = metric_values(baseline)
    current_history = metric_history(database)
    changed = {
        key for key in set(baseline_history) & set(current_history)
        if baseline_history[key] != current_history[key]
    }
    if changed:
        details = append_only_errors(baseline_history, current_history)
        raise RuntimeError("; ".join(details))
    missing: dict[MetricKey, MetricProvenance] = {
        key: baseline_history[key]
        for key in sorted(set(baseline_history) - set(current_history))
    }
    unsupported = sorted(
        key for key in missing if key[2] not in monitor_sources.LISTING_METRIC_SOURCES
    )
    if unsupported:
        raise RuntimeError(
            "repair is limited to Listing metric sources; unsupported missing key: "
            + " | ".join(unsupported[0])
        )
    if not missing:
        return 0, 0

    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        item_ids = {
            str(row["canonical_url"]): int(row["id"])
            for row in connection.execute("SELECT id, canonical_url FROM items")
        }
        run_versions = {
            int(row["id"]): str(row["dataset_version"])
            for row in connection.execute("SELECT id, dataset_version FROM collection_runs")
        }
        for key, (run_id, dataset_version) in missing.items():
            if run_id is not None and run_versions.get(run_id) != dataset_version:
                raise RuntimeError(
                    "target database does not retain baseline run provenance for "
                    f"{' | '.join(key)}: {run_id}/{dataset_version}"
                )
        snapshot_rows = connection.execute(
            """
            SELECT DISTINCT rs.id, rs.raw_path, rs.collected_at, rs.payload_json,
                            rs.collection_run_id
            FROM raw_snapshots AS rs
            JOIN observations AS o ON o.raw_snapshot_id = rs.id
            WHERE o.collector IN (?, ?)
              AND rs.payload_json <> '{}'
            ORDER BY rs.id
            """,
            tuple(sorted(monitor_sources.SOURCE_COLLECTORS)),
        ).fetchall()
        restored = 0
        for row in snapshot_rows:
            payload = monitor_sources.normalized_raw_payload(
                str(row["raw_path"]), str(row["collected_at"]), str(row["payload_json"])
            )
            if payload is None:
                continue
            for observation in payload.get("observations", []):
                if not isinstance(observation, dict):
                    continue
                observed_at = str(
                    observation.get("collected_at")
                    or payload.get("collected_at")
                    or row["collected_at"]
                )
                for item in observation.get("items", []):
                    if not isinstance(item, dict):
                        continue
                    canonical = collect.canonical_url(
                        str(item.get("url") or item.get("canonical_url") or "")
                    )
                    metrics = item.get("metrics")
                    if not isinstance(metrics, dict):
                        continue
                    metric_source = str(metrics.get("metric_source") or "")
                    metric_observed_at = str(metrics.get("observed_at") or observed_at)
                    key = (canonical, metric_observed_at, metric_source)
                    if key not in missing:
                        continue
                    item_id = item_ids.get(canonical)
                    if item_id is None:
                        continue
                    integers = [collect.metric_int(metrics.get(field)) for field in INTEGER_FIELDS]
                    upvote_ratio = collect.metric_float(metrics.get("upvote_ratio"))
                    values = (*integers, upvote_ratio)
                    if not any(value is not None for value in values):
                        continue
                    if values != baseline_values[key]:
                        continue
                    metric_run_id = missing[key][0]
                    cursor = connection.execute(
                        """
                        INSERT INTO metrics(
                            item_id, collection_run_id, observed_at,
                            likes, replies, reposts, comments, bookmarks, views, points,
                            stars, forks, open_issues, subscribers, favorites, shares, coins, danmaku,
                            upvote_ratio, metric_source, raw_json
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(item_id, observed_at, metric_source) DO NOTHING
                        """,
                        (
                            item_id, metric_run_id, metric_observed_at, *values,
                            metric_source, json.dumps(metrics, ensure_ascii=False, sort_keys=True),
                        ),
                    )
                    if cursor.rowcount > 0:
                        restored += 1
                    missing.pop(key)
        if missing:
            first = next(iter(missing))
            raise RuntimeError(
                f"full raw snapshots could not restore {len(missing)} baseline metric row(s); "
                f"first unresolved key: {' | '.join(first)}"
            )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    errors = append_only_errors(baseline_history, metric_history(database))
    if errors:
        raise RuntimeError("; ".join(errors))
    return restored, restored


def parse_args() -> argparse.Namespace:
    """Parse baseline and target full-database paths."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True, help="previous authoritative full SQLite")
    parser.add_argument("--database", type=Path, required=True, help="full SQLite database to repair")
    return parser.parse_args()


def main() -> int:
    """Repair baseline-missing Listing metrics atomically."""

    args = parse_args()
    try:
        missing, restored = replay_missing_metrics(args.baseline, args.database)
    except (RuntimeError, sqlite3.Error, OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    print(json.dumps({"missing_metrics": missing, "restored_metrics": restored}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
