#!/usr/bin/env python3
"""Validate raw snapshots, SQLite integrity, and core aggregator invariants."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import build_market_registry
import collect


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "aggregator.sqlite3"
FULL_ARCHIVE_PATH = ROOT / "data" / "aggregator-full.sqlite3.zst"
RAW_DIR = ROOT / "data" / "raw"
MEDIA_DIR = ROOT / "media"
PUBLISHED_MEDIA_DIR = ROOT / "docs" / "media"
SITEMAP_PATH = ROOT / "docs" / "sitemap.xml"
DETAIL_DIR = ROOT / "docs" / "skills"
INDEX_PATH = ROOT / "index" / "records.jsonl"
VALUE_MATRIX_PATH = ROOT / "index" / "value-matrix.jsonl"
FORK_INDEX_PATH = ROOT / "docs" / "data" / "forks.json"
COMMUNITY_REGISTRY_PATH = ROOT / "registry" / "plugins.json"
MARKET_REGISTRY_PATHS = (
    ROOT / "index" / "market-registry.json",
    ROOT / "docs" / "data" / "market-registry.json",
    ROOT / "plugin" / "data" / "market-registry.json",
)
MARKET_SCHEMA_PATHS = (
    ROOT / "index" / "market-registry.schema.json",
    ROOT / "docs" / "data" / "market-registry.schema.json",
    ROOT / "plugin" / "data" / "market-registry.schema.json",
)
INDEX_FIELDS = {
    "id", "summary", "url", "repo", "context", "picture", "comment", "favor",
    "views", "refs", "rank", "stars", "dataset_version", "first_seen_at", "last_seen_at",
}
VALUE_MATRIX_FIELDS = {
    "id", "item_id", "title", "url", "platform", "category", "dataset_version", "scoring_version",
    "assessed_at", "utility", "evidence", "traction", "ecosystem", "freshness", "reviewability",
    "value_score", "confidence_score", "value_band", "evidence_count", "source_count", "risk_flags",
}
PUBLIC_DB_MAX_BYTES = 95 * 1024 * 1024
PUBLIC_PROJECTION_VERSION = 4
PUBLIC_DROPPED_INDEXES = ("idx_metrics_dedupe",)
PUBLIC_STRIPPED_JSON_COLUMNS = (
    ("raw_snapshots", "payload_json"),
    ("items", "raw_json"),
    ("metrics", "raw_json"),
    ("github_user_profiles", "raw_json"),
    ("fork_file_changes", "raw_json"),
    ("fork_commits", "raw_json"),
    ("fork_rankings", "components_json"),
    ("upstream_entries", "source_json"),
)


def identical_json(paths: tuple[Path, ...]) -> dict[str, Any]:
    """Load byte-identical generated JSON mirrors."""

    contents = [path.read_bytes() for path in paths]
    assert all(content == contents[0] for content in contents[1:]), paths
    decoded = json.loads(contents[0])
    assert isinstance(decoded, dict), paths[0]
    return decoded


def validate_market_registry() -> int:
    """Validate generated Market registry identity, safety, and mirror invariants."""

    registry = identical_json(MARKET_REGISTRY_PATHS)
    schema = identical_json(MARKET_SCHEMA_PATHS)
    assert registry["version"] == 2
    assert schema["$id"] == "https://deeplugin.store/data/market-registry.schema.json"
    assert schema["properties"]["version"]["const"] == registry["version"]
    plugins = registry["plugins"]
    assert isinstance(plugins, list)
    assert registry["count"] == len(plugins)
    assert registry["verifiedCount"] == sum(plugin["verified"] is True for plugin in plugins)
    required_fields = set(schema["$defs"]["plugin"]["required"])
    ids: set[str] = set()
    install_specs: set[str] = set()
    for plugin in plugins:
        assert isinstance(plugin, dict)
        assert required_fields <= set(plugin)
        plugin_id = plugin["id"]
        install = plugin["install"]
        assert isinstance(plugin_id, str)
        assert isinstance(install, dict)
        target = install["target"]
        spec = install["spec"]
        normalized = build_market_registry.normalize_install_spec(spec)
        assert normalized == (target, spec), (plugin_id, spec)
        assert plugin_id == build_market_registry.stable_plugin_id(spec)
        assert plugin_id not in ids
        assert spec not in install_specs
        assert plugin["category"] in registry["categories"]
        assert isinstance(plugin["sources"], list) and plugin["sources"]
        if plugin["verified"] is True:
            assert plugin["version"]
        ids.add(plugin_id)
        install_specs.add(spec)
    return len(plugins)


def validate_community_registry() -> int:
    """Validate source-local community Listings before scheduled ingestion."""

    registry = json.loads(COMMUNITY_REGISTRY_PATH.read_text(encoding="utf-8"))
    assert isinstance(registry, dict)
    assert registry["version"] == 2
    plugins = registry["plugins"]
    assert isinstance(plugins, list)
    assert registry["count"] == len(plugins)
    required_fields = {
        "id", "name", "author", "category", "description", "description_zh",
        "install", "version", "homepage", "verified", "stars", "tags", "source",
    }
    ids: set[str] = set()
    install_specs: set[str] = set()
    for plugin in plugins:
        assert isinstance(plugin, dict)
        assert required_fields <= set(plugin)
        assert plugin["verified"] is False
        plugin_id = plugin["id"]
        install = plugin["install"]
        assert isinstance(plugin_id, str) and plugin_id
        assert isinstance(install, dict)
        target = install["target"]
        spec = install["spec"]
        assert build_market_registry.normalize_install_spec(spec) == (target, spec)
        assert plugin_id not in ids
        assert spec not in install_specs
        assert plugin["stars"] is None or (
            isinstance(plugin["stars"], int)
            and not isinstance(plugin["stars"], bool)
            and plugin["stars"] >= 0
        )
        assert isinstance(plugin["source"], dict)
        assert plugin["source"].get("name") and plugin["source"].get("url")
        ids.add(plugin_id)
        install_specs.add(spec)
    return len(plugins)


def validate_rich_media_site(connection: sqlite3.Connection, item_count: int) -> tuple[int, int]:
    """Validate deployable local media and crawlable image/video projections."""

    source_files = sorted(path.relative_to(MEDIA_DIR) for path in MEDIA_DIR.rglob("*") if path.is_file())
    published_files = sorted(
        path.relative_to(PUBLISHED_MEDIA_DIR)
        for path in PUBLISHED_MEDIA_DIR.rglob("*")
        if path.is_file()
    )
    assert published_files == source_files
    for relative_path in source_files:
        assert (MEDIA_DIR / relative_path).read_bytes() == (PUBLISHED_MEDIA_DIR / relative_path).read_bytes()
    for item_id, local_path in connection.execute(
        "SELECT item_id, url FROM media_assets WHERE url LIKE 'media/%' ORDER BY item_id, id"
    ):
        relative_path = Path(local_path)
        assert not relative_path.is_absolute() and ".." not in relative_path.parts, local_path
        assert (ROOT / relative_path).is_file(), (item_id, local_path)
        assert (ROOT / "docs" / relative_path).is_file(), (item_id, local_path)

    sitemap_root = ET.parse(SITEMAP_PATH).getroot()
    sitemap_ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    image_ns = "http://www.google.com/schemas/sitemap-image/1.1"
    video_ns = "http://www.google.com/schemas/sitemap-video/1.1"
    entries = sitemap_root.findall(f"{{{sitemap_ns}}}url")
    locations = [entry.findtext(f"{{{sitemap_ns}}}loc") for entry in entries]
    required_static_locations = {
        "https://deeplugin.store/",
        "https://deeplugin.store/market.html",
        "https://deeplugin.store/report.html",
        "https://deeplugin.store/timeline.html",
        "https://deeplugin.store/categories.html",
        "https://deeplugin.store/directories.html",
        "https://deeplugin.store/sources.html",
        "https://deeplugin.store/forks.html",
        "https://deeplugin.store/register.html",
        "https://deeplugin.store/register-agent.html",
    }
    assert required_static_locations.issubset(set(locations))
    assert len(entries) == item_count + len(required_static_locations)
    assert len(set(locations)) == len(locations)
    image_entries = sitemap_root.findall(f".//{{{image_ns}}}image")
    video_entries = sitemap_root.findall(f".//{{{video_ns}}}video")
    assert image_entries
    assert video_entries
    required_video_fields = {
        "thumbnail_loc", "title", "description", "player_loc", "publication_date",
    }
    for video in video_entries:
        fields = {
            child.tag.removeprefix(f"{{{video_ns}}}")
            for child in video
            if child.text and child.text.strip()
        }
        assert fields == required_video_fields
    for item_id, video_url in connection.execute(
        "SELECT id, canonical_url FROM items WHERE media_kind = 'video' ORDER BY id"
    ):
        detail = (DETAIL_DIR / f"id-{item_id}.html").read_text(encoding="utf-8")
        assert f'<img src="{video_url}"' not in detail, item_id
    return len(image_entries), len(video_entries)


def validate_item_seen_ranges(connection: sqlite3.Connection) -> None:
    """Require item date boundaries and run ids to match observation history."""

    inverted = connection.execute(
        "SELECT COUNT(*) FROM items WHERE first_seen_at > last_seen_at"
    ).fetchone()[0]
    assert inverted == 0, f"{inverted} item date range(s) are inverted"
    mismatched_dates = connection.execute(
        """
        WITH boundaries AS (
            SELECT
                io.item_id,
                MIN(o.collected_at) AS first_seen_at,
                MAX(o.collected_at) AS last_seen_at
            FROM item_observations AS io
            JOIN observations AS o ON o.id = io.observation_id
            GROUP BY io.item_id
        )
        SELECT COUNT(*)
        FROM items
        LEFT JOIN boundaries ON boundaries.item_id = items.id
        WHERE boundaries.item_id IS NULL
           OR items.first_seen_at IS NOT boundaries.first_seen_at
           OR items.last_seen_at IS NOT boundaries.last_seen_at
        """
    ).fetchone()[0]
    assert mismatched_dates == 0, f"{mismatched_dates} item date range(s) disagree with observation history"
    for boundary in ("first", "last"):
        mismatched_runs = connection.execute(
            f"""
            SELECT COUNT(*)
            FROM items
            WHERE NOT EXISTS (
                SELECT 1
                FROM item_observations AS io
                JOIN observations AS o ON o.id = io.observation_id
                WHERE io.item_id = items.id
                  AND o.collected_at = items.{boundary}_seen_at
                  AND o.collection_run_id = items.{boundary}_seen_run_id
            )
            """
        ).fetchone()[0]
        assert mismatched_runs == 0, f"{mismatched_runs} item {boundary}-seen run id(s) lack boundary evidence"


def main() -> None:
    """Run deterministic checks and print the current dataset size."""

    raw_paths = [
        path for path in RAW_DIR.rglob("*.json")
        if "auto" not in path.parts and "forks" not in path.parts
    ]
    for path in raw_paths:
        json.loads(path.read_text(encoding="utf-8"))
    connection = sqlite3.connect(DB_PATH)
    integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    assert integrity == "ok", integrity
    schema_version = connection.execute("PRAGMA user_version").fetchone()[0]
    assert schema_version == collect.SCHEMA_VERSION, schema_version
    is_public_projection = connection.execute(
        "SELECT 1 FROM sqlite_schema WHERE type = 'table' AND name = 'public_projection_metadata'"
    ).fetchone() is not None
    if is_public_projection:
        projection = connection.execute(
            "SELECT projection_version, source_sha256, authoritative_archive, latest_value_run_id, "
            "stripped_fields_json "
            "FROM public_projection_metadata"
        ).fetchall()
        assert len(projection) == 1
        assert projection[0][0] == PUBLIC_PROJECTION_VERSION
        assert len(projection[0][1]) == 64
        assert projection[0][2]
        projection_policy = json.loads(projection[0][4])
        assert projection_policy["dropped_indexes"] == list(PUBLIC_DROPPED_INDEXES)
        assert projection_policy["stripped_fields"] == [
            f"{table}.{column}" for table, column in PUBLIC_STRIPPED_JSON_COLUMNS
        ]
        assert set(projection_policy["retention"]) == {
            "fork_commits", "fork_file_changes", "fork_rankings", "fork_snapshots",
            "upstream_entry_observations", "value_assessments",
        }
        assert FULL_ARCHIVE_PATH.is_file() and FULL_ARCHIVE_PATH.stat().st_size > 0
        assert DB_PATH.stat().st_size <= PUBLIC_DB_MAX_BYTES
        for table, column in PUBLIC_STRIPPED_JSON_COLUMNS:
            assert connection.execute(
                f'SELECT COUNT(*) FROM "{table}" WHERE "{column}" <> ?', ("{}",)
            ).fetchone()[0] == 0
        assert connection.execute(
            "SELECT COUNT(*) FROM sqlite_schema WHERE type = 'index' AND name IN (?)",
            PUBLIC_DROPPED_INDEXES,
        ).fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM items WHERE canonical_url = ''").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM items WHERE raw_json IS NULL OR raw_json = ''").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM metrics WHERE metric_source IS NULL OR metric_source = ''").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM item_observations").fetchone()[0] >= connection.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    assert connection.execute("SELECT COUNT(*) FROM items").fetchone()[0] == connection.execute("SELECT COUNT(DISTINCT canonical_url) FROM items").fetchone()[0]
    assert connection.execute("SELECT COUNT(*) FROM items").fetchone()[0] == connection.execute("SELECT COUNT(DISTINCT platform || char(0) || external_id) FROM items").fetchone()[0]
    assert connection.execute("SELECT COUNT(*) FROM fork_repositories").fetchone()[0] == connection.execute("SELECT COUNT(DISTINCT full_name) FROM fork_repositories").fetchone()[0]
    assert connection.execute("SELECT COUNT(*) FROM github_user_profiles").fetchone()[0] == connection.execute("SELECT COUNT(DISTINCT login) FROM github_user_profiles").fetchone()[0]
    assert connection.execute(
        "SELECT COUNT(*) FROM (SELECT fork_id, collection_run_id FROM fork_snapshots GROUP BY fork_id, collection_run_id HAVING COUNT(*) > 1)"
    ).fetchone()[0] == 0
    assert connection.execute(
        "SELECT COUNT(*) FROM (SELECT fork_id, collection_run_id, ranking_version FROM fork_rankings GROUP BY fork_id, collection_run_id, ranking_version HAVING COUNT(*) > 1)"
    ).fetchone()[0] == 0
    assert connection.execute(
        "SELECT COUNT(*) FROM (SELECT collection_run_id, ranking_version, rank FROM fork_rankings GROUP BY collection_run_id, ranking_version, rank HAVING COUNT(*) > 1)"
    ).fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM metrics WHERE item_id IS NULL OR metric_source = ''").fetchone()[0] == 0
    duplicate_metric_keys = connection.execute(
        """
        SELECT COUNT(*)
        FROM (
            SELECT item_id, observed_at, metric_source
            FROM metrics
            GROUP BY item_id, observed_at, metric_source
            HAVING COUNT(*) > 1
        )
        """
    ).fetchone()[0]
    assert duplicate_metric_keys == 0, f"{duplicate_metric_keys} duplicate metric history key(s)"
    assert connection.execute("SELECT COUNT(*) FROM collection_runs").fetchone()[0] > 0
    assert connection.execute("SELECT COUNT(*) FROM observations WHERE collection_run_id IS NULL").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM metrics WHERE collection_run_id IS NULL").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM items WHERE first_seen_run_id IS NULL OR last_seen_run_id IS NULL").fetchone()[0] == 0
    validate_item_seen_ranges(connection)
    assert connection.execute("SELECT COUNT(*) FROM raw_snapshots WHERE payload_json IS NULL OR payload_json = ''").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM raw_snapshots").fetchone()[0] == connection.execute(
        "SELECT COUNT(DISTINCT raw_path) FROM raw_snapshots"
    ).fetchone()[0]
    verified_paths: dict[Path, str] = {}
    for raw_path, expected_digest in connection.execute(
        "SELECT raw_path, raw_sha256 FROM raw_snapshots ORDER BY raw_path"
    ):
        relative_path = Path(raw_path)
        if relative_path.parts[:3] == ("data", "raw", "forks"):
            continue
        assert not relative_path.is_absolute(), raw_path
        path = (ROOT / relative_path).resolve()
        assert path.is_relative_to(RAW_DIR.resolve()), raw_path
        assert path.is_file(), raw_path
        if path not in verified_paths:
            verified_paths[path] = hashlib.sha256(path.read_bytes()).hexdigest()
        assert verified_paths[path] == expected_digest, raw_path
    for path in raw_paths:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert connection.execute("SELECT 1 FROM raw_snapshots WHERE raw_sha256 = ?", (digest,)).fetchone(), path
    assert connection.execute("SELECT COUNT(*) FROM observations WHERE raw_path IS NOT NULL AND raw_snapshot_id IS NULL").fetchone()[0] == 0
    items = connection.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    index_records = [json.loads(line) for line in INDEX_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(index_records) == connection.execute("SELECT COUNT(*) FROM index_records").fetchone()[0]
    assert len({record["id"] for record in index_records}) == len(index_records)
    assert all(set(record) == INDEX_FIELDS for record in index_records)
    fork_index = json.loads(FORK_INDEX_PATH.read_text(encoding="utf-8"))
    fork_records = fork_index["records"]
    assert len({record["full_name"] for record in fork_records}) == len(fork_records)
    assert len({record["rank"] for record in fork_records}) == len(fork_records)
    assert len(fork_records) == connection.execute("SELECT COUNT(*) FROM v_current_fork_rankings").fetchone()[0]
    assert connection.execute("SELECT COUNT(*) FROM index_records WHERE dataset_version IS NULL OR dataset_version = ''").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM item_details WHERE status = 'ok' AND char_count = 0").fetchone()[0] == 0
    current_run_id = connection.execute(
        "SELECT id FROM collection_runs WHERE trigger <> 'legacy-migration' ORDER BY id DESC LIMIT 1"
    ).fetchone()[0]
    assert connection.execute("SELECT COUNT(*) FROM value_assessments WHERE collection_run_id = ?", (current_run_id,)).fetchone()[0] == items
    if is_public_projection:
        assert connection.execute("SELECT COUNT(*) FROM value_assessments").fetchone()[0] == items
        assert projection[0][3] == current_run_id
    value_records = [json.loads(line) for line in VALUE_MATRIX_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(value_records) == items
    assert len({record["id"] for record in value_records}) == len(value_records)
    assert all(set(record) == VALUE_MATRIX_FIELDS for record in value_records)
    assert all(record["value_band"] in {"A", "B", "C", "D"} for record in value_records)
    assert all(0 <= record[key] <= 100 for record in value_records for key in ("utility", "evidence", "traction", "ecosystem", "freshness", "reviewability", "value_score", "confidence_score"))
    community_listings = validate_community_registry()
    market_plugins = validate_market_registry()
    sitemap_images, sitemap_videos = validate_rich_media_site(connection, items)
    platforms = connection.execute("SELECT COUNT(DISTINCT platform) FROM items").fetchone()[0]
    metrics = connection.execute("SELECT COUNT(*) FROM metrics").fetchone()[0]
    media = connection.execute("SELECT COUNT(*) FROM media_assets").fetchone()[0]
    snapshots = connection.execute("SELECT COUNT(*) FROM raw_snapshots").fetchone()[0]
    latest_version = connection.execute("SELECT dataset_version FROM collection_runs WHERE trigger <> 'legacy-migration' ORDER BY id DESC LIMIT 1").fetchone()[0]
    print(f"validated {len(raw_paths)} raw files/{snapshots} snapshots; latest {latest_version}; {items} items; {platforms} platforms; {metrics} metrics; {media} media assets; {sitemap_images} sitemap images; {sitemap_videos} sitemap videos; {len(index_records)} index records; {community_listings} community Listings; {market_plugins} market plugins")


if __name__ == "__main__":
    main()
