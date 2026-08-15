#!/usr/bin/env python3
"""Build the static skills-store projection from the authoritative SQLite database."""

from __future__ import annotations

import html
import json
import re
import sqlite3
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
DOCS = ROOT / "docs"
DATA = DOCS / "data"
SKILLS = DOCS / "skills"
CONFIG_PATH = ROOT / "config" / "site.json"

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


def connection() -> sqlite3.Connection:
    """Open the generated database with named result columns."""

    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def read_config() -> dict[str, str]:
    """Read deployment and canonical URL settings."""

    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


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
             LIMIT 1) AS metric_source
        FROM items AS i
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
        if not valid_url(media["url"]):
            continue
        media_by_item.setdefault(int(media["item_id"]), []).append(
            {
                "kind": media["kind"],
                "url": media["url"],
                "thumbnail_url": media["thumbnail_url"] if valid_url(media["thumbnail_url"]) else None,
                "alt": media["alt_text"] or "Public media reference",
                "rights_note": media["rights_note"],
            }
        )

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
                "refs": [ref for ref in refs if valid_url(ref)],
            }
        )
    return records


def latest_run(db: sqlite3.Connection) -> tuple[str, str]:
    """Read the latest successful dataset version and completion time."""

    row = db.execute(
        """
        SELECT dataset_version, COALESCE(finished_at, started_at)
        FROM collection_runs
        WHERE trigger <> 'legacy-migration'
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
        candidate = asset.get("thumbnail_url") or asset.get("url")
        if valid_url(candidate):
            return str(candidate)
    return None


def install_command(record: dict[str, object]) -> str | None:
    """Return the documented DSH install command for a clearly named plugin repo."""

    if record["platform"] != "github" or not record["repo"]:
        return None
    repository = str(record["repo"])
    package_name = repository.rsplit("/", 1)[-1]
    return f"dsh plugin --profile web add {package_name}" if package_name.startswith("dsh-") else None


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
        f'<img src="{esc(image, attribute=True)}" alt="" loading="lazy">'
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
        cover = f'<img src="{esc(image, attribute=True)}" alt="" loading="lazy">' if image else '<span class="cover-initial">DS</span>'
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


def footer_html(prefix: str = "", *, data_path: str, readme_path: str | None = None, seo_path: str | None = None) -> str:
    """Render the provenance and deployment footer."""

    readme_path = readme_path or ("../README.md" if not prefix else "../../README.md")
    seo_path = seo_path or ("seo.md" if not prefix else "../seo.md")
    return f"""<footer class="site-footer"><div><strong>dsh store</strong><p>A public, dated directory for the DeepSeek Harness plugin ecosystem.</p></div><div><a href="{readme_path}">Collection rules</a><a href="{data_path}">SQLite</a><a href="{seo_path}">SEO notes</a></div><p class="footer-note">Public metadata only. Platform counts stay native and are never added together.</p></footer>"""


def render_home(records: list[dict[str, object]], dataset_version: str, generated_at: str, config: dict[str, str], platform_counts: list[sqlite3.Row], category_counts: list[sqlite3.Row]) -> str:
    """Render the store-style directory homepage."""

    category_html, platform_html = filter_buttons(records)
    cards = "".join(card_html(record) for record in records)
    site_url = config["site_url"].rstrip("/")
    image = f"{site_url}/media/screenshots/official.png"
    item_list = [
        {"@type": "ListItem", "position": index, "url": f"{site_url}/skills/{record['id']}.html", "name": record["title"]}
        for index, record in enumerate(records[:24], 1)
    ]
    head = page_head(
        "dsh store — DeepSeek Harness plugin ecosystem",
        config["description"],
        site_url + "/",
        image,
        config,
        extra_json_ld={"@type": "CollectionPage", "mainEntity": {"@type": "ItemList", "itemListElement": item_list}},
    ).replace("{ASSET_PREFIX}", "")
    stats = {
        "records": len(records),
        "platforms": len(platform_counts),
        "media": sum(1 for record in records if record["media"]),
        "direct": sum(1 for record in records if record["relevance"] == "direct"),
    }
    platform_summary = "".join(
        f'<span><b>{row["count"]:,}</b> {esc(PLATFORM_LABELS.get(str(row["platform"]), row["platform"]))}</span>'
        for row in platform_counts[:6]
    )
    projects = hot_records(records, "github")
    posts = hot_records(records)
    hot_tables = signal_table(projects, "GitHub projects people are using", "PROJECTS · STARS", "插件系统内的仓库按 GitHub stars 排序；Use 只对明确的 dsh-* 仓库提供安装命令。", "Open") + signal_table(posts, "Posts and videos people are sharing", "POSTS · NATIVE SIGNAL", "帖子、文章和视频按各自平台的公开指标排序；数字不跨平台相加。", "Open")
    return f"""{head}<body data-page="home">
{nav_html()}
<main class="site-main">
  <section class="hero-store">
    <div class="hero-copy"><p class="kicker">DSH PLUGIN SIGNALS · {esc(dataset_version)}</p><h1>See what is hot.<br><em>Use what works.</em></h1><p class="hero-lede">当前插件系统里的热门 GitHub 项目、帖子和视频。每条记录都能回到源头，明确的 dsh 插件可以直接复制安装命令。</p><div class="hero-actions"><a class="button button-primary" href="#hot">View hot signals <span aria-hidden="true">↓</span></a><a class="button button-quiet" href="#directory">Browse all <span aria-hidden="true">↓</span></a></div></div>
    <div class="hero-panel"><div class="panel-label">LATEST SNAPSHOT</div><strong>{esc(date_label(generated_at))}</strong><p>Native counters only. Missing values stay NULL.</p><div class="signal-line"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div></div>
  </section>
  <section class="stats-row" aria-label="Dataset statistics"><div><strong>{stats['records']:,}</strong><span>records</span></div><div><strong>{stats['direct']:,}</strong><span>direct signals</span></div><div><strong>{stats['platforms']}</strong><span>platforms</span></div><div><strong>{stats['media']:,}</strong><span>with media</span></div></section>
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


def render_detail(record: dict[str, object], dataset_version: str, generated_at: str, config: dict[str, str]) -> str:
    """Render a static, crawlable detail page for one store record."""

    site_url = config["site_url"].rstrip("/")
    canonical = f"{site_url}/skills/{record['id']}.html"
    title = f"{record['title']} — dsh store"
    description = compact_text(record["description"], 180) or "Public DeepSeek Harness ecosystem record."
    image = record_image(record) or f"{site_url}/media/screenshots/official.png"
    detail_json_ld = {"@type": "CreativeWork", "name": record["title"], "url": canonical, "isPartOf": {"@type": "WebSite", "url": site_url + "/"}}
    head = page_head(title, description, canonical, image, config, extra_json_ld=detail_json_ld).replace("{ASSET_PREFIX}", "../")
    media = record["media"]
    assert isinstance(media, list)
    gallery = "".join(
        f'<a href="{esc(asset["url"], attribute=True)}" rel="noreferrer"><img src="{esc(asset.get("thumbnail_url") or asset["url"], attribute=True)}" alt="{esc(asset.get("alt"), attribute=True)}" loading="lazy"></a>'
        for asset in media
        if valid_url(asset.get("url"))
    )
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
    command = install_command(record)
    source_action = (
        f'<div class="install-command"><code>{esc(command)}</code><button class="copy-install" type="button" data-install="{esc(command, attribute=True)}" aria-label="Copy install command">Copy</button></div>'
        if command
        else f'<a class="source-entry" href="{esc(record["url"], attribute=True)}" rel="noreferrer">Open the public source page ↗</a>'
    )
    author = record["author"] or record["repo"] or record["platform_label"]
    return f"""{head}<body data-page="detail">
{nav_html('../')}
<main class="site-main detail-main">
  <div class="breadcrumbs"><a href="../">store</a><span>/</span><span>{esc(record['platform_label'])}</span><span>/</span><span>{esc(record['id'])}</span></div>
  <section class="detail-heading"><div><p class="kicker">{esc(record['platform_label'])} · {esc(record['category_label'])}</p><h1>{esc(record['title'])}</h1><p class="detail-author">{esc(str(author))} · {esc(record['item_type'])} · {esc('direct signal' if record['relevance'] == 'direct' else 'related signal')}</p></div><a class="button button-primary" href="{esc(record['url'], attribute=True)}" rel="noreferrer">Open source <span aria-hidden="true">↗</span></a></section>
  <section class="detail-grid"><div class="detail-primary"><p class="detail-description">{esc(record['description'])}</p><div class="install-panel"><p class="filter-label">SOURCE ENTRY</p>{source_action}</div><div class="detail-media"><div class="section-heading"><div><p class="kicker">MEDIA REFERENCES</p><h2>Captured in public view</h2></div><span>External URLs only</span></div><div class="media-gallery">{gallery}</div></div></div><aside class="detail-sidebar"><div class="metric-grid">{metric_items}</div><div class="evidence-panel"><p class="filter-label">EVIDENCE</p><dl><div><dt>Registry ID</dt><dd>{esc(record['id'])}</dd></div><div><dt>Dataset</dt><dd>{esc(dataset_version)}</dd></div><div><dt>First seen</dt><dd>{esc(date_label(record['first_seen_at']))}</dd></div><div><dt>Last seen</dt><dd>{esc(date_label(record['last_seen_at']))}</dd></div><div><dt>Metric source</dt><dd>{esc(record['metric_source'] or 'unreported')}</dd></div><div><dt>Metric observed</dt><dd>{esc(record['metric_observed_at'] or 'NULL')}</dd></div></dl></div><div class="evidence-panel"><p class="filter-label">PUBLIC URL</p><a class="break-link" href="{esc(record['url'], attribute=True)}" rel="noreferrer">{esc(record['url'])}</a></div></aside></section>
  <section class="detail-context"><div><p class="kicker">CONTEXT</p><h2>Why it is here</h2></div><p>{esc(record['description'])}</p></section>
{references_section}
  <p class="detail-footnote">Page generated {esc(generated_at)}. Interaction numbers are platform-native snapshots; the evidence panel records the metric source and observation time. NULL means the public page did not expose a number at collection time.</p>
</main>
{footer_html('../', data_path=config["public_database_url"])}
</body></html>"""


def table_page(title: str, heading: str, intro: str, body: str, config: dict[str, str], *, prefix: str = "") -> str:
    """Render a compact HTML projection for a generated Markdown view."""

    site_url = config["site_url"].rstrip("/")
    canonical = site_url + "/" + title.lower() + ".html"
    head = page_head(title, intro, canonical, f"{site_url}/media/screenshots/official.png", config).replace("{ASSET_PREFIX}", prefix)
    return f"""{head}<body>
{nav_html(prefix)}
<main class="site-main table-main"><div class="breadcrumbs"><a href="{prefix}">store</a><span>/</span><span>{esc(heading)}</span></div><section class="page-intro"><p class="kicker">PUBLIC PROJECTION · GENERATED FROM SQLITE</p><h1>{esc(heading)}</h1><p>{esc(intro)}</p></section>{body}</main>
{footer_html(prefix, data_path=config["public_database_url"])}
</body></html>"""


def render_timeline_page(db: sqlite3.Connection, dataset_version: str, config: dict[str, str]) -> str:
    """Render a crawlable chronology with links back to detail pages."""

    rows = db.execute(
        """
        SELECT i.id, i.platform, i.item_type, i.title, i.author, i.category,
               COALESCE(i.published_at, i.first_seen_at) AS event_at,
               i.published_label
        FROM items AS i
        ORDER BY event_at DESC, i.platform, i.title
        """
    ).fetchall()
    body_rows = "".join(
        f'<tr><td>{esc(row["published_label"] or str(row["event_at"] or "")[:10])}</td><td>{esc(PLATFORM_LABELS.get(str(row["platform"]), row["platform"]))}</td><td><a href="skills/id-{row["id"]}.html">{esc(row["title"] or "Untitled")}</a></td><td>{esc(row["author"] or "—")}</td><td>{esc(CATEGORY_LABELS.get(str(row["category"]), row["category"]))}</td></tr>'
        for row in rows
    )
    body = f'<section class="table-section"><div class="table-caption"><strong>{len(rows):,}</strong> records · dataset {esc(dataset_version)}</div><div class="table-scroll"><table class="data-table"><thead><tr><th>Time</th><th>Source</th><th>Record</th><th>Author</th><th>Topic</th></tr></thead><tbody>{body_rows}</tbody></table></div></section>'
    return table_page("timeline", "Timeline", "按发布日期和首次观测日期排序的公开生态记录。", body, config)


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


def write_store_site(db: sqlite3.Connection, dataset_version: str, generated_at: str) -> None:
    """Write the homepage, detail pages, catalog JSON, and SEO files."""

    config = read_config()
    records = load_records(db)
    for record in records:
        record["dataset_version"] = dataset_version
    platform_counts = db.execute("SELECT platform, COUNT(*) AS count FROM items GROUP BY platform ORDER BY count DESC, platform").fetchall()
    category_counts = db.execute("SELECT category, COUNT(*) AS count FROM items GROUP BY category ORDER BY count DESC, category").fetchall()
    DATA.mkdir(parents=True, exist_ok=True)
    SKILLS.mkdir(parents=True, exist_ok=True)
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
    (DOCS / "index.html").write_text(render_home(records, dataset_version, generated_at, config, platform_counts, category_counts), encoding="utf-8")
    (DOCS / "timeline.html").write_text(render_timeline_page(db, dataset_version, config), encoding="utf-8")
    (DOCS / "categories.html").write_text(render_categories_page(records, config), encoding="utf-8")
    (DOCS / "directories.html").write_text(render_directories_page(records, config), encoding="utf-8")
    (DOCS / "sources.html").write_text(render_sources_page(db, config), encoding="utf-8")
    for record in records:
        (SKILLS / f"{record['id']}.html").write_text(render_detail(record, dataset_version, generated_at, config), encoding="utf-8")
    site_url = config["site_url"].rstrip("/")
    sitemap_paths = ["/", "/report.html", "/timeline.html", "/categories.html", "/directories.html", "/sources.html", "/forks.html"] + [f"/skills/{record['id']}.html" for record in records]
    sitemap = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" + "\n".join(
        f"  <url><loc>{html.escape(site_url + path)}</loc></url>" for path in sitemap_paths
    ) + "\n</urlset>\n"
    (DOCS / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n", encoding="utf-8")
    (DOCS / "CNAME").write_text(urlparse(site_url).netloc + "\n", encoding="utf-8")
    (DOCS / ".nojekyll").write_text("\n", encoding="utf-8")
