#!/usr/bin/env python3
"""Build the public Fork ranking projection from SQLite."""

from __future__ import annotations

import html
import json
import math
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any

import build_site


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
INDEX_PATH = ROOT / "index" / "forks.jsonl"
JSON_PATH = ROOT / "docs" / "data" / "forks.json"
CATALOG_PATH = ROOT / "docs" / "data" / "fork-catalog.json"
DOC_PATH = ROOT / "docs" / "forks.md"
HTML_PATH = ROOT / "docs" / "forks.html"
CONFIG_PATH = ROOT / "config" / "forks.json"


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


def score_text(value: object, digits: int = 3) -> str:
    """Format an optional ranking score without converting NULL to zero."""

    return "—" if value is None else f"{float(value):.{digits}f}"


def records(connection: sqlite3.Connection) -> tuple[str, list[dict[str, Any]]]:
    """Read the latest successful Fork ranking run."""

    rows = connection.execute(
        """
        SELECT
            fr.rank, fr.fork_id, fr.collection_run_id, fr.ranking_version,
            fr.observed_at, fr.influence_score, fr.overall_score, fr.reputation_score,
            fr.reputation_coverage, fr.reputation_status, fr.repository_weight,
            fr.reputation_weight, fr.stars_component,
            fr.forks_component, fr.watchers_component, fr.activity_component,
            fr.divergence_component, fr.change_component, fr.rationale,
            fr.components_json, cr.dataset_version,
            fp.full_name, fp.html_url, fp.owner_login, fp.owner_type,
            fp.owner_profile_id, fp.owner_profile_status, fp.owner_profile_checked_at,
            fp.description, fp.parent_full_name, fp.source_full_name,
            fp.default_branch, fp.archived, fp.disabled, fp.stars, fp.forks,
            fp.open_issues, fp.watchers, fp.subscribers, fp.pushed_at,
            fp.updated_at, fp.last_deep_checked_at, fp.detail_status,
            fs.compare_status, fs.ahead_by, fs.behind_by, fs.total_commits,
            fs.changed_files, fs.additions, fs.deletions, fs.change_summary,
            fs.modification_categories, fs.latest_commit_sha,
            fs.latest_commit_message, fs.latest_commit_at, fs.readme_sha,
            fs.id AS snapshot_id, fs.status AS snapshot_status, fs.notes AS snapshot_notes
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
            "owner_profile": {
                "id": row["owner_profile_id"],
                "status": row["owner_profile_status"],
                "checked_at": row["owner_profile_checked_at"],
            },
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
            "change_summary": row["change_summary"],
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
                "score": row["overall_score"],
                "repository_influence_score": row["influence_score"],
                "reputation_score": row["reputation_score"],
                "reputation_coverage": row["reputation_coverage"],
                "reputation_status": row["reputation_status"],
                "repository_weight": row["repository_weight"],
                "reputation_weight": row["reputation_weight"],
                "components": {
                    "stars": row["stars_component"],
                    "forks": row["forks_component"],
                    "watchers": row["watchers_component"],
                    "activity": row["activity_component"],
                    "divergence": row["divergence_component"],
                    "changes": row["change_component"],
                },
                "reputation_components": {
                    "followers": components.get("components", {}).get("followers"),
                    "public_repos": components.get("components", {}).get("public_repos"),
                    "account_age": components.get("components", {}).get("account_age"),
                    "public_gists": components.get("components", {}).get("public_gists"),
                    "following": components.get("components", {}).get("following"),
                },
                "raw_components": components.get("raw_metrics", {}),
                "ranking_version": row["ranking_version"],
                "rationale": row["rationale"],
            },
            "dataset_version": row["dataset_version"],
            "observed_at": row["observed_at"],
        })
    return str(rows[0]["dataset_version"]), result


def attach_audit_details(connection: sqlite3.Connection, result: list[dict[str, Any]]) -> None:
    """Attach the latest retained file and commit evidence to each Fork record."""

    files_by_fork: dict[int, list[dict[str, Any]]] = {}
    file_rows = connection.execute(
        """
        WITH latest_deep AS (
            SELECT id, fork_id,
                   ROW_NUMBER() OVER (PARTITION BY fork_id ORDER BY observed_at DESC, id DESC) AS row_number
            FROM fork_snapshots
            WHERE status IN ('ok', 'partial')
        )
        SELECT ld.fork_id, ffc.filename, ffc.status, ffc.additions,
               ffc.deletions, ffc.changes, ffc.previous_filename,
               ffc.category, ffc.blob_url, ffc.raw_url
        FROM latest_deep AS ld
        JOIN fork_file_changes AS ffc ON ffc.snapshot_id = ld.id
        WHERE ld.row_number = 1
        ORDER BY ld.fork_id, ffc.filename
        """
    ).fetchall()
    for row in file_rows:
        files_by_fork.setdefault(int(row["fork_id"]), []).append({
            "filename": row["filename"],
            "status": row["status"],
            "additions": row["additions"],
            "deletions": row["deletions"],
            "changes": row["changes"],
            "previous_filename": row["previous_filename"],
            "category": row["category"],
            "blob_url": row["blob_url"],
            "raw_url": row["raw_url"],
        })

    commits_by_fork: dict[int, list[dict[str, Any]]] = {}
    commit_rows = connection.execute(
        """
        SELECT fork_id, sha, html_url, message, author_login, committer_login,
               authored_at, committed_at, first_seen_at, last_seen_at
        FROM fork_commits
        ORDER BY fork_id, COALESCE(committed_at, authored_at) DESC, id DESC
        """
    ).fetchall()
    for row in commit_rows:
        values = commits_by_fork.setdefault(int(row["fork_id"]), [])
        if len(values) >= 10:
            continue
        values.append({
            "sha": row["sha"],
            "url": row["html_url"],
            "message": row["message"],
            "author": row["author_login"],
            "committer": row["committer_login"],
            "authored_at": row["authored_at"],
            "committed_at": row["committed_at"],
            "first_seen_at": row["first_seen_at"],
            "last_seen_at": row["last_seen_at"],
        })

    for record in result:
        fork_id = int(record["fork_id"])
        files = files_by_fork.get(fork_id, [])
        observed_count = record["compare"]["changed_files"]
        record["audit"] = {
            "files_indexed": len(files),
            "files_truncated": observed_count is not None and int(observed_count) > len(files),
            "changed_files": files,
            "recent_commits": commits_by_fork.get(fork_id, []),
        }


def assign_github_star_ranks(result: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Add GitHub-native star ordering while preserving the composite ranking."""

    ordered = sorted(
        result,
        key=lambda record: (
            -int(record.get("stars") or 0),
            -int(record.get("forks") or 0),
            str(record["full_name"]).lower(),
        ),
    )
    for rank, record in enumerate(ordered, 1):
        record["github_star_rank"] = rank
    return ordered


def coverage_summary(connection: sqlite3.Connection, config: dict[str, Any]) -> dict[str, Any]:
    """Build current deep-audit coverage, queue, and conservative completion ETA."""

    latest_run = connection.execute(
        """
        SELECT id
        FROM collection_runs
        WHERE trigger = 'forks' AND status = 'succeeded'
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()
    latest_run_id = int(latest_run["id"]) if latest_run is not None else None
    historical_observed = int(connection.execute("SELECT COUNT(*) FROM fork_repositories").fetchone()[0])
    row = connection.execute(
        """
        SELECT COUNT(*) AS observed,
               SUM(last_deep_checked_at IS NOT NULL) AS audited,
               SUM(last_deep_checked_at IS NULL) AS pending,
               SUM(detail_status = 'ok') AS complete,
               SUM(detail_status = 'partial') AS partial,
               MIN(last_deep_checked_at) AS first_audited_at,
               MAX(last_deep_checked_at) AS last_audited_at
        FROM fork_repositories
        WHERE last_seen_run_id = ?
        """,
        (latest_run_id,),
    ).fetchone()
    observed = int(row["observed"] or 0)
    audited = int(row["audited"] or 0)
    pending = int(row["pending"] or 0)
    deep_limit = max(1, int(config.get("deep_scan_limit", 1000)))
    recheck_fraction = min(1.0, max(0.0, float(config.get("changed_recheck_fraction", 0.2))))
    guaranteed_backfill = max(1, int(deep_limit * (1.0 - recheck_fraction)))
    queue_rows = connection.execute(
        """
        SELECT full_name, html_url, stars, forks, pushed_at, last_deep_checked_at
        FROM fork_repositories
        WHERE last_seen_run_id = ?
          AND last_deep_checked_at IS NULL
        ORDER BY COALESCE(stars, 0) DESC, COALESCE(forks, 0) DESC, full_name
        LIMIT 200
        """,
        (latest_run_id,),
    ).fetchall()
    changed_rows = connection.execute(
        """
        SELECT full_name, html_url, stars, forks, pushed_at, last_deep_checked_at
        FROM fork_repositories
        WHERE last_seen_run_id = ?
          AND last_deep_checked_at IS NOT NULL
          AND pushed_at IS NOT NULL
          AND pushed_at > last_deep_checked_at
        ORDER BY COALESCE(stars, 0) DESC, COALESCE(forks, 0) DESC, full_name
        LIMIT 200
        """,
        (latest_run_id,),
    ).fetchall()

    def queue_record(value: sqlite3.Row) -> dict[str, Any]:
        return {
            "full_name": value["full_name"],
            "url": value["html_url"],
            "stars": value["stars"],
            "forks": value["forks"],
            "pushed_at": value["pushed_at"],
            "last_deep_checked_at": value["last_deep_checked_at"],
        }

    return {
        "observed": observed,
        "historical_observed": historical_observed,
        "inactive_or_missing": max(0, historical_observed - observed),
        "audited": audited,
        "pending": pending,
        "complete": int(row["complete"] or 0),
        "partial": int(row["partial"] or 0),
        "coverage_percent": round(100 * audited / observed, 2) if observed else 0.0,
        "first_audited_at": row["first_audited_at"],
        "last_audited_at": row["last_audited_at"],
        "daily_deep_scan_limit": deep_limit,
        "changed_recheck_fraction": recheck_fraction,
        "guaranteed_daily_backfill": guaranteed_backfill,
        "estimated_backfill_days": math.ceil(pending / guaranteed_backfill) if pending else 0,
        "next_never_scanned": [queue_record(value) for value in queue_rows],
        "changed_since_audit": [queue_record(value) for value in changed_rows],
    }


def catalog_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return the compact fields needed by the public Fork browser."""

    return {
        "fork_id": record["fork_id"],
        "rank": record["rank"],
        "github_star_rank": record["github_star_rank"],
        "full_name": record["full_name"],
        "url": record["url"],
        "description": record["description"],
        "stars": record["stars"],
        "forks": record["forks"],
        "pushed_at": record["pushed_at"],
        "detail_status": record["detail_status"],
        "last_deep_checked_at": record["last_deep_checked_at"],
        "change_summary": record["change_summary"],
        "compare": record["compare"],
        "influence": {
            "score": record["influence"]["score"],
            "repository_influence_score": record["influence"]["repository_influence_score"],
            "reputation_score": record["influence"]["reputation_score"],
            "reputation_status": record["influence"]["reputation_status"],
        },
        "audit": record["audit"],
    }


def fork_row_html(record: dict[str, Any]) -> str:
    """Render one crawlable initial row for the Fork browser."""

    stars = "—" if record["stars"] is None else f"{int(record['stars']):,}"
    ahead = record["compare"]["ahead_by"]
    changed = record["compare"]["changed_files"]
    status = "audited" if record["last_deep_checked_at"] else "pending"
    return (
        f'<tr data-fork-id="{int(record["fork_id"])}">'
        f'<td>{int(record["github_star_rank"]):,}</td>'
        f'<td><a href="{html.escape(str(record["url"]), quote=True)}" rel="noreferrer">{html.escape(str(record["full_name"]))}</a>'
        f'<small>{html.escape(str(record["change_summary"] or record["description"] or "No public description"))}</small></td>'
        f'<td>{stars}</td><td>{score_text(record["influence"]["score"])}</td>'
        f'<td>{ahead if ahead is not None else "—"}</td><td>{changed if changed is not None else "—"}</td>'
        f'<td><span class="fork-status fork-status-{status}">{status}</span></td>'
        f'<td><button class="fork-inspect" type="button" data-fork-id="{int(record["fork_id"])}">查看盘点</button></td></tr>'
    )


def render_fork_page(
    dataset_version: str,
    result: list[dict[str, Any]],
    coverage: dict[str, Any],
    star_order: list[dict[str, Any]],
) -> str:
    """Render the searchable Fork inventory backed by the compact JSON catalog."""

    site_config = build_site.read_config()
    site_url = site_config["site_url"].rstrip("/")
    head = build_site.page_head(
        "DeepSeek Harness Fork inventory — dsh store",
        "All public DeepSeek Harness Forks, ordered by GitHub stars and composite public influence with dated change audits.",
        site_url + "/forks.html",
        site_url + "/media/screenshots/official.png",
        site_config,
        extra_json_ld={"@type": "CollectionPage", "name": "DeepSeek Harness Fork inventory"},
    ).replace("{ASSET_PREFIX}", "")
    initial_rows = "".join(fork_row_html(record) for record in star_order[:100])
    return f"""{head}<body class="fork-page">
{build_site.nav_html()}
<main class="site-main table-main">
  <div class="breadcrumbs"><a href="">store</a><span>/</span><span>Forks</span></div>
  <section class="page-intro fork-intro"><p class="kicker">PUBLIC FORK NETWORK · {html.escape(dataset_version)}</p><h1>DeepSeek Harness Forks</h1><p>公开 Fork 全量登记、原生影响力顺序与逐仓库变更证据。</p></section>
  <section class="fork-stats" aria-label="Fork audit coverage">
    <div><strong>{int(coverage['observed']):,}</strong><span>public Forks</span></div>
    <div><strong>{int(coverage['audited']):,}</strong><span>audited</span></div>
    <div><strong>{coverage['coverage_percent']:.2f}%</strong><span>coverage</span></div>
    <div><strong>{int(coverage['estimated_backfill_days']):,}</strong><span>estimated days</span></div>
  </section>
  <section class="fork-browser">
    <div class="fork-toolbar">
      <label class="search-field"><span aria-hidden="true">⌕</span><input id="fork-search" type="search" placeholder="Search owner, repository, summary..." autocomplete="off"></label>
      <div class="fork-modes" role="group" aria-label="Fork ordering">
        <button class="is-selected" type="button" data-mode="stars">GitHub stars</button>
        <button type="button" data-mode="influence">综合影响力</button>
        <button type="button" data-mode="audited">已盘点</button>
        <button type="button" data-mode="pending">待盘点</button>
      </div>
    </div>
    <div class="table-caption" id="fork-result-summary"><strong>{len(result):,}</strong> records · showing GitHub star order</div>
    <div class="table-scroll"><table class="data-table fork-table"><thead><tr><th>Star rank</th><th>Fork / evidence</th><th>Stars</th><th>Influence</th><th>Ahead</th><th>Files</th><th>Audit</th><th></th></tr></thead><tbody id="fork-table-body">{initial_rows}</tbody></table></div>
    <div class="fork-pagination"><button id="fork-prev" type="button" disabled>上一页</button><span id="fork-page-label">1</span><button id="fork-next" type="button">下一页</button></div>
  </section>
  <section class="fork-dossier" id="fork-dossier" hidden aria-live="polite"></section>
</main>
    {build_site.footer_html(data_path=build_site.read_config()["public_database_url"])}
<script>
(() => {{
  const state = {{ records: [], filtered: [], mode: 'stars', query: '', page: 0, pageSize: 100 }};
  const body = document.getElementById('fork-table-body');
  const summary = document.getElementById('fork-result-summary');
  const dossier = document.getElementById('fork-dossier');
  const pageLabel = document.getElementById('fork-page-label');
  const previous = document.getElementById('fork-prev');
  const next = document.getElementById('fork-next');
  const escapeHtml = value => String(value ?? '').replace(/[&<>\"']/g, character => ({{'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}})[character]);
  const number = value => value === null || value === undefined ? '—' : Number(value).toLocaleString();
  const score = value => value === null || value === undefined ? '—' : Number(value).toFixed(3);
  const date = value => value ? String(value).slice(0, 10) : '—';
  const safeUrl = value => String(value || '').startsWith('https://') ? escapeHtml(value) : '#';
  const row = record => `<tr data-fork-id="${{record.fork_id}}"><td>${{number(record.github_star_rank)}}</td><td><a href="${{safeUrl(record.url)}}" rel="noreferrer">${{escapeHtml(record.full_name)}}</a><small>${{escapeHtml(record.change_summary || record.description || 'No public description')}}</small></td><td>${{number(record.stars)}}</td><td>${{score(record.influence.score)}}</td><td>${{number(record.compare.ahead_by)}}</td><td>${{number(record.compare.changed_files)}}</td><td><span class="fork-status fork-status-${{record.last_deep_checked_at ? 'audited' : 'pending'}}">${{record.last_deep_checked_at ? 'audited' : 'pending'}}</span></td><td><button class="fork-inspect" type="button" data-fork-id="${{record.fork_id}}">查看盘点</button></td></tr>`;
  const compare = (left, right) => left === right ? 0 : left < right ? -1 : 1;
  function apply() {{
    const query = state.query.toLowerCase();
    state.filtered = state.records.filter(record => !query || `${{record.full_name}} ${{record.description || ''}} ${{record.change_summary || ''}}`.toLowerCase().includes(query));
    if (state.mode === 'pending') state.filtered = state.filtered.filter(record => !record.last_deep_checked_at);
    if (state.mode === 'audited') state.filtered = state.filtered.filter(record => record.last_deep_checked_at);
    const key = state.mode === 'influence' ? 'rank' : 'github_star_rank';
    state.filtered.sort((left, right) => compare(Number(left[key] || 999999), Number(right[key] || 999999)) || compare(left.full_name, right.full_name));
    state.page = Math.min(state.page, Math.max(0, Math.ceil(state.filtered.length / state.pageSize) - 1));
    render();
  }}
  function render() {{
    const start = state.page * state.pageSize;
    const visible = state.filtered.slice(start, start + state.pageSize);
    body.innerHTML = visible.map(row).join('');
    const pages = Math.max(1, Math.ceil(state.filtered.length / state.pageSize));
    summary.innerHTML = `<strong>${{number(state.filtered.length)}}</strong> records · ${{state.mode === 'influence' ? 'composite influence order' : state.mode === 'audited' ? 'audited Forks' : state.mode === 'pending' ? 'pending audit queue' : 'GitHub star order'}}`;
    pageLabel.textContent = `${{state.page + 1}} / ${{pages}}`;
    previous.disabled = state.page === 0;
    next.disabled = state.page + 1 >= pages;
  }}
  function inspect(id) {{
    const record = state.records.find(value => Number(value.fork_id) === Number(id));
    if (!record) return;
    const files = record.audit.changed_files || [];
    const commits = record.audit.recent_commits || [];
    const fileRows = files.slice(0, 100).map(file => `<tr><td><a href="${{safeUrl(file.blob_url)}}" rel="noreferrer">${{escapeHtml(file.filename)}}</a></td><td>${{escapeHtml(file.category)}}</td><td>+${{number(file.additions)}} / -${{number(file.deletions)}}</td></tr>`).join('');
    const commitRows = commits.map(commit => `<li><a href="${{safeUrl(commit.url)}}" rel="noreferrer"><code>${{escapeHtml(String(commit.sha || '').slice(0, 8))}}</code> ${{escapeHtml(commit.message || 'Commit')}}</a><time>${{date(commit.committed_at || commit.authored_at)}}</time></li>`).join('');
    dossier.innerHTML = `<div class="fork-dossier-head"><div><p class="kicker">FORK DOSSIER</p><h2>${{escapeHtml(record.full_name)}}</h2></div><a class="button button-primary" href="${{safeUrl(record.url)}}" rel="noreferrer">Open GitHub ↗</a></div><p class="fork-summary">${{escapeHtml(record.change_summary || record.description || 'No public description')}}</p><dl class="fork-facts"><div><dt>Last audit</dt><dd>${{date(record.last_deep_checked_at)}}</dd></div><div><dt>Compare</dt><dd>${{escapeHtml(record.compare.status || 'pending')}}</dd></div><div><dt>Ahead / behind</dt><dd>${{number(record.compare.ahead_by)}} / ${{number(record.compare.behind_by)}}</dd></div><div><dt>Additions / deletions</dt><dd>+${{number(record.compare.additions)}} / -${{number(record.compare.deletions)}}</dd></div></dl><div class="fork-evidence-grid"><section><h3>Changed files · ${{number(record.audit.files_indexed)}}</h3>${{fileRows ? `<div class="table-scroll"><table class="data-table"><thead><tr><th>Path</th><th>Area</th><th>Delta</th></tr></thead><tbody>${{fileRows}}</tbody></table></div>` : '<p class="fork-empty">No file-level evidence has been indexed yet.</p>'}}</section><section><h3>Recent commits · ${{number(commits.length)}}</h3>${{commitRows ? `<ol class="fork-commits">${{commitRows}}</ol>` : '<p class="fork-empty">No commit evidence has been indexed yet.</p>'}}</section></div>`;
    dossier.hidden = false;
    dossier.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }}
  document.getElementById('fork-search').addEventListener('input', event => {{ state.query = event.target.value.trim(); state.page = 0; apply(); }});
  document.querySelector('.fork-modes').addEventListener('click', event => {{ const button = event.target.closest('button[data-mode]'); if (!button) return; document.querySelectorAll('.fork-modes button').forEach(value => value.classList.toggle('is-selected', value === button)); state.mode = button.dataset.mode; state.page = 0; apply(); }});
  body.addEventListener('click', event => {{ const button = event.target.closest('.fork-inspect'); if (button) inspect(button.dataset.forkId); }});
  previous.addEventListener('click', () => {{ if (state.page > 0) {{ state.page -= 1; render(); }} }});
  next.addEventListener('click', () => {{ if ((state.page + 1) * state.pageSize < state.filtered.length) {{ state.page += 1; render(); }} }});
  fetch('data/fork-catalog.json').then(response => {{ if (!response.ok) throw new Error(`HTTP ${{response.status}}`); return response.json(); }}).then(payload => {{ state.records = payload.records || []; apply(); }}).catch(error => {{ summary.textContent = `Catalog load failed: ${{error.message}}`; }});
}})();
</script>
</body></html>"""


def write_markdown(
    dataset_version: str,
    result: list[dict[str, Any]],
    star_filter: dict[str, Any],
    coverage: dict[str, Any],
    star_order: list[dict[str, Any]],
) -> None:
    """Write a compact human-readable report with a complete JSONL companion."""

    deep = sum(record["detail_status"] == "ok" for record in result)
    compare = sum(record["compare"]["status"] is not None for record in result)
    reputation_observed = sum(record["influence"]["reputation_status"] in {"observed", "partial"} for record in result)
    categories: Counter[str] = Counter()
    for record in result:
        categories.update(record["compare"]["modification_categories"])
    lines = [
        "# DeepSeek Harness Fork Network",
        "",
        f"- Dataset version: `{dataset_version}`",
        f"- Public Fork records: **{len(result):,}**",
        f"- Ranking filter: **{star_filter.get('minimum_stars', 0):,}+ stars**; observed Fork identities: **{star_filter.get('observed_forks', len(result)):,}**; filtered out of ranking: **{star_filter.get('filtered_out', 0):,}**.",
        f"- Ever deep-scanned: **{coverage['audited']:,} / {coverage['observed']:,}** ({coverage['coverage_percent']:.2f}%); pending: **{coverage['pending']:,}**; conservative backfill ETA: **{coverage['estimated_backfill_days']:,} daily runs**.",
        f"- Deep-scanned successfully in the current projection: **{deep:,}**; compare responses retained: **{compare:,}**",
        f"- Fork rows with public owner reputation observed: **{reputation_observed:,}**; the current ranking pool applies a configurable minimum-Star filter.",
        "- Scope: public Forks returned by GitHub REST API pagination for `deepseek-ai/deepseek-harness`.",
        f"- Raw evidence is collected under `data/raw/forks/`; the [latest compressed SQLite snapshot]({build_site.read_config()['full_database_url']}) includes the fork tables and raw JSON payloads. Unpack it with `zstd -d aggregator-full.sqlite3.zst -o aggregator-full.sqlite3`.",
        "- Searchable browser: `docs/forks.html`; compact catalog: `docs/data/fork-catalog.json`; complete machine-readable ranking: `index/forks.jsonl`.",
        "- `overall score = repository influence 60% + public-account reputation 40%` when the profile is observed; missing profile signals are not treated as zero. This is a public-signal ordering aid, not a quality, safety, integrity, or endorsement claim.",
        "",
        "## GitHub star order",
        "",
        "| Star rank | Fork | Stars | Composite rank | Audit | Evidence |",
        "| ---: | --- | ---: | ---: | --- | --- |",
    ]
    for record in star_order[:100]:
        lines.append(
            f"| {record['github_star_rank']} | [{record['full_name']}]({record['url']}) | "
            f"{record['stars'] if record['stars'] is not None else '—'} | {record['rank']} | "
            f"{'audited' if record['last_deep_checked_at'] else 'pending'} | {record['change_summary'] or '—'} |"
        )
    lines.extend([
        "",
        "## Modification categories",
        "",
        "| Category | Changed paths |",
        "| --- | ---: |",
    ])
    lines.extend(f"| {name} | {count:,} |" for name, count in categories.most_common())
    lines.extend([
        "",
        "## Influence order",
        "",
        "| Rank | Fork | Stars | Owner reputation | Repo influence | Overall | Ahead | Changed files | Deep status | One-sentence evidence |",
        "| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ])
    for record in result[:200]:
        compare_data = record["compare"]
        lines.append(
            f"| {record['rank']} | [{record['full_name']}]({record['url']}) | "
            f"{record['stars'] if record['stars'] is not None else '—'} | "
            f"{score_text(record['influence']['reputation_score'], 1)} ({record['influence']['reputation_status']}) | "
            f"{score_text(record['influence']['repository_influence_score'])} | "
            f"{score_text(record['influence']['score'])} | "
            f"{compare_data['ahead_by'] if compare_data['ahead_by'] is not None else '—'} | "
            f"{compare_data['changed_files'] if compare_data['changed_files'] is not None else '—'} | "
            f"{record['detail_status']} | {record['change_summary'] or '—'} |"
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

    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        config = {}
    with connect() as connection:
        dataset_version, result = records(connection)
        attach_audit_details(connection, result)
        coverage = coverage_summary(connection, config)
        observed_forks = int(coverage["observed"])
    star_order = assign_github_star_ranks(result)
    star_filter = {
        "minimum_stars": max(0, int(config.get("min_stars", 0))),
        "observed_forks": observed_forks,
        "eligible_forks": len(result),
        "filtered_out": max(0, observed_forks - len(result)),
    }
    if not result:
        INDEX_PATH.write_text("", encoding="utf-8")
        empty = {"schema_version": 1, "dataset_version": dataset_version, "coverage": coverage, "star_filter": star_filter, "records": []}
        JSON_PATH.write_text(json.dumps(empty, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        CATALOG_PATH.write_text(json.dumps(empty, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        DOC_PATH.write_text("# DeepSeek Harness Fork Network\n\nNo Fork ranking is available yet.\n", encoding="utf-8")
        print("no fork ranking available")
        return 0
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text("".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in result), encoding="utf-8")
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema_version": 1, "dataset_version": dataset_version, "coverage": coverage, "star_filter": star_filter, "records": result}
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    catalog = {**{key: value for key, value in payload.items() if key != "records"}, "records": [catalog_record(record) for record in result]}
    CATALOG_PATH.write_text(json.dumps(catalog, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    write_markdown(dataset_version, result, star_filter, coverage, star_order)
    HTML_PATH.write_text(render_fork_page(dataset_version, result, coverage, star_order), encoding="utf-8")
    print(f"built Fork index: {len(result):,} records in {dataset_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
