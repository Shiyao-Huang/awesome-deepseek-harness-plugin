#!/usr/bin/env python3
"""Monitor community indexes and import their public plugin references.

The monitor stores repository metadata, selected README/data files, and
normalized plugin links. It does not clone or execute arbitrary third-party
code; source repositories remain the installation and review authority.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import html
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urlsplit
from urllib.request import Request, urlopen

import collect


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
CONFIG_PATH = ROOT / "config" / "sources.json"
RAW_DIR = ROOT / "data" / "raw"
MAX_FILE_CHARS = 400_000
RESERVED_GITHUB_PATHS = {"topics", "orgs", "search", "sponsors", "settings", "marketplace"}


def utc_now() -> str:
    """Return a second-precision UTC timestamp."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def github_token() -> str | None:
    """Read an Actions token or the local GitHub CLI token when available."""

    for name in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(name):
            return os.environ[name]
    try:
        result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() or None


def request_bytes(url: str, token: str | None = None) -> bytes:
    """Fetch a public GitHub endpoint with bounded network time."""

    gh_endpoint: str | None = None
    accept = "application/vnd.github+json"
    parsed = urlsplit(url)
    if parsed.netloc == "api.github.com":
        gh_endpoint = parsed.path.removeprefix("/")
        if parsed.query:
            gh_endpoint = f"{gh_endpoint}?{parsed.query}"
    elif parsed.netloc == "raw.githubusercontent.com":
        parts = [unquote(part) for part in parsed.path.split("/") if part]
        if len(parts) >= 4:
            owner, repo, branch = parts[:3]
            content_path = "/".join(parts[3:])
            gh_endpoint = f"repos/{owner}/{repo}/contents/{quote(content_path, safe='/')}?ref={quote(branch, safe='')}"
            accept = "application/vnd.github.raw+json"
    if gh_endpoint:
        env = dict(os.environ)
        if token:
            env["GH_TOKEN"] = token
        try:
            result = subprocess.run(
                ["gh", "api", gh_endpoint, "-H", f"Accept: {accept}"],
                capture_output=True,
                timeout=20,
                env=env,
            )
            if result.returncode == 0:
                return result.stdout
        except (OSError, subprocess.SubprocessError):
            pass

    headers = {
        "Accept": "application/vnd.github+json, application/json",
        "User-Agent": "awesome-deepseek-harness-plugin/source-monitor",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=12) as response:
        return response.read()


def api_json(url: str, token: str | None) -> dict[str, Any]:
    """Fetch and decode one GitHub JSON response."""

    return json.loads(request_bytes(url, token).decode("utf-8"))


def raw_text(url: str, token: str | None) -> str:
    """Fetch one selected source file without interpreting executable content."""

    return request_bytes(url, token).decode("utf-8", "replace")[:MAX_FILE_CHARS]


def github_repo(url: str) -> str | None:
    """Extract an owner/repository slug from a GitHub URL."""

    parts = [part for part in urlsplit(url).path.split("/") if part]
    if len(parts) < 2 or parts[0].lower() in RESERVED_GITHUB_PATHS:
        return None
    owner, name = parts[0], parts[1].removesuffix(".git")
    if not owner or not name or owner.lower() == "features":
        return None
    return f"{owner}/{name}"


def github_url(slug: str) -> str:
    """Return the canonical public repository URL for a slug."""

    return f"https://github.com/{slug}"


def strip_markdown(value: str) -> str:
    """Keep a compact plain-text description from a Markdown line."""

    value = re.sub(r"!\[[^]]*\]\([^)]*\)", "", value)
    value = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"[`*_>#]", "", value)
    return html.unescape(re.sub(r"\s+", " ", value)).strip(" |-—")


def entry_kind(category: str, name: str, description: str) -> str:
    """Classify a linked repository without asserting that it is verified."""

    text = f"{category} {name} {description}".lower()
    if any(term in text for term in ("ecosystem index", "awesome list", "directory", "registry", "marketplace")):
        return "index"
    if any(term in text for term in ("launcher", "client", "desktop app")):
        return "client-or-launcher"
    if "resource" in text or "tutorial" in text or "documentation" in text:
        return "resource"
    if name.lower().startswith(("dsh-", "deepseek-harness-", "awesome-")) or "plugin" in text:
        return "plugin-candidate"
    return "candidate"


def markdown_entries(text: str, path: str, source_repo: str) -> list[dict[str, Any]]:
    """Extract repository links and nearby descriptions from a Markdown file."""

    pattern = re.compile(r"\[([^]]+)\]\((https://github\.com/[^)\s]+)\)")
    entries: list[dict[str, Any]] = []
    category = "uncategorized"
    for line_number, line in enumerate(text.splitlines(), 1):
        heading = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading:
            category = strip_markdown(heading.group(1))
        cells = [strip_markdown(cell) for cell in line.split("|")]
        for match in pattern.finditer(line):
            slug = github_repo(match.group(2))
            if not slug or slug.lower() == source_repo.lower():
                continue
            name = strip_markdown(match.group(1))
            description = ""
            if len(cells) >= 2:
                description = cells[1]
            if not description:
                tail = line[match.end():]
                description = strip_markdown(re.split(r"\s+-\s+|\s+—\s+", tail, maxsplit=1)[-1])
            install_match = re.search(r"`([^`]*(?:dsh plugin|npm (?:i|install)|pnpm add|npx )[^`]*)`", line, re.I)
            entries.append({
                "name": name or slug.rsplit("/", 1)[-1],
                "owner": slug.split("/", 1)[0],
                "url": github_url(slug),
                "category": category,
                "description": description[:1200] or None,
                "install": install_match.group(1) if install_match else None,
                "source_path": path,
                "source_line": line_number,
                "entry_kind": "core-resource" if slug == "deepseek-ai/deepseek-harness" else entry_kind(category, name, description),
            })
    return dedupe_entries(entries)


def structured_entries(value: dict[str, Any], path: str) -> list[dict[str, Any]]:
    """Normalize a structured community plugin registry such as plugins.json."""

    entries: list[dict[str, Any]] = []
    for plugin in value.get("plugins", []):
        if not isinstance(plugin, dict) or not plugin.get("url"):
            continue
        description = plugin.get("description") or {}
        if isinstance(description, dict):
            description = description.get("zh") or description.get("en") or ""
        entries.append({
            "name": str(plugin.get("name") or plugin["url"].rstrip("/").rsplit("/", 1)[-1]),
            "owner": plugin.get("owner"),
            "url": plugin["url"],
            "category": plugin.get("category") or "uncategorized",
            "description": str(description)[:1200] or None,
            "install": plugin.get("install"),
            "added": plugin.get("added"),
            "npm": plugin.get("npm"),
            "source_path": path,
            "source_line": None,
            "entry_kind": "plugin-candidate",
        })
    return dedupe_entries(entries)


def dedupe_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep the first source location for each repository/category pair."""

    result: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for entry in entries:
        slug = github_repo(str(entry.get("url") or ""))
        key = (slug or str(entry.get("url")), str(entry.get("category") or "uncategorized"))
        if key in seen:
            continue
        seen.add(key)
        result.append(entry)
    return result


def selected_paths(tree: dict[str, Any], configured: list[str]) -> list[str]:
    """Select README/registry files from a recursive tree manifest."""

    available = {str(row.get("path")) for row in tree.get("tree", []) if row.get("type") == "blob"}
    result = [path for path in configured if path in available]
    return result or [path for path in ("README.md", "README.zh.md", "README.zh-CN.md") if path in available]


def compact_repo_meta(meta: dict[str, Any], checked_at: str, readme_path: str | None, readme_sha: str | None) -> dict[str, Any]:
    """Keep stable public repository metadata in the raw snapshot."""

    license_data = meta.get("license") or {}
    return {
        "full_name": meta.get("full_name"),
        "html_url": meta.get("html_url"),
        "default_branch": meta.get("default_branch") or "main",
        "description": meta.get("description"),
        "license_spdx": license_data.get("spdx_id"),
        "stars": meta.get("stargazers_count"),
        "forks": meta.get("forks_count"),
        "open_issues": meta.get("open_issues_count"),
        "pushed_at": meta.get("pushed_at"),
        "last_checked_at": checked_at,
        "readme_path": readme_path,
        "readme_sha": readme_sha,
        "source_kind": "community-index",
        "status": "ok",
    }


def monitor_repository(repo: str, configured_paths: list[str], token: str | None, checked_at: str, metadata_limit: int) -> dict[str, Any]:
    """Fetch one source repository and normalize its public entries."""

    meta = api_json(f"https://api.github.com/repos/{repo}", token)
    branch = str(meta.get("default_branch") or "main")
    tree = api_json(f"https://api.github.com/repos/{repo}/git/trees/{quote(branch, safe='')}?recursive=1", token)
    manifest = [{"path": row.get("path"), "sha": row.get("sha"), "type": row.get("type")} for row in tree.get("tree", [])]
    paths = selected_paths(tree, configured_paths)
    files: dict[str, str] = {}
    entries: list[dict[str, Any]] = []
    for path in paths:
        try:
            files[path] = raw_text(f"https://raw.githubusercontent.com/{repo}/{quote(branch, safe='')}/{quote(path, safe='/')}", token)
        except (HTTPError, URLError, TimeoutError):
            continue
        if path.endswith(".json"):
            try:
                entries.extend(structured_entries(json.loads(files[path]), path))
            except json.JSONDecodeError:
                pass
        elif path.lower().endswith((".md", ".markdown")):
            entries.extend(markdown_entries(files[path], path, repo))
    entries = dedupe_entries(entries)
    def enrich(entry: dict[str, Any]) -> dict[str, Any]:
        """Best-effort enrich one entry without blocking the source snapshot."""

        slug = github_repo(str(entry["url"]))
        if not slug:
            return entry
        try:
            linked = api_json(f"https://api.github.com/repos/{slug}", token)
        except Exception:
            return entry
        entry["repository_metadata"] = compact_repo_meta(linked, checked_at, None, None)
        entry["metrics"] = {
            "stars": linked.get("stargazers_count"),
            "forks": linked.get("forks_count"),
            "open_issues": linked.get("open_issues_count"),
            "metric_source": "GitHub repository API via upstream index",
            "observed_at": checked_at,
        }
        return entry

    candidates = entries[:metadata_limit]
    if candidates:
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(enrich, entry) for entry in candidates]
            for future in as_completed(futures):
                future.result()
    readme_path = next((path for path in paths if path.lower() == "readme.md"), paths[0] if paths else None)
    readme_sha = next((row["sha"] for row in manifest if row["path"] == readme_path), None)
    source = compact_repo_meta(meta, checked_at, readme_path, readme_sha)
    source["entry_count"] = len(entries)
    source["tree_file_count"] = len(manifest)
    source["files"] = files
    source["tree"] = manifest
    source["entries"] = entries
    return source


def item_for_entry(entry: dict[str, Any], checked_at: str, source_repo: str) -> dict[str, Any]:
    """Convert one upstream link into the shared item format."""

    meta = entry.get("repository_metadata") or {}
    slug = github_repo(str(entry.get("url") or "")) or str(entry.get("url"))
    return {
        "platform": "github",
        "external_id": slug,
        "url": github_url(slug) if "/" in slug else entry.get("url"),
        "item_type": "plugin" if entry.get("entry_kind") == "plugin-candidate" else "ecosystem-reference",
        "title": entry.get("name") or slug,
        "author": entry.get("owner") or (slug.split("/", 1)[0] if "/" in slug else None),
        "content_text": entry.get("description") or meta.get("description"),
        "published_label": entry.get("added"),
        "media_kind": "none",
        "metrics": entry.get("metrics") or {},
        "tags": ["upstream-index", source_repo, str(entry.get("category") or "uncategorized"), str(entry.get("entry_kind") or "candidate")],
        "source_entry": entry,
    }


def build_payload(config: dict[str, Any], token: str | None) -> dict[str, Any]:
    """Fetch configured sources and return a normalized raw payload."""

    checked_at = utc_now()
    limits = config.get("limits") or {}
    metadata_limit = int(limits.get("plugin_metadata", 100))
    repositories: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []
    for source in config.get("github_repositories", []):
        repo = str(source["repo"])
        try:
            descriptor = monitor_repository(repo, list(source.get("files", [])), token, checked_at, metadata_limit)
            repositories.append(descriptor)
            source_item = {
                "platform": "github", "external_id": repo, "url": descriptor["html_url"], "item_type": "source-repository",
                "title": repo, "author": repo.split("/", 1)[0], "content_text": descriptor.get("description"),
                "media_kind": "none", "metrics": {"stars": descriptor.get("stars"), "forks": descriptor.get("forks"), "open_issues": descriptor.get("open_issues"), "metric_source": "GitHub repository API", "observed_at": checked_at},
                "tags": ["upstream-index", "source-repository", "community-index"],
            }
            items = [source_item, *[item_for_entry(entry, checked_at, repo) for entry in descriptor["entries"]]]
            observations.append({
                "platform": "github", "query": f"upstream:{repo}", "source_url": descriptor["html_url"], "collected_at": checked_at,
                "collector": "scripts/monitor_sources.py", "method": "GitHub repository API + public raw files", "status": "ok",
                "result_count": len(descriptor["entries"]), "notes": "Entries are upstream references; repository source remains authoritative.", "items": items,
            })
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, KeyError) as error:
            observations.append({
                "platform": "github", "query": f"upstream:{repo}", "source_url": github_url(repo), "collected_at": checked_at,
                "collector": "scripts/monitor_sources.py", "method": "GitHub repository API + public raw files", "status": "error",
                "result_count": 0, "notes": str(error), "items": [],
            })
    return {"collected_at": checked_at, "collector": "scripts/monitor_sources.py", "repositories": repositories, "observations": observations}


def record_upstream_repositories(connection: Any, payload: dict[str, Any], raw_snapshot_id: int) -> None:
    """Persist source repositories and link their entries to normalized items."""

    for descriptor in payload.get("repositories", []):
        connection.execute(
            """
            INSERT INTO upstream_repositories(
                full_name, source_url, default_branch, description, license_spdx, stars, forks,
                open_issues, pushed_at, last_checked_at, readme_path, readme_sha,
                source_kind, status, raw_snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(full_name) DO UPDATE SET
                source_url=excluded.source_url, default_branch=excluded.default_branch,
                description=excluded.description, license_spdx=excluded.license_spdx,
                stars=excluded.stars, forks=excluded.forks, open_issues=excluded.open_issues,
                pushed_at=excluded.pushed_at, last_checked_at=excluded.last_checked_at,
                readme_path=excluded.readme_path, readme_sha=excluded.readme_sha,
                source_kind=excluded.source_kind, status=excluded.status, raw_snapshot_id=excluded.raw_snapshot_id
            """,
            (descriptor["full_name"], descriptor["html_url"], descriptor["default_branch"], descriptor.get("description"), descriptor.get("license_spdx"), descriptor.get("stars"), descriptor.get("forks"), descriptor.get("open_issues"), descriptor.get("pushed_at"), descriptor["last_checked_at"], descriptor.get("readme_path"), descriptor.get("readme_sha"), descriptor.get("source_kind", "community-index"), descriptor.get("status", "ok"), raw_snapshot_id),
        )
        repo_id = int(connection.execute("SELECT id FROM upstream_repositories WHERE full_name = ?", (descriptor["full_name"],)).fetchone()[0])
        connection.execute("DELETE FROM upstream_entries WHERE repository_id = ?", (repo_id,))
        for entry in descriptor.get("entries", []):
            entry_url = collect.canonical_url(str(entry.get("url") or ""))
            item_row = connection.execute("SELECT id FROM items WHERE canonical_url = ?", (entry_url,)).fetchone()
            connection.execute(
                """
                INSERT INTO upstream_entries(
                    repository_id, item_id, entry_name, entry_url, entry_kind, category,
                    description, install_hint, source_path, source_line, first_seen_at, last_seen_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(repository_id, entry_url, category) DO UPDATE SET
                    item_id=excluded.item_id, entry_name=excluded.entry_name, entry_kind=excluded.entry_kind,
                    description=excluded.description, install_hint=excluded.install_hint,
                    source_path=excluded.source_path, source_line=excluded.source_line,
                    last_seen_at=excluded.last_seen_at
                """,
                (repo_id, int(item_row[0]) if item_row else None, entry.get("name") or entry_url, entry_url, entry.get("entry_kind", "candidate"), entry.get("category"), entry.get("description"), entry.get("install"), entry.get("source_path"), entry.get("source_line"), descriptor["last_checked_at"], descriptor["last_checked_at"]),
            )


def main() -> int:
    """Monitor sources, import the raw snapshot, and update source tables."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=CONFIG_PATH)
    parser.add_argument("--db", type=Path, default=DB_PATH)
    parser.add_argument("--raw-output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    token = github_token()
    payload = build_payload(config, token)
    collect.dump_json(args.raw_output, payload)
    collect.init_db(args.db)
    with collect.connect(args.db) as connection:
        run_id, version, _ = collect.begin_collection_run(connection, "source-monitor")
        stats = collect.ImportStats(raw_files_seen=1)
        try:
            stats = collect.import_payload(connection, payload, run_id, args.raw_output)
            stats.raw_files_seen = 1
            raw_sha = collect.sha256_file(args.raw_output)
            raw_snapshot_id = int(connection.execute("SELECT id FROM raw_snapshots WHERE raw_sha256 = ?", (raw_sha,)).fetchone()[0])
            record_upstream_repositories(connection, payload, raw_snapshot_id)
            collect.finish_collection_run(connection, run_id, stats)
        except Exception as error:
            collect.finish_collection_run(connection, run_id, stats, "failed", str(error))
            connection.commit()
            raise
    print(f"monitored {len(payload.get('repositories', []))} upstream repositories in {version}; raw snapshot: {args.raw_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
