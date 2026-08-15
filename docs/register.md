# Register a DeepSeek Harness plugin

`deeplugin.store` publishes an attributed market registry, not an official trust list. A submission records what a named public source claims at a dated observation. It does not transfer ownership, certify security, or guarantee compatibility.

## Choose a route

### Register one plugin

Open a pull request that adds one contract-v2 entry to [`registry/plugins.json`](../registry/plugins.json). Keep `count` equal to the number of entries and set `updated` to the current UTC date.

### Connect another public registry

Open a pull request that adds its public GitHub repository and selected registry path or HTTPS registry URL to [`config/sources.json`](../config/sources.json). The two-hour collector stores every selected registry response as immutable raw evidence before normalizing Listings. A failed source observation never deactivates its last successful state.

## Contract v2 entry

The generated [JSON Schema](https://deeplugin.store/data/market-registry.schema.json) is authoritative for field types. The community source accepts this entry form:

```json
{
  "id": "source-local-id",
  "name": "Plugin name",
  "author": "owner",
  "category": "tools",
  "description": "One concrete English sentence.",
  "description_zh": "一条具体的中文说明。",
  "install": {
    "target": "git",
    "spec": "github:owner/repository#path:/plugin"
  },
  "version": "1.2.3",
  "homepage": "https://github.com/owner/repository/tree/main/plugin",
  "verified": false,
  "stars": null,
  "tags": ["search", "tools"],
  "source": {
    "name": "project registry",
    "url": "https://github.com/owner/repository"
  }
}
```

For an npm package, use `{"target":"npm","spec":"@scope/package"}`. GitHub specs accept only `github:owner/repository` or `github:owner/repository#path:/subdirectory`. Branches, shell operators, URLs, local paths, flags, and arbitrary commands are rejected from the public registry. Invalid source entries remain in raw and SQLite history when observed, but they cannot produce install plans.

## Field rules

| Field | Rule |
| --- | --- |
| `id` | Unique inside the source registry. It is source-local and does not become the public plugin id. |
| `name`, `author` | Public display name and author or organization. |
| `category` | A stable lowercase category such as `tools`, `skill`, `workflow`, `model`, `memory`, `ui`, `dev`, or `market`. |
| `description`, `description_zh` | Concrete behavior, without ranking or trust claims. |
| `install.target` | `git` or `npm`; it must agree with the spec. |
| `install.spec` | The exact source-declared package identity. This normalized value defines deduplication and the stable public id. |
| `version` | A declared release version or `null`. |
| `homepage` | Public HTTPS page where a reviewer can inspect the plugin. |
| `verified` | Contributors must use `false`. Curators may set `true` only with a declared version and attributable evidence; it is never a security endorsement. |
| `stars` | A source-observed GitHub value or `null`; never estimate or write zero for missing data. |
| `tags` | Short, factual search terms. |
| `source` | The public registry or project making this Listing claim. |

The public Market Plugin id is deterministic: `deeplugin-` plus the first 20 lowercase hexadecimal characters of SHA-256 over the normalized install spec. Renaming a plugin does not change that id; changing the install artifact does.

## Review checklist

1. Confirm the homepage and install artifact are public and belong to the submitted project.
2. Confirm the install spec names only one npm package or one GitHub repository and optional plugin subdirectory.
3. Keep `verified` false unless a curator supplies versioned, attributable evidence.
4. Run `python3 -m json.tool registry/plugins.json`, `python3 -m unittest tests.test_market_registry`, and `python3 scripts/build_market_registry.py` against a restored full SQLite database.
5. Do not hand-edit `index/market-registry.json`, `docs/data/market-registry.json`, or `plugin/data/market-registry.json`; the builder writes byte-identical copies.

Accepted changes enter the next successful two-hour collection. Existing Listings are deduplicated by normalized install spec while every source attribution and observation date remains queryable in SQLite.
