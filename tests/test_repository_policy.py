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


if __name__ == "__main__":
    unittest.main()
