#!/usr/bin/env python3
"""Validate raw snapshots, SQLite integrity, and core aggregator invariants."""

from __future__ import annotations

import json
import hashlib
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
RAW_DIR = ROOT / "data" / "raw"
INDEX_PATH = ROOT / "index" / "records.jsonl"
INDEX_FIELDS = {
    "id", "summary", "url", "repo", "context", "picture", "comment", "favor",
    "views", "refs", "rank", "stars", "dataset_version", "first_seen_at", "last_seen_at",
}


def main() -> None:
    """Run deterministic checks and print the current dataset size."""

    raw_paths = [path for path in RAW_DIR.rglob("*.json") if "auto" not in path.parts]
    for path in raw_paths:
        json.loads(path.read_text(encoding="utf-8"))
    connection = sqlite3.connect(DB_PATH)
    integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    assert integrity == "ok", integrity
    assert connection.execute("SELECT COUNT(*) FROM items WHERE canonical_url = ''").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM items WHERE raw_json IS NULL OR raw_json = ''").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM metrics WHERE metric_source IS NULL OR metric_source = ''").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM item_observations").fetchone()[0] >= connection.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    assert connection.execute("SELECT COUNT(*) FROM collection_runs").fetchone()[0] > 0
    assert connection.execute("SELECT COUNT(*) FROM observations WHERE collection_run_id IS NULL").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM metrics WHERE collection_run_id IS NULL").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM items WHERE first_seen_run_id IS NULL OR last_seen_run_id IS NULL").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM raw_snapshots WHERE payload_json IS NULL OR payload_json = ''").fetchone()[0] == 0
    for path in raw_paths:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert connection.execute("SELECT 1 FROM raw_snapshots WHERE raw_sha256 = ?", (digest,)).fetchone(), path
    assert connection.execute("SELECT COUNT(*) FROM observations WHERE raw_path IS NOT NULL AND raw_snapshot_id IS NULL").fetchone()[0] == 0
    index_records = [json.loads(line) for line in INDEX_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(index_records) == connection.execute("SELECT COUNT(*) FROM index_records").fetchone()[0]
    assert len({record["id"] for record in index_records}) == len(index_records)
    assert all(set(record) == INDEX_FIELDS for record in index_records)
    assert connection.execute("SELECT COUNT(*) FROM index_records WHERE dataset_version IS NULL OR dataset_version = ''").fetchone()[0] == 0
    items = connection.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    platforms = connection.execute("SELECT COUNT(DISTINCT platform) FROM items").fetchone()[0]
    metrics = connection.execute("SELECT COUNT(*) FROM metrics").fetchone()[0]
    media = connection.execute("SELECT COUNT(*) FROM media_assets").fetchone()[0]
    snapshots = connection.execute("SELECT COUNT(*) FROM raw_snapshots").fetchone()[0]
    latest_version = connection.execute("SELECT dataset_version FROM collection_runs WHERE trigger <> 'legacy-migration' ORDER BY id DESC LIMIT 1").fetchone()[0]
    print(f"validated {len(raw_paths)} raw files/{snapshots} snapshots; latest {latest_version}; {items} items; {platforms} platforms; {metrics} metrics; {media} media assets; {len(index_records)} index records")


if __name__ == "__main__":
    main()
