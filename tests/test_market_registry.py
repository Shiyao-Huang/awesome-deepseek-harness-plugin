from __future__ import annotations

import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import collect
import build_value_matrix
import import_ego_source
import monitor_sources


class StructuredRegistryTests(unittest.TestCase):
    def test_source_config_collects_live_v1_and_v2_registries(self) -> None:
        config = json.loads((ROOT / "config" / "sources.json").read_text(encoding="utf-8"))
        sources = {source["repo"]: source for source in config["github_repositories"]}

        self.assertEqual(
            sources["awesome-dsh-plugin/awesome-dsh-plugin"]["registry_url"],
            "https://awesome-dsh-plugin.com/plugins.json",
        )
        self.assertIn("data/registry-snapshot.json", sources["dsh-market/dsh-market"]["files"])
        self.assertIn("registry.json", sources["zoahdev/dsh-subscribe"]["files"])
        self.assertIn(
            "registry/plugins.json",
            sources["Shiyao-Huang/awesome-deepseek-harness-plugin"]["files"],
        )

    def test_local_submission_registry_is_valid_contract_v2(self) -> None:
        path = ROOT / "registry" / "plugins.json"
        value = json.loads(path.read_text(encoding="utf-8"))

        snapshot = monitor_sources.registry_snapshot(value, "registry/plugins.json")
        entries = monitor_sources.structured_entries(value, "registry/plugins.json")

        self.assertEqual(snapshot["status"], "ok")
        self.assertEqual(snapshot["format_version"], 2)
        self.assertEqual(snapshot["actual_count"], value["count"])
        self.assertEqual(len(entries), 1)
        self.assertEqual(
            entries[0]["install_spec"],
            "github:shiyao-huang/awesome-deepseek-harness-plugin#path:/plugin",
        )
        self.assertIs(entries[0]["verified"], False)

    def test_preserves_install_metadata_and_bilingual_descriptions(self) -> None:
        registry = {
            "plugins": [{
                "name": "dsh-example",
                "owner": "owner",
                "url": "https://github.com/owner/dsh-example",
                "page": "https://example.test/p/owner/dsh-example/",
                "category": "tools",
                "description": {"en": "Search files.", "zh": "搜索文件。"},
                "npm": "@owner/dsh-example",
                "stars": 17,
                "install": "dsh plugin --profile web add @owner/dsh-example",
                "added": "2026-08-16",
            }],
        }

        entry = monitor_sources.structured_entries(registry, "plugins.json")[0]

        self.assertEqual(entry["description"], "搜索文件。")
        self.assertEqual(entry["description_i18n"], {"en": "Search files.", "zh": "搜索文件。"})
        self.assertEqual(entry["page"], "https://example.test/p/owner/dsh-example/")
        self.assertEqual(entry["npm"], "@owner/dsh-example")
        self.assertEqual(entry["stars"], 17)
        self.assertEqual(entry["install"], "dsh plugin --profile web add @owner/dsh-example")
        self.assertEqual(entry["added"], "2026-08-16")

    def test_normalizes_v2_install_contract_without_guessing_from_homepage(self) -> None:
        registry = {
            "version": 2,
            "plugins": [{
                "id": "dsh-example",
                "name": "Example",
                "author": "owner",
                "homepage": "https://github.com/owner/monorepo",
                "category": "tools",
                "description": "Search files.",
                "description_zh": "搜索文件。",
                "install": {"target": "git", "spec": "github:owner/monorepo#path:/plugin"},
                "version": "1.2.3",
                "verified": True,
                "stars": 17,
                "tags": ["search", "files"],
                "source": {"name": "owner", "url": "https://github.com/owner/registry"},
            }],
        }

        entry = monitor_sources.structured_entries(registry, "registry.json")[0]

        self.assertEqual(entry["registry_id"], "dsh-example")
        self.assertEqual(entry["url"], "https://github.com/owner/monorepo")
        self.assertEqual(entry["owner"], "owner")
        self.assertEqual(entry["description"], "搜索文件。")
        self.assertEqual(entry["description_i18n"], {"en": "Search files.", "zh": "搜索文件。"})
        self.assertEqual(entry["install_spec"], "github:owner/monorepo#path:/plugin")
        self.assertEqual(entry["install_target"], "git")
        self.assertEqual(entry["install"], "dsh plugin --profile web add github:owner/monorepo#path:/plugin")
        self.assertEqual(entry["version"], "1.2.3")
        self.assertIs(entry["verified"], True)
        self.assertEqual(entry["tags"], ["search", "files"])
        self.assertEqual(entry["registry_source"], {"name": "owner", "url": "https://github.com/owner/registry"})

    def test_structured_listing_wins_over_duplicate_readme_link(self) -> None:
        registry_url = "https://registry.example/plugins.json"
        registry = {
            "count": 1,
            "plugins": [{
                "name": "dsh-example",
                "owner": "owner",
                "url": "https://github.com/owner/dsh-example",
                "category": "tools",
                "description": {"en": "Search files.", "zh": "搜索文件。"},
                "install": "dsh plugin --profile web add @owner/dsh-example",
            }],
        }

        def api_json(url: str, _token: str | None) -> dict[str, object]:
            if "/git/trees/" in url:
                return {"tree": [{"path": "README.md", "sha": "readme", "type": "blob"}]}
            if url.endswith("/repos/owner/dsh-example"):
                return {"full_name": "owner/dsh-example", "html_url": "https://github.com/owner/dsh-example", "default_branch": "main"}
            return {"full_name": "owner/registry", "html_url": "https://github.com/owner/registry", "default_branch": "main"}

        def raw_text(url: str, _token: str | None) -> str:
            if url == registry_url:
                return json.dumps(registry, ensure_ascii=False)
            return "## tools\n- [dsh-example](https://github.com/owner/dsh-example) - README text"

        with (
            mock.patch.object(monitor_sources, "api_json", side_effect=api_json),
            mock.patch.object(monitor_sources, "raw_text", side_effect=raw_text),
        ):
            descriptor = monitor_sources.monitor_repository(
                "owner/registry", ["README.md"], None, "2026-08-16T00:00:00Z", 0, registry_url=registry_url
            )

        self.assertEqual(len(descriptor["entries"]), 1)
        self.assertEqual(descriptor["entries"][0]["description"], "搜索文件。")
        self.assertEqual(descriptor["entries"][0]["install_spec"], "@owner/dsh-example")
        self.assertEqual(descriptor["entry_sources"], [
            {"source_ref": "README.md", "kind": "markdown", "status": "ok", "entry_count": 1},
            {"source_ref": registry_url, "kind": "registry", "status": "ok", "entry_count": 1},
        ])

    def test_invalid_registry_is_retained_as_raw_without_importing_listings(self) -> None:
        registry_url = "https://registry.example/plugins.json"
        raw_registry = json.dumps({
            "version": 2,
            "count": 2,
            "plugins": [{
                "id": "dsh-example",
                "name": "Example",
                "author": "owner",
                "homepage": "https://github.com/owner/dsh-example",
                "install": {"target": "git", "spec": "github:owner/dsh-example"},
                "verified": True,
            }],
        })

        def api_json(url: str, _token: str | None) -> dict[str, object]:
            if "/git/trees/" in url:
                return {"tree": []}
            return {"full_name": "owner/registry", "html_url": "https://github.com/owner/registry", "default_branch": "main"}

        with (
            mock.patch.object(monitor_sources, "api_json", side_effect=api_json),
            mock.patch.object(monitor_sources, "raw_text", return_value=raw_registry),
        ):
            descriptor = monitor_sources.monitor_repository(
                "owner/registry", [], None, "2026-08-16T00:00:00Z", 0, registry_url=registry_url
            )

        self.assertEqual(descriptor["external_files"], {registry_url: raw_registry})
        self.assertEqual(descriptor["entries"], [])
        self.assertEqual(descriptor["entry_sources"][0]["status"], "invalid")
        self.assertEqual(descriptor["registries"][0]["status"], "invalid")
        self.assertIn("declared count 2 does not match 1 plugins", descriptor["registries"][0]["error"])
        self.assertIn("verified listing dsh-example has no version", descriptor["registries"][0]["error"])

    def test_large_registry_is_preserved_completely_in_raw_descriptor(self) -> None:
        registry_url = "https://registry.example/plugins.json"
        raw_registry = json.dumps({
            "count": 1,
            "plugins": [{
                "name": "dsh-example",
                "owner": "owner",
                "url": "https://github.com/owner/dsh-example",
                "description": {"en": "x" * 410_000},
                "install": "dsh plugin --profile web add github:owner/dsh-example",
            }],
        })

        def api_json(url: str, _token: str | None) -> dict[str, object]:
            if "/git/trees/" in url:
                return {"tree": []}
            if url.endswith("/repos/owner/dsh-example"):
                return {"full_name": "owner/dsh-example", "html_url": "https://github.com/owner/dsh-example", "default_branch": "main"}
            return {"full_name": "owner/registry", "html_url": "https://github.com/owner/registry", "default_branch": "main"}

        with (
            mock.patch.object(monitor_sources, "api_json", side_effect=api_json),
            mock.patch.object(monitor_sources, "request_bytes", return_value=raw_registry.encode("utf-8")),
        ):
            descriptor = monitor_sources.monitor_repository(
                "owner/registry", [], None, "2026-08-16T00:00:00Z", 0, registry_url=registry_url
            )

        self.assertGreater(len(raw_registry), 400_000)
        self.assertEqual(descriptor["external_files"][registry_url], raw_registry)
        self.assertEqual(descriptor["registries"][0]["status"], "ok")
        self.assertEqual(len(descriptor["entries"]), 1)

    def test_monitor_repository_keeps_external_registry_raw_and_metadata(self) -> None:
        registry_url = "https://registry.example/plugins.json"
        registry = {
            "name": "DSH plugins",
            "url": "https://registry.example",
            "source": "https://github.com/owner/registry",
            "updated": "2026-08-16",
            "count": 1,
            "categories": {"tools": {"en": "Tools", "zh": "工具"}},
            "plugins": [{
                "name": "dsh-example",
                "owner": "owner",
                "url": "https://github.com/owner/dsh-example",
                "category": "tools",
                "description": {"en": "Search files.", "zh": "搜索文件。"},
                "npm": None,
                "stars": 17,
                "install": "dsh plugin --profile web add github:owner/dsh-example",
                "added": "2026-08-16",
            }],
        }
        raw_registry = json.dumps(registry, ensure_ascii=False)

        def api_json(url: str, _token: str | None) -> dict[str, object]:
            if "/git/trees/" in url:
                return {"tree": []}
            if url.endswith("/repos/owner/dsh-example"):
                return {
                    "full_name": "owner/dsh-example",
                    "html_url": "https://github.com/owner/dsh-example",
                    "default_branch": "main",
                }
            return {
                "full_name": "owner/registry",
                "html_url": "https://github.com/owner/registry",
                "default_branch": "main",
            }

        with (
            mock.patch.object(monitor_sources, "api_json", side_effect=api_json),
            mock.patch.object(monitor_sources, "raw_text", return_value=raw_registry),
        ):
            descriptor = monitor_sources.monitor_repository(
                "owner/registry",
                [],
                None,
                "2026-08-16T00:00:00Z",
                0,
                registry_url=registry_url,
            )

        self.assertEqual(descriptor["entry_count"], 1)
        self.assertEqual(descriptor["external_files"], {registry_url: raw_registry})
        self.assertEqual(descriptor["registry_metadata"], {
            "name": "DSH plugins",
            "url": "https://registry.example",
            "source": "https://github.com/owner/registry",
            "updated": "2026-08-16",
            "count": 1,
            "categories": {"tools": {"en": "Tools", "zh": "工具"}},
        })

    def test_external_registry_request_does_not_receive_github_token(self) -> None:
        captured_requests: list[object] = []

        class Response:
            def __enter__(self) -> Response:
                return self

            def __exit__(self, *_args: object) -> None:
                return None

            @staticmethod
            def read() -> bytes:
                return b"{}"

        def fake_urlopen(request: object, **_kwargs: object) -> Response:
            captured_requests.append(request)
            return Response()

        with mock.patch.object(monitor_sources, "urlopen", side_effect=fake_urlopen):
            monitor_sources.request_bytes("https://registry.example/plugins.json", "github-secret")

        self.assertEqual(len(captured_requests), 1)
        self.assertIsNone(captured_requests[0].get_header("Authorization"))

    def test_non_object_registry_is_invalid_without_losing_raw(self) -> None:
        registry_url = "https://registry.example/plugins.json"

        def api_json(url: str, _token: str | None) -> dict[str, object]:
            if "/git/trees/" in url:
                return {"tree": []}
            return {"full_name": "owner/registry", "html_url": "https://github.com/owner/registry", "default_branch": "main"}

        with (
            mock.patch.object(monitor_sources, "api_json", side_effect=api_json),
            mock.patch.object(monitor_sources, "raw_text", return_value="[]"),
        ):
            descriptor = monitor_sources.monitor_repository(
                "owner/registry", [], None, "2026-08-16T00:00:00Z", 0, registry_url=registry_url
            )

        self.assertEqual(descriptor["external_files"], {registry_url: "[]"})
        self.assertEqual(descriptor["entries"], [])
        self.assertEqual(descriptor["registries"][0]["status"], "invalid")
        self.assertEqual(descriptor["registries"][0]["error"], "registry root is not an object")

    def test_missing_configured_registry_is_recorded_as_authoritative_absence(self) -> None:
        def api_json(url: str, _token: str | None) -> dict[str, object]:
            if "/git/trees/" in url:
                return {"tree": [{"path": "README.md", "sha": "readme", "type": "blob"}]}
            return {"full_name": "owner/registry", "html_url": "https://github.com/owner/registry", "default_branch": "main"}

        with (
            mock.patch.object(monitor_sources, "api_json", side_effect=api_json),
            mock.patch.object(monitor_sources, "raw_text", return_value="# Empty registry"),
        ):
            descriptor = monitor_sources.monitor_repository(
                "owner/registry", ["registry.json"], None, "2026-08-16T00:00:00Z", 0
            )

        self.assertIn(
            {"source_ref": "registry.json", "kind": "registry", "status": "missing", "entry_count": 0},
            descriptor["entry_sources"],
        )
        self.assertEqual(descriptor["registries"][0]["status"], "missing")


class RegistryPersistenceTests(unittest.TestCase):
    def test_reconcile_restores_native_item_without_deleting_listing_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "registry.sqlite3"
            native_raw = Path(directory) / "native.json"
            listing_raw = Path(directory) / "listing.json"
            collect.init_db(database)
            native_payload = {
                "collected_at": "2026-08-16T00:00:00Z",
                "collector": "scripts/collect.py",
                "observations": [{
                    "platform": "github",
                    "query": "owner/existing",
                    "source_url": "https://github.com/owner/existing",
                    "collected_at": "2026-08-16T00:00:00Z",
                    "collector": "scripts/collect.py",
                    "method": "GitHub REST API",
                    "status": "ok",
                    "result_count": 1,
                    "notes": "Native fixture.",
                    "items": [{
                        "platform": "github",
                        "external_id": "owner/existing",
                        "url": "https://github.com/owner/existing",
                        "item_type": "repository",
                        "title": "owner/existing",
                        "author": "owner",
                        "content_text": "Native GitHub description.",
                        "category": "repository",
                        "relevance": "direct",
                        "media_kind": "none",
                        "metrics": {
                            "stars": 900,
                            "metric_source": "github REST API",
                            "observed_at": "2026-08-16T00:00:00Z",
                        },
                    }],
                }],
            }
            collect.dump_json(native_raw, native_payload)
            with collect.connect(database) as connection:
                connection.execute(
                    "INSERT INTO collection_runs(id, dataset_version, started_at, trigger, status) "
                    "VALUES (1, 'v20260816T000000Z', '2026-08-16T00:00:00Z', 'scheduled', 'succeeded')"
                )
                collect.import_payload(connection, native_payload, 1, native_raw)
                connection.execute(
                    "INSERT INTO collection_runs(id, dataset_version, started_at, trigger, status) "
                    "VALUES (2, 'v20260816T020000Z', '2026-08-16T02:00:00Z', 'source-monitor', 'succeeded')"
                )
                descriptor = self.descriptor("2026-08-16T02:00:00Z")
                listing = descriptor["entries"][0]
                listing["url"] = "https://github.com/owner/existing"
                listing["name"] = "官方核心 · owner/existing"
                listing["metrics"] = {
                    "stars": 7,
                    "metric_source": "GitHub repository API via upstream index",
                    "observed_at": "2026-08-16T02:00:00Z",
                }
                listing_payload = {
                    "collected_at": "2026-08-16T02:00:00Z",
                    "collector": "scripts/monitor_sources.py",
                    "repositories": [descriptor],
                    "observations": [{
                        "platform": "github",
                        "query": "upstream:owner/registry",
                        "source_url": "https://github.com/owner/registry",
                        "collected_at": "2026-08-16T02:00:00Z",
                        "collector": "scripts/monitor_sources.py",
                        "method": "registry fixture",
                        "status": "ok",
                        "result_count": 1,
                        "notes": "Legacy collision fixture.",
                        "items": [monitor_sources.item_for_entry(
                            listing, "2026-08-16T02:00:00Z", "owner/registry"
                        )],
                    }],
                }
                collect.dump_json(listing_raw, listing_payload)
                collect.import_payload(connection, listing_payload, 2, listing_raw)
                listing_snapshot_id = int(connection.execute(
                    "SELECT id FROM raw_snapshots WHERE raw_sha256 = ?",
                    (collect.sha256_file(listing_raw),),
                ).fetchone()[0])
                monitor_sources.record_upstream_repositories(
                    connection, listing_payload, listing_snapshot_id
                )
                self.assertEqual(
                    connection.execute("SELECT title FROM items").fetchone()[0],
                    "官方核心 · owner/existing",
                )

                report = monitor_sources.reconcile_listing_item_collisions(connection)

                item = connection.execute(
                    "SELECT title, content_text, category, last_seen_run_id, raw_json FROM items"
                ).fetchone()
                self.assertEqual(item["title"], "owner/existing")
                self.assertEqual(item["content_text"], "Native GitHub description.")
                self.assertEqual(item["category"], "repository")
                self.assertEqual(item["last_seen_run_id"], 1)
                self.assertNotIn("source_entry", json.loads(item["raw_json"]))
                self.assertEqual(report, {
                    "restored_items": 1,
                    "removed_metrics": 1,
                    "removed_item_observations": 1,
                })
                self.assertEqual(
                    [tuple(row) for row in connection.execute(
                        "SELECT stars, metric_source FROM metrics ORDER BY id"
                    )],
                    [(900, "github REST API")],
                )
                self.assertEqual(connection.execute("SELECT COUNT(*) FROM raw_snapshots").fetchone()[0], 2)
                self.assertEqual(connection.execute("SELECT COUNT(*) FROM upstream_entries").fetchone()[0], 1)
                self.assertEqual(
                    connection.execute("SELECT COUNT(*) FROM upstream_entry_observations").fetchone()[0],
                    1,
                )

    def test_listing_import_preserves_existing_item_and_keeps_complete_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "registry.sqlite3"
            raw_path = Path(directory) / "registry.json"
            collect.init_db(database)
            with collect.connect(database) as connection:
                connection.execute(
                    "INSERT INTO collection_runs(id, dataset_version, started_at, trigger, status) "
                    "VALUES (1, 'v20260816T000000Z', '2026-08-16T00:00:00Z', 'github-search', 'succeeded')"
                )
                connection.execute(
                    "INSERT INTO items(id, platform, external_id, canonical_url, item_type, title, author, content_text, category, relevance, media_kind, first_seen_at, last_seen_at, first_seen_run_id, last_seen_run_id, raw_json) "
                    "VALUES (1, 'github', 'owner/existing', 'https://github.com/owner/existing', 'repository', 'owner/existing', 'owner', 'Native GitHub description.', 'repository', 'direct', 'none', '2026-08-16T00:00:00Z', '2026-08-16T00:00:00Z', 1, 1, '{\"native\":true}')"
                )
                connection.execute(
                    "INSERT INTO metrics(item_id, collection_run_id, observed_at, stars, metric_source, raw_json) "
                    "VALUES (1, 1, '2026-08-16T00:00:00Z', 900, 'github REST API', '{\"stars\":900}')"
                )
                connection.execute(
                    "INSERT INTO collection_runs(id, dataset_version, started_at, trigger, status) "
                    "VALUES (2, 'v20260816T020000Z', '2026-08-16T02:00:00Z', 'source-monitor', 'running')"
                )
                descriptor = self.descriptor("2026-08-16T02:00:00Z")
                existing = dict(descriptor["entries"][0])
                existing.update({
                    "name": "官方核心 · owner/existing",
                    "url": "https://github.com/owner/existing",
                    "description": "Registry editorial description.",
                    "stars": 7,
                    "metrics": {
                        "stars": 7,
                        "metric_source": "Registry declared stars",
                        "observed_at": "2026-08-16T02:00:00Z",
                    },
                })
                new = dict(existing)
                new.update({
                    "name": "owner/new-plugin",
                    "url": "https://github.com/owner/new-plugin",
                    "install": "dsh plugin --profile web add github:owner/new-plugin",
                    "install_spec": "github:owner/new-plugin",
                    "stars": 11,
                    "metrics": {
                        "stars": 11,
                        "metric_source": "Registry declared stars",
                        "observed_at": "2026-08-16T02:00:00Z",
                    },
                })
                descriptor["entries"] = [existing, new]
                descriptor["entry_sources"][0]["entry_count"] = 2
                descriptor["registries"][0]["declared_count"] = 2
                descriptor["registries"][0]["actual_count"] = 2
                payload = {
                    "collected_at": "2026-08-16T02:00:00Z",
                    "collector": "scripts/monitor_sources.py",
                    "repositories": [descriptor],
                    "observations": [{
                        "platform": "github",
                        "query": "upstream:owner/registry",
                        "source_url": "https://github.com/owner/registry",
                        "collected_at": "2026-08-16T02:00:00Z",
                        "collector": "scripts/monitor_sources.py",
                        "method": "registry fixture",
                        "status": "ok",
                        "result_count": 2,
                        "notes": "Regression fixture.",
                        "items": [
                            monitor_sources.item_for_entry(existing, "2026-08-16T02:00:00Z", "owner/registry"),
                            monitor_sources.item_for_entry(new, "2026-08-16T02:00:00Z", "owner/registry"),
                        ],
                    }],
                }
                collect.dump_json(raw_path, payload)

                import_payload = monitor_sources.payload_for_item_import(connection, payload)
                self.assertEqual(
                    [item["url"] for item in import_payload["observations"][0]["items"]],
                    ["https://github.com/owner/new-plugin"],
                )
                collect.import_payload(connection, import_payload, 2, raw_path)
                raw_sha = collect.sha256_file(raw_path)
                raw_snapshot_id = int(connection.execute(
                    "SELECT id FROM raw_snapshots WHERE raw_sha256 = ?", (raw_sha,)
                ).fetchone()[0])
                monitor_sources.record_upstream_repositories(connection, payload, raw_snapshot_id)

                existing_item = connection.execute(
                    "SELECT title, author, content_text, category, last_seen_run_id, raw_json "
                    "FROM items WHERE id = 1"
                ).fetchone()
                self.assertEqual(tuple(existing_item), (
                    "owner/existing",
                    "owner",
                    "Native GitHub description.",
                    "repository",
                    1,
                    '{"native":true}',
                ))
                new_item = connection.execute(
                    "SELECT id, title FROM items WHERE canonical_url = 'https://github.com/owner/new-plugin'"
                ).fetchone()
                self.assertEqual(new_item["title"], "owner/new-plugin")
                listing_rows = connection.execute(
                    "SELECT entry_url, item_id FROM upstream_entries ORDER BY entry_url"
                ).fetchall()
                self.assertEqual([row["entry_url"] for row in listing_rows], [
                    "https://github.com/owner/existing",
                    "https://github.com/owner/new-plugin",
                ])
                self.assertEqual([row["item_id"] for row in listing_rows], [1, new_item["id"]])
                self.assertEqual(
                    connection.execute("SELECT COUNT(*) FROM upstream_entry_observations").fetchone()[0],
                    2,
                )
                self.assertEqual(
                    connection.execute("SELECT payload_json FROM raw_snapshots").fetchone()[0],
                    raw_path.read_text(encoding="utf-8"),
                )
                existing_metrics = connection.execute(
                    "SELECT stars, metric_source FROM metrics WHERE item_id = 1 ORDER BY id"
                ).fetchall()
                self.assertEqual([tuple(row) for row in existing_metrics], [(900, "github REST API")])
                listing_stars = connection.execute(
                    "SELECT stars FROM upstream_entry_observations ORDER BY stars"
                ).fetchall()
                self.assertEqual([row["stars"] for row in listing_stars], [7, 11])

    def test_ego_import_appends_listing_history_without_replacing_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "registry.sqlite3"
            collect.init_db(database)
            with collect.connect(database) as connection:
                for run_id, observed_at in (
                    (1, "2026-08-16T00:00:00Z"),
                    (2, "2026-08-16T02:00:00Z"),
                ):
                    connection.execute(
                        "INSERT INTO collection_runs(id, dataset_version, started_at, trigger, status) VALUES (?, ?, ?, 'ego-browser-source-capture', 'succeeded')",
                        (run_id, f"v20260816T0{2 * (run_id - 1)}0000Z", observed_at),
                    )
                    connection.execute(
                        "INSERT INTO raw_snapshots(id, collection_run_id, raw_sha256, raw_path, collected_at, byte_size, payload_json) VALUES (?, ?, ?, ?, ?, 2, '{}')",
                        (run_id, run_id, f"ego-raw-{run_id}", f"data/raw/ego/{run_id}.json", observed_at),
                    )
                    descriptor = self.descriptor(observed_at)
                    import_ego_source.record_upstream_repositories(
                        connection, {"repositories": [descriptor]}, run_id
                    )

                listing = connection.execute(
                    "SELECT first_seen_run_id, last_seen_run_id, active FROM upstream_entries"
                ).fetchall()
                history = connection.execute(
                    "SELECT collection_run_id, active FROM upstream_entry_observations ORDER BY collection_run_id"
                ).fetchall()

                self.assertEqual([tuple(row) for row in listing], [(1, 2, 1)])
                self.assertEqual([tuple(row) for row in history], [(1, 1), (2, 1)])

    def test_registry_entry_keeps_install_metadata_and_collection_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "registry.sqlite3"
            collect.init_db(database)
            with collect.connect(database) as connection:
                connection.execute(
                    "INSERT INTO collection_runs(id, dataset_version, started_at, trigger, status) "
                    "VALUES (1, 'v20260816T000000Z', '2026-08-16T00:00:00Z', 'source-monitor', 'succeeded')"
                )
                connection.execute(
                    "INSERT INTO raw_snapshots(id, collection_run_id, raw_sha256, raw_path, collected_at, byte_size, payload_json) "
                    "VALUES (1, 1, 'raw-1', 'data/raw/upstreams/one.json', '2026-08-16T00:00:00Z', 2, '{}')"
                )
                descriptor = {
                    "full_name": "owner/registry",
                    "html_url": "https://github.com/owner/registry",
                    "default_branch": "main",
                    "last_checked_at": "2026-08-16T00:00:00Z",
                    "entries": [{
                        "name": "dsh-example",
                        "owner": "owner",
                        "url": "https://github.com/owner/dsh-example",
                        "page": "https://example.test/p/owner/dsh-example/",
                        "category": "tools",
                        "description": "搜索文件。",
                        "description_i18n": {"en": "Search files.", "zh": "搜索文件。"},
                        "npm": "@owner/dsh-example",
                        "stars": 17,
                        "install": "dsh plugin --profile web add @owner/dsh-example",
                        "added": "2026-08-16",
                        "source_path": "plugins.json",
                        "source_line": None,
                        "entry_kind": "plugin-candidate",
                    }],
                }

                monitor_sources.record_upstream_repositories(connection, {"repositories": [descriptor]}, 1)

                row = connection.execute(
                    "SELECT owner, npm_package, page_url, description_i18n, stars, added_at, "
                    "raw_snapshot_id, first_seen_run_id, last_seen_run_id, active, source_json "
                    "FROM upstream_entries"
                ).fetchone()
                self.assertEqual(row["owner"], "owner")
                self.assertEqual(row["npm_package"], "@owner/dsh-example")
                self.assertEqual(row["page_url"], "https://example.test/p/owner/dsh-example/")
                self.assertEqual(row["description_i18n"], '{"en":"Search files.","zh":"搜索文件。"}')
                self.assertEqual(row["stars"], 17)
                self.assertEqual(row["added_at"], "2026-08-16")
                self.assertEqual(row["raw_snapshot_id"], 1)
                self.assertEqual(row["first_seen_run_id"], 1)
                self.assertEqual(row["last_seen_run_id"], 1)
                self.assertEqual(row["active"], 1)
                self.assertEqual(row["source_json"], json.dumps(descriptor["entries"][0], ensure_ascii=False, sort_keys=True, separators=(",", ":")))

    def test_successful_runs_append_listing_history_and_preserve_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "registry.sqlite3"
            collect.init_db(database)
            with collect.connect(database) as connection:
                for run_id, version, observed_at, stars in (
                    (1, "v20260816T000000Z", "2026-08-16T00:00:00Z", 17),
                    (2, "v20260816T020000Z", "2026-08-16T02:00:00Z", 19),
                ):
                    connection.execute(
                        "INSERT INTO collection_runs(id, dataset_version, started_at, trigger, status) VALUES (?, ?, ?, 'source-monitor', 'succeeded')",
                        (run_id, version, observed_at),
                    )
                    connection.execute(
                        "INSERT INTO raw_snapshots(id, collection_run_id, raw_sha256, raw_path, collected_at, byte_size, payload_json) VALUES (?, ?, ?, ?, ?, 2, '{}')",
                        (run_id, run_id, f"raw-{run_id}", f"data/raw/upstreams/{run_id}.json", observed_at),
                    )
                    descriptor = self.descriptor(observed_at, stars=stars)
                    monitor_sources.record_upstream_repositories(connection, {"repositories": [descriptor]}, run_id)

                current = connection.execute(
                    "SELECT first_seen_run_id, last_seen_run_id, stars, active FROM upstream_entries"
                ).fetchall()
                history = connection.execute(
                    "SELECT collection_run_id, stars, active FROM upstream_entry_observations ORDER BY collection_run_id"
                ).fetchall()

                self.assertEqual([tuple(row) for row in current], [(1, 2, 19, 1)])
                self.assertEqual([tuple(row) for row in history], [(1, 17, 1), (2, 19, 1)])

    def test_distinct_monorepo_install_specs_remain_distinct_listings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "registry.sqlite3"
            collect.init_db(database)
            with collect.connect(database) as connection:
                connection.execute(
                    "INSERT INTO collection_runs(id, dataset_version, started_at, trigger, status) "
                    "VALUES (1, 'v20260816T000000Z', '2026-08-16T00:00:00Z', 'source-monitor', 'succeeded')"
                )
                connection.execute(
                    "INSERT INTO raw_snapshots(id, collection_run_id, raw_sha256, raw_path, collected_at, byte_size, payload_json) "
                    "VALUES (1, 1, 'raw-1', 'data/raw/upstreams/one.json', '2026-08-16T00:00:00Z', 2, '{}')"
                )
                descriptor = self.descriptor("2026-08-16T00:00:00Z")
                first = dict(descriptor["entries"][0])
                first["install_spec"] = "github:owner/monorepo#path:/one"
                first["install"] = "dsh plugin --profile web add github:owner/monorepo#path:/one"
                second = dict(first)
                second["name"] = "dsh-two"
                second["install_spec"] = "github:owner/monorepo#path:/two"
                second["install"] = "dsh plugin --profile web add github:owner/monorepo#path:/two"
                descriptor["entries"] = [first, second]
                descriptor["entry_sources"][0]["entry_count"] = 2
                descriptor["registries"][0]["declared_count"] = 2
                descriptor["registries"][0]["actual_count"] = 2

                monitor_sources.record_upstream_repositories(connection, {"repositories": [descriptor]}, 1)

                rows = connection.execute(
                    "SELECT listing_key, entry_name FROM upstream_entries ORDER BY listing_key"
                ).fetchall()
                self.assertEqual([tuple(row) for row in rows], [
                    ("install:github:owner/monorepo#path:/one", "dsh-example"),
                    ("install:github:owner/monorepo#path:/two", "dsh-two"),
                ])

    def test_listing_key_migration_preserves_parent_and_history_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "registry.sqlite3"
            legacy_schema = collect.SCHEMA_PATH.read_text(encoding="utf-8")
            legacy_schema = legacy_schema.replace("PRAGMA user_version = 6;", "PRAGMA user_version = 5;")
            legacy_schema = legacy_schema.replace(
                "    listing_key TEXT NOT NULL,\n    entry_name TEXT NOT NULL,",
                "    entry_name TEXT NOT NULL,",
            )
            legacy_schema = legacy_schema.replace(
                "    UNIQUE(repository_id, listing_key)",
                "    UNIQUE(repository_id, entry_url, category)",
            )
            legacy_schema = legacy_schema.replace(
                "    listing_key TEXT NOT NULL,\n    registry_id TEXT,",
                "    registry_id TEXT,",
            )
            connection = sqlite3.connect(database)
            connection.row_factory = sqlite3.Row
            connection.executescript(legacy_schema)
            connection.execute(
                "INSERT INTO collection_runs(id, dataset_version, started_at, trigger, status) "
                "VALUES (1, 'v20260816T000000Z', '2026-08-16T00:00:00Z', 'source-monitor', 'succeeded')"
            )
            connection.execute(
                "INSERT INTO raw_snapshots(id, collection_run_id, raw_sha256, raw_path, collected_at, byte_size, payload_json) "
                "VALUES (1, 1, 'raw-1', 'data/raw/upstreams/one.json', '2026-08-16T00:00:00Z', 2, '{}')"
            )
            connection.execute(
                "INSERT INTO upstream_repositories(id, full_name, source_url, default_branch, last_checked_at) "
                "VALUES (1, 'owner/registry', 'https://github.com/owner/registry', 'main', '2026-08-16T00:00:00Z')"
            )
            connection.execute(
                "INSERT INTO upstream_entries(id, repository_id, entry_name, entry_url, entry_kind, category, install_spec, source_path, raw_snapshot_id, first_seen_run_id, last_seen_run_id, first_seen_at, last_seen_at) "
                "VALUES (1, 1, 'one', 'https://github.com/owner/monorepo', 'plugin-candidate', 'tools', 'github:owner/monorepo#path:/one', 'registry.json', 1, 1, 1, '2026-08-16T00:00:00Z', '2026-08-16T00:00:00Z')"
            )
            connection.execute(
                "INSERT INTO upstream_entry_observations(id, entry_id, collection_run_id, raw_snapshot_id, observed_at, active, entry_name, entry_url, entry_kind, category, description_i18n, install_spec, tags_json, registry_source_json, source_path) "
                "VALUES (1, 1, 1, 1, '2026-08-16T00:00:00Z', 1, 'one', 'https://github.com/owner/monorepo', 'plugin-candidate', 'tools', '{}', 'github:owner/monorepo#path:/one', '[]', '{}', 'registry.json')"
            )
            connection.commit()
            connection.close()

            collect.init_db(database)

            with collect.connect(database) as migrated:
                parent = migrated.execute(
                    "SELECT id, listing_key, entry_name FROM upstream_entries"
                ).fetchone()
                history = migrated.execute(
                    "SELECT entry_id, listing_key, entry_name FROM upstream_entry_observations"
                ).fetchone()
                self.assertEqual(tuple(parent), (1, "install:github:owner/monorepo#path:/one", "one"))
                self.assertEqual(tuple(history), (1, "install:github:owner/monorepo#path:/one", "one"))
                self.assertEqual(migrated.execute("PRAGMA user_version").fetchone()[0], 6)
                self.assertEqual(migrated.execute("PRAGMA foreign_key_check").fetchall(), [])

    def test_failed_source_does_not_deactivate_last_successful_listing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "registry.sqlite3"
            collect.init_db(database)
            with collect.connect(database) as connection:
                for run_id, source_status in ((1, "ok"), (2, "error"), (3, "ok")):
                    observed_at = f"2026-08-16T0{run_id}:00:00Z"
                    connection.execute(
                        "INSERT INTO collection_runs(id, dataset_version, started_at, trigger, status) VALUES (?, ?, ?, 'source-monitor', 'succeeded')",
                        (run_id, f"v20260816T0{run_id}0000Z", observed_at),
                    )
                    connection.execute(
                        "INSERT INTO raw_snapshots(id, collection_run_id, raw_sha256, raw_path, collected_at, byte_size, payload_json) VALUES (?, ?, ?, ?, ?, 2, '{}')",
                        (run_id, run_id, f"raw-{run_id}", f"data/raw/upstreams/{run_id}.json", observed_at),
                    )
                    descriptor = self.descriptor(observed_at) if run_id == 1 else self.descriptor(observed_at, entries=[])
                    descriptor["entry_sources"][0]["status"] = source_status
                    monitor_sources.record_upstream_repositories(connection, {"repositories": [descriptor]}, run_id)
                    active = connection.execute("SELECT active FROM upstream_entries").fetchone()[0]
                    self.assertEqual(active, 1 if run_id < 3 else 0)

                history = connection.execute(
                    "SELECT collection_run_id, active FROM upstream_entry_observations ORDER BY collection_run_id"
                ).fetchall()
                self.assertEqual([tuple(row) for row in history], [(1, 1), (3, 0)])

    def test_value_matrix_ignores_inactive_upstream_listings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "registry.sqlite3"
            collect.init_db(database)
            with collect.connect(database) as connection:
                connection.execute(
                    "INSERT INTO collection_runs(id, dataset_version, started_at, trigger, status) "
                    "VALUES (1, 'v20260816T000000Z', '2026-08-16T00:00:00Z', 'source-monitor', 'succeeded')"
                )
                connection.execute(
                    "INSERT INTO items(id, platform, external_id, canonical_url, item_type, title, category, relevance, media_kind, first_seen_at, last_seen_at, first_seen_run_id, last_seen_run_id, raw_json) "
                    "VALUES (1, 'github', 'owner/plugin', 'https://github.com/owner/plugin', 'plugin', 'plugin', 'tools', 'direct', 'none', '2026-08-16T00:00:00Z', '2026-08-16T00:00:00Z', 1, 1, '{}')"
                )
                connection.execute(
                    "INSERT INTO upstream_repositories(id, full_name, source_url, default_branch, last_checked_at) "
                    "VALUES (1, 'owner/registry', 'https://github.com/owner/registry', 'main', '2026-08-16T00:00:00Z')"
                )
                connection.execute(
                    "INSERT INTO upstream_entries(repository_id, item_id, listing_key, entry_name, entry_url, entry_kind, category, install_hint, active, first_seen_at, last_seen_at) "
                    "VALUES (1, 1, 'install:plugin', 'plugin', 'https://github.com/owner/plugin', 'plugin-candidate', 'tools', 'dsh plugin add plugin', 0, '2026-08-16T00:00:00Z', '2026-08-16T00:00:00Z')"
                )

                row = build_value_matrix.rows_for_scoring(connection)[0]

                self.assertEqual(row["upstream_count"], 0)
                self.assertEqual(row["plugin_count"], 0)
                self.assertEqual(row["install_count"], 0)

    @staticmethod
    def descriptor(observed_at: str, *, stars: int = 17, entries: list[dict[str, object]] | None = None) -> dict[str, object]:
        listing: dict[str, object] = {
            "name": "dsh-example",
            "owner": "owner",
            "url": "https://github.com/owner/dsh-example",
            "page": "https://example.test/p/owner/dsh-example/",
            "category": "tools",
            "description": "搜索文件。",
            "description_i18n": {"en": "Search files.", "zh": "搜索文件。"},
            "npm": "@owner/dsh-example",
            "stars": stars,
            "install": "dsh plugin --profile web add @owner/dsh-example",
            "install_spec": "@owner/dsh-example",
            "install_target": "npm",
            "added": "2026-08-16",
            "source_path": "plugins.json",
            "source_line": None,
            "entry_kind": "plugin-candidate",
        }
        return {
            "full_name": "owner/registry",
            "html_url": "https://github.com/owner/registry",
            "default_branch": "main",
            "last_checked_at": observed_at,
            "entry_sources": [{"source_ref": "plugins.json", "kind": "registry", "status": "ok", "entry_count": 1}],
            "registries": [{
                "source_ref": "plugins.json",
                "status": "ok",
                "format_version": 1,
                "declared_count": 1,
                "actual_count": 1,
                "updated": "2026-08-16",
                "metadata": {"name": "DSH plugins"},
            }],
            "entries": [listing] if entries is None else entries,
        }


if __name__ == "__main__":
    unittest.main()
