#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <release-note>" >&2
  exit 2
fi

note=$1
tag=${DATASET_RELEASE_TAG:-dataset-latest}
retry_delay=${RELEASE_RETRY_DELAY:-2}
max_attempts=${RELEASE_MAX_ATTEMPTS:-8}
assets=(data/aggregator.sqlite3 data/aggregator-full.sqlite3.zst)

if [[ ! $retry_delay =~ ^[0-9]+$ || ! $max_attempts =~ ^[1-9][0-9]*$ ]]; then
  echo "RELEASE_RETRY_DELAY must be non-negative and RELEASE_MAX_ATTEMPTS must be positive" >&2
  exit 2
fi

for ((attempt = 1; attempt <= max_attempts; attempt++)); do
  if gh release upload "$tag" "${assets[@]}" --clobber; then
    if gh release edit "$tag" \
      --title "Latest DeepSeek Harness ecosystem dataset" \
      --notes "$note" \
      --latest; then
      exit 0
    fi
  elif ! gh release view "$tag" >/dev/null 2>&1; then
    if ! gh release create "$tag" \
      --target main \
      --title "Latest DeepSeek Harness ecosystem dataset" \
      --notes "$note" \
      --latest; then
      echo "Release creation raced another publisher; retrying ($attempt/$max_attempts)" >&2
    fi
  fi

  if [[ $attempt -lt $max_attempts ]]; then
    sleep $((retry_delay * attempt))
  fi
done

echo "Failed to publish stable SQLite assets after $max_attempts attempts" >&2
exit 1
