#!/usr/bin/env bash

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <commit-message> <path> [<path> ...]" >&2
  exit 2
fi

commit_message=$1
shift
stage_paths=("$@")
source_root=$(git rev-parse --show-toplevel)
source_database="$source_root/data/aggregator.sqlite3"
full_database="$source_root/data/aggregator-full.sqlite3.zst"
public_database="$source_root/data/aggregator.sqlite3"
max_attempts=${GENERATED_PUSH_MAX_ATTEMPTS:-3}
publish_worktree=""

if [[ ! $max_attempts =~ ^[1-9][0-9]*$ ]]; then
  echo "GENERATED_PUSH_MAX_ATTEMPTS must be positive" >&2
  exit 2
fi
if [[ ! -f $source_database ]]; then
  echo "missing complete SQLite database: $source_database" >&2
  exit 1
fi

cleanup_worktree() {
  if [[ -n $publish_worktree ]]; then
    git -C "$source_root" worktree remove --force "$publish_worktree" >/dev/null 2>&1 || true
    publish_worktree=""
  fi
}
trap cleanup_worktree EXIT

for ((attempt = 1; attempt <= max_attempts; attempt++)); do
  git -C "$source_root" fetch origin main
  publish_worktree=$(mktemp -d "${TMPDIR:-/tmp}/deeplugin-publish.XXXXXX")
  git -C "$source_root" worktree add --detach "$publish_worktree" origin/main

  if [[ -d $source_root/data/raw ]]; then
    rsync -a "$source_root/data/raw/" "$publish_worktree/data/raw/"
  fi
  cp "$source_database" "$publish_worktree/data/aggregator.sqlite3"

  python3 "$publish_worktree/scripts/build_fork_index.py"
  make -C "$publish_worktree" build
  make -C "$publish_worktree" archive-full
  make -C "$publish_worktree" public-db
  python3 "$publish_worktree/scripts/validate.py"
  if [[ -n ${APPEND_ONLY_BASELINE_DB:-} ]]; then
    if [[ ! -f $APPEND_ONLY_BASELINE_DB ]]; then
      echo "missing append-only baseline database: $APPEND_ONLY_BASELINE_DB" >&2
      exit 1
    fi
    python3 "$publish_worktree/scripts/validate_append_only.py" \
      --before "$APPEND_ONLY_BASELINE_DB" \
      --after "$publish_worktree/data/aggregator.sqlite3"
  fi

  git -C "$publish_worktree" add -- "${stage_paths[@]}"
  if git -C "$publish_worktree" diff --cached --quiet; then
    cp "$publish_worktree/data/aggregator.sqlite3" "$public_database"
    cp "$publish_worktree/data/aggregator-full.sqlite3.zst" "$full_database"
    echo "No generated index changes"
    exit 0
  fi

  git -C "$publish_worktree" config user.name "github-actions[bot]"
  git -C "$publish_worktree" config user.email "41898282+github-actions[bot]@users.noreply.github.com"
  git -C "$publish_worktree" commit -m "$commit_message"
  if git -C "$publish_worktree" push origin HEAD:main; then
    cp "$publish_worktree/data/aggregator.sqlite3" "$public_database"
    cp "$publish_worktree/data/aggregator-full.sqlite3.zst" "$full_database"
    exit 0
  fi

  echo "main advanced during push; rebuilding from the new main ($attempt/$max_attempts)" >&2
  cleanup_worktree
done

echo "Failed to publish generated index after $max_attempts attempts" >&2
exit 1
