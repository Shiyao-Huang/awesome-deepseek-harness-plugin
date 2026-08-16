"""Regression tests for stable GitHub Release publication."""

from __future__ import annotations

import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLISHER = ROOT / "scripts" / "publish_release_assets.sh"


class ReleasePublisherTests(unittest.TestCase):
    def test_existing_release_survives_extended_transient_probe_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            command_log = temporary / "calls.log"
            fake_gh = temporary / "gh"
            fake_gh.write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env bash
                    set -eu
                    printf '%s\n' "$*" >> "$COMMAND_LOG"
                    case "$1 $2" in
                      "release upload")
                        attempts_file="$COMMAND_LOG.upload-attempts"
                        attempts=0
                        if [[ -f "$attempts_file" ]]; then
                          attempts=$(<"$attempts_file")
                        fi
                        attempts=$((attempts + 1))
                        printf '%s' "$attempts" > "$attempts_file"
                        [[ "$attempts" -gt 4 ]]
                        ;;
                      "release view")
                        exit 1
                        ;;
                      "release create")
                        echo "a release with the same tag name already exists" >&2
                        exit 1
                        ;;
                      "release edit")
                        exit 0
                        ;;
                    esac
                    """
                ),
                encoding="utf-8",
            )
            fake_gh.chmod(0o755)
            environment = os.environ | {
                "COMMAND_LOG": str(command_log),
                "PATH": f"{temporary}:{os.environ['PATH']}",
                "RELEASE_RETRY_DELAY": "0",
            }

            result = subprocess.run(
                ["bash", str(PUBLISHER), "test publication note"],
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            calls = command_log.read_text(encoding="utf-8").splitlines()
            self.assertEqual(
                [call.split()[1] for call in calls],
                [
                    "upload", "view", "create",
                    "upload", "view", "create",
                    "upload", "view", "create",
                    "upload", "view", "create",
                    "upload", "edit",
                ],
            )


if __name__ == "__main__":
    unittest.main()
