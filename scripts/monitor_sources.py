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
import shlex
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
MAX_FILE_BYTES = 5_000_000
RESERVED_GITHUB_PATHS = {"topics", "orgs", "search", "sponsors", "settings", "marketplace"}
SOURCE_COLLECTORS = {"scripts/monitor_sources.py", "scripts/import_ego_source.py"}
LISTING_METRIC_SOURCES = {
    "GitHub repository API via upstream index",
    "GitHub repository API via ego-browser source capture",
}


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
    if token and parsed.hostname in {"api.github.com", "raw.githubusercontent.com"}:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=12) as response:
        return response.read()


def api_json(url: str, token: str | None) -> dict[str, Any]:
    """Fetch and decode one GitHub JSON response."""

    return json.loads(request_bytes(url, token).decode("utf-8"))


def raw_text(url: str, token: str | None) -> str:
    """Fetch one selected source file without interpreting executable content."""

    payload = request_bytes(url, token)
    if len(payload) > MAX_FILE_BYTES:
        raise ValueError(f"source file exceeds {MAX_FILE_BYTES} bytes: {url}")
    return payload.decode("utf-8", "replace")


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
                "source_url": match.group(2),
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
        if not isinstance(plugin, dict):
            continue
        url = plugin.get("url") or plugin.get("homepage")
        if not url:
            continue
        description_value = plugin.get("description") or ""
        if isinstance(description_value, dict):
            description_i18n = {
                language: str(text)
                for language, text in description_value.items()
                if language in {"en", "zh"} and text
            }
        else:
            description_i18n = {"en": str(description_value)} if description_value else {}
            if plugin.get("description_zh"):
                description_i18n["zh"] = str(plugin["description_zh"])
        description = description_i18n.get("zh") or description_i18n.get("en") or ""
        install_value = plugin.get("install")
        install_hint: str | None = None
        install_spec: str | None = None
        install_target: str | None = None
        if isinstance(install_value, dict):
            install_spec = str(install_value.get("spec") or "").strip() or None
            install_target = str(install_value.get("target") or "").strip() or None
            if install_spec:
                install_hint = f"dsh plugin --profile web add {install_spec}"
        elif isinstance(install_value, str):
            install_hint = install_value.strip() or None
            if install_hint:
                try:
                    tokens = shlex.split(install_hint)
                except ValueError:
                    tokens = []
                if len(tokens) >= 2 and tokens[-2] == "add":
                    install_spec = tokens[-1]
                    install_target = "git" if install_spec.startswith("github:") else "npm"
        entries.append({
            "registry_id": plugin.get("id"),
            "name": str(plugin.get("name") or str(url).rstrip("/").rsplit("/", 1)[-1]),
            "owner": plugin.get("owner") or plugin.get("author"),
            "url": url,
            "page": plugin.get("page"),
            "category": plugin.get("category") or "uncategorized",
            "description": str(description)[:1200] or None,
            "description_i18n": description_i18n,
            "install": install_hint,
            "install_spec": install_spec,
            "install_target": install_target,
            "added": plugin.get("added"),
            "npm": plugin.get("npm"),
            "stars": plugin.get("stars"),
            "version": plugin.get("version"),
            "verified": plugin.get("verified"),
            "tags": plugin.get("tags") if isinstance(plugin.get("tags"), list) else [],
            "registry_source": plugin.get("source") if isinstance(plugin.get("source"), dict) else {},
            "source_path": path,
            "source_line": None,
            "entry_kind": "plugin-candidate",
        })
    return dedupe_entries(entries)


def dedupe_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge duplicate listings while preserving distinct monorepo install specs."""

    result: list[dict[str, Any]] = []
    for entry in entries:
        canonical = collect.canonical_url(str(entry.get("url") or entry.get("source_url") or ""))
        install_spec = str(entry.get("install_spec") or "")
        duplicate_index = next(
            (
                index
                for index, existing in enumerate(result)
                if collect.canonical_url(str(existing.get("url") or existing.get("source_url") or "")) == canonical
                and (
                    not install_spec
                    or not existing.get("install_spec")
                    or str(existing.get("install_spec")) == install_spec
                )
            ),
            None,
        )
        if duplicate_index is None:
            result.append(entry)
            continue
        merged = dict(result[duplicate_index])
        merged.update({key: value for key, value in entry.items() if value not in (None, "", [], {})})
        result[duplicate_index] = merged
    return result


def is_registry_ref(source_ref: str) -> bool:
    """Return whether a configured JSON path is intended as a plugin registry."""

    name = urlsplit(source_ref).path.rsplit("/", 1)[-1].lower()
    return name.endswith(".json") and ("plugin" in name or "registry" in name)


def registry_snapshot(value: Any, source_ref: str) -> dict[str, Any]:
    """Return source-attributed metadata for one structured registry capture."""

    errors: list[str] = []
    if not isinstance(value, dict):
        return {
            "source_ref": source_ref,
            "status": "invalid",
            "format_version": None,
            "declared_count": None,
            "actual_count": None,
            "updated": None,
            "metadata": {},
            "error": "registry root is not an object",
        }
    plugins_value = value.get("plugins")
    if not isinstance(plugins_value, list):
        errors.append("plugins is not an array")
        plugins: list[Any] = []
        actual_count: int | None = None
    else:
        plugins = plugins_value
        actual_count = len(plugins)
    declared_count = value.get("count") if isinstance(value.get("count"), int) else None
    if declared_count is not None and actual_count is not None and declared_count != actual_count:
        errors.append(f"declared count {declared_count} does not match {actual_count} plugins")
    format_version = value.get("version") if isinstance(value.get("version"), int) else 1
    if format_version == 2:
        seen_ids: set[str] = set()
        seen_specs: set[str] = set()
        for index, plugin in enumerate(plugins):
            if not isinstance(plugin, dict):
                errors.append(f"plugin at index {index} is not an object")
                continue
            plugin_id = str(plugin.get("id") or "").strip()
            install = plugin.get("install") if isinstance(plugin.get("install"), dict) else {}
            install_spec = str(install.get("spec") or "").strip()
            if not plugin_id:
                errors.append(f"plugin at index {index} has no id")
            elif plugin_id in seen_ids:
                errors.append(f"duplicate plugin id {plugin_id}")
            else:
                seen_ids.add(plugin_id)
            if not install_spec:
                errors.append(f"listing {plugin_id or index} has no install spec")
            elif install_spec in seen_specs:
                errors.append(f"duplicate install spec {install_spec}")
            else:
                seen_specs.add(install_spec)
            if plugin.get("verified") is True and not plugin.get("version"):
                errors.append(f"verified listing {plugin_id or index} has no version")
    status = "invalid" if errors else "ok"
    metadata = {
        key: value[key]
        for key in ("name", "url", "source", "updated", "count", "verifiedCount", "categories", "note")
        if key in value
    }
    return {
        "source_ref": source_ref,
        "status": status,
        "format_version": format_version,
        "declared_count": declared_count,
        "actual_count": actual_count,
        "updated": value.get("updated"),
        "metadata": metadata,
        "error": "; ".join(errors) or None,
    }


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


def monitor_repository(
    repo: str,
    configured_paths: list[str],
    token: str | None,
    checked_at: str,
    metadata_limit: int,
    registry_url: str | None = None,
) -> dict[str, Any]:
    """Fetch one source repository; a non-positive metadata limit enriches every entry."""

    meta = api_json(f"https://api.github.com/repos/{repo}", token)
    branch = str(meta.get("default_branch") or "main")
    tree = api_json(f"https://api.github.com/repos/{repo}/git/trees/{quote(branch, safe='')}?recursive=1", token)
    manifest = [{"path": row.get("path"), "sha": row.get("sha"), "type": row.get("type")} for row in tree.get("tree", [])]
    paths = selected_paths(tree, configured_paths)
    files: dict[str, str] = {}
    external_files: dict[str, str] = {}
    registry_metadata: dict[str, Any] = {}
    registries: list[dict[str, Any]] = []
    entry_sources: list[dict[str, Any]] = []
    entries: list[dict[str, Any]] = []
    available_paths = {str(row.get("path")) for row in tree.get("tree", []) if row.get("type") == "blob"}
    for path in configured_paths:
        if path in available_paths:
            continue
        kind = "registry" if is_registry_ref(path) else "file"
        entry_sources.append({"source_ref": path, "kind": kind, "status": "missing", "entry_count": 0})
        if kind == "registry":
            registries.append({
                "source_ref": path,
                "status": "missing",
                "format_version": None,
                "declared_count": None,
                "actual_count": None,
                "updated": None,
                "metadata": {},
                "error": "configured registry path is absent from the repository tree",
            })
    for path in paths:
        try:
            files[path] = raw_text(f"https://raw.githubusercontent.com/{repo}/{quote(branch, safe='')}/{quote(path, safe='/')}", token)
        except (HTTPError, URLError, TimeoutError, ValueError) as error:
            entry_sources.append({"source_ref": path, "kind": "file", "status": "error", "entry_count": 0, "error": str(error)})
            continue
        if path.endswith(".json"):
            try:
                parsed = json.loads(files[path])
                parsed_entries = structured_entries(parsed, path) if isinstance(parsed, dict) else []
                kind = "registry" if is_registry_ref(path) or (isinstance(parsed, dict) and "plugins" in parsed) else "json"
                if kind == "registry":
                    snapshot = registry_snapshot(parsed, path)
                    registries.append(snapshot)
                    if snapshot["status"] == "ok":
                        entries.extend(parsed_entries)
                    source_status = snapshot["status"]
                    source_error = snapshot.get("error")
                else:
                    entries.extend(parsed_entries)
                    source_status = "ok"
                    source_error = None
                source_record = {"source_ref": path, "kind": kind, "status": source_status, "entry_count": len(parsed_entries) if source_status == "ok" else 0}
                if source_error:
                    source_record["error"] = source_error
                entry_sources.append(source_record)
            except json.JSONDecodeError as error:
                entry_sources.append({"source_ref": path, "kind": "json", "status": "error", "entry_count": 0, "error": str(error)})
        elif path.lower().endswith((".md", ".markdown")):
            parsed_entries = markdown_entries(files[path], path, repo)
            entries.extend(parsed_entries)
            entry_sources.append({"source_ref": path, "kind": "markdown", "status": "ok", "entry_count": len(parsed_entries)})
    if registry_url:
        try:
            external_files[registry_url] = raw_text(registry_url, token)
            registry = json.loads(external_files[registry_url])
            parsed_entries = structured_entries(registry, registry_url) if isinstance(registry, dict) else []
            snapshot = registry_snapshot(registry, registry_url)
            registries.append(snapshot)
            registry_metadata = snapshot["metadata"]
            if snapshot["status"] == "ok":
                entries.extend(parsed_entries)
            source_record = {
                "source_ref": registry_url,
                "kind": "registry",
                "status": snapshot["status"],
                "entry_count": len(parsed_entries) if snapshot["status"] == "ok" else 0,
            }
            if snapshot.get("error"):
                source_record["error"] = snapshot["error"]
            entry_sources.append(source_record)
        except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
            entry_sources.append({"source_ref": registry_url, "kind": "registry", "status": "error", "entry_count": 0, "error": str(error)})
            registries.append({
                "source_ref": registry_url,
                "status": "error",
                "format_version": None,
                "declared_count": None,
                "actual_count": None,
                "updated": None,
                "metadata": {},
                "error": str(error),
            })
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

    candidates = entries if metadata_limit <= 0 else entries[:metadata_limit]
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
    source["external_files"] = external_files
    source["registry_metadata"] = registry_metadata
    source["registries"] = registries
    source["entry_sources"] = entry_sources
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
            descriptor = monitor_repository(
                repo,
                list(source.get("files", [])),
                token,
                checked_at,
                metadata_limit,
                registry_url=source.get("registry_url"),
            )
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


def payload_for_item_import(connection: Any, payload: dict[str, Any]) -> dict[str, Any]:
    """Keep new Listings in the item pipeline without replacing existing source-native items."""

    known_urls = {
        str(row[0])
        for row in connection.execute("SELECT canonical_url FROM items")
    }
    observations: list[dict[str, Any]] = []
    for observation in payload.get("observations", []):
        items: list[dict[str, Any]] = []
        for item in observation.get("items", []):
            canonical = collect.canonical_url(str(item.get("url") or item.get("canonical_url") or ""))
            if item.get("source_entry") is not None and canonical in known_urls:
                continue
            items.append(item)
            if canonical:
                known_urls.add(canonical)
        observations.append({**observation, "items": items})
    return {**payload, "observations": observations}


def normalized_raw_payload(raw_path: str, collected_at: str, payload_json: str) -> dict[str, Any] | None:
    """Return the shared payload represented by one preserved raw snapshot."""

    if payload_json == "{}":
        return None
    data = json.loads(payload_json)
    if isinstance(data, dict) and isinstance(data.get("observations"), list):
        return data
    if not isinstance(data, dict):
        return None
    dated_data = dict(data)
    dated_data.setdefault("collected_at", collected_at)
    path = Path(raw_path)
    if not path.is_absolute():
        path = ROOT / path
    try:
        return collect.legacy_payload(path, dated_data)
    except (OSError, ValueError):
        return None


def reconcile_listing_item_collisions(connection: Any) -> dict[str, int]:
    """Restore source-native item fields while preserving dated evidence."""

    target_rows = connection.execute(
        """
        SELECT DISTINCT i.id, i.canonical_url
        FROM items AS i
        WHERE json_type(i.raw_json, '$.source_entry') IS NOT NULL
          AND EXISTS (
              SELECT 1
              FROM item_observations AS io
              JOIN observations AS o ON o.id = io.observation_id
              WHERE io.item_id = i.id
                AND (
                    o.collector NOT IN (?, ?)
                    OR EXISTS (
                        SELECT 1
                        FROM upstream_repositories AS ur
                        WHERE o.query = 'upstream:' || ur.full_name
                          AND i.canonical_url = ur.source_url
                    )
                )
          )
        """,
        tuple(sorted(SOURCE_COLLECTORS)),
    ).fetchall()
    targets = {int(row[0]): str(row[1]) for row in target_rows}
    target_by_url = {url: item_id for item_id, url in targets.items()}
    snapshot_targets: dict[int, set[str]] = {}
    snapshot_rows: dict[int, Any] = {}
    for item_id, url in targets.items():
        rows = connection.execute(
            """
            SELECT DISTINCT rs.id, rs.raw_path, rs.collected_at, rs.payload_json,
                            rs.collection_run_id
            FROM raw_snapshots AS rs
            JOIN observations AS o ON o.raw_snapshot_id = rs.id
            JOIN item_observations AS io ON io.observation_id = o.id
            WHERE io.item_id = ? AND rs.payload_json <> '{}'
            """,
            (item_id,),
        ).fetchall()
        for row in rows:
            snapshot_id = int(row[0])
            snapshot_rows[snapshot_id] = row
            snapshot_targets.setdefault(snapshot_id, set()).add(url)

    candidates: dict[int, tuple[tuple[str, int, int], dict[str, Any], str, int | None]] = {}
    for snapshot_id in sorted(snapshot_rows):
        row = snapshot_rows[snapshot_id]
        payload = normalized_raw_payload(str(row[1]), str(row[2]), str(row[3]))
        if payload is None:
            continue
        run_id = int(row[4]) if row[4] is not None else None
        for observation_index, observation in enumerate(payload.get("observations", [])):
            observed_at = str(observation.get("collected_at") or payload.get("collected_at") or row[2])
            for item in observation.get("items", []):
                if not isinstance(item, dict) or item.get("source_entry") is not None:
                    continue
                canonical = collect.canonical_url(str(item.get("url") or item.get("canonical_url") or ""))
                if canonical not in snapshot_targets[snapshot_id]:
                    continue
                item_id = target_by_url[canonical]
                key = (observed_at, snapshot_id, observation_index)
                previous = candidates.get(item_id)
                if previous is None or key > previous[0]:
                    candidates[item_id] = (key, item, observed_at, run_id)

    missing = sorted(set(targets) - set(candidates))
    if missing:
        raise RuntimeError(
            "full raw payloads are required to reconcile "
            f"{len(missing)} Listing-overwritten item(s)"
        )

    restored = 0
    for item_id, (_key, item, observed_at, run_id) in candidates.items():
        category, relevance, _tags = collect.classify(item)
        title = str(item.get("title") or "").strip() or None
        content_text = str(item.get("content_text") or item.get("description") or "").strip() or None
        connection.execute(
            """
            UPDATE items
            SET platform = ?,
                title = COALESCE(?, title),
                author = COALESCE(?, author),
                author_url = COALESCE(?, author_url),
                published_at = COALESCE(?, published_at),
                published_label = COALESCE(?, published_label),
                content_text = COALESCE(?, content_text),
                language = COALESCE(?, language),
                category = ?, relevance = ?,
                media_kind = CASE
                    WHEN ? = 'video' OR media_kind = 'video' THEN 'video'
                    ELSE ?
                END,
                last_seen_at = ?, last_seen_run_id = COALESCE(?, last_seen_run_id),
                raw_json = ?
            WHERE id = ?
            """,
            (
                str(item.get("platform") or item.get("source") or "unknown"),
                title,
                item.get("author"),
                item.get("author_url"),
                item.get("published_at"),
                item.get("published_label"),
                content_text,
                item.get("language"),
                str(item.get("category") or category),
                str(item.get("relevance") or relevance),
                str(item.get("media_kind") or "none"),
                str(item.get("media_kind") or "none"),
                observed_at,
                run_id,
                json.dumps(item, ensure_ascii=False, sort_keys=True),
                item_id,
            ),
        )
        restored += 1

    link_cursor = connection.execute(
        """
        DELETE FROM item_observations
        WHERE EXISTS (
            SELECT 1
            FROM observations AS o
            JOIN items AS i ON i.id = item_observations.item_id
            WHERE o.id = item_observations.observation_id
              AND o.collector IN (?, ?)
              AND o.collection_run_id IS NOT i.first_seen_run_id
              AND NOT EXISTS (
                  SELECT 1
                  FROM upstream_repositories AS ur
                  WHERE o.query = 'upstream:' || ur.full_name
                    AND i.canonical_url = ur.source_url
              )
        )
        """,
        tuple(sorted(SOURCE_COLLECTORS)),
    )
    return {
        "restored_items": restored,
        "removed_metrics": 0,
        "removed_item_observations": max(0, link_cursor.rowcount),
    }


def record_upstream_repositories(connection: Any, payload: dict[str, Any], raw_snapshot_id: int) -> None:
    """Persist source repositories and link their entries to normalized items."""

    collection_run_id = int(connection.execute(
        "SELECT collection_run_id FROM raw_snapshots WHERE id = ?",
        (raw_snapshot_id,),
    ).fetchone()[0])
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
        entries = list(descriptor.get("entries", []))
        successful_sources = {
            str(source["source_ref"])
            for source in descriptor.get("entry_sources", [])
            if source.get("status") in {"ok", "missing"} and source.get("source_ref")
        }
        current_keys_by_source: dict[str, set[str]] = {}
        for entry in entries:
            source_ref = str(entry.get("source_path") or "")
            source_url = str(entry.get("source_url") or entry.get("url") or "")
            listing_key = collect.upstream_listing_key(
                source_url,
                entry.get("category"),
                entry.get("install_spec"),
                entry.get("registry_id"),
            )
            current_keys_by_source.setdefault(source_ref, set()).add(listing_key)
        for source_ref in successful_sources:
            current_keys = current_keys_by_source.get(source_ref, set())
            previous = connection.execute(
                "SELECT id, listing_key FROM upstream_entries "
                "WHERE repository_id = ? AND source_path = ? AND active = 1",
                (repo_id, source_ref),
            ).fetchall()
            for row in previous:
                if str(row["listing_key"]) in current_keys:
                    continue
                connection.execute("UPDATE upstream_entries SET active = 0 WHERE id = ?", (int(row["id"]),))
                record_upstream_entry_observation(
                    connection, int(row["id"]), collection_run_id, raw_snapshot_id, descriptor["last_checked_at"]
                )
        for registry in descriptor.get("registries", []):
            connection.execute(
                """
                INSERT INTO upstream_registry_snapshots(
                    repository_id, collection_run_id, raw_snapshot_id, source_ref,
                    observed_at, status, format_version, declared_count, actual_count,
                    registry_updated_at, metadata_json, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(repository_id, collection_run_id, source_ref) DO UPDATE SET
                    raw_snapshot_id=excluded.raw_snapshot_id, observed_at=excluded.observed_at,
                    status=excluded.status, format_version=excluded.format_version,
                    declared_count=excluded.declared_count, actual_count=excluded.actual_count,
                    registry_updated_at=excluded.registry_updated_at,
                    metadata_json=excluded.metadata_json, error_message=excluded.error_message
                """,
                (
                    repo_id, collection_run_id, raw_snapshot_id, registry["source_ref"],
                    descriptor["last_checked_at"], registry["status"], registry.get("format_version"),
                    registry.get("declared_count"), registry.get("actual_count"), registry.get("updated"),
                    json.dumps(registry.get("metadata") or {}, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                    registry.get("error"),
                ),
            )
        for entry in entries:
            source_url = str(entry.get("source_url") or entry.get("url") or "")
            listing_key = collect.upstream_listing_key(
                source_url,
                entry.get("category"),
                entry.get("install_spec"),
                entry.get("registry_id"),
            )
            canonical = collect.canonical_url(str(entry.get("url") or source_url))
            item_row = connection.execute("SELECT id FROM items WHERE canonical_url = ?", (canonical,)).fetchone()
            source_json = json.dumps(entry, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            description_i18n = json.dumps(entry.get("description_i18n") or {}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            tags_json = json.dumps(entry.get("tags") or [], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            registry_source_json = json.dumps(entry.get("registry_source") or {}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            connection.execute(
                """
                INSERT INTO upstream_entries(
                    repository_id, item_id, listing_key, entry_name, entry_url, registry_id, owner, page_url,
                    entry_kind, category, description, description_i18n, npm_package,
                    stars, install_hint, install_spec, install_target, plugin_version,
                    verified, tags_json, registry_source_json, added_at,
                    source_path, source_line, source_json,
                    raw_snapshot_id, first_seen_run_id, last_seen_run_id, active,
                    first_seen_at, last_seen_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                ON CONFLICT(repository_id, listing_key) DO UPDATE SET
                    item_id=excluded.item_id, entry_name=excluded.entry_name,
                    registry_id=excluded.registry_id, owner=excluded.owner, page_url=excluded.page_url,
                    entry_kind=excluded.entry_kind, description=excluded.description,
                    description_i18n=excluded.description_i18n, npm_package=excluded.npm_package,
                    stars=excluded.stars, install_hint=excluded.install_hint,
                    install_spec=excluded.install_spec, install_target=excluded.install_target,
                    plugin_version=excluded.plugin_version, verified=excluded.verified,
                    tags_json=excluded.tags_json, registry_source_json=excluded.registry_source_json,
                    added_at=excluded.added_at, source_path=excluded.source_path,
                    source_line=excluded.source_line, source_json=excluded.source_json,
                    raw_snapshot_id=excluded.raw_snapshot_id,
                    last_seen_run_id=excluded.last_seen_run_id, active=1,
                    last_seen_at=excluded.last_seen_at
                """,
                (
                    repo_id, int(item_row[0]) if item_row else None,
                    listing_key, entry.get("name") or source_url, source_url,
                    entry.get("registry_id"), entry.get("owner"),
                    entry.get("page"), entry.get("entry_kind", "candidate"),
                    entry.get("category"), entry.get("description"), description_i18n,
                    entry.get("npm"), entry.get("stars"), entry.get("install"),
                    entry.get("install_spec"), entry.get("install_target"), entry.get("version"),
                    int(entry["verified"]) if isinstance(entry.get("verified"), bool) else None,
                    tags_json, registry_source_json, entry.get("added"),
                    entry.get("source_path"), entry.get("source_line"),
                    source_json, raw_snapshot_id, collection_run_id, collection_run_id,
                    descriptor["last_checked_at"], descriptor["last_checked_at"],
                ),
            )
            entry_id = int(connection.execute(
                "SELECT id FROM upstream_entries WHERE repository_id = ? AND listing_key = ?",
                (repo_id, listing_key),
            ).fetchone()[0])
            record_upstream_entry_observation(
                connection, entry_id, collection_run_id, raw_snapshot_id, descriptor["last_checked_at"]
            )


def record_upstream_entry_observation(
    connection: Any,
    entry_id: int,
    collection_run_id: int,
    raw_snapshot_id: int,
    observed_at: str,
) -> None:
    """Append the normalized state of one Listing for a dated collection run."""

    connection.execute(
        """
        INSERT INTO upstream_entry_observations(
            entry_id, collection_run_id, raw_snapshot_id, observed_at, active,
            listing_key, registry_id, entry_name, entry_url, owner, page_url, entry_kind,
            category, description, description_i18n, npm_package, stars,
            install_hint, install_spec, install_target, plugin_version, verified,
            tags_json, registry_source_json, added_at, source_path, source_line
        )
        SELECT id, ?, ?, ?, active, listing_key, registry_id, entry_name, entry_url, owner,
               page_url, entry_kind, category, description, description_i18n,
               npm_package, stars, install_hint, install_spec, install_target,
               plugin_version, verified, tags_json, registry_source_json,
               added_at, source_path, source_line
        FROM upstream_entries
        WHERE id = ?
        ON CONFLICT(entry_id, collection_run_id) DO UPDATE SET
            raw_snapshot_id=excluded.raw_snapshot_id, observed_at=excluded.observed_at,
            active=excluded.active, listing_key=excluded.listing_key,
            registry_id=excluded.registry_id,
            entry_name=excluded.entry_name, entry_url=excluded.entry_url,
            owner=excluded.owner, page_url=excluded.page_url,
            entry_kind=excluded.entry_kind, category=excluded.category,
            description=excluded.description, description_i18n=excluded.description_i18n,
            npm_package=excluded.npm_package, stars=excluded.stars,
            install_hint=excluded.install_hint, install_spec=excluded.install_spec,
            install_target=excluded.install_target, plugin_version=excluded.plugin_version,
            verified=excluded.verified, tags_json=excluded.tags_json,
            registry_source_json=excluded.registry_source_json,
            added_at=excluded.added_at, source_path=excluded.source_path,
            source_line=excluded.source_line
        """,
        (collection_run_id, raw_snapshot_id, observed_at, entry_id),
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
            reconciliation = reconcile_listing_item_collisions(connection)
            stats = collect.import_payload(
                connection,
                payload_for_item_import(connection, payload),
                run_id,
                args.raw_output,
            )
            stats.raw_files_seen = 1
            raw_sha = collect.sha256_file(args.raw_output)
            raw_snapshot_id = int(connection.execute("SELECT id FROM raw_snapshots WHERE raw_sha256 = ?", (raw_sha,)).fetchone()[0])
            record_upstream_repositories(connection, payload, raw_snapshot_id)
            collect.finish_collection_run(connection, run_id, stats)
        except Exception as error:
            collect.finish_collection_run(connection, run_id, stats, "failed", str(error))
            connection.commit()
            raise
    print(
        f"monitored {len(payload.get('repositories', []))} upstream repositories in {version}; "
        f"reconciled {reconciliation['restored_items']} item(s), "
        f"{reconciliation['removed_metrics']} metric(s), and "
        f"{reconciliation['removed_item_observations']} item-observation link(s); "
        f"raw snapshot: {args.raw_output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
