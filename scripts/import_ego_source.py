#!/usr/bin/env python3
"""Import an ego-browser README capture as a versioned upstream source run.

The browser capture remains an immutable raw snapshot. Linked GitHub
repository metadata is fetched separately and stored as dated item metrics;
an unavailable repository never becomes a zero-valued metric.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any

import collect
import monitor_sources


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"


def clean_description(value: Any) -> str | None:
    """Normalize the separator left by a README DOM entry."""

    text = str(value or "").strip().lstrip("-–—: \\t")
    return text[:1200] or None


def read_capture(path: Path) -> dict[str, Any]:
    """Load and validate the browser capture envelope."""

    value = json.loads(path.read_text(encoding="utf-8"))
    capture = value.get("capture") if isinstance(value, dict) else None
    source = value.get("source") if isinstance(value, dict) else None
    if not isinstance(capture, dict) or not isinstance(source, dict):
        raise ValueError("capture must contain source and capture objects")
    if source.get("platform") != "github" or not source.get("repository"):
        raise ValueError("capture source must be a GitHub repository")
    if not isinstance(capture.get("entries"), list):
        raise ValueError("capture.entries must be a list")
    return value


def normalize_entry(entry: dict[str, Any]) -> dict[str, Any] | None:
    """Convert one DOM entry to the source-monitor entry format."""

    raw_url = str(entry.get("entry_url") or "")
    slug = monitor_sources.github_repo(raw_url)
    if not slug:
        return None
    return {
        "name": str(entry.get("entry_name") or slug),
        "owner": slug.split("/", 1)[0],
        "url": monitor_sources.github_url(slug),
        "source_url": raw_url,
        "category": str(entry.get("category") or "uncategorized"),
        "description": clean_description(entry.get("description")),
        "install": None,
        "source_path": entry.get("source_path") or "README.md",
        "source_line": entry.get("source_line"),
        "entry_kind": entry.get("entry_kind") or "candidate",
    }


def enrich_entry(entry: dict[str, Any], checked_at: str, token: str | None) -> dict[str, Any]:
    """Fetch one linked repository's public metadata when available."""

    slug = monitor_sources.github_repo(str(entry["url"]))
    if not slug:
        return entry
    try:
        metadata = monitor_sources.api_json(f"https://api.github.com/repos/{slug}", token)
    except Exception as error:
        entry["enrichment_status"] = "error"
        entry["enrichment_error"] = str(error)
        return entry
    entry["repository_metadata"] = monitor_sources.compact_repo_meta(metadata, checked_at, None, None)
    entry["metrics"] = {
        "stars": metadata.get("stargazers_count"),
        "forks": metadata.get("forks_count"),
        "open_issues": metadata.get("open_issues_count"),
        "metric_source": "GitHub repository API via ego-browser source capture",
        "observed_at": checked_at,
    }
    entry["enrichment_status"] = "ok"
    return entry


def enrich_entries(entries: list[dict[str, Any]], checked_at: str, token: str | None, limit: int) -> tuple[list[dict[str, Any]], int]:
    """Enrich a bounded or complete entry set concurrently."""

    selected = entries if limit <= 0 else entries[:limit]
    selected_ids = {id(entry) for entry in selected}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(enrich_entry, entry, checked_at, token): entry for entry in selected}
        for future in as_completed(futures):
            future.result()
    return entries, sum(entry.get("enrichment_status") == "ok" for entry in entries if id(entry) in selected_ids)


def build_payload(capture: dict[str, Any], token: str | None, enrich_limit: int) -> dict[str, Any]:
    """Build the normalized import payload from one browser capture."""

    source = capture["source"]
    browser_capture = capture["capture"]
    checked_at = str(capture.get("collected_at") or browser_capture.get("captured_at") or collect.utc_now())
    source_repo = str(source["repository"])
    repository_api = capture.get("repository_api") or {}
    entries: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for raw_entry in browser_capture["entries"]:
        if not isinstance(raw_entry, dict):
            continue
        entry = normalize_entry(raw_entry)
        if entry is None:
            continue
        key = (str(entry["source_url"]), str(entry["category"]))
        if key in seen:
            continue
        seen.add(key)
        entries.append(entry)
    entries, enriched = enrich_entries(entries, checked_at, token, enrich_limit)
    license_data = repository_api.get("license") or {}
    source_descriptor = {
        "full_name": repository_api.get("full_name") or source_repo,
        "html_url": repository_api.get("html_url") or source["url"],
        "default_branch": repository_api.get("default_branch") or "main",
        "description": repository_api.get("description"),
        "license_spdx": license_data.get("spdx_id"),
        "stars": repository_api.get("stargazers_count"),
        "forks": repository_api.get("forks_count"),
        "open_issues": repository_api.get("open_issues_count"),
        "pushed_at": repository_api.get("pushed_at"),
        "last_checked_at": checked_at,
        "readme_path": "README.md",
        "readme_sha": hashlib.sha256(str(browser_capture.get("article_text") or "").encode("utf-8")).hexdigest(),
        "source_kind": "community-index",
        "status": "ok",
        "entry_count": len(entries),
        "metadata_enriched": enriched,
        "entry_sources": [{
            "source_ref": "README.md",
            "kind": "markdown",
            "status": "ok",
            "entry_count": len(entries),
        }],
        "files": {"README.md": browser_capture.get("article_text") or ""},
        "tree": [],
        "entries": entries,
    }
    source_item = {
        "platform": "github",
        "external_id": source_descriptor["full_name"],
        "url": source_descriptor["html_url"],
        "item_type": "source-repository",
        "title": source_descriptor["full_name"],
        "author": str(source_descriptor["full_name"]).split("/", 1)[0],
        "content_text": source_descriptor.get("description"),
        "media_kind": "none",
        "metrics": {
            "stars": source_descriptor.get("stars"),
            "forks": source_descriptor.get("forks"),
            "open_issues": source_descriptor.get("open_issues"),
            "metric_source": "GitHub repository API via ego-browser source capture",
            "observed_at": checked_at,
        },
        "tags": ["upstream-index", "source-repository", "community-index"],
    }
    items = [source_item, *[monitor_sources.item_for_entry(entry, checked_at, source_repo) for entry in entries]]
    observation = {
        "platform": "github",
        "query": f"upstream:{source_repo}",
        "source_url": source_descriptor["html_url"],
        "collected_at": checked_at,
        "collector": "scripts/import_ego_source.py",
        "method": "ego-browser visible README DOM + GitHub repository API metadata",
        "status": "ok",
        "result_count": len(entries),
        "notes": "The browser capture is preserved as raw evidence; linked repository metrics are dated observations.",
        "items": items,
    }
    return {"collected_at": checked_at, "collector": "scripts/import_ego_source.py", "repositories": [source_descriptor], "observations": [observation]}


def main() -> int:
    """Import one immutable capture and rebuild its source relationships."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, required=True, help="ego-browser capture envelope")
    parser.add_argument("--db", type=Path, default=DB_PATH)
    parser.add_argument("--enrich-limit", type=int, default=0, help="linked repositories to enrich; 0 means all")
    parser.add_argument("--normalized-output", type=Path, help="derived import payload path")
    args = parser.parse_args()
    capture = read_capture(args.raw)
    token = monitor_sources.github_token()
    payload = build_payload(capture, token, args.enrich_limit)
    normalized_path = args.normalized_output or args.raw.with_name(f"{args.raw.stem}-payload.json")
    collect.dump_json(normalized_path, payload)
    collect.init_db(args.db)
    with collect.connect(args.db) as connection:
        run_id, version, _ = collect.begin_collection_run(connection, "ego-browser-source-capture")
        stats = collect.ImportStats(raw_files_seen=1)
        try:
            stats = collect.import_payload(connection, payload, run_id, normalized_path)
            original_raw_id, _sha, _new = collect.store_raw_snapshot(connection, args.raw, run_id, payload["collected_at"])
            record_upstream_repositories(connection, payload, original_raw_id)
            stats.raw_files_seen = 2
            collect.finish_collection_run(connection, run_id, stats)
        except Exception as error:
            collect.finish_collection_run(connection, run_id, stats, "failed", str(error))
            connection.commit()
            raise
    print(f"imported {len(payload['repositories'][0]['entries'])} entries in {version}; enriched {payload['repositories'][0]['metadata_enriched']}; raw capture: {args.raw}")
    return 0


def record_upstream_repositories(connection: sqlite3.Connection, payload: dict[str, Any], raw_snapshot_id: int) -> None:
    """Persist browser-captured Listings through the shared history writer."""

    monitor_sources.record_upstream_repositories(connection, payload, raw_snapshot_id)


if __name__ == "__main__":
    raise SystemExit(main())
