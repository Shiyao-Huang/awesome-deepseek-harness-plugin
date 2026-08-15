#!/usr/bin/env python3
"""Build trend pages and SVG charts from metric history, publication dates, and the value matrix.

Outputs (regenerated each run):
  docs/trends.md                     — narrative trend report with tables
  docs/assets/trends-growth.svg      — daily new plugin repos + cumulative ecosystem curve
  docs/assets/trends-activity.svg    — cross-platform daily published items
  docs/assets/trends-bands.svg       — current value-band distribution
  docs/assets/trends-velocity.svg    — engagement-per-day leaders
Trends are honest about snapshot depth: growth/activity come from publication dates,
velocity from latest metrics over item age, and deltas only where >= 2 snapshots exist.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import sqlite3
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"
COLORS = ["#ef8354", "#4f6d7a", "#5da399", "#d4a373", "#7b6d8d", "#e07a5f", "#3d5a80"]


def esc(value: object) -> str:
    """Escape a value for Markdown/HTML text contexts."""

    return html.escape(str(value or ""))


def connect() -> sqlite3.Connection:
    """Open the aggregator database."""

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def fmt(value: object) -> str:
    """Format counts with thousands separators, None as em dash."""

    return f"{value:,}" if value is not None else "—"


def svg_header(title: str, width: int, height: int) -> list[str]:
    """Shared SVG opening with the report style sheet."""

    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#253237} .muted{fill:#6b7a80;font-size:12px}</style>',
        f'<rect width="100%" height="100%" rx="18" fill="#fbfaf7"/>',
        f'<text x="28" y="34" font-size="20" font-weight="700">{esc(title)}</text>',
    ]


def write_svg(filename: str, parts: Iterable[str]) -> None:
    """Write one SVG asset."""

    (ASSETS / filename).write_text("\n".join(list(parts) + ["</svg>\n"]), encoding="utf-8")


def growth_chart(rows: list[sqlite3.Row]) -> None:
    """Daily new plugin repos as bars plus a cumulative line."""

    width, height = 920, 430
    left, top, bottom = 60, 60, 60
    chart_h = height - top - bottom
    max_new = max((row["n"] for row in rows), default=1)
    max_total = rows[-1]["cumulative"] if rows else 1
    span = max(len(rows) - 1, 1)
    step = (width - left - 40) / (len(rows) or 1)
    parts = svg_header("Plugin ecosystem growth — new dsh-plugin repos per day", width, height)
    for index, row in enumerate(rows):
        bar_h = int(chart_h * row["n"] / max_new) if max_new else 0
        x = left + index * step
        y = top + chart_h - bar_h
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(step - 3, 2):.1f}" height="{bar_h}" rx="3" fill="{COLORS[0]}" fill-opacity="0.75"/>'
        )
    cumulative_points = []
    for index, row in enumerate(rows):
        x = left + index * step + step / 2
        y = top + chart_h - chart_h * row["cumulative"] / max_total
        cumulative_points.append(f"{x:.1f},{y:.1f}")
    parts.append(f'<polyline points="{" ".join(cumulative_points)}" fill="none" stroke="{COLORS[1]}" stroke-width="2.5"/>')
    first, peak, last = rows[0], max(rows, key=lambda r: r["n"]), rows[-1]
    for row, label in ((first, "start"), (peak, f"peak {fmt(peak['n'])}"), (last, f"{fmt(last['cumulative'])} total")):
        x = left + rows.index(row) * step
        parts.append(f'<text x="{min(x, width - 90):.0f}" y="{height - 34}" font-size="12" class="muted">{row["day"]} · {label}</text>')
    parts.append(f'<text x="{width - 150}" y="{top - 12}" font-size="12" class="muted">line = cumulative repos</text>')
    write_svg("trends-growth.svg", parts)


def activity_chart(rows: list[sqlite3.Row]) -> None:
    """Stacked-free daily item counts across platforms for the recent window."""

    width, height = 920, 380
    left, top, bottom = 60, 56, 56
    chart_h = height - top - bottom
    max_count = max((row["n"] for row in rows), default=1)
    step = (width - left - 40) / (len(rows) or 1)
    parts = svg_header("Cross-platform daily activity — items by publish date (90d)", width, height)
    for index, row in enumerate(rows):
        bar_h = int(chart_h * row["n"] / max_count) if max_count else 0
        x = left + index * step
        y = top + chart_h - bar_h
        color = COLORS[2] if row["n"] == max_count else COLORS[3]
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(step - 2, 2):.1f}" height="{bar_h}" rx="3" fill="{color}"/>')
    if rows:
        peak = max(rows, key=lambda r: r["n"])
        parts.append(f'<text x="{left + rows.index(peak) * step - 40:.0f}" y="{top - 14}" font-size="12" class="muted">peak {fmt(peak["n"])} on {peak["day"]}</text>')
    write_svg("trends-activity.svg", parts)


def bands_chart(rows: list[sqlite3.Row]) -> None:
    """Current value-band distribution as horizontal bars."""

    width, row_height, top = 920, 46, 70
    height = top + row_height * max(len(rows), 1) + 30
    max_n = max((row["n"] for row in rows), default=1)
    parts = svg_header("Value-band distribution — current dataset", width, height)
    for index, row in enumerate(rows):
        y = top + index * row_height
        bar = int(600 * row["n"] / max_n)
        parts.extend([
            f'<text x="28" y="{y + 22}" font-size="15">band {esc(row["value_band"])}（avg value {row["avg_score"]:.1f}）</text>',
            f'<rect x="300" y="{y + 4}" width="600" height="22" rx="11" fill="#e8e2d6"/>',
            f'<rect x="300" y="{y + 4}" width="{bar}" height="22" rx="11" fill="{COLORS[index % len(COLORS)]}"/>',
            f'<text x="912" y="{y + 22}" text-anchor="end" font-size="15" font-weight="700">{fmt(row["n"])}</text>',
        ])
    write_svg("trends-bands.svg", parts)


def velocity_chart(rows: list[sqlite3.Row]) -> None:
    """Top engagement-per-day items as horizontal bars."""

    width, row_height, top = 920, 44, 70
    height = top + row_height * max(len(rows), 1) + 20
    max_v = max((row["velocity"] for row in rows), default=1.0)
    parts = svg_header("Engagement velocity — signal per day since publication (top 15)", width, height)
    for index, row in enumerate(rows):
        y = top + index * row_height
        bar = int(600 * row["velocity"] / max_v)
        label = f"{str(row['title'])[:44]} [{row['platform']}]"
        parts.extend([
            f'<text x="28" y="{y + 21}" font-size="13">{esc(label)}</text>',
            f'<rect x="470" y="{y + 3}" width="380" height="22" rx="11" fill="#e8e2d6"/>',
            f'<rect x="470" y="{y + 3}" width="{int(380 * row["velocity"] / max_v)}" height="22" rx="11" fill="{COLORS[5]}"/>',
            f'<text x="900" y="{y + 21}" text-anchor="end" font-size="13" font-weight="700">{row["velocity"]:,.0f}/day</text>',
        ])
    write_svg("trends-velocity.svg", parts)


def daily_series(connection: sqlite3.Connection, platform: str | None, days: int) -> list[sqlite3.Row]:
    """Daily item counts by published_at, zero-filled across the window."""

    if platform:
        rows = connection.execute(
            """
            SELECT date(published_at) AS day, COUNT(*) AS n
            FROM items WHERE platform = ? AND published_at IS NOT NULL
            GROUP BY 1 ORDER BY 1
            """,
            (platform,),
        ).fetchall()
    else:
        rows = connection.execute(
            """
            SELECT date(published_at) AS day, COUNT(*) AS n
            FROM items WHERE published_at IS NOT NULL
            GROUP BY 1 ORDER BY 1
            """
        ).fetchall()
    rows = [row for row in rows if row["day"]]
    if not rows:
        return []
    start = dt.date.fromisoformat(rows[0]["day"])
    end = max(dt.date.fromisoformat(rows[-1]["day"]), dt.date.today() - dt.timedelta(days=1))
    counts = {row["day"]: row["n"] for row in rows}
    window = []
    for offset in range((end - start).days + 1):
        day = (start + dt.timedelta(days=offset)).isoformat()
        if days and offset > (end - start).days:
            break
        window.append({"day": day, "n": counts.get(day, 0)})
    if days:
        window = window[-days:]
    total = 0
    filled = []
    for entry in window:
        total += entry["n"]
        filled.append({"day": entry["day"], "n": entry["n"], "cumulative": total})
    return filled


def build(connection: sqlite3.Connection) -> None:
    """Generate every trend artifact from the database."""

    DOCS.mkdir(exist_ok=True)
    ASSETS.mkdir(exist_ok=True)
    generated_row = connection.execute(
        "SELECT COALESCE(finished_at, started_at) FROM collection_runs WHERE trigger <> 'legacy-migration' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    generated = str(generated_row[0]) if generated_row and generated_row[0] else dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    github_growth = daily_series(connection, "github", days=None)
    activity = daily_series(connection, None, days=90)
    growth_chart(github_growth)
    activity_chart(activity)

    bands = connection.execute(
        """
        SELECT value_band, COUNT(*) AS n, AVG(value_score) AS avg_score
        FROM v_current_value_matrix GROUP BY value_band ORDER BY value_band
        """
    ).fetchall()
    bands_chart(bands)

    velocity = connection.execute(
        """
        SELECT i.platform, i.title, i.canonical_url, v.value_band,
               CASE
                 WHEN i.platform = 'github' THEN (COALESCE(m.stars,0) + 2*COALESCE(m.forks,0))
                 WHEN i.platform = 'x' THEN (COALESCE(m.likes,0) + 2*COALESCE(m.reposts,0) + COALESCE(m.views,0)/10000.0)
                 WHEN i.platform = 'hacker_news' THEN (COALESCE(m.points,0) + 3*COALESCE(m.comments,0))
                 WHEN i.platform = 'bilibili' THEN (COALESCE(m.views,0)/50.0 + COALESCE(m.likes,0))
                 ELSE (COALESCE(m.likes,0) + COALESCE(m.views,0)/100.0)
               END * 1.0 / MAX(julianday('now') - julianday(COALESCE(i.published_at, i.first_seen_at)), 0.5) AS velocity
        FROM items i
        JOIN v_current_value_matrix v ON v.item_id = i.id
        LEFT JOIN metrics m ON m.id = (
            SELECT m2.id FROM metrics m2 WHERE m2.item_id = i.id ORDER BY m2.observed_at DESC, m2.id DESC LIMIT 1
        )
        WHERE i.published_at IS NOT NULL
        ORDER BY velocity DESC LIMIT 15
        """
    ).fetchall()
    velocity_chart(velocity)

    deltas = connection.execute(
        """
        SELECT i.platform, i.title, i.canonical_url,
               COUNT(m.id) AS snapshots,
               MAX(m.observed_at) AS latest_at, MIN(m.observed_at) AS first_at,
               CASE i.platform WHEN 'github' THEN MAX(m.stars) - MIN(m.stars) END AS delta_stars
        FROM items i JOIN metrics m ON m.item_id = i.id
        WHERE i.platform = 'github'
        GROUP BY i.id
        HAVING snapshots >= 2 AND delta_stars IS NOT NULL AND delta_stars > 0
        ORDER BY delta_stars DESC LIMIT 10
        """
    ).fetchall()

    runs = connection.execute(
        "SELECT dataset_version, started_at, trigger, status, raw_files_seen, item_observations FROM collection_runs ORDER BY id DESC LIMIT 8"
    ).fetchall()

    weekly = connection.execute(
        """
        SELECT strftime('%Y-W%W', published_at) AS week, COUNT(*) AS n
        FROM items WHERE platform='github' AND published_at IS NOT NULL
        GROUP BY 1 ORDER BY 1 DESC LIMIT 6
        """
    ).fetchall()

    launch_day = connection.execute(
        "SELECT COUNT(*) AS n FROM items WHERE platform='github' AND date(published_at)='2026-08-13'"
    ).fetchone()["n"]

    lines = [
        "# 趋势 Trends — 生态增长、活跃度与价值分布",
        "",
        f"> 生成时间 {generated}。增长曲线来自仓库创建日期；活跃度来自全平台发布日期；价值分布来自当前 value matrix；增量仅在存在多快照时计算。",
        "",
        "## 生态增长（GitHub dsh-plugin 仓库/日）",
        "",
        f"![growth](assets/trends-growth.svg)",
        "",
        f"- 开源日 **2026-08-13** 当天新增 **{fmt(launch_day)}** 个插件仓库；次日再增 {fmt(dict((r['day'], r['n']) for r in github_growth).get('2026-08-14'))} 个。",
        f"- 累计收录（本库观察到的）**{fmt(github_growth[-1]['cumulative'])}** 个仓库；topic 全量见 `sources` 表。",
        "",
        "| 周 | 新增仓库 |", "|---|---:|",
    ]
    for row in weekly:
        lines.append(f"| {row['week']} | {fmt(row['n'])} |")
    lines.extend([
        "",
        "## 全平台活跃度（近 90 天按发布日期）",
        "",
        "![activity](assets/trends-activity.svg)",
        "",
        "| 日期 | 条目 |", "|---|---:|",
    ])
    for row in activity[-14:]:
        lines.append(f"| {row['day']} | {fmt(row['n'])} |")
    lines.extend([
        "",
        "## 价值分布（当前 dataset）",
        "",
        "![bands](assets/trends-bands.svg)",
        "",
        "| 档 | 条目 | 平均 value |", "|---|---:|---:|",
    ])
    for row in bands:
        lines.append(f"| {row['value_band']} | {fmt(row['n'])} | {row['avg_score']:.1f} |")
    lines.extend([
        "",
        "## 增速榜（互动/天，含价值档）",
        "",
        "![velocity](assets/trends-velocity.svg)",
        "",
        "| 平台 | 条目 | 价值档 | 互动/天 |", "|---|---|---|---:|",
    ])
    for row in velocity:
        title = str(row["title"] or row["canonical_url"]).replace("|", "\\|")[:60]
        lines.append(f"| {row['platform']} | [{esc(title)}]({row['canonical_url']}) | {row['value_band']} | {row['velocity']:,.0f} |")
    if deltas:
        lines.extend([
            "",
            "## 快照增量（GitHub stars，需 ≥2 次观测）",
            "",
            "| 仓库 | 快照数 | Δstars |", "|---|---:|---:|",
        ])
        for row in deltas:
            lines.append(f"| [{esc(str(row['title']))}]({row['canonical_url']}) | {row['snapshots']} | +{fmt(row['delta_stars'])} |")
    lines.extend([
        "",
        "## 采集运行历史",
        "",
        "| dataset | 时间 | 触发 | 状态 | raw 文件 | item 观测 |", "|---|---|---|---|---:|---:|",
    ])
    for row in runs:
        lines.append(f"| {row['dataset_version']} | {row['started_at']} | {row['trigger']} | {row['status']} | {fmt(row['raw_files_seen'])} | {fmt(row['item_observations'])} |")
    lines.extend([
        "",
        "## 如何持续追踪",
        "",
        "- `make update`：抓取 GitHub/HN API 并追加指标快照（metrics 按 observed_at 去重，天然形成时间序列）。",
        "- `make schedule`：运行 source monitor + 全量重建（采集运行历史随之增长）。",
        "- `python3 scripts/build_trends.py`：本页与 4 张 SVG 重新生成。",
        "",
    ])
    (DOCS / "trends.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"trends written: docs/trends.md + 4 SVGs ({generated})")


def main() -> int:
    """Entry point."""

    connection = connect()
    try:
        build(connection)
    finally:
        connection.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
