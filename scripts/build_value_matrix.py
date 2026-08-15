#!/usr/bin/env python3
"""Score the current ecosystem snapshot with an evidence-aware value matrix."""

from __future__ import annotations

import datetime as dt
import html
import json
import math
import sqlite3
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
CONFIG_PATH = ROOT / "config" / "value_matrix.json"
INDEX_PATH = ROOT / "index" / "value-matrix.jsonl"
DOC_PATH = ROOT / "docs" / "value-matrix.md"
SVG_PATH = ROOT / "docs" / "assets" / "value-matrix.svg"

SIGNAL_FIELDS = {
    "github": ("stars",),
    "hacker_news": ("points",),
    "x": ("likes", "views", "replies", "reposts"),
    "xiaohongshu": ("likes",),
    "youtube": ("views",),
    "bilibili": ("views", "likes", "replies"),
    "reddit": ("likes", "comments"),
    "zhihu": ("views", "likes", "replies"),
    "wechat": ("likes", "views", "comments", "replies"),
    "web": ("views", "likes", "comments"),
}
DEFAULT_SIGNAL_FIELDS = ("likes", "views", "points", "comments", "replies", "favorites", "shares", "forks")
BAND_COLORS = {"A": "#2a9d8f", "B": "#4f6d7a", "C": "#e9c46a", "D": "#e76f51"}


def connect() -> sqlite3.Connection:
    """Open the aggregator database with named result columns."""

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def utc_now() -> str:
    """Return a second-precision UTC timestamp."""

    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_time(value: Any) -> dt.datetime | None:
    """Parse a stored ISO timestamp while accepting a trailing Z."""

    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)


def clamp(value: float) -> float:
    """Keep a score in the public 0–100 range."""

    return max(0.0, min(100.0, value))


def as_json(value: Any) -> dict[str, Any]:
    """Decode an item raw payload into an object or return an empty object."""

    try:
        decoded = json.loads(value or "{}")
    except (TypeError, json.JSONDecodeError):
        return {}
    return decoded if isinstance(decoded, dict) else {}


def has_license(raw: dict[str, Any]) -> bool:
    """Detect a reported license without inferring one from repository code."""

    candidates = [raw.get("license"), raw.get("license_spdx")]
    metadata = raw.get("repository_metadata")
    if isinstance(metadata, dict):
        candidates.extend((metadata.get("license"), metadata.get("license_spdx")))
    return any(
        isinstance(value, str) and value.strip() and value.strip().lower() not in {"none", "noassertion"}
        for value in candidates
    )


def signal_fields(platform: str) -> tuple[str, ...]:
    """Return platform-native metrics used for within-platform traction."""

    return SIGNAL_FIELDS.get(platform, DEFAULT_SIGNAL_FIELDS)


def native_signal(row: sqlite3.Row) -> tuple[float | None, str | None]:
    """Return the largest available native metric and its field name."""

    values = [
        (float(row[field]), field)
        for field in signal_fields(str(row["platform"]))
        if row[field] is not None and float(row[field]) >= 0
    ]
    return max(values, default=(None, None))


def value_band(score: float, bands: dict[str, Any]) -> str:
    """Map a weighted score to the configured A–D band."""

    for band in ("A", "B", "C", "D"):
        if score >= float(bands.get(band, 0)):
            return band
    return "D"


def current_run(connection: sqlite3.Connection) -> sqlite3.Row:
    """Return the newest non-legacy collection run."""

    row = connection.execute(
        "SELECT id, dataset_version, COALESCE(finished_at, started_at) AS assessed_at FROM collection_runs WHERE trigger <> 'legacy-migration' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    if row is None:
        raise RuntimeError("cannot score a database without a collection run")
    return row


def rows_for_scoring(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    """Load items, latest metrics, provenance, details, media, and upstream links."""

    return connection.execute(
        """
        WITH obs AS (
            SELECT io.item_id, COUNT(*) AS observation_count, COUNT(DISTINCT o.source_id) AS source_count
            FROM item_observations AS io
            JOIN observations AS o ON o.id = io.observation_id
            GROUP BY io.item_id
        ), media AS (
            SELECT item_id, COUNT(*) AS media_count
            FROM media_assets
            GROUP BY item_id
        ), upstream AS (
            SELECT item_id,
                   COUNT(DISTINCT repository_id) AS upstream_count,
                   SUM(CASE WHEN entry_kind = 'plugin-candidate' THEN 1 ELSE 0 END) AS plugin_count,
                   SUM(CASE WHEN install_hint IS NOT NULL AND TRIM(install_hint) <> '' THEN 1 ELSE 0 END) AS install_count
            FROM upstream_entries
            WHERE item_id IS NOT NULL AND active = 1
            GROUP BY item_id
        )
        SELECT i.id, i.platform, i.external_id, i.canonical_url, i.item_type, i.title,
               i.category, i.content_text, i.last_seen_at, i.raw_json,
               lm.observed_at, lm.likes, lm.replies, lm.reposts, lm.comments,
               lm.bookmarks, lm.views, lm.points, lm.stars, lm.forks, lm.favorites,
               lm.shares,
               COALESCE(obs.observation_count, 0) AS observation_count,
               COALESCE(obs.source_count, 0) AS source_count,
               COALESCE(media.media_count, 0) AS media_count,
               COALESCE(upstream.upstream_count, 0) AS upstream_count,
               COALESCE(upstream.plugin_count, 0) AS plugin_count,
               COALESCE(upstream.install_count, 0) AS install_count,
               COALESCE(details.status, 'missing') AS detail_status,
               COALESCE(details.char_count, 0) AS detail_char_count
        FROM items AS i
        LEFT JOIN v_latest_metrics AS lm ON lm.item_id = i.id
        LEFT JOIN obs ON obs.item_id = i.id
        LEFT JOIN media ON media.item_id = i.id
        LEFT JOIN upstream ON upstream.item_id = i.id
        LEFT JOIN item_details AS details ON details.item_id = i.id
        ORDER BY i.id
        """
    ).fetchall()


def score_rows(connection: sqlite3.Connection, config: dict[str, Any], run: sqlite3.Row) -> list[dict[str, Any]]:
    """Calculate deterministic matrix rows for one collection run."""

    rows = rows_for_scoring(connection)
    logged_signals: dict[str, list[float]] = {}
    signals: dict[int, tuple[float | None, str | None]] = {}
    for row in rows:
        signal, field = native_signal(row)
        signals[int(row["id"])] = (signal, field)
        if signal is not None:
            logged_signals.setdefault(str(row["platform"]), []).append(math.log1p(signal))
    platform_max = {platform: max(values, default=0.0) for platform, values in logged_signals.items()}
    now = parse_time(run["assessed_at"]) or dt.datetime.now(dt.timezone.utc)
    weights = {key: float(value) for key, value in config["weights"].items()}
    result: list[dict[str, Any]] = []
    for row in rows:
        item_id = int(row["id"])
        raw = as_json(row["raw_json"])
        detail_status = str(row["detail_status"])
        detail_chars = int(row["detail_char_count"] or 0)
        observation_count = int(row["observation_count"] or 0)
        source_count = int(row["source_count"] or 0)
        media_count = int(row["media_count"] or 0)
        upstream_count = int(row["upstream_count"] or 0)
        plugin_count = int(row["plugin_count"] or 0)
        install_count = int(row["install_count"] or 0)
        metric_signal, signal_field = signals[item_id]
        logged_max = platform_max.get(str(row["platform"]), 0.0)
        traction = clamp(100.0 * math.log1p(metric_signal) / logged_max) if metric_signal is not None and logged_max else 0.0

        utility = 25.0
        if row["item_type"] == "plugin":
            utility += 35.0
        elif row["item_type"] == "source-repository":
            utility += 25.0
        elif row["item_type"] == "ecosystem-reference":
            utility += 20.0
        if plugin_count:
            utility += 20.0
        if install_count:
            utility += 10.0
        if len(str(row["content_text"] or "")) >= 120:
            utility += 10.0
        if detail_chars >= 200:
            utility += 10.0
        utility = clamp(utility)

        evidence = 20.0 if observation_count else 0.0
        evidence += 25.0 if detail_status == "ok" and detail_chars >= 200 else 0.0
        evidence += 15.0 if media_count else 0.0
        evidence += 20.0 if metric_signal is not None else 0.0
        evidence += 20.0 * min(source_count, 3) / 3
        evidence = clamp(evidence)

        ecosystem = (
            0.5 * min(100.0, upstream_count * 40.0)
            + 0.3 * min(100.0, source_count * 40.0)
            + 0.2 * min(100.0, observation_count * 20.0)
        )
        age_days = 365.0
        last_seen = parse_time(row["last_seen_at"])
        if last_seen is not None:
            age_days = max(0.0, (now - last_seen.astimezone(dt.timezone.utc)).total_seconds() / 86400)
        freshness = clamp(100.0 * math.exp(-age_days / 90.0))

        reviewability = 20.0 if observation_count else 0.0
        reviewability += 30.0 if detail_status == "ok" and detail_chars >= 200 else 0.0
        reviewability += 20.0 if install_count else 0.0
        reviewability += 15.0 if has_license(raw) else 0.0
        reviewability += 15.0 if detail_status not in {"blocked", "failed", "thin"} else 0.0
        reviewability = clamp(reviewability)

        components = {
            "utility": round(utility, 2),
            "evidence": round(evidence, 2),
            "traction": round(traction, 2),
            "ecosystem": round(ecosystem, 2),
            "freshness": round(freshness, 2),
            "reviewability": round(reviewability, 2),
        }
        value_score = clamp(sum(components[key] * weights[key] for key in weights))
        evidence_count = sum((
            observation_count > 0,
            detail_status == "ok" and detail_chars >= 200,
            media_count > 0,
            metric_signal is not None,
            upstream_count > 0,
        ))
        confidence = clamp(
            (25.0 if observation_count else 0.0)
            + (25.0 if detail_status == "ok" and detail_chars >= 200 else 0.0)
            + (20.0 if metric_signal is not None else 0.0)
            + (15.0 if source_count >= 2 or upstream_count >= 2 else 0.0)
            + (15.0 if evidence_count >= 3 else 0.0)
        )
        risk_flags: list[str] = []
        if metric_signal is None:
            risk_flags.append("metrics_missing")
        if detail_status != "ok":
            risk_flags.append(f"detail_{detail_status}")
        if str(row["platform"]) == "github" and not has_license(raw):
            risk_flags.append("license_unreported")
        if row["item_type"] == "plugin" and upstream_count == 0:
            risk_flags.append("ecosystem_link_missing")
        result.append({
            "id": f"id-{item_id}",
            "item_id": item_id,
            "title": row["title"] or row["canonical_url"],
            "url": row["canonical_url"],
            "platform": row["platform"],
            "category": row["category"],
            "dataset_version": run["dataset_version"],
            "collection_run_id": int(run["id"]),
            "scoring_version": config["scoring_version"],
            "assessed_at": run["assessed_at"],
            **components,
            "value_score": round(value_score, 2),
            "confidence_score": round(confidence, 2),
            "value_band": value_band(value_score, config["bands"]),
            "evidence_count": evidence_count,
            "source_count": source_count,
            "risk_flags": risk_flags,
            "components": {
                **components,
                "native_signal": metric_signal,
                "signal_field": signal_field,
                "age_days": round(age_days, 2),
                "detail_status": detail_status,
                "detail_char_count": detail_chars,
            },
        })
    return sorted(result, key=lambda row: (-row["value_score"], -row["confidence_score"], row["item_id"]))


def write_database(connection: sqlite3.Connection, rows: list[dict[str, Any]]) -> None:
    """Upsert one assessment per item for the current run and scoring version."""

    for row in rows:
        connection.execute(
            """
            INSERT INTO value_assessments(
                item_id, collection_run_id, dataset_version, scoring_version, assessed_at,
                utility_score, evidence_score, traction_score, ecosystem_score,
                freshness_score, reviewability_score, value_score, confidence_score,
                value_band, evidence_count, source_count, risk_flags, components_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(item_id, collection_run_id, scoring_version) DO UPDATE SET
                dataset_version=excluded.dataset_version, assessed_at=excluded.assessed_at,
                utility_score=excluded.utility_score, evidence_score=excluded.evidence_score,
                traction_score=excluded.traction_score, ecosystem_score=excluded.ecosystem_score,
                freshness_score=excluded.freshness_score, reviewability_score=excluded.reviewability_score,
                value_score=excluded.value_score, confidence_score=excluded.confidence_score,
                value_band=excluded.value_band, evidence_count=excluded.evidence_count,
                source_count=excluded.source_count, risk_flags=excluded.risk_flags,
                components_json=excluded.components_json
            """,
            (
                row["item_id"], row["collection_run_id"], row["dataset_version"], row["scoring_version"], row["assessed_at"],
                row["utility"], row["evidence"], row["traction"], row["ecosystem"], row["freshness"], row["reviewability"],
                row["value_score"], row["confidence_score"], row["value_band"], row["evidence_count"], row["source_count"],
                json.dumps(row["risk_flags"], ensure_ascii=False), json.dumps(row["components"], ensure_ascii=False, sort_keys=True),
            ),
        )


def write_jsonl(rows: list[dict[str, Any]]) -> None:
    """Write the public machine-readable value matrix projection."""

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    fields = (
        "id", "item_id", "title", "url", "platform", "category", "dataset_version", "scoring_version",
        "assessed_at", "utility", "evidence", "traction", "ecosystem", "freshness", "reviewability",
        "value_score", "confidence_score", "value_band", "evidence_count", "source_count", "risk_flags",
    )
    INDEX_PATH.write_text(
        "".join(json.dumps({key: row[key] for key in fields}, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )


def write_svg(rows: list[dict[str, Any]]) -> None:
    """Write an evidence-versus-utility scatter plot as dependency-free SVG."""

    width, height = 920, 620
    left, top, plot_width, plot_height = 78, 62, 790, 470
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#253237}.muted{fill:#6b7a80;font-size:13px}</style>',
        '<rect width="100%" height="100%" rx="18" fill="#fbfaf7"/>',
        '<text x="28" y="34" font-size="21" font-weight="700">Value matrix: evidence × utility</text>',
        f'<line x1="{left}" y1="{top + plot_height}" x2="{left + plot_width}" y2="{top + plot_height}" stroke="#6b7a80"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" stroke="#6b7a80"/>',
        f'<text x="{left + plot_width / 2}" y="{top + plot_height + 42}" text-anchor="middle" class="muted">evidence score →</text>',
        f'<text x="24" y="{top + plot_height / 2}" transform="rotate(-90 24 {top + plot_height / 2})" text-anchor="middle" class="muted">utility score →</text>',
    ]
    for tick in (0, 25, 50, 75, 100):
        x = left + plot_width * tick / 100
        y = top + plot_height - plot_height * tick / 100
        parts.append(f'<text x="{x}" y="{top + plot_height + 20}" text-anchor="middle" class="muted">{tick}</text>')
        parts.append(f'<text x="{left - 12}" y="{y + 4}" text-anchor="end" class="muted">{tick}</text>')
    for row in rows:
        x = left + plot_width * row["evidence"] / 100
        y = top + plot_height - plot_height * row["utility"] / 100
        color = BAND_COLORS[row["value_band"]]
        label = html.escape(str(row["title"])[:80], quote=True)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{color}" fill-opacity=".72"><title>{label} · {row["value_score"]:.2f}</title></circle>')
    legend_x = 710
    for index, band in enumerate(("A", "B", "C", "D")):
        x = legend_x + index * 42
        parts.append(f'<circle cx="{x}" cy="34" r="5" fill="{BAND_COLORS[band]}"/><text x="{x + 9}" y="39" class="muted">{band}</text>')
    parts.append("</svg>\n")
    SVG_PATH.parent.mkdir(parents=True, exist_ok=True)
    SVG_PATH.write_text("\n".join(parts), encoding="utf-8")


def markdown_text(value: Any) -> str:
    """Escape a value for a Markdown table cell."""

    return str(value or "").replace("|", "\\|").replace("\n", " ").strip()


def write_markdown(rows: list[dict[str, Any]], config: dict[str, Any]) -> None:
    """Write the curated value-matrix explanation and top records."""

    lines = [
        "# Value matrix",
        "",
        "价值矩阵衡量“值得进一步研究/采用的信号”，不是质量认证、销量排名或安全审计。热度与价值分开：traction 只在同一平台内归一化，其他维度负责补充可用性、证据和生态连接。",
        "",
        "## 当前高价值记录",
        "",
        "| # | 平台 | 记录 | value | band | utility | evidence | traction | ecosystem | freshness | reviewability | confidence | 风险提示 |",
        "| ---: | --- | --- | ---: | :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for rank, row in enumerate(rows[:50], 1):
        flags = ", ".join(row["risk_flags"]) or "—"
        lines.append(
            f"| {rank} | {markdown_text(row['platform'])} | [{markdown_text(row['title'])}]({row['url']}) | {row['value_score']:.2f} | {row['value_band']} | "
            f"{row['utility']:.2f} | {row['evidence']:.2f} | {row['traction']:.2f} | {row['ecosystem']:.2f} | "
            f"{row['freshness']:.2f} | {row['reviewability']:.2f} | {row['confidence_score']:.2f} | {markdown_text(flags)} |"
        )
    lines.extend(["", "## 维度与权重", "", "| 维度 | 权重 | 解释 |", "| --- | ---: | --- |"])
    for key, weight in config["weights"].items():
        lines.append(f"| {key} | {float(weight):.0%} | {markdown_text(config['dimension_notes'][key])} |")
    lines.extend([
        "",
        "## 去重与缺失值规则",
        "",
        "- 一条 item 仍以 canonical_url 唯一；同一 raw SHA 只导入一次；同一 item、采集时间和指标来源的 metric 只保留一条。",
        "- 互动数缺失保持 NULL，不会转换成 0；缺失指标只产生 metrics_missing 风险提示并降低证据/置信度。",
        "- 详情抓取按 item_id 幂等；成功详情不会重复请求，blocked/thin/failed 记录保留为 provenance。",
        "- value_assessments 按 item_id + collection_run_id + scoring_version 保存历史评估；同一批次重跑只 upsert，不产生重复评估。",
        "",
        "完整逐条矩阵见 index/value-matrix.jsonl，SQLite 查询视图为 v_current_value_matrix。",
        "",
        "![Evidence × utility value matrix](assets/value-matrix.svg)",
        "",
    ])
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    """Build the current value matrix and its public projections."""

    from collect import init_db

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    init_db(DB_PATH)
    with connect() as connection:
        run = current_run(connection)
        rows = score_rows(connection, config, run)
        write_database(connection, rows)
        write_jsonl(rows)
        write_markdown(rows, config)
        write_svg(rows)
    print(f"built {len(rows)} value assessments for {run['dataset_version']} at {INDEX_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
