#!/usr/bin/env python3
"""Build deterministic Atom feeds and author launch packets for Market plugins."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from build_market_registry import normalize_install_spec, stable_plugin_id


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
REGISTRY_PATH = ROOT / "docs" / "data" / "market-registry.json"
DOCS = ROOT / "docs"
SITE_URL = "https://deeplugin.store"
SCHEMA_URL = SITE_URL + "/data/launch-packet.schema.json"
ATOM_NAMESPACE = "http://www.w3.org/2005/Atom"

MATERIAL_FIELDS = (
    "active",
    "entry_name",
    "entry_url",
    "owner",
    "page_url",
    "entry_kind",
    "category",
    "description",
    "description_i18n",
    "npm_package",
    "install_hint",
    "install_spec",
    "install_target",
    "plugin_version",
    "verified",
    "tags_json",
    "registry_source_json",
    "added_at",
    "source_path",
)


def xml(value: object, *, attribute: bool = False) -> str:
    """Escape one value for Atom text or attribute content."""

    return html.escape(str(value or ""), quote=attribute)


def load_registry(path: Path) -> dict[str, Any]:
    """Read the public Market registry and validate stable plugin identities."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("plugins"), list):
        raise ValueError("Market registry must contain a plugins array")
    for plugin in value["plugins"]:
        if not isinstance(plugin, dict) or not isinstance(plugin.get("install"), dict):
            raise ValueError("Market registry plugin is missing install data")
        spec = str(plugin["install"].get("spec") or "")
        normalized = normalize_install_spec(spec)
        if normalized is None or normalized[1] != spec:
            raise ValueError(f"Market registry contains an unsafe install spec: {spec!r}")
        if plugin.get("id") != stable_plugin_id(spec):
            raise ValueError(f"Market registry contains a mismatched stable id for {spec!r}")
    return value


def observation_rows(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    """Load ordered source-local Listing observations from the full database."""

    connection.row_factory = sqlite3.Row
    return connection.execute(
        """
        SELECT o.*, r.full_name AS registry_name
        FROM upstream_entry_observations AS o
        JOIN upstream_entries AS e ON e.id = o.entry_id
        JOIN upstream_repositories AS r ON r.id = e.repository_id
        WHERE o.install_spec IS NOT NULL
          AND TRIM(o.install_spec) <> ''
        ORDER BY o.observed_at, o.collection_run_id, o.entry_id
        """
    ).fetchall()


def material_state(row: sqlite3.Row) -> tuple[object, ...]:
    """Return fields whose change represents a Listing change rather than a metric refresh."""

    return tuple(row[field] for field in MATERIAL_FIELDS)


def changed_fields(previous: sqlite3.Row, current: sqlite3.Row) -> list[str]:
    """Name the material Listing fields changed by one observation."""

    return [field for field in MATERIAL_FIELDS if previous[field] != current[field]]


def fallback_event(plugin: dict[str, Any], generated_at: str) -> dict[str, Any]:
    """Create a first-observed event when retained history predates the current projection."""

    observed = [
        str(source.get("observedAt"))
        for source in plugin.get("sources", [])
        if isinstance(source, dict) and source.get("observedAt")
    ]
    return {
        "kind": "new",
        "observed_at": min(observed, default=generated_at),
        "source": str(plugin.get("source", {}).get("name") or "attributed registry"),
        "changes": ["listed"],
        "active": True,
    }


def release_events(
    connection: sqlite3.Connection,
    plugins: list[dict[str, Any]],
    generated_at: str,
) -> dict[str, list[dict[str, Any]]]:
    """Derive material plugin events while ignoring identical repeat observations and stars."""

    plugins_by_spec = {
        str(plugin["install"]["spec"]): plugin
        for plugin in plugins
    }
    source_events: dict[str, list[dict[str, Any]]] = defaultdict(list)
    previous_by_entry: dict[int, sqlite3.Row] = {}
    for row in observation_rows(connection):
        entry_id = int(row["entry_id"])
        previous = previous_by_entry.get(entry_id)
        previous_by_entry[entry_id] = row
        normalized = normalize_install_spec(row["install_spec"])
        if normalized is None:
            continue
        spec = normalized[1]
        plugin = plugins_by_spec.get(spec)
        if plugin is None:
            continue
        active = bool(row["active"])
        source_initial = previous is None
        changes: list[str]
        if previous is None:
            if not active:
                continue
            changes = ["listed"]
        else:
            previous_normalized = normalize_install_spec(previous["install_spec"])
            same_identity = previous_normalized is not None and previous_normalized[1] == spec
            if same_identity and material_state(previous) == material_state(row):
                continue
            if not same_identity:
                if not active:
                    continue
                source_initial = True
                changes = ["install_spec"]
            else:
                changes = changed_fields(previous, row)
        source_events[str(plugin["id"])].append(
            {
                "kind": "updated",
                "observed_at": str(row["observed_at"]),
                "source": str(row["registry_name"]),
                "changes": changes,
                "active": active,
                "source_initial": source_initial,
            }
        )

    events_by_plugin: dict[str, list[dict[str, Any]]] = {}
    for plugin in plugins:
        plugin_id = str(plugin["id"])
        events = sorted(
            source_events.get(plugin_id, []),
            key=lambda event: (event["observed_at"], event["source"], ",".join(event["changes"])),
        )
        seen_active_plugin = False
        normalized_events: list[dict[str, Any]] = []
        for event in events:
            normalized = dict(event)
            if event["active"] and not seen_active_plugin:
                normalized["kind"] = "new"
                normalized["changes"] = ["listed"]
                seen_active_plugin = True
            elif event.get("source_initial") and event["active"]:
                normalized["kind"] = "updated"
                normalized["changes"] = ["sources"]
            normalized.pop("source_initial", None)
            normalized_events.append(normalized)
        if not normalized_events:
            normalized_events.append(fallback_event(plugin, generated_at))
        events_by_plugin[plugin_id] = normalized_events
    return events_by_plugin


def event_identifier(plugin_id: str, event: dict[str, Any]) -> str:
    """Return a stable Atom entry id for one material event."""

    payload = json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"tag:deeplugin.store,{str(event['observed_at'])[:10]}:{plugin_id}/{digest}"


def atom_entry(plugin: dict[str, Any], event: dict[str, Any], site_url: str) -> str:
    """Render one Atom entry pointing to the stable plugin detail page."""

    plugin_id = str(plugin["id"])
    canonical = f"{site_url}/plugins/{plugin_id}.html"
    kind = str(event["kind"])
    title_prefix = "New" if kind == "new" else "Updated"
    change_label = ", ".join(str(value) for value in event.get("changes", [])) or "listing"
    description = str(plugin.get("description") or plugin.get("name"))
    separator = "" if description.endswith((".", "!", "?", "。", "！", "？")) else "."
    summary = (
        f"{description}{separator} "
        f"Exact install spec: {plugin['install']['spec']}. "
        f"Source event: {event['source']}; changed: {change_label}."
    )
    return "\n".join([
        "  <entry>",
        f"    <title>{xml(title_prefix + ': ' + str(plugin['name']))}</title>",
        f"    <id>{xml(event_identifier(plugin_id, event))}</id>",
        f"    <updated>{xml(event['observed_at'])}</updated>",
        f"    <link rel=\"alternate\" href=\"{xml(canonical, attribute=True)}\"/>",
        f"    <author><name>{xml(plugin.get('author') or 'unknown')}</name></author>",
        f"    <category term=\"{xml(plugin.get('category') or 'tools', attribute=True)}\"/>",
        f"    <summary>{xml(summary)}</summary>",
        "  </entry>",
    ])


def atom_feed(
    title: str,
    feed_url: str,
    alternate_url: str,
    entries: Iterable[tuple[dict[str, Any], dict[str, Any]]],
    fallback_updated: str,
    site_url: str,
) -> str:
    """Render a deterministic Atom 1.0 document."""

    values = list(entries)
    updated = max((str(event["observed_at"]) for _, event in values), default=fallback_updated)
    rendered_entries = "\n".join(atom_entry(plugin, event, site_url) for plugin, event in values)
    return "\n".join([
        '<?xml version="1.0" encoding="utf-8"?>',
        f'<feed xmlns="{ATOM_NAMESPACE}">',
        f"  <title>{xml(title)}</title>",
        f"  <id>{xml(feed_url)}</id>",
        f"  <updated>{xml(updated)}</updated>",
        f'  <link rel="self" type="application/atom+xml" href="{xml(feed_url, attribute=True)}"/>',
        f'  <link rel="alternate" href="{xml(alternate_url, attribute=True)}"/>',
        rendered_entries,
        "</feed>",
        "",
    ])


def launch_packet_schema() -> dict[str, Any]:
    """Return the JSON Schema for generated author launch packets."""

    nullable_string = {"type": ["string", "null"]}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": SCHEMA_URL,
        "title": "deeplugin.store author launch packet",
        "type": "object",
        "additionalProperties": False,
        "required": ["$schema", "version", "plugin", "links", "install", "badge", "posts"],
        "properties": {
            "$schema": {"const": SCHEMA_URL},
            "version": {"const": 1},
            "plugin": {"$ref": "#/$defs/plugin"},
            "links": {"$ref": "#/$defs/links"},
            "install": {"$ref": "#/$defs/install"},
            "badge": {"$ref": "#/$defs/badge"},
            "posts": {"$ref": "#/$defs/posts"},
        },
        "$defs": {
            "plugin": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "id", "name", "author", "category", "version", "homepage",
                    "firstObservedAt", "lastChangedAt",
                ],
                "properties": {
                    "id": {"type": "string", "pattern": "^deeplugin-[0-9a-f]{20}$"},
                    "name": {"type": "string", "minLength": 1},
                    "author": {"type": "string", "minLength": 1},
                    "category": {"type": "string", "minLength": 1},
                    "version": nullable_string,
                    "homepage": {"type": ["string", "null"], "format": "uri"},
                    "firstObservedAt": {"type": "string", "format": "date-time"},
                    "lastChangedAt": {"type": "string", "format": "date-time"},
                },
            },
            "links": {
                "type": "object",
                "additionalProperties": False,
                "required": ["detail", "feed", "newFeed", "updatedFeed"],
                "properties": {
                    key: {"type": "string", "format": "uri"}
                    for key in ("detail", "feed", "newFeed", "updatedFeed")
                },
            },
            "install": {
                "type": "object",
                "additionalProperties": False,
                "required": ["spec", "command", "agentRequest"],
                "properties": {
                    "spec": {"type": "string", "minLength": 1},
                    "command": {"type": "string", "minLength": 1},
                    "agentRequest": {"type": "string", "minLength": 1},
                },
            },
            "badge": {
                "type": "object",
                "additionalProperties": False,
                "required": ["markdown", "html"],
                "properties": {
                    "markdown": {"type": "string", "minLength": 1},
                    "html": {"type": "string", "minLength": 1},
                },
            },
            "posts": {
                "type": "object",
                "additionalProperties": False,
                "required": ["zh", "en"],
                "properties": {
                    "zh": {"type": "string", "minLength": 1},
                    "en": {"type": "string", "minLength": 1},
                },
            },
        },
    }


def launch_packet(
    plugin: dict[str, Any],
    events: list[dict[str, Any]],
    site_url: str,
) -> dict[str, Any]:
    """Build a bilingual, fact-only launch packet for one current plugin identity."""

    plugin_id = str(plugin["id"])
    name = str(plugin["name"])
    spec = str(plugin["install"]["spec"])
    canonical = f"{site_url}/plugins/{plugin_id}.html"
    feed = f"{site_url}/plugins/{plugin_id}.atom.xml"
    badge_image = f"{site_url}/assets/deeplugin-listed.svg"
    badge_markdown = f"[![Listed on deeplugin.store]({badge_image})]({canonical})"
    badge_html = f'<a href="{canonical}"><img src="{badge_image}" alt="Listed on deeplugin.store"></a>'
    description_zh = " ".join(str(plugin.get("description_zh") or plugin.get("description") or name).split())
    description_en = " ".join(str(plugin.get("description") or name).split())
    return {
        "$schema": SCHEMA_URL,
        "version": 1,
        "plugin": {
            "id": plugin_id,
            "name": name,
            "author": str(plugin.get("author") or "unknown"),
            "category": str(plugin.get("category") or "tools"),
            "version": plugin.get("version"),
            "homepage": plugin.get("homepage"),
            "firstObservedAt": events[0]["observed_at"],
            "lastChangedAt": events[-1]["observed_at"],
        },
        "links": {
            "detail": canonical,
            "feed": feed,
            "newFeed": f"{site_url}/feeds/new.atom.xml",
            "updatedFeed": f"{site_url}/feeds/updated.atom.xml",
        },
        "install": {
            "spec": spec,
            "command": f"dsh plugin --profile web add {spec}",
            "agentRequest": (
                f"请先在 deeplugin.store 中检索 Registry ID {plugin_id}，展示来源和精确安装 spec，"
                "为 web profile 生成安装计划；等我明确批准后再安装。"
            ),
        },
        "badge": {"markdown": badge_markdown, "html": badge_html},
        "posts": {
            "zh": f"{name} 已收录到 DeepSeek Harness Plugin Store。{description_zh}\n\n查看来源与安装：{canonical}",
            "en": f"{name} is now listed on the DeepSeek Harness Plugin Store. {description_en}\n\nSource and install details: {canonical}",
        },
    }


def write_json(path: Path, value: Any) -> None:
    """Write deterministic UTF-8 JSON with one trailing newline."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_growth_assets(
    database: Path,
    registry_path: Path,
    docs: Path,
    site_url: str,
) -> dict[str, int]:
    """Write global/plugin Atom feeds and one launch packet per current plugin."""

    site_url = site_url.rstrip("/")
    registry = load_registry(registry_path)
    plugins = [plugin for plugin in registry["plugins"] if isinstance(plugin, dict)]
    generated_at = str(registry.get("generatedAt") or "1970-01-01T00:00:00Z")
    with sqlite3.connect(database) as connection:
        events_by_plugin = release_events(connection, plugins, generated_at)

    plugins_by_id = {str(plugin["id"]): plugin for plugin in plugins}
    first_events = sorted(
        ((plugins_by_id[plugin_id], events[0]) for plugin_id, events in events_by_plugin.items()),
        key=lambda value: (value[1]["observed_at"], value[0]["id"]),
        reverse=True,
    )[:100]
    latest_updates = sorted(
        (
            (plugins_by_id[plugin_id], updates[-1])
            for plugin_id, events in events_by_plugin.items()
            if (updates := [event for event in events if event["kind"] == "updated"])
        ),
        key=lambda value: (value[1]["observed_at"], value[0]["id"]),
        reverse=True,
    )[:100]

    feeds = docs / "feeds"
    feeds.mkdir(parents=True, exist_ok=True)
    (feeds / "new.atom.xml").write_text(
        atom_feed(
            "deeplugin.store — New plugins",
            f"{site_url}/feeds/new.atom.xml",
            f"{site_url}/market.html",
            first_events,
            generated_at,
            site_url,
        ),
        encoding="utf-8",
    )
    (feeds / "updated.atom.xml").write_text(
        atom_feed(
            "deeplugin.store — Updated plugins",
            f"{site_url}/feeds/updated.atom.xml",
            f"{site_url}/market.html",
            latest_updates,
            generated_at,
            site_url,
        ),
        encoding="utf-8",
    )

    plugin_directory = docs / "plugins"
    plugin_directory.mkdir(parents=True, exist_ok=True)
    for plugin in plugins:
        plugin_id = str(plugin["id"])
        events = events_by_plugin[plugin_id]
        ordered_events = list(reversed(events[-50:]))
        (plugin_directory / f"{plugin_id}.atom.xml").write_text(
            atom_feed(
                f"{plugin['name']} — release evidence",
                f"{site_url}/plugins/{plugin_id}.atom.xml",
                f"{site_url}/plugins/{plugin_id}.html",
                ((plugin, event) for event in ordered_events),
                generated_at,
                site_url,
            ),
            encoding="utf-8",
        )
        write_json(plugin_directory / f"{plugin_id}.launch.json", launch_packet(plugin, events, site_url))
    write_json(docs / "data" / "launch-packet.schema.json", launch_packet_schema())
    return {"plugins": len(plugins), "new": len(first_events), "updated": len(latest_updates)}


def parse_args() -> argparse.Namespace:
    """Parse reproducible input and output paths."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DB_PATH)
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--docs", type=Path, default=DOCS)
    parser.add_argument("--site-url", default=SITE_URL)
    return parser.parse_args()


def main() -> int:
    """Build growth assets and print deterministic output counts."""

    args = parse_args()
    counts = write_growth_assets(args.db, args.registry, args.docs, args.site_url)
    print(json.dumps(counts, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
