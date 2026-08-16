"""Regression tests for append-only metric history publication."""

from __future__ import annotations

import json
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_append_only.py"
REPAIR = ROOT / "scripts" / "repair_metric_history.py"


class MetricHistoryTests(unittest.TestCase):
    def test_validator_accepts_new_metrics_without_changing_history(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            before = temporary / "before.sqlite3"
            after = temporary / "after.sqlite3"
            self.create_database(before, [(1, 1, "2026-08-16T00:00:00Z", "source-a", 10)])
            self.create_database(after, [
                (1, 1, "2026-08-16T00:00:00Z", "source-a", 10),
                (1, 2, "2026-08-16T02:00:00Z", "source-b", 11),
            ])

            result = self.run_validator(before, after)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), {
                "after_metrics": 2,
                "before_metrics": 1,
                "preserved_metrics": 1,
            })

    def test_validator_rejects_missing_metric_history(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            before = temporary / "before.sqlite3"
            after = temporary / "after.sqlite3"
            self.create_database(before, [
                (1, 1, "2026-08-16T00:00:00Z", "source-a", 10),
                (1, 2, "2026-08-16T02:00:00Z", "source-b", 11),
            ])
            self.create_database(after, [(1, 1, "2026-08-16T00:00:00Z", "source-a", 10)])

            result = self.run_validator(before, after)

            self.assertEqual(result.returncode, 1)
            self.assertIn("missing 1 metric history row(s)", result.stderr)
            self.assertIn("2026-08-16T02:00:00Z", result.stderr)

    def test_validator_rejects_changed_run_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            before = temporary / "before.sqlite3"
            after = temporary / "after.sqlite3"
            self.create_database(before, [(1, 1, "2026-08-16T00:00:00Z", "source-a", 10)])
            self.create_database(after, [(1, 2, "2026-08-16T00:00:00Z", "source-a", 10)])

            result = self.run_validator(before, after)

            self.assertEqual(result.returncode, 1)
            self.assertIn("changed collection run provenance for 1 metric history row(s)", result.stderr)
            self.assertIn("1/v20260816T000000Z -> 2/v20260816T020000Z", result.stderr)

    def test_repair_replays_only_baseline_missing_metrics_from_raw(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            baseline = temporary / "baseline.sqlite3"
            database = temporary / "database.sqlite3"
            self.create_database(
                baseline,
                [(1, 1, "2026-08-16T00:00:00Z", "GitHub repository API via upstream index", 10)],
            )
            self.create_repair_database(database)

            first = self.run_repair(baseline, database)
            second = self.run_repair(baseline, database)

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(json.loads(first.stdout), {"missing_metrics": 1, "restored_metrics": 1})
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(json.loads(second.stdout), {"missing_metrics": 0, "restored_metrics": 0})
            self.assertEqual(self.run_validator(baseline, database).returncode, 0)
            with sqlite3.connect(database) as connection:
                rows = connection.execute(
                    "SELECT collection_run_id, observed_at, metric_source, stars, raw_json FROM metrics"
                ).fetchall()
            self.assertEqual(rows, [(
                1,
                "2026-08-16T00:00:00Z",
                "GitHub repository API via upstream index",
                10,
                '{"metric_source": "GitHub repository API via upstream index", "observed_at": "2026-08-16T00:00:00Z", "stars": 10}',
            )])

    @staticmethod
    def create_database(path: Path, metrics: list[tuple[int, int, str, str, int]]) -> None:
        with sqlite3.connect(path) as connection:
            connection.executescript(
                """
                CREATE TABLE collection_runs(
                    id INTEGER PRIMARY KEY,
                    dataset_version TEXT NOT NULL UNIQUE
                );
                CREATE TABLE items(
                    id INTEGER PRIMARY KEY,
                    canonical_url TEXT NOT NULL UNIQUE
                );
                CREATE TABLE metrics(
                    id INTEGER PRIMARY KEY,
                    item_id INTEGER NOT NULL,
                    collection_run_id INTEGER,
                    observed_at TEXT NOT NULL,
                    metric_source TEXT NOT NULL,
                    stars INTEGER,
                    raw_json TEXT NOT NULL DEFAULT '{}'
                );
                INSERT INTO collection_runs VALUES (1, 'v20260816T000000Z');
                INSERT INTO collection_runs VALUES (2, 'v20260816T020000Z');
                INSERT INTO items VALUES (1, 'https://github.com/owner/plugin');
                """
            )
            connection.executemany(
                "INSERT INTO metrics(item_id, collection_run_id, observed_at, metric_source, stars) "
                "VALUES (?, ?, ?, ?, ?)",
                metrics,
            )

    @staticmethod
    def create_repair_database(path: Path) -> None:
        payload = {
            "collected_at": "2026-08-16T00:00:00Z",
            "observations": [{
                "collected_at": "2026-08-16T00:00:00Z",
                "items": [
                    {
                        "url": "https://github.com/owner/plugin",
                        "metrics": {
                            "stars": 10,
                            "metric_source": "GitHub repository API via upstream index",
                            "observed_at": "2026-08-16T00:00:00Z",
                        },
                    },
                    {
                        "url": "https://github.com/owner/plugin",
                        "metrics": {
                            "stars": 99,
                            "metric_source": "GitHub repository API via upstream index",
                            "observed_at": "2026-08-16T02:00:00Z",
                        },
                    },
                ],
            }],
        }
        with sqlite3.connect(path) as connection:
            connection.executescript(
                """
                CREATE TABLE collection_runs(id INTEGER PRIMARY KEY, dataset_version TEXT NOT NULL UNIQUE);
                CREATE TABLE items(id INTEGER PRIMARY KEY, canonical_url TEXT NOT NULL UNIQUE);
                CREATE TABLE metrics(
                    id INTEGER PRIMARY KEY,
                    item_id INTEGER NOT NULL,
                    collection_run_id INTEGER,
                    observed_at TEXT NOT NULL,
                    likes INTEGER, replies INTEGER, reposts INTEGER, comments INTEGER,
                    bookmarks INTEGER, views INTEGER, points INTEGER, stars INTEGER,
                    forks INTEGER, open_issues INTEGER, subscribers INTEGER, favorites INTEGER,
                    shares INTEGER, coins INTEGER, danmaku INTEGER, upvote_ratio REAL,
                    metric_source TEXT NOT NULL, raw_json TEXT NOT NULL,
                    UNIQUE(item_id, observed_at, metric_source)
                );
                CREATE TABLE raw_snapshots(
                    id INTEGER PRIMARY KEY,
                    collection_run_id INTEGER,
                    raw_path TEXT NOT NULL,
                    collected_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE observations(
                    id INTEGER PRIMARY KEY,
                    raw_snapshot_id INTEGER,
                    collector TEXT NOT NULL
                );
                INSERT INTO collection_runs VALUES (1, 'v20260816T000000Z');
                INSERT INTO collection_runs VALUES (2, 'v20260816T020000Z');
                INSERT INTO items VALUES (1, 'https://github.com/owner/plugin');
                """
            )
            connection.execute(
                "INSERT INTO raw_snapshots VALUES (1, 2, 'data/raw/upstreams/one.json', ?, ?)",
                ("2026-08-16T00:00:00Z", json.dumps(payload)),
            )
            connection.execute(
                "INSERT INTO observations VALUES (1, 1, 'scripts/monitor_sources.py')"
            )

    @staticmethod
    def run_validator(before: Path, after: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(VALIDATOR), "--before", str(before), "--after", str(after)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    @staticmethod
    def run_repair(baseline: Path, database: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(REPAIR), "--baseline", str(baseline), "--database", str(database)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
