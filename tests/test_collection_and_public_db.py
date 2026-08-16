from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_public_db
import collect
import materialize_raw_snapshots
import reconcile_raw_snapshots


class EgoGitHubAdapterTests(unittest.TestCase):
    def test_visible_search_keeps_dom_and_native_stars(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / "data" / "raw" / "ego" / "github.json"
            raw.parent.mkdir(parents=True)
            raw.write_text("{}", encoding="utf-8")
            data = {
                "collected_at": "2026-08-15T19:17:51Z",
                "source": {
                    "platform": "github",
                    "query": '"deepseek-harness" plugin',
                    "url": "https://github.com/search?q=deepseek-harness",
                    "visible_result_count": 1,
                },
                "capture": {
                    "items": [{
                        "external_id": "owner/plugin",
                        "url": "https://github.com/owner/plugin",
                        "title": "owner/plugin",
                        "stars": 7,
                        "language": "TypeScript",
                        "visible_dom": "<article>exact visible evidence</article>",
                    }]
                },
            }

            with mock.patch.object(collect, "ROOT", root):
                payload = collect.legacy_payload(raw, data)

        self.assertIsNotNone(payload)
        observation = payload["observations"][0]
        item = observation["items"][0]
        self.assertEqual(observation["result_count"], 1)
        self.assertEqual(item["metrics"]["stars"], 7)
        self.assertEqual(item["raw_capture"]["visible_dom"], "<article>exact visible evidence</article>")

    def test_repository_api_keeps_full_payload_and_subscribers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / "data" / "raw" / "ego" / "repository.json"
            raw.parent.mkdir(parents=True)
            raw.write_text("{}", encoding="utf-8")
            repository = {
                "full_name": "owner/plugin",
                "html_url": "https://github.com/owner/plugin",
                "owner": {"login": "owner", "html_url": "https://github.com/owner"},
                "stargazers_count": 3,
                "forks_count": 2,
                "open_issues_count": 1,
                "subscribers_count": 4,
            }
            data = {
                "capture_kind": "ego-lite-github-repository-api",
                "captured_at": "2026-08-15T19:21:19Z",
                "source_url": "https://api.github.com/repos/owner/plugin",
                "repository": "owner/plugin",
                "payload": repository,
            }

            with mock.patch.object(collect, "ROOT", root):
                payload = collect.legacy_payload(raw, data)

        self.assertIsNotNone(payload)
        observation = payload["observations"][0]
        item = observation["items"][0]
        self.assertEqual(observation["collected_at"], data["captured_at"])
        self.assertEqual(item["metrics"]["subscribers"], 4)
        self.assertEqual(item["raw_capture"], repository)


class SeedSelectionTests(unittest.TestCase):
    def test_default_seed_excludes_auto_and_fork_manifests(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            raw_dir = Path(directory)
            included = raw_dir / "ego" / "capture.json"
            excluded_auto = raw_dir / "auto" / "capture.json"
            excluded_fork = raw_dir / "forks" / "capture.json"
            for path in (included, excluded_auto, excluded_fork):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}", encoding="utf-8")
            connection = mock.MagicMock()
            connection.__enter__.return_value = connection
            import_result = collect.ImportStats()
            args = argparse.Namespace(db=Path(directory) / "db.sqlite3", raw=None)
            with (
                mock.patch.object(collect, "RAW_DIR", raw_dir),
                mock.patch.object(collect, "init_db"),
                mock.patch.object(collect, "connect", return_value=connection),
                mock.patch.object(collect, "begin_collection_run", return_value=(1, "v-test", "now")),
                mock.patch.object(collect, "finish_collection_run"),
                mock.patch.object(collect, "import_files", return_value=import_result) as import_files,
            ):
                collect.command_seed(args)

        selected = import_files.call_args.args[1]
        self.assertEqual(selected, [included])

    def test_reconcile_imports_only_unregistered_checked_in_raw(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw_dir = root / "data" / "raw"
            database = root / "aggregator.sqlite3"
            known = raw_dir / "known.json"
            fresh = raw_dir / "xiaohongshu" / "fresh.json"
            for path, label, collected_at in (
                (known, "known", "2026-08-16T01:00:00Z"),
                (fresh, "fresh", "2026-08-16T02:00:00Z"),
            ):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({
                    "collected_at": collected_at,
                    "observations": [{
                        "platform": "web",
                        "query": label,
                        "source_url": f"https://example.com/{label}",
                        "collected_at": collected_at,
                        "items": [{
                            "platform": "web",
                            "external_id": label,
                            "url": f"https://example.com/{label}",
                            "title": label,
                        }],
                    }],
                }), encoding="utf-8")

            collect.init_db(database)
            with collect.connect(database) as connection:
                run_id, _, _ = collect.begin_collection_run(connection, "seed")
                stats = collect.import_files(connection, [known], run_id)
                collect.finish_collection_run(connection, run_id, stats)

            args = argparse.Namespace(db=database)
            version, stats = reconcile_raw_snapshots.reconcile(args.db, raw_dir)
            repeated_version, repeated_stats = reconcile_raw_snapshots.reconcile(args.db, raw_dir)

            with collect.connect(database) as connection:
                raw_count = connection.execute("SELECT COUNT(*) FROM raw_snapshots").fetchone()[0]
                triggers = [
                    str(row[0])
                    for row in connection.execute("SELECT trigger FROM collection_runs ORDER BY id")
                ]

        self.assertEqual(raw_count, 2)
        self.assertEqual(triggers, ["seed", "reconcile"])
        self.assertIsNotNone(version)
        self.assertEqual(stats.raw_files_seen, 1)
        self.assertIsNone(repeated_version)
        self.assertEqual(repeated_stats.raw_files_seen, 0)

    def test_reconcile_preserves_progress_when_later_raw_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw_dir = root / "data" / "raw"
            database = root / "aggregator.sqlite3"
            valid = raw_dir / "01-valid.json"
            invalid = raw_dir / "02-invalid.json"
            raw_dir.mkdir(parents=True)
            valid.write_text(json.dumps({
                "collected_at": "2026-08-16T01:00:00Z",
                "observations": [{
                    "platform": "web",
                    "query": "valid",
                    "source_url": "https://example.com/valid",
                    "collected_at": "2026-08-16T01:00:00Z",
                    "items": [{
                        "platform": "web",
                        "external_id": "valid",
                        "url": "https://example.com/valid",
                        "title": "valid",
                    }],
                }],
            }), encoding="utf-8")
            invalid.write_text("{", encoding="utf-8")

            with self.assertRaises(json.JSONDecodeError):
                reconcile_raw_snapshots.reconcile(database, raw_dir)

            with collect.connect(database) as connection:
                run = connection.execute(
                    "SELECT status, raw_files_seen, item_observations, new_items, error_message "
                    "FROM collection_runs"
                ).fetchone()
                raw_count = connection.execute("SELECT COUNT(*) FROM raw_snapshots").fetchone()[0]
                item_count = connection.execute("SELECT COUNT(*) FROM items").fetchone()[0]

        self.assertEqual(tuple(run[:4]), ("error", 2, 1, 1))
        self.assertIn("Expecting property name", str(run[4]))
        self.assertEqual(raw_count, 1)
        self.assertEqual(item_count, 1)


class RawMaterializationTests(unittest.TestCase):
    def test_overwritten_snapshot_gets_unique_restored_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / "data" / "raw" / "source.json"
            raw.parent.mkdir(parents=True)
            old_payload = b'{"version":1}'
            current_payload = b'{"version":2}'
            raw.write_bytes(current_payload)
            database = root / "archive.sqlite3"
            connection = sqlite3.connect(database)
            connection.execute(
                "CREATE TABLE raw_snapshots("
                "id INTEGER PRIMARY KEY, raw_path TEXT, collected_at TEXT, "
                "raw_sha256 TEXT, payload_json TEXT)"
            )
            connection.executemany(
                "INSERT INTO raw_snapshots VALUES (?, ?, ?, ?, ?)",
                [
                    (
                        1, "data/raw/source.json", "2026-08-15T01:00:00Z",
                        materialize_raw_snapshots.sha256_bytes(old_payload), old_payload.decode(),
                    ),
                    (
                        2, "data/raw/source.json", "2026-08-15T02:00:00Z",
                        materialize_raw_snapshots.sha256_bytes(current_payload), current_payload.decode(),
                    ),
                ],
            )
            connection.commit()
            connection.close()

            repairs = materialize_raw_snapshots.materialize(database, root)
            rerun = materialize_raw_snapshots.materialize(database, root)

            self.assertEqual(len(repairs), 1)
            self.assertEqual(rerun, [])
            restored = root / repairs[0].new_path
            self.assertEqual(restored.read_bytes(), old_payload)
            connection = sqlite3.connect(database)
            paths = connection.execute("SELECT raw_path FROM raw_snapshots ORDER BY id").fetchall()
            connection.close()
            self.assertEqual(paths[1], ("data/raw/source.json",))
            self.assertNotEqual(paths[0], paths[1])

    def test_fork_payload_is_release_only_unless_explicitly_requested(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data" / "raw" / "forks").mkdir(parents=True)
            payload = b'{"forks":[]}'
            database = root / "archive.sqlite3"
            connection = sqlite3.connect(database)
            connection.execute(
                "CREATE TABLE raw_snapshots("
                "id INTEGER PRIMARY KEY, raw_path TEXT, collected_at TEXT, "
                "raw_sha256 TEXT, payload_json TEXT)"
            )
            connection.execute(
                "INSERT INTO raw_snapshots VALUES (1, 'data/raw/forks/run/page.json', "
                "'2026-08-15T01:00:00Z', ?, ?)",
                (materialize_raw_snapshots.sha256_bytes(payload), payload.decode()),
            )
            connection.commit()
            connection.close()

            self.assertEqual(materialize_raw_snapshots.materialize(database, root), [])
            repairs = materialize_raw_snapshots.materialize(
                database,
                root,
                include_forks=True,
            )

            self.assertEqual(len(repairs), 1)
            self.assertEqual((root / repairs[0].new_path).read_bytes(), payload)

    def test_stripped_projection_cannot_restore_missing_raw(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data" / "raw").mkdir(parents=True)
            database = root / "public.sqlite3"
            connection = sqlite3.connect(database)
            connection.execute(
                "CREATE TABLE raw_snapshots("
                "id INTEGER PRIMARY KEY, raw_path TEXT, collected_at TEXT, "
                "raw_sha256 TEXT, payload_json TEXT)"
            )
            connection.execute(
                "INSERT INTO raw_snapshots VALUES (1, 'data/raw/missing.json', "
                "'2026-08-15T01:00:00Z', ?, '{}')",
                ("a" * 64,),
            )
            connection.commit()
            connection.close()

            with self.assertRaisesRegex(RuntimeError, "use the full archive"):
                materialize_raw_snapshots.materialize(database, root)


class ItemSeenRangeTests(unittest.TestCase):
    def test_out_of_order_imports_preserve_observation_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "aggregator.sqlite3"
            collect.init_db(database)
            observations = (
                (1, "2026-08-16T03:00:00Z"),
                (2, "2026-08-16T01:00:00Z"),
                (3, "2026-08-16T02:00:00Z"),
            )
            with collect.connect(database) as connection:
                for run_id, observed_at in observations:
                    connection.execute(
                        "INSERT INTO collection_runs("
                        "id, dataset_version, started_at, finished_at, trigger, status"
                        ") VALUES (?, ?, ?, ?, 'test', 'succeeded')",
                        (run_id, f"test-{run_id}", observed_at, observed_at),
                    )
                    collect.import_payload(
                        connection,
                        {
                            "observations": [{
                                "platform": "web",
                                "query": "deepseek harness",
                                "source_url": "https://example.com/search",
                                "collected_at": observed_at,
                                "items": [{
                                    "platform": "web",
                                    "external_id": "example-plugin",
                                    "url": "https://example.com/plugin",
                                    "title": "Example plugin",
                                }],
                            }],
                        },
                        run_id,
                    )

                row = connection.execute(
                    "SELECT first_seen_at, last_seen_at, first_seen_run_id, last_seen_run_id "
                    "FROM items WHERE canonical_url = 'https://example.com/plugin'"
                ).fetchone()

            self.assertEqual(
                tuple(row),
                ("2026-08-16T01:00:00Z", "2026-08-16T03:00:00Z", 2, 1),
            )

    def test_init_repairs_seen_ranges_from_observation_history_idempotently(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "aggregator.sqlite3"
            collect.init_db(database)
            with collect.connect(database) as connection:
                for run_id, observed_at in (
                    (1, "2026-08-16T03:00:00Z"),
                    (2, "2026-08-16T01:00:00Z"),
                ):
                    connection.execute(
                        "INSERT INTO collection_runs("
                        "id, dataset_version, started_at, finished_at, trigger, status"
                        ") VALUES (?, ?, ?, ?, 'test', 'succeeded')",
                        (run_id, f"test-{run_id}", observed_at, observed_at),
                    )
                    collect.import_payload(
                        connection,
                        {
                            "observations": [{
                                "platform": "web",
                                "query": "deepseek harness",
                                "source_url": "https://example.com/search",
                                "collected_at": observed_at,
                                "items": [{
                                    "platform": "web",
                                    "external_id": "example-plugin",
                                    "url": "https://example.com/plugin",
                                }],
                            }],
                        },
                        run_id,
                    )
                connection.execute(
                    "UPDATE items SET first_seen_at = '2026-08-16T04:00:00Z', "
                    "last_seen_at = '2026-08-16T00:00:00Z', "
                    "first_seen_run_id = 1, last_seen_run_id = 2"
                )

            collect.init_db(database)
            collect.init_db(database)

            with collect.connect(database) as connection:
                row = connection.execute(
                    "SELECT first_seen_at, last_seen_at, first_seen_run_id, last_seen_run_id "
                    "FROM items WHERE canonical_url = 'https://example.com/plugin'"
                ).fetchone()
            self.assertEqual(
                tuple(row),
                ("2026-08-16T01:00:00Z", "2026-08-16T03:00:00Z", 2, 1),
            )


class PublicDatabaseTests(unittest.TestCase):
    @staticmethod
    def create_database(path: Path) -> None:
        connection = sqlite3.connect(path)
        connection.executescript(
            """
            CREATE TABLE collection_runs(id INTEGER PRIMARY KEY, trigger TEXT);
            CREATE TABLE items(id INTEGER PRIMARY KEY, canonical_url TEXT, platform TEXT, external_id TEXT, raw_json TEXT);
            CREATE TABLE raw_snapshots(raw_sha256 TEXT, payload_json TEXT);
            CREATE TABLE metrics(
                id INTEGER PRIMARY KEY,
                item_id INTEGER,
                observed_at TEXT,
                metric_source TEXT,
                raw_json TEXT
            );
            CREATE UNIQUE INDEX idx_metrics_dedupe ON metrics(item_id, observed_at, metric_source);
            CREATE TABLE github_user_profiles(raw_json TEXT);
            CREATE TABLE upstream_entries(source_json TEXT);
            CREATE TABLE upstream_entry_observations(
                id INTEGER PRIMARY KEY,
                entry_id INTEGER,
                collection_run_id INTEGER
            );
            CREATE TABLE plugin_packs(
                id TEXT PRIMARY KEY,
                slug TEXT NOT NULL UNIQUE,
                current_version TEXT NOT NULL,
                active INTEGER NOT NULL,
                maintainer TEXT NOT NULL,
                first_observed_at TEXT NOT NULL,
                last_observed_at TEXT NOT NULL
            );
            CREATE TABLE plugin_pack_versions(
                pack_id TEXT NOT NULL,
                version TEXT NOT NULL,
                dataset_version TEXT NOT NULL,
                name_en TEXT NOT NULL,
                name_zh TEXT NOT NULL,
                description_en TEXT NOT NULL,
                description_zh TEXT NOT NULL,
                task_en TEXT NOT NULL,
                task_zh TEXT NOT NULL,
                observed_at TEXT NOT NULL,
                source_path TEXT NOT NULL,
                source_sha256 TEXT NOT NULL,
                definition_json TEXT NOT NULL,
                PRIMARY KEY(pack_id, version),
                FOREIGN KEY(pack_id) REFERENCES plugin_packs(id) ON DELETE CASCADE
            );
            CREATE TABLE plugin_pack_members(
                pack_id TEXT NOT NULL,
                pack_version TEXT NOT NULL,
                member_order INTEGER NOT NULL,
                deeplugin_id TEXT NOT NULL,
                expected_name TEXT NOT NULL,
                install_spec TEXT NOT NULL,
                relationship TEXT NOT NULL,
                member_group TEXT NOT NULL,
                reason_en TEXT NOT NULL,
                reason_zh TEXT NOT NULL,
                definition_json TEXT NOT NULL,
                PRIMARY KEY(pack_id, pack_version, member_order),
                FOREIGN KEY(pack_id, pack_version)
                    REFERENCES plugin_pack_versions(pack_id, version) ON DELETE CASCADE
            );
            CREATE TABLE fork_snapshots(
                id INTEGER PRIMARY KEY,
                fork_id INTEGER,
                collection_run_id INTEGER
            );
            CREATE TABLE fork_file_changes(
                snapshot_id INTEGER REFERENCES fork_snapshots(id) ON DELETE CASCADE,
                raw_json TEXT
            );
            CREATE TABLE fork_commits(
                id INTEGER PRIMARY KEY,
                fork_id INTEGER,
                snapshot_id INTEGER REFERENCES fork_snapshots(id) ON DELETE CASCADE,
                committed_at TEXT,
                authored_at TEXT,
                last_seen_at TEXT,
                first_seen_at TEXT,
                raw_json TEXT
            );
            CREATE TABLE fork_rankings(
                fork_id INTEGER,
                collection_run_id INTEGER,
                components_json TEXT
            );
            CREATE TABLE value_assessments(collection_run_id INTEGER);
            INSERT INTO collection_runs VALUES (1, 'seed'), (2, 'scheduled');
            INSERT INTO items VALUES
                (1, 'https://example.com/1', 'web', '1', '{"raw": 1}'),
                (2, 'https://example.com/2', 'web', '2', '{"raw": 2}');
            INSERT INTO raw_snapshots VALUES ('sha-1', '{"raw": 1}');
            INSERT INTO metrics VALUES (1, 1, '2026-08-16T00:00:00Z', 'test', '{"raw": 1}');
            INSERT INTO github_user_profiles VALUES ('{"raw": 1}');
            INSERT INTO upstream_entries VALUES ('{"raw": 1}');
            INSERT INTO upstream_entry_observations VALUES
                (1, 1, 1),
                (2, 1, 2),
                (3, 2, 1),
                (4, 2, 2);
            INSERT INTO plugin_packs VALUES
                ('deeplugin-pack-example', 'example', '1.0.0', 1, 'fixture',
                 '2026-08-16T00:00:00Z', '2026-08-16T00:00:00Z');
            INSERT INTO plugin_pack_versions VALUES
                ('deeplugin-pack-example', '1.0.0', 'scheduled', 'Example', '示例',
                 'Example pack', '示例组合', 'Run an example', '运行示例',
                 '2026-08-16T00:00:00Z', 'registry/packs.json', 'pack-sha', '{}');
            INSERT INTO plugin_pack_members VALUES
                ('deeplugin-pack-example', '1.0.0', 1, 'deeplugin-example', 'example',
                 'github:owner/example', 'required', 'core', 'Required', '必需', '{}');
            INSERT INTO fork_snapshots VALUES
                (1, 1, 1),
                (2, 1, 2),
                (3, 2, 1),
                (4, 2, 2),
                (5, 3, 1),
                (6, 3, 2);
            INSERT INTO fork_file_changes VALUES
                (5, '{"raw": 1}'),
                (6, '{"raw": 2}');
            INSERT INTO fork_commits VALUES
                (1, 1, 1, '2026-08-13T00:00:00Z', NULL, '2026-08-13T00:00:00Z', '2026-08-13T00:00:00Z', '{"raw": 1}'),
                (2, 1, 1, '2026-08-14T00:00:00Z', NULL, '2026-08-14T00:00:00Z', '2026-08-14T00:00:00Z', '{"raw": 2}'),
                (3, 1, 1, '2026-08-15T00:00:00Z', NULL, '2026-08-15T00:00:00Z', '2026-08-15T00:00:00Z', '{"raw": 3}'),
                (4, 1, 1, '2026-08-16T00:00:00Z', NULL, '2026-08-16T00:00:00Z', '2026-08-16T00:00:00Z', '{"raw": 4}');
            INSERT INTO fork_rankings VALUES
                (1, 1, '{"score": 1}'),
                (2, 1, '{"score": 1}'),
                (3, 1, '{"score": 1}'),
                (1, 2, '{"score": 2}'),
                (2, 2, '{"score": 2}'),
                (3, 2, '{"score": 2}');
            INSERT INTO value_assessments VALUES (1), (1), (2), (2);
            """
        )
        connection.close()

    def test_projection_strips_blobs_and_prunes_superseded_derived_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "public.sqlite3"
            self.create_database(path)

            run_id = build_public_db.project_database(path, "a" * 64, "aggregator-full.sqlite3.zst")

            connection = sqlite3.connect(path)
            self.assertEqual(run_id, 2)
            for table, column in build_public_db.STRIPPED_JSON_COLUMNS:
                self.assertEqual(connection.execute(f'SELECT DISTINCT "{column}" FROM "{table}"').fetchall(), [("{}",)])
            self.assertEqual(connection.execute("SELECT source_json FROM upstream_entries").fetchall(), [("{}",)])
            self.assertEqual(
                connection.execute("SELECT id FROM upstream_entry_observations ORDER BY id").fetchall(),
                [(2,), (4,)],
            )
            self.assertEqual(connection.execute("SELECT collection_run_id FROM value_assessments").fetchall(), [(2,), (2,)])
            self.assertEqual(connection.execute("SELECT DISTINCT collection_run_id FROM fork_rankings").fetchall(), [(2,)])
            self.assertEqual(connection.execute("SELECT DISTINCT components_json FROM fork_rankings").fetchall(), [("{}",)])
            self.assertEqual(connection.execute("SELECT id FROM fork_snapshots ORDER BY id").fetchall(), [(1,), (2,), (4,), (6,)])
            self.assertEqual(connection.execute("SELECT id FROM fork_commits ORDER BY id").fetchall(), [(2,), (3,), (4,)])
            self.assertEqual(connection.execute("SELECT snapshot_id FROM fork_file_changes").fetchall(), [(6,)])
            self.assertEqual(connection.execute("SELECT id FROM plugin_packs").fetchall(), [("deeplugin-pack-example",)])
            self.assertEqual(
                connection.execute("SELECT pack_id, version FROM plugin_pack_versions").fetchall(),
                [("deeplugin-pack-example", "1.0.0")],
            )
            self.assertEqual(
                connection.execute("SELECT pack_id, deeplugin_id FROM plugin_pack_members").fetchall(),
                [("deeplugin-pack-example", "deeplugin-example")],
            )
            self.assertIsNone(
                connection.execute(
                    "SELECT 1 FROM sqlite_schema WHERE type = 'index' AND name = 'idx_metrics_dedupe'"
                ).fetchone()
            )
            policy = json.loads(
                connection.execute("SELECT stripped_fields_json FROM public_projection_metadata").fetchone()[0]
            )
            self.assertEqual(policy["dropped_indexes"], ["idx_metrics_dedupe"])
            self.assertEqual(
                connection.execute("SELECT projection_version FROM public_projection_metadata").fetchone()[0],
                4,
            )
            self.assertEqual(connection.execute("SELECT source_sha256 FROM public_projection_metadata").fetchone()[0], "a" * 64)
            connection.close()

    def test_projection_verification_rejects_duplicate_metrics_without_write_index(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.sqlite3"
            projected = Path(directory) / "projected.sqlite3"
            self.create_database(source)
            with sqlite3.connect(source) as connection:
                connection.execute("DROP INDEX idx_metrics_dedupe")
                connection.execute(
                    "INSERT INTO metrics VALUES (2, 1, '2026-08-16T00:00:00Z', 'test', '{\"raw\": 2}')"
                )
            shutil.copyfile(source, projected)
            run_id = build_public_db.project_database(projected, "a" * 64, "aggregator-full.sqlite3.zst")

            with self.assertRaisesRegex(RuntimeError, "duplicate metric history key"):
                build_public_db.verify_projection(source, projected, run_id, 95 * 1024 * 1024)

    def test_archive_mismatch_blocks_projection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.sqlite3"
            archive = Path(directory) / "source.sqlite3.zst"
            source.write_bytes(b"database")
            archive.write_bytes(b"archive")
            with mock.patch.object(build_public_db, "sha256_zstd_payload", return_value="b" * 64):
                with self.assertRaisesRegex(RuntimeError, "does not match"):
                    build_public_db.verify_archive(source, archive)


if __name__ == "__main__":
    unittest.main()
