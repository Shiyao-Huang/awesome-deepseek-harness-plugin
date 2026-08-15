#!/usr/bin/env python3
"""Collect public DeepSeek Harness ecosystem records into SQLite."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
SCHEMA_PATH = ROOT / "src" / "schema.sql"
CONFIG_PATH = ROOT / "config" / "queries.json"
RAW_DIR = ROOT / "data" / "raw"
SCHEMA_VERSION = 2


@dataclass
class ImportStats:
    """Counters persisted on one collection run."""

    raw_files_seen: int = 0
    raw_files_skipped: int = 0
    observations_seen: int = 0
    item_observations: int = 0
    new_items: int = 0
    existing_items: int = 0
    new_metrics: int = 0
    duplicate_metrics: int = 0

    def add(self, other: "ImportStats") -> None:
        """Add counters from one imported raw file."""

        for field in self.__dataclass_fields__:
            setattr(self, field, getattr(self, field) + getattr(other, field))

SOURCE_DEFAULTS = {
    "github": {
        "display_name": "GitHub",
        "base_url": "https://github.com",
        "collection_mode": "public REST API",
        "terms_url": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
    },
    "hacker_news": {
        "display_name": "Hacker News",
        "base_url": "https://news.ycombinator.com",
        "collection_mode": "Algolia public search API",
        "terms_url": "https://news.ycombinator.com/newsguidelines.html",
    },
    "x": {
        "display_name": "X",
        "base_url": "https://x.com",
        "collection_mode": "ego-browser visible DOM",
        "terms_url": "https://x.com/en/tos",
    },
    "xiaohongshu": {
        "display_name": "小红书",
        "base_url": "https://www.xiaohongshu.com",
        "collection_mode": "ego-browser visible DOM",
        "terms_url": "https://www.xiaohongshu.com/privacy_policy",
    },
    "youtube": {
        "display_name": "YouTube",
        "base_url": "https://www.youtube.com",
        "collection_mode": "ego-browser visible DOM",
        "terms_url": "https://www.youtube.com/static?template=terms",
    },
    "wechat": {
        "display_name": "微信公众号",
        "base_url": "https://mp.weixin.qq.com",
        "collection_mode": "ego-browser visible DOM",
        "terms_url": "https://weixin.qq.com/cgi-bin/readtemplate?t=weixin_agreement&s=privacy",
    },
    "bilibili": {
        "display_name": "哔哩哔哩",
        "base_url": "https://www.bilibili.com",
        "collection_mode": "public web metadata API",
        "terms_url": "https://www.bilibili.com/blackboard/aboutUs.html",
    },
    "reddit": {
        "display_name": "Reddit",
        "base_url": "https://www.reddit.com",
        "collection_mode": "ego-browser visible DOM",
        "terms_url": "https://www.redditinc.com/policies/user-agreement",
    },
    "zhihu": {
        "display_name": "知乎",
        "base_url": "https://www.zhihu.com",
        "collection_mode": "ego-browser visible DOM",
        "terms_url": "https://www.zhihu.com/term/ugc",
    },
    "linuxdo": {
        "display_name": "LINUX DO",
        "base_url": "https://linux.do",
        "collection_mode": "public page metadata",
        "terms_url": "https://linux.do/terms",
    },
    "v2ex": {
        "display_name": "V2EX",
        "base_url": "https://v2ex.com",
        "collection_mode": "public page metadata",
        "terms_url": "https://www.v2ex.com/about",
    },
    "weibo": {
        "display_name": "微博",
        "base_url": "https://weibo.com",
        "collection_mode": "public page metadata",
        "terms_url": "https://weibo.com/signup/v5/privacy",
    },
    "official": {
        "display_name": "DeepSeek 官方站",
        "base_url": "https://www.deepseek.com",
        "collection_mode": "public page metadata",
        "terms_url": "https://www.deepseek.com/terms",
    },
    "web": {
        "display_name": "Open Web",
        "base_url": "",
        "collection_mode": "public page metadata",
        "terms_url": "",
    },
    "linuxdo": {
        "display_name": "LINUX DO",
        "base_url": "https://linux.do",
        "collection_mode": "ego-browser visible DOM",
        "terms_url": "https://linux.do/tos",
    },
    "v2ex": {
        "display_name": "V2EX",
        "base_url": "https://v2ex.com",
        "collection_mode": "ego-browser visible DOM",
        "terms_url": "https://www.v2ex.com/about",
    },
    "weibo": {
        "display_name": "微博",
        "base_url": "https://weibo.com",
        "collection_mode": "ego-browser visible DOM",
        "terms_url": "https://weibo.com/signup/v5/privacy",
    },
    "official": {
        "display_name": "DeepSeek 官方站",
        "base_url": "https://www.deepseek.com",
        "collection_mode": "ego-browser visible DOM",
        "terms_url": "https://www.deepseek.com/terms",
    },
}


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp with second precision."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    """Read one UTF-8 JSON value from disk."""

    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, value: Any) -> None:
    """Write deterministic UTF-8 JSON for reviewable raw snapshots."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    """Return a file's SHA-256 digest."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def connect(path: Path = DB_PATH) -> sqlite3.Connection:
    """Open a foreign-key-enforcing SQLite connection."""

    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 30000")
    return connection


def snapshot_version(timestamp: str, prefix: str = "v") -> str:
    """Convert a UTC timestamp into a sortable dataset snapshot version."""

    compact = re.sub(r"[^0-9TZ]", "", timestamp)
    return f"{prefix}{compact}"


def ensure_column(connection: sqlite3.Connection, table: str, name: str, sql_type: str) -> None:
    """Add one column when upgrading a database created by an older schema."""

    columns = {row[1] for row in connection.execute(f"PRAGMA table_info({table})")}
    if name not in columns:
        connection.execute(f"ALTER TABLE {table} ADD COLUMN {name} {sql_type}")


def backfill_collection_runs(connection: sqlite3.Connection) -> None:
    """Attach legacy observations, metrics, raw files, and items to dated runs."""

    timestamps = {
        row[0]
        for table, column in (("observations", "collected_at"), ("metrics", "observed_at"))
        for row in connection.execute(f"SELECT DISTINCT {column} FROM {table} WHERE {column} IS NOT NULL")
    }
    for timestamp in sorted(timestamps):
        unlinked = connection.execute(
            "SELECT 1 FROM observations WHERE collected_at = ? AND collection_run_id IS NULL "
            "UNION ALL SELECT 1 FROM metrics WHERE observed_at = ? AND collection_run_id IS NULL LIMIT 1",
            (timestamp, timestamp),
        ).fetchone()
        if unlinked is None:
            continue
        version = snapshot_version(str(timestamp), "legacy-")
        connection.execute(
            """
            INSERT OR IGNORE INTO collection_runs(
                dataset_version, started_at, finished_at, trigger, status, notes
            ) VALUES (?, ?, ?, 'legacy-migration', 'backfilled', 'Migrated from the pre-versioned SQLite schema.')
            """,
            (version, timestamp, timestamp),
        )
        run_id = int(connection.execute("SELECT id FROM collection_runs WHERE dataset_version = ?", (version,)).fetchone()[0])
        connection.execute("UPDATE observations SET collection_run_id = ? WHERE collection_run_id IS NULL AND collected_at = ?", (run_id, timestamp))
        connection.execute("UPDATE metrics SET collection_run_id = ? WHERE collection_run_id IS NULL AND observed_at = ?", (run_id, timestamp))

    raw_rows = connection.execute(
        "SELECT DISTINCT raw_path, raw_sha256, collected_at, collection_run_id FROM observations WHERE raw_path IS NOT NULL"
    ).fetchall()
    for row in raw_rows:
        raw_path = ROOT / str(row[0])
        raw_sha = str(row[1] or (sha256_file(raw_path) if raw_path.exists() else "missing:" + str(row[0])))
        payload = raw_path.read_text(encoding="utf-8") if raw_path.exists() else json.dumps({"missing_raw_path": str(row[0])}, ensure_ascii=False)
        connection.execute(
            """
            INSERT OR IGNORE INTO raw_snapshots(
                collection_run_id, raw_sha256, raw_path, collected_at, byte_size, payload_json
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (row[3], raw_sha, str(row[0]), str(row[2]), len(payload.encode("utf-8")), payload),
        )
        snapshot_id = int(connection.execute("SELECT id FROM raw_snapshots WHERE raw_sha256 = ?", (raw_sha,)).fetchone()[0])
        connection.execute(
            "UPDATE observations SET raw_sha256 = ?, raw_snapshot_id = ? WHERE raw_path = ? AND raw_snapshot_id IS NULL",
            (raw_sha, snapshot_id, str(row[0])),
        )

    connection.execute(
        """
        UPDATE observations
        SET raw_snapshot_id = (
            SELECT id FROM raw_snapshots AS s
            WHERE s.raw_sha256 = observations.raw_sha256
        )
        WHERE raw_snapshot_id IS NULL AND raw_sha256 IS NOT NULL
        """
    )
    connection.execute(
        """
        UPDATE raw_snapshots
        SET collection_run_id = (
            SELECT collection_run_id FROM observations AS o
            WHERE o.raw_snapshot_id = raw_snapshots.id AND o.collection_run_id IS NOT NULL
            ORDER BY o.id LIMIT 1
        )
        WHERE collection_run_id IS NULL
        """
    )
    connection.execute(
        """
        UPDATE items
        SET first_seen_run_id = (
                SELECT o.collection_run_id FROM item_observations AS io
                JOIN observations AS o ON o.id = io.observation_id
                WHERE io.item_id = items.id AND o.collection_run_id IS NOT NULL
                ORDER BY o.collected_at, o.id LIMIT 1
            ),
            last_seen_run_id = (
                SELECT o.collection_run_id FROM item_observations AS io
                JOIN observations AS o ON o.id = io.observation_id
                WHERE io.item_id = items.id AND o.collection_run_id IS NOT NULL
                ORDER BY o.collected_at DESC, o.id DESC LIMIT 1
            )
        WHERE first_seen_run_id IS NULL OR last_seen_run_id IS NULL
        """
    )


def init_db(path: Path = DB_PATH) -> None:
    """Create or migrate the SQLite schema without discarding raw evidence."""

    with connect(path) as connection:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        has_observations = bool(connection.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'observations'").fetchone())
        if has_observations:
            prefix = schema.split("CREATE TABLE IF NOT EXISTS observations", 1)[0]
            connection.executescript(prefix)
            ensure_column(connection, "observations", "collection_run_id", "INTEGER REFERENCES collection_runs(id)")
            ensure_column(connection, "observations", "raw_snapshot_id", "INTEGER REFERENCES raw_snapshots(id)")
            ensure_column(connection, "items", "first_seen_run_id", "INTEGER REFERENCES collection_runs(id)")
            ensure_column(connection, "items", "last_seen_run_id", "INTEGER REFERENCES collection_runs(id)")
            ensure_column(connection, "metrics", "collection_run_id", "INTEGER REFERENCES collection_runs(id)")
        connection.executescript(schema)
        for name, sql_type in (
            ("favorites", "INTEGER"), ("shares", "INTEGER"), ("coins", "INTEGER"),
            ("danmaku", "INTEGER"), ("upvote_ratio", "REAL"),
        ):
            ensure_column(connection, "metrics", name, sql_type)
        backfill_collection_runs(connection)
        connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
        connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_metrics_dedupe ON metrics(item_id, observed_at, metric_source)")


def begin_collection_run(
    connection: sqlite3.Connection,
    trigger: str,
    scheduled_for: str | None = None,
) -> tuple[int, str, str]:
    """Create a dated dataset version before importing a batch."""

    started_at = utc_now()
    base_version = snapshot_version(started_at)
    version = base_version
    suffix = 2
    while connection.execute("SELECT 1 FROM collection_runs WHERE dataset_version = ?", (version,)).fetchone():
        version = f"{base_version}-{suffix}"
        suffix += 1
    cursor = connection.execute(
        """
        INSERT INTO collection_runs(dataset_version, started_at, scheduled_for, trigger, status)
        VALUES (?, ?, ?, ?, 'running')
        """,
        (version, started_at, scheduled_for, trigger),
    )
    return int(cursor.lastrowid), version, started_at


def finish_collection_run(
    connection: sqlite3.Connection,
    run_id: int,
    stats: ImportStats,
    status: str = "succeeded",
    error_message: str | None = None,
) -> None:
    """Persist batch counters and final status for one dataset version."""

    connection.execute(
        """
        UPDATE collection_runs
        SET finished_at = ?, status = ?, raw_files_seen = ?, raw_files_skipped = ?,
            observations_seen = ?, item_observations = ?, new_items = ?,
            existing_items = ?, new_metrics = ?, duplicate_metrics = ?, error_message = ?
        WHERE id = ?
        """,
        (
            utc_now(), status, stats.raw_files_seen, stats.raw_files_skipped,
            stats.observations_seen, stats.item_observations, stats.new_items,
            stats.existing_items, stats.new_metrics, stats.duplicate_metrics,
            error_message, run_id,
        ),
    )


def canonical_url(url: str) -> str:
    """Normalize known platform URLs while preserving the public record identity."""

    if not url:
        return ""
    parts = urlsplit(url.strip())
    host = parts.netloc.lower()
    path = parts.path.rstrip("/") or "/"
    query: dict[str, list[str]] = {}
    if host in {"x.com", "www.x.com", "twitter.com", "www.twitter.com"}:
        return urlunsplit(("https", "x.com", path, "", ""))
    if host in {"youtube.com", "www.youtube.com", "youtu.be"}:
        values = parse_qs(parts.query)
        if "v" in values:
            query = {"v": [values["v"][0]]}
        elif host == "youtu.be":
            path = f"/watch"
            query = {"v": [parts.path.strip("/")]}
        return urlunsplit(("https", "www.youtube.com", path, urlencode(query, doseq=True), ""))
    if "xiaohongshu.com" in host and "/search_result/" in path:
        note_id = path.split("/search_result/", 1)[1]
        return f"https://www.xiaohongshu.com/explore/{note_id}"
    if host.endswith("github.com"):
        return urlunsplit(("https", host, path, "", ""))
    return urlunsplit((parts.scheme or "https", parts.netloc, path, parts.query, ""))


def metric_int(value: Any) -> int | None:
    """Parse visible integer, compact K/M, and common Chinese count labels."""

    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value).strip().replace(",", "")
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*([KkMm万亿]?)", text)
    if not match:
        return None
    number = float(match.group(1))
    suffix = match.group(2).lower()
    multiplier = {"k": 1_000, "m": 1_000_000, "万": 10_000, "亿": 100_000_000}.get(suffix, 1)
    return int(number * multiplier)


def metric_float(value: Any) -> float | None:
    """Parse a decimal platform metric such as Reddit's upvote ratio."""

    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def strip_html(value: str | None) -> str | None:
    """Convert HN HTML snippets to compact text without losing the source wording."""

    if not value:
        return None
    text = re.sub(r"<[^>]+>", " ", html.unescape(value))
    return re.sub(r"\s+", " ", text).strip()


def classify(item: dict[str, Any]) -> tuple[str, str, list[str]]:
    """Assign a conservative category, relevance level, and searchable tags."""

    haystack = " ".join(
        str(item.get(key) or "") for key in ("title", "content_text", "description", "external_id")
    ).lower()
    tags = {str(tag).strip().lower() for tag in item.get("tags", []) if str(tag).strip()}
    if any(word in haystack for word in ("marketplace", "plugin store", "package index", "awesome", "directory", "hub")):
        category = "index-and-marketplace"
    elif any(word in haystack for word in ("desktop", "web ui", "sidebar", "skin", "theme", "tui")):
        category = "ui-and-desktop"
    elif any(word in haystack for word in ("vision", "image", "ocr", "video", "eyes")):
        category = "multimedia-and-vision"
    elif any(word in haystack for word in ("agent team", "multi-agent", "orchestration", "subagent")):
        category = "agents-and-orchestration"
    elif any(word in haystack for word in ("tutorial", "guide", "quickstart", "paper", "architecture", "book")):
        category = "docs-and-learning"
    elif any(word in haystack for word in ("sandbox", "security", "permission", "billing", "balance", "token")):
        category = "operations-and-safety"
    else:
        category = "core-and-ecosystem"
    exact_terms = ("deepseek harness", "dsh-plugin", "deepseek-harness", "deepseek-harness-plugin")
    relevance = "direct" if any(term in haystack for term in exact_terms) else "related"
    tags.update({"deepseek", "deepseek-harness"})
    if "plugin" in haystack or "dsh-plugin" in haystack:
        tags.add("dsh-plugin")
    return category, relevance, sorted(tags)


def source_id(connection: sqlite3.Connection, platform: str) -> int:
    """Get or create the source row for a platform."""

    source = SOURCE_DEFAULTS.get(platform, {
        "display_name": platform,
        "base_url": "",
        "collection_mode": "imported raw snapshot",
        "terms_url": "",
    })
    connection.execute(
        """
        INSERT INTO sources(platform, display_name, base_url, collection_mode, terms_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(platform) DO UPDATE SET
            display_name=excluded.display_name,
            base_url=excluded.base_url,
            collection_mode=excluded.collection_mode,
            terms_url=excluded.terms_url
        """,
        (platform, source["display_name"], source["base_url"], source["collection_mode"], source["terms_url"], utc_now()),
    )
    return int(connection.execute("SELECT id FROM sources WHERE platform = ?", (platform,)).fetchone()[0])


def insert_observation(
    connection: sqlite3.Connection,
    observation: dict[str, Any],
    collection_run_id: int,
    raw_path: str | None,
    raw_sha256: str | None,
) -> tuple[int, bool]:
    """Insert one auditable observation and report whether it was new."""

    platform = str(observation.get("platform") or observation.get("source") or "unknown")
    sid = source_id(connection, platform)
    query = str(observation.get("query") or "")
    source_url = str(observation.get("source_url") or "")
    collected_at = str(observation.get("collected_at") or utc_now())
    existing = connection.execute(
        """
        SELECT id FROM observations
        WHERE source_id = ? AND query = ? AND source_url = ? AND collected_at = ?
        """,
        (sid, query, source_url, collected_at),
    ).fetchone()
    if existing is not None:
        return int(existing[0]), False
    connection.execute(
        """
        INSERT OR IGNORE INTO observations(
            source_id, collection_run_id, raw_snapshot_id, query, source_url, collected_at,
            collector, method, status, result_count, notes, raw_path, raw_sha256
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            sid,
            collection_run_id,
            None,
            query,
            source_url,
            collected_at,
            str(observation.get("collector") or "unknown"),
            str(observation.get("method") or "imported raw snapshot"),
            str(observation.get("status") or "ok"),
            observation.get("result_count"),
            str(observation.get("notes") or ""),
            raw_path,
            raw_sha256,
        ),
    )
    row = connection.execute(
        """
        SELECT id FROM observations
        WHERE source_id = ? AND query = ? AND source_url = ? AND collected_at = ?
        """,
        (sid, query, source_url, collected_at),
    ).fetchone()
    if row is None:
        raise RuntimeError("observation insert did not return an id")
    return int(row[0]), True


def store_raw_snapshot(
    connection: sqlite3.Connection,
    raw_path: Path,
    collection_run_id: int,
    collected_at: str,
) -> tuple[int, str, bool]:
    """Store the exact raw UTF-8 JSON payload once and return its identity."""

    raw_bytes = raw_path.read_bytes()
    raw_sha256 = hashlib.sha256(raw_bytes).hexdigest()
    raw_name = str(raw_path.relative_to(ROOT)) if raw_path.is_relative_to(ROOT) else str(raw_path)
    existing = connection.execute("SELECT id FROM raw_snapshots WHERE raw_sha256 = ?", (raw_sha256,)).fetchone()
    if existing is not None:
        return int(existing[0]), raw_sha256, False
    payload_json = raw_bytes.decode("utf-8")
    cursor = connection.execute(
        """
        INSERT INTO raw_snapshots(
            collection_run_id, raw_sha256, raw_path, collected_at, byte_size, payload_json
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        (collection_run_id, raw_sha256, raw_name, collected_at, len(raw_bytes), payload_json),
    )
    return int(cursor.lastrowid), raw_sha256, True


def upsert_item(
    connection: sqlite3.Connection,
    item: dict[str, Any],
    observed_at: str,
    collection_run_id: int,
) -> tuple[int, bool, bool]:
    """Upsert one item and return its id plus item/metric insertion status."""

    platform = str(item.get("platform") or item.get("source") or "unknown")
    url = canonical_url(str(item.get("url") or item.get("canonical_url") or ""))
    external_id = str(item.get("external_id") or url)
    category, relevance, inferred_tags = classify(item)
    title = str(item.get("title") or "").strip() or None
    content_text = str(item.get("content_text") or item.get("description") or "").strip() or None
    existing_item = connection.execute("SELECT id FROM items WHERE canonical_url = ?", (url,)).fetchone()
    values = (
        platform,
        external_id,
        url,
        str(item.get("item_type") or "post"),
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
        observed_at,
        observed_at,
        collection_run_id,
        collection_run_id,
        json.dumps(item, ensure_ascii=False, sort_keys=True),
    )
    connection.execute(
        """
        INSERT INTO items(
            platform, external_id, canonical_url, item_type, title, author, author_url,
            published_at, published_label, content_text, language, category, relevance,
            media_kind, first_seen_at, last_seen_at, first_seen_run_id, last_seen_run_id, raw_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(canonical_url) DO UPDATE SET
            platform=excluded.platform,
            title=COALESCE(excluded.title, items.title),
            author=COALESCE(excluded.author, items.author),
            author_url=COALESCE(excluded.author_url, items.author_url),
            published_at=COALESCE(excluded.published_at, items.published_at),
            published_label=COALESCE(excluded.published_label, items.published_label),
            content_text=COALESCE(excluded.content_text, items.content_text),
            language=COALESCE(excluded.language, items.language),
            category=excluded.category,
            relevance=excluded.relevance,
            media_kind=CASE
                WHEN excluded.media_kind = 'video' OR items.media_kind = 'video' THEN 'video'
                ELSE excluded.media_kind
            END,
            last_seen_at=excluded.last_seen_at,
            last_seen_run_id=excluded.last_seen_run_id,
            raw_json=excluded.raw_json
        """,
        values,
    )
    row = connection.execute("SELECT id FROM items WHERE canonical_url = ?", (url,)).fetchone()
    if row is None:
        raise RuntimeError(f"item insert did not return an id: {url}")
    item_id = int(row[0])
    is_new_item = existing_item is None

    metrics = item.get("metrics") or {}
    metric_values = {key: metric_int(metrics.get(key)) for key in (
        "likes", "replies", "reposts", "comments", "bookmarks", "views", "points", "stars", "forks", "open_issues", "subscribers", "favorites", "shares", "coins", "danmaku"
    )}
    metric_values["upvote_ratio"] = metric_float(metrics.get("upvote_ratio"))
    metric_is_new = False
    if any(value is not None for value in metric_values.values()):
        metric_observed_at = str(metrics.get("observed_at") or observed_at)
        metric_source = str(metrics.get("metric_source") or platform)
        existing_metric = connection.execute(
            "SELECT id FROM metrics WHERE item_id = ? AND observed_at = ? AND metric_source = ?",
            (item_id, metric_observed_at, metric_source),
        ).fetchone()
        metric_is_new = existing_metric is None
        connection.execute(
            """
            INSERT INTO metrics(
                item_id, collection_run_id, observed_at, likes, replies, reposts, comments, bookmarks, views,
                points, stars, forks, open_issues, subscribers, favorites, shares, coins, danmaku,
                upvote_ratio, metric_source, raw_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(item_id, observed_at, metric_source) DO UPDATE SET
                collection_run_id=COALESCE(metrics.collection_run_id, excluded.collection_run_id),
                likes=excluded.likes,
                replies=excluded.replies,
                reposts=excluded.reposts,
                comments=excluded.comments,
                bookmarks=excluded.bookmarks,
                views=excluded.views,
                points=excluded.points,
                stars=excluded.stars,
                forks=excluded.forks,
                open_issues=excluded.open_issues,
                subscribers=excluded.subscribers,
                favorites=excluded.favorites,
                shares=excluded.shares,
                coins=excluded.coins,
                danmaku=excluded.danmaku,
                upvote_ratio=excluded.upvote_ratio,
                raw_json=excluded.raw_json
            """,
            (
                item_id,
                collection_run_id,
                metric_observed_at,
                metric_values["likes"], metric_values["replies"], metric_values["reposts"],
                metric_values["comments"], metric_values["bookmarks"], metric_values["views"],
                metric_values["points"], metric_values["stars"], metric_values["forks"],
                metric_values["open_issues"], metric_values["subscribers"],
                metric_values["favorites"], metric_values["shares"], metric_values["coins"], metric_values["danmaku"], metric_values["upvote_ratio"],
                metric_source,
                json.dumps(metrics, ensure_ascii=False, sort_keys=True),
            ),
        )

    media = item.get("media") or []
    if item.get("media_url"):
        media = [*media, {"kind": item.get("media_kind", "link"), "url": item["media_url"], "thumbnail_url": item.get("thumbnail_url")}]
    for asset in media:
        if not asset.get("url"):
            continue
        connection.execute(
            """
            INSERT OR IGNORE INTO media_assets(item_id, kind, url, thumbnail_url, alt_text, rights_note)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                item_id,
                str(asset.get("kind") or item.get("media_kind") or "link"),
                str(asset["url"]),
                asset.get("thumbnail_url"),
                asset.get("alt_text"),
                asset.get("rights_note") or "External URL; do not mirror without permission.",
            ),
        )
    for tag in sorted(set(inferred_tags + [str(tag) for tag in item.get("tags", [])])):
        if not tag:
            continue
        connection.execute("INSERT OR IGNORE INTO tags(name) VALUES (?)", (tag,))
        tag_id = int(connection.execute("SELECT id FROM tags WHERE name = ?", (tag,)).fetchone()[0])
        connection.execute("INSERT OR IGNORE INTO item_tags(item_id, tag_id) VALUES (?, ?)", (item_id, tag_id))
    return item_id, is_new_item, metric_is_new


def import_payload(
    connection: sqlite3.Connection,
    payload: dict[str, Any],
    collection_run_id: int,
    raw_path: Path | None = None,
) -> ImportStats:
    """Import a raw snapshot while preserving its exact payload and audit links."""

    stats = ImportStats()
    if raw_path:
        collected_at = str(payload.get("collected_at") or utc_now())
        raw_snapshot_id, raw_hash, _ = store_raw_snapshot(connection, raw_path, collection_run_id, collected_at)
        raw_name = str(raw_path.relative_to(ROOT)) if raw_path.is_relative_to(ROOT) else str(raw_path)
    else:
        raw_snapshot_id = None
        raw_hash = None
        raw_name = None
    for observation in payload.get("observations", []):
        stats.observations_seen += 1
        observation_id, _ = insert_observation(connection, observation, collection_run_id, raw_name, raw_hash)
        if raw_snapshot_id is not None:
            connection.execute("UPDATE observations SET raw_snapshot_id = ? WHERE id = ?", (raw_snapshot_id, observation_id))
        observed_at = str(observation.get("collected_at") or payload.get("collected_at") or utc_now())
        for item in observation.get("items", []):
            item_id, is_new_item, metric_is_new = upsert_item(connection, item, observed_at, collection_run_id)
            if is_new_item:
                stats.new_items += 1
            else:
                stats.existing_items += 1
            if metric_is_new:
                stats.new_metrics += 1
            elif item.get("metrics"):
                stats.duplicate_metrics += 1
            connection.execute(
                "INSERT OR IGNORE INTO item_observations(item_id, observation_id) VALUES (?, ?)",
                (item_id, observation_id),
            )
            stats.item_observations += 1
    return stats


def fetch_json(url: str) -> dict[str, Any]:
    """Fetch one public JSON endpoint with a descriptive user agent."""

    request = Request(url, headers={
        "Accept": "application/vnd.github+json, application/json",
        "User-Agent": "awesome-deepseek-harness-plugin/0.1 public-research",
    })
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def github_item(hit: dict[str, Any], observed_at: str) -> dict[str, Any]:
    """Map a GitHub repository search result to the normalized item format."""

    return {
        "platform": "github",
        "external_id": hit.get("full_name"),
        "url": hit.get("html_url"),
        "item_type": "repository",
        "title": hit.get("full_name"),
        "author": hit.get("owner", {}).get("login"),
        "author_url": hit.get("owner", {}).get("html_url"),
        "published_at": hit.get("created_at"),
        "content_text": hit.get("description"),
        "language": hit.get("language"),
        "tags": hit.get("topics") or [],
        "media": ([{"kind": "avatar", "url": hit.get("owner", {}).get("avatar_url")}] if hit.get("owner", {}).get("avatar_url") else []),
        "metrics": {
            "stars": hit.get("stargazers_count"),
            "forks": hit.get("forks_count"),
            "open_issues": hit.get("open_issues_count"),
            "metric_source": "github REST API",
            "observed_at": observed_at,
        },
    }


def hn_item(hit: dict[str, Any], observed_at: str) -> dict[str, Any]:
    """Map a Hacker News Algolia hit to the normalized item format."""

    object_id = str(hit.get("objectID"))
    target_url = hit.get("url") or hit.get("story_url")
    title = hit.get("title") or ""
    media_kind = "video" if "[video]" in title.lower() or "youtube.com" in str(target_url) else "none"
    item: dict[str, Any] = {
        "platform": "hacker_news",
        "external_id": object_id,
        "url": f"https://news.ycombinator.com/item?id={object_id}",
        "item_type": "story",
        "title": title,
        "author": hit.get("author"),
        "published_at": hit.get("created_at"),
        "content_text": strip_html(hit.get("story_text")),
        "media_kind": media_kind,
        "media_url": target_url if target_url else None,
        "tags": ["hacker-news"],
        "metrics": {
            "points": hit.get("points"),
            "comments": hit.get("num_comments"),
            "metric_source": "HN Algolia API",
            "observed_at": observed_at,
        },
    }
    return item


def file_timestamp(path: Path) -> str:
    """Use a file modification time when a legacy snapshot has no timestamp."""

    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def unix_timestamp(value: Any) -> str | None:
    """Convert a Unix timestamp from a public API response to UTC ISO-8601."""

    if value in (None, ""):
        return None
    try:
        return datetime.fromtimestamp(float(value), timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    except (TypeError, ValueError, OverflowError):
        return None


def x_metrics(value: str | None, observed_at: str) -> dict[str, Any]:
    """Parse X's visible interaction summary, including unlabeled status-page counts."""

    text = value or ""
    metrics: dict[str, Any] = {"metric_source": "X visible aria-label", "observed_at": observed_at}
    for key, pattern in {
        "replies": r"([\d,.]+\s*[KkMm万亿]?)\s+repl(?:y|ies)",
        "reposts": r"([\d,.]+\s*[KkMm万亿]?)\s+repost(?:s)?",
        "likes": r"([\d,.]+\s*[KkMm万亿]?)\s+like(?:s)?",
        "bookmarks": r"([\d,.]+\s*[KkMm万亿]?)\s+bookmark(?:s)?",
        "views": r"([\d,.]+\s*[KkMm万亿]?)\s+views?",
    }.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            metrics[key] = metric_int(match.group(1))
    if "views" not in metrics:
        view_match = re.search(r"([\d,.]+\s*[KkMm万亿]?)\s*\n?\s*views?", text, flags=re.IGNORECASE)
        if view_match:
            metrics["views"] = metric_int(view_match.group(1))
            values = re.findall(r"[\d,.]+\s*[KkMm万亿]?", text)
            tail = values[-5:]
            if len(tail) >= 2:
                for key, raw in zip(("replies", "reposts", "likes", "bookmarks"), tail[1:]):
                    metrics.setdefault(key, metric_int(raw))
            metrics["metric_source"] = "X visible DOM order; labels absent"
    return metrics


def x_item(tweet: dict[str, Any], observed_at: str, query: str, fallback_url: str | None = None) -> dict[str, Any]:
    """Normalize a legacy X search/status capture."""

    url = str(tweet.get("link") or tweet.get("pageUrl") or fallback_url or "")
    text = str(tweet.get("text") or tweet.get("bodyText") or "").strip()
    user = str(tweet.get("user") or tweet.get("author") or "").strip()
    author = user.split("@", 1)[0].strip(" ·") if user else None
    handle = user.split("@", 1)[1].split()[0] if "@" in user else None
    links = [str(link) for link in tweet.get("links", []) if link]
    media_links = [link for link in links if "/photo/" in link or "/video/" in link]
    media_kind = "image" if any("/photo/" in link for link in media_links) else ("video" if media_links else "link")
    title = re.sub(r"\s+", " ", text.replace("|", " ")).strip()[:140] or f"X post {url.rsplit('/', 1)[-1]}"
    external_id = url.rstrip("/").rsplit("/", 1)[-1].split("?", 1)[0] or title
    time_value = tweet.get("time")
    published_at = time_value.get("datetime") if isinstance(time_value, dict) else time_value
    published_label = time_value.get("text") if isinstance(time_value, dict) else (time_value if isinstance(time_value, str) and len(time_value) < 20 else None)
    return {
        "platform": "x",
        "external_id": external_id,
        "url": url,
        "item_type": "post",
        "title": title,
        "author": author,
        "author_url": f"https://x.com/{handle}" if handle else None,
        "published_at": published_at,
        "published_label": published_label,
        "content_text": text,
        "media_kind": media_kind,
        "media": [{"kind": "image" if "/photo/" in link else "video", "url": link} for link in media_links],
        "metrics": x_metrics(tweet.get("aria") or tweet.get("bodyText"), observed_at),
        "tags": ["x", query],
    }


def legacy_payload(path: Path, data: Any) -> dict[str, Any] | None:
    """Convert older platform-specific raw files into the normalized import format."""

    if isinstance(data, dict) and isinstance(data.get("observations"), list):
        return data
    if not isinstance(data, dict):
        return None
    observed_at = str(data.get("harvestedAt") or data.get("collected_at") or file_timestamp(path))
    relative = str(path.relative_to(ROOT))
    stem = path.stem

    def observation(
        platform: str,
        query: str,
        source_url: str,
        items: list[dict[str, Any]],
        count: int | None = None,
        notes: str = "legacy raw snapshot",
        status: str = "ok",
    ) -> dict[str, Any]:
        return {"collected_at": observed_at, "collector": "legacy raw adapter", "observations": [{
            "platform": platform,
            "query": query,
            "source_url": source_url,
            "collected_at": observed_at,
            "collector": "legacy raw adapter",
            "method": "imported platform snapshot",
            "status": status,
            "result_count": count if count is not None else len(items),
            "notes": f"{notes}; raw path: {relative}",
            "items": items,
        }]}

    if "tweets" in data:
        query = str(data.get("query") or stem)
        tweets = [x_item(tweet, observed_at, query) for tweet in data.get("tweets", []) if isinstance(tweet, dict)]
        return observation("x", query, f"https://x.com/search?q={query.replace(' ', '+')}", tweets, len(tweets), "X search/profile capture")
    if "bodyText" in data and ("pageUrl" in data or "aria" in data):
        item = x_item(data, observed_at, stem, str(data.get("pageUrl") or ""))
        return observation("x", stem, str(data.get("pageUrl") or item["url"]), [item], 1, "X status capture")
    if data.get("url") and "youtube.com" in str(data["url"]).lower() and data.get("title"):
        video_url = str(data["url"])
        video_id = parse_qs(urlsplit(video_url).query).get("v", [video_url])[0]
        item = {
            "platform": "youtube",
            "external_id": video_id,
            "url": video_url,
            "item_type": "video",
            "title": data.get("title"),
            "content_text": data.get("snippet"),
            "media_kind": "video",
            "media_url": video_url,
            "tags": ["youtube", "video", "curated"],
        }
        return observation("youtube", str(data["title"]), video_url, [item], 1, "Curated public video metadata")
    if "cards" in data:
        items: list[dict[str, Any]] = []
        seen: set[str] = set()
        for card in data.get("cards", []):
            if not isinstance(card, dict) or not card.get("href"):
                continue
            url = str(card["href"])
            external_id = url.rstrip("/").rsplit("/", 1)[-1]
            if external_id in seen or not card.get("text"):
                continue
            seen.add(external_id)
            parts = [part.strip() for part in str(card.get("text") or "").split("|") if part.strip()]
            likes = None
            if parts and re.fullmatch(r"[\d,.]+\s*[KkMm万亿]?", parts[-1]):
                likes = metric_int(parts.pop())
            time_index = next(
                (
                    index
                    for index in range(len(parts) - 1, -1, -1)
                    if re.fullmatch(
                        r"(?:刚刚|昨天(?:\s+\d{1,2}:\d{2})?|前天(?:\s+\d{1,2}:\d{2})?|"
                        r"\d+\s*(?:秒|分钟|小时|天|周|月|年)前|\d{1,2}月\d{1,2}日(?:\s+\d{1,2}:\d{2})?)",
                        parts[index],
                    )
                ),
                None,
            )
            before_time = parts[:time_index] if time_index is not None else parts
            published_label = parts[time_index] if time_index is not None else None
            title = None
            author = None
            if len(before_time) >= 3 and before_time[0] in {"文件", "视频", "图文", "笔记", "直播"}:
                title, author = before_time[1], before_time[2]
            elif len(before_time) >= 2:
                title, author = before_time[-2], before_time[-1]
            elif len(before_time) == 1:
                author = before_time[0] if time_index is not None else None
                title = before_time[0] if time_index is None else None
            items.append({
                "platform": "xiaohongshu", "external_id": external_id, "url": url, "item_type": "note",
                "title": title, "author": author,
                "published_label": published_label, "content_text": str(card.get("text") or ""),
                "media_kind": "none", "metrics": {"likes": likes, "metric_source": "XHS visible card", "observed_at": observed_at},
                "tags": ["xiaohongshu", "search-card"],
            })
        return observation("xiaohongshu", stem, str(data.get("pageUrl") or "https://www.xiaohongshu.com"), items, data.get("cardCount", len(items)), "XHS search-card capture; card title was not exposed in this raw file")
    if data.get("type") == "story" and data.get("id") is not None:
        hit = dict(data)
        hit["objectID"] = str(data["id"])
        hit["story_text"] = data.get("text")
        item = hn_item(hit, observed_at)
        return observation("hacker_news", str(data.get("title") or data["id"]), item["url"], [item], 1, "HN item snapshot")
    if "hits" in data and "nbHits" in data:
        query = str(data.get("query") or stem)
        items = [hn_item(hit, observed_at) for hit in data.get("hits", []) if isinstance(hit, dict)]
        return observation("hacker_news", query, f"https://hn.algolia.com/?q={query.replace(' ', '%20')}", items, data.get("nbHits"), "HN Algolia snapshot")
    if "total_count" in data and isinstance(data.get("items"), list):
        query = stem.replace("-", " ")
        items = [github_item(hit, observed_at) for hit in data.get("items", []) if isinstance(hit, dict)]
        return observation("github", query, f"https://api.github.com/search/repositories?{urlencode({'q': query})}", items, data.get("total_count"), "GitHub REST search snapshot")
    if "full_name" in data and "html_url" in data:
        return observation("github", "official repository", str(data["html_url"]), [github_item(data, observed_at)], 1, "GitHub repository snapshot")
    if "score" in data and "permalink" in data:
        permalink = str(data["permalink"])
        url = permalink if permalink.startswith("http") else f"https://www.reddit.com{permalink}"
        item = {
            "platform": "reddit", "external_id": permalink.rstrip("/").rsplit("/", 1)[-1], "url": url,
            "item_type": "post", "title": data.get("title"), "author": data.get("author"),
            "published_at": data.get("created"), "content_text": data.get("selftext"), "media_kind": "none",
            "metrics": {"likes": metric_int(data.get("score")), "comments": metric_int(data.get("commentCount")), "upvote_ratio": metric_float(data.get("upvoteRatio")), "metric_source": "Reddit visible DOM", "observed_at": observed_at},
            "tags": ["reddit", str(data.get("flair") or "").strip()],
        }
        return observation("reddit", str(data.get("title") or stem), url, [item], 1, "Reddit post capture")
    if "answerCount" in data and "answers" in data:
        qid = str(data.get("pageUrl", "").rstrip("/").rsplit("/", 1)[-1] or stem)
        body = str(data.get("bodySample") or "")
        metrics: dict[str, Any] = {
            "metric_source": "Zhihu visible page",
            "observed_at": observed_at,
        }
        for key, pattern, fallback in (
            ("views", r"被浏览\s*([\d,]+)", None),
            ("followers", r"关注者\s*([\d,]+)", data.get("followers")),
            ("likes", r"好问题\s*([\d,]+)", None),
            ("comments", r"([\d,]+)\s*条评论", None),
            ("replies", r"([\d,]+)\s*个回答", data.get("answerCount")),
        ):
            match = re.search(pattern, body)
            metrics[key] = metric_int(match.group(1)) if match else metric_int(fallback)
        item = {
            "platform": "zhihu", "external_id": qid, "url": data.get("pageUrl"), "item_type": "question",
            "title": data.get("h1") or data.get("title"), "content_text": data.get("bodySample"), "media_kind": "none",
            "metrics": metrics,
            "tags": ["zhihu", "question"],
        }
        return observation("zhihu", str(data.get("h1") or data.get("title") or stem), str(data.get("pageUrl") or "https://www.zhihu.com"), [item], 1, "Zhihu question capture; answer excerpts remain in raw JSON")
    if isinstance(data.get("data"), dict) and data["data"].get("bvid"):
        video = data["data"]
        stats = video.get("stat") or {}
        bvid = str(video["bvid"])
        item = {
            "platform": "bilibili", "external_id": bvid, "url": f"https://www.bilibili.com/video/{bvid}", "item_type": "video",
            "title": video.get("title"), "author": (video.get("owner") or {}).get("name"), "content_text": video.get("desc"),
            "published_at": unix_timestamp(video.get("pubdate") or video.get("ctime")),
            "media_kind": "video", "media_url": f"https://www.bilibili.com/video/{bvid}", "thumbnail_url": video.get("pic"),
            "media": ([{"kind": "avatar", "url": video.get("owner", {}).get("face")}] if video.get("owner", {}).get("face") else []),
            "metrics": {"views": stats.get("view"), "replies": stats.get("reply"), "likes": stats.get("like"), "favorites": stats.get("favorite"), "shares": stats.get("share"), "coins": stats.get("coin"), "danmaku": stats.get("danmaku"), "metric_source": "Bilibili public metadata API", "observed_at": observed_at},
            "tags": ["bilibili", "video"],
        }
        return observation("bilibili", str(video.get("title") or bvid), item["url"], [item], 1, "Bilibili video metadata capture")
    if "pageUrl" in data and any(key in data for key in ("ogTitle", "ogDesc", "ogImage", "h1")):
        url = str(data["pageUrl"])
        host = urlsplit(url).netloc.lower()
        platform = (
            "linuxdo" if host.endswith("linux.do") else
            "v2ex" if host.endswith("v2ex.com") else
            "weibo" if host.endswith("weibo.com") else
            "wechat" if host.endswith("mp.weixin.qq.com") else
            "official" if host.endswith("deepseek.com") else
            "youtube" if host.endswith("youtube.com") else
            "bilibili" if host.endswith("bilibili.com") else
            "zhihu" if host.endswith("zhihu.com") else
            "web"
        )
        og_image = str(data.get("ogImage") or "")
        if og_image.startswith("//"):
            og_image = f"https:{og_image}"
        media = []
        if og_image:
            media.append({"kind": "image", "url": og_image, "thumbnail_url": og_image})
        if data.get("ogImageSaved"):
            media.append({"kind": "image-local", "url": str(data["ogImageSaved"]), "rights_note": "Local capture from the dated raw snapshot."})
        title = strip_html(str(data.get("ogTitle") or data.get("title") or data.get("h1") or ""))
        if platform == "bilibili" and title:
            title = re.sub(r"_哔哩哔哩_bilibili$", "", title).strip()
        blocked_text = " ".join(str(data.get(key) or "") for key in ("title", "h1", "sample")).lower()
        blocked = not data.get("ogTitle") and any(marker in blocked_text for marker in ("security verification", "正在验证连接安全", "protected by/tencent cloud", "protected by tencent cloud"))
        item = {
            "platform": platform, "external_id": canonical_url(url), "url": url, "item_type": "article",
            "title": None if blocked else title, "content_text": data.get("ogDesc") or data.get("sample"),
            "media_kind": "image" if media else "none", "media": media,
            "published_at": data.get("published"), "tags": [platform, stem],
        }
        notes = "Open-web metadata capture"
        if blocked:
            notes += "; page exposed a verification/interstitial response; no title asserted."
        return observation(platform, str(item.get("title") or stem), url, [item], 1, notes, "blocked" if blocked else "ok")
    return None


def collect_api_payload(config: dict[str, Any]) -> dict[str, Any]:
    """Fetch GitHub and HN public APIs and return a raw, normalized payload."""

    collected_at = utc_now()
    observations: list[dict[str, Any]] = []
    limits = config.get("limits", {})
    for query in config.get("github", []):
        url = f"https://api.github.com/search/repositories?{urlencode({'q': query, 'per_page': limits.get('github_per_query', 50), 'sort': 'stars', 'order': 'desc'})}"
        try:
            response = fetch_json(url)
            items = [github_item(hit, collected_at) for hit in response.get("items", [])]
            observations.append({
                "platform": "github",
                "query": query,
                "source_url": url,
                "collected_at": collected_at,
                "collector": "scripts/collect.py",
                "method": "public REST API",
                "status": "ok",
                "result_count": response.get("total_count"),
                "notes": "Search results are candidates; topic matches can contain unrelated repositories.",
                "items": items,
                "raw_response": response,
            })
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            observations.append({
                "platform": "github", "query": query, "source_url": url, "collected_at": collected_at,
                "collector": "scripts/collect.py", "method": "public REST API", "status": "error",
                "result_count": 0, "notes": str(error), "items": [], "raw_response": None,
            })
    for query in config.get("hacker_news", []):
        url = f"https://hn.algolia.com/api/v1/search?{urlencode({'query': query, 'tags': 'story', 'hitsPerPage': limits.get('hacker_news_per_query', 50)})}"
        try:
            response = fetch_json(url)
            items = [hn_item(hit, collected_at) for hit in response.get("hits", [])]
            observations.append({
                "platform": "hacker_news",
                "query": query,
                "source_url": url,
                "collected_at": collected_at,
                "collector": "scripts/collect.py",
                "method": "Algolia public search API",
                "status": "ok",
                "result_count": response.get("nbHits"),
                "notes": "HN point/comment counts are snapshots and may change after collection.",
                "items": items,
                "raw_response": response,
            })
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            observations.append({
                "platform": "hacker_news", "query": query, "source_url": url, "collected_at": collected_at,
                "collector": "scripts/collect.py", "method": "Algolia public search API", "status": "error",
                "result_count": 0, "notes": str(error), "items": [], "raw_response": None,
            })
    return {"collected_at": collected_at, "collector": "scripts/collect.py", "observations": observations}


def import_files(connection: sqlite3.Connection, paths: list[Path], collection_run_id: int) -> ImportStats:
    """Import raw files once while retaining exact payloads and normalized links."""

    total = ImportStats()
    resolved_paths = [path if path.is_absolute() else (ROOT / path).resolve() for path in paths]
    for path in sorted(resolved_paths):
        total.raw_files_seen += 1
        raw_hash = sha256_file(path)
        if connection.execute("SELECT 1 FROM raw_snapshots WHERE raw_sha256 = ?", (raw_hash,)).fetchone():
            total.raw_files_skipped += 1
            continue
        data = load_json(path)
        collected_at = str(
            data.get("collected_at") or data.get("harvestedAt") or file_timestamp(path)
        ) if isinstance(data, dict) else file_timestamp(path)
        store_raw_snapshot(connection, path, collection_run_id, collected_at)
        payload = legacy_payload(path, data)
        if payload is not None:
            total.add(import_payload(connection, payload, collection_run_id, path))
    return total


def command_seed(args: argparse.Namespace) -> None:
    """Initialize and import all checked-in raw snapshots."""

    init_db(args.db)
    if args.raw:
        paths = [path for path in args.raw if path.exists()]
    else:
        paths = [path for path in sorted(RAW_DIR.rglob("*.json")) if "auto" not in path.parts]
    with connect(args.db) as connection:
        run_id, version, _ = begin_collection_run(connection, "seed")
        stats = ImportStats()
        try:
            stats = import_files(connection, paths, run_id)
            finish_collection_run(connection, run_id, stats)
        except Exception as error:
            finish_collection_run(connection, run_id, stats, "failed", str(error))
            connection.commit()
            raise
    print(
        f"seeded {stats.item_observations} item observations in {version}; "
        f"{stats.raw_files_skipped}/{stats.raw_files_seen} duplicate raw file(s) skipped into {args.db}"
    )


def command_update(args: argparse.Namespace) -> None:
    """Fetch API sources, persist raw snapshots, then import manual browser snapshots."""

    init_db(args.db)
    output = args.raw_output or (RAW_DIR / "auto" / f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json")
    if not output.is_absolute():
        output = ROOT / output
    with connect(args.db) as connection:
        run_id, version, _ = begin_collection_run(connection, args.trigger)
        stats = ImportStats()
        try:
            payload = collect_api_payload(load_json(CONFIG_PATH))
            dump_json(output, payload)
            paths = [output, *args.raw]
            stats = import_files(connection, [path for path in paths if path.exists()], run_id)
            finish_collection_run(connection, run_id, stats)
        except Exception as error:
            finish_collection_run(connection, run_id, stats, "failed", str(error))
            connection.commit()
            raise
    try:
        output_label = output.relative_to(ROOT)
    except ValueError:
        output_label = output
    print(
        f"updated {stats.item_observations} item observations in {version}; "
        f"{stats.raw_files_skipped}/{stats.raw_files_seen} duplicate raw file(s) skipped; "
        f"API raw snapshot: {output_label}"
    )


def command_init(args: argparse.Namespace) -> None:
    """Create an empty database."""

    init_db(args.db)
    print(f"initialized {args.db}")


def main() -> int:
    """Run the collection CLI."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DB_PATH, help="SQLite database path")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("init", help="create the SQLite schema")
    seed = subparsers.add_parser("seed", help="import checked-in or explicit raw JSON")
    seed.add_argument("--raw", type=Path, action="append", default=[], help="raw JSON file; repeatable")
    update = subparsers.add_parser("update", help="fetch public APIs and optionally import browser raw JSON")
    update.add_argument("--raw", type=Path, action="append", default=[], help="ego-browser raw JSON file; repeatable")
    update.add_argument("--raw-output", type=Path, help="where to persist the API snapshot; defaults to data/raw/auto/")
    update.add_argument("--trigger", choices=("manual", "scheduled"), default="manual", help="why this collection run started")
    args = parser.parse_args()
    if args.command == "init":
        command_init(args)
    elif args.command == "seed":
        command_seed(args)
    elif args.command == "update":
        command_update(args)
    else:
        parser.error("unknown command")
    return 0


if __name__ == "__main__":
    sys.exit(main())
