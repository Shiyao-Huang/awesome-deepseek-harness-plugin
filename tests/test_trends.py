"""Determinism checks for generated trend projections."""

from __future__ import annotations

import datetime as dt
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_trends


class _NoWallClockDate(dt.date):
    @classmethod
    def today(cls) -> _NoWallClockDate:
        raise AssertionError("trend generation must not read the wall-clock date")


class _NoWallClockDateTime(dt.datetime):
    @classmethod
    def now(cls, tz: dt.tzinfo | None = None) -> _NoWallClockDateTime:
        raise AssertionError("trend generation must not read the wall-clock time")


class TrendProjectionTests(unittest.TestCase):
    def test_same_collection_reference_produces_identical_artifacts(self) -> None:
        connection = sqlite3.connect(":memory:")
        connection.row_factory = sqlite3.Row
        connection.executescript(
            """
            CREATE TABLE collection_runs (
                id INTEGER PRIMARY KEY,
                dataset_version TEXT,
                started_at TEXT,
                finished_at TEXT,
                trigger TEXT,
                status TEXT,
                raw_files_seen INTEGER,
                item_observations INTEGER
            );
            CREATE TABLE items (
                id INTEGER PRIMARY KEY,
                platform TEXT,
                title TEXT,
                canonical_url TEXT,
                published_at TEXT,
                first_seen_at TEXT
            );
            CREATE TABLE metrics (
                id INTEGER PRIMARY KEY,
                item_id INTEGER,
                observed_at TEXT,
                stars INTEGER,
                forks INTEGER,
                likes INTEGER,
                reposts INTEGER,
                views INTEGER,
                points INTEGER,
                comments INTEGER
            );
            CREATE TABLE v_current_value_matrix (
                item_id INTEGER,
                value_band TEXT,
                value_score REAL
            );
            INSERT INTO collection_runs VALUES (
                1, 'v20260816T012711Z', '2026-08-16T01:27:00Z',
                '2026-08-16T01:27:11Z', 'manual', 'success', 1, 1
            );
            INSERT INTO items VALUES (
                1, 'github', 'Example plugin', 'https://github.com/example/plugin',
                '2026-08-13T01:00:00Z', '2026-08-13T01:00:00Z'
            );
            INSERT INTO metrics VALUES (
                1, 1, '2026-08-16T01:27:00Z', 1000000000, 1, NULL, NULL, NULL, NULL, NULL
            );
            INSERT INTO v_current_value_matrix VALUES (1, 'A', 88.0);
            """
        )
        traced_sql: list[str] = []
        connection.set_trace_callback(traced_sql.append)

        with tempfile.TemporaryDirectory() as directory:
            docs = Path(directory) / "docs"
            assets = docs / "assets"
            with (
                patch.object(build_trends, "DOCS", docs),
                patch.object(build_trends, "ASSETS", assets),
                patch.object(build_trends.dt, "date", _NoWallClockDate),
                patch.object(build_trends.dt, "datetime", _NoWallClockDateTime),
            ):
                build_trends.build(connection)
                first = {
                    path.relative_to(docs): path.read_bytes()
                    for path in sorted(docs.rglob("*"))
                    if path.is_file()
                }
                build_trends.build(connection)
                second = {
                    path.relative_to(docs): path.read_bytes()
                    for path in sorted(docs.rglob("*"))
                    if path.is_file()
                }

        connection.close()
        self.assertEqual(first, second)
        self.assertEqual(len(first), 5)
        self.assertFalse(any("julianday('now')" in statement for statement in traced_sql))
        self.assertTrue(any("julianday('2026-08-16T01:27:11Z')" in statement for statement in traced_sql))


if __name__ == "__main__":
    unittest.main()
