#!/usr/bin/env python3
"""Build the static skills-store projection from the authoritative SQLite database."""

from __future__ import annotations

import datetime as dt
import html
import json
import re
import shutil
import sqlite3
from pathlib import Path, PurePosixPath
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
DOCS = ROOT / "docs"
DATA = DOCS / "data"
SKILLS = DOCS / "skills"
MEDIA = ROOT / "media"
PUBLISHED_MEDIA = DOCS / "media"
CONFIG_PATH = ROOT / "config" / "site.json"
MARKET_REGISTRY_PATH = DATA / "market-registry.json"

PLATFORM_LABELS = {
    "github": "GitHub",
    "hacker_news": "Hacker News",
    "x": "X",
    "xiaohongshu": "小红书",
    "youtube": "YouTube",
    "bilibili": "哔哩哔哩",
    "reddit": "Reddit",
    "wechat": "微信公众号",
    "web": "开放网页",
    "zhihu": "知乎",
    "official": "官方站",
    "linuxdo": "LINUX DO",
    "v2ex": "V2EX",
    "weibo": "微博",
}

CATEGORY_LABELS = {
    "core-and-ecosystem": "核心生态",
    "index-and-marketplace": "索引与市场",
    "ui-and-desktop": "界面与桌面",
    "operations-and-safety": "运维与安全",
    "multimedia-and-vision": "多媒体与视觉",
    "docs-and-learning": "文档与学习",
    "agents-and-orchestration": "Agent 与编排",
}

METRIC_FIELDS = (
    ("stars", "★"),
    ("likes", "♥"),
    ("views", "views"),
    ("points", "points"),
    ("comments", "comments"),
    ("forks", "forks"),
    ("replies", "replies"),
    ("favorites", "favorites"),
    ("shares", "shares"),
    ("coins", "coins"),
    ("danmaku", "danmaku"),
)


def esc(value: object, *, attribute: bool = False) -> str:
    """Escape a value for a generated HTML or XML context."""

    return html.escape(str(value or ""), quote=attribute)


def compact_text(value: object, limit: int = 280) -> str:
    """Collapse captured whitespace and cap public excerpts."""

    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def format_number(value: object) -> str:
    """Format a metric without inventing a value for NULL."""

    if value is None:
        return ""
    return f"{int(value):,}"


def date_label(value: object) -> str:
    """Keep the UTC date visible while removing noisy time precision."""

    text = str(value or "")
    return text[:10] if len(text) >= 10 else text


def valid_url(value: object) -> bool:
    """Allow only public HTTP(S) media and source URLs in the static view."""

    return urlparse(str(value or "")).scheme in {"http", "https"}


def valid_media_reference(value: object) -> bool:
    """Allow public URLs and safe paths inside the published media directory."""

    if valid_url(value):
        return True
    text = str(value or "")
    path = PurePosixPath(text)
    return (
        bool(text)
        and not text.startswith("/")
        and "\\" not in text
        and path.parts[:1] == ("media",)
        and ".." not in path.parts
    )


def page_media_url(value: object, prefix: str = "") -> str:
    """Resolve one safe local media path for the current generated page."""

    text = str(value or "")
    return text if valid_url(text) else prefix + text


def absolute_media_url(value: object, site_url: str) -> str:
    """Resolve one safe local media path against the configured site URL."""

    text = str(value or "")
    return text if valid_url(text) else site_url.rstrip("/") + "/" + text


def connection() -> sqlite3.Connection:
    """Open the generated database with named result columns."""

    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def read_config() -> dict[str, str]:
    """Read deployment and canonical URL settings."""

    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def load_market_registry() -> dict[str, object]:
    """Read the exact public Market registry shared by the website and Agent plugin."""

    payload = json.loads(MARKET_REGISTRY_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("market registry must be a JSON object")
    plugins = payload.get("plugins")
    categories = payload.get("categories")
    if not isinstance(plugins, list) or not isinstance(categories, dict):
        raise ValueError("market registry must contain plugins and categories")
    if payload.get("count") != len(plugins):
        raise ValueError("market registry count does not match plugins")
    for plugin in plugins:
        install = plugin.get("install") if isinstance(plugin, dict) else None
        if (
            not isinstance(plugin, dict)
            or not isinstance(plugin.get("id"), str)
            or not isinstance(install, dict)
            or not isinstance(install.get("spec"), str)
        ):
            raise ValueError("market registry contains an invalid plugin identity")
    return payload


def metric_values(row: sqlite3.Row) -> dict[str, int]:
    """Return only observed integer metrics for a card or detail page."""

    values: dict[str, int] = {}
    for field, _label in METRIC_FIELDS:
        value = row[field]
        if value is not None:
            values[field] = int(value)
    return values


def metric_score(metrics: dict[str, int]) -> int:
    """Provide a local sort signal without combining platform metrics in copy."""

    return max(metrics.values(), default=0)


def extract_repo(url: str, platform: str) -> str | None:
    """Extract a GitHub owner/repository label when the URL is a repository."""

    if platform != "github":
        return None
    parts = [part for part in urlparse(url).path.split("/") if part]
    return "/".join(parts[:2]) if len(parts) >= 2 else None


def load_records(db: sqlite3.Connection) -> list[dict[str, object]]:
    """Load deduplicated records, latest metrics, media, and registry dates."""

    rows = db.execute(
        """
        SELECT
            i.id, i.platform, i.external_id, i.canonical_url, i.item_type,
            i.title, i.author, i.author_url, i.published_at, i.published_label,
            i.content_text, i.language, i.category, i.relevance, i.media_kind,
            i.first_seen_at, i.last_seen_at,
            item_run.dataset_version AS item_dataset_version,
            ir.id AS registry_id, ir.rank, ir.stars AS registry_stars,
            ir.refs AS registry_refs, ir.picture AS registry_picture,
            vm.likes, vm.replies, vm.reposts, vm.comments, vm.bookmarks,
            vm.views, vm.points, vm.stars, vm.forks, vm.open_issues,
            vm.favorites, vm.shares, vm.coins, vm.danmaku, vm.upvote_ratio,
            vm.observed_at AS metric_observed_at,
            (SELECT m.metric_source
             FROM metrics AS m
             WHERE m.item_id = i.id
             ORDER BY m.observed_at DESC, m.id DESC
             LIMIT 1) AS metric_source,
            (SELECT cr.dataset_version
             FROM metrics AS m
             LEFT JOIN collection_runs AS cr ON cr.id = m.collection_run_id
             WHERE m.item_id = i.id
             ORDER BY m.observed_at DESC, m.id DESC
             LIMIT 1) AS metric_dataset_version
        FROM items AS i
        LEFT JOIN collection_runs AS item_run ON item_run.id = i.last_seen_run_id
        LEFT JOIN index_records AS ir ON ir.item_id = i.id
        LEFT JOIN v_latest_metrics AS vm ON vm.item_id = i.id
        ORDER BY COALESCE(ir.rank, 999999), i.id
        """
    ).fetchall()
    media_rows = db.execute(
        """
        SELECT item_id, kind, url, thumbnail_url, alt_text, rights_note
        FROM media_assets
        WHERE url IS NOT NULL
        ORDER BY id
        """
    ).fetchall()
    media_by_item: dict[int, list[dict[str, object]]] = {}
    for media in media_rows:
        if not valid_media_reference(media["url"]):
            continue
        media_by_item.setdefault(int(media["item_id"]), []).append(
            {
                "kind": media["kind"],
                "url": media["url"],
                "thumbnail_url": media["thumbnail_url"] if valid_media_reference(media["thumbnail_url"]) else None,
                "alt": media["alt_text"] or "Public media reference",
                "rights_note": media["rights_note"],
            }
        )
    listing_rows = db.execute(
        """
        SELECT ue.item_id, ue.listing_key, ue.entry_name, ue.entry_url,
               ue.registry_id, ue.owner, ue.page_url, ue.category,
               ue.install_hint, ue.install_spec, ue.install_target,
               ue.plugin_version, ue.verified, ue.tags_json,
               ue.source_path, ue.raw_snapshot_id,
               ue.first_seen_at, ue.last_seen_at,
               listing_run.dataset_version,
               ur.full_name AS source_repository,
               ur.source_url AS source_repository_url
        FROM upstream_entries AS ue
        JOIN upstream_repositories AS ur ON ur.id = ue.repository_id
        LEFT JOIN raw_snapshots AS listing_raw ON listing_raw.id = ue.raw_snapshot_id
        LEFT JOIN collection_runs AS listing_run ON listing_run.id = listing_raw.collection_run_id
        WHERE ue.active = 1 AND ue.item_id IS NOT NULL
        ORDER BY ue.item_id,
                 ue.install_hint IS NULL,
                 ue.registry_id IS NULL,
                 ue.last_seen_at DESC,
                 ur.full_name,
                 ue.listing_key
        """
    ).fetchall()
    listings_by_item: dict[int, list[dict[str, object]]] = {}
    for listing in listing_rows:
        try:
            tags = json.loads(listing["tags_json"] or "[]")
        except (TypeError, json.JSONDecodeError):
            tags = []
        listings_by_item.setdefault(int(listing["item_id"]), []).append({
            "listing_key": listing["listing_key"],
            "name": listing["entry_name"],
            "url": listing["entry_url"],
            "registry_id": listing["registry_id"],
            "owner": listing["owner"],
            "page_url": listing["page_url"] if valid_url(listing["page_url"]) else None,
            "category": listing["category"],
            "install_hint": listing["install_hint"],
            "install_spec": listing["install_spec"],
            "install_target": listing["install_target"],
            "version": listing["plugin_version"],
            "verified_claim": None if listing["verified"] is None else bool(listing["verified"]),
            "tags": tags if isinstance(tags, list) else [],
            "source_path": listing["source_path"],
            "raw_snapshot_id": listing["raw_snapshot_id"],
            "first_seen_at": listing["first_seen_at"],
            "last_seen_at": listing["last_seen_at"],
            "dataset_version": listing["dataset_version"],
            "source_repository": listing["source_repository"],
            "source_repository_url": listing["source_repository_url"],
        })

    records: list[dict[str, object]] = []
    for row in rows:
        metrics = metric_values(row)
        url = str(row["canonical_url"])
        record_id = str(row["registry_id"] or f"id-{row['id']}")
        repo = extract_repo(url, str(row["platform"]))
        media = media_by_item.get(int(row["id"]), [])[:6]
        try:
            refs = json.loads(row["registry_refs"] or "[]")
        except (TypeError, json.JSONDecodeError):
            refs = []
        try:
            pictures = json.loads(row["registry_picture"] or "[]")
        except (TypeError, json.JSONDecodeError):
            pictures = []
        listings = listings_by_item.get(int(row["id"]), [])
        evidence_timestamps = [
            str(timestamp)
            for timestamp in [
                row["last_seen_at"],
                row["metric_observed_at"],
                *(listing.get("last_seen_at") for listing in listings),
            ]
            if timestamp
        ]
        evidence_versions = [
            (str(timestamp), str(version))
            for timestamp, version in [
                (row["last_seen_at"], row["item_dataset_version"]),
                (row["metric_observed_at"], row["metric_dataset_version"]),
                *((listing.get("last_seen_at"), listing.get("dataset_version")) for listing in listings),
            ]
            if timestamp and version
        ]
        if not media:
            for picture in pictures:
                if valid_url(picture) and picture != url:
                    media.append({"kind": "picture", "url": picture, "thumbnail_url": None, "alt": "Public picture reference", "rights_note": None})
        if not media and row["platform"] == "github" and valid_url(row["author_url"]):
            media = [{"kind": "avatar", "url": row["author_url"], "thumbnail_url": None, "alt": "Repository author", "rights_note": None}]
        records.append(
            {
                "id": record_id,
                "item_id": int(row["id"]),
                "platform": row["platform"],
                "platform_label": PLATFORM_LABELS.get(str(row["platform"]), str(row["platform"])),
                "external_id": row["external_id"],
                "url": url,
                "repo": repo,
                "item_type": row["item_type"],
                "title": row["title"] or url,
                "author": row["author"],
                "author_url": row["author_url"] if valid_url(row["author_url"]) else None,
                "published_at": row["published_at"],
                "published_label": row["published_label"],
                "description": compact_text(row["content_text"] or row["title"], 360),
                "language": row["language"],
                "category": row["category"],
                "category_label": CATEGORY_LABELS.get(str(row["category"]), str(row["category"])),
                "relevance": row["relevance"],
                "media_kind": row["media_kind"],
                "metrics": metrics,
                "metric_observed_at": row["metric_observed_at"],
                "metric_source": row["metric_source"],
                "metric_score": metric_score(metrics),
                "media": media,
                "rank": int(row["rank"] or 999999),
                "first_seen_at": row["first_seen_at"],
                "last_seen_at": row["last_seen_at"],
                "dataset_version": None,
                "evidence_dataset_version": max(evidence_versions)[1] if evidence_versions else None,
                "evidence_updated_at": max(evidence_timestamps) if evidence_timestamps else row["last_seen_at"],
                "refs": [ref for ref in refs if valid_url(ref)],
                "listings": listings,
            }
        )
    return records


def latest_run(db: sqlite3.Connection) -> tuple[str, str]:
    """Read the latest successful dataset version and completion time."""

    row = db.execute(
        """
        SELECT dataset_version, COALESCE(finished_at, started_at)
        FROM collection_runs
        WHERE trigger <> 'legacy-migration' AND status = 'success'
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()
    return (str(row[0]), str(row[1])) if row else ("unversioned", "unknown")


def card_metrics(record: dict[str, object]) -> str:
    """Render native platform metrics as compact, non-additive labels."""

    metrics = record["metrics"]
    assert isinstance(metrics, dict)
    parts = []
    for field, label in METRIC_FIELDS:
        if field in metrics:
            parts.append(f"<span>{esc(label)} {esc(format_number(metrics[field]))}</span>")
        if len(parts) == 3:
            break
    return "".join(parts) or '<span class="muted">No public count</span>'


def metric_summary(record: dict[str, object]) -> str:
    """Render every observed native counter for a comparison table."""

    metrics = record["metrics"]
    assert isinstance(metrics, dict)
    labels = {
        "stars": "stars", "likes": "likes", "views": "views", "points": "points",
        "comments": "comments", "replies": "replies", "favorites": "favorites",
        "shares": "shares", "coins": "coins", "danmaku": "danmaku", "forks": "forks",
        "open_issues": "open issues", "bookmarks": "bookmarks", "reposts": "reposts",
    }
    parts = [
        f"{labels[field]} {format_number(metrics[field])}"
        for field in labels
        if field in metrics
    ]
    return " · ".join(parts) or "NULL"


def record_image(record: dict[str, object]) -> str | None:
    """Select the first public image or thumbnail for a card cover."""

    media = record["media"]
    assert isinstance(media, list)
    for asset in media:
        assert isinstance(asset, dict)
        thumbnail = asset.get("thumbnail_url")
        if valid_media_reference(thumbnail):
            return str(thumbnail)
    for asset in media:
        assert isinstance(asset, dict)
        if asset.get("kind") not in {"image", "image-local", "thumbnail", "avatar", "picture"}:
            continue
        if valid_media_reference(asset.get("url")):
            return str(asset["url"])
    return None


def video_embed_url(value: object) -> str | None:
    """Convert supported public watch URLs into embeddable player URLs."""

    if not valid_url(value):
        return None
    parsed = urlparse(str(value))
    host = parsed.netloc.lower().split(":", 1)[0]
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        video_id = parse_qs(parsed.query).get("v", [""])[0]
        if re.fullmatch(r"[A-Za-z0-9_-]{6,}", video_id):
            return f"https://www.youtube-nocookie.com/embed/{video_id}"
    if host == "youtu.be":
        video_id = parsed.path.strip("/").split("/", 1)[0]
        if re.fullmatch(r"[A-Za-z0-9_-]{6,}", video_id):
            return f"https://www.youtube-nocookie.com/embed/{video_id}"
    if host in {"bilibili.com", "www.bilibili.com"}:
        match = re.search(r"/video/(BV[A-Za-z0-9]+)", parsed.path)
        if match:
            return f"https://player.bilibili.com/player.html?bvid={match.group(1)}"
    if host == "mp.weixin.qq.com" and parsed.path == "/mp/readtemplate":
        return str(value)
    return None


def video_structured_data(
    record: dict[str, object],
    canonical: str,
    description: str,
    site_url: str,
) -> dict[str, object] | None:
    """Build a complete VideoObject only when captured evidence has required fields."""

    published_at = str(record.get("published_at") or "").strip()
    media = record.get("media")
    if not published_at or not isinstance(media, list):
        return None
    for asset in media:
        if not isinstance(asset, dict) or asset.get("kind") != "video":
            continue
        thumbnail = asset.get("thumbnail_url")
        embed_url = video_embed_url(asset.get("url"))
        if not valid_media_reference(thumbnail) or not embed_url:
            continue
        return {
            "@type": "VideoObject",
            "name": record["title"],
            "description": description,
            "thumbnailUrl": [absolute_media_url(thumbnail, site_url)],
            "uploadDate": published_at,
            "embedUrl": embed_url,
            "url": canonical,
            "isPartOf": {"@type": "WebSite", "url": site_url + "/"},
        }
    return None


def render_media_gallery(record: dict[str, object]) -> str:
    """Render captured images as images and captured videos as players."""

    media = record.get("media")
    if not isinstance(media, list):
        return ""
    title = str(record.get("title") or "Public media reference")
    figures = []
    for asset in media:
        if not isinstance(asset, dict) or not valid_media_reference(asset.get("url")):
            continue
        source_url = str(asset["url"])
        page_url = page_media_url(source_url, "../")
        kind = str(asset.get("kind") or "link")
        rights_note = str(asset.get("rights_note") or "").strip()
        rights_html = f"<span>{esc(rights_note)}</span>" if rights_note else ""
        if kind == "video":
            embed_url = video_embed_url(source_url)
            if embed_url:
                content = (
                    f'<div class="media-frame"><iframe class="media-video-player" '
                    f'src="{esc(embed_url, attribute=True)}" title="{esc(title, attribute=True)}" '
                    'loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture; web-share" '
                    'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>'
                )
            else:
                content = f'<a class="media-source-link" href="{esc(page_url, attribute=True)}" rel="noreferrer">Open video source ↗</a>'
            figures.append(
                f'<figure class="media-item media-video">{content}<figcaption>'
                f'<a href="{esc(page_url, attribute=True)}" rel="noreferrer">Video source ↗</a>{rights_html}'
                '</figcaption></figure>'
            )
            continue
        image_url = asset.get("thumbnail_url") or asset.get("url")
        if kind in {"image", "image-local", "thumbnail", "avatar", "picture"} and valid_media_reference(image_url):
            page_image_url = page_media_url(image_url, "../")
            referrer_policy = ' referrerpolicy="no-referrer"' if valid_url(image_url) else ""
            figures.append(
                f'<figure class="media-item media-image"><a href="{esc(page_url, attribute=True)}" rel="noreferrer">'
                f'<img src="{esc(page_image_url, attribute=True)}" alt="{esc(asset.get("alt"), attribute=True)}" loading="lazy"{referrer_policy}></a>'
                f'<figcaption><a href="{esc(page_url, attribute=True)}" rel="noreferrer">Image source ↗</a>{rights_html}</figcaption></figure>'
            )
            continue
        figures.append(
            f'<figure class="media-item media-link"><a class="media-source-link" href="{esc(page_url, attribute=True)}" rel="noreferrer">'
            f'Open {esc(kind)} source ↗</a><figcaption>{rights_html}</figcaption></figure>'
        )
    return "".join(figures)


def install_command(record: dict[str, object]) -> str | None:
    """Return a source-declared DSH install command without guessing a package name."""

    listings = record.get("listings")
    if not isinstance(listings, list):
        return None
    for listing in listings:
        if not isinstance(listing, dict):
            continue
        command = str(listing.get("install_hint") or "").strip()
        if command:
            return command
    return None


def primary_signal(record: dict[str, object]) -> str:
    """Format one platform-native signal without combining unrelated counters."""

    metrics = record["metrics"]
    assert isinstance(metrics, dict)
    preferred = {
        "github": ("stars", "★"),
        "hacker_news": ("points", "points"),
        "x": ("likes", "♥"),
        "xiaohongshu": ("likes", "♥"),
        "youtube": ("views", "views"),
        "bilibili": ("views", "views"),
    }.get(str(record["platform"]))
    fields = [preferred] if preferred else []
    fields.extend((field, label) for field, label in METRIC_FIELDS if not preferred or field != preferred[0])
    for field, label in fields:
        if field in metrics:
            return f"{label} {format_number(metrics[field])}"
    return "NULL"


def primary_value(record: dict[str, object]) -> int:
    """Return the platform-native value shown in a hot-table row."""

    metrics = record["metrics"]
    assert isinstance(metrics, dict)
    preferred = {
        "github": "stars",
        "hacker_news": "points",
        "x": "likes",
        "xiaohongshu": "likes",
        "youtube": "views",
        "bilibili": "views",
    }.get(str(record["platform"]))
    fields = [preferred] if preferred else []
    fields.extend(field for field, _label in METRIC_FIELDS if not preferred or field != preferred)
    for field in fields:
        if field in metrics:
            return int(metrics[field])
    return 0


def hot_records(records: list[dict[str, object]], platform: str | None = None) -> list[dict[str, object]]:
    """Select direct plugin-system signals for the two homepage hot tables."""

    candidates = [
        record for record in records
        if record["relevance"] == "direct"
        and (record["platform"] == platform if platform else record["platform"] != "github")
        and (record["item_type"] == "repository" if platform == "github" else record["item_type"] != "repository")
        and primary_value(record) > 0
    ]
    candidates.sort(key=lambda record: (-primary_value(record), int(record["rank"])))
    return candidates[:10]


def signal_table(records: list[dict[str, object]], title: str, kicker: str, description: str, action_label: str) -> str:
    """Render a ranked signal table with a direct detail or install action."""

    rows = []
    for position, record in enumerate(records, 1):
        details_url = f"skills/{record['id']}.html"
        command = install_command(record)
        action = (
            f'<button class="table-action copy-install" type="button" data-install="{esc(command, attribute=True)}" aria-label="Use {esc(record["title"], attribute=True)}">Use</button>'
            if command
            else f'<a class="table-action" href="{esc(record["url"], attribute=True)}" rel="noreferrer">{action_label}</a>'
        )
        rows.append(
            f'<tr><td class="signal-rank">{position:02d}</td>'
            f'<td><a class="signal-title" href="{details_url}">{esc(record["title"])}</a>'
            f'<small>{esc(record["platform_label"])} · {esc(record["category_label"])} · {esc(record["author"] or record["repo"] or "—")}</small></td>'
            f'<td class="signal-count"><strong>{esc(primary_signal(record))}</strong><small>{esc(record["item_type"])}</small></td>'
            f'<td class="signal-metrics"><span>{esc(metric_summary(record))}</span><small>snapshot {esc(date_label(record["metric_observed_at"]) or "NULL")}</small></td>'
            f'<td class="signal-source"><a href="{esc(record["url"], attribute=True)}" rel="noreferrer">Source ↗</a><small>{esc(record["metric_source"] or "metric source unreported")}</small></td>'
            f'<td class="signal-action">{action}</td></tr>'
        )
    if not rows:
        rows.append('<tr><td colspan="6" class="signal-empty">No public counter captured yet.</td></tr>')
    return f'<section class="signal-panel"><div class="signal-heading"><div><p class="kicker">{esc(kicker)}</p><h2>{esc(title)}</h2></div><p>{esc(description)}</p></div><div class="signal-scroll"><table class="signal-table"><thead><tr><th>#</th><th>Record</th><th>Rank signal</th><th>Platform metrics</th><th>Evidence source</th><th>Action</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></section>'


def card_html(record: dict[str, object], prefix: str = "") -> str:
    """Render one store card with search and sort metadata."""

    title = str(record["title"])
    image = record_image(record)
    cover = (
        f'<img src="{esc(page_media_url(image, prefix), attribute=True)}" alt="" loading="lazy">'
        if image
        else f'<span class="cover-initial">{esc(title[:1].upper())}</span>'
    )
    details_url = f"{prefix}skills/{record['id']}.html"
    author = record["author"] or record["repo"] or record["platform_label"]
    relevance = "direct" if record["relevance"] == "direct" else "related"
    command = install_command(record)
    action = (
        f'<button class="card-use copy-install" type="button" data-install="{esc(command, attribute=True)}" aria-label="Use {esc(title, attribute=True)}">Use</button>'
        if command
        else f'<a class="card-use" href="{esc(record["url"], attribute=True)}" rel="noreferrer">Open ↗</a>'
    )
    return f"""<article class="skill-card" data-platform="{esc(record['platform'], attribute=True)}" data-category="{esc(record['category'], attribute=True)}" data-relevance="{relevance}" data-title="{esc(title.lower(), attribute=True)}" data-rank="{record['rank']}" data-score="{record['metric_score']}" data-seen="{esc(record['last_seen_at'], attribute=True)}">
  <a class="card-cover" href="{esc(details_url, attribute=True)}" aria-label="Open {esc(title, attribute=True)}">{cover}<span class="cover-type">{esc(record['item_type'])}</span></a>
  <div class="card-body">
    <div class="card-meta"><span>{esc(record['platform_label'])}</span><span>{esc(record['category_label'])}</span></div>
    <h3><a href="{esc(details_url, attribute=True)}">{esc(title)}</a></h3>
    <p class="card-description">{esc(record['description'])}</p>
    <div class="card-footer"><span>{esc(str(author))}</span><span class="card-metrics">{card_metrics(record)}</span></div>
    <div class="card-actions"><a class="card-view" href="{esc(details_url, attribute=True)}">Details</a>{action}</div>
  </div>
</article>"""


def spotlight_html(records: list[dict[str, object]]) -> str:
    """Render a small editorial strip of high-signal public records."""

    candidates = [record for record in records if record["relevance"] == "direct"]
    candidates.sort(key=lambda record: (-int(record["metric_score"]), int(record["rank"])))
    selected = candidates[:6]
    cards = []
    for record in selected:
        image = record_image(record)
        cover = f'<img src="{esc(page_media_url(image), attribute=True)}" alt="" loading="lazy">' if image else '<span class="cover-initial">DS</span>'
        cards.append(
            f'<a class="spotlight-item" href="skills/{esc(record["id"], attribute=True)}.html">{cover}<span><strong>{esc(record["title"])}</strong><small>{esc(record["platform_label"])} · {esc(record["category_label"])}</small></span></a>'
        )
    return "".join(cards)


def filter_buttons(records: list[dict[str, object]]) -> tuple[str, str]:
    """Render topic and platform filters with stable counts."""

    category_counts: dict[str, int] = {}
    platform_counts: dict[str, int] = {}
    for record in records:
        category_counts[str(record["category"])] = category_counts.get(str(record["category"]), 0) + 1
        platform_counts[str(record["platform"])] = platform_counts.get(str(record["platform"]), 0) + 1
    categories = sorted(category_counts.items(), key=lambda pair: (-pair[1], pair[0]))
    platforms = sorted(platform_counts.items(), key=lambda pair: (-pair[1], pair[0]))
    category_html = "".join(
        f'<button class="filter-option" data-filter-type="category" data-filter-value="{esc(key, attribute=True)}"><span>{esc(CATEGORY_LABELS.get(key, key))}</span><em>{count}</em></button>'
        for key, count in categories
    )
    platform_html = "".join(
        f'<button class="filter-option" data-filter-type="platform" data-filter-value="{esc(key, attribute=True)}"><span>{esc(PLATFORM_LABELS.get(key, key))}</span><em>{count}</em></button>'
        for key, count in platforms
    )
    return category_html, platform_html


def market_observed_at(plugin: dict[str, object]) -> str:
    """Return the latest attributed Listing observation for one Market plugin."""

    sources = plugin.get("sources")
    if not isinstance(sources, list):
        return ""
    observed = [
        str(source.get("observedAt") or "")
        for source in sources
        if isinstance(source, dict) and source.get("observedAt")
    ]
    return max(observed, default="")


def market_source_names(plugin: dict[str, object]) -> list[str]:
    """Return stable Registry Source names attributed to one Market plugin."""

    sources = plugin.get("sources")
    if not isinstance(sources, list):
        return []
    return sorted({
        str(source["registry"])
        for source in sources
        if isinstance(source, dict) and source.get("registry")
    })


def market_card_html(plugin: dict[str, object], category_label: str, rank: int) -> str:
    """Render one installable Market registry entry without inferring its spec."""

    install = plugin["install"]
    assert isinstance(install, dict)
    spec = str(install["spec"])
    command = f"dsh plugin --profile web add {spec}"
    name = str(plugin.get("name") or plugin["id"])
    agent_request = (
        f"请先在 deeplugin.store 中检索 Registry ID {plugin['id']}，展示来源和精确安装 spec，"
        "为 web profile 生成安装计划；等我明确批准后再安装。"
    )
    author = str(plugin.get("author") or "unknown")
    description = str(plugin.get("description_zh") or plugin.get("description") or name)
    homepage = str(plugin.get("homepage") or "")
    source_names = market_source_names(plugin)
    source_summary = ", ".join(source_names[:3])
    if len(source_names) > 3:
        source_summary += f" +{len(source_names) - 3}"
    tags = plugin.get("tags")
    search_terms = " ".join([
        name,
        author,
        spec,
        description,
        " ".join(str(tag) for tag in tags) if isinstance(tags, list) else "",
        " ".join(source_names),
    ]).lower()
    stars = plugin.get("stars")
    score = int(stars) if isinstance(stars, int) else -1
    stars_label = format_number(stars) if isinstance(stars, int) else "NULL"
    version = str(plugin.get("version") or "NULL")
    verified = plugin.get("verified") is True
    verified_label = "source claim verified" if verified else "no verified source claim"
    category = str(plugin.get("category") or "tools")
    observed_at = market_observed_at(plugin)
    source_link = homepage if valid_url(homepage) else "data/market-registry.json"
    return f"""<article class="skill-card market-plugin-card" data-category="{esc(category, attribute=True)}" data-verified="{str(verified).lower()}" data-title="{esc(search_terms, attribute=True)}" data-rank="{rank}" data-score="{score}" data-seen="{esc(observed_at, attribute=True)}">
  <div class="card-body">
    <div class="card-meta"><span>{esc(category_label)}</span><span>{esc(author)}</span></div>
    <h3><a href="{esc(source_link, attribute=True)}" rel="noreferrer">{esc(name)}</a></h3>
    <p class="card-description">{esc(description)}</p>
    <p class="market-plugin-id"><span>Registry ID</span><code>{esc(plugin['id'])}</code></p>
    <div class="install-command"><code>{esc(spec)}</code><button class="copy-install" type="button" data-install="{esc(command, attribute=True)}" aria-label="Copy install command for {esc(name, attribute=True)}" aria-live="polite">Copy CLI</button></div>
    <div class="market-agent-action"><span>ASK YOUR AGENT</span><button class="card-use copy-install" type="button" data-install="{esc(agent_request, attribute=True)}" aria-label="Copy an Agent installation request for {esc(name, attribute=True)}" aria-live="polite">Copy request</button></div>
    <div class="market-plugin-proof"><span>version <strong>{esc(version)}</strong></span><span>stars <strong>{esc(stars_label)}</strong></span><span class="{'claim-verified' if verified else 'claim-unverified'}">{esc(verified_label)}</span></div>
    <div class="card-actions"><span class="market-plugin-sources" title="{esc(', '.join(source_names), attribute=True)}">{esc(source_summary or 'source unreported')}</span><a class="card-view" href="{esc(source_link, attribute=True)}" rel="noreferrer">Source ↗</a></div>
  </div>
</article>"""


def render_market_page(registry: dict[str, object], config: dict[str, str]) -> str:
    """Render the human Store from the same registry consumed by the Agent plugin."""

    plugins = registry["plugins"]
    categories = registry["categories"]
    assert isinstance(plugins, list)
    assert isinstance(categories, dict)
    category_counts: dict[str, int] = {}
    registry_sources: set[str] = set()
    cards: list[str] = []
    for rank, plugin in enumerate(plugins, 1):
        assert isinstance(plugin, dict)
        category = str(plugin.get("category") or "tools")
        category_counts[category] = category_counts.get(category, 0) + 1
        registry_sources.update(market_source_names(plugin))
        labels = categories.get(category)
        category_label = str(labels.get("zh") or labels.get("en") or category) if isinstance(labels, dict) else category
        cards.append(market_card_html(plugin, category_label, rank))
    category_filters = []
    for key, count in sorted(category_counts.items(), key=lambda pair: (-pair[1], pair[0])):
        labels = categories.get(key)
        label = str(labels.get("zh") or labels.get("en") or key) if isinstance(labels, dict) else key
        category_filters.append(
            f'<button class="filter-option" data-filter-type="category" data-filter-value="{esc(key, attribute=True)}"><span>{esc(label)}</span><em>{count}</em></button>'
        )
    verified_count = sum(plugin.get("verified") is True for plugin in plugins if isinstance(plugin, dict))
    site_url = config["site_url"].rstrip("/")
    image = f"{site_url}/media/screenshots/official.png"
    item_list = [
        {"@type": "ListItem", "position": rank, "url": plugin.get("homepage"), "name": plugin.get("name")}
        for rank, plugin in enumerate(plugins[:24], 1)
        if isinstance(plugin, dict) and valid_url(plugin.get("homepage"))
    ]
    description = "可搜索、带来源、可由 Agent 在批准后安装的 DeepSeek Harness 插件目录。"
    head = page_head(
        "Plugin Store — deeplugin.store",
        description,
        site_url + "/market.html",
        image,
        config,
        extra_json_ld={"@type": "CollectionPage", "mainEntity": {"@type": "ItemList", "itemListElement": item_list}},
    ).replace("{ASSET_PREFIX}", "")
    market_plugin_command = "dsh plugin --profile web add github:Shiyao-Huang/awesome-deepseek-harness-plugin#path:/plugin"
    return f"""{head}<body data-page="market" data-result-noun="plugins">
{market_nav_html()}
<main class="site-main market-page">
  <section class="market-catalog-hero"><div><p class="kicker">INSTALLABLE STORE · {esc(registry.get('datasetVersion'))}</p><h1>Browse the Store.<br>Then ask your Agent to install.</h1><p>这里的 {len(plugins):,} 个插件全部来自公开 Registry Listing 或直接提交。每张卡片同时提供稳定 ID、精确 spec、来源，以及一条可复制给 Market Plugin 的自然语言安装请求。</p><div class="hero-actions"><a class="button button-primary" href="#market-directory">浏览插件 <span aria-hidden="true">↓</span></a><a class="button market-button-quiet" href="register.html">提交一个插件</a></div></div><div class="market-install"><span>INSTALL THE MARKET PLUGIN ONCE</span><code>{esc(market_plugin_command)}</code><button class="copy-install" type="button" data-install="{esc(market_plugin_command, attribute=True)}" aria-live="polite">Copy</button><div class="market-install-footer"><small>之后复制卡片里的 Agent request；Agent 展示来源与精确 spec，你批准后才安装。</small><a href="register-agent.html">Agent protocol ↗</a></div></div></section>
  <section class="stats-row market-catalog-stats" aria-label="Market registry statistics"><div><strong>{len(plugins):,}</strong><span>installable plugins</span></div><div><strong>{verified_count:,}</strong><span>source verification claims</span></div><div><strong>{len(category_counts):,}</strong><span>categories</span></div><div><strong>{len(registry_sources):,}</strong><span>attributed registries</span></div></section>
  <section class="directory-layout" id="market-directory">
    <aside class="filters"><div class="filter-mobile-head"><span>Plugin filters</span><button id="clear-filters" class="text-button">Clear</button></div><div class="filter-group"><p class="filter-label">BROWSE</p><button class="filter-option is-selected" data-filter-type="all" data-filter-value="all"><span>All installable</span><em>{len(plugins)}</em></button><button class="filter-option" data-filter-type="verified" data-filter-value="true"><span>Source claim verified</span><em>{verified_count}</em></button></div><div class="filter-group"><p class="filter-label">CATEGORIES</p>{''.join(category_filters)}</div><div class="filter-note"><strong>One registry, two clients</strong><p>Cards come from <a href="data/market-registry.json">the same JSON</a> embedded in Market Plugin. Verified is an attributed source claim, not this Store's security or compatibility endorsement.</p></div></aside>
    <div class="directory-content"><div class="directory-toolbar"><div><p class="kicker">THE STORE</p><h2>Find an installable plugin</h2><p id="result-summary">Showing {len(plugins):,} plugins</p></div><div class="toolbar-controls"><label class="search-field"><span aria-hidden="true">⌕</span><input id="search-input" type="search" placeholder="Search name, capability, spec, source..." autocomplete="off"><kbd>/</kbd></label><label class="sort-field"><span>Sort</span><select id="sort-select"><option value="rank">Registry order</option><option value="score">Most GitHub stars</option><option value="latest">Recently observed</option><option value="title">Title A–Z</option></select></label></div></div><div class="platform-summary"><span><b>{esc(registry.get('updated'))}</b> registry date</span><span><b>{esc(registry.get('generatedAt'))}</b> generated UTC</span><span><a href="data/market-registry.schema.json">JSON Schema ↗</a></span></div><div class="catalog-grid market-catalog-grid" id="catalog-grid">{''.join(cards)}</div><p class="no-results" id="no-results" hidden>No installable plugin matches this search. Clear a filter or try another phrase.</p></div>
  </section>
</main>
{footer_html(data_path=config['public_database_url'])}
<script src="assets/store.js" defer></script>
</body></html>"""


def page_head(title: str, description: str, canonical: str, image: str, config: dict[str, str], *, extra_json_ld: dict[str, object] | None = None) -> str:
    """Render shared SEO metadata and structured data."""

    json_ld: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": config["site_name"],
        "url": config["site_url"] + "/",
        "description": config["description"],
    }
    if extra_json_ld:
        json_ld.update(extra_json_ld)
    return f"""<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc(description, attribute=True)}">
<meta name="theme-color" content="#f5f1e8">
<link rel="canonical" href="{esc(canonical, attribute=True)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title, attribute=True)}">
<meta property="og:description" content="{esc(description, attribute=True)}">
<meta property="og:url" content="{esc(canonical, attribute=True)}">
<meta property="og:image" content="{esc(image, attribute=True)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title, attribute=True)}">
<meta name="twitter:description" content="{esc(description, attribute=True)}">
<title>{esc(title)}</title>
<link rel="stylesheet" href="{{ASSET_PREFIX}}assets/store.css">
<script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False, separators=(",", ":"))}</script>
</head>"""


def nav_html(prefix: str = "") -> str:
    """Render the store navigation used by all static pages."""

    return f"""<header class="site-header"><a class="brand" href="{prefix}"><span class="brand-mark">dsh</span><span>store</span></a><nav><a class="nav-active" href="{prefix}">Directory</a><a href="{prefix}#hot">Hot</a><a href="{prefix}timeline.html">Timeline</a><a href="{prefix}directories.html">Directories</a><a href="{prefix}sources.html">Sources</a></nav><a class="header-source" href="https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin">GitHub <span aria-hidden="true">↗</span></a></header>"""


def market_nav_html() -> str:
    """Render Store navigation without rewriting every ecosystem detail page."""

    return """<header class="site-header"><a class="brand" href="./"><span class="brand-mark">dsh</span><span>store</span></a><nav><a href="./">Directory</a><a class="nav-active" href="market.html">Store</a><a href="./#hot">Hot</a><a href="timeline.html">Timeline</a><a href="directories.html">Directories</a><a href="sources.html">Sources</a></nav><a class="header-source" href="https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin">GitHub <span aria-hidden="true">↗</span></a></header>"""


def footer_html(prefix: str = "", *, data_path: str, readme_path: str | None = None, seo_path: str | None = None) -> str:
    """Render the provenance and deployment footer."""

    readme_path = readme_path or ("../README.md" if not prefix else "../../README.md")
    seo_path = seo_path or ("seo.md" if not prefix else "../seo.md")
    return f"""<footer class="site-footer"><div><strong>dsh store</strong><p>A public, dated directory for the DeepSeek Harness plugin ecosystem.</p></div><div><a href="{readme_path}">Collection rules</a><a href="{data_path}">SQLite</a><a href="{seo_path}">SEO notes</a></div><p class="footer-note">Public metadata only. Platform counts stay native and are never added together.</p></footer>"""


def render_home(records: list[dict[str, object]], dataset_version: str, generated_at: str, config: dict[str, str], platform_counts: list[sqlite3.Row], category_counts: list[sqlite3.Row], market_registry: dict[str, object]) -> str:
    """Render the store-style directory homepage."""

    category_html, platform_html = filter_buttons(records)
    cards = "".join(card_html(record) for record in records)
    site_url = config["site_url"].rstrip("/")
    image = f"{site_url}/media/screenshots/official.png"
    market_plugins_value = market_registry.get("plugins")
    market_plugins = market_plugins_value if isinstance(market_plugins_value, list) else []
    market_dataset_version = market_registry.get("datasetVersion") or "unversioned"
    verified_plugins = sum(
        plugin.get("verified") is True
        for plugin in market_plugins
        if isinstance(plugin, dict)
    )
    registry_sources = {
        str(source["registry"])
        for plugin in market_plugins
        if isinstance(plugin, dict) and isinstance(plugin.get("sources"), list)
        for source in plugin["sources"]
        if isinstance(source, dict) and source.get("registry")
    }
    item_list = [
        {"@type": "ListItem", "position": index, "url": plugin["homepage"], "name": plugin["name"]}
        for index, plugin in enumerate(market_plugins[:24], 1)
        if isinstance(plugin, dict) and valid_url(plugin.get("homepage")) and plugin.get("name")
    ]
    description = "DeepSeek Harness Plugin Store：聚合市面上公开可安装的插件，安装一次 Market Plugin 后，可以用自然语言让 Agent 搜索、核对来源、批准安装并管理插件。"
    head = page_head(
        "deeplugin.store — DeepSeek Harness Plugin Store",
        description,
        site_url + "/",
        image,
        config,
        extra_json_ld={"@type": "CollectionPage", "mainEntity": {"@type": "ItemList", "itemListElement": item_list}},
    ).replace("{ASSET_PREFIX}", "")
    stats = {
        "records": len(records),
        "market": len(market_plugins),
        "verified": verified_plugins,
        "registries": len(registry_sources),
        "direct": sum(1 for record in records if record["relevance"] == "direct"),
    }
    platform_summary = "".join(
        f'<span><b>{row["count"]:,}</b> {esc(PLATFORM_LABELS.get(str(row["platform"]), row["platform"]))}</span>'
        for row in platform_counts[:6]
    )
    projects = hot_records(records, "github")
    posts = hot_records(records)
    hot_tables = signal_table(projects, "GitHub projects people are using", "PROJECTS · STARS", "插件系统内的仓库按 GitHub stars 排序；Use 只对明确的 dsh-* 仓库提供安装命令。", "Open") + signal_table(posts, "Posts and videos people are sharing", "POSTS · NATIVE SIGNAL", "帖子、文章和视频按各自平台的公开指标排序；数字不跨平台相加。", "Open")
    market_install_command = "dsh plugin --profile web add github:Shiyao-Huang/awesome-deepseek-harness-plugin#path:/plugin"
    market_agent_prompt_zh = (
        "请从 https://deeplugin.store/ 安装 Market Plugin 到 web profile。精确 spec 是 "
        "github:Shiyao-Huang/awesome-deepseek-harness-plugin#path:/plugin；先展示安装计划，等我明确批准后再安装。"
    )
    market_agent_prompt_en = (
        "Install the Market Plugin from https://deeplugin.store/ into my web profile. Its exact spec is "
        "github:Shiyao-Huang/awesome-deepseek-harness-plugin#path:/plugin. Show the install plan first and wait for my explicit approval."
    )
    return f"""{head}<body data-page="home">
{nav_html()}
<main class="site-main">
  <section class="hero-store">
    <div class="hero-copy"><p class="kicker">DEEPSEEK HARNESS PLUGIN STORE · {stats['market']:,} INSTALLABLE</p><h1>Find the right plugin.<br><em>Ask your Agent to install it.</em></h1><form class="hero-search" action="market.html" method="get"><input type="search" name="q" aria-label="What should DeepSeek do?" placeholder="What should DeepSeek do?" autocomplete="off"><button type="submit">Search Store <span aria-hidden="true">→</span></button></form><div class="hero-actions"><a class="button button-quiet" href="market.html">Browse all plugins</a><a class="button button-quiet" href="#market-plugin">Install Market Plugin <span aria-hidden="true">↓</span></a></div></div>
    <div class="hero-panel"><div class="panel-label">ONE COMMAND · OR ONE REQUEST</div><strong>自己装，或交给 DeepSeek。</strong><p>任选一种，复制即可。</p><div class="hero-tools" aria-label="Dataset versions"><span>ECOSYSTEM DATASET · {esc(dataset_version)}</span><span>MARKET REGISTRY · {esc(market_dataset_version)}</span><span>UPDATED · {esc(date_label(generated_at))}</span></div></div>
  </section>
  <section class="stats-row" aria-label="Store statistics"><div><strong>{stats['market']:,}</strong><span>installable plugins</span></div><div><strong>{stats['verified']:,}</strong><span>source verification claims</span></div><div><strong>{stats['registries']:,}</strong><span>attributed registries</span></div><div><strong>{stats['records']:,}</strong><span>ecosystem signals</span></div></section>
  <div class="market-guide" data-market-i18n data-market-lang="zh">
    <section class="market-band market-install-guide" id="market-plugin" aria-labelledby="market-heading">
      <div class="market-guide-head"><div><p class="kicker">INSTALL THE MARKET PLUGIN</p><h2 id="market-heading"><span data-copy-lang="zh" lang="zh-CN">选一种安装方式。</span><span data-copy-lang="en" lang="en">Choose one install path.</span></h2></div><div class="market-language" role="group" aria-label="Language"><button type="button" data-market-language="zh" aria-pressed="true">中文</button><button type="button" data-market-language="en" aria-pressed="false">EN</button></div></div>
      <div class="install-route-grid">
        <article class="install-route"><div class="install-route-label"><span>01</span><strong><span data-copy-lang="zh" lang="zh-CN">自己安装</span><span data-copy-lang="en" lang="en">Install it yourself</span></strong></div><p><span data-copy-lang="zh" lang="zh-CN">复制命令，在 DeepSeek Harness 的终端里运行。</span><span data-copy-lang="en" lang="en">Copy the command and run it in your DeepSeek Harness terminal.</span></p><div class="route-copy"><code>{esc(market_install_command)}</code><button class="copy-install" type="button" data-install="{esc(market_install_command, attribute=True)}" aria-label="Copy Market Plugin install command" aria-live="polite"><span data-copy-lang="zh">复制命令</span><span data-copy-lang="en">Copy command</span></button></div><ol class="route-steps"><li><span data-copy-lang="zh">运行命令</span><span data-copy-lang="en">Run the command</span></li><li><span data-copy-lang="zh">重启 DSH</span><span data-copy-lang="en">Restart DSH</span></li><li><span data-copy-lang="zh">直接问 Agent 找插件</span><span data-copy-lang="en">Ask your Agent for a plugin</span></li></ol></article>
        <article class="install-route install-route-agent"><div class="install-route-label"><span>02</span><strong><span data-copy-lang="zh" lang="zh-CN">交给 DeepSeek</span><span data-copy-lang="en" lang="en">Hand it to DeepSeek</span></strong></div><p><span data-copy-lang="zh" lang="zh-CN">复制下面这句话，粘贴到 DeepSeek Harness。</span><span data-copy-lang="en" lang="en">Copy this request and paste it into DeepSeek Harness.</span></p><div class="route-prompt"><p data-copy-lang="zh" lang="zh-CN">{esc(market_agent_prompt_zh)}</p><p data-copy-lang="en" lang="en">{esc(market_agent_prompt_en)}</p><button class="copy-install" type="button" data-copy-lang="zh" data-install="{esc(market_agent_prompt_zh, attribute=True)}" aria-label="复制给 DeepSeek" aria-live="polite">复制给 DeepSeek</button><button class="copy-install" type="button" data-copy-lang="en" data-install="{esc(market_agent_prompt_en, attribute=True)}" aria-label="Copy for DeepSeek" aria-live="polite">Copy for DeepSeek</button></div><ol class="route-steps"><li><span data-copy-lang="zh">DeepSeek 展示计划</span><span data-copy-lang="en">DeepSeek shows the plan</span></li><li><span data-copy-lang="zh">你确认精确 spec</span><span data-copy-lang="en">You review the exact spec</span></li><li><span data-copy-lang="zh">批准后执行</span><span data-copy-lang="en">It runs after approval</span></li></ol></article>
      </div>
      <div class="market-links"><a class="button button-primary" href="market.html"><span data-copy-lang="zh">浏览 {stats['market']:,} 个插件</span><span data-copy-lang="en">Browse {stats['market']:,} plugins</span></a><a class="market-text-link" href="https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin/tree/main/plugin">Source ↗</a><a class="market-text-link" href="data/market-registry.json">Registry JSON ↗</a><a class="market-text-link" href="data/market-registry.schema.json">Schema ↗</a><a class="market-text-link" href="register.html"><span data-copy-lang="zh">提交插件 ↗</span><span data-copy-lang="en">Submit a plugin ↗</span></a></div>
    </section>
    <section class="market-demo" aria-labelledby="market-demo-heading">
      <div class="market-demo-head"><div><p class="kicker">QA CASE · ACTUAL REGISTRY IDENTITY</p><h2 id="market-demo-heading"><span data-copy-lang="zh" lang="zh-CN">一句话，到插件开始工作。</span><span data-copy-lang="en" lang="en">From one request to a working plugin.</span></h2></div><p><span data-copy-lang="zh" lang="zh-CN">示例使用当前 Store 中真实的 modsearch 条目。</span><span data-copy-lang="en" lang="en">This example uses the current Store listing for modsearch.</span></p></div>
      <div class="chat-frames" aria-label="Example DeepSeek Harness chat sequence">
        <article class="chat-frame"><div class="chat-frame-bar"><span>01</span><strong>ASK</strong></div><div class="chat-frame-body"><p class="chat-role">YOU</p><p class="chat-message chat-message-user"><span data-copy-lang="zh" lang="zh-CN">我想让 DeepSeek 能搜索网页和 X，并在回答里保留引用。帮我找一个插件。</span><span data-copy-lang="en" lang="en">I need DeepSeek to search the web and X, with citations in every answer. Find me a plugin.</span></p><p class="chat-status"><span aria-hidden="true"></span><span data-copy-lang="zh">Market Plugin 正在检索</span><span data-copy-lang="en">Market Plugin is searching</span></p></div></article>
        <article class="chat-frame"><div class="chat-frame-bar"><span>02</span><strong>MATCH</strong></div><div class="chat-frame-body"><p class="chat-role">MARKET SEARCH · 3 MATCHES</p><h3>ModSearch</h3><p class="chat-description"><span data-copy-lang="zh" lang="zh-CN">匹配 web / search；返回结构化证据和可点击引用。</span><span data-copy-lang="en" lang="en">Matches web / search and returns structured evidence with clickable citations.</span></p><dl class="chat-proof"><div><dt>Source</dt><dd>zoahdev/dsh-subscribe</dd></div><div><dt>Version</dt><dd>5.4.2</dd></div><div><dt>Registry ID</dt><dd>deeplugin-c39668d81007d2defdf8</dd></div><div><dt>Exact spec</dt><dd>github:liustack/modsearch</dd></div></dl><p class="chat-status chat-status-ready"><span aria-hidden="true"></span><span data-copy-lang="zh">来源 Registry 声明 verified</span><span data-copy-lang="en">Verified claim from the named Registry</span></p></div></article>
        <article class="chat-frame"><div class="chat-frame-bar"><span>03</span><strong>REVIEW</strong></div><div class="chat-frame-body"><p class="chat-role">DEEPSEEK · INSTALL PLAN</p><p class="chat-message chat-message-agent"><span data-copy-lang="zh" lang="zh-CN">目标：web profile。将执行下面的完整命令。是否确认？</span><span data-copy-lang="en" lang="en">Target: web profile. The full command below will run. Confirm?</span></p><p class="chat-command">dsh plugin --profile web add github:liustack/modsearch</p><p class="chat-role">YOU</p><p class="chat-message chat-message-user"><span data-copy-lang="zh" lang="zh-CN">确认。</span><span data-copy-lang="en" lang="en">Confirm.</span></p></div></article>
        <article class="chat-frame"><div class="chat-frame-bar"><span>04</span><strong>USE</strong></div><div class="chat-frame-body"><p class="chat-role">DEEPSEEK</p><p class="chat-message chat-message-agent"><span data-copy-lang="zh" lang="zh-CN">安装完成。现在我可以搜索“DeepSeek Harness plugin registry”，并把结果和引用返回给你。</span><span data-copy-lang="en" lang="en">Installed. I can now search for “DeepSeek Harness plugin registry” and return the results with citations.</span></p><p class="chat-status chat-status-ready"><span aria-hidden="true"></span><span data-copy-lang="zh">ModSearch · web profile · ready</span><span data-copy-lang="en">ModSearch · web profile · ready</span></p></div></article>
      </div>
    </section>
  </div>
  <section class="hot-signals" id="hot"><div class="section-heading"><div><p class="kicker">HOT NOW</p><h2>What the plugin system is pulling forward</h2></div><p>项目看 stars，内容看各自平台的原生互动信号。</p></div><div class="hot-grid">{hot_tables}</div></section>
  <section class="spotlight"><div class="section-heading"><div><p class="kicker">EDITOR'S CUT</p><h2>What is moving now</h2></div><p>按平台原生指标排序；不同平台不混算。</p></div><div class="spotlight-grid">{spotlight_html(records)}</div></section>
  <section class="directory-layout" id="directory">
    <aside class="filters"><div class="filter-mobile-head"><span>Browse</span><button id="clear-filters" class="text-button">Clear</button></div><div class="filter-group"><p class="filter-label">BROWSE</p><button class="filter-option is-selected" data-filter-type="all" data-filter-value="all"><span>All records</span><em>{stats['records']}</em></button><button class="filter-option" data-filter-type="relevance" data-filter-value="direct"><span>Direct signals</span><em>{stats['direct']}</em></button></div><div class="filter-group"><p class="filter-label">TOPICS</p>{category_html}</div><div class="filter-group"><p class="filter-label">PLATFORMS</p>{platform_html}</div><div class="filter-note"><strong>Provenance first</strong><p>Every card points to an independent detail page with dates, native counts, media references, and a source URL.</p></div></aside>
    <div class="directory-content"><div class="directory-toolbar"><div><p class="kicker">THE DIRECTORY</p><h2>Discover ecosystem records</h2><p id="result-summary">Showing {stats['records']:,} records</p></div><div class="toolbar-controls"><label class="search-field"><span aria-hidden="true">⌕</span><input id="search-input" type="search" placeholder="Search repositories, topics, authors..." autocomplete="off"><kbd>/</kbd></label><label class="sort-field"><span>Sort</span><select id="sort-select"><option value="rank">Curated rank</option><option value="score">Highest native count</option><option value="latest">Recently observed</option><option value="title">Title A–Z</option></select></label></div></div><div class="platform-summary">{platform_summary}</div><div class="catalog-grid" id="catalog-grid">{cards}</div><p class="no-results" id="no-results" hidden>No records match this search. Clear a filter or try another phrase.</p></div>
  </section>
  <section class="method-band"><div><p class="kicker">HOW THIS DIRECTORY WORKS</p><h2>Collected, dated, and reviewable.</h2></div><div class="method-items"><p><strong>01</strong><span>Raw captures live in <code>data/raw/</code>.</span></p><p><strong>02</strong><span>SQLite stores versions and metric history.</span></p><p><strong>03</strong><span>Every two-hour run rebuilds this static store.</span></p></div></section>
</main>
{footer_html(data_path=config["public_database_url"])}
<script src="assets/store.js" defer></script>
</body></html>"""


def render_listing_evidence(record: dict[str, object]) -> str:
    """Render active source-attributed Registry Listings for one item."""

    listings = record.get("listings")
    if not isinstance(listings, list) or not listings:
        return ""
    rows = []
    for listing in listings:
        if not isinstance(listing, dict):
            continue
        source_repository = str(listing.get("source_repository") or "unknown registry")
        source_path = str(listing.get("source_path") or "unknown source")
        source_url = listing.get("page_url") or listing.get("source_repository_url")
        source_label = f"{source_repository} · {source_path}"
        source_html = (
            f'<a href="{esc(source_url, attribute=True)}" rel="noreferrer">{esc(source_label)}</a>'
            if valid_url(source_url)
            else esc(source_label)
        )
        install_spec = str(listing.get("install_spec") or "").strip()
        install_target = str(listing.get("install_target") or "").strip()
        install_html = f"<code>{esc(install_spec)}</code>" if install_spec else "—"
        if install_target:
            install_html += f"<br><small>{esc(install_target)}</small>"
        verified_claim = listing.get("verified_claim")
        if verified_claim is True:
            verification = "source claims verified"
        elif verified_claim is False:
            verification = "source does not claim verified"
        else:
            verification = "unreported"
        rows.append(
            f'<tr><td>{source_html}</td><td>{install_html}</td>'
            f'<td>{esc(listing.get("version") or "—")}</td><td>{esc(verification)}</td>'
            f'<td>{esc(date_label(listing.get("first_seen_at")))} → {esc(date_label(listing.get("last_seen_at")))}</td>'
            f'<td>{esc(listing.get("raw_snapshot_id") or "—")}</td></tr>'
        )
    if not rows:
        return ""
    return (
        '<section class="detail-context"><div><p class="kicker">REGISTRY LISTINGS</p>'
        '<h2>Source-attributed install evidence</h2></div>'
        '<div class="table-scroll"><table class="data-table"><thead><tr>'
        '<th>Registry source</th><th>Install spec</th><th>Version</th>'
        '<th>Verification claim</th><th>Observed</th><th>Raw snapshot</th>'
        f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
        '<p class="detail-footnote">Verification is a claim made by the named Registry Source; '
        'it is not a security, compatibility, quality, or official-endorsement claim by this site.</p></section>'
    )


def render_detail(record: dict[str, object], dataset_version: str, generated_at: str, config: dict[str, str]) -> str:
    """Render a static, crawlable detail page for one store record."""

    evidence_dataset_version = record.get("evidence_dataset_version") or dataset_version
    evidence_updated_at = record.get("evidence_updated_at") or generated_at
    site_url = config["site_url"].rstrip("/")
    canonical = f"{site_url}/skills/{record['id']}.html"
    title = f"{record['title']} — dsh store"
    description = compact_text(record["description"], 180) or "Public DeepSeek Harness ecosystem record."
    image_reference = record_image(record)
    image = absolute_media_url(image_reference, site_url) if image_reference else f"{site_url}/media/screenshots/official.png"
    detail_json_ld = video_structured_data(record, canonical, description, site_url)
    if not detail_json_ld:
        detail_json_ld = {
            "@type": "CreativeWork",
            "name": record["title"],
            "url": canonical,
            "isPartOf": {"@type": "WebSite", "url": site_url + "/"},
        }
        if image_reference:
            detail_json_ld["image"] = [image]
    head = page_head(title, description, canonical, image, config, extra_json_ld=detail_json_ld).replace("{ASSET_PREFIX}", "../")
    media = record["media"]
    assert isinstance(media, list)
    gallery = render_media_gallery(record)
    if not gallery:
        gallery = '<div class="empty-media">No public media reference was captured for this record.</div>'
    metric_items = "".join(
        f'<div><strong>{esc(format_number(value))}</strong><span>{esc(label)}</span></div>'
        for field, label in METRIC_FIELDS
        for value in [record["metrics"].get(field)]
        if value is not None
    )
    if not metric_items:
        metric_items = '<div><strong>NULL</strong><span>no public count</span></div>'
    refs = record.get("refs")
    assert isinstance(refs, list)
    refs_html = "".join(f'<li><a href="{esc(ref, attribute=True)}" rel="noreferrer">{esc(ref)}</a></li>' for ref in refs if valid_url(ref))
    references_section = (
        f'  <section class="detail-context"><div><p class="kicker">REFERENCES</p><h2>Linked evidence</h2></div><ul>{refs_html}</ul></section>'
        if refs_html
        else ""
    )
    listing_section = render_listing_evidence(record)
    command = install_command(record)
    source_action = (
        f'<div class="install-command"><code>{esc(command)}</code><button class="copy-install" type="button" data-install="{esc(command, attribute=True)}" aria-label="Copy install command">Copy</button></div><p class="detail-footnote">Source-declared command. Review the package and Registry Listing before running it.</p>'
        if command
        else f'<a class="source-entry" href="{esc(record["url"], attribute=True)}" rel="noreferrer">Open the public source page ↗</a>'
    )
    author = record["author"] or record["repo"] or record["platform_label"]
    return f"""{head}<body data-page="detail">
{nav_html('../')}
<main class="site-main detail-main">
  <div class="breadcrumbs"><a href="../">store</a><span>/</span><span>{esc(record['platform_label'])}</span><span>/</span><span>{esc(record['id'])}</span></div>
  <section class="detail-heading"><div><p class="kicker">{esc(record['platform_label'])} · {esc(record['category_label'])}</p><h1>{esc(record['title'])}</h1><p class="detail-author">{esc(str(author))} · {esc(record['item_type'])} · {esc('direct signal' if record['relevance'] == 'direct' else 'related signal')}</p></div><a class="button button-primary" href="{esc(record['url'], attribute=True)}" rel="noreferrer">Open source <span aria-hidden="true">↗</span></a></section>
  <section class="detail-grid"><div class="detail-primary"><p class="detail-description">{esc(record['description'])}</p><div class="install-panel"><p class="filter-label">SOURCE-DECLARED INSTALL</p>{source_action}</div><div class="detail-media"><div class="section-heading"><div><p class="kicker">MEDIA REFERENCES</p><h2>Captured in public view</h2></div><span>Local and external references · rights noted</span></div><div class="media-gallery">{gallery}</div></div></div><aside class="detail-sidebar"><div class="metric-grid">{metric_items}</div><div class="evidence-panel"><p class="filter-label">EVIDENCE</p><dl><div><dt>Registry ID</dt><dd>{esc(record['id'])}</dd></div><div><dt>Evidence dataset</dt><dd>{esc(evidence_dataset_version)}</dd></div><div><dt>First seen</dt><dd>{esc(date_label(record['first_seen_at']))}</dd></div><div><dt>Last seen</dt><dd>{esc(date_label(record['last_seen_at']))}</dd></div><div><dt>Metric source</dt><dd>{esc(record['metric_source'] or 'unreported')}</dd></div><div><dt>Metric observed</dt><dd>{esc(record['metric_observed_at'] or 'NULL')}</dd></div></dl></div><div class="evidence-panel"><p class="filter-label">PUBLIC URL</p><a class="break-link" href="{esc(record['url'], attribute=True)}" rel="noreferrer">{esc(record['url'])}</a></div></aside></section>
{listing_section}
  <section class="detail-context"><div><p class="kicker">CONTEXT</p><h2>Why it is here</h2></div><p>{esc(record['description'])}</p></section>
{references_section}
  <p class="detail-footnote">Evidence updated {esc(evidence_updated_at)}. Interaction numbers are platform-native snapshots; the evidence panel records the metric source and observation time. NULL means the public page did not expose a number at collection time.</p>
</main>
{footer_html('../', data_path=config["public_database_url"])}
</body></html>"""


def table_page(
    title: str,
    heading: str,
    intro: str,
    body: str,
    config: dict[str, str],
    *,
    prefix: str = "",
    script_path: str | None = None,
) -> str:
    """Render a compact HTML projection for a generated Markdown view."""

    site_url = config["site_url"].rstrip("/")
    canonical = site_url + "/" + title.lower() + ".html"
    head = page_head(title, intro, canonical, f"{site_url}/media/screenshots/official.png", config).replace("{ASSET_PREFIX}", prefix)
    home_prefix = prefix or "./"
    script = (
        f'\n<script src="{esc(script_path, attribute=True)}" defer></script>'
        if script_path
        else ""
    )
    return f"""{head}<body>
{nav_html(home_prefix)}
<main class="site-main table-main"><div class="breadcrumbs"><a href="{home_prefix}">store</a><span>/</span><span>{esc(heading)}</span></div><section class="page-intro"><p class="kicker">PUBLIC PROJECTION · GENERATED FROM SQLITE</p><h1>{esc(heading)}</h1><p>{esc(intro)}</p></section>{body}</main>
{footer_html(prefix, data_path=config["public_database_url"])}{script}
</body></html>"""


def load_timeline_trends(db: sqlite3.Connection) -> dict[int, dict[str, object]]:
    """Compare the newest two native-metric snapshots from one source per item."""

    metric_columns = ", ".join(field for field, _label in METRIC_FIELDS)
    rows = db.execute(
        f"""
        SELECT id, item_id, observed_at, metric_source, {metric_columns}
        FROM metrics
        ORDER BY item_id, metric_source, observed_at DESC, id DESC
        """
    ).fetchall()
    histories: dict[tuple[int, str], list[sqlite3.Row]] = {}
    for row in rows:
        key = (int(row["item_id"]), str(row["metric_source"]))
        history = histories.setdefault(key, [])
        if len(history) < 2:
            history.append(row)

    pairs: dict[int, list[tuple[sqlite3.Row, sqlite3.Row]]] = {}
    for (item_id, _source), history in histories.items():
        if len(history) == 2:
            pairs.setdefault(item_id, []).append((history[0], history[1]))

    trends: dict[int, dict[str, object]] = {}
    for item_id, item_pairs in pairs.items():
        current, previous = max(
            item_pairs,
            key=lambda pair: (str(pair[0]["observed_at"]), str(pair[0]["metric_source"])),
        )
        selected = next(
            (
                (field, label, int(current[field]), int(previous[field]))
                for field, label in METRIC_FIELDS
                if current[field] is not None and previous[field] is not None
            ),
            None,
        )
        if selected is None:
            continue
        field, label, current_value, previous_value = selected
        delta = current_value - previous_value
        percent = round(delta * 100 / previous_value, 1) if previous_value else None
        start = dt.datetime.fromisoformat(str(previous["observed_at"]).replace("Z", "+00:00"))
        end = dt.datetime.fromisoformat(str(current["observed_at"]).replace("Z", "+00:00"))
        trends[item_id] = {
            "hasEvidence": True,
            "metric": field,
            "metricLabel": label,
            "current": current_value,
            "previous": previous_value,
            "delta": delta,
            "percent": percent,
            "from": str(previous["observed_at"]),
            "to": str(current["observed_at"]),
            "elapsedHours": round((end - start).total_seconds() / 3600, 1),
            "source": str(current["metric_source"]),
        }
    return trends


def render_timeline_page(db: sqlite3.Connection, dataset_version: str, config: dict[str, str]) -> str:
    """Render a crawlable, filterable Timeline projection."""

    rows = db.execute(
        """
        SELECT i.id AS item_id, ir.id AS registry_id, ir.rank,
               i.platform, i.item_type, i.title, i.author, i.category,
               COALESCE(i.published_at, i.first_seen_at) AS event_at,
               i.published_label
        FROM items AS i
        JOIN index_records AS ir ON ir.item_id = i.id
        ORDER BY event_at DESC, i.platform, i.title
        """
    ).fetchall()
    trends = load_timeline_trends(db)
    records = [
        {
            "id": str(row["registry_id"]),
            "rank": int(row["rank"]),
            "eventAt": str(row["event_at"] or ""),
            "timeLabel": str(row["published_label"] or date_label(row["event_at"]) or "未知"),
            "source": str(row["platform"]),
            "sourceLabel": str(PLATFORM_LABELS.get(str(row["platform"]), row["platform"])),
            "itemType": str(row["item_type"] or ""),
            "title": str(row["title"] or "Untitled"),
            "author": str(row["author"] or "—"),
            "category": str(row["category"]),
            "categoryLabel": str(CATEGORY_LABELS.get(str(row["category"]), row["category"])),
            "trend": trends.get(int(row["item_id"]), {"hasEvidence": False}),
        }
        for row in rows
    ]

    def timeline_row(record: dict[str, object]) -> str:
        """Render one crawlable Timeline table row."""

        trend = record["trend"]
        assert isinstance(trend, dict)
        if trend.get("hasEvidence"):
            delta = int(trend["delta"])
            percent = trend["percent"]
            percent_label = f"{float(percent):+.1f}%" if percent is not None else "rate n/a"
            hours = float(trend["elapsedHours"])
            hours_label = f"{hours:g}h"
            signal = (
                '<span class="timeline-trend-signal">'
                f'<strong>{esc(trend["metricLabel"])} {format_number(trend["current"])}</strong>'
                f'<span>{delta:+,} · {percent_label} · {hours_label}</span>'
                f'<small>{esc(trend["source"])} · {esc(date_label(trend["from"]))} → {esc(date_label(trend["to"]))}</small>'
                "</span>"
            )
        else:
            signal = '<span class="timeline-no-trend">暂无趋势证据</span>'
        return (
            f'<tr class="timeline-row" data-record-id="{esc(record["id"], attribute=True)}">'
            f'<td class="timeline-rank">#{int(record["rank"]):,}</td>'
            f'<td><time datetime="{esc(record["eventAt"], attribute=True)}">{esc(record["timeLabel"])}</time></td>'
            f'<td>{esc(record["sourceLabel"])}</td>'
            f'<td><a href="skills/{esc(record["id"], attribute=True)}.html">{esc(record["title"])}</a>'
            f'<small>{esc(record["author"])} · {esc(record["itemType"])}</small></td>'
            f"<td>{signal}</td>"
            f'<td>{esc(record["categoryLabel"])}</td></tr>'
        )

    body_rows = "".join(timeline_row(record) for record in records[:100])
    source_options = "".join(
        f'<option value="{esc(source, attribute=True)}">{esc(PLATFORM_LABELS.get(source, source))}</option>'
        for source in sorted({str(record["source"]) for record in records})
    )
    category_options = "".join(
        f'<option value="{esc(category, attribute=True)}">{esc(CATEGORY_LABELS.get(category, category))}</option>'
        for category in sorted({str(record["category"]) for record in records})
    )
    reference_time = latest_run(db)[1]
    timeline_data = json.dumps(
        {"referenceTime": reference_time, "records": records},
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("<", "\\u003c")
    intro = "按时间、Registry 影响力或有历史证据的原生指标变化浏览公开生态记录。"
    site_url = config["site_url"].rstrip("/")
    head = page_head(
        "Timeline Analytics — deeplugin.store",
        intro,
        site_url + "/timeline.html",
        f"{site_url}/media/screenshots/official.png",
        config,
    ).replace("{ASSET_PREFIX}", "")
    return f"""{head}<body data-page="timeline">
{nav_html('./')}
<main class="site-main table-main timeline-page"><div class="breadcrumbs"><a href="./">store</a><span>/</span><span>Timeline</span></div>
  <section class="page-intro timeline-intro"><p class="kicker">PUBLIC PROJECTION · GENERATED FROM SQLITE</p><h1>Timeline Analytics</h1><p>{esc(intro)}</p><p class="timeline-method">Trend 只比较同一记录、同一 metric source 的连续两次平台原生指标；不把 stars、likes、views 或 points 相加。</p></section>
  <section class="timeline-browser" aria-label="Timeline filters">
    <div class="timeline-sort" role="group" aria-label="Sort records"><button class="is-selected" type="button" data-timeline-sort="time">时间线</button><button type="button" data-timeline-sort="influence">影响力</button><button type="button" data-timeline-sort="trend">趋势</button></div>
    <div class="timeline-filters">
      <label class="search-field timeline-search"><span aria-hidden="true">⌕</span><input id="timeline-search" type="search" placeholder="搜索记录、作者、来源…" autocomplete="off"></label>
      <label><span>来源</span><select id="timeline-source"><option value="all">全部来源</option>{source_options}</select></label>
      <label><span>分类</span><select id="timeline-category"><option value="all">全部分类</option>{category_options}</select></label>
      <label><span>时间范围</span><select id="timeline-window"><option value="1">24 小时</option><option value="7">7 天</option><option value="30" selected>30 天</option><option value="365">1 年</option><option value="all">全部时间</option></select></label>
      <label class="timeline-check"><input id="timeline-trending-only" type="checkbox"><span>仅显示有趋势证据</span></label>
    </div>
    <div class="timeline-status"><p id="timeline-summary"><strong>{len(records):,}</strong> records · 时间线排序</p><p>reference {esc(reference_time)} · dataset {esc(dataset_version)}</p></div>
  </section>
  <section class="timeline-trending" aria-labelledby="trending-heading"><div class="section-heading"><div><p class="kicker">MEASURED MOMENTUM</p><h2 id="trending-heading">Trending now</h2></div><span>同来源连续快照中的正增长证据</span></div><div class="timeline-trend-grid" id="timeline-trend-grid"><p class="timeline-empty-trend">当前数据中暂无可展示的正增长证据。</p></div></section>
  <section class="table-section timeline-results"><div class="table-scroll"><table class="data-table timeline-table"><thead><tr><th aria-sort="none"><button class="timeline-table-sort" type="button" data-timeline-sort="influence">Rank</button></th><th aria-sort="descending"><button class="timeline-table-sort is-selected" type="button" data-timeline-sort="time" data-sort-direction="desc">Time</button></th><th aria-sort="none"><button class="timeline-table-sort" type="button" data-timeline-sort="source">Source</button></th><th aria-sort="none"><button class="timeline-table-sort" type="button" data-timeline-sort="record">Record</button></th><th aria-sort="none"><button class="timeline-table-sort" type="button" data-timeline-sort="trend">Native signal / Trend</button></th><th aria-sort="none"><button class="timeline-table-sort" type="button" data-timeline-sort="topic">Topic</button></th></tr></thead><tbody id="timeline-body">{body_rows}</tbody></table></div><p class="no-results" id="timeline-empty" hidden>没有记录符合当前筛选条件。</p><button class="timeline-more" id="timeline-more" type="button"{' hidden' if len(records) <= 100 else ''}>Load 100 more</button></section>
</main>
{footer_html(data_path=config["public_database_url"])}
<script type="application/json" id="timeline-data">{timeline_data}</script>
<script src="assets/timeline.js" defer></script>
</body></html>"""


def render_categories_page(records: list[dict[str, object]], config: dict[str, str]) -> str:
    """Render category shelves in the same card language as the store."""

    sections = []
    for category in sorted({str(record["category"]) for record in records}):
        category_records = [record for record in records if record["category"] == category]
        category_records.sort(key=lambda record: (-int(record["metric_score"]), int(record["rank"])))
        cards = "".join(card_html(record) for record in category_records[:18])
        sections.append(f'<section class="category-shelf"><div class="section-heading"><div><p class="kicker">TOPIC</p><h2>{esc(CATEGORY_LABELS.get(category, category))}</h2></div><span>{len(category_records):,} records</span></div><div class="catalog-grid">{cards}</div></section>')
    return table_page("categories", "Topics", "启发式分类用于浏览，不是质量背书；每条记录仍回到公开来源核验。", "".join(sections), config)


def directory_records(records: list[dict[str, object]]) -> list[dict[str, object]]:
    """Select public aggregation, marketplace, and discovery records."""

    terms = ("awesome", "market", "store", "hub", "find", "directory", "registry", "catalog", "index")
    result = []
    for record in records:
        item_type = str(record["item_type"])
        is_repository = record["platform"] == "github" and item_type in {"repository", "source-repository"}
        is_website = record["platform"] in {"web", "official"} and item_type in {"website", "directory", "marketplace", "index"}
        public_label = f'{record["title"]} {urlparse(str(record["url"])).path}'.lower()
        if (
            record["category"] == "index-and-marketplace"
            and record["relevance"] == "direct"
            and (is_repository or is_website)
            and any(term in public_label for term in terms)
        ):
            result.append(record)
    result.sort(key=lambda record: (-int(record["metric_score"]), int(record["rank"])))
    return result


def render_directories_page(records: list[dict[str, object]], config: dict[str, str]) -> str:
    """Render other public aggregation projects and discovery sites."""

    directories = directory_records(records)
    cards = "".join(card_html(record) for record in directories)
    body = f'<section class="category-shelf"><div class="section-heading"><div><p class="kicker">COMMUNITY PROJECTS</p><h2>GitHub directories, markets, and discovery tools</h2></div><span>{len(directories):,} records</span></div><div class="catalog-grid">{cards}</div></section>'
    return table_page("directories", "Other directories & sites", "浏览社区维护的插件目录、市场、发现工具与网站；每个项目和站内其他记录一样展示公开指标、简介和访问入口。", body, config)


def render_sources_page(db: sqlite3.Connection, config: dict[str, str]) -> str:
    """Render public platform provenance without internal monitoring targets."""

    rows = db.execute(
        """
        SELECT s.platform, s.display_name, s.base_url, s.collection_mode, s.terms_url,
               (SELECT COUNT(*) FROM items AS i WHERE i.platform = s.platform) AS record_count,
               (SELECT COUNT(*) FROM observations AS o WHERE o.source_id = s.id) AS observation_count,
               (SELECT COUNT(DISTINCT o.raw_snapshot_id) FROM observations AS o WHERE o.source_id = s.id) AS raw_snapshot_count,
               COALESCE(
                   (SELECT MAX(o.collected_at) FROM observations AS o WHERE o.source_id = s.id),
                   (SELECT MAX(i.last_seen_at) FROM items AS i WHERE i.platform = s.platform)
               ) AS last_observed_at
        FROM sources AS s
        ORDER BY record_count DESC, s.platform
        """
    ).fetchall()
    body_rows = []
    for row in rows:
        source_label = esc(row["display_name"])
        source_link = f'<a href="{esc(row["base_url"], attribute=True)}" rel="noreferrer">{source_label}</a>' if valid_url(row["base_url"]) else source_label
        policy_link = f'<a href="{esc(row["terms_url"], attribute=True)}" rel="noreferrer">policy ↗</a>' if valid_url(row["terms_url"]) else "—"
        body_rows.append(
            f'<tr><td>{source_link}<br><code>{esc(row["platform"])}</code></td><td>{esc(row["collection_mode"])}</td><td>{int(row["record_count"]):,}</td><td>{int(row["observation_count"]):,}</td><td>{int(row["raw_snapshot_count"]):,}</td><td>{esc(date_label(row["last_observed_at"]))}</td><td>{policy_link}</td></tr>'
        )
    body = f'<section class="table-section"><div class="table-caption"><strong>{len(rows):,}</strong> public platforms · internal monitoring targets are intentionally excluded</div><div class="table-scroll"><table class="data-table"><thead><tr><th>Platform</th><th>Collection mode</th><th>Records</th><th>Observations</th><th>Raw snapshots</th><th>Last observed</th><th>Policy</th></tr></thead><tbody>{"".join(body_rows)}</tbody></table></div></section>'
    return table_page("sources", "Sources & provenance", "公开展示来源平台、允许的采集方式、记录量、原始快照量和最近观测时间；不公开本站内部监控仓库或查询目标。", body, config)


def render_register_page(config: dict[str, str]) -> str:
    """Render the public human registration entry point."""

    repository = "https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin"
    site_url = config["site_url"].rstrip("/")
    agent_guide_url = f"{site_url}/register-agent.html"
    agent_source_url = (
        "https://raw.githubusercontent.com/Shiyao-Huang/awesome-deepseek-harness-plugin/"
        "main/docs/register-agent.md"
    )
    agent_request = f"""Help me register a DeepSeek Harness plugin or public registry with deeplugin.store.

Read the complete Agent protocol first:
{agent_guide_url}

Read the source guide and public data contracts:
{agent_source_url}
{site_url}/data/market-registry.schema.json
{site_url}/data/market-registry.json

Inspect the public repository, package metadata, release/version evidence, and exact DeepSeek Harness installation documentation. Deduplicate by normalized install spec, use the narrowest registration route, preserve attributable facts, keep missing values NULL, and set contributor verification to false.

Do not install anything, open a pull request, or write to an external service until I explicitly approve. If I have not supplied the plugin or registry URL, ask for it first. Then show me the proposed Listing, source evidence, changed files, and validation plan."""
    body = f'''<section class="guide-section"><div class="guide-primary"><p class="kicker">TWO REGISTRATION ROUTES</p><h2>Add one plugin or connect a public registry</h2><div class="agent-handoff"><div class="agent-handoff-copy"><p class="filter-label">AGENT HANDOFF</p><strong>Give this registration task to your Agent.</strong><span>Copies the protocol URL, public contracts, workflow, and approval limits as one ready-to-run request.</span><code>{esc(agent_guide_url)}</code></div><div class="agent-handoff-actions"><button class="agent-handoff-button copy-install" type="button" data-install="{esc(agent_request, attribute=True)}" aria-label="Copy the Agent registration guide and task" aria-live="polite">Copy for Agent</button><a href="register-agent.html">Open Agent guide ↗</a></div></div><ol class="guide-steps"><li><strong>One plugin</strong><span>Add a contract-v2 Listing to <a href="{repository}/blob/main/registry/plugins.json">registry/plugins.json ↗</a>.</span></li><li><strong>Another registry</strong><span>Add its public repository and selected registry path or HTTPS URL to <a href="{repository}/blob/main/config/sources.json">config/sources.json ↗</a>.</span></li><li><strong>Next observation</strong><span>After merge, the next successful two-hour run preserves raw evidence, writes SQLite history, and rebuilds the market.</span></li></ol></div><aside class="guide-aside"><p class="filter-label">AUTHORITATIVE REFERENCES</p><a href="register-agent.html">Agent registration guide ↗</a><a href="{repository}/blob/main/docs/register.md">Human field guide ↗</a><a href="data/market-registry.schema.json">Contract-v2 JSON Schema ↗</a><a href="data/market-registry.json">Current public registry ↗</a><a href="{repository}/compare">Open a pull request ↗</a></aside></section><section class="guide-rules"><p><strong>Identity</strong><span>Normalized install spec, not name or homepage.</span></p><p><strong>Missing data</strong><span>Use NULL; never estimate stars, versions, or metrics.</span></p><p><strong>Verification</strong><span>Source-attributed claim, never a security endorsement.</span></p><p><strong>Installation</strong><span>Plans require explicit user confirmation.</span></p></section>'''
    return table_page(
        "register",
        "Register a plugin",
        "提交可追溯、可验证、可去重的 DeepSeek Harness 插件 Listing；单个插件和第三方 registry 都有明确入口。",
        body,
        config,
        script_path="assets/store.js",
    )


def render_register_agent_page(config: dict[str, str]) -> str:
    """Render the public Agent registration workflow."""

    repository = "https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin"
    body = f'''<section class="guide-section"><div class="guide-primary"><p class="kicker">AGENT PROTOCOL</p><h2>Inspect, deduplicate, validate, then ask.</h2><ol class="guide-steps"><li><strong>Inspect evidence</strong><span>Read package metadata, release/version evidence, exact install documentation, and the public repository.</span></li><li><strong>Resolve identity</strong><span>Search the current registry by normalized npm or GitHub install spec before creating a Listing.</span></li><li><strong>Record facts</strong><span>Use public attributed values, keep missing values NULL, and set contributor verification to false.</span></li><li><strong>Validate</strong><span>Update source count/date, run repository checks, and inspect the generated diff.</span></li><li><strong>Request authority</strong><span>Show the Listing and evidence before opening a pull request. Registration never authorizes installation.</span></li></ol></div><aside class="guide-aside"><p class="filter-label">AGENT INPUTS</p><a href="{repository}/blob/main/docs/register-agent.md">Complete Agent protocol ↗</a><a href="{repository}/blob/main/docs/register.md">Normative field guide ↗</a><a href="data/market-registry.schema.json">JSON Schema ↗</a><a href="data/market-registry.json">Deduplication registry ↗</a></aside></section><section class="guide-rules"><p><strong>Allowed specs</strong><span>npm package or github:owner/repository#path:/plugin.</span></p><p><strong>Rejected specs</strong><span>Commands, flags, branches, URLs, and local paths.</span></p><p><strong>Pull requests</strong><span>External writes require explicit user authorization.</span></p><p><strong>Install plans</strong><span>Known registry ids only; requiresConfirmation is always true.</span></p></section>'''
    return table_page(
        "register-agent",
        "Agent registration protocol",
        "Agent 应先核验来源和安装身份，再构造 Listing；创建 PR 与执行安装是两个独立且都需要授权的动作。",
        body,
        config,
    )


def publish_local_media() -> None:
    """Mirror rights-cleared local media into the GitHub Pages source tree."""

    if PUBLISHED_MEDIA.exists():
        shutil.rmtree(PUBLISHED_MEDIA)
    shutil.copytree(MEDIA, PUBLISHED_MEDIA)


def render_sitemap(records: list[dict[str, object]], site_url: str) -> str:
    """Render page, image, and complete video evidence for search crawlers."""

    static_paths = (
        "/",
        "/market.html",
        "/report.html",
        "/timeline.html",
        "/categories.html",
        "/directories.html",
        "/sources.html",
        "/forks.html",
        "/register.html",
        "/register-agent.html",
    )
    entries = [f"  <url><loc>{esc(site_url + path)}</loc></url>" for path in static_paths]
    for record in records:
        canonical = f"{site_url}/skills/{record['id']}.html"
        title = compact_text(record.get("title"), 100) or "DeepSeek Harness ecosystem video"
        description = compact_text(record.get("description"), 2048) or title
        parts = [f"  <url><loc>{esc(canonical)}</loc>"]
        media = record.get("media")
        image_urls: list[str] = []
        if isinstance(media, list):
            for asset in media:
                if not isinstance(asset, dict):
                    continue
                kind = str(asset.get("kind") or "")
                image_url = asset.get("thumbnail_url")
                if not valid_media_reference(image_url) and kind in {"image", "image-local", "thumbnail", "avatar", "picture"}:
                    image_url = asset.get("url")
                if valid_media_reference(image_url):
                    absolute_image_url = absolute_media_url(image_url, site_url)
                    if absolute_image_url not in image_urls:
                        image_urls.append(absolute_image_url)
        for image_url in image_urls:
            parts.append(f"<image:image><image:loc>{esc(image_url)}</image:loc></image:image>")
        video = video_structured_data(record, canonical, description, site_url)
        if video:
            thumbnail = video["thumbnailUrl"]
            assert isinstance(thumbnail, list) and thumbnail
            parts.append(
                "<video:video>"
                f"<video:thumbnail_loc>{esc(thumbnail[0])}</video:thumbnail_loc>"
                f"<video:title>{esc(title)}</video:title>"
                f"<video:description>{esc(description)}</video:description>"
                f"<video:player_loc>{esc(video['embedUrl'])}</video:player_loc>"
                f"<video:publication_date>{esc(video['uploadDate'])}</video:publication_date>"
                "</video:video>"
            )
        parts.append("</url>")
        entries.append("".join(parts))
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" '
        'xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )


def write_store_site(db: sqlite3.Connection, dataset_version: str, generated_at: str) -> None:
    """Write the homepage, detail pages, catalog JSON, and SEO files."""

    config = read_config()
    records = load_records(db)
    market_registry = load_market_registry()
    for record in records:
        record["dataset_version"] = dataset_version
    platform_counts = db.execute("SELECT platform, COUNT(*) AS count FROM items GROUP BY platform ORDER BY count DESC, platform").fetchall()
    category_counts = db.execute("SELECT category, COUNT(*) AS count FROM items GROUP BY category ORDER BY count DESC, category").fetchall()
    DATA.mkdir(parents=True, exist_ok=True)
    SKILLS.mkdir(parents=True, exist_ok=True)
    publish_local_media()
    catalog = {
        "meta": {
            "dataset_version": dataset_version,
            "generated_at": generated_at,
            "site_url": config["site_url"],
            "record_count": len(records),
        },
        "platforms": [{"key": row["platform"], "label": PLATFORM_LABELS.get(str(row["platform"]), row["platform"]), "count": row["count"]} for row in platform_counts],
        "categories": [{"key": row["category"], "label": CATEGORY_LABELS.get(str(row["category"]), row["category"]), "count": row["count"]} for row in category_counts],
        "items": records,
    }
    (DATA / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    (DOCS / "index.html").write_text(render_home(records, dataset_version, generated_at, config, platform_counts, category_counts, market_registry), encoding="utf-8")
    (DOCS / "market.html").write_text(render_market_page(market_registry, config), encoding="utf-8")
    (DOCS / "timeline.html").write_text(render_timeline_page(db, dataset_version, config), encoding="utf-8")
    (DOCS / "categories.html").write_text(render_categories_page(records, config), encoding="utf-8")
    (DOCS / "directories.html").write_text(render_directories_page(records, config), encoding="utf-8")
    (DOCS / "sources.html").write_text(render_sources_page(db, config), encoding="utf-8")
    (DOCS / "register.html").write_text(render_register_page(config), encoding="utf-8")
    (DOCS / "register-agent.html").write_text(render_register_agent_page(config), encoding="utf-8")
    for record in records:
        (SKILLS / f"{record['id']}.html").write_text(render_detail(record, dataset_version, generated_at, config), encoding="utf-8")
    site_url = config["site_url"].rstrip("/")
    sitemap = render_sitemap(records, site_url)
    (DOCS / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n", encoding="utf-8")
    (DOCS / "CNAME").write_text(urlparse(site_url).netloc + "\n", encoding="utf-8")
    (DOCS / ".nojekyll").write_text("\n", encoding="utf-8")
