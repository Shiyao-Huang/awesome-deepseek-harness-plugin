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
        self.assertIn('href="./sources.html">Sources</a>', page)
        db.close()


class StoreListingEvidenceTests(unittest.TestCase):
    def test_install_command_requires_source_declared_evidence(self) -> None:
        guessed_record = {
            "platform": "github",
            "repo": "owner/dsh-guessed",
            "listings": [],
        }
        declared_record = {
            "platform": "github",
            "repo": "owner/monorepo",
            "listings": [{
                "install_hint": "dsh plugin --profile web add github:owner/monorepo#path:/plugin",
            }],
        }

        self.assertIsNone(build_site.install_command(guessed_record))
        self.assertEqual(
            build_site.install_command(declared_record),
            "dsh plugin --profile web add github:owner/monorepo#path:/plugin",
        )

    def test_listing_evidence_names_source_and_limits_verified_claim(self) -> None:
        record = {
            "listings": [{
                "source_repository": "owner/registry",
                "source_repository_url": "https://github.com/owner/registry",
                "source_path": "registry.json",
                "page_url": "https://registry.example/plugins/example",
                "install_spec": "github:owner/monorepo#path:/plugin",
                "install_target": "git",
                "version": "1.2.3",
                "verified_claim": True,
                "first_seen_at": "2026-08-16T00:00:00Z",
                "last_seen_at": "2026-08-16T02:00:00Z",
                "raw_snapshot_id": 7,
            }],
        }

        page = build_site.render_listing_evidence(record)

        self.assertIn("owner/registry · registry.json", page)
        self.assertIn("github:owner/monorepo#path:/plugin", page)
        self.assertIn("source claims verified", page)
        self.assertIn("not a security, compatibility, quality, or official-endorsement claim", page)


class MarketAccessPageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = {
            "site_name": "dsh store",
            "site_url": "https://deeplugin.store",
            "description": "Test directory",
            "public_database_url": "https://example.com/aggregator.sqlite3",
        }

    def test_home_links_registry_schema_guides_and_market_plugin(self) -> None:
        page = build_site.render_home([], "v-test", "2026-08-16T00:00:00Z", self.config, [], [])

        self.assertIn('href="register.html"', page)
        self.assertIn('href="register-agent.html"', page)
        self.assertIn('href="data/market-registry.json"', page)
        self.assertIn('href="data/market-registry.schema.json"', page)
        self.assertIn("github:Shiyao-Huang/awesome-deepseek-harness-plugin#path:/plugin", page)
        self.assertIn("Every install requires explicit confirmation", page)

    def test_registration_pages_link_one_normative_guide(self) -> None:
        human = build_site.render_register_page(self.config)
        agent = build_site.render_register_agent_page(self.config)

        self.assertIn('class="brand" href="./"', human)
        self.assertIn('class="breadcrumbs"><a href="./"', human)
        self.assertIn("docs/register.md", human)
        self.assertIn("market-registry.schema.json", human)
        self.assertIn('class="brand" href="./"', agent)
        self.assertIn('class="breadcrumbs"><a href="./"', agent)
        self.assertIn("docs/register.md", agent)
        self.assertIn("Registration never authorizes installation", agent)


if __name__ == "__main__":
    unittest.main()
