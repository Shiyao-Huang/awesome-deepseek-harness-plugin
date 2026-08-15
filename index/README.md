# Index Registry

`records.jsonl` is the generated registration of every deduplicated item in `data/aggregator.sqlite3`. Its normative schema is [schema.json](schema.json). Each line is one record and can be traced through `id` to `index_records`, `items`, `item_observations`, `observations`, and `raw_snapshots`.

Rebuild it with:

```sh
python3 scripts/build_index.py
```

The registry is generated from SQLite. Do not hand-edit it; update or import raw evidence, then rebuild the registry.
