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
- `docs/index.html`, `docs/skills/`, `docs/data/catalog.json`, `docs/timeline.html`, `docs/categories.html`, `docs/sources.html`, `docs/robots.txt`, `docs/sitemap.xml`, and `docs/CNAME` are generated projections. Run `python3 scripts/build_views.py`; do not hand-edit generated HTML or catalog data.
- A store detail page uses the stable registry id (`skills/id-<n>.html`) and must display its dataset version, first/last seen dates, native platform metrics, public source URL, and media rights note when available.
- Third-party media remains an external URL reference unless permission is recorded. The site must never present missing interaction values as zero or combine metrics from different platforms.
- Hostinger only supplies DNS for `deeplugin.store`; GitHub Pages hosts the static files. Google Search Console verification and sitemap submission are manual account actions documented in `docs/seo.md`.
