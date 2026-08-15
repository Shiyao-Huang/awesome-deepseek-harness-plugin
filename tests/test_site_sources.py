from __future__ import annotations

import sqlite3
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_site


class SourcesPageTests(unittest.TestCase):
    def test_source_without_public_homepage_is_plain_text(self) -> None:
        db = sqlite3.connect(":memory:")
        db.row_factory = sqlite3.Row
        db.executescript(
            """
            CREATE TABLE sources(
                id INTEGER PRIMARY KEY,
                platform TEXT,
                display_name TEXT,
                base_url TEXT,
                collection_mode TEXT,
                terms_url TEXT
            );
            CREATE TABLE items(id INTEGER PRIMARY KEY, platform TEXT, last_seen_at TEXT);
            CREATE TABLE observations(
                id INTEGER PRIMARY KEY,
                source_id INTEGER,
                raw_snapshot_id INTEGER,
                collected_at TEXT
            );
            INSERT INTO sources VALUES (1, 'web', 'Open Web', '', 'public page metadata', NULL);
            INSERT INTO items VALUES (1, 'web', '2026-08-15T07:04:51Z');
            INSERT INTO observations VALUES (1, 1, 1, '2026-08-15T07:04:51Z');
            """
        )
        config = {
            "site_name": "dsh store",
            "site_url": "https://deeplugin.store",
            "description": "Test directory",
            "public_database_url": "https://example.com/aggregator.sqlite3",
        }

        page = build_site.render_sources_page(db, config)

        self.assertIn("<td>Open Web<br><code>web</code></td>", page)
        self.assertNotIn('href="" rel="noreferrer">Open Web</a>', page)
        self.assertIn('href="sources.html">Sources</a>', page)
        db.close()


if __name__ == "__main__":
    unittest.main()
