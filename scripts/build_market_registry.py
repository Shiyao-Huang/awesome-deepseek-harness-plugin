#!/usr/bin/env python3
"""Build the public DeepSeek Harness market registry from active Listings."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
INDEX_REGISTRY_PATH = ROOT / "index" / "market-registry.json"
DOCS_REGISTRY_PATH = ROOT / "docs" / "data" / "market-registry.json"
PLUGIN_REGISTRY_PATH = ROOT / "plugin" / "data" / "market-registry.json"
INDEX_SCHEMA_PATH = ROOT / "index" / "market-registry.schema.json"
DOCS_SCHEMA_PATH = ROOT / "docs" / "data" / "market-registry.schema.json"
PLUGIN_SCHEMA_PATH = ROOT / "plugin" / "data" / "market-registry.schema.json"
REGISTRY_URL = "https://deeplugin.store/data/market-registry.json"
SCHEMA_URL = "https://deeplugin.store/data/market-registry.schema.json"

NPM_SPEC = re.compile(r"^(?:@[a-z0-9-~][a-z0-9-._~]*/)?[a-z0-9-~][a-z0-9-._~]*$")
GITHUB_SPEC = re.compile(
    r"^github:([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:#path:(/[A-Za-z0-9._~/-]+))?$"
)
CATEGORY_LABELS = {
    "ui": {"en": "UI Enhancements", "zh": "UI 增强"},
    "theme": {"en": "Themes & Appearance", "zh": "主题与外观"},
    "model": {"en": "Models & Providers", "zh": "模型与账号接入"},
    "session": {"en": "Sessions & Messages", "zh": "会话与消息"},
    "memory": {"en": "Memory", "zh": "记忆"},
    "tools": {"en": "Tools & Capabilities", "zh": "工具与能力"},
    "skill": {"en": "Skills", "zh": "技能包"},
    "workflow": {"en": "Workflow & Automation", "zh": "工作流与自动化"},
    "notify": {"en": "Notifications & Integrations", "zh": "通知与集成"},
    "dev": {"en": "Development & Runtime", "zh": "开发与运行时"},
    "market": {"en": "Market", "zh": "市场"},
    "fun": {"en": "Just for Fun", "zh": "娱乐"},
}


def json_object(value: Any) -> dict[str, Any]:
    """Decode a stored JSON object without accepting other JSON types."""

    try:
        decoded = json.loads(value or "{}")
    except (TypeError, json.JSONDecodeError):
        return {}
    return decoded if isinstance(decoded, dict) else {}


def json_strings(value: Any) -> list[str]:
    """Decode a stored JSON array and retain unique non-empty strings."""

    try:
        decoded = json.loads(value or "[]")
    except (TypeError, json.JSONDecodeError):
        return []
    if not isinstance(decoded, list):
        return []
    return sorted({str(item).strip() for item in decoded if str(item).strip()})


def normalize_install_spec(value: Any) -> tuple[str, str] | None:
    """Return a safe contract-v2 target and normalized pnpm install spec."""

    spec = str(value or "").strip()
    github = GITHUB_SPEC.fullmatch(spec)
    if github:
        owner, repository, subpath = github.groups()
        repository = repository.removesuffix(".git")
        normalized = f"github:{owner.lower()}/{repository.lower()}"
        if subpath:
            normalized += f"#path:{subpath}"
        return "git", normalized
    if NPM_SPEC.fullmatch(spec):
        return "npm", spec
    return None


def stable_plugin_id(install_spec: str) -> str:
    """Derive an opaque stable registry id from the normalized install spec."""

    digest = hashlib.sha256(install_spec.encode("utf-8")).hexdigest()[:20]
    return f"deeplugin-{digest}"


def listing_rows(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    """Load active installable Listings and their source/version provenance."""

    connection.row_factory = sqlite3.Row
    return connection.execute(
        """
        SELECT e.registry_id, e.entry_name, e.entry_url, e.owner, e.page_url,
               e.category, e.description, e.description_i18n, e.npm_package,
               e.stars, e.install_spec, e.install_target, e.plugin_version,
               e.verified, e.tags_json, e.registry_source_json, e.added_at,
               e.source_path, e.last_seen_at, r.full_name AS registry_name,
               r.source_url AS registry_url, c.dataset_version
        FROM upstream_entries AS e
        JOIN upstream_repositories AS r ON r.id = e.repository_id
        LEFT JOIN collection_runs AS c ON c.id = e.last_seen_run_id
        WHERE e.active = 1
          AND e.install_spec IS NOT NULL
          AND TRIM(e.install_spec) <> ''
        ORDER BY r.full_name, e.source_path, e.entry_name, e.id
        """
    ).fetchall()


def source_attribution(row: sqlite3.Row) -> dict[str, Any]:
    """Project one source-attributed Listing without turning claims into endorsement."""

    source = {
        "registry": str(row["registry_name"]),
        "registryUrl": str(row["registry_url"]),
        "sourceRef": str(row["source_path"] or ""),
        "listingId": row["registry_id"],
        "entryUrl": str(row["entry_url"]),
        "page": row["page_url"],
        "verified": bool(row["verified"]) if row["verified"] is not None else False,
        "version": row["plugin_version"],
        "observedAt": str(row["last_seen_at"]),
    }
    declared_source = json_object(row["registry_source_json"])
    if declared_source:
        source["declaredSource"] = declared_source
    return source


def listing_priority(row: sqlite3.Row) -> tuple[int, int, int, int, str]:
    """Prefer complete verified claims, then richer and more visible Listings."""

    return (
        int(row["verified"] is not None and bool(row["verified"]) and bool(row["plugin_version"])),
        int(row["plugin_version"] is not None),
        int(row["stars"] or -1),
        len(str(row["description"] or "")),
        str(row["registry_name"]),
    )


def author_for(row: sqlite3.Row) -> str:
    """Use the declared owner or the GitHub homepage owner when available."""

    if row["owner"]:
        return str(row["owner"])
    parts = urlsplit(str(row["entry_url"])).path.strip("/").split("/")
    return parts[0] if len(parts) >= 2 else "unknown"


def plugin_from_group(install_target: str, install_spec: str, rows: list[sqlite3.Row]) -> dict[str, Any]:
    """Merge Listings that identify the same normalized install artifact."""

    primary = max(rows, key=listing_priority)
    descriptions = json_object(primary["description_i18n"])
    fallback_description = str(primary["description"] or primary["entry_name"] or install_spec)
    description = str(descriptions.get("en") or fallback_description)
    description_zh = str(descriptions.get("zh") or fallback_description)
    category = str(primary["category"] or "uncategorized")
    tags = {category}
    for row in rows:
        tags.update(json_strings(row["tags_json"]))
    verified_rows = [
        row for row in rows
        if row["verified"] is not None and bool(row["verified"]) and row["plugin_version"]
    ]
    sources = sorted(
        (source_attribution(row) for row in rows),
        key=lambda source: (str(source["registry"]), str(source["sourceRef"]), str(source["entryUrl"])),
    )
    stars = [int(row["stars"]) for row in rows if row["stars"] is not None]
    plugin = {
        "id": stable_plugin_id(install_spec),
        "name": str(primary["entry_name"] or install_spec),
        "author": author_for(primary),
        "category": category,
        "description": description,
        "description_zh": description_zh,
        "install": {"target": install_target, "spec": install_spec},
        "version": str(max(verified_rows, key=listing_priority)["plugin_version"]) if verified_rows else None,
        "homepage": str(primary["entry_url"]),
        "verified": bool(verified_rows),
        "stars": max(stars) if stars else None,
        "tags": sorted(tags),
        "source": {
            "name": str(sources[0]["registry"]),
            "url": str(sources[0]["registryUrl"]),
        },
        "sources": sources,
    }
    return plugin


def categories_for(plugins: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    """Return bilingual labels for every category present in the registry."""

    categories: dict[str, dict[str, str]] = {}
    for category in sorted({str(plugin["category"]) for plugin in plugins}):
        fallback = category.replace("-", " ").replace("_", " ").title()
        categories[category] = CATEGORY_LABELS.get(category, {"en": fallback, "zh": fallback})
    return categories


def build_registry(connection: sqlite3.Connection) -> dict[str, Any]:
    """Build a deterministic contract-v2 registry from current valid Listings."""

    groups: dict[str, list[sqlite3.Row]] = defaultdict(list)
    targets: dict[str, str] = {}
    for row in listing_rows(connection):
        normalized = normalize_install_spec(row["install_spec"])
        if normalized is None:
            continue
        target, spec = normalized
        targets[spec] = target
        groups[spec].append(row)
    plugins = [plugin_from_group(targets[spec], spec, rows) for spec, rows in groups.items()]
    plugins.sort(key=lambda plugin: (-(plugin["stars"] if plugin["stars"] is not None else -1), plugin["name"].casefold(), plugin["id"]))
    observed = [str(source["observedAt"]) for plugin in plugins for source in plugin["sources"]]
    versions = sorted({
        str(row["dataset_version"])
        for row in listing_rows(connection)
        if row["dataset_version"]
    })
    updated_at = max(observed, default="1970-01-01T00:00:00Z")
    return {
        "$schema": SCHEMA_URL,
        "version": 2,
        "updated": updated_at[:10],
        "generatedAt": updated_at,
        "datasetVersion": versions[-1] if versions else None,
        "count": len(plugins),
        "verifiedCount": sum(bool(plugin["verified"]) for plugin in plugins),
        "note": (
            "Listings are aggregated from attributed community registries. "
            "verified=true reports at least one source curator's limited CI/release/install claim; "
            "it is not a deeplugin.store security or compatibility endorsement."
        ),
        "categories": categories_for(plugins),
        "plugins": plugins,
    }


def registry_schema() -> dict[str, Any]:
    """Return the JSON Schema for the public registry and attribution extensions."""

    nullable_string = {"type": ["string", "null"]}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": SCHEMA_URL,
        "title": "deeplugin.store DeepSeek Harness market registry v2",
        "type": "object",
        "additionalProperties": False,
        "required": ["version", "updated", "count", "verifiedCount", "note", "categories", "plugins"],
        "properties": {
            "$schema": {"const": SCHEMA_URL},
            "version": {"const": 2},
            "updated": {"type": "string", "format": "date"},
            "generatedAt": {"type": "string", "format": "date-time"},
            "datasetVersion": nullable_string,
            "count": {"type": "integer", "minimum": 0},
            "verifiedCount": {"type": "integer", "minimum": 0},
            "note": {"type": "string", "minLength": 1},
            "categories": {
                "type": "object",
                "additionalProperties": {"$ref": "#/$defs/category"},
            },
            "plugins": {"type": "array", "items": {"$ref": "#/$defs/plugin"}},
        },
        "$defs": {
            "category": {
                "type": "object",
                "additionalProperties": False,
                "required": ["en", "zh"],
                "properties": {"en": {"type": "string"}, "zh": {"type": "string"}},
            },
            "install": {
                "type": "object",
                "additionalProperties": False,
                "required": ["target", "spec"],
                "properties": {
                    "target": {"enum": ["git", "npm"]},
                    "spec": {"type": "string", "minLength": 1},
                },
            },
            "source": {
                "type": "object",
                "additionalProperties": True,
                "required": ["registry", "registryUrl", "sourceRef", "entryUrl", "verified", "observedAt"],
                "properties": {
                    "registry": {"type": "string"},
                    "registryUrl": {"type": "string", "format": "uri"},
                    "sourceRef": {"type": "string"},
                    "listingId": nullable_string,
                    "entryUrl": {"type": "string", "format": "uri"},
                    "page": nullable_string,
                    "verified": {"type": "boolean"},
                    "version": nullable_string,
                    "observedAt": {"type": "string", "format": "date-time"},
                    "declaredSource": {"type": "object"},
                },
            },
            "plugin": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "id", "name", "author", "category", "description", "description_zh",
                    "install", "version", "homepage", "verified", "stars", "tags", "source", "sources",
                ],
                "properties": {
                    "id": {"type": "string", "pattern": "^deeplugin-[0-9a-f]{20}$"},
                    "name": {"type": "string", "minLength": 1},
                    "author": {"type": "string", "minLength": 1},
                    "category": {"type": "string", "minLength": 1},
                    "description": {"type": "string", "minLength": 1},
                    "description_zh": {"type": "string", "minLength": 1},
                    "install": {"$ref": "#/$defs/install"},
                    "version": nullable_string,
                    "homepage": {"type": "string", "format": "uri"},
                    "verified": {"type": "boolean"},
                    "stars": {"type": ["integer", "null"], "minimum": 0},
                    "tags": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
                    "source": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["name", "url"],
                        "properties": {"name": {"type": "string"}, "url": {"type": "string", "format": "uri"}},
                    },
                    "sources": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/source"}},
                },
            },
        },
    }


def write_json(path: Path, value: Any) -> None:
    """Write deterministic UTF-8 JSON with one trailing newline."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_outputs(
    database: Path,
    *,
    index_registry: Path = INDEX_REGISTRY_PATH,
    docs_registry: Path = DOCS_REGISTRY_PATH,
    plugin_registry: Path | None = None,
    index_schema: Path = INDEX_SCHEMA_PATH,
    docs_schema: Path = DOCS_SCHEMA_PATH,
    plugin_schema: Path | None = None,
) -> dict[str, Any]:
    """Build and mirror the public registry and schema from one SQLite file."""

    with sqlite3.connect(database) as connection:
        registry = build_registry(connection)
    schema = registry_schema()
    registry_paths = [index_registry, docs_registry]
    if plugin_registry is not None:
        registry_paths.append(plugin_registry)
    for path in registry_paths:
        write_json(path, registry)
    schema_paths = [index_schema, docs_schema]
    if plugin_schema is not None:
        schema_paths.append(plugin_schema)
    for path in schema_paths:
        write_json(path, schema)
    return registry


def parse_args() -> argparse.Namespace:
    """Parse command-line paths for reproducible local or CI builds."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DB_PATH)
    parser.add_argument("--index-registry", type=Path, default=INDEX_REGISTRY_PATH)
    parser.add_argument("--docs-registry", type=Path, default=DOCS_REGISTRY_PATH)
    parser.add_argument("--plugin-registry", type=Path, default=PLUGIN_REGISTRY_PATH)
    parser.add_argument("--index-schema", type=Path, default=INDEX_SCHEMA_PATH)
    parser.add_argument("--docs-schema", type=Path, default=DOCS_SCHEMA_PATH)
    parser.add_argument("--plugin-schema", type=Path, default=PLUGIN_SCHEMA_PATH)
    return parser.parse_args()


def main() -> int:
    """Build all public registry artifacts and report aggregate counts."""

    args = parse_args()
    registry = write_outputs(
        args.db,
        index_registry=args.index_registry,
        docs_registry=args.docs_registry,
        plugin_registry=args.plugin_registry,
        index_schema=args.index_schema,
        docs_schema=args.docs_schema,
        plugin_schema=args.plugin_schema,
    )
    print(json.dumps({
        "registry": str(args.index_registry),
        "count": registry["count"],
        "verified": registry["verifiedCount"],
        "dataset_version": registry["datasetVersion"],
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
