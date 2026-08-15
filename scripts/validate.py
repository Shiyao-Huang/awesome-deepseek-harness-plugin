#!/usr/bin/env python3
"""Validate raw snapshots, SQLite integrity, and core aggregator invariants."""

from __future__ import annotations

import json
import hashlib
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
FULL_ARCHIVE_PATH = ROOT / "data" / "aggregator-full.sqlite3.zst"
RAW_DIR = ROOT / "data" / "raw"
INDEX_PATH = ROOT / "index" / "records.jsonl"
VALUE_MATRIX_PATH = ROOT / "index" / "value-matrix.jsonl"
FORK_INDEX_PATH = ROOT / "docs" / "data" / "forks.json"
INDEX_FIELDS = {
    "id", "summary", "url", "repo", "context", "picture", "comment", "favor",
    "views", "refs", "rank", "stars", "dataset_version", "first_seen_at", "last_seen_at",
}
VALUE_MATRIX_FIELDS = {
    "id", "item_id", "title", "url", "platform", "category", "dataset_version", "scoring_version",
    "assessed_at", "utility", "evidence", "traction", "ecosystem", "freshness", "reviewability",
    "value_score", "confidence_score", "value_band", "evidence_count", "source_count", "risk_flags",
}
PUBLIC_DB_MAX_BYTES = 95 * 1024 * 1024
PUBLIC_RAW_JSON_COLUMNS = (
    ("raw_snapshots", "payload_json"),
    ("items", "raw_json"),
    ("metrics", "raw_json"),
    ("github_user_profiles", "raw_json"),
    ("fork_file_changes", "raw_json"),
    ("fork_commits", "raw_json"),
)


def main() -> None:
    """Run deterministic checks and print the current dataset size."""

    raw_paths = [
        path for path in RAW_DIR.rglob("*.json")
        if "auto" not in path.parts and "forks" not in path.parts
    ]
    for path in raw_paths:
        json.loads(path.read_text(encoding="utf-8"))
    connection = sqlite3.connect(DB_PATH)
    integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    assert integrity == "ok", integrity
    is_public_projection = connection.execute(
        "SELECT 1 FROM sqlite_schema WHERE type = 'table' AND name = 'public_projection_metadata'"
    ).fetchone() is not None
    if is_public_projection:
        projection = connection.execute(
            "SELECT projection_version, source_sha256, authoritative_archive, latest_value_run_id "
            "FROM public_projection_metadata"
        ).fetchall()
        assert len(projection) == 1
        assert projection[0][0] == 1
        assert len(projection[0][1]) == 64
        assert projection[0][2]
        assert FULL_ARCHIVE_PATH.is_file() and FULL_ARCHIVE_PATH.stat().st_size > 0
        assert DB_PATH.stat().st_size <= PUBLIC_DB_MAX_BYTES
        for table, column in PUBLIC_RAW_JSON_COLUMNS:
            assert connection.execute(
                f'SELECT COUNT(*) FROM "{table}" WHERE "{column}" <> ?', ("{}",)
            ).fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM items WHERE canonical_url = ''").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM items WHERE raw_json IS NULL OR raw_json = ''").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM metrics WHERE metric_source IS NULL OR metric_source = ''").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM item_observations").fetchone()[0] >= connection.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    assert connection.execute("SELECT COUNT(*) FROM items").fetchone()[0] == connection.execute("SELECT COUNT(DISTINCT canonical_url) FROM items").fetchone()[0]
    assert connection.execute("SELECT COUNT(*) FROM items").fetchone()[0] == connection.execute("SELECT COUNT(DISTINCT platform || char(0) || external_id) FROM items").fetchone()[0]
    assert connection.execute("SELECT COUNT(*) FROM fork_repositories").fetchone()[0] == connection.execute("SELECT COUNT(DISTINCT full_name) FROM fork_repositories").fetchone()[0]
    assert connection.execute("SELECT COUNT(*) FROM github_user_profiles").fetchone()[0] == connection.execute("SELECT COUNT(DISTINCT login) FROM github_user_profiles").fetchone()[0]
    assert connection.execute(
        "SELECT COUNT(*) FROM (SELECT fork_id, collection_run_id FROM fork_snapshots GROUP BY fork_id, collection_run_id HAVING COUNT(*) > 1)"
    ).fetchone()[0] == 0
    assert connection.execute(
        "SELECT COUNT(*) FROM (SELECT fork_id, collection_run_id, ranking_version FROM fork_rankings GROUP BY fork_id, collection_run_id, ranking_version HAVING COUNT(*) > 1)"
    ).fetchone()[0] == 0
    assert connection.execute(
        "SELECT COUNT(*) FROM (SELECT collection_run_id, ranking_version, rank FROM fork_rankings GROUP BY collection_run_id, ranking_version, rank HAVING COUNT(*) > 1)"
    ).fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM metrics WHERE item_id IS NULL OR metric_source = ''").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM collection_runs").fetchone()[0] > 0
    assert connection.execute("SELECT COUNT(*) FROM observations WHERE collection_run_id IS NULL").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM metrics WHERE collection_run_id IS NULL").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM items WHERE first_seen_run_id IS NULL OR last_seen_run_id IS NULL").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM raw_snapshots WHERE payload_json IS NULL OR payload_json = ''").fetchone()[0] == 0
    for path in raw_paths:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert connection.execute("SELECT 1 FROM raw_snapshots WHERE raw_sha256 = ?", (digest,)).fetchone(), path
    assert connection.execute("SELECT COUNT(*) FROM observations WHERE raw_path IS NOT NULL AND raw_snapshot_id IS NULL").fetchone()[0] == 0
    items = connection.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    index_records = [json.loads(line) for line in INDEX_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(index_records) == connection.execute("SELECT COUNT(*) FROM index_records").fetchone()[0]
    assert len({record["id"] for record in index_records}) == len(index_records)
    assert all(set(record) == INDEX_FIELDS for record in index_records)
    fork_index = json.loads(FORK_INDEX_PATH.read_text(encoding="utf-8"))
    fork_records = fork_index["records"]
    assert len({record["full_name"] for record in fork_records}) == len(fork_records)
    assert len({record["rank"] for record in fork_records}) == len(fork_records)
    assert len(fork_records) == connection.execute("SELECT COUNT(*) FROM v_current_fork_rankings").fetchone()[0]
    assert connection.execute("SELECT COUNT(*) FROM index_records WHERE dataset_version IS NULL OR dataset_version = ''").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM item_details WHERE status = 'ok' AND char_count = 0").fetchone()[0] == 0
    current_run_id = connection.execute(
        "SELECT id FROM collection_runs WHERE trigger <> 'legacy-migration' ORDER BY id DESC LIMIT 1"
    ).fetchone()[0]
    assert connection.execute("SELECT COUNT(*) FROM value_assessments WHERE collection_run_id = ?", (current_run_id,)).fetchone()[0] == items
    if is_public_projection:
        assert connection.execute("SELECT COUNT(*) FROM value_assessments").fetchone()[0] == items
        assert projection[0][3] == current_run_id
    value_records = [json.loads(line) for line in VALUE_MATRIX_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(value_records) == items
    assert len({record["id"] for record in value_records}) == len(value_records)
    assert all(set(record) == VALUE_MATRIX_FIELDS for record in value_records)
    assert all(record["value_band"] in {"A", "B", "C", "D"} for record in value_records)
    assert all(0 <= record[key] <= 100 for record in value_records for key in ("utility", "evidence", "traction", "ecosystem", "freshness", "reviewability", "value_score", "confidence_score"))
    platforms = connection.execute("SELECT COUNT(DISTINCT platform) FROM items").fetchone()[0]
    metrics = connection.execute("SELECT COUNT(*) FROM metrics").fetchone()[0]
    media = connection.execute("SELECT COUNT(*) FROM media_assets").fetchone()[0]
    snapshots = connection.execute("SELECT COUNT(*) FROM raw_snapshots").fetchone()[0]
    latest_version = connection.execute("SELECT dataset_version FROM collection_runs WHERE trigger <> 'legacy-migration' ORDER BY id DESC LIMIT 1").fetchone()[0]
    print(f"validated {len(raw_paths)} raw files/{snapshots} snapshots; latest {latest_version}; {items} items; {platforms} platforms; {metrics} metrics; {media} media assets; {len(index_records)} index records")


if __name__ == "__main__":
    main()
