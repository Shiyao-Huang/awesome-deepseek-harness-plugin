# Workspace Rules

This repository is a public, append-only research aggregator for the DeepSeek Harness plugin ecosystem. The rules in this file apply to every collection, import, index rebuild, schedule, and documentation update.

## Workspace Layout

```text
data/raw/       raw evidence: complete JSON captures, grouped by source
index/          generated item registry and its schema
data/           SQLite database and data-layer documentation
scripts/        collectors, importers, validators, and index builders
docs/           generated human-readable projections
media/          locally stored screenshots or thumbnails with rights notes
config/         source lists and collection limits
```

`data/raw/` is the physical raw namespace. The short name `raw` in issue descriptions and collection notes refers to this directory. `index/` is the registration namespace described below. The release asset `aggregator.sqlite3` is the queryable public projection and must contain the same registration fields as `index/records.jsonl`; `aggregator-full.sqlite3.zst` is the compressed authoritative database.

## Raw Evidence

- A raw file is the original public response or visible DOM capture, not a rewritten summary.
- Raw files are immutable after import. A changed page creates a new dated file.
- Every raw file must have a UTC collection time, source URL, collector, method, status, and SHA-256 recorded in SQLite. The full archive retains its exact UTF-8 JSON in `raw_snapshots.payload_json`; the public projection retains SHA/path/date provenance and replaces duplicated JSON blobs with `{}`.
- The same raw SHA-256 is imported once. Re-running a command must not create another raw snapshot or another item observation for that exact file.
- Public-only collection is allowed. Do not bypass login, CAPTCHA, QR code, paywalls, rate limits, robots controls, or platform access restrictions.
- Store external media URLs and rights notes by default. Do not mirror third-party media without permission.

## Index Registration

`index/records.jsonl` is generated from SQLite and has one registration record per deduplicated item. Do not edit it manually. The normative field schema is `index/schema.json`:

```text
id, summary, url, repo, context, picture, comment, favor, views,
refs, rank, stars, dataset_version, first_seen_at, last_seen_at
```

Field meanings:

- `id`: stable registry identifier, currently `id-<items.id>`.
- `summary`: concise title or description.
- `url`: canonical public source URL.
- `repo`: repository slug when the record is a repository or names one; otherwise `null`.
- `context`: source, item type, author, category, relevance, language, and body context.
- `picture`: JSON array of public media URLs and thumbnails.
- `comment`: latest visible comment count, or `null` when not reported.
- `favor`: latest visible favorite/like count using the platform-native value.
- `views`: latest visible view count.
- `refs`: JSON array of public references extracted from the raw record.
- `rank`: deterministic ranking position in the generated registry, not a platform claim.
- `stars`: latest GitHub star count, or `null` for other platforms.
- `dataset_version`, `first_seen_at`, and `last_seen_at`: database-managed snapshot and date fields.

The SQLite table `index_records` mirrors these fields. The `raw_snapshots`, `observations`, and `item_observations` tables remain the provenance path from a registration back to its original evidence.

## Versioning, Dates, and Deduplication

- Every import creates a `collection_runs` row with a sortable UTC `dataset_version`, start/end dates, trigger, status, and counters.
- Items are unique by canonical URL and platform/external ID. Do not insert a second row for the same public object.
- Media is unique by item, media kind, and URL.
- Dated observation and metric rows are historical snapshots. They may repeat a value when a later collection run confirms the same public state; they must retain their collection date and dataset version.
- Missing interaction numbers are `NULL`, never an invented zero.
- A failed run remains in `collection_runs` with `status=error`; do not hide failures by deleting the run.
- Generated docs and `index/records.jsonl` must be rebuilt after a successful import.

## Schedule

The public GitHub Actions workflow runs every two hours at minute 17 UTC. It restores the latest full database, calls `make core-refresh` to collect sources that expose a permitted public API, writes dated raw snapshots, imports them, rebuilds the value matrix, index, site, trends, and README, validates both database forms, and commits only incremental raw and generated text/site changes. It overwrites the stable `dataset-latest` GitHub Release assets instead of committing a new 60+ MiB SQLite binary every two hours. Browser-only sources such as X, Xiaohongshu, Reddit, and WeChat are never collected by this unattended job; they require a fresh permitted ego-browser capture and an explicit `--raw` import.

The DeepSeek Harness Fork network has a separate daily workflow at `.github/workflows/refresh-forks.yml`. It enumerates every public page from `https://api.github.com/repos/deepseek-ai/deepseek-harness/forks`, stores each page under `data/raw/forks/<UTC timestamp>/`, rotates a bounded, owner-deduplicated set of public `GET /users/{login}` profiles, and upserts the public Fork identities into `fork_repositories`. The complete list is the observable GitHub API result at collection time; private, deleted, or inaccessible repositories are outside the dataset.

Fork metadata and native metrics are historical in `fork_snapshots`. Deep compare results, recent commits, README metadata, and changed-file categories are rotated by the configured deep-scan budget and remain `NULL` or `metadata-only` until that Fork is selected. The daily queue reserves at most `changed_recheck_fraction` for previously scanned Forks pushed after their last deep scan, then spends the remaining budget on never-scanned Forks in native GitHub influence order before rotating through stale records. `--deep-scan-all` is available for a sufficiently provisioned authenticated run, but a missing compare response must never be interpreted as no code change.

Fork ranking is deterministic and versioned in `fork_rankings`: repository influence and public-account reputation remain separate, then combine only when a profile signal is observed; `min_stars`/`--min-stars` filters the ranking pool without deleting raw Fork records. The current scoring configuration is `config/forks.json`; raw GitHub values are preserved separately from the score, and the score is not a quality, security, integrity, compatibility, or official-endorsement claim. `change_summary` is an evidence-qualified one-sentence description of observed changes and goal clues, not inferred author intent. Rebuild `index/forks.jsonl` and `docs/forks.md` with `python3 scripts/build_fork_index.py` after importing a Fork snapshot.

## Required Checks

```sh
python3 scripts/collect.py seed
python3 scripts/build_index.py
python3 scripts/build_views.py
python3 scripts/validate.py
git diff --check
```

Never use a destructive database reset or delete raw evidence to make a check pass. If a schema changes, add an idempotent migration in `scripts/collect.py:init_db` and update `index/schema.json`, this file, and the data documentation together.

## Store Website

- `config/site.json` is the single deployment configuration for the public store, canonical URL, and stable public/full database download URLs. The current canonical URL is `https://deeplugin.store` and the GitHub Pages source is `main:/docs`.
- `docs/index.html`, `docs/skills/`, `docs/data/catalog.json`, `docs/timeline.html`, `docs/categories.html`, `docs/directories.html`, `docs/sources.html`, `docs/robots.txt`, `docs/sitemap.xml`, and `docs/CNAME` are generated projections. `directories.html` lists ordinary public aggregation and discovery records. `sources.html` lists source platforms, public collection modes, aggregate counts, dates, and policy links. Neither page may expose internal monitoring repositories or query `upstream_repositories`/`upstream_entries`. Run `python3 scripts/build_views.py`; `README.md` landing and snapshot blocks are generated by `python3 scripts/build_readme.py`; do not hand-edit generated HTML, catalog data, or marked README blocks.
- A store detail page uses the stable registry id (`skills/id-<n>.html`) and must display its dataset version, first/last seen dates, native platform metrics, public source URL, and media rights note when available.
- Third-party media remains an external URL reference unless permission is recorded. The site must never present missing interaction values as zero or combine metrics from different platforms.
- Hostinger only supplies DNS for `deeplugin.store`; GitHub Pages hosts the static files. Google Search Console verification and sitemap submission are manual account actions documented in `docs/seo.md`.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **awesome-deepseek-harness-plugin** (13232 symbols, 14104 relationships, 58 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> Index stale? Run `node .gitnexus/run.cjs analyze` from the project root — it auto-selects an available runner. No `.gitnexus/run.cjs` yet? `npx gitnexus analyze` (npm 11 crash → `npm i -g gitnexus`; #1939).

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows. For regression review, compare against the default branch: `detect_changes({scope: "compare", base_ref: "main"})`.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `query({search_query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `context({name: "symbolName"})`.
- For security review, `explain({target: "fileOrSymbol"})` lists taint findings (source→sink flows; needs `analyze --pdg`).

## Never Do

- NEVER edit a function, class, or method without first running `impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `rename` which understands the call graph.
- NEVER commit changes without running `detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/awesome-deepseek-harness-plugin/context` | Codebase overview, check index freshness |
| `gitnexus://repo/awesome-deepseek-harness-plugin/clusters` | All functional areas |
| `gitnexus://repo/awesome-deepseek-harness-plugin/processes` | All execution flows |
| `gitnexus://repo/awesome-deepseek-harness-plugin/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
