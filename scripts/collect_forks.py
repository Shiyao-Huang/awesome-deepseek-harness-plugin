#!/usr/bin/env python3
"""Index the public fork network of the DeepSeek Harness upstream repository.

The collector stores every public fork returned by GitHub's paginated forks
endpoint. A bounded deep-scan budget adds compare results, recent commits,
README metadata, and changed-file categories. Use ``--deep-scan-all`` only
with a token and a request budget that can cover the complete network.
"""

from __future__ import annotations

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import math
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import collect


DB_PATH = ROOT / "data" / "aggregator.sqlite3"
CONFIG_PATH = ROOT / "config" / "forks.json"
RAW_DIR = ROOT / "data" / "raw" / "forks"
UPSTREAM = "deepseek-ai/deepseek-harness"
USER_AGENT = "awesome-deepseek-harness-plugin/fork-index"


def utc_now() -> str:
    """Return a second-precision UTC timestamp."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def github_token() -> str | None:
    """Read an Actions token or the local GitHub CLI token without printing it."""

    for name in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(name):
            return os.environ[name]
    try:
        result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() or None


def api_request(url: str, token: str | None) -> tuple[Any, dict[str, str]]:
    """Fetch and decode one public GitHub JSON response."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": USER_AGENT,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        response_headers = {key.lower(): value for key, value in response.headers.items()}
        return json.loads(response.read().decode("utf-8")), response_headers


def api_error(error: Exception) -> dict[str, Any]:
    """Convert a public API failure into reviewable raw metadata."""

    result: dict[str, Any] = {"status": "error", "error": str(error)}
    if isinstance(error, HTTPError):
        result["http_status"] = error.code
        try:
            result["response"] = json.loads(error.read().decode("utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            result["response"] = None
    return result


def api_call(url: str, token: str | None) -> dict[str, Any]:
    """Fetch one endpoint and retain its URL, response, and rate headers."""

    try:
        response, headers = api_request(url, token)
        return {
            "status": "ok",
            "url": url,
            "response": response,
            "rate_limit_remaining": headers.get("x-ratelimit-remaining"),
            "rate_limit_reset": headers.get("x-ratelimit-reset"),
            "link": headers.get("link"),
        }
    except (HTTPError, URLError, TimeoutError, RuntimeError, json.JSONDecodeError) as error:
        result = api_error(error)
        result["url"] = url
        return result


def next_link(link: str | None) -> str | None:
    """Return the next URL from a GitHub Link response header."""

    if not link:
        return None
    for value in link.split(","):
        parts = value.strip().split(";", 1)
        if len(parts) == 2 and 'rel="next"' in parts[1]:
            return parts[0].strip().strip("<>")
    return None


def error_response(record: dict[str, Any]) -> bool:
    """Return whether an endpoint record did not contain a successful response."""

    return record.get("status") != "ok"


def fetch_fork_pages(
    upstream: str,
    page_size: int,
    token: str | None,
    sort: str = "oldest",
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Fetch every public fork page in ordered concurrent batches."""

    pages: list[dict[str, Any]] = []
    forks: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    page_number = 1
    batch_size = 8
    while page_number <= 1000:
        page_numbers = list(range(page_number, page_number + batch_size))
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            responses = list(executor.map(
                lambda number: api_call(
                    f"https://api.github.com/repos/{upstream}/forks?{urlencode({'sort': sort, 'direction': 'asc' if sort == 'oldest' else 'desc', 'per_page': page_size, 'page': number})}",
                    token,
                ),
                page_numbers,
            ))
        stop_after = False
        for page in responses:
            pages.append(page)
            url = page.get("url")
            if error_response(page):
                errors.append({"stage": "fork-list", "url": url, "error": page})
                stop_after = True
                break
            response = page.get("response")
            if not isinstance(response, list):
                errors.append({"stage": "fork-list", "url": url, "error": "GitHub returned a non-list response"})
                stop_after = True
                break
            existing = {full_name(row) for row in forks}
            forks.extend(
                row for row in response
                if isinstance(row, dict) and full_name(row) and full_name(row) not in existing
            )
            if len(response) < page_size:
                stop_after = True
                break
        if stop_after:
            break
        page_number += batch_size
    return pages, forks, errors


def full_name(value: dict[str, Any]) -> str:
    """Read a repository full name from a GitHub response object."""

    return str(value.get("full_name") or "").strip()


def parent_name(value: dict[str, Any]) -> str | None:
    """Read the parent repository name when GitHub exposes it."""

    parent = value.get("parent")
    return full_name(parent) if isinstance(parent, dict) and full_name(parent) else None


def source_name(value: dict[str, Any]) -> str | None:
    """Read the network source repository name when GitHub exposes it."""

    source = value.get("source")
    if isinstance(source, dict) and full_name(source):
        return full_name(source)
    return parent_name(value)


def repository_metadata(row: dict[str, Any], detail: dict[str, Any] | None, checked_at: str, deep_scanned: bool) -> dict[str, Any]:
    """Normalize stable public repository metadata without discarding raw data."""

    value = detail if detail and full_name(detail) else row
    license_data = value.get("license") or {}
    owner = value.get("owner") or row.get("owner") or {}
    status = "ok" if deep_scanned and detail and full_name(detail) else ("metadata-only" if not deep_scanned else "partial")
    return {
        "full_name": full_name(value) or full_name(row),
        "html_url": value.get("html_url") or row.get("html_url"),
        "api_url": value.get("url") or row.get("url"),
        "node_id": value.get("node_id") or row.get("node_id"),
        "owner_login": owner.get("login"),
        "owner_type": owner.get("type"),
        "parent_full_name": parent_name(value) or parent_name(row),
        "source_full_name": source_name(value) or source_name(row),
        "default_branch": value.get("default_branch") or row.get("default_branch") or "main",
        "description": value.get("description") if value.get("description") is not None else row.get("description"),
        "license_spdx": license_data.get("spdx_id"),
        "visibility": value.get("visibility") or row.get("visibility"),
        "is_fork": int(bool(value.get("fork", row.get("fork", True)))),
        "archived": int(bool(value.get("archived", row.get("archived", False)))),
        "disabled": int(bool(value.get("disabled", row.get("disabled", False)))),
        "stars": value.get("stargazers_count", row.get("stargazers_count")),
        "forks": value.get("forks_count", row.get("forks_count")),
        "open_issues": value.get("open_issues_count", row.get("open_issues_count")),
        "watchers": value.get("watchers_count", row.get("watchers_count")),
        "subscribers": value.get("subscribers_count", row.get("subscribers_count")),
        "size_kb": value.get("size", row.get("size")),
        "forked_at": value.get("forked_at", row.get("forked_at")),
        "created_at": value.get("created_at", row.get("created_at")),
        "updated_at": value.get("updated_at", row.get("updated_at")),
        "pushed_at": value.get("pushed_at", row.get("pushed_at")),
        "last_checked_at": checked_at,
        "status": status,
    }


def file_category(filename: str) -> str:
    """Classify one changed path for browsing and aggregate reporting."""

    path = filename.lower().replace("\\", "/")
    name = path.rsplit("/", 1)[-1]
    if path.startswith(("docs/", "doc/")) or name.endswith((".md", ".mdx", ".rst")):
        return "docs"
    if path.startswith((".github/", ".gitlab/")) or name in {"dockerfile", "makefile"}:
        return "ci-and-build"
    if path.startswith(("test/", "tests/", "__tests__/")) or ".test." in name or ".spec." in name:
        return "tests"
    if name in {"package.json", "pnpm-lock.yaml", "yarn.lock", "package-lock.json", "pyproject.toml", "requirements.txt", "cargo.toml", "cargo.lock"}:
        return "dependencies"
    if path.startswith(("config/", ".env", "settings/")) or name.endswith((".yml", ".yaml", ".toml")):
        return "configuration"
    if path.startswith(("packages/", "src/", "lib/", "python/", "native/")):
        return "harness-core"
    if any(term in path for term in ("agent", "subagent", "workflow", "skill")):
        return "agents-and-skills"
    if path.startswith(("ui/", "web/", "website/", "apps/")) or any(term in path for term in ("component", "frontend", "desktop")):
        return "ui-and-apps"
    if path.startswith(("scripts/", "tools/", "bin/")):
        return "tools-and-scripts"
    return "other"


def decode_readme(readme: dict[str, Any] | None) -> str:
    """Decode a GitHub contents API README response for conservative classification."""

    if not readme or readme.get("status") != "ok":
        return ""
    response = readme.get("response")
    if not isinstance(response, dict):
        return ""
    content = response.get("content")
    if not isinstance(content, str):
        return ""
    try:
        return base64.b64decode(content.encode("ascii"), validate=False).decode("utf-8", "replace")
    except (ValueError, UnicodeEncodeError):
        return ""


def changed_files(compare: dict[str, Any], max_files: int) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Normalize compare files and count conservative modification categories."""

    response = compare.get("response") if compare.get("status") == "ok" else None
    files = response.get("files", []) if isinstance(response, dict) else []
    if not isinstance(files, list):
        files = []
    normalized: list[dict[str, Any]] = []
    categories: dict[str, int] = {}
    for file in files[:max_files]:
        if not isinstance(file, dict) or not file.get("filename"):
            continue
        category = file_category(str(file["filename"]))
        categories[category] = categories.get(category, 0) + 1
        normalized.append({
            "filename": file["filename"],
            "status": file.get("status"),
            "additions": file.get("additions"),
            "deletions": file.get("deletions"),
            "changes": file.get("changes"),
            "previous_filename": file.get("previous_filename"),
            "category": category,
            "blob_url": file.get("blob_url"),
            "raw_url": file.get("raw_url"),
            "raw": file,
        })
    return normalized, categories


def latest_commit(commits: dict[str, Any]) -> dict[str, Any]:
    """Extract a compact latest commit descriptor from the commits response."""

    response = commits.get("response") if commits.get("status") == "ok" else None
    if not isinstance(response, list) or not response or not isinstance(response[0], dict):
        return {}
    row = response[0]
    commit = row.get("commit") or {}
    author = commit.get("author") or {}
    committer = commit.get("committer") or {}
    return {
        "sha": row.get("sha"),
        "html_url": row.get("html_url"),
        "message": str(commit.get("message") or "").splitlines()[0][:500],
        "author_login": (row.get("author") or {}).get("login") if isinstance(row.get("author"), dict) else None,
        "committer_login": (row.get("committer") or {}).get("login") if isinstance(row.get("committer"), dict) else None,
        "authored_at": author.get("date"),
        "committed_at": committer.get("date"),
    }


CATEGORY_LABELS = {
    "harness-core": "Harness 核心能力",
    "agents-and-skills": "agent/skill 能力",
    "ui-and-apps": "UI/应用层",
    "tools-and-scripts": "工具与脚本",
    "docs": "文档",
    "ci-and-build": "CI/构建",
    "tests": "测试",
    "configuration": "配置",
    "dependencies": "依赖",
    "other": "其他文件",
}


def compact_public_text(value: Any, limit: int = 180) -> str:
    """Collapse public repository text for a one-sentence evidence note."""

    text = " ".join(str(value or "").split())
    text = text.replace("|", " ").replace("`", "")
    return text[:limit].rstrip(" .。；;")


def readme_goal(readme_text: str) -> str:
    """Extract a conservative goal clue from the first useful README line."""

    for line in readme_text.splitlines():
        candidate = line.strip().lstrip("#>-* ")
        if not candidate or candidate.startswith(("[", "!", "<", "```")):
            continue
        candidate = compact_public_text(candidate)
        if len(candidate) >= 12:
            return candidate
    return "目标线索尚未从 README 观察到"


def change_summary(normalized: dict[str, Any], readme_text: str = "") -> str:
    """Describe observed changes and the stated goal in one evidence-qualified sentence."""

    if normalized.get("detail_status") == "metadata-only":
        goal = compact_public_text(normalized.get("description")) or "未从 Fork 列表元数据观察到"
        return f"当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“{goal}”，修改面待下一轮 compare/README 深扫。"
    changed = normalized.get("changed_files")
    ahead = normalized.get("ahead_by")
    categories = normalized.get("modification_categories") or {}
    labels = [CATEGORY_LABELS.get(str(key), str(key)) for key in categories]
    if changed is None:
        change_text = "compare 未返回修改文件数"
    elif int(changed) == 0:
        change_text = "未观察到相对 upstream 的文件修改"
    else:
        commit_text = f"新增约 {int(ahead)} 个提交并" if ahead is not None else ""
        category_text = "、".join(labels[:4]) or "未分类文件"
        change_text = f"{commit_text}修改 {int(changed)} 个文件，主要涉及 {category_text}"
    goal = compact_public_text(normalized.get("description")) or readme_goal(readme_text)
    return f"{change_text}；目标线索是“{goal}”。"


def profile_from_api(call: dict[str, Any], login: str, fetched_at: str) -> dict[str, Any]:
    """Normalize one public GitHub user response without retaining private fields."""

    response = call.get("response") if call.get("status") == "ok" else None
    value = response if isinstance(response, dict) else {}
    return {
        "login": str(value.get("login") or login),
        "html_url": value.get("html_url") or f"https://github.com/{login}",
        "api_url": value.get("url") or f"https://api.github.com/users/{login}",
        "node_id": value.get("node_id"),
        "type": value.get("type"),
        "public_repos": value.get("public_repos"),
        "public_gists": value.get("public_gists"),
        "followers": value.get("followers"),
        "following": value.get("following"),
        "created_at": value.get("created_at"),
        "updated_at": value.get("updated_at"),
        "fetched_at": fetched_at,
        "status": "ok" if call.get("status") == "ok" and isinstance(response, dict) else "error",
        "raw_json": json.dumps(call, ensure_ascii=False, sort_keys=True),
        "from_cache": False,
    }


def cached_profile(row: Any) -> dict[str, Any]:
    """Convert a cached SQLite user profile into the ranking input format."""

    return {
        "login": row["login"],
        "html_url": row["html_url"],
        "api_url": row["api_url"],
        "node_id": row["node_id"],
        "type": row["type"],
        "public_repos": row["public_repos"],
        "public_gists": row["public_gists"],
        "followers": row["followers"],
        "following": row["following"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "fetched_at": row["fetched_at"],
        "status": row["status"],
        "raw_json": row["raw_json"],
        "from_cache": True,
    }


def profile_is_fresh(profile: dict[str, Any], observed_at: str, stale_days: int) -> bool:
    """Return whether a cached profile is recent enough for this run."""

    fetched = parse_time(str(profile.get("fetched_at") or ""))
    observed = parse_time(observed_at)
    if fetched is None or observed is None or stale_days < 0:
        return False
    return profile.get("status") == "ok" and (observed - fetched).total_seconds() <= stale_days * 86_400


def load_cached_profiles(connection: Any, logins: set[str]) -> dict[str, dict[str, Any]]:
    """Load public user profiles already cached in SQLite."""

    if not logins:
        return {}
    placeholders = ",".join("?" for _ in logins)
    rows = connection.execute(
        f"SELECT login, html_url, api_url, node_id, type, public_repos, public_gists, followers, following, created_at, updated_at, fetched_at, status, raw_json FROM github_user_profiles WHERE login IN ({placeholders})",
        sorted(logins),
    ).fetchall()
    return {str(row["login"]): cached_profile(row) for row in rows}


def select_profile_logins(
    descriptors: list[dict[str, Any]],
    repository_rankings: list[dict[str, Any]],
    cached: dict[str, dict[str, Any]],
    limit: int,
    observed_at: str,
    stale_days: int,
) -> list[str]:
    """Select unique high-influence owners whose public profiles need observation."""

    rank_by_name = {row["full_name"]: row for row in repository_rankings}
    candidates: dict[str, tuple[float, str, bool]] = {}
    for descriptor in descriptors:
        value = descriptor["normalized"]
        login = str(value.get("owner_login") or "").strip()
        name = str(value.get("full_name") or "")
        if not login or not name:
            continue
        profile = cached.get(login)
        needs_fetch = not profile or not profile_is_fresh(profile, observed_at, stale_days)
        rank = rank_by_name.get(name) or {}
        score = float(rank.get("score") or 0)
        previous = candidates.get(login)
        if previous is None or (needs_fetch and not previous[2]) or score > previous[0]:
            candidates[login] = (score, name, needs_fetch)
    ordered = sorted(candidates.items(), key=lambda pair: (-pair[1][0], pair[0]))
    return [login for login, (_, _, needs_fetch) in ordered if needs_fetch][:max(0, limit)]


def fetch_owner_profiles(
    connection: Any,
    descriptors: list[dict[str, Any]],
    repository_rankings: list[dict[str, Any]],
    observed_at: str,
    token: str | None,
    config: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Reuse fresh public user profiles and fetch a bounded stale-owner rotation."""

    logins = {str(d["normalized"].get("owner_login") or "").strip() for d in descriptors}
    logins.discard("")
    cached = load_cached_profiles(connection, logins)
    selected = select_profile_logins(
        descriptors,
        repository_rankings,
        cached,
        int(config.get("owner_profile_limit", 100)),
        observed_at,
        int(config.get("owner_profile_stale_days", 30)),
    )
    profiles = dict(cached)
    for login in selected:
        profiles[login] = profile_from_api(api_call(f"https://api.github.com/users/{quote(login)}", token), login, observed_at)
    return profiles


def deep_scan_fork(
    row: dict[str, Any],
    upstream: str,
    upstream_branch: str,
    token: str | None,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Fetch one fork's metadata, compare result, commits, and README."""

    slug = full_name(row)
    branch = str(row.get("default_branch") or "main")
    detail = api_call(f"https://api.github.com/repos/{slug}", token)
    detail_value = detail.get("response") if detail.get("status") == "ok" and isinstance(detail.get("response"), dict) else None
    owner = str((row.get("owner") or {}).get("login") or slug.split("/", 1)[0])
    compare_ref = f"{upstream_branch}...{owner}:{branch}"
    compare_path = f"/repos/{upstream}/compare/{quote(compare_ref, safe=':.')}"
    compare = api_call(f"https://api.github.com{compare_path}", token)
    commits_url = f"https://api.github.com/repos/{slug}/commits?{urlencode({'sha': branch, 'per_page': int(config.get('recent_commits', 10))})}"
    commits = api_call(commits_url, token)
    readme = api_call(f"https://api.github.com/repos/{slug}/readme", token)
    files, categories = changed_files(compare, int(config.get("max_file_changes", 300)))
    commit = latest_commit(commits)
    readme_response = readme.get("response") if readme.get("status") == "ok" else None
    compare_response = compare.get("response") if isinstance(compare.get("response"), dict) else {}
    changed_file_count = compare_response.get("changed_files")
    additions = compare_response.get("additions")
    deletions = compare_response.get("deletions")
    if changed_file_count is None:
        changed_file_count = len(files)
    if additions is None:
        additions = sum(int(file.get("additions") or 0) for file in files)
    if deletions is None:
        deletions = sum(int(file.get("deletions") or 0) for file in files)
    normalized = repository_metadata(row, detail_value, str(config["collected_at"]), True)
    normalized.update({
        "latest_commit": commit,
        "readme_sha": readme_response.get("sha") if isinstance(readme_response, dict) else None,
        "compare_status": compare_response.get("status"),
        "ahead_by": compare_response.get("ahead_by"),
        "behind_by": compare_response.get("behind_by"),
        "total_commits": compare_response.get("total_commits"),
        "changed_files": changed_file_count,
        "additions": additions,
        "deletions": deletions,
        "modification_categories": categories,
        "deep_scanned_at": str(config["collected_at"]),
        "detail_status": "ok" if not any(error_response(value) for value in (detail, compare, commits, readme)) else "partial",
    })
    normalized["change_summary"] = change_summary(normalized, decode_readme(readme))
    return {
        "normalized": normalized,
        "repository": None,
        "repository_detail": detail,
        "compare": compare,
        "commits": commits,
        "readme": readme,
        "readme_text_for_analysis": decode_readme(readme)[:50_000],
        "files": files,
    }


def metadata_only_fork(row: dict[str, Any], checked_at: str) -> dict[str, Any]:
    """Normalize a fork that was observed in the complete list but not deep-scanned."""

    normalized = {
        **repository_metadata(row, row, checked_at, False),
        "readme_sha": None,
        "deep_scanned_at": None,
        "detail_status": "metadata-only",
        "compare_status": None,
        "ahead_by": None,
        "behind_by": None,
        "total_commits": None,
        "changed_files": None,
        "additions": None,
        "deletions": None,
        "modification_categories": {},
        "latest_commit": {},
    }
    normalized["change_summary"] = change_summary(normalized)
    return {
        "normalized": normalized,
        "repository": row,
        "repository_detail": None,
        "compare": None,
        "commits": None,
        "readme": None,
        "readme_text_for_analysis": "",
        "files": [],
    }


def select_deep_forks(
    connection: Any,
    rows: list[dict[str, Any]],
    limit: int,
    deep_scan_all: bool,
    recheck_deep: bool,
    changed_recheck_fraction: float = 0.2,
) -> set[str]:
    """Select changed, never-scanned, then stale forks without starving backfill."""

    if deep_scan_all:
        return {full_name(row) for row in rows if full_name(row)}
    names = [full_name(row) for row in rows if full_name(row)]
    if not names or limit <= 0:
        return set()
    if recheck_deep:
        ordered = sorted(
            rows,
            key=lambda row: (
                -int(row.get("stargazers_count") or 0),
                -int(row.get("forks_count") or 0),
                full_name(row),
            ),
        )
        return {full_name(row) for row in ordered[:limit]}
    placeholders = ",".join("?" for _ in names)
    prior = {
        row["full_name"]: row
        for row in connection.execute(
            f"SELECT full_name, last_deep_checked_at, pushed_at, stars, forks FROM fork_repositories WHERE full_name IN ({placeholders})",
            names,
        )
    }
    def prior_value(slug: str, key: str) -> Any:
        row = prior.get(slug)
        return row[key] if row is not None else None

    def influence_key(row: dict[str, Any]) -> tuple[int, int, str]:
        return (
            -int(row.get("stargazers_count") or 0),
            -int(row.get("forks_count") or 0),
            full_name(row),
        )

    changed: list[dict[str, Any]] = []
    never_scanned: list[dict[str, Any]] = []
    stale: list[dict[str, Any]] = []
    for row in rows:
        slug = full_name(row)
        last_deep = parse_time(prior_value(slug, "last_deep_checked_at"))
        pushed = parse_time(str(row.get("pushed_at") or ""))
        if last_deep is None:
            never_scanned.append(row)
        elif pushed is not None and pushed > last_deep:
            changed.append(row)
        else:
            stale.append(row)

    changed.sort(key=influence_key)
    never_scanned.sort(key=influence_key)
    stale.sort(
        key=lambda row: (
            prior_value(full_name(row), "last_deep_checked_at") or "",
            *influence_key(row),
        )
    )
    fraction = min(1.0, max(0.0, float(changed_recheck_fraction)))
    changed_limit = min(len(changed), int(limit * fraction)) if never_scanned else min(len(changed), limit)
    ordered = changed[:changed_limit] + never_scanned + stale + changed[changed_limit:]
    return {full_name(row) for row in ordered[:limit]}


def build_item(descriptor: dict[str, Any], observed_at: str) -> dict[str, Any]:
    """Convert a normalized fork descriptor into the shared aggregator item format."""

    normalized = descriptor["normalized"]
    categories = normalized.get("modification_categories") or {}
    tags = ["deepseek-harness-fork", "fork-network", normalized.get("detail_status") or "metadata-only"]
    tags.extend(str(key) for key in categories)
    return {
        "platform": "github",
        "external_id": normalized["full_name"],
        "url": normalized["html_url"],
        "item_type": "fork",
        "title": normalized["full_name"],
        "author": normalized.get("owner_login"),
        "published_at": normalized.get("created_at"),
        "content_text": normalized.get("change_summary") or normalized.get("description"),
        "category": "deepseek-harness-forks",
        "relevance": "direct",
        "media_kind": "none",
        "metrics": {
            "stars": normalized.get("stars"),
            "forks": normalized.get("forks"),
            "open_issues": normalized.get("open_issues"),
            "metric_source": "GitHub fork network API",
            "observed_at": observed_at,
        },
        "description": normalized.get("description"),
        "change_summary": normalized.get("change_summary"),
        "tags": tags,
    }


def deduplicate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Keep the first normalized record for each public Fork full name."""

    seen: set[str] = set()
    forks: list[dict[str, Any]] = []
    for descriptor in payload.get("forks", []):
        name = str((descriptor.get("normalized") or {}).get("full_name") or "")
        if not name or name in seen:
            continue
        seen.add(name)
        forks.append(descriptor)
    payload["forks"] = forks
    ranking_seen: set[str] = set()
    rankings: list[dict[str, Any]] = []
    for row in payload.get("rankings", []):
        name = str(row.get("full_name") or "")
        if not name or name in ranking_seen:
            continue
        ranking_seen.add(name)
        rankings.append(row)
    for rank, row in enumerate(rankings, 1):
        row["rank"] = rank
    payload["rankings"] = rankings
    observations = payload.get("observations") or []
    if observations:
        item_seen: set[str] = set()
        items: list[dict[str, Any]] = []
        for item in observations[0].get("items", []):
            name = str(item.get("external_id") or "")
            if not name or name in item_seen:
                continue
            item_seen.add(name)
            items.append(item)
        observations[0]["items"] = items
        observations[0]["result_count"] = len(items)
    if isinstance(payload.get("fork_list"), dict):
        payload["fork_list"]["normalized_fork_count"] = len(forks)
    return payload


def parse_time(value: str | None) -> datetime | None:
    """Parse a GitHub ISO timestamp."""

    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def normalized_log(value: Any, maximum: Any) -> float:
    """Normalize a non-negative metric on a logarithmic 0..1 scale."""

    number = max(0.0, float(value or 0))
    ceiling = max(0.0, float(maximum or 0))
    if ceiling <= 0:
        return 0.0
    return min(1.0, math.log1p(number) / math.log1p(ceiling))


def activity_ratio(value: str | None, now: datetime, horizon_days: int) -> float:
    """Return a linear recent-activity ratio in the 0..1 range."""

    timestamp = parse_time(value)
    if timestamp is None:
        return 0.0
    age = max(0.0, (now - timestamp).total_seconds() / 86_400)
    if horizon_days <= 0:
        return 0.0
    return max(0.0, 1.0 - age / horizon_days)


def account_age_ratio(value: str | None, observed_at: str, cap_days: int) -> float:
    """Normalize public GitHub account age with a configurable upper bound."""

    created = parse_time(value)
    observed = parse_time(observed_at)
    if created is None or observed is None or cap_days <= 0:
        return 0.0
    age_days = max(0.0, (observed - created).total_seconds() / 86_400)
    return min(1.0, age_days / cap_days)


def reputation_maxima(profiles: dict[str, dict[str, Any]]) -> dict[str, float]:
    """Build log-normalization ceilings from observed public profile values."""

    return {
        field: max(1.0, max((float(profile.get(field) or 0) for profile in profiles.values() if profile.get("status") == "ok"), default=0.0))
        for field in ("followers", "public_repos", "public_gists", "following")
    }


def rank_forks(
    descriptors: list[dict[str, Any]],
    config: dict[str, Any],
    observed_at: str,
    profiles: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Rank eligible Forks by repository influence and observed public-account signals."""

    profiles = profiles or {}
    weights = {key: float(value) for key, value in (config.get("weights") or {}).items()}
    reputation_weights = {key: float(value) for key, value in (config.get("reputation_weights") or {}).items()}
    repository_weight = max(0.0, float(config.get("repository_weight", 0.6)))
    reputation_weight = max(0.0, float(config.get("reputation_weight", 0.4)))
    min_stars = max(0, int(config.get("min_stars", 0)))
    now = parse_time(observed_at) or datetime.now(timezone.utc)
    horizon = int(config.get("activity_horizon_days", 365))
    maxima: dict[str, float] = {}
    eligible = [
        descriptor for descriptor in descriptors
        if descriptor["normalized"].get("stars") is not None
        and int(descriptor["normalized"].get("stars") or 0) >= min_stars
    ]
    for key in ("stars", "forks", "watchers"):
        maxima[key] = max((float(d["normalized"].get(key) or 0) for d in eligible), default=0.0)
    maxima["ahead"] = max((float(d["normalized"].get("ahead_by") or 0) for d in eligible), default=0.0)
    maxima["changed"] = max((float(d["normalized"].get("changed_files") or 0) for d in eligible), default=0.0)
    profile_maxima = reputation_maxima(profiles)
    ranked: list[dict[str, Any]] = []
    for descriptor in eligible:
        value = descriptor["normalized"]
        repository_components = {
            "stars": weights.get("stars", 0) * normalized_log(value.get("stars"), maxima["stars"]),
            "forks": weights.get("forks", 0) * normalized_log(value.get("forks"), maxima["forks"]),
            "watchers": weights.get("watchers", 0) * normalized_log(value.get("watchers"), maxima["watchers"]),
            "activity": weights.get("activity", 0) * activity_ratio(value.get("pushed_at"), now, horizon),
            "divergence": weights.get("divergence", 0) * normalized_log(value.get("ahead_by"), maxima["ahead"]),
            "changes": weights.get("changes", 0) * normalized_log(value.get("changed_files"), maxima["changed"]),
        }
        repository_score = round(sum(repository_components.values()), 6)
        profile = profiles.get(str(value.get("owner_login") or ""))
        profile_components: dict[str, float] = {}
        profile_values = {
            "followers": profile.get("followers") if profile else None,
            "public_repos": profile.get("public_repos") if profile else None,
            "account_age": account_age_ratio(profile.get("created_at") if profile else None, observed_at, int(config.get("reputation_account_age_cap_days", 5475))),
            "public_gists": profile.get("public_gists") if profile else None,
            "following": profile.get("following") if profile else None,
        }
        profile_maximums = {**profile_maxima, "account_age": 1.0}
        profile_fields = {"followers": "followers", "public_repos": "public_repos", "account_age": "account_age", "public_gists": "public_gists", "following": "following"}
        available_weight = 0.0
        total_profile_weight = sum(reputation_weights.values())
        if profile and profile.get("status") == "ok":
            for key, field in profile_fields.items():
                if key != "account_age" and profile_values[key] is None:
                    continue
                available_weight += reputation_weights.get(key, 0.0)
                ratio = profile_values[key] if key == "account_age" else normalized_log(profile_values[key], profile_maximums[field])
                profile_components[key] = reputation_weights.get(key, 0.0) * ratio
        reputation_coverage = available_weight / total_profile_weight if total_profile_weight > 0 else 0.0
        reputation_score = round(100 * sum(profile_components.values()) / available_weight, 6) if available_weight > 0 else None
        profile_status = "unobserved"
        if profile:
            profile_status = "observed" if reputation_score is not None and reputation_coverage >= 0.999 else ("partial" if reputation_score is not None else "error")
        denominator = repository_weight + reputation_weight * reputation_coverage
        overall_score = repository_score if denominator <= 0 else round(
            (repository_weight * repository_score + reputation_weight * (reputation_score or 0) * reputation_coverage) / denominator,
            6,
        )
        components = {**repository_components, **profile_components}
        ranked.append({
            "full_name": value["full_name"],
            "score": overall_score,
            "repository_influence_score": repository_score,
            "reputation_score": reputation_score,
            "reputation_coverage": round(reputation_coverage, 6),
            "reputation_status": profile_status,
            "repository_weight": repository_weight,
            "reputation_weight": reputation_weight,
            "components": components,
            "raw_metrics": {
                key: value.get(key) for key in ("stars", "forks", "watchers", "open_issues", "pushed_at", "ahead_by", "behind_by", "changed_files", "additions", "deletions")
            } | {
                "owner_login": value.get("owner_login"),
                "owner_profile": {key: profile.get(key) for key in ("followers", "public_repos", "public_gists", "following", "created_at", "fetched_at")} if profile else None,
            },
            "rationale": f"repository influence {repository_weight:.0%} + public-account reputation {reputation_weight:.0%}; repository metrics keep stars/forks/watchers/activity/divergence/changes separate, and missing profile signals are not treated as zero.",
        })
    ranked.sort(
        key=lambda row: (
            -row["score"],
            -int(row["raw_metrics"].get("stars") or 0),
            -int(row["raw_metrics"].get("forks") or 0),
            row["full_name"],
        )
    )
    for index, row in enumerate(ranked, 1):
        row["rank"] = index
    return ranked


def fetch_payload(
    connection: Any,
    config: dict[str, Any],
    token: str | None,
    deep_scan_all: bool,
    deep_limit: int,
    recheck_deep: bool,
) -> dict[str, Any]:
    """Fetch the upstream, every fork page, and the bounded deep-scan set."""

    collected_at = utc_now()
    config = {**config, "collected_at": collected_at}
    upstream_record = api_call(f"https://api.github.com/repos/{config['upstream']}", token)
    upstream_response = upstream_record.get("response") if upstream_record.get("status") == "ok" else {}
    upstream_response = upstream_response if isinstance(upstream_response, dict) else {}
    upstream_branch = str(upstream_response.get("default_branch") or "main")
    pages, rows, errors = fetch_fork_pages(
        config["upstream"], int(config.get("list_page_size", 100)), token, str(config.get("list_sort", "oldest"))
    )
    selected = select_deep_forks(
        connection,
        rows,
        deep_limit,
        deep_scan_all,
        recheck_deep,
        float(config.get("changed_recheck_fraction", 0.2)),
    )
    selected_rows = [row for row in rows if full_name(row) in selected]
    workers = max(1, min(32, int(config.get("deep_scan_workers", 16))))

    def scan_selected(row: dict[str, Any]) -> tuple[str, dict[str, Any], dict[str, Any] | None]:
        slug = full_name(row)
        try:
            return slug, deep_scan_fork(row, config["upstream"], upstream_branch, token, config), None
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, KeyError, TypeError) as error:
            descriptor = metadata_only_fork(row, collected_at)
            descriptor["deep_scan_error"] = api_error(error)
            return slug, descriptor, {"stage": "fork-deep-scan", "full_name": slug, "error": str(error)}

    scanned: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for slug, descriptor, error in executor.map(scan_selected, selected_rows):
            scanned[slug] = descriptor
            if error is not None:
                errors.append(error)
    descriptors: list[dict[str, Any]] = []
    for row in rows:
        slug = full_name(row)
        if not slug:
            continue
        if slug in selected:
            descriptor = scanned[slug]
        else:
            descriptor = metadata_only_fork(row, collected_at)
        descriptors.append(descriptor)
    repository_rankings = rank_forks(descriptors, {**config, "reputation_weight": 0}, collected_at)
    profiles = fetch_owner_profiles(connection, descriptors, repository_rankings, collected_at, token, config)
    for descriptor in descriptors:
        value = descriptor["normalized"]
        profile = profiles.get(str(value.get("owner_login") or ""))
        value["owner_profile_status"] = profile.get("status") if profile else "unobserved"
        value["owner_profile_checked_at"] = profile.get("fetched_at") if profile else None
    rankings = rank_forks(descriptors, config, collected_at, profiles)
    rank_by_name = {row["full_name"]: row for row in rankings}
    items = [build_item(descriptor, collected_at) for descriptor in descriptors]
    for item in items:
        ranking = rank_by_name.get(item["external_id"])
        if ranking:
            item["tags"].append(f"fork-rank-{ranking['rank']}")
        else:
            item["tags"].append("fork-filtered-out")
    return {
        "schema_version": 2,
        "collected_at": collected_at,
        "collector": "scripts/collect_forks.py",
        "method": "GitHub public REST API; no third-party code executed",
        "upstream": {"repository": upstream_record, "normalized": {
            "full_name": config["upstream"],
            "html_url": upstream_response.get("html_url") or f"https://github.com/{config['upstream']}",
            "api_url": upstream_response.get("url") or f"https://api.github.com/repos/{config['upstream']}",
            "default_branch": upstream_branch,
            "description": upstream_response.get("description"),
            "license_spdx": (upstream_response.get("license") or {}).get("spdx_id"),
            "stars": upstream_response.get("stargazers_count"),
            "forks": upstream_response.get("forks_count"),
            "open_issues": upstream_response.get("open_issues_count"),
            "watchers": upstream_response.get("watchers_count"),
            "subscribers": upstream_response.get("subscribers_count"),
            "pushed_at": upstream_response.get("pushed_at"),
            "updated_at": upstream_response.get("updated_at"),
        }},
        "fork_list": {"page_count": len(pages), "fork_count": len(rows), "pages": pages},
        "forks": descriptors,
        "rankings": rankings,
        "owner_profiles": [profile for profile in profiles.values() if not profile.get("from_cache")],
        "ranking_version": config.get("ranking_version", "fork-influence-reputation-v1"),
        "star_filter": {
            "minimum_stars": max(0, int(config.get("min_stars", 0))),
            "observed_forks": len(descriptors),
            "eligible_forks": len(rankings),
            "filtered_out": len(descriptors) - len(rankings),
        },
        "errors": errors,
        "deep_scan": {
            "selected_count": len(selected),
            "selected_forks": sorted(selected),
            "limit": deep_limit,
            "all": deep_scan_all,
            "workers": workers,
            "changed_recheck_fraction": float(config.get("changed_recheck_fraction", 0.2)),
        },
        "observations": [{
            "platform": "github",
            "query": f"forks:{config['upstream']}",
            "source_url": f"https://github.com/{config['upstream']}/network",
            "collected_at": collected_at,
            "collector": "scripts/collect_forks.py",
            "method": "GitHub public REST API",
            "status": "ok" if not errors else "partial",
            "result_count": len(items),
            "notes": "All public fork-list pages are captured; deep compare/commit/README details follow the recorded scan budget.",
            "items": items,
        }],
    }


def write_page_raw_files(payload: dict[str, Any], root: Path) -> tuple[list[Path], list[dict[str, Any]]]:
    """Write each raw fork-list page as its own immutable dated evidence file."""

    paths: list[Path] = []
    references: list[dict[str, Any]] = []
    for index, page in enumerate(payload.get("fork_list", {}).get("pages", []), 1):
        path = root / f"page-{index:03d}.json"
        collect.dump_json(path, page)
        paths.append(path)
        response = page.get("response") if isinstance(page, dict) else None
        references.append({
            "raw_path": str(path.relative_to(ROOT)),
            "raw_sha256": collect.sha256_file(path),
            "url": page.get("url") if isinstance(page, dict) else None,
            "status": page.get("status") if isinstance(page, dict) else None,
            "row_count": len(response) if isinstance(response, list) else 0,
        })
    return paths, references


def raw_snapshot_id(connection: Any, raw_sha: str) -> int:
    """Resolve a stored raw snapshot id."""

    row = connection.execute("SELECT id FROM raw_snapshots WHERE raw_sha256 = ?", (raw_sha,)).fetchone()
    if row is None:
        raise RuntimeError(f"raw snapshot was not stored: {raw_sha}")
    return int(row[0])


def upsert_github_user_profile(connection: Any, profile: dict[str, Any], raw_id: int) -> int:
    """Persist one public GitHub user profile and its raw API response."""

    connection.execute(
        """
        INSERT INTO github_user_profiles(
            login, html_url, api_url, node_id, type, public_repos, public_gists,
            followers, following, created_at, updated_at, fetched_at, status,
            raw_snapshot_id, raw_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(login) DO UPDATE SET
            html_url=COALESCE(excluded.html_url, github_user_profiles.html_url),
            api_url=COALESCE(excluded.api_url, github_user_profiles.api_url),
            node_id=COALESCE(excluded.node_id, github_user_profiles.node_id),
            type=COALESCE(excluded.type, github_user_profiles.type),
            public_repos=COALESCE(excluded.public_repos, github_user_profiles.public_repos),
            public_gists=COALESCE(excluded.public_gists, github_user_profiles.public_gists),
            followers=COALESCE(excluded.followers, github_user_profiles.followers),
            following=COALESCE(excluded.following, github_user_profiles.following),
            created_at=COALESCE(excluded.created_at, github_user_profiles.created_at),
            updated_at=COALESCE(excluded.updated_at, github_user_profiles.updated_at),
            fetched_at=excluded.fetched_at, status=excluded.status,
            raw_snapshot_id=excluded.raw_snapshot_id, raw_json=excluded.raw_json
        """,
        (
            profile["login"], profile.get("html_url"), profile.get("api_url"), profile.get("node_id"),
            profile.get("type"), profile.get("public_repos"), profile.get("public_gists"),
            profile.get("followers"), profile.get("following"), profile.get("created_at"),
            profile.get("updated_at"), profile.get("fetched_at") or utc_now(), profile.get("status", "error"),
            raw_id, profile.get("raw_json") or "{}",
        ),
    )
    row = connection.execute("SELECT id FROM github_user_profiles WHERE login = ?", (profile["login"],)).fetchone()
    if row is None:
        raise RuntimeError(f"profile insert did not return an id: {profile['login']}")
    return int(row[0])


def upsert_network(connection: Any, payload: dict[str, Any], raw_id: int, checked_at: str) -> int:
    """Persist the upstream fork network descriptor."""

    normalized = payload["upstream"]["normalized"]
    connection.execute(
        """
        INSERT INTO fork_networks(
            upstream_full_name, upstream_url, api_url, node_id, default_branch,
            description, license_spdx, stars, forks, open_issues, watchers,
            subscribers, pushed_at, updated_at, last_checked_at, raw_snapshot_id,
            created_at, last_seen_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(upstream_full_name) DO UPDATE SET
            upstream_url=excluded.upstream_url, api_url=excluded.api_url,
            node_id=excluded.node_id, default_branch=excluded.default_branch,
            description=excluded.description, license_spdx=excluded.license_spdx,
            stars=excluded.stars, forks=excluded.forks, open_issues=excluded.open_issues,
            watchers=excluded.watchers, subscribers=excluded.subscribers,
            pushed_at=excluded.pushed_at, updated_at=excluded.updated_at,
            last_checked_at=excluded.last_checked_at, raw_snapshot_id=excluded.raw_snapshot_id,
            last_seen_at=excluded.last_seen_at
        """,
        (
            normalized["full_name"], normalized["html_url"], normalized["api_url"],
            None, normalized["default_branch"], normalized.get("description"),
            normalized.get("license_spdx"), normalized.get("stars"), normalized.get("forks"),
            normalized.get("open_issues"), normalized.get("watchers"), normalized.get("subscribers"),
            normalized.get("pushed_at"), normalized.get("updated_at"), checked_at, raw_id,
            checked_at, checked_at,
        ),
    )
    row = connection.execute("SELECT id FROM fork_networks WHERE upstream_full_name = ?", (normalized["full_name"],)).fetchone()
    if row is None:
        raise RuntimeError("fork network insert did not return an id")
    return int(row[0])


def persist_forks(
    connection: Any,
    payload: dict[str, Any],
    collection_run_id: int,
    dataset_version: str,
    raw_id: int,
    checked_at: str,
) -> None:
    """Persist fork identities, snapshots, files, commits, and rankings."""

    network_id = upsert_network(connection, payload, raw_id, checked_at)
    profile_ids: dict[str, int] = {}
    for profile in payload.get("owner_profiles", []):
        if isinstance(profile, dict) and profile.get("login"):
            profile_ids[str(profile["login"])] = upsert_github_user_profile(connection, profile, raw_id)
    item_ids: dict[str, int] = {}
    for item in payload["observations"][0]["items"]:
        row = connection.execute("SELECT id FROM items WHERE canonical_url = ?", (collect.canonical_url(str(item["url"])),)).fetchone()
        if row is not None:
            item_ids[str(item["external_id"])] = int(row[0])
    for descriptor in payload.get("forks", []):
        value = descriptor["normalized"]
        existing_summary = str(value.get("change_summary") or "")
        if not existing_summary or (
            value.get("detail_status") == "metadata-only"
            and existing_summary.startswith("当前仅确认这是 upstream 的公开 Fork")
        ):
            value["change_summary"] = change_summary(value, str(descriptor.get("readme_text_for_analysis") or ""))
        full = value["full_name"]
        owner_login = str(value.get("owner_login") or "")
        if owner_login and owner_login not in profile_ids:
            profile_row = connection.execute("SELECT id FROM github_user_profiles WHERE login = ?", (owner_login,)).fetchone()
            if profile_row is not None:
                profile_ids[owner_login] = int(profile_row[0])
        commit = value.get("latest_commit") or {}
        existing_fork = connection.execute(
            "SELECT id FROM fork_repositories WHERE full_name = ?",
            (full,),
        ).fetchone()
        prior_deep = None
        if existing_fork is not None:
            prior_deep = connection.execute(
                """
                SELECT compare_status, ahead_by, behind_by, total_commits, changed_files,
                       additions, deletions, modification_categories, change_summary,
                       latest_commit_sha, latest_commit_message, latest_commit_at, readme_sha
                FROM fork_snapshots
                WHERE fork_id = ? AND status IN ('ok', 'partial')
                ORDER BY observed_at DESC, id DESC
                LIMIT 1
                """,
                (int(existing_fork[0]),),
            ).fetchone()
        retained_deep_fields = (
            "compare_status", "ahead_by", "behind_by", "total_commits", "changed_files",
            "additions", "deletions", "latest_commit_sha", "latest_commit_message",
            "latest_commit_at", "readme_sha",
        )
        if value.get("detail_status") == "metadata-only" and prior_deep is not None:
            for field in retained_deep_fields:
                if value.get(field) is None and prior_deep[field] is not None:
                    value[field] = prior_deep[field]
            if not value.get("modification_categories") and prior_deep["modification_categories"]:
                value["modification_categories"] = json.loads(str(prior_deep["modification_categories"]))
            if not value.get("change_summary") or value["change_summary"] == change_summary(value):
                value["change_summary"] = prior_deep["change_summary"] or value["change_summary"]
        connection.execute(
            """
            INSERT INTO fork_repositories(
                network_id, item_id, full_name, html_url, api_url, node_id, owner_login,
                owner_type, owner_profile_id, owner_profile_status, owner_profile_checked_at,
                parent_full_name, source_full_name, default_branch, description,
                license_spdx, visibility, is_fork, archived, disabled, stars, forks,
                open_issues, watchers, subscribers, size_kb, forked_at, created_at,
                updated_at, pushed_at, last_checked_at, latest_commit_sha,
                latest_commit_message, latest_commit_at, readme_sha, change_summary, status,
                raw_snapshot_id, first_seen_run_id, last_seen_run_id, last_deep_checked_at,
                detail_status, first_seen_at, last_seen_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(full_name) DO UPDATE SET
                network_id=excluded.network_id, item_id=COALESCE(excluded.item_id, fork_repositories.item_id),
                html_url=excluded.html_url, api_url=excluded.api_url, node_id=excluded.node_id,
                owner_login=excluded.owner_login, owner_type=excluded.owner_type,
                owner_profile_id=COALESCE(excluded.owner_profile_id, fork_repositories.owner_profile_id),
                owner_profile_status=excluded.owner_profile_status,
                owner_profile_checked_at=excluded.owner_profile_checked_at,
                parent_full_name=excluded.parent_full_name, source_full_name=excluded.source_full_name,
                default_branch=excluded.default_branch, description=excluded.description,
                license_spdx=excluded.license_spdx, visibility=excluded.visibility,
                is_fork=excluded.is_fork, archived=excluded.archived, disabled=excluded.disabled,
                stars=excluded.stars, forks=excluded.forks, open_issues=excluded.open_issues,
                watchers=excluded.watchers, subscribers=excluded.subscribers, size_kb=excluded.size_kb,
                forked_at=excluded.forked_at, created_at=excluded.created_at, updated_at=excluded.updated_at,
                pushed_at=excluded.pushed_at, last_checked_at=excluded.last_checked_at,
                latest_commit_sha=COALESCE(excluded.latest_commit_sha, fork_repositories.latest_commit_sha),
                latest_commit_message=COALESCE(excluded.latest_commit_message, fork_repositories.latest_commit_message),
                latest_commit_at=COALESCE(excluded.latest_commit_at, fork_repositories.latest_commit_at),
                readme_sha=COALESCE(excluded.readme_sha, fork_repositories.readme_sha),
                change_summary=COALESCE(excluded.change_summary, fork_repositories.change_summary),
                status=excluded.status, raw_snapshot_id=excluded.raw_snapshot_id,
                last_seen_run_id=excluded.last_seen_run_id,
                last_deep_checked_at=COALESCE(excluded.last_deep_checked_at, fork_repositories.last_deep_checked_at),
                detail_status=CASE WHEN excluded.detail_status = 'ok' THEN 'ok' ELSE fork_repositories.detail_status END,
                last_seen_at=excluded.last_seen_at
            """,
            (
                network_id, item_ids.get(full), full, value.get("html_url"), value.get("api_url"),
                value.get("node_id"), value.get("owner_login"), value.get("owner_type"), profile_ids.get(owner_login),
                value.get("owner_profile_status", "unobserved"), value.get("owner_profile_checked_at"),
                value.get("parent_full_name"), value.get("source_full_name"), value.get("default_branch"),
                value.get("description"), value.get("license_spdx"), value.get("visibility"),
                value.get("is_fork", 1), value.get("archived", 0), value.get("disabled", 0),
                value.get("stars"), value.get("forks"), value.get("open_issues"), value.get("watchers"),
                value.get("subscribers"), value.get("size_kb"), value.get("forked_at"), value.get("created_at"),
                value.get("updated_at"), value.get("pushed_at"), checked_at, commit.get("sha"),
                commit.get("message"), commit.get("committed_at"), value.get("readme_sha"), value.get("change_summary"),
                value.get("status", "ok"), raw_id, collection_run_id, collection_run_id,
                value.get("deep_scanned_at"), value.get("detail_status", "metadata-only"), checked_at, checked_at,
            ),
        )
        fork_id = int(connection.execute("SELECT id FROM fork_repositories WHERE full_name = ?", (full,)).fetchone()[0])
        snapshot = {
            "fork_id": fork_id,
            "collection_run_id": collection_run_id,
            "raw_snapshot_id": raw_id,
            "dataset_version": dataset_version,
            "observed_at": checked_at,
            "stars": value.get("stars"),
            "forks": value.get("forks"),
            "open_issues": value.get("open_issues"),
            "watchers": value.get("watchers"),
            "subscribers": value.get("subscribers"),
            "pushed_at": value.get("pushed_at"),
            "updated_at": value.get("updated_at"),
            "compare_status": value.get("compare_status"),
            "ahead_by": value.get("ahead_by"),
            "behind_by": value.get("behind_by"),
            "total_commits": value.get("total_commits"),
            "changed_files": value.get("changed_files"),
            "additions": value.get("additions"),
            "deletions": value.get("deletions"),
            "modification_categories": json.dumps(value.get("modification_categories") or {}, sort_keys=True),
            "change_summary": value.get("change_summary"),
            "latest_commit_sha": commit.get("sha"),
            "latest_commit_message": commit.get("message"),
            "latest_commit_at": commit.get("committed_at"),
            "readme_sha": value.get("readme_sha"),
            "tree_sha": None,
            "status": value.get("detail_status", "metadata-only"),
            "notes": (
                "Complete fork metadata captured; deep fields are retained from the latest deep observation."
                if value.get("detail_status") == "metadata-only" and prior_deep is not None
                else "Complete fork metadata captured; deep fields are NULL when this run did not select the fork."
            ),
        }
        connection.execute(
            """
            INSERT INTO fork_snapshots(
                fork_id, collection_run_id, raw_snapshot_id, dataset_version, observed_at,
                stars, forks, open_issues, watchers, subscribers, pushed_at, updated_at,
                compare_status, ahead_by, behind_by, total_commits, changed_files,
                additions, deletions, modification_categories, change_summary, latest_commit_sha,
                latest_commit_message, latest_commit_at, readme_sha, tree_sha, status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(fork_id, collection_run_id) DO UPDATE SET
                raw_snapshot_id=excluded.raw_snapshot_id, dataset_version=excluded.dataset_version,
                observed_at=excluded.observed_at, stars=excluded.stars, forks=excluded.forks,
                open_issues=excluded.open_issues, watchers=excluded.watchers, subscribers=excluded.subscribers,
                pushed_at=excluded.pushed_at, updated_at=excluded.updated_at, compare_status=excluded.compare_status,
                ahead_by=excluded.ahead_by, behind_by=excluded.behind_by, total_commits=excluded.total_commits,
                changed_files=excluded.changed_files, additions=excluded.additions, deletions=excluded.deletions,
                modification_categories=excluded.modification_categories, change_summary=excluded.change_summary,
                latest_commit_sha=excluded.latest_commit_sha,
                latest_commit_message=excluded.latest_commit_message, latest_commit_at=excluded.latest_commit_at,
                readme_sha=excluded.readme_sha, status=excluded.status, notes=excluded.notes
            """,
            tuple(snapshot.values()),
        )
        snapshot_id = int(connection.execute("SELECT id FROM fork_snapshots WHERE fork_id = ? AND collection_run_id = ?", (fork_id, collection_run_id)).fetchone()[0])
        for file in descriptor.get("files", []):
            connection.execute(
                """
                INSERT INTO fork_file_changes(
                    snapshot_id, filename, status, additions, deletions, changes,
                    previous_filename, category, blob_url, raw_url, raw_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(snapshot_id, filename) DO UPDATE SET
                    status=excluded.status, additions=excluded.additions, deletions=excluded.deletions,
                    changes=excluded.changes, previous_filename=excluded.previous_filename,
                    category=excluded.category, blob_url=excluded.blob_url, raw_url=excluded.raw_url,
                    raw_json=excluded.raw_json
                """,
                (
                    snapshot_id, file["filename"], file.get("status"), file.get("additions"),
                    file.get("deletions"), file.get("changes"), file.get("previous_filename"),
                    file["category"], file.get("blob_url"), file.get("raw_url"),
                    json.dumps(file.get("raw") or file, ensure_ascii=False, sort_keys=True),
                ),
            )
        commits = descriptor.get("commits") or {}
        commit_rows = commits.get("response") if commits.get("status") == "ok" else []
        if isinstance(commit_rows, list):
            for row in commit_rows:
                if not isinstance(row, dict) or not row.get("sha"):
                    continue
                commit_data = row.get("commit") or {}
                author_data = commit_data.get("author") or {}
                committer_data = commit_data.get("committer") or {}
                connection.execute(
                    """
                    INSERT INTO fork_commits(
                        fork_id, snapshot_id, collection_run_id, sha, html_url, message,
                        author_login, committer_login, authored_at, committed_at,
                        first_seen_at, last_seen_at, raw_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(fork_id, sha) DO UPDATE SET
                        snapshot_id=excluded.snapshot_id, collection_run_id=excluded.collection_run_id,
                        html_url=excluded.html_url, message=excluded.message,
                        author_login=excluded.author_login, committer_login=excluded.committer_login,
                        authored_at=excluded.authored_at, committed_at=excluded.committed_at,
                        last_seen_at=excluded.last_seen_at, raw_json=excluded.raw_json
                    """,
                    (
                        fork_id, snapshot_id, collection_run_id, row["sha"], row.get("html_url"),
                        str(commit_data.get("message") or ""),
                        (row.get("author") or {}).get("login") if isinstance(row.get("author"), dict) else None,
                        (row.get("committer") or {}).get("login") if isinstance(row.get("committer"), dict) else None,
                        author_data.get("date"), committer_data.get("date"), checked_at, checked_at,
                        json.dumps(row, ensure_ascii=False, sort_keys=True),
                    ),
                )
        ranking = next((row for row in payload.get("rankings", []) if row["full_name"] == full), None)
        if ranking is None:
            continue
        connection.execute(
            """
            INSERT INTO fork_rankings(
                fork_id, collection_run_id, ranking_version, observed_at, rank,
                influence_score, overall_score, reputation_score, reputation_coverage, reputation_status,
                stars_component, forks_component, watchers_component,
                activity_component, divergence_component, change_component, rationale,
                reputation_followers_component, reputation_repos_component, reputation_age_component,
                reputation_gists_component, reputation_following_component, repository_weight,
                reputation_weight, components_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(fork_id, collection_run_id, ranking_version) DO UPDATE SET
                observed_at=excluded.observed_at, rank=excluded.rank, influence_score=excluded.influence_score,
                overall_score=excluded.overall_score, reputation_score=excluded.reputation_score,
                reputation_coverage=excluded.reputation_coverage, reputation_status=excluded.reputation_status,
                stars_component=excluded.stars_component, forks_component=excluded.forks_component,
                watchers_component=excluded.watchers_component, activity_component=excluded.activity_component,
                divergence_component=excluded.divergence_component, change_component=excluded.change_component,
                reputation_followers_component=excluded.reputation_followers_component,
                reputation_repos_component=excluded.reputation_repos_component,
                reputation_age_component=excluded.reputation_age_component,
                reputation_gists_component=excluded.reputation_gists_component,
                reputation_following_component=excluded.reputation_following_component,
                repository_weight=excluded.repository_weight, reputation_weight=excluded.reputation_weight,
                rationale=excluded.rationale, components_json=excluded.components_json
            """,
            (
                fork_id, collection_run_id, str(payload.get("ranking_version") or "fork-influence-v1"), checked_at,
                ranking["rank"], ranking.get("repository_influence_score", ranking["score"]), ranking["score"],
                ranking.get("reputation_score"), ranking.get("reputation_coverage", 0), ranking.get("reputation_status", "unobserved"),
                ranking["components"].get("stars", 0),
                ranking["components"].get("forks", 0), ranking["components"].get("watchers", 0),
                ranking["components"].get("activity", 0), ranking["components"].get("divergence", 0),
                ranking["components"].get("changes", 0), ranking["rationale"],
                ranking["components"].get("followers"), ranking["components"].get("public_repos"),
                ranking["components"].get("account_age"), ranking["components"].get("public_gists"),
                ranking["components"].get("following"), ranking.get("repository_weight", 0.6),
                ranking.get("reputation_weight", 0.4),
                json.dumps({"components": ranking["components"], "raw_metrics": ranking["raw_metrics"], "reputation_status": ranking.get("reputation_status")}, sort_keys=True),
            ),
        )


def import_payload(
    connection: Any,
    payload: dict[str, Any],
    raw_path: Path,
    page_paths: list[Path],
    run_id: int,
    version: str,
) -> tuple[collect.ImportStats, int, int]:
    """Import the manifest, page raw files, and normalized fork tables."""

    manifest_preexisting = connection.execute(
        "SELECT 1 FROM raw_snapshots WHERE raw_sha256 = ?",
        (collect.sha256_file(raw_path),),
    ).fetchone() is not None
    stats = collect.import_payload(connection, payload, run_id, raw_path)
    manifest_sha = collect.sha256_file(raw_path)
    manifest_id = raw_snapshot_id(connection, manifest_sha)
    skipped = 0
    for page_path in page_paths:
        _, _, is_new = collect.store_raw_snapshot(connection, page_path, run_id, str(payload["collected_at"]))
        if not is_new:
            skipped += 1
    persist_forks(connection, payload, run_id, version, manifest_id, str(payload["collected_at"]))
    stats.raw_files_seen = len(page_paths) + 1
    stats.raw_files_skipped = skipped + int(manifest_preexisting)
    connection.execute(
        "UPDATE collection_runs SET notes = ? WHERE id = ?",
        (
            f"fork network {payload['upstream']['normalized']['full_name']}; "
            f"public forks={len(payload.get('forks', []))}; "
            f"deep scans={payload.get('deep_scan', {}).get('selected_count', 0)}; "
            f"fork-list pages={len(page_paths)}",
            run_id,
        ),
    )
    return stats, manifest_id, len(page_paths) + 1


def read_config(path: Path) -> dict[str, Any]:
    """Read and validate the fork collector configuration."""

    config = json.loads(path.read_text(encoding="utf-8"))
    if str(config.get("upstream") or "") != UPSTREAM:
        raise ValueError(f"fork collector is scoped to {UPSTREAM}")
    return config


def main() -> int:
    """Collect the public fork network and persist its dated snapshot."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DB_PATH)
    parser.add_argument("--config", type=Path, default=CONFIG_PATH)
    parser.add_argument("--raw-output", type=Path, help="manifest path; defaults to data/raw/forks/<timestamp>/manifest.json")
    parser.add_argument("--deep-limit", type=int, help="deep scans per run; defaults to config")
    parser.add_argument("--min-stars", type=int, help="minimum Fork stars included in the ranking; all observed Forks remain in raw/SQLite")
    parser.add_argument("--deep-scan-all", action="store_true", help="deep-scan every public fork returned by GitHub")
    parser.add_argument("--recheck-deep", action="store_true", help="recheck highest-influence Forks even if previously scanned")
    parser.add_argument("--no-token", action="store_true", help="do not read GH_TOKEN, GITHUB_TOKEN, or gh auth token")
    parser.add_argument("--raw-input", type=Path, help="re-import an existing manifest without making API requests")
    args = parser.parse_args()
    config = read_config(args.config)
    if args.min_stars is not None:
        config["min_stars"] = max(0, args.min_stars)
    deep_limit = max(0, int(args.deep_limit if args.deep_limit is not None else config.get("deep_scan_limit", 100)))
    token = None if args.no_token else github_token()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    raw_root = args.raw_output.parent if args.raw_output else RAW_DIR / stamp
    raw_root.mkdir(parents=True, exist_ok=True)
    manifest_path = args.raw_output or (raw_root / "manifest.json")
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    collect.init_db(args.db)
    payload: dict[str, Any] = {"collected_at": utc_now(), "collector": "scripts/collect_forks.py", "observations": []}
    with collect.connect(args.db) as connection:
        run_id, version, _ = collect.begin_collection_run(connection, "forks", utc_now())
        stats = collect.ImportStats()
        try:
            if args.raw_input:
                input_path = args.raw_input if args.raw_input.is_absolute() else ROOT / args.raw_input
                payload = deduplicate_payload(collect.load_json(input_path))
                observed_at = str(payload.get("collected_at") or utc_now())
                logins = {
                    str(descriptor["normalized"].get("owner_login") or "").strip()
                    for descriptor in payload.get("forks", [])
                }
                profiles = load_cached_profiles(connection, logins - {""})
                profiles.update({
                    str(profile["login"]): profile
                    for profile in payload.get("owner_profiles", [])
                    if isinstance(profile, dict) and profile.get("login")
                })
                for descriptor in payload.get("forks", []):
                    value = descriptor["normalized"]
                    profile = profiles.get(str(value.get("owner_login") or ""))
                    value["owner_profile_status"] = profile.get("status") if profile else "unobserved"
                    value["owner_profile_checked_at"] = profile.get("fetched_at") if profile else None
                payload["rankings"] = rank_forks(payload.get("forks", []), config, observed_at, profiles)
                rank_by_name = {row["full_name"]: row for row in payload["rankings"]}
                for item in (payload.get("observations") or [{}])[0].get("items", []):
                    item["tags"] = [
                        tag for tag in item.get("tags", [])
                        if not str(tag).startswith("fork-rank-") and tag != "fork-filtered-out"
                    ]
                    ranking = rank_by_name.get(str(item.get("external_id") or ""))
                    item["tags"].append(f"fork-rank-{ranking['rank']}" if ranking else "fork-filtered-out")
                payload["star_filter"] = {
                    "minimum_stars": max(0, int(config.get("min_stars", 0))),
                    "observed_forks": len(payload.get("forks", [])),
                    "eligible_forks": len(payload["rankings"]),
                    "filtered_out": len(payload.get("forks", [])) - len(payload["rankings"]),
                }
                manifest_path = input_path
                page_paths = sorted(input_path.parent.glob("page-*.json"))
            else:
                payload = deduplicate_payload(
                    fetch_payload(connection, config, token, args.deep_scan_all, deep_limit, args.recheck_deep)
                )
                page_paths, page_references = write_page_raw_files(payload, manifest_path.parent)
                payload["fork_list"]["pages"] = page_references
                collect.dump_json(manifest_path, payload)
            stats, _, raw_count = import_payload(connection, payload, manifest_path, page_paths, run_id, version)
            stats.raw_files_seen = raw_count
            collect.finish_collection_run(connection, run_id, stats)
        except Exception as error:
            collect.finish_collection_run(connection, run_id, stats, "failed", str(error))
            connection.commit()
            raise
    token_note = "authenticated" if token else "unauthenticated"
    print(
        f"indexed {len(payload.get('forks', []))} public forks in {version}; "
        f"deep scans={payload.get('deep_scan', {}).get('selected_count', 0)}; "
        f"raw files={stats.raw_files_seen}; auth={token_note}; manifest={manifest_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
