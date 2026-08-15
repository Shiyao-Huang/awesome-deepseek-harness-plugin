#!/usr/bin/env python3
"""Validate raw snapshots, SQLite integrity, and core aggregator invariants."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
RAW_DIR = ROOT / "data" / "raw"


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
    items = connection.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    platforms = connection.execute("SELECT COUNT(DISTINCT platform) FROM items").fetchone()[0]
    metrics = connection.execute("SELECT COUNT(*) FROM metrics").fetchone()[0]
    media = connection.execute("SELECT COUNT(*) FROM media_assets").fetchone()[0]
    print(f"validated {len(raw_paths)} raw files; {items} items; {platforms} platforms; {metrics} metrics; {media} media assets")


if __name__ == "__main__":
    main()

