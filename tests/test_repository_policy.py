"""Repository-level policy checks for generated dataset assets."""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_ONLY_SQLITE_ASSETS = (
    "data/aggregator.sqlite3",
    "data/aggregator-full.sqlite3.zst",
)


class RepositoryPolicyTests(unittest.TestCase):
    def test_release_only_sqlite_assets_are_ignored_and_untracked(self) -> None:
        ignored = subprocess.run(
            ["git", "check-ignore", "--stdin"],
            cwd=ROOT,
            input="\n".join(RELEASE_ONLY_SQLITE_ASSETS) + "\n",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(ignored.returncode, 0, ignored.stderr)
        self.assertEqual(
            set(ignored.stdout.splitlines()),
            set(RELEASE_ONLY_SQLITE_ASSETS),
        )

        tracked = subprocess.check_output(
            ["git", "ls-files", "--", *RELEASE_ONLY_SQLITE_ASSETS],
            cwd=ROOT,
            text=True,
        )
        self.assertEqual(tracked, "")

    def test_refresh_workflows_rebuild_on_latest_main_without_rebase(self) -> None:
        publisher = (ROOT / "scripts" / "publish_generated_commit.sh").read_text(encoding="utf-8")
        self.assertIn('worktree add --detach "$publish_worktree" origin/main', publisher)
        self.assertIn('make -C "$publish_worktree" build', publisher)
        self.assertIn('git -C "$publish_worktree" push origin HEAD:main', publisher)

        for name in ("refresh-index.yml", "refresh-forks.yml"):
            workflow = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
            self.assertIn("scripts/publish_generated_commit.sh", workflow)
            self.assertNotIn("git rebase", workflow)

    def test_refresh_workflow_publish_commands_use_yaml_block_scalars(self) -> None:
        for name in ("refresh-index.yml", "refresh-forks.yml"):
            workflow = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
            self.assertIn(
                'run: |\n          scripts/publish_generated_commit.sh "data: ',
                workflow,
            )
            self.assertNotIn(
                'run: scripts/publish_generated_commit.sh "data: ',
                workflow,
            )

    def test_generated_publisher_rebuilds_forks_before_other_projections(self) -> None:
        publisher = (ROOT / "scripts" / "publish_generated_commit.sh").read_text(encoding="utf-8")
        fork_build = publisher.index('python3 "$publish_worktree/scripts/build_fork_index.py"')
        other_builds = publisher.index('make -C "$publish_worktree" build')

        self.assertLess(fork_build, other_builds)

    def test_generated_publisher_reconciles_committed_raw_before_build(self) -> None:
        publisher = (ROOT / "scripts" / "publish_generated_commit.sh").read_text(encoding="utf-8")
        reconcile = publisher.index('scripts/reconcile_raw_snapshots.py')
        fork_build = publisher.index('python3 "$publish_worktree/scripts/build_fork_index.py"')

        self.assertLess(reconcile, fork_build)

    def test_refresh_workflows_publish_one_full_database_build(self) -> None:
        publisher = (ROOT / "scripts" / "publish_generated_commit.sh").read_text(encoding="utf-8")
        self.assertIn('cp "$source_database" "$publish_worktree/data/aggregator.sqlite3"', publisher)
        self.assertNotIn('make -C "$publish_worktree" restore-full', publisher)

        core = (ROOT / ".github" / "workflows" / "refresh-index.yml").read_text(encoding="utf-8")
        forks = (ROOT / ".github" / "workflows" / "refresh-forks.yml").read_text(encoding="utf-8")
        self.assertIn("run: make core-collect", core)
        self.assertNotIn("make core-refresh", core)
        self.assertNotIn("Rebuild projections and database assets", forks)

    def test_refresh_workflows_gate_append_only_metrics_before_push(self) -> None:
        publisher = (ROOT / "scripts" / "publish_generated_commit.sh").read_text(encoding="utf-8")
        validation = publisher.index('scripts/validate_append_only.py')
        commit = publisher.index('git -C "$publish_worktree" commit')
        push = publisher.index('git -C "$publish_worktree" push')
        self.assertLess(validation, commit)
        self.assertLess(validation, push)

        for name in ("refresh-index.yml", "refresh-forks.yml"):
            workflow = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
            self.assertIn('cp data/aggregator.sqlite3 "$RUNNER_TEMP/aggregator-before.sqlite3"', workflow)
            self.assertIn("APPEND_ONLY_BASELINE_DB: ${{ runner.temp }}/aggregator-before.sqlite3", workflow)


if __name__ == "__main__":
    unittest.main()
