#!/usr/bin/env python3
"""Build the public Fork ranking projection from SQLite."""

from __future__ import annotations

import html
import json
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
INDEX_PATH = ROOT / "index" / "forks.jsonl"
JSON_PATH = ROOT / "docs" / "data" / "forks.json"
DOC_PATH = ROOT / "docs" / "forks.md"


def connect() -> sqlite3.Connection:
    """Open SQLite with named result columns."""

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def parse_json(value: str | None, fallback: Any) -> Any:
    """Decode one stored JSON field without hiding malformed evidence."""

    if not value:
        return fallback
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return fallback


def records(connection: sqlite3.Connection) -> tuple[str, list[dict[str, Any]]]:
    """Read the latest successful Fork ranking run."""

    rows = connection.execute(
        """
        SELECT
            fr.rank, fr.fork_id, fr.collection_run_id, fr.ranking_version,
            fr.observed_at, fr.influence_score, fr.stars_component,
            fr.forks_component, fr.watchers_component, fr.activity_component,
            fr.divergence_component, fr.change_component, fr.rationale,
            fr.components_json, cr.dataset_version,
            fp.full_name, fp.html_url, fp.owner_login, fp.owner_type,
            fp.description, fp.parent_full_name, fp.source_full_name,
            fp.default_branch, fp.archived, fp.disabled, fp.stars, fp.forks,
            fp.open_issues, fp.watchers, fp.subscribers, fp.pushed_at,
            fp.updated_at, fp.last_deep_checked_at, fp.detail_status,
            fs.compare_status, fs.ahead_by, fs.behind_by, fs.total_commits,
            fs.changed_files, fs.additions, fs.deletions,
            fs.modification_categories, fs.latest_commit_sha,
            fs.latest_commit_message, fs.latest_commit_at, fs.readme_sha,
            fs.status AS snapshot_status, fs.notes AS snapshot_notes
        FROM fork_rankings AS fr
        JOIN collection_runs AS cr ON cr.id = fr.collection_run_id
        JOIN fork_repositories AS fp ON fp.id = fr.fork_id
        JOIN fork_snapshots AS fs
          ON fs.fork_id = fr.fork_id
         AND fs.collection_run_id = fr.collection_run_id
        WHERE fr.collection_run_id = (
            SELECT fr2.collection_run_id
            FROM fork_rankings AS fr2
            JOIN collection_runs AS cr2 ON cr2.id = fr2.collection_run_id
            WHERE cr2.status = 'succeeded'
            ORDER BY fr2.observed_at DESC, fr2.collection_run_id DESC
            LIMIT 1
        )
        ORDER BY fr.rank, fp.full_name
        """
    ).fetchall()
    if not rows:
        return "", []
    result: list[dict[str, Any]] = []
    for row in rows:
        components = parse_json(row["components_json"], {})
        result.append({
            "rank": row["rank"],
            "fork_id": row["fork_id"],
            "full_name": row["full_name"],
            "url": row["html_url"],
            "owner": {"login": row["owner_login"], "type": row["owner_type"]},
            "description": row["description"],
            "parent": row["parent_full_name"],
            "source": row["source_full_name"],
            "default_branch": row["default_branch"],
            "archived": bool(row["archived"]),
            "disabled": bool(row["disabled"]),
            "stars": row["stars"],
            "forks": row["forks"],
            "open_issues": row["open_issues"],
            "watchers": row["watchers"],
            "subscribers": row["subscribers"],
            "pushed_at": row["pushed_at"],
            "updated_at": row["updated_at"],
            "detail_status": row["detail_status"],
            "last_deep_checked_at": row["last_deep_checked_at"],
            "compare": {
                "status": row["compare_status"],
                "ahead_by": row["ahead_by"],
                "behind_by": row["behind_by"],
                "total_commits": row["total_commits"],
                "changed_files": row["changed_files"],
                "additions": row["additions"],
                "deletions": row["deletions"],
                "modification_categories": parse_json(row["modification_categories"], {}),
            },
            "latest_commit": {
                "sha": row["latest_commit_sha"],
                "message": row["latest_commit_message"],
                "committed_at": row["latest_commit_at"],
            },
            "readme_sha": row["readme_sha"],
            "snapshot_status": row["snapshot_status"],
            "snapshot_notes": row["snapshot_notes"],
            "influence": {
                "score": row["influence_score"],
                "components": {
                    "stars": row["stars_component"],
                    "forks": row["forks_component"],
                    "watchers": row["watchers_component"],
                    "activity": row["activity_component"],
                    "divergence": row["divergence_component"],
                    "changes": row["change_component"],
                },
                "raw_components": components.get("raw_metrics", {}),
                "ranking_version": row["ranking_version"],
                "rationale": row["rationale"],
            },
            "dataset_version": row["dataset_version"],
            "observed_at": row["observed_at"],
        })
    return str(rows[0]["dataset_version"]), result


def write_markdown(dataset_version: str, result: list[dict[str, Any]]) -> None:
    """Write a compact human-readable report with a complete JSONL companion."""

    deep = sum(record["detail_status"] == "ok" for record in result)
    compare = sum(record["compare"]["status"] is not None for record in result)
    categories: Counter[str] = Counter()
    for record in result:
        categories.update(record["compare"]["modification_categories"])
    lines = [
        "# DeepSeek Harness Fork Network",
        "",
        f"- Dataset version: `{dataset_version}`",
        f"- Public Fork records: **{len(result):,}**",
        f"- Deep-scanned in this snapshot: **{deep:,}**; compare responses: **{compare:,}**",
        "- Scope: public Forks returned by GitHub REST API pagination for `deepseek-ai/deepseek-harness`.",
        "- Raw evidence is collected under `data/raw/forks/`; the compressed SQLite snapshot `data/aggregator-full.sqlite3.zst` includes the fork tables and raw JSON payloads. Unpack it with `zstd -d data/aggregator-full.sqlite3.zst -o aggregator-full.sqlite3`.",
        "- Complete machine-readable ranking: `index/forks.jsonl`.",
        "- The score is an ordering aid, not a quality or security claim. Stars, forks, watchers, activity, divergence, and changed-file counts remain separate.",
        "",
        "## Modification categories",
        "",
        "| Category | Changed paths |",
        "| --- | ---: |",
    ]
    lines.extend(f"| {name} | {count:,} |" for name, count in categories.most_common())
    lines.extend([
        "",
        "## Influence order",
        "",
        "| Rank | Fork | Stars | Forks | Ahead | Changed files | Deep status | Score |",
        "| ---: | --- | ---: | ---: | ---: | ---: | --- | ---: |",
    ])
    for record in result[:200]:
        compare_data = record["compare"]
        lines.append(
            f"| {record['rank']} | [{record['full_name']}]({record['url']}) | "
            f"{record['stars'] if record['stars'] is not None else '—'} | "
            f"{record['forks'] if record['forks'] is not None else '—'} | "
            f"{compare_data['ahead_by'] if compare_data['ahead_by'] is not None else '—'} | "
            f"{compare_data['changed_files'] if compare_data['changed_files'] is not None else '—'} | "
            f"{record['detail_status']} | {record['influence']['score']:.3f} |"
        )
    if len(result) > 200:
        lines.extend(["", f"> Showing the first 200 rows here; `{len(result):,}` rows are preserved in `index/forks.jsonl` and `docs/data/forks.json`." ] )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "The collector records every public Fork returned by the paginated endpoint. Deep compare, recent commits, and README metadata are rotated by a per-run budget because GitHub rate limits make an unbounded daily deep audit impractical for a network of this size. Use `python3 scripts/collect_forks.py --deep-scan-all` only when the available token and request budget are sufficient.",
        "",
    ])
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    """Build all Fork projections."""

    with connect() as connection:
        dataset_version, result = records(connection)
    if not result:
        INDEX_PATH.write_text("", encoding="utf-8")
        JSON_PATH.write_text("[]\n", encoding="utf-8")
        DOC_PATH.write_text("# DeepSeek Harness Fork Network\n\nNo Fork ranking is available yet.\n", encoding="utf-8")
        print("no fork ranking available")
        return 0
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text("".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in result), encoding="utf-8")
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps({"dataset_version": dataset_version, "records": result}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(dataset_version, result)
    print(f"built Fork index: {len(result):,} records in {dataset_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
