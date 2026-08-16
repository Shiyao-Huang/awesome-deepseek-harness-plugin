from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from http.client import RemoteDisconnected
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_fork_index
import collect
import collect_forks


class WorkflowSafetyTests(unittest.TestCase):
    def test_refresh_workflows_checkout_latest_main_at_job_start(self) -> None:
        for filename in ("refresh-index.yml", "refresh-forks.yml"):
            workflow = (ROOT / ".github" / "workflows" / filename).read_text()
            checkout_start = workflow.index("uses: actions/checkout@v4")
            checkout_end = workflow.index("- name: Set up Python", checkout_start)

            self.assertIn("ref: main", workflow[checkout_start:checkout_end], filename)

    def test_core_refresh_commits_every_raw_evidence_namespace(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "refresh-index.yml").read_text()

        self.assertIn(
            'scripts/publish_generated_commit.sh "data: refresh public ecosystem index" data/raw index docs plugin/data README.md',
            workflow,
        )


def fork(name: str, stars: int, pushed_at: str, forks: int = 0) -> dict[str, object]:
    return {
        "full_name": name,
        "stargazers_count": stars,
        "forks_count": forks,
        "pushed_at": pushed_at,
    }


class ApiCallTests(unittest.TestCase):
    def test_transient_disconnect_is_retried(self) -> None:
        response = ({"name": "owner/repo"}, {"x-ratelimit-remaining": "42"})
        with (
            mock.patch.object(
                collect_forks,
                "api_request",
                side_effect=[RemoteDisconnected("closed"), response],
            ) as request,
            mock.patch("time.sleep") as sleeper,
        ):
            result = collect_forks.api_call("https://api.github.com/repos/owner/repo", "token")

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["response"], response[0])
        self.assertEqual(request.call_count, 2)
        sleeper.assert_called_once_with(1)

    def test_repeated_disconnect_becomes_reviewable_error(self) -> None:
        with (
            mock.patch.object(
                collect_forks,
                "api_request",
                side_effect=RemoteDisconnected("closed"),
            ) as request,
            mock.patch("time.sleep") as sleeper,
        ):
            result = collect_forks.api_call("https://api.github.com/repos/owner/repo", "token")

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["url"], "https://api.github.com/repos/owner/repo")
        self.assertIn("closed", result["error"])
        self.assertEqual(result["attempts"], 3)
        self.assertTrue(result["transient"])
        self.assertEqual(request.call_count, 3)
        self.assertEqual([call.args for call in sleeper.call_args_list], [(1,), (2,)])


class DeepScanQueueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.db = sqlite3.connect(":memory:")
        self.db.row_factory = sqlite3.Row
        self.db.execute(
            """
            CREATE TABLE fork_repositories(
                full_name TEXT PRIMARY KEY,
                html_url TEXT,
                stars INTEGER,
                forks INTEGER,
                pushed_at TEXT,
                last_deep_checked_at TEXT,
                detail_status TEXT
            )
            """
        )

    def tearDown(self) -> None:
        self.db.close()

    def add_prior(self, name: str, pushed_at: str, last_deep_checked_at: str | None) -> None:
        self.db.execute(
            "INSERT INTO fork_repositories VALUES (?, ?, 0, 0, ?, ?, ?)",
            (name, f"https://github.com/{name}", pushed_at, last_deep_checked_at, "ok" if last_deep_checked_at else "metadata-only"),
        )

    def test_changed_rechecks_do_not_starve_never_scanned_forks(self) -> None:
        self.add_prior("changed/high", "2026-08-01T00:00:00Z", "2026-08-01T00:00:00Z")
        self.add_prior("changed/low", "2026-08-01T00:00:00Z", "2026-08-01T00:00:00Z")
        rows = [
            fork("changed/high", 50, "2026-08-02T00:00:00Z"),
            fork("changed/low", 1, "2026-08-02T00:00:00Z"),
            fork("new/a", 40, "2026-08-03T00:00:00Z"),
            fork("new/b", 30, "2026-08-03T00:00:00Z"),
            fork("new/c", 20, "2026-08-03T00:00:00Z"),
            fork("new/d", 10, "2026-08-03T00:00:00Z"),
        ]

        selected = collect_forks.select_deep_forks(self.db, rows, 5, False, False, 0.2)

        self.assertEqual(selected, {"changed/high", "new/a", "new/b", "new/c", "new/d"})

    def test_changed_forks_fill_budget_after_backfill_finishes(self) -> None:
        for name in ("changed/a", "changed/b", "changed/c"):
            self.add_prior(name, "2026-08-01T00:00:00Z", "2026-08-01T00:00:00Z")
        rows = [
            fork("changed/a", 3, "2026-08-02T00:00:00Z"),
            fork("changed/b", 2, "2026-08-02T00:00:00Z"),
            fork("changed/c", 1, "2026-08-02T00:00:00Z"),
        ]

        selected = collect_forks.select_deep_forks(self.db, rows, 2, False, False, 0.2)

        self.assertEqual(selected, {"changed/a", "changed/b"})

    def test_manual_recheck_uses_native_repository_influence(self) -> None:
        rows = [fork("owner/low", 1, "2026-08-02T00:00:00Z"), fork("owner/high", 20, "2026-08-02T00:00:00Z")]

        selected = collect_forks.select_deep_forks(self.db, rows, 1, False, True)

        self.assertEqual(selected, {"owner/high"})


class ForkProjectionTests(unittest.TestCase):
    def test_fork_page_links_back_to_store_root(self) -> None:
        coverage = {
            "observed": 0,
            "audited": 0,
            "coverage_percent": 0,
            "estimated_backfill_days": 0,
        }

        page = build_fork_index.render_fork_page("v-test", [], coverage, [])

        self.assertIn('class="brand" href="./"', page)
        self.assertIn('class="breadcrumbs"><a href="./"', page)

    def test_star_rank_is_separate_from_composite_rank(self) -> None:
        records = [
            {"full_name": "owner/influential", "stars": 2, "forks": 1, "rank": 1},
            {"full_name": "owner/popular", "stars": 20, "forks": 0, "rank": 2},
            {"full_name": "owner/tie", "stars": 2, "forks": 3, "rank": 3},
        ]

        ordered = build_fork_index.assign_github_star_ranks(records)

        self.assertEqual([record["full_name"] for record in ordered], ["owner/popular", "owner/tie", "owner/influential"])
        self.assertEqual(records[0]["github_star_rank"], 3)
        self.assertEqual(records[1]["rank"], 2)

    def test_coverage_eta_reserves_changed_recheck_capacity(self) -> None:
        db = sqlite3.connect(":memory:")
        db.row_factory = sqlite3.Row
        db.execute("CREATE TABLE collection_runs(id INTEGER PRIMARY KEY, trigger TEXT, status TEXT)")
        db.execute(
            """
            CREATE TABLE fork_repositories(
                full_name TEXT,
                html_url TEXT,
                stars INTEGER,
                forks INTEGER,
                pushed_at TEXT,
                last_deep_checked_at TEXT,
                detail_status TEXT,
                last_seen_run_id INTEGER
            )
            """
        )
        db.executemany(
            "INSERT INTO collection_runs VALUES (?, 'forks', 'succeeded')",
            [(1,), (2,)],
        )
        db.executemany(
            "INSERT INTO fork_repositories VALUES (?, ?, ?, 0, ?, ?, ?, ?)",
            [
                ("owner/a", "https://github.com/owner/a", 3, "2026-08-02T00:00:00Z", "2026-08-01T00:00:00Z", "ok", 2),
                ("owner/b", "https://github.com/owner/b", 2, "2026-08-02T00:00:00Z", None, "metadata-only", 2),
                ("owner/c", "https://github.com/owner/c", 1, "2026-08-02T00:00:00Z", None, "metadata-only", 2),
                ("owner/gone", "https://github.com/owner/gone", 99, "2026-08-02T00:00:00Z", None, "metadata-only", 1),
            ],
        )

        coverage = build_fork_index.coverage_summary(db, {"deep_scan_limit": 2, "changed_recheck_fraction": 0.5})

        self.assertEqual(coverage["audited"], 1)
        self.assertEqual(coverage["pending"], 2)
        self.assertEqual(coverage["observed"], 3)
        self.assertEqual(coverage["historical_observed"], 4)
        self.assertEqual(coverage["inactive_or_missing"], 1)
        self.assertEqual(coverage["guaranteed_daily_backfill"], 1)
        self.assertEqual(coverage["estimated_backfill_days"], 2)
        self.assertEqual(coverage["changed_since_audit"][0]["full_name"], "owner/a")
        self.assertNotIn("owner/gone", {row["full_name"] for row in coverage["next_never_scanned"]})
        db.close()

    def test_fork_repository_retains_deep_change_summary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "forks.sqlite3"
            collect.init_db(db_path)
            with collect.connect(db_path) as db:
                timestamp = "2026-08-01T00:00:00Z"
                db.execute(
                    "INSERT INTO collection_runs(id, dataset_version, started_at, trigger, status) "
                    "VALUES (1, 'v1', ?, 'forks', 'succeeded')",
                    (timestamp,),
                )
                db.execute(
                    "INSERT INTO raw_snapshots(id, collection_run_id, raw_sha256, raw_path, collected_at, byte_size, payload_json) "
                    "VALUES (1, 1, 'raw-1', 'raw-1.json', ?, 2, '{}')",
                    (timestamp,),
                )
                deep_summary = "观察到 3 个提交修改 2 个文件，主要涉及工具与脚本。"

                def payload(detail_status: str, summary: str, deep_scanned_at: str | None) -> dict[str, object]:
                    normalized = {
                        "full_name": "owner/fork",
                        "html_url": "https://github.com/owner/fork",
                        "api_url": "https://api.github.com/repos/owner/fork",
                        "owner_login": "owner",
                        "owner_type": "User",
                        "default_branch": "main",
                        "parent_full_name": "deepseek-ai/deepseek-harness",
                        "source_full_name": "deepseek-ai/deepseek-harness",
                        "is_fork": 1,
                        "archived": 0,
                        "disabled": 0,
                        "status": "ok",
                        "detail_status": detail_status,
                        "deep_scanned_at": deep_scanned_at,
                        "change_summary": summary,
                        "modification_categories": {"tools-and-scripts": 2} if deep_scanned_at else {},
                        "compare_status": "ahead" if deep_scanned_at else None,
                        "ahead_by": 3 if deep_scanned_at else None,
                        "changed_files": 2 if deep_scanned_at else None,
                    }
                    return {
                        "upstream": {"normalized": {
                            "full_name": "deepseek-ai/deepseek-harness",
                            "html_url": "https://github.com/deepseek-ai/deepseek-harness",
                            "api_url": "https://api.github.com/repos/deepseek-ai/deepseek-harness",
                            "default_branch": "main",
                        }},
                        "owner_profiles": [],
                        "observations": [{"items": []}],
                        "forks": [{"normalized": normalized, "files": [], "commits": {"status": "ok", "response": []}}],
                        "rankings": [],
                    }

                collect_forks.persist_forks(db, payload("ok", deep_summary, timestamp), 1, "v1", 1, timestamp)
                self.assertEqual(
                    db.execute("SELECT change_summary FROM fork_repositories WHERE full_name = 'owner/fork'").fetchone()[0],
                    deep_summary,
                )

                next_timestamp = "2026-08-02T00:00:00Z"
                db.execute(
                    "INSERT INTO collection_runs(id, dataset_version, started_at, trigger, status) "
                    "VALUES (2, 'v2', ?, 'forks', 'succeeded')",
                    (next_timestamp,),
                )
                db.execute(
                    "INSERT INTO raw_snapshots(id, collection_run_id, raw_sha256, raw_path, collected_at, byte_size, payload_json) "
                    "VALUES (2, 2, 'raw-2', 'raw-2.json', ?, 2, '{}')",
                    (next_timestamp,),
                )
                metadata_summary = "当前仅确认这是 upstream 的公开 Fork；修改面待下一轮深扫。"
                collect_forks.persist_forks(
                    db,
                    payload("metadata-only", metadata_summary, None),
                    2,
                    "v2",
                    2,
                    next_timestamp,
                )

                self.assertEqual(
                    db.execute("SELECT change_summary FROM fork_repositories WHERE full_name = 'owner/fork'").fetchone()[0],
                    deep_summary,
                )
                self.assertEqual(
                    db.execute("SELECT change_summary FROM fork_snapshots WHERE collection_run_id = 2").fetchone()[0],
                    deep_summary,
                )


if __name__ == "__main__":
    unittest.main()
