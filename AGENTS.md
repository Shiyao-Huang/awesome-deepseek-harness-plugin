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

`data/raw/` is the physical raw namespace. The short name `raw` in issue descriptions and collection notes refers to this directory. `index/` is the registration namespace described below. `data/aggregator.sqlite3` is the queryable database and must contain the same registration fields as `index/records.jsonl`.

## Raw Evidence

- A raw file is the original public response or visible DOM capture, not a rewritten summary.
- Raw files are immutable after import. A changed page creates a new dated file.
- Every raw file must have a UTC collection time, source URL, collector, method, status, and SHA-256 recorded in SQLite.
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

The public GitHub Actions workflow runs every two hours at minute 17 UTC. It collects sources that expose a permitted public API, writes a dated raw snapshot, imports it, rebuilds the index and docs, validates the database, and commits only the resulting data changes. Browser-only sources such as X, Xiaohongshu, Reddit, and WeChat require a fresh permitted ego-browser capture and are imported with `--raw`.

The DeepSeek Harness Fork network has a separate daily workflow at `.github/workflows/refresh-forks.yml`. It enumerates every public page from `https://api.github.com/repos/deepseek-ai/deepseek-harness/forks`, stores each page under `data/raw/forks/<UTC timestamp>/`, and upserts the public Fork identities into `fork_repositories`. The complete list is the observable GitHub API result at collection time; private, deleted, or inaccessible repositories are outside the dataset.

Fork metadata and native metrics are historical in `fork_snapshots`. Deep compare results, recent commits, README metadata, and changed-file categories are rotated by the configured deep-scan budget and remain `NULL` or `metadata-only` until that Fork is selected. `--deep-scan-all` is available for a sufficiently provisioned authenticated run, but a missing compare response must never be interpreted as no code change.

Fork influence ranking is deterministic and versioned in `fork_rankings`. The current scoring configuration is `config/forks.json`; raw GitHub values are preserved separately from the score, and the score is not a quality, security, compatibility, or official-endorsement claim. Rebuild `index/forks.jsonl` and `docs/forks.md` with `python3 scripts/build_fork_index.py` after importing a Fork snapshot.

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

- `config/site.json` is the single deployment configuration for the public store. The current canonical URL is `https://deeplugin.store` and the GitHub Pages source is `main:/docs`.
- `docs/index.html`, `docs/skills/`, `docs/data/catalog.json`, `docs/timeline.html`, `docs/categories.html`, `docs/sources.html`, `docs/robots.txt`, `docs/sitemap.xml`, and `docs/CNAME` are generated projections. Run `python3 scripts/build_views.py`; `README.md` landing and snapshot blocks are generated by `python3 scripts/build_readme.py`; do not hand-edit generated HTML, catalog data, or marked README blocks.
- A store detail page uses the stable registry id (`skills/id-<n>.html`) and must display its dataset version, first/last seen dates, native platform metrics, public source URL, and media rights note when available.
- Third-party media remains an external URL reference unless permission is recorded. The site must never present missing interaction values as zero or combine metrics from different platforms.
- Hostinger only supplies DNS for `deeplugin.store`; GitHub Pages hosts the static files. Google Search Console verification and sitemap submission are manual account actions documented in `docs/seo.md`.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **awesome-deepseek-harness-plugin** (11687 symbols, 12356 relationships, 49 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

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
