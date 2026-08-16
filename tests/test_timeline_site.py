"""Timeline analytics projection checks for the generated store."""

from __future__ import annotations

import json
import re
import sqlite3
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_site


CONFIG = {
    "site_name": "dsh store",
    "site_url": "https://deeplugin.store",
    "description": "Test directory",
    "public_database_url": "https://example.com/aggregator.sqlite3",
}


def timeline_db(record_count: int = 125) -> sqlite3.Connection:
    """Create the public tables consumed by the Timeline projection."""

    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.executescript(
        """
        CREATE TABLE collection_runs (
            id INTEGER PRIMARY KEY,
            dataset_version TEXT,
            started_at TEXT,
            finished_at TEXT,
            trigger TEXT,
            status TEXT
        );
        CREATE TABLE items (
            id INTEGER PRIMARY KEY,
            platform TEXT,
            item_type TEXT,
            title TEXT,
            author TEXT,
            category TEXT,
            published_at TEXT,
            published_label TEXT,
            first_seen_at TEXT
        );
        CREATE TABLE index_records (
            id TEXT PRIMARY KEY,
            item_id INTEGER,
            rank INTEGER
        );
        CREATE TABLE metrics (
            id INTEGER PRIMARY KEY,
            item_id INTEGER,
            observed_at TEXT,
            likes INTEGER,
            replies INTEGER,
            comments INTEGER,
            views INTEGER,
            points INTEGER,
            stars INTEGER,
            forks INTEGER,
            favorites INTEGER,
            shares INTEGER,
            coins INTEGER,
            danmaku INTEGER,
            metric_source TEXT
        );
        INSERT INTO collection_runs VALUES (
            1, 'v-test', '2026-08-16T10:00:00Z', '2026-08-16T10:05:00Z',
            'manual', 'success'
        );
        """
    )
    for item_id in range(1, record_count + 1):
        db.execute(
            "INSERT INTO items VALUES (?, 'github', 'repository', ?, ?, ?, ?, NULL, ?)",
            (
                item_id,
                f"Plugin {item_id:03d}",
                f"Author {item_id:03d}",
                "core-and-ecosystem",
                f"2026-08-{1 + item_id % 15:02d}T08:00:00Z",
                "2026-08-01T08:00:00Z",
            ),
        )
        db.execute(
            "INSERT INTO index_records VALUES (?, ?, ?)",
            (f"id-{item_id}", item_id, item_id),
        )
    db.commit()
    return db


def timeline_payload(page: str) -> dict[str, object]:
    """Read the public JSON payload embedded for Timeline interactions."""

    match = re.search(
        r'<script type="application/json" id="timeline-data">(.*?)</script>',
        page,
    )
    if match is None:
        raise AssertionError("Timeline data payload is missing")
    return json.loads(match.group(1))


class TimelinePageTests(unittest.TestCase):
    def test_page_exposes_analytics_controls_without_rendering_every_row(self) -> None:
        db = timeline_db()

        page = build_site.render_timeline_page(db, "v-test", CONFIG)

        self.assertIn('data-page="timeline"', page)
        self.assertIn('data-timeline-sort="time"', page)
        self.assertIn('data-timeline-sort="influence"', page)
        self.assertIn('data-timeline-sort="trend"', page)
        self.assertIn('id="timeline-search"', page)
        self.assertIn('id="timeline-source"', page)
        self.assertIn('id="timeline-category"', page)
        self.assertIn('id="timeline-window"', page)
        self.assertIn('id="timeline-trending-only"', page)
        self.assertIn('<th>Rank</th>', page)
        self.assertEqual(page.count('class="timeline-row"'), 100)
        self.assertIn('<script src="assets/timeline.js" defer></script>', page)
        db.close()

    def test_trend_uses_two_snapshots_from_one_metric_source(self) -> None:
        db = timeline_db(2)
        db.executemany(
            """
            INSERT INTO metrics(
                item_id, observed_at, likes, stars, metric_source
            ) VALUES (?, ?, ?, ?, ?)
            """,
            [
                (1, "2026-08-16T06:00:00Z", 50, 10, "GitHub repository API"),
                (1, "2026-08-16T08:00:00Z", 100, 15, "GitHub repository API"),
                (1, "2026-08-16T09:00:00Z", None, 999, "Unpaired source"),
                (2, "2026-08-16T08:30:00Z", None, 7, "GitHub repository API"),
            ],
        )
        db.commit()

        page = build_site.render_timeline_page(db, "v-test", CONFIG)
        records = timeline_payload(page)["records"]
        assert isinstance(records, list)
        by_id = {record["id"]: record for record in records}

        self.assertEqual(
            by_id["id-1"]["trend"],
            {
                "hasEvidence": True,
                "metric": "stars",
                "metricLabel": "★",
                "current": 15,
                "previous": 10,
                "delta": 5,
                "percent": 50.0,
                "from": "2026-08-16T06:00:00Z",
                "to": "2026-08-16T08:00:00Z",
                "elapsedHours": 2.0,
                "source": "GitHub repository API",
            },
        )
        self.assertEqual(by_id["id-2"]["trend"], {"hasEvidence": False})
        self.assertIn("★ 15", page)
        self.assertIn("+5 · +50.0% · 2h", page)
        db.close()

    def test_time_window_reference_ignores_a_failed_collection_run(self) -> None:
        db = timeline_db(1)
        db.execute(
            """
            INSERT INTO collection_runs VALUES (
                2, 'v-failed', '2026-08-16T12:00:00Z', '2026-08-16T12:05:00Z',
                'scheduled', 'failed'
            )
            """
        )
        db.commit()

        page = build_site.render_timeline_page(db, "v-test", CONFIG)

        self.assertEqual(
            timeline_payload(page)["referenceTime"],
            "2026-08-16T10:05:00Z",
        )
        db.close()


if __name__ == "__main__":
    unittest.main()
