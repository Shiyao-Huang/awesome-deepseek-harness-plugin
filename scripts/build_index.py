#!/usr/bin/env python3
"""Build the item registration table and JSONL index from SQLite."""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
INDEX_DIR = ROOT / "index"
REGISTRY_PATH = INDEX_DIR / "records.jsonl"


def connect() -> sqlite3.Connection:
    """Open the database with rows addressable by column name."""

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def json_list(value: Any) -> list[str]:
    """Return a de-duplicated list of non-empty URL-like strings."""

    if not isinstance(value, list):
        return []
    result: list[str] = []
    for entry in value:
        if not isinstance(entry, str) or not entry.strip() or entry in result:
            continue
        result.append(entry.strip())
    return result


def raw_item(row: sqlite3.Row) -> dict[str, Any]:
    """Decode an item's normalized raw JSON payload."""

    try:
        value = json.loads(row["raw_json"])
    except (TypeError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def repo_name(row: sqlite3.Row, raw: dict[str, Any]) -> str | None:
    """Extract a repository slug when the item explicitly names one."""

    if row["platform"] == "github" and "/" in str(row["external_id"]):
        return str(row["external_id"])
    for key in ("repo", "repository", "source_repo"):
        value = raw.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    source_entry = raw.get("source_entry")
    if isinstance(source_entry, dict) and isinstance(source_entry.get("source_repo"), str):
        return source_entry["source_repo"]
    return None


def latest_run(connection: sqlite3.Connection) -> str:
    """Return the current dataset version, including legacy databases."""

    row = connection.execute(
        "SELECT dataset_version FROM collection_runs WHERE trigger <> 'legacy-migration' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    return str(row[0]) if row else "legacy"


def build_records(connection: sqlite3.Connection, dataset_version: str) -> list[dict[str, Any]]:
    """Create registry records in deterministic ranking order."""

    rows = connection.execute(
        """
        SELECT m.*, i.raw_json, i.content_text, i.relevance,
               v.value_score, v.value_band, v.confidence_score, v.risk_flags,
               i.first_seen_at AS item_first_seen_at,
               i.last_seen_at AS item_last_seen_at
        FROM v_latest_metrics AS m
        JOIN items AS i ON i.id = m.item_id
        LEFT JOIN v_current_value_matrix AS v ON v.item_id = m.item_id
        """
    ).fetchall()
    media_by_item: dict[int, list[str]] = {}
    for row in connection.execute(
        "SELECT item_id, url, thumbnail_url FROM media_assets ORDER BY id"
    ):
        values = media_by_item.setdefault(int(row["item_id"]), [])
        for value in (row["url"], row["thumbnail_url"]):
            if value and value not in values:
                values.append(str(value))

    ranked = sorted(
        rows,
        key=lambda row: (
            -max(
                int(row["stars"] or 0),
                int(row["favorites"] or row["likes"] or 0),
                int(row["views"] or 0),
                int(row["comments"] or row["replies"] or 0),
            ),
            str(row["platform"]),
            str(row["canonical_url"]),
        ),
    )
    records: list[dict[str, Any]] = []
    for rank, row in enumerate(ranked, 1):
        raw = raw_item(row)
        refs = json_list(raw.get("links"))
        for value in json_list(raw.get("refs")):
            if value not in refs:
                refs.append(value)
        for key in ("media_url", "thumbnail_url"):
            value = raw.get(key)
            if isinstance(value, str) and value and value not in refs:
                refs.append(value)
        comments = row["comments"] if row["comments"] is not None else row["replies"]
        favor = row["favorites"] if row["favorites"] is not None else row["likes"]
        context = {
            "platform": row["platform"],
            "item_type": row["item_type"],
            "author": row["author"],
            "category": row["category"],
            "relevance": row["relevance"],
            "language": raw.get("language"),
            "content": row["content_text"],
            "value_matrix": {
                "score": row["value_score"],
                "band": row["value_band"],
                "confidence": row["confidence_score"],
                "risk_flags": json.loads(row["risk_flags"]) if row["risk_flags"] else [],
            },
        }
        records.append({
            "id": f"id-{row['item_id']}",
            "summary": row["title"] or row["content_text"],
            "url": row["canonical_url"],
            "repo": repo_name(row, raw),
            "context": context,
            "picture": media_by_item.get(int(row["item_id"]), []),
            "comment": comments,
            "favor": favor,
            "views": row["views"],
            "refs": refs,
            "rank": rank,
            "stars": row["stars"],
            "dataset_version": dataset_version,
            "first_seen_at": row["item_first_seen_at"],
            "last_seen_at": row["item_last_seen_at"],
        })
    return records


def write_records(connection: sqlite3.Connection, records: list[dict[str, Any]]) -> None:
    """Replace the generated registry projection and write its JSONL form."""

    connection.execute("DELETE FROM index_records")
    for record in records:
        connection.execute(
            """
            INSERT INTO index_records(
                id, item_id, summary, url, repo, context, picture, comment, favor,
                views, refs, rank, stars, dataset_version, first_seen_at, last_seen_at
            )
            SELECT ?, i.id, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, i.first_seen_at, i.last_seen_at
            FROM items AS i
            WHERE i.id = ?
            """,
            (
                record["id"],
                record["summary"],
                record["url"],
                record["repo"],
                json.dumps(record["context"], ensure_ascii=False, sort_keys=True),
                json.dumps(record["picture"], ensure_ascii=False),
                record["comment"],
                record["favor"],
                record["views"],
                json.dumps(record["refs"], ensure_ascii=False),
                record["rank"],
                record["stars"],
                record["dataset_version"],
                int(record["id"].removeprefix("id-")),
            ),
        )
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(
        "".join(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n" for record in records),
        encoding="utf-8",
    )


def main() -> int:
    """Build and validate the generated registration."""

    from collect import init_db

    init_db(DB_PATH)
    with connect() as connection:
        records = build_records(connection, latest_run(connection))
        write_records(connection, records)
    print(f"built {len(records)} index records at {REGISTRY_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
