#!/usr/bin/env python3
"""Build human-readable index, timeline, category pages, and SVG charts."""

from __future__ import annotations

import html
import sqlite3
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"

COLORS = ["#ef8354", "#4f6d7a", "#5da399", "#d4a373", "#7b6d8d", "#e07a5f", "#3d5a80"]


def esc(value: object) -> str:
    """Escape a value for Markdown or HTML text contexts."""

    return html.escape(str(value or ""))


def connect() -> sqlite3.Connection:
    """Open the generated SQLite database."""

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def metric_label(row: sqlite3.Row) -> str:
    """Format the platform-appropriate visible metric values."""

    values = []
    for key, label in (("stars", "★"), ("likes", "♥"), ("points", "points"), ("views", "views"), ("comments", "comments"), ("replies", "replies"), ("forks", "forks"), ("favorites", "favorites"), ("shares", "shares"), ("coins", "coins"), ("danmaku", "danmaku")):
        if row[key] is not None:
            values.append(f"{row[key]:,} {label}")
    if row["upvote_ratio"] is not None:
        values.append(f"{row['upvote_ratio']:.3f} upvote ratio")
    return ", ".join(values) if values else "—"


def svg_bars(title: str, rows: Iterable[sqlite3.Row], label_key: str, value_key: str, filename: Path) -> None:
    """Write a compact horizontal bar chart as dependency-free SVG."""

    values = [(str(row[label_key]), int(row[value_key] or 0)) for row in rows]
    width = 920
    row_height = 42
    height = max(150, 86 + row_height * len(values))
    max_value = max((value for _, value in values), default=1)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#253237} .muted{fill:#6b7a80;font-size:13px}</style>',
        f'<rect width="100%" height="100%" rx="18" fill="#fbfaf7"/>',
        f'<text x="28" y="36" font-size="21" font-weight="700">{esc(title)}</text>',
    ]
    for index, (label, value) in enumerate(values):
        y = 62 + index * row_height
        bar_width = int(620 * value / max_value) if max_value else 0
        parts.extend([
            f'<text x="28" y="{y + 20}" font-size="14">{esc(label)}</text>',
            f'<rect x="245" y="{y + 5}" width="620" height="20" rx="10" fill="#e8e2d6"/>',
            f'<rect x="245" y="{y + 5}" width="{bar_width}" height="20" rx="10" fill="{COLORS[index % len(COLORS)]}"/>',
            f'<text x="878" y="{y + 20}" text-anchor="end" font-size="14" font-weight="700">{value:,}</text>',
        ])
    parts.append("</svg>\n")
    filename.write_text("\n".join(parts), encoding="utf-8")


def write_index(connection: sqlite3.Connection, generated_at: str, dataset_version: str) -> None:
    """Write the front page with the current dataset version and top records."""

    totals = connection.execute("SELECT COUNT(*) AS items, COUNT(DISTINCT platform) AS platforms FROM items").fetchone()
    media_total = connection.execute("SELECT COUNT(*) AS count FROM media_assets").fetchone()[0]
    platforms = connection.execute("SELECT platform, COUNT(*) AS count FROM items GROUP BY platform ORDER BY count DESC").fetchall()
    categories = connection.execute("SELECT category, item_count, media_count FROM v_category_rollup ORDER BY item_count DESC, category").fetchall()
    top = connection.execute(
        """
        SELECT * FROM v_latest_metrics
        ORDER BY COALESCE(stars, likes, points, views, comments, 0) DESC, item_id
        LIMIT 20
        """
    ).fetchall()
    lines = [
        "# DeepSeek Harness Plugin Aggregator",
        "",
        "> 一个可重复更新的公开资料聚合体：仓库、插件、索引、文章、帖子、图片缩略图和视频链接。原始观测保留在 `data/raw/`，SQLite 是可查询的派生索引。",
        "",
        f"当前数据集版本：**{esc(dataset_version)}**，完成时间：**{esc(generated_at)}**。共 **{totals['items']:,}** 条去重记录，覆盖 **{totals['platforms']}** 个平台，外部媒体资产 **{media_total:,}** 条。",
        "",
        "## 三句话结论",
        "",
        "1. 传播核心仍是 GitHub：官方仓库与一批插件/桌面端/目录项目在短时间内形成明显的生态簇。",
        "2. 讨论扩散到 HN、X、小红书和 YouTube；互动指标必须按平台分别解释，不能把星标、点赞、观看数直接相加。",
        "3. 本项目把“可验证来源 + 观测时间 + 原始快照 + 指标历史”作为第一等数据，方便之后持续更新和回溯。",
        "",
        "## 导航",
        "",
        "- [按来源浏览](timeline.md)",
        "- [按主题归类](categories.md)",
        "- [上游源仓库与插件关系](sources.md)",
        "- [可视化报告](report.html)",
        "- [采集与更新说明](../README.md#更新)",
        "",
        "## 来源分布",
        "",
        "| 平台 | 去重记录 | 采集方式 |",
        "| --- | ---: | --- |",
    ]
    modes = {row["platform"]: row["collection_mode"] for row in connection.execute("SELECT platform, collection_mode FROM sources")}
    for row in platforms:
        lines.append(f"| {esc(row['platform'])} | {row['count']:,} | {esc(modes.get(row['platform'], ''))} |")
    lines.extend(["", "## 主题分布", "", "| 分类 | 记录 | 带媒体 |", "| --- | ---: | ---: |"])
    for row in categories:
        lines.append(f"| {esc(row['category'])} | {row['item_count']:,} | {row['media_count']:,} |")
    lines.extend(["", "## 高互动/高关注记录", "", "| 平台 | 标题 | 作者 | 指标 | 分类 |", "| --- | --- | --- | --- | --- |"])
    for row in top:
        title = (row["title"] or row["canonical_url"] or "未命名").replace("|", "\\|")
        lines.append(f"| {esc(row['platform'])} | [{esc(title)}]({row['canonical_url']}) | {esc(row['author'])} | {esc(metric_label(row))} | {esc(row['category'])} |")
    (DOCS / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sources(connection: sqlite3.Connection) -> None:
    """Write monitored community indexes and their current plugin references."""

    repositories = connection.execute(
        """
        SELECT u.*, r.raw_path,
               COUNT(e.id) AS entry_count,
               COUNT(e.id) FILTER (WHERE e.entry_kind = 'plugin-candidate') AS plugin_count
        FROM upstream_repositories AS u
        LEFT JOIN raw_snapshots AS r ON r.id = u.raw_snapshot_id
        LEFT JOIN upstream_entries AS e ON e.repository_id = u.id
        GROUP BY u.id
        ORDER BY u.full_name
        """
    ).fetchall()
    lines = [
        "# Monitored upstream indexes",
        "",
        "这些仓库是聚合器的源，不等同于项目质量背书。每次监测保存 README/结构化目录 raw，并把公开条目链接到 SQLite 中的去重 item；安装前仍应回到插件仓库审查代码、权限和兼容性。",
        "",
        "| 源仓库 | stars | forks | 开放 issue | 当前条目 | 插件候选 | 最近检查 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in repositories:
        raw_link = f"[raw]({('../' + row['raw_path']) if row['raw_path'] else '#'})"
        lines.append(
            f"| [{esc(row['full_name'])}]({row['source_url']}) | {row['stars'] if row['stars'] is not None else '—'} | "
            f"{row['forks'] if row['forks'] is not None else '—'} | {row['open_issues'] if row['open_issues'] is not None else '—'} | "
            f"{row['entry_count']:,} | {row['plugin_count']:,} | {esc(row['last_checked_at'])} · {raw_link} |"
        )
    for repository in repositories:
        lines.extend(["", f"## {esc(repository['full_name'])}", "", f"{esc(repository['description'])}", ""])
        entries = connection.execute(
            """
            SELECT entry_name, entry_url, entry_kind, category, description, install_hint
            FROM upstream_entries
            WHERE repository_id = ? AND entry_kind = 'plugin-candidate'
            ORDER BY category, entry_name
            LIMIT 20
            """,
            (repository["id"],),
        ).fetchall()
        lines.extend(["展示前 20 个插件候选；完整目录在 `upstream_entries` 表和对应 raw 中。", "", "| 插件 | 类别 | 描述 | 安装提示 |", "| --- | --- | --- | --- |"])
        for entry in entries:
            description = (entry["description"] or "").replace("|", "\\|")
            install = (entry["install_hint"] or "—").replace("|", "\\|")
            lines.append(f"| [{esc(entry['entry_name'])}]({entry['entry_url']}) | {esc(entry['category'])} | {esc(description)} | `{esc(install)}` |")
    (DOCS / "sources.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_timeline(connection: sqlite3.Connection) -> None:
    """Write the chronological index, preserving platform-native time labels."""

    rows = connection.execute(
        """
        SELECT event_at, platform, item_type, title, author, category, canonical_url, published_label
        FROM v_timeline
        ORDER BY event_at DESC, platform, title
        """
    ).fetchall()
    lines = [
        "# Timeline",
        "",
        "按发布日期排序；没有可靠绝对日期的平台记录使用采集时间，并保留页面原始相对时间标签。",
        "",
        "| 时间 | 平台 | 类型 | 标题 | 作者 | 分类 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        title = (row["title"] or row["canonical_url"] or "未命名").replace("|", "\\|")
        time_value = row["published_label"] or row["event_at"] or "未知"
        lines.append(f"| {esc(time_value)} | {esc(row['platform'])} | {esc(row['item_type'])} | [{esc(title)}]({row['canonical_url']}) | {esc(row['author'])} | {esc(row['category'])} |")
    (DOCS / "timeline.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_categories(connection: sqlite3.Connection) -> None:
    """Write category pages with a short curator-facing description."""

    descriptions = {
        "index-and-marketplace": "索引、精选清单、插件市场与发现入口。",
        "ui-and-desktop": "桌面端、Web UI、侧边栏、皮肤和终端界面。",
        "multimedia-and-vision": "视觉、OCR、图片、视频、媒体桥接与富媒体工作流。",
        "agents-and-orchestration": "多 Agent、团队、编排、子代理与工作流。",
        "docs-and-learning": "官方文档、教程、白皮书、论文和入门资料。",
        "operations-and-safety": "沙箱、权限、计费、余额、token 和安全。",
        "core-and-ecosystem": "官方项目、通用生态项目和暂未细分的直接相关记录。",
    }
    categories = connection.execute("SELECT DISTINCT category FROM items ORDER BY category").fetchall()
    lines = ["# Categories", "", "分类是可解释的启发式初筛，不代表项目质量背书；原始标题、描述和来源链接始终优先。", ""]
    for category_row in categories:
        category = category_row["category"]
        rows = connection.execute(
            """
            SELECT * FROM v_latest_metrics WHERE category = ?
            ORDER BY COALESCE(stars, likes, points, views, comments, 0) DESC, item_id
            """,
            (category,),
        ).fetchall()
        lines.extend([f"## {esc(category)}", "", descriptions.get(category, "公开资料聚合记录。"), "", "| 平台 | 标题 | 指标 | 作者 |", "| --- | --- | --- | --- |"])
        for row in rows:
            title = (row["title"] or row["canonical_url"] or "未命名").replace("|", "\\|")
            lines.append(f"| {esc(row['platform'])} | [{esc(title)}]({row['canonical_url']}) | {esc(metric_label(row))} | {esc(row['author'])} |")
        lines.append("")
    (DOCS / "categories.md").write_text("\n".join(lines), encoding="utf-8")


def write_report(connection: sqlite3.Connection, generated_at: str) -> None:
    """Write an illustrated HTML report with a small narrative arc."""

    platform_rows = connection.execute("SELECT platform, COUNT(*) AS count FROM items GROUP BY platform ORDER BY count DESC").fetchall()
    category_rows = connection.execute("SELECT category, item_count AS count FROM v_category_rollup ORDER BY count DESC, category").fetchall()
    media_rows = connection.execute("SELECT media_kind AS kind, COUNT(*) AS count FROM items GROUP BY media_kind ORDER BY count DESC").fetchall()
    top_rows = connection.execute(
        "SELECT * FROM v_latest_metrics ORDER BY COALESCE(stars, likes, points, views, comments, 0) DESC LIMIT 12"
    ).fetchall()
    svg_bars("Records by platform", platform_rows, "platform", "count", ASSETS / "platform-volume.svg")
    svg_bars("Records by category", category_rows, "category", "count", ASSETS / "category-distribution.svg")
    svg_bars("Media kinds", media_rows, "kind", "count", ASSETS / "media-kinds.svg")
    cards = []
    for row in top_rows:
        cards.append(
            f'<article><div class="eyebrow">{esc(row["platform"])} · {esc(row["category"])}</div>'
            f'<h3><a href="{esc(row["canonical_url"])}">{esc(row["title"] or row["canonical_url"])}</a></h3>'
            f'<p>{esc(row["author"])} · {esc(metric_label(row))}</p></article>'
        )
    html_doc = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>DeepSeek Harness Plugin Aggregator Report</title>
<style>
:root {{ color-scheme: light; --ink:#253237; --muted:#6b7a80; --paper:#fbfaf7; --accent:#ef8354; }}
body {{ margin:0; background:#e8e2d6; color:var(--ink); font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
main {{ max-width:1080px; margin:0 auto; padding:48px 22px 72px; }}
.hero {{ background:linear-gradient(135deg,#253237,#4f6d7a); color:white; padding:38px; border-radius:24px; box-shadow:0 20px 50px #25323733; }}
.hero h1 {{ margin:0 0 10px; font-size:clamp(30px,6vw,58px); line-height:1.05; }}
.hero p {{ max-width:760px; color:#edf4f5; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:18px; margin-top:22px; }}
section, article {{ background:var(--paper); border-radius:18px; padding:22px; box-shadow:0 8px 24px #25323712; }}
section {{ margin-top:22px; }}
img.chart {{ display:block; width:100%; height:auto; border-radius:12px; }}
.eyebrow {{ color:var(--accent); font-size:12px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }}
article h3 {{ margin:8px 0 5px; line-height:1.25; }}
a {{ color:#27667b; }}
.note {{ color:var(--muted); }}
</style></head><body><main>
<header class="hero"><div class="eyebrow">PUBLIC SNAPSHOT · {esc(generated_at)}</div>
<h1>DeepSeek Harness 的插件生态正在形成一张可追踪的网</h1>
<p>把仓库、帖子、笔记、视频与互动指标放进同一个可回溯索引。Setup 是生态出现，Conflict 是平台指标不可直接相加，Resolution 是保留原始证据并按来源观察变化。</p></header>
<section><h2>先看分布</h2><div class="grid"><img class="chart" src="assets/platform-volume.svg" alt="Records by platform"><img class="chart" src="assets/category-distribution.svg" alt="Records by category"><img class="chart" src="assets/media-kinds.svg" alt="Media kinds"></div></section>
<section><h2>当前解读</h2><p>GitHub 反映可复用代码与生态基础设施，HN 反映开发者讨论，X 与小红书反映传播和教程扩散，YouTube 反映长视频解释与实测。它们是不同的信号，报告只在各自平台内比较。</p><p class="note">指标为采集时快照；外部媒体只保存链接和缩略图地址，不镜像受版权保护的内容。</p></section>
<section><h2>高关注记录</h2><div class="grid">{"".join(cards)}</div></section>
<section><h2>继续更新</h2><p>执行 <code>python3 scripts/collect.py update --raw path/to/egolite.json</code>，再执行 <code>python3 scripts/build_views.py</code>。每次更新都会保留 API 原始快照和指标观测时间。</p></section>
</main></body></html>
"""
    (DOCS / "report.html").write_text(html_doc, encoding="utf-8")


def main() -> None:
    """Build all derived views."""

    DOCS.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    with connect() as connection:
        run = connection.execute(
            "SELECT dataset_version, COALESCE(finished_at, started_at) AS generated_at FROM collection_runs WHERE trigger <> 'legacy-migration' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        if run is None:
            dataset_version, generated_at = "unversioned", "unknown"
        else:
            dataset_version, generated_at = str(run[0]), str(run[1])
        write_index(connection, generated_at, dataset_version)
        write_timeline(connection)
        write_categories(connection)
        write_sources(connection)
        write_report(connection, f"{dataset_version} · {generated_at}")
    print(f"built docs and charts from {DB_PATH}")


if __name__ == "__main__":
    main()
