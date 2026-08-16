#!/usr/bin/env python3
"""Reject a candidate SQLite dataset that loses or rewrites metric history."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Optional


MetricKey = tuple[str, str, str]
MetricProvenance = tuple[Optional[int], Optional[str]]


def metric_history(path: Path) -> dict[MetricKey, MetricProvenance]:
    """Return metric identities and their collection-run provenance."""

    if not path.is_file():
        raise RuntimeError(f"SQLite database does not exist: {path}")
    connection = sqlite3.connect(f"file:{path.resolve()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            """
            SELECT
                i.canonical_url,
                m.observed_at,
                m.metric_source,
                m.collection_run_id,
                r.dataset_version
            FROM metrics AS m
            JOIN items AS i ON i.id = m.item_id
            LEFT JOIN collection_runs AS r ON r.id = m.collection_run_id
            ORDER BY i.canonical_url, m.observed_at, m.metric_source, m.id
            """
        ).fetchall()
    except sqlite3.Error as error:
        raise RuntimeError(f"could not read metric history from {path}: {error}") from error
    finally:
        connection.close()

    history: dict[MetricKey, MetricProvenance] = {}
    for row in rows:
        key = (str(row[0]), str(row[1]), str(row[2]))
        provenance = (int(row[3]) if row[3] is not None else None, row[4])
        if key in history:
            raise RuntimeError(f"duplicate metric history key in {path}: {format_key(key)}")
        history[key] = provenance
    return history


def append_only_errors(
    before: dict[MetricKey, MetricProvenance],
    after: dict[MetricKey, MetricProvenance],
) -> list[str]:
    """Describe missing keys and changed run provenance."""

    missing = sorted(set(before) - set(after))
    changed = sorted(key for key in set(before) & set(after) if before[key] != after[key])
    errors: list[str] = []
    if missing:
        samples = "; ".join(format_key(key) for key in missing[:5])
        errors.append(f"missing {len(missing)} metric history row(s): {samples}")
    if changed:
        samples = "; ".join(
            f"{format_key(key)}: {format_provenance(before[key])} -> {format_provenance(after[key])}"
            for key in changed[:5]
        )
        errors.append(
            f"changed collection run provenance for {len(changed)} metric history row(s): {samples}"
        )
    return errors


def format_key(key: MetricKey) -> str:
    """Format a metric identity for a diagnostic."""

    return " | ".join(key)


def format_provenance(provenance: MetricProvenance) -> str:
    """Format a metric run id and dataset version."""

    run_id, dataset_version = provenance
    return f"{run_id}/{dataset_version}"


def parse_args() -> argparse.Namespace:
    """Parse command-line database paths."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", type=Path, required=True, help="previous authoritative SQLite database")
    parser.add_argument("--after", type=Path, required=True, help="candidate SQLite database")
    return parser.parse_args()


def main() -> int:
    """Validate append-only metric identities and run provenance."""

    args = parse_args()
    try:
        before = metric_history(args.before)
        after = metric_history(args.after)
        errors = append_only_errors(before, after)
    except RuntimeError as error:
        print(error, file=sys.stderr)
        return 1
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(json.dumps({
        "after_metrics": len(after),
        "before_metrics": len(before),
        "preserved_metrics": len(before),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
