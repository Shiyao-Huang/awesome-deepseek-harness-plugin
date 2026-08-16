from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_market_registry
import collect
import monitor_sources


class MarketRegistryBuilderTests(unittest.TestCase):
    def test_deduplicates_safe_specs_with_stable_ids_and_source_attribution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "registry.sqlite3"
            collect.init_db(database, pack_definitions=Path(directory) / "missing-packs.json")
            with collect.connect(database) as connection:
                connection.execute(
                    "INSERT INTO collection_runs(id, dataset_version, started_at, finished_at, trigger, status) "
                    "VALUES (1, 'v20260816T020000Z', '2026-08-16T02:00:00Z', '2026-08-16T02:01:00Z', 'source-monitor', 'succeeded')"
                )
                connection.execute(
                    "INSERT INTO raw_snapshots(id, collection_run_id, raw_sha256, raw_path, collected_at, byte_size, payload_json) "
                    "VALUES (1, 1, 'raw-1', 'data/raw/upstreams/one.json', '2026-08-16T02:00:00Z', 2, '{}')"
                )
                for descriptor in (
                    self.descriptor(
                        "catalog-a/registry",
                        "https://github.com/catalog-a/registry",
                        [{
                            "registry_id": "plugin-a",
                            "name": "Plugin A",
                            "owner": "Owner",
                            "url": "https://github.com/Owner/Plugin",
                            "category": "tools",
                            "description": "Search files.",
                            "description_i18n": {"en": "Search files.", "zh": "搜索文件。"},
                            "install_spec": "github:Owner/Plugin",
                            "install_target": "git",
                            "stars": 7,
                            "tags": ["search"],
                            "source_path": "registry.json",
                            "entry_kind": "plugin-candidate",
                        }],
                    ),
                    self.descriptor(
                        "catalog-b/registry",
                        "https://github.com/catalog-b/registry",
                        [{
                            "registry_id": "different-id",
                            "name": "Plugin A Verified",
                            "owner": "Owner",
                            "url": "https://github.com/Owner/Plugin",
                            "category": "tools",
                            "description": "Verified search plugin.",
                            "install_spec": "github:owner/plugin",
                            "install_target": "git",
                            "version": "1.2.3",
                            "verified": True,
                            "stars": 11,
                            "tags": ["files"],
                            "source_path": "plugins.json",
                            "entry_kind": "plugin-candidate",
                        }, {
                            "registry_id": "unsafe",
                            "name": "Unsafe",
                            "owner": "Owner",
                            "url": "https://github.com/Owner/Unsafe",
                            "category": "tools",
                            "description": "Must not be published.",
                            "install_spec": "github:owner/unsafe;touch /tmp/x",
                            "install_target": "git",
                            "source_path": "plugins.json",
                            "entry_kind": "plugin-candidate",
                        }],
                    ),
                ):
                    monitor_sources.record_upstream_repositories(
                        connection, {"repositories": [descriptor]}, 1
                    )

                registry = build_market_registry.build_registry(connection)

        self.assertEqual(registry["version"], 3)
        self.assertEqual(registry["updated"], "2026-08-16")
        self.assertEqual(registry["count"], 1)
        self.assertEqual(registry["verifiedCount"], 1)
        plugin = registry["plugins"][0]
        self.assertEqual(plugin["id"], "deeplugin-d3c019855ffb09041d24")
        self.assertEqual(plugin["install"], {"target": "git", "spec": "github:owner/plugin"})
        self.assertEqual(plugin["version"], "1.2.3")
        self.assertIs(plugin["verified"], True)
        self.assertEqual(plugin["stars"], 11)
        self.assertEqual(plugin["tags"], ["files", "search", "tools"])
        self.assertEqual(
            [source["registry"] for source in plugin["sources"]],
            ["catalog-a/registry", "catalog-b/registry"],
        )
        self.assertTrue(all("verified" in source for source in plugin["sources"]))

    def test_writes_identical_registry_and_schema_to_index_and_docs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "registry.sqlite3"
            collect.init_db(database, pack_definitions=root / "missing-packs.json")
            with collect.connect(database) as connection:
                connection.execute(
                    "INSERT INTO collection_runs(id, dataset_version, started_at, finished_at, trigger, status) "
                    "VALUES (1, 'v20260816T020000Z', '2026-08-16T02:00:00Z', '2026-08-16T02:01:00Z', 'source-monitor', 'succeeded')"
                )
                connection.execute(
                    "INSERT INTO raw_snapshots(id, collection_run_id, raw_sha256, raw_path, collected_at, byte_size, payload_json) "
                    "VALUES (1, 1, 'raw-1', 'data/raw/upstreams/one.json', '2026-08-16T02:00:00Z', 2, '{}')"
                )
                monitor_sources.record_upstream_repositories(
                    connection,
                    {"repositories": [self.descriptor(
                        "catalog/registry",
                        "https://github.com/catalog/registry",
                        [{
                            "name": "Example",
                            "owner": "owner",
                            "url": "https://github.com/owner/example",
                            "category": "tools",
                            "description": "Example plugin.",
                            "install_spec": "@owner/example",
                            "install_target": "npm",
                            "source_path": "registry.json",
                            "entry_kind": "plugin-candidate",
                        }],
                    )]},
                    1,
                )

            index_registry = root / "index" / "market-registry.json"
            docs_registry = root / "docs" / "data" / "market-registry.json"
            plugin_registry = root / "plugin" / "data" / "market-registry.json"
            index_schema = root / "index" / "market-registry.schema.json"
            docs_schema = root / "docs" / "data" / "market-registry.schema.json"
            plugin_schema = root / "plugin" / "data" / "market-registry.schema.json"
            build_market_registry.write_outputs(
                database,
                index_registry=index_registry,
                docs_registry=docs_registry,
                plugin_registry=plugin_registry,
                index_schema=index_schema,
                docs_schema=docs_schema,
                plugin_schema=plugin_schema,
            )

            self.assertEqual(index_registry.read_bytes(), docs_registry.read_bytes())
            self.assertEqual(index_registry.read_bytes(), plugin_registry.read_bytes())
            self.assertEqual(index_schema.read_bytes(), docs_schema.read_bytes())
            self.assertEqual(index_schema.read_bytes(), plugin_schema.read_bytes())
            registry = json.loads(index_registry.read_text(encoding="utf-8"))
            schema = json.loads(index_schema.read_text(encoding="utf-8"))
            self.assertEqual(registry["count"], len(registry["plugins"]))
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertIn("install", schema["$defs"]["plugin"]["required"])

    def test_projects_pack_members_with_listing_and_raw_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "registry.sqlite3"
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
                    "description": {"en": "Search and synthesize.", "zh": "检索并综合。"},
                    "task": {"en": "Research with citations.", "zh": "用引用开展研究。"},
                    "members": [{
                        "pluginId": "deeplugin-bd33bf840601b8e894cd",
                        "name": "search",
                        "installSpec": "@owner/search",
                        "relationship": "complement",
                        "group": "research-stack",
                        "reason": {"en": "Find sources.", "zh": "查找来源。"},
                    }, {
                        "pluginId": "deeplugin-f4610fb13b8ef0ccd764",
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
                connection.execute(
                    "INSERT INTO collection_runs(id, dataset_version, started_at, finished_at, trigger, status) "
                    "VALUES (1, 'v20260816T020000Z', '2026-08-16T02:00:00Z', '2026-08-16T02:01:00Z', 'source-monitor', 'succeeded')"
                )
                connection.execute(
                    "INSERT INTO raw_snapshots(id, collection_run_id, raw_sha256, raw_path, collected_at, byte_size, payload_json) "
                    "VALUES (1, 1, 'raw-1', 'data/raw/upstreams/one.json', '2026-08-16T02:00:00Z', 2, '{}')"
                )
                monitor_sources.record_upstream_repositories(
                    connection,
                    {"repositories": [self.descriptor(
                        "catalog/registry",
                        "https://github.com/catalog/registry",
                        [{
                            "registry_id": "search-listing",
                            "name": "search",
                            "owner": "owner",
                            "url": "https://github.com/owner/search",
                            "category": "tools",
                            "description": "Find sources.",
                            "install_spec": "@owner/search",
                            "install_target": "npm",
                            "source_path": "registry.json",
                            "entry_kind": "plugin-candidate",
                        }, {
                            "registry_id": "research-listing",
                            "name": "research",
                            "owner": "owner",
                            "url": "https://github.com/owner/research",
                            "category": "tools",
                            "description": "Synthesize evidence.",
                            "install_spec": "github:owner/research",
                            "install_target": "git",
                            "version": "2.0.0",
                            "verified": True,
                            "source_path": "registry.json",
                            "entry_kind": "plugin-candidate",
                        }],
                    )]},
                    1,
                )

                registry = build_market_registry.build_registry(connection)

        self.assertEqual(registry["packCount"], 1)
        pack = registry["packs"][0]
        self.assertEqual(pack["id"], "deeplugin-pack-1a44f493cd18411366b2")
        self.assertIs(pack["installable"], True)
        self.assertEqual(pack["missingMembers"], [])
        self.assertEqual(pack["missingVersions"], ["deeplugin-bd33bf840601b8e894cd"])
        self.assertEqual(
            [(member["pluginId"], member["install"]["spec"]) for member in pack["members"]],
            [
                ("deeplugin-bd33bf840601b8e894cd", "@owner/search"),
                ("deeplugin-f4610fb13b8ef0ccd764", "github:owner/research"),
            ],
        )
        self.assertEqual(pack["members"][0]["provenance"], [{
            "registry": "catalog/registry",
            "registryUrl": "https://github.com/catalog/registry",
            "sourceRef": "registry.json",
            "listingId": "search-listing",
            "rawSnapshotId": 1,
            "observedAt": "2026-08-16T02:00:00Z",
            "spec": "@owner/search",
        }])

    @staticmethod
    def descriptor(
        full_name: str,
        source_url: str,
        entries: list[dict[str, object]],
    ) -> dict[str, object]:
        source_refs = sorted({str(entry["source_path"]) for entry in entries})
        return {
            "full_name": full_name,
            "html_url": source_url,
            "default_branch": "main",
            "last_checked_at": "2026-08-16T02:00:00Z",
            "entry_sources": [
                {
                    "source_ref": source_ref,
                    "kind": "registry",
                    "status": "ok",
                    "entry_count": sum(entry["source_path"] == source_ref for entry in entries),
                }
                for source_ref in source_refs
            ],
            "entries": entries,
        }


if __name__ == "__main__":
    unittest.main()
