#!/usr/bin/env python3
"""Refresh the data-backed landing section at the top of README.md."""

from __future__ import annotations

import html
import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
FORK_INDEX_PATH = ROOT / "docs" / "data" / "forks.json"
README_PATH = ROOT / "README.md"
CONFIG_PATH = ROOT / "config" / "site.json"
START = "<!-- landing:start -->"
END = "<!-- landing:end -->"
SNAPSHOT_START = "<!-- snapshot:start -->"
SNAPSHOT_END = "<!-- snapshot:end -->"
SITE_CONFIG = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
PUBLIC_DATABASE_URL = str(SITE_CONFIG["public_database_url"])
FULL_DATABASE_URL = str(SITE_CONFIG["full_database_url"])

PLATFORM_LABELS = {
    "github": "GitHub",
    "hacker_news": "Hacker News",
    "x": "X",
    "xiaohongshu": "小红书",
    "youtube": "YouTube",
    "bilibili": "哔哩哔哩",
    "wechat": "微信公众号",
    "web": "开放网页",
    "reddit": "Reddit",
    "official": "官方站",
    "linuxdo": "LINUX DO",
    "v2ex": "V2EX",
    "weibo": "微博",
    "zhihu": "知乎",
}

PRIMARY_METRICS = {
    "github": ("stars", "★ stars"),
    "hacker_news": ("points", "points"),
    "x": ("likes", "♥ likes"),
    "xiaohongshu": ("likes", "♥ likes"),
    "youtube": ("views", "views"),
    "bilibili": ("views", "views"),
}

PLATFORM_DESCRIPTIONS = {
    "github": "官方仓库、topic、社区索引候选和 stars/forks/issues",
    "x": "公开帖子、图片/视频链接和 replies/reposts/likes/views",
    "hacker_news": "精确短语搜索、points/comments 和讨论链接",
    "xiaohongshu": "搜索卡片、作者、点赞、缩略图和详情文本",
    "web": "文章、教程和报道的公开元数据与摘要",
    "youtube": "视频标题、频道、观看数和缩略图",
    "bilibili": "视频元数据、播放/点赞/投币/收藏/转发/弹幕/评论",
    "reddit": "公开讨论、分数、评论和正文证据",
    "linuxdo": "公开讨论页面和互动信息",
    "wechat": "公开文章、图像/视频外链和正文证据",
    "official": "官方页面和补充证据",
    "v2ex": "公开讨论页面和互动信息",
    "weibo": "公开页面和互动信息",
    "zhihu": "公开问题、回答和页面互动信息",
}


def connect() -> sqlite3.Connection:
    """Open the authoritative database with named result columns."""

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def clean(value: object) -> str:
    """Make one database value safe for a compact Markdown row."""

    return " ".join(str(value or "").split()).replace("|", "\\|")


def number(value: object) -> str:
    """Format an observed count without turning NULL into zero."""

    return "—" if value is None else f"{int(value):,}"


def link(title: object, url: object) -> str:
    """Render one external link from a captured canonical URL."""

    return f"[{clean(title)}]({html.escape(str(url or ''), quote=True)})"


def metric_text(row: sqlite3.Row) -> str:
    """Render only native metrics for one platform; never add platforms together."""

    platform = str(row["platform"])
    fields = [PRIMARY_METRICS[platform]] if platform in PRIMARY_METRICS else []
    fields.extend((field, label) for field, label in (("comments", "comments"), ("replies", "replies"), ("views", "views")) if field not in {item[0] for item in fields})
    observed = [f"{label} {number(row[field])}" for field, label in fields if row[field] is not None]
    return " · ".join(observed[:2]) or "no public counter"


def primary_value(row: sqlite3.Row) -> float:
    """Return a platform-local sort value for an attention signal."""

    field = PRIMARY_METRICS.get(str(row["platform"]), ("likes", "likes"))[0]
    value = row[field]
    return float(value) if value is not None else float(row["value_score"] or 0)


def rows(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    """Load records with their latest native metrics and value assessment."""

    return connection.execute(
        """
        SELECT i.id, i.platform, i.item_type, i.title, i.author, i.canonical_url,
               i.published_label, i.category, i.relevance, m.stars, m.likes, m.views, m.points,
               m.comments, m.replies, m.favorites, m.shares,
               v.value_score, v.value_band, v.confidence_score
        FROM items AS i
        LEFT JOIN v_latest_metrics AS m ON m.item_id = i.id
        LEFT JOIN v_current_value_matrix AS v ON v.item_id = i.id
        ORDER BY i.id
        """
    ).fetchall()


def find_record(records: list[sqlite3.Row], url: str) -> sqlite3.Row | None:
    """Find a stable featured record by canonical URL."""

    return next((row for row in records if row["canonical_url"] == url), None)


def attention_rows(records: list[sqlite3.Row]) -> list[sqlite3.Row]:
    """Select one high-attention direct record per media platform."""

    selected: list[sqlite3.Row] = []
    for platform in ("x", "youtube", "bilibili", "hacker_news", "xiaohongshu"):
        candidates = [row for row in records if row["platform"] == platform and row["relevance"] == "direct"]
        if candidates:
            selected.append(max(candidates, key=lambda row: (primary_value(row), float(row["value_score"] or 0))))
    return selected


def snapshot_block(connection: sqlite3.Connection) -> str:
    """Build the maintained snapshot summary below the landing section."""

    run = connection.execute(
        "SELECT dataset_version, COALESCE(finished_at, started_at) AS assessed_at FROM collection_runs WHERE trigger <> 'legacy-migration' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    counts = connection.execute(
        "SELECT COUNT(*) AS items, COUNT(DISTINCT platform) AS platforms FROM items"
    ).fetchone()
    metrics = connection.execute("SELECT COUNT(*) FROM metrics").fetchone()[0]
    media = connection.execute("SELECT COUNT(*) FROM media_assets").fetchone()[0]
    details = connection.execute("SELECT COUNT(*) FROM item_details").fetchone()[0]
    raw = connection.execute("SELECT COUNT(*) FROM raw_snapshots").fetchone()[0]
    platform_rows = connection.execute(
        "SELECT platform, COUNT(*) AS n FROM items GROUP BY platform ORDER BY n DESC, platform"
    ).fetchall()
    lines = [
        SNAPSHOT_START,
        f"公开查询 SQLite 当前包含 **{counts['items']:,} 条去重记录**、**{counts['platforms']} 个来源平台**、**{metrics:,} 条指标历史**、**{media:,} 个媒体资产引用**、**{details:,} 条详情记录**和 **{raw:,} 个去重 raw provenance**。当前批次 **{clean(run['dataset_version'] if run else 'unknown')}** 于 **{clean(run['assessed_at'] if run else 'unknown')}** 完成；价值矩阵为当前批次的 {counts['items']:,} 条记录提供六维评分。完整原始 JSON 位于压缩权威 SQLite；公开查询库保留 raw SHA-256、路径、字节数、采集时间和批次，并去除可由 `data/raw/` 或完整库恢复的重复 JSON blob。",
        "",
        "| 来源 | 去重记录 | 采集内容 |",
        "| --- | ---: | --- |",
    ]
    for row in platform_rows:
        platform = str(row["platform"])
        label = PLATFORM_LABELS.get(platform, platform)
        lines.append(f"| {label} | {row['n']:,} | {PLATFORM_DESCRIPTIONS.get(platform, '公开页面与媒体元数据')} |")
    lines.append(SNAPSHOT_END)
    return "\n".join(lines)


def landing_block(connection: sqlite3.Connection) -> str:
    """Build a compact editorial front page from the current database snapshot."""

    records = rows(connection)
    run = connection.execute(
        "SELECT dataset_version, COALESCE(finished_at, started_at) AS assessed_at FROM collection_runs WHERE trigger <> 'legacy-migration' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    counts = connection.execute(
        "SELECT COUNT(*) AS items, COUNT(DISTINCT platform) AS platforms FROM items"
    ).fetchone()
    media_count = connection.execute("SELECT COUNT(*) FROM media_assets").fetchone()[0]
    bands = connection.execute(
        "SELECT value_band, COUNT(*) AS n FROM v_current_value_matrix GROUP BY value_band ORDER BY value_band"
    ).fetchall()
    official = find_record(records, "https://github.com/deepseek-ai/deepseek-harness")
    web_ui = find_record(records, "https://github.com/zhu1090093659/dsh-web-ui")
    article = find_record(records, "https://mp.weixin.qq.com/s/HrOgdg7ZBKQlvGM-xPeKtw")
    related_article = find_record(records, "https://mp.weixin.qq.com/s/O6u4JsV-cFl9mKF9t5SJqw")
    plugin_urls = (
        "https://github.com/CocoSgt/dsh-nsfw",
        "https://github.com/CocoSgt/dsh-skills",
        "https://github.com/CocoSgt/dsh-attachments",
        "https://github.com/CocoSgt/dsh-inspector",
    )
    plugin_rows = [record for record in records if record["canonical_url"] in plugin_urls]
    attention = attention_rows(records)
    fork_records: list[dict[str, object]] = []
    fork_payload: object = {}
    if FORK_INDEX_PATH.exists():
        try:
            fork_payload = json.loads(FORK_INDEX_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            fork_payload = {}
        if isinstance(fork_payload, dict) and isinstance(fork_payload.get("records"), list):
            fork_records = [row for row in fork_payload["records"] if isinstance(row, dict)]
    fork_filter = fork_payload.get("star_filter", {}) if isinstance(fork_payload, dict) else {}
    band_text = " · ".join(f"{row['value_band']} {row['n']:,}" for row in bands)
    assessed = str(run["assessed_at"] or "")[:10] if run else "unknown"
    article_media = connection.execute(
        "SELECT kind, COUNT(*) AS n FROM media_assets WHERE item_id = ? GROUP BY kind ORDER BY kind",
        (article["id"],) if article else (-1,),
    ).fetchall()
    media_text = " · ".join(f"{row['n']} {row['kind']}" for row in article_media) or "media references captured"

    lines = [
        START,
        "## Start here — the DSH signal desk",
        "",
        f"> 这里不是又一份静态 Awesome List，而是一张持续更新的 DeepSeek Harness 生态地图：先看最值得点开的仓库、帖子和视频，再沿着 raw、SQLite、时间轴回到证据。当前批次 **{clean(run['dataset_version'] if run else 'unknown')}**（{assessed}）：**{counts['items']:,}** 条去重记录、**{counts['platforms']}** 个平台、**{media_count:,}** 个媒体引用。",
        "",
        f"[打开 dsh store](docs/index.html) · [看价值矩阵](docs/value-matrix.md) · [看趋势](docs/trends.md) · [下载查询 SQLite]({PUBLIC_DATABASE_URL})",
        "",
        "![DeepSeek Harness official preview](media/screenshots/official.png)",
        "",
        "### 先看这三个入口",
        "",
        "| 入口 | 为什么值得看 | 当前信号 |",
        "| --- | --- | ---: |",
    ]
    if official:
        lines.append(f"| {link('官方核心 · ' + str(official['title']), official['canonical_url'])} | DSH 的源头仓库；所有插件和能力最终回到这里核验。 | {metric_text(official)} |")
    if web_ui:
        lines.append(f"| {link('高关注插件 · ' + str(web_ui['title']), web_ui['canonical_url'])} | 真实可见的 UI / 桌面扩展，适合从“能不能直接用”开始。 | {metric_text(web_ui)} |")
    lines.append(f"| [新文章 · 如何用 GLM 5.3，开发 DeepSeek Harness 插件](https://mp.weixin.qq.com/s/HrOgdg7ZBKQlvGM-xPeKtw) | 一篇文章串起模型接入、插件契约、skill、附件和 inspector；{media_text}。 | counters NULL |")
    lines.extend(["", "### 新：一篇文章与一项社区补充", ""])
    if article:
        related = f"相关历史报道：{link(related_article['title'], related_article['canonical_url'])}。" if related_article else ""
        lines.append(f"> [如何用 GLM 5.3，开发 DeepSeek Harness 插件](https://mp.weixin.qq.com/s/HrOgdg7ZBKQlvGM-xPeKtw) · {clean(article['author'])} · {clean(article['published_label'])}。文章报告作者用 GLM 5.3 为 DSH 补上 skill 索引、文件附件和约束/skill 检查能力；互动计数未公开，保持 `NULL`。{related}")
    lines.append("> 另从 GitHub 的公开贡献记录补入 [CocoSgt/dsh-nsfw](https://github.com/CocoSgt/dsh-nsfw)：一个由仓库驱动的 DeepSeek 鲸鱼娘全年龄漫画收藏与分享站；当前 GitHub 快照为 10 stars、3 forks，详情以仓库 README 和 raw 记录为准。")
    lines.extend(["", "| 插件 | 用途 |", "| --- | --- |"])
    descriptions = {
        "dsh-nsfw": "由仓库驱动的 DeepSeek 鲸鱼娘全年龄漫画收藏与分享站。",
        "dsh-skills": "索引和加载项目里的 skill，支持完整 `.skill` 文件。",
        "dsh-attachments": "为 DSH 增加文件/图片附件与继续引用能力。",
        "dsh-inspector": "查看生效的约束文件和当前被索引的 skill。",
    }
    for row in plugin_rows:
        name = str(row["title"]).split("/", 1)[-1]
        lines.append(f"| {link(str(row['title']), row['canonical_url'])} | {descriptions.get(name, '文章中公开的 DSH 插件。')} · {metric_text(row)} |")
    lines.extend(["", "安装提示（文章原文，三个插件）：", "", "```sh", "dsh plugin --profile web add dsh-skills dsh-attachments dsh-inspector", "```", "", "### 大家正在关注什么", "", "| 平台 | 记录 | 平台原生信号 | 为什么在首页 |", "| --- | --- | ---: | --- |"])
    reasons = {"x": "官方发布与开发者传播", "youtube": "长视频实测/解读", "bilibili": "中文教程与体验", "hacker_news": "开发者讨论", "xiaohongshu": "中文入门与教程"}
    for row in attention:
        lines.append(f"| {PLATFORM_LABELS.get(str(row['platform']), row['platform'])} | {link(row['title'], row['canonical_url'])} | {metric_text(row)} | {reasons.get(str(row['platform']), '公开生态信号')} |")
    if fork_records:
        fork_version = str(fork_records[0].get("dataset_version") or "unknown")
        deep_count = sum(row.get("detail_status") == "ok" for row in fork_records)
        lines.extend([
            "",
            "### 官方 Fork network：把分叉当作生态信号",
            "",
            f"沿 `deepseek-ai/deepseek-harness` 的公开分页，本批次登记 **{fork_filter.get('observed_forks', len(fork_records)):,}** 个 Fork（{fork_version}）；按 **{fork_filter.get('minimum_stars', 0):,}+ stars** 进入排序的 **{len(fork_records):,}** 个，深度盘点成功 **{deep_count:,}** 个。它是公开信号和变体线索，不是质量、安全或诚信背书。",
            "",
            f"[打开 Fork 检索页](docs/forks.html) · [看 Fork 数据报告](docs/forks.md) · [下载完整压缩 SQLite 快照]({FULL_DATABASE_URL}) · [看完整 JSONL 索引](index/forks.jsonl)",
            "",
            "| Rank | Fork | stars | owner reputation | repo influence | overall | deep status | one-sentence evidence |",
            "| ---: | --- | ---: | --- | ---: | ---: | --- | --- |",
        ])
        for row in fork_records[:5]:
            owner = row.get("full_name") or "unknown"
            influence = row.get("influence") if isinstance(row.get("influence"), dict) else {}
            score = influence.get("score") if isinstance(influence, dict) else None
            score_text = f"{float(score):.3f}" if isinstance(score, (int, float)) else "—"
            reputation = influence.get("reputation_score") if isinstance(influence, dict) else None
            reputation_status = influence.get("reputation_status", "unobserved") if isinstance(influence, dict) else "unobserved"
            reputation_text = f"{float(reputation):.1f} ({reputation_status})" if isinstance(reputation, (int, float)) else f"— ({reputation_status})"
            repository_score = influence.get("repository_influence_score") if isinstance(influence, dict) else None
            repository_text = f"{float(repository_score):.3f}" if isinstance(repository_score, (int, float)) else "—"
            stars = row.get("stars")
            stars_text = number(stars)
            lines.append(f"| {row.get('rank', '—')} | [{clean(owner)}]({html.escape(str(row.get('url') or ''), quote=True)}) | {stars_text} | {reputation_text} | {repository_text} | {score_text} | {clean(row.get('detail_status') or 'unknown')} | {clean(row.get('change_summary') or '—')} |")
    lines.extend(["", f"> 价值档当前分布：**{band_text}**。分数只用于安排复核优先级；不同平台的 stars、likes、views、points 不相加，缺失互动数不补零。", "", "<!-- landing:end -->"])
    return "\n".join(lines)


def main() -> int:
    """Replace only the marked landing block and keep the long-form docs below it."""

    text = README_PATH.read_text(encoding="utf-8")
    if any(marker not in text for marker in (START, END, SNAPSHOT_START, SNAPSHOT_END)):
        raise SystemExit("README.md is missing landing or snapshot markers")
    with connect() as connection:
        block = landing_block(connection)
        snapshot = snapshot_block(connection)
    before, remainder = text.split(START, 1)
    _old, after = remainder.split(END, 1)
    updated = before + block + after
    before, remainder = updated.split(SNAPSHOT_START, 1)
    _old, after = remainder.split(SNAPSHOT_END, 1)
    README_PATH.write_text(before + snapshot + after, encoding="utf-8")
    print(f"updated README landing block from {DB_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
