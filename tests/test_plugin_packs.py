"""Versioned Plugin Pack persistence checks."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import collect


class PluginPackPersistenceTests(unittest.TestCase):
    def test_init_imports_one_current_pack_version_with_ordered_members(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "aggregator.sqlite3"
            definitions = root / "packs.json"
            definitions.write_text(json.dumps({
                "version": 1,
                "packs": [{
                    "slug": "connected-research",
                    "version": "1.0.0",
                    "active": True,
                    "maintainer": "deeplugin.store",
                    "observedAt": "2026-08-16T08:00:00Z",
                    "datasetVersion": "pack-v20260816T080000Z",
                    "name": {"en": "Connected research", "zh": "联网研究"},
                    "description": {
                        "en": "Search public sources, then synthesize them.",
                        "zh": "先检索公开来源，再综合研究。",
                    },
                    "task": {
                        "en": "Research one question with cited public evidence.",
                        "zh": "用带引用的公开证据研究一个问题。",
                    },
                    "members": [{
                        "pluginId": "deeplugin-aaaaaaaaaaaaaaaaaaaa",
                        "name": "search",
                        "installSpec": "@owner/search",
                        "relationship": "complement",
                        "group": "research-stack",
                        "reason": {"en": "Find sources.", "zh": "查找来源。"},
                    }, {
                        "pluginId": "deeplugin-bbbbbbbbbbbbbbbbbbbb",
                        "name": "research",
                        "installSpec": "github:owner/research",
                        "relationship": "complement",
                        "group": "research-stack",
                        "reason": {"en": "Synthesize evidence.", "zh": "综合证据。"},
                    }],
                }],
            }), encoding="utf-8")

            collect.init_db(database, pack_definitions=definitions)

            with collect.connect(database) as connection:
                state = {
                    "schema": connection.execute("PRAGMA user_version").fetchone()[0],
                    "pack": tuple(connection.execute(
                        "SELECT slug, current_version, active, maintainer, first_observed_at, last_observed_at "
                        "FROM plugin_packs"
                    ).fetchone()),
                    "version": tuple(connection.execute(
                        "SELECT version, dataset_version, name_en, name_zh, source_path "
                        "FROM plugin_pack_versions"
                    ).fetchone()),
                    "members": [tuple(row) for row in connection.execute(
                        "SELECT member_order, deeplugin_id, install_spec, relationship, member_group "
                        "FROM plugin_pack_members ORDER BY member_order"
                    )],
                }

        self.assertEqual(state, {
            "schema": 8,
            "pack": (
                "connected-research",
                "1.0.0",
                1,
                "deeplugin.store",
                "2026-08-16T08:00:00Z",
                "2026-08-16T08:00:00Z",
            ),
            "version": (
                "1.0.0",
                "pack-v20260816T080000Z",
                "Connected research",
                "联网研究",
                str(definitions),
            ),
            "members": [
                (1, "deeplugin-aaaaaaaaaaaaaaaaaaaa", "@owner/search", "complement", "research-stack"),
                (2, "deeplugin-bbbbbbbbbbbbbbbbbbbb", "github:owner/research", "complement", "research-stack"),
            ],
        })

    def test_same_pack_version_rejects_changed_definition_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "aggregator.sqlite3"
            definitions = root / "packs.json"
            pack = {
                "slug": "connected-research",
                "version": "1.0.0",
                "active": True,
                "maintainer": "deeplugin.store",
                "observedAt": "2026-08-16T08:00:00Z",
                "datasetVersion": "pack-v20260816T080000Z",
                "name": {"en": "Connected research", "zh": "联网研究"},
                "description": {"en": "Original description.", "zh": "原始描述。"},
                "task": {"en": "Research one question.", "zh": "研究一个问题。"},
                "members": [{
                    "pluginId": "deeplugin-aaaaaaaaaaaaaaaaaaaa",
                    "name": "search",
                    "installSpec": "@owner/search",
                    "relationship": "required",
                    "group": "research-stack",
                    "reason": {"en": "Find sources.", "zh": "查找来源。"},
                }],
            }
            definitions.write_text(json.dumps({"version": 1, "packs": [pack]}), encoding="utf-8")
            collect.init_db(database, pack_definitions=definitions)
            pack["description"]["en"] = "Changed without a version bump."
            definitions.write_text(json.dumps({"version": 1, "packs": [pack]}), encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "changed without a version bump"):
                collect.init_db(database, pack_definitions=definitions)

    def test_new_version_appends_history_and_explicitly_deactivates_the_pack(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "aggregator.sqlite3"
            definitions = root / "packs.json"
            pack = {
                "slug": "session-memory",
                "version": "1.0.0",
                "active": True,
                "maintainer": "deeplugin.store",
                "observedAt": "2026-08-16T08:00:00Z",
                "datasetVersion": "pack-v20260816T080000Z",
                "name": {"en": "Session memory", "zh": "会话记忆"},
                "description": {"en": "Choose a memory provider.", "zh": "选择一个记忆提供方。"},
                "task": {"en": "Keep session memory.", "zh": "保留会话记忆。"},
                "members": [{
                    "pluginId": "deeplugin-aaaaaaaaaaaaaaaaaaaa",
                    "name": "memory",
                    "installSpec": "@owner/memory",
                    "relationship": "alternative",
                    "group": "memory-provider",
                    "reason": {"en": "One provider option.", "zh": "一个提供方选项。"},
                }],
            }
            definitions.write_text(json.dumps({"version": 1, "packs": [pack]}), encoding="utf-8")
            collect.init_db(database, pack_definitions=definitions)
            pack.update({
                "version": "2.0.0",
                "active": False,
                "observedAt": "2026-08-17T08:00:00Z",
                "datasetVersion": "pack-v20260817T080000Z",
            })
            definitions.write_text(json.dumps({"version": 1, "packs": [pack]}), encoding="utf-8")
            collect.init_db(database, pack_definitions=definitions)
            collect.init_db(database, pack_definitions=definitions)

            with collect.connect(database) as connection:
                state = {
                    "pack": tuple(connection.execute(
                        "SELECT current_version, active, first_observed_at, last_observed_at FROM plugin_packs"
                    ).fetchone()),
                    "versions": [tuple(row) for row in connection.execute(
                        "SELECT version, dataset_version FROM plugin_pack_versions ORDER BY observed_at"
                    )],
                    "member_versions": [row[0] for row in connection.execute(
                        "SELECT pack_version FROM plugin_pack_members ORDER BY pack_version"
                    )],
                }

        self.assertEqual(state, {
            "pack": ("2.0.0", 0, "2026-08-16T08:00:00Z", "2026-08-17T08:00:00Z"),
            "versions": [
                ("1.0.0", "pack-v20260816T080000Z"),
                ("2.0.0", "pack-v20260817T080000Z"),
            ],
            "member_versions": ["1.0.0", "2.0.0"],
        })


if __name__ == "__main__":
    unittest.main()
