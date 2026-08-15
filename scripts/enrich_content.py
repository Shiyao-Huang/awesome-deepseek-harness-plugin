#!/usr/bin/env python3
"""Fetch and store the detailed content behind each item URL.

Stages, all idempotent against the item_details table:
- github: README text for the top repositories by stars (gh CLI token)
- hacker_news: full comment trees for stories with traction (Algolia item API)
- web/official: article body text (best-effort tag-stripped extraction)
- reddit: post body plus top comments from the checked-in DOM captures
- x: full post text from the checked-in status/search/profile captures
- zhihu: full answer texts from the ego-browser full-text capture
- xiaohongshu: stores trusted-click detail text and records blocked attempts as provenance
Stdlib only; run after `collect.py seed`.
"""

from __future__ import annotations

import base64
import datetime as dt
import html
import json
import re
import sqlite3
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
RAW_DIR = ROOT / "data" / "raw"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/131.0 Safari/537.36"}
GITHUB_TOP = 150
GITHUB_MAX_CHARS = 16000
ARTICLE_MAX_CHARS = 12000
HN_MAX_CHARS = 16000
REDDIT_MAX_CHARS = 8000


def utc_now() -> str:
    """ISO-8601 UTC timestamp with second precision."""

    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def connect() -> sqlite3.Connection:
    """Open the aggregator database with foreign keys enforced."""

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def ensure_tables(connection: sqlite3.Connection) -> None:
    """Create the detail table and indices when absent."""

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS item_details (
            item_id INTEGER PRIMARY KEY REFERENCES items(id) ON DELETE CASCADE,
            method TEXT NOT NULL,
            fetched_at TEXT NOT NULL,
            url TEXT,
            content TEXT NOT NULL,
            char_count INTEGER NOT NULL,
            language TEXT,
            status TEXT NOT NULL DEFAULT 'ok',
            notes TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_details_status ON item_details(status);
        """
    )
    connection.commit()


def detect_language(text: str) -> str:
    """Coarse zh/en classifier over the first 2,000 characters."""

    sample = text[:2000]
    if not sample.strip():
        return "en"
    cjk = len(re.findall(r"[\u4e00-\u9fff]", sample))
    return "zh" if cjk > max(2, len(sample) * 0.15) else "en"


def store_detail(connection: sqlite3.Connection, item_id: int, method: str, url: str | None,
                 content: str, status: str = "ok", notes: str | None = None) -> bool:
    """Insert or refresh one detail row; returns True when content landed."""

    content = (content or "").strip()
    connection.execute(
        """
        INSERT INTO item_details(item_id, method, fetched_at, url, content, char_count, language, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(item_id) DO UPDATE SET
            method=excluded.method, fetched_at=excluded.fetched_at, url=excluded.url,
            content=excluded.content, char_count=excluded.char_count,
            language=excluded.language, status=excluded.status, notes=excluded.notes
        """,
        (item_id, method, utc_now(), url, content, len(content),
         detect_language(content) if content else None, status, notes),
    )
    return bool(content)


def done_item_ids(connection: sqlite3.Connection) -> set:
    """Item ids that already have a successful detail row (idempotent reruns)."""

    return {row[0] for row in connection.execute(
        "SELECT item_id FROM item_details WHERE status='ok' AND char_count>0"
    )}


def gh_token() -> str | None:
    """Read the GitHub CLI token when available for the 5,000/h rate limit."""

    try:
        result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=15)
        token = result.stdout.strip()
        return token or None
    except Exception:
        return None


def github_readmes(connection: sqlite3.Connection, token: str | None) -> dict[str, int]:
    """Store README text for the top-starred repositories."""

    rows = connection.execute(
        """
        SELECT i.id, i.external_id FROM items i
        JOIN v_latest_metrics m ON m.item_id = i.id
        WHERE i.platform = 'github' AND m.stars IS NOT NULL
        ORDER BY m.stars DESC LIMIT ?
        """,
        (GITHUB_TOP,),
    ).fetchall()
    stats = {"fetched": 0, "skipped": 0, "empty": 0, "failed": 0}
    failures = 0
    done = done_item_ids(connection)
    for row in rows:
        if row["id"] in done:
            stats["skipped"] += 1
            continue
        full_name = row["external_id"]
        url = f"https://api.github.com/repos/{full_name}/readme"
        headers = dict(Accept="application/vnd.github.raw+json", **UA)
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read().decode("utf-8", "replace")
            if not raw.strip() and failures_guard(stats):
                stats["empty"] += 1
                store_detail(connection, row["id"], "GitHub README API", url, "", "empty", "README endpoint returned empty content")
                continue
            stats["fetched"] += 1
            failures = 0
            store_detail(connection, row["id"], "GitHub README API", url, raw[:GITHUB_MAX_CHARS], "ok",
                         None if len(raw) <= GITHUB_MAX_CHARS else f"truncated from {len(raw):,} chars")
        except Exception as error:
            stats["failed"] += 1
            failures += 1
            store_detail(connection, row["id"], "GitHub README API", url, "", "failed", str(error)[:200])
            if failures >= 5:
                print(f"  github: aborting after 5 consecutive failures", file=sys.stderr)
                break
    connection.commit()
    return stats


def failures_guard(stats: dict[str, int]) -> bool:
    """Placeholder guard kept for symmetric failure accounting."""

    return True


def flatten_hn_children(children: Iterable[dict[str, Any]], depth: int = 0, lines: list[str] | None = None) -> list[str]:
    """Flatten an Algolia item tree into readable comment lines."""

    if lines is None:
        lines = []
    for child in children or []:
        author = child.get("author") or "anon"
        created = (child.get("created_at") or "")[:10]
        text = re.sub(r"<[^>]+>", " ", html.unescape(child.get("text") or ""))
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            lines.append(f"{'  ' * depth}- [{author} @ {created}] {text}")
        flatten_hn_children(child.get("children") or [], depth + 1, lines)
    return lines


def hackernews_threads(connection: sqlite3.Connection) -> dict[str, int]:
    """Store full HN comment trees for stories with visible traction."""

    rows = connection.execute(
        """
        SELECT i.id, i.external_id, i.title FROM items i
        JOIN v_latest_metrics m ON m.item_id = i.id
        WHERE i.platform = 'hacker_news' AND COALESCE(m.points, 0) >= 5
        ORDER BY m.points DESC
        """
    ).fetchall()
    stats = {"fetched": 0, "skipped": 0, "failed": 0}
    done = done_item_ids(connection)
    for row in rows:
        if row["id"] in done:
            stats["skipped"] += 1
            continue
        url = f"https://hn.algolia.com/api/v1/items/{row['external_id']}"
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as response:
                tree = json.loads(response.read().decode("utf-8"))
            lines = flatten_hn_children(tree.get("children") or [])
            content = f"{row['title']}\n\n" + "\n".join(lines)
            stats["fetched"] += 1
            store_detail(connection, row["id"], "HN Algolia item API", url, content[:HN_MAX_CHARS], "ok",
                         f"{len(lines)} comments" + ("; truncated" if len(content) > HN_MAX_CHARS else ""))
        except Exception as error:
            stats["failed"] += 1
            store_detail(connection, row["id"], "HN Algolia item API", url, "", "failed", str(error)[:200])
    connection.commit()
    return stats


def extract_article_text(page_html: str) -> str:
    """Best-effort main-text extraction from an HTML page."""

    page_html = re.sub(r"(?is)<(script|style|noscript|svg|iframe|nav|header|footer)[^>]*>.*?</\1>", " ", page_html)
    match = re.search(r"(?is)<(article|main)[^>]*>(.*?)</\1>", page_html)
    body = match.group(2) if match else page_html
    text = re.sub(r"(?is)<br\s*/?>|</p>|</div>|</li>|</h[1-6]>", "\n", body)
    text = re.sub(r"<[^>]+>", " ", html.unescape(text))
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.split("\n")]
    lines = [line for line in lines if len(line) > 1]
    return "\n".join(lines)


def web_articles(connection: sqlite3.Connection) -> dict[str, int]:
    """Store extracted article body text for web/official items."""

    stats = {"fetched": 0, "skipped": 0, "blocked": 0, "failed": 0}
    rows = connection.execute(
        "SELECT id, canonical_url FROM items WHERE platform IN ('web', 'official')"
    ).fetchall()
    done = done_item_ids(connection)
    for row in rows:
        if row["id"] in done:
            stats["skipped"] += 1
            continue
        url = row["canonical_url"]
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as response:
                page = response.read(400_000).decode("utf-8", "replace")
            content = extract_article_text(page)
            if len(content) < 200:
                stats["blocked"] += 1
                store_detail(connection, row["id"], "HTTP fetch + tag strip", url, content, "thin",
                             f"extracted only {len(content)} chars; page may be JS-rendered")
            else:
                stats["fetched"] += 1
                store_detail(connection, row["id"], "HTTP fetch + tag strip", url, content[:ARTICLE_MAX_CHARS], "ok",
                             None if len(content) <= ARTICLE_MAX_CHARS else f"truncated from {len(content):,} chars")
        except Exception as error:
            stats["failed"] += 1
            store_detail(connection, row["id"], "HTTP fetch + tag strip", url, "", "failed", str(error)[:200])
    connection.commit()
    return stats


def load_raw(relative: str) -> Any:
    """Load one checked-in raw JSON file."""

    return json.loads((RAW_DIR / relative).read_text(encoding="utf-8"))


def reddit_bodies(connection: sqlite3.Connection) -> dict[str, int]:
    """Store post body plus visible top comments from DOM captures."""

    stats = {"fetched": 0}
    for path in sorted((RAW_DIR / "web").glob("reddit-dom-*.json")):
        data = load_raw(f"web/{path.name}")
        permalink = str(data.get("permalink") or "")
        slug = permalink.rstrip("/").rsplit("/", 1)[-1]
        row = (connection.execute(
            "SELECT id FROM items WHERE platform='reddit' AND external_id=?", (slug,)
        ).fetchone() if slug else None)
        if row is None:
            continue
        parts = [f"{data.get('title') or ''}", "", data.get("selftext") or ""]
        comments = data.get("comments") or []
        if comments:
            parts.append("— comments —")
            for comment in comments:
                author = comment.get("author") or "anon"
                text = re.sub(r"\s+", " ", comment.get("text") or "").strip()
                if text:
                    parts.append(f"- [{author} · {comment.get('score') or '?'}] {text}")
        content = "\n".join(parts)
        stats["fetched"] += 1
        store_detail(connection, row["id"], "ego-browser DOM capture (checked-in raw)", data.get("permalink"),
                     content[:REDDIT_MAX_CHARS], "ok",
                         f"{len(comments)} visible comments" + ("; truncated" if len(content) > REDDIT_MAX_CHARS else ""))
    connection.commit()
    return stats


def x_bodies(connection: sqlite3.Connection) -> dict[str, int]:
    """Store full post text from the checked-in X captures."""

    texts: dict[str, tuple[str, str]] = {}
    for name in ("deepseek-ai-announce", "jiqizhixin", "jiayuan-jy-beta", "yicaichina-report"):
        data = load_raw(f"x/status-{name}.json")
        sid = str(data.get("pageUrl") or "").rstrip("/").split("/status/")[-1].split("?")[0]
        texts.setdefault(sid, (data.get("bodyText") or "", data.get("pageUrl")))
    for query in ("plugin", "general", "topic"):
        try:
            data = load_raw(f"x/search-{query}.json")
        except FileNotFoundError:
            continue
        for tweet in data.get("tweets", []):
            link = str(tweet.get("link") or "")
            if "/status/" in link:
                sid = link.rstrip("/").split("/status/")[-1].split("?")[0].split("#")[0]
                texts.setdefault(sid, (str(tweet.get("text") or ""), link))
    try:
        profile = load_raw("x/profile-tianyi.json")
        for tweet in profile.get("tweets", []):
            link = str(tweet.get("link") or "")
            if "/status/" in link:
                sid = link.rstrip("/").split("/status/")[-1].split("?")[0].split("#")[0]
                texts.setdefault(sid, (str(tweet.get("text") or ""), link))
    except FileNotFoundError:
        pass
    stats = {"fetched": 0}
    for sid, (text, url) in texts.items():
        row = connection.execute("SELECT id FROM items WHERE platform='x' AND external_id=?", (sid,)).fetchone()
        if row is None or not text.strip():
            continue
        stats["fetched"] += 1
        store_detail(connection, row["id"], "ego-browser DOM capture (checked-in raw)", url,
                     re.sub(r"\s*\n\s*", "\n", text))
    connection.commit()
    return stats


def bilibili_descriptions(connection: sqlite3.Connection) -> dict[str, int]:
    """Store video description plus a stat summary line for Bilibili items."""

    stats = {"fetched": 0}
    for path in sorted((RAW_DIR / "web").glob("bilibili-*.json")):
        data = load_raw(f"web/{path.name}")
        video = data.get("data") or {}
        bvid = video.get("bvid")
        if not bvid:
            continue
        row = connection.execute("SELECT id FROM items WHERE platform='bilibili' AND external_id=?", (bvid,)).fetchone()
        if row is None:
            continue
        stat = video.get("stat") or {}
        owner = video.get("owner") or {}
        summary = (
            f"UP: {owner.get('name') or '?'} | 播放 {stat.get('view'):,} | 点赞 {stat.get('like'):,} | "
            f"投币 {stat.get('coin'):,} | 收藏 {stat.get('favorite'):,} | 弹幕 {stat.get('danmaku'):,}"
            if stat.get("view") is not None else ""
        )
        content = "\n".join(part for part in (video.get("title"), summary, video.get("desc")) if part)
        stats["fetched"] += 1
        store_detail(connection, row["id"], "Bilibili public metadata API", video.get("pic") and f"https://www.bilibili.com/video/{bvid}", content)
    connection.commit()
    return stats


def zhihu_full_answers(connection: sqlite3.Connection) -> dict[str, int]:
    """Store full answer texts under the question item."""

    stats = {"fetched": 0}
    try:
        data = load_raw("zhihu/question-2071348486667237276-detail.json")
    except FileNotFoundError:
        return stats
    row = connection.execute(
        "SELECT id FROM items WHERE canonical_url LIKE '%zhihu.com/question/2071348486667237276%'"
    ).fetchone()
    if row is None:
        return stats
    parts = [f"问题浏览量：{data.get('views') or '?'}", ""]
    answers = [a for a in data.get("answers", []) if (a.get("content") or "").strip()]
    for answer in answers:
        vote = re.sub(r"\s+", " ", str(answer.get("voteText") or "赞同 ?")).replace("\n", " ")
        parts.append(f"## {answer.get('author') or '匿名'} — {vote}")
        parts.append(str(answer.get("time") or "").strip())
        parts.append(str(answer.get("content") or "").strip())
        parts.append("")
    stats["fetched"] = len(answers)
    store_detail(connection, row["id"], "ego-browser DOM full-text capture", data.get("pageUrl"),
                 "\n".join(parts)[:16000], "ok", f"{len(answers)} answers in full")
    connection.commit()
    return stats


def xiaohongshu_details(connection: sqlite3.Connection) -> dict[str, int]:
    """Store note detail text from the trusted-click captures; record blocks."""

    stats = {"fetched": 0, "skipped": 0, "blocked": 0}
    done = done_item_ids(connection)
    for path in sorted((RAW_DIR / "xiaohongshu").glob("note-*.json")):
        data = load_raw(f"xiaohongshu/{path.name}")
        note_id = path.stem.replace("note-", "")
        row = connection.execute(
            "SELECT id FROM items WHERE platform='xiaohongshu' AND external_id LIKE ?", (f"%{note_id}%",)
        ).fetchone()
        if row is None:
            continue
        if row["id"] in done:
            stats["skipped"] += 1
            continue
        blocked = "当前笔记暂时无法浏览" in str(data.get("title") or "") + str(data.get("bodySample") or "")
        if blocked:
            stats["blocked"] += 1
            store_detail(connection, row["id"], "ego-browser DOM detail attempt", data.get("pageUrl"),
                         "", "blocked", "detail page shows 暂时无法浏览 without login; card-level data remains authoritative")
            continue
        content_parts = [str(data.get("title") or ""), str(data.get("content") or "")]
        comments = [str(c) for c in (data.get("comments") or []) if str(c).strip()]
        if comments:
            content_parts.append("— comments —")
            content_parts.extend(f"- {c}" for c in comments)
        engage = re.sub(r"\s+", " ", str(data.get("engageText") or "")).strip()
        content = "\n".join(part for part in content_parts if part).strip()
        if content:
            stats["fetched"] += 1
            store_detail(connection, row["id"], str(data.get("method") or "ego-browser DOM detail"),
                         data.get("pageUrl"), content[:6000], "ok",
                         (f"engage: {engage}" if engage else None) + (f"; {len(comments)} comments" if comments else ""))
    connection.commit()
    return stats


def main() -> int:
    """Run every enrichment stage and print per-stage statistics."""

    connection = connect()
    ensure_tables(connection)
    token = gh_token()
    stages = [
        ("xhs-details", lambda: xiaohongshu_details(connection)),
        ("github-readme", lambda: github_readmes(connection, token)),
        ("hn-threads", lambda: hackernews_threads(connection)),
        ("web-articles", lambda: web_articles(connection)),
        ("reddit-bodies", lambda: reddit_bodies(connection)),
        ("x-bodies", lambda: x_bodies(connection)),
        ("bilibili-desc", lambda: bilibili_descriptions(connection)),
        ("zhihu-answers", lambda: zhihu_full_answers(connection)),
    ]
    for name, stage in stages:
        stats = stage()
        print(f"{name:16s} {stats}")
    total = connection.execute("SELECT COUNT(*) FROM item_details").fetchone()[0]
    with_content = connection.execute("SELECT COUNT(*) FROM item_details WHERE status='ok' AND char_count > 0").fetchone()[0]
    chars = connection.execute("SELECT SUM(char_count) FROM item_details WHERE status='ok'").fetchone()[0] or 0
    print(f"details: {total} rows, {with_content} with content, {chars:,} chars total")
    return 0


if __name__ == "__main__":
    sys.exit(main())
