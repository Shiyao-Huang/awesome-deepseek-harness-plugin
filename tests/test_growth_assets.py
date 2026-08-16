"""Public growth-feed and launch-packet projection checks."""

from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_growth_assets.py"
PLUGIN_ID = "deeplugin-8158663eeb5d525203d7"
ATOM = "http://www.w3.org/2005/Atom"


class GrowthAssetProjectionTests(unittest.TestCase):
    def test_cli_ignores_repeat_observations_and_publishes_real_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            database = root / "aggregator.sqlite3"
            registry_path = root / "market-registry.json"
            docs = root / "docs"
            self.write_history_fixture(database)
            registry_path.write_text(
                json.dumps(
                    {
                        "generatedAt": "2026-08-16T04:00:00Z",
                        "plugins": [
                            {
                                "id": PLUGIN_ID,
                                "name": "Example Plugin",
                                "author": "example",
                                "category": "tools",
                                "description": "Second description.",
                                "description_zh": "第二版说明。",
                                "install": {"target": "npm", "spec": "@example/plugin"},
                                "version": "1.1.0",
                                "homepage": "https://github.com/example/plugin",
                                "verified": False,
                                "stars": 3,
                                "tags": ["tools"],
                                "source": {"name": "example/registry", "url": "https://github.com/example/registry"},
                                "sources": [],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--db",
                    str(database),
                    "--registry",
                    str(registry_path),
                    "--docs",
                    str(docs),
                    "--site-url",
                    "https://deeplugin.store",
                ],
                check=True,
                cwd=ROOT,
            )

            new_entries = self.feed_entries(docs / "feeds" / "new.atom.xml")
            updated_entries = self.feed_entries(docs / "feeds" / "updated.atom.xml")
            plugin_entries = self.feed_entries(docs / "plugins" / f"{PLUGIN_ID}.atom.xml")

            self.assertEqual([entry.findtext(f"{{{ATOM}}}updated") for entry in new_entries], ["2026-08-16T00:00:00Z"])
            self.assertEqual([entry.findtext(f"{{{ATOM}}}updated") for entry in updated_entries], ["2026-08-16T04:00:00Z"])
            self.assertEqual(
                [entry.findtext(f"{{{ATOM}}}updated") for entry in plugin_entries],
                ["2026-08-16T04:00:00Z", "2026-08-16T00:00:00Z"],
            )
            self.assertNotIn("2026-08-16T02:00:00Z", (docs / "plugins" / f"{PLUGIN_ID}.atom.xml").read_text(encoding="utf-8"))

            packet = json.loads((docs / "plugins" / f"{PLUGIN_ID}.launch.json").read_text(encoding="utf-8"))
            self.assertEqual(packet["plugin"]["id"], PLUGIN_ID)
            self.assertEqual(packet["install"]["spec"], "@example/plugin")
            self.assertEqual(packet["install"]["command"], "dsh plugin --profile web add @example/plugin")
            self.assertEqual(
                packet["links"]["feed"],
                f"https://deeplugin.store/plugins/{PLUGIN_ID}.atom.xml",
            )
            self.assertIn(f"https://deeplugin.store/plugins/{PLUGIN_ID}.html", packet["posts"]["zh"])
            self.assertIn(f"https://deeplugin.store/plugins/{PLUGIN_ID}.html", packet["posts"]["en"])
            schema = json.loads((docs / "data" / "launch-packet.schema.json").read_text(encoding="utf-8"))
            self.assertEqual(schema["properties"]["plugin"], {"$ref": "#/$defs/plugin"})
            self.assertEqual(schema["properties"]["links"], {"$ref": "#/$defs/links"})
            self.assertFalse(schema["$defs"]["plugin"]["additionalProperties"])
            self.assertEqual(
                schema["$defs"]["install"]["required"],
                ["spec", "command", "agentRequest"],
            )

            first_build = {
                path.relative_to(docs): path.read_bytes()
                for path in docs.rglob("*")
                if path.is_file()
            }
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--db",
                    str(database),
                    "--registry",
                    str(registry_path),
                    "--docs",
                    str(docs),
                    "--site-url",
                    "https://deeplugin.store",
                ],
                check=True,
                cwd=ROOT,
            )
            second_build = {
                path.relative_to(docs): path.read_bytes()
                for path in docs.rglob("*")
                if path.is_file()
            }
            self.assertEqual(second_build, first_build)

    def test_store_build_exposes_global_and_plugin_growth_assets(self) -> None:
        registry = json.loads((ROOT / "docs" / "data" / "market-registry.json").read_text(encoding="utf-8"))
        plugin = registry["plugins"][0]
        plugin_id = plugin["id"]
        market_page = (ROOT / "docs" / "market.html").read_text(encoding="utf-8")
        detail_page = (ROOT / "docs" / "plugins" / f"{plugin_id}.html").read_text(encoding="utf-8")

        self.assertIn('href="feeds/new.atom.xml"', market_page)
        self.assertIn('href="feeds/updated.atom.xml"', market_page)
        self.assertIn(f'href="{plugin_id}.atom.xml"', detail_page)
        self.assertIn(f'href="{plugin_id}.launch.json"', detail_page)
        self.assertIn("Copy launch post · 中文", detail_page)
        self.assertIn("Copy launch post · EN", detail_page)
        self.assertTrue((ROOT / "docs" / "feeds" / "new.atom.xml").is_file())
        self.assertTrue((ROOT / "docs" / "feeds" / "updated.atom.xml").is_file())
        self.assertTrue((ROOT / "docs" / "plugins" / f"{plugin_id}.atom.xml").is_file())
        self.assertTrue((ROOT / "docs" / "plugins" / f"{plugin_id}.launch.json").is_file())

    @staticmethod
    def feed_entries(path: Path) -> list[ET.Element]:
        return ET.parse(path).getroot().findall(f"{{{ATOM}}}entry")

    @staticmethod
    def write_history_fixture(database: Path) -> None:
        with sqlite3.connect(database) as connection:
            connection.executescript(
                """
                CREATE TABLE upstream_repositories(id INTEGER PRIMARY KEY, full_name TEXT NOT NULL);
                CREATE TABLE upstream_entries(id INTEGER PRIMARY KEY, repository_id INTEGER NOT NULL);
                CREATE TABLE upstream_entry_observations(
                    entry_id INTEGER NOT NULL,
                    collection_run_id INTEGER NOT NULL,
                    observed_at TEXT NOT NULL,
                    active INTEGER NOT NULL,
                    entry_name TEXT NOT NULL,
                    entry_url TEXT NOT NULL,
                    owner TEXT,
                    page_url TEXT,
                    entry_kind TEXT NOT NULL,
                    category TEXT,
                    description TEXT,
                    description_i18n TEXT NOT NULL,
                    npm_package TEXT,
                    stars INTEGER,
                    install_hint TEXT,
                    install_spec TEXT,
                    install_target TEXT,
                    plugin_version TEXT,
                    verified INTEGER,
                    tags_json TEXT NOT NULL,
                    registry_source_json TEXT NOT NULL,
                    added_at TEXT,
                    source_path TEXT
                );
                INSERT INTO upstream_repositories VALUES (1, 'example/registry');
                INSERT INTO upstream_entries VALUES (1, 1);
                """
            )
            rows = [
                (1, "2026-08-16T00:00:00Z", "First description.", "1.0.0", 1),
                (2, "2026-08-16T02:00:00Z", "First description.", "1.0.0", 2),
                (3, "2026-08-16T04:00:00Z", "Second description.", "1.1.0", 3),
            ]
            for run_id, observed_at, description, version, stars in rows:
                connection.execute(
                    """
                    INSERT INTO upstream_entry_observations VALUES (
                        1, ?, ?, 1, 'Example Plugin', 'https://github.com/example/plugin',
                        'example', NULL, 'plugin', 'tools', ?, '{}', '@example/plugin', ?,
                        NULL, '@example/plugin', 'npm', ?, 0, '["tools"]', '{}',
                        '2026-08-16', 'registry.json'
                    )
                    """,
                    (run_id, observed_at, description, stars, version),
                )


if __name__ == "__main__":
    unittest.main()
