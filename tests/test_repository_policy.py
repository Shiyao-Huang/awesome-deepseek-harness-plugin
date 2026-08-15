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


if __name__ == "__main__":
    unittest.main()
