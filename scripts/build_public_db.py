#!/usr/bin/env python3
"""Build a GitHub-compatible SQLite projection without mutating the full archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "aggregator.sqlite3"
DEFAULT_FULL_ARCHIVE = ROOT / "data" / "aggregator-full.sqlite3.zst"
PROJECTION_VERSION = 3
STRIPPED_JSON_COLUMNS = (
    ("raw_snapshots", "payload_json"),
    ("items", "raw_json"),
    ("metrics", "raw_json"),
    ("github_user_profiles", "raw_json"),
    ("fork_file_changes", "raw_json"),
    ("fork_commits", "raw_json"),
    ("fork_rankings", "components_json"),
    ("upstream_entries", "source_json"),
)
FORK_SNAPSHOT_RETENTION = """
    fork_snapshots.id = (
        SELECT MAX(latest.id)
        FROM fork_snapshots AS latest
        WHERE latest.fork_id = fork_snapshots.fork_id
    )
    OR EXISTS (
        SELECT 1 FROM fork_commits
        WHERE fork_commits.snapshot_id = fork_snapshots.id
    )
    OR EXISTS (
        SELECT 1 FROM fork_file_changes
        WHERE fork_file_changes.snapshot_id = fork_snapshots.id
    )
"""
UPSTREAM_ENTRY_OBSERVATION_RETENTION = """
    upstream_entry_observations.id = (
        SELECT latest.id
        FROM upstream_entry_observations AS latest
        WHERE latest.entry_id = upstream_entry_observations.entry_id
        ORDER BY latest.collection_run_id DESC, latest.id DESC
        LIMIT 1
    )
"""


def utc_now() -> str:
    """Return a second-precision UTC timestamp."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest of one file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_zstd_payload(path: Path) -> str:
    """Return the SHA-256 digest of the bytes inside a Zstandard archive."""

    digest = hashlib.sha256()
    try:
        process = subprocess.Popen(
            ["zstd", "--decompress", "--stdout", str(path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as error:
        raise RuntimeError("zstd is required to verify an in-place full archive") from error
    assert process.stdout is not None
    for chunk in iter(lambda: process.stdout.read(4 * 1024 * 1024), b""):
        digest.update(chunk)
    stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
    if process.wait() != 0:
        raise RuntimeError(f"could not verify {path}: {stderr.strip()}")
    return digest.hexdigest()


def connect_read_only(path: Path) -> sqlite3.Connection:
    """Open an existing SQLite database without permitting mutations."""

    connection = sqlite3.connect(f"file:{path.resolve()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def user_tables(connection: sqlite3.Connection) -> set[str]:
    """Return application-owned table names."""

    return {
        str(row[0])
        for row in connection.execute(
            "SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        )
    }


def table_counts(connection: sqlite3.Connection) -> dict[str, int]:
    """Return row counts for every application-owned table."""

    return {
        table: int(connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0])
        for table in sorted(user_tables(connection))
    }


def verify_archive(source: Path, archive: Path) -> str:
    """Require a full archive whose decompressed bytes equal the source database."""

    if not archive.is_file() or archive.stat().st_size == 0:
        raise RuntimeError(f"full archive is missing or empty: {archive}")
    source_sha256 = sha256_file(source)
    archive_sha256 = sha256_zstd_payload(archive)
    if source_sha256 != archive_sha256:
        raise RuntimeError(
            "refusing in-place projection: the full archive does not match the source SQLite "
            f"({archive_sha256} != {source_sha256})"
        )
    return source_sha256


def copy_database(source: Path, destination: Path) -> None:
    """Create a transactionally consistent SQLite copy."""

    with connect_read_only(source) as source_connection, sqlite3.connect(destination) as destination_connection:
        source_connection.backup(destination_connection, pages=32768)


def latest_complete_value_run(connection: sqlite3.Connection) -> int:
    """Return the newest value-matrix run covering every normalized item."""

    row = connection.execute(
        """
        SELECT collection_run_id
        FROM value_assessments
        GROUP BY collection_run_id
        HAVING COUNT(*) = (SELECT COUNT(*) FROM items)
        ORDER BY collection_run_id DESC
        LIMIT 1
        """
    ).fetchone()
    if row is None:
        raise RuntimeError("no value assessment run covers every item")
    run_id = int(row[0])
    latest_run = connection.execute(
        "SELECT id FROM collection_runs WHERE trigger <> 'legacy-migration' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    if latest_run is None or int(latest_run[0]) != run_id:
        raise RuntimeError("latest collection run has no complete value matrix; rebuild it before projection")
    return run_id


def project_database(path: Path, source_sha256: str, archive_label: str) -> int:
    """Remove duplicated blobs and superseded derived rows from a copy."""

    connection = sqlite3.connect(path)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        tables = user_tables(connection)
        required_tables = {table for table, _ in STRIPPED_JSON_COLUMNS} | {
            "collection_runs",
            "fork_snapshots",
            "upstream_entry_observations",
            "value_assessments",
        }
        missing = sorted(required_tables - tables)
        if missing:
            raise RuntimeError(f"database is missing required tables: {', '.join(missing)}")
        latest_value_run_id = latest_complete_value_run(connection)
        for table, column in STRIPPED_JSON_COLUMNS:
            columns = {str(row[1]) for row in connection.execute(f'PRAGMA table_info("{table}")')}
            if column not in columns:
                raise RuntimeError(f"database is missing required column: {table}.{column}")
            connection.execute(f'UPDATE "{table}" SET "{column}" = ?', ("{}",))
        connection.execute(
            "DELETE FROM value_assessments WHERE collection_run_id <> ?",
            (latest_value_run_id,),
        )
        latest_fork_ranking_run = connection.execute(
            "SELECT MAX(collection_run_id) FROM fork_rankings"
        ).fetchone()[0]
        if latest_fork_ranking_run is None:
            raise RuntimeError("no Fork ranking run is available for the public projection")
        connection.execute(
            "DELETE FROM fork_rankings WHERE collection_run_id <> ?",
            (int(latest_fork_ranking_run),),
        )
        connection.execute(
            f"DELETE FROM fork_snapshots WHERE NOT ({FORK_SNAPSHOT_RETENTION})"
        )
        connection.execute(
            f"DELETE FROM upstream_entry_observations WHERE NOT ({UPSTREAM_ENTRY_OBSERVATION_RETENTION})"
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS public_projection_metadata (
                projection_version INTEGER PRIMARY KEY,
                generated_at TEXT NOT NULL,
                source_sha256 TEXT NOT NULL,
                authoritative_archive TEXT NOT NULL,
                latest_value_run_id INTEGER NOT NULL,
                stripped_fields_json TEXT NOT NULL
            )
            """
        )
        connection.execute("DELETE FROM public_projection_metadata")
        connection.execute(
            """
            INSERT INTO public_projection_metadata(
                projection_version, generated_at, source_sha256, authoritative_archive,
                latest_value_run_id, stripped_fields_json
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                PROJECTION_VERSION,
                utc_now(),
                source_sha256,
                archive_label,
                latest_value_run_id,
                json.dumps(
                    {
                        "stripped_fields": [
                            f"{table}.{column}" for table, column in STRIPPED_JSON_COLUMNS
                        ],
                        "retention": {
                            "fork_rankings": "latest collection run",
                            "fork_snapshots": "latest per Fork plus commit/file-evidence snapshots",
                            "upstream_entry_observations": "latest per Registry Listing",
                            "value_assessments": "latest complete collection run",
                        },
                    },
                    sort_keys=True,
                ),
            ),
        )
        connection.commit()
        connection.execute("VACUUM")
        return latest_value_run_id
    finally:
        connection.close()


def verify_projection(
    source: Path,
    projected: Path,
    latest_value_run_id: int,
    max_bytes: int,
) -> dict[str, int | str]:
    """Verify integrity, row preservation, deduplication, and the publication limit."""

    output_bytes = projected.stat().st_size
    if output_bytes > max_bytes:
        raise RuntimeError(f"public SQLite is {output_bytes} bytes; limit is {max_bytes} bytes")
    with connect_read_only(source) as source_connection, connect_read_only(projected) as output_connection:
        integrity = str(output_connection.execute("PRAGMA integrity_check").fetchone()[0])
        if integrity != "ok":
            raise RuntimeError(f"public SQLite integrity check failed: {integrity}")
        foreign_key_errors = output_connection.execute("PRAGMA foreign_key_check").fetchall()
        if foreign_key_errors:
            raise RuntimeError(f"public SQLite has {len(foreign_key_errors)} foreign-key error(s)")
        source_counts = table_counts(source_connection)
        output_counts = table_counts(output_connection)
        for table, expected in source_counts.items():
            if table == "value_assessments":
                expected = int(
                    source_connection.execute(
                        "SELECT COUNT(*) FROM value_assessments WHERE collection_run_id = ?",
                        (latest_value_run_id,),
                    ).fetchone()[0]
                )
            elif table == "fork_rankings":
                expected = int(
                    source_connection.execute(
                        """
                        SELECT COUNT(*)
                        FROM fork_rankings
                        WHERE collection_run_id = (SELECT MAX(collection_run_id) FROM fork_rankings)
                        """
                    ).fetchone()[0]
                )
            elif table == "fork_snapshots":
                expected = int(
                    source_connection.execute(
                        f"SELECT COUNT(*) FROM fork_snapshots WHERE {FORK_SNAPSHOT_RETENTION}"
                    ).fetchone()[0]
                )
            elif table == "upstream_entry_observations":
                expected = int(
                    source_connection.execute(
                        f"SELECT COUNT(*) FROM upstream_entry_observations WHERE {UPSTREAM_ENTRY_OBSERVATION_RETENTION}"
                    ).fetchone()[0]
                )
            actual = output_counts.get(table)
            if actual != expected:
                raise RuntimeError(f"row-count mismatch for {table}: {actual} != {expected}")
        for table, column in STRIPPED_JSON_COLUMNS:
            nonempty_raw = int(
                output_connection.execute(
                    f'SELECT COUNT(*) FROM "{table}" WHERE "{column}" <> ?',
                    ("{}",),
                ).fetchone()[0]
            )
            if nonempty_raw:
                raise RuntimeError(f"{table}.{column} retains {nonempty_raw} duplicated raw value(s)")
        duplicate_urls = int(
            output_connection.execute(
                "SELECT COUNT(*) - COUNT(DISTINCT canonical_url) FROM items"
            ).fetchone()[0]
        )
        duplicate_external_ids = int(
            output_connection.execute(
                "SELECT COUNT(*) - COUNT(DISTINCT platform || char(0) || external_id) FROM items"
            ).fetchone()[0]
        )
        duplicate_raw_hashes = int(
            output_connection.execute(
                "SELECT COUNT(*) - COUNT(DISTINCT raw_sha256) FROM raw_snapshots"
            ).fetchone()[0]
        )
        if duplicate_urls or duplicate_external_ids or duplicate_raw_hashes:
            raise RuntimeError(
                "deduplication invariant failed: "
                f"urls={duplicate_urls}, external_ids={duplicate_external_ids}, raw_sha256={duplicate_raw_hashes}"
            )
        return {
            "items": output_counts["items"],
            "metrics": output_counts["metrics"],
            "raw_snapshots": output_counts["raw_snapshots"],
            "listing_observations": output_counts["upstream_entry_observations"],
            "value_assessments": output_counts["value_assessments"],
            "bytes": output_bytes,
            "integrity": integrity,
        }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "aggregator-public.sqlite3")
    parser.add_argument("--full-archive", type=Path, default=DEFAULT_FULL_ARCHIVE)
    parser.add_argument("--max-mib", type=float, default=95.0)
    parser.add_argument("--replace", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    return parser.parse_args()


def main() -> int:
    """Build and atomically publish the lightweight SQLite projection."""

    args = parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    archive = args.full_archive.resolve()
    if not source.is_file():
        raise SystemExit(f"source SQLite does not exist: {source}")
    same_path = source == output
    if same_path and not args.in_place:
        raise SystemExit("--in-place is required when --source and --output are the same path")
    if output.exists() and not same_path and not args.replace:
        raise SystemExit(f"output exists; pass --replace to overwrite it: {output}")
    source_sha256 = verify_archive(source, archive)
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output.name}.public-",
        suffix=".tmp",
        dir=output.parent,
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        copy_database(source, temporary)
        latest_value_run_id = project_database(temporary, source_sha256, str(args.full_archive))
        report = verify_projection(
            source,
            temporary,
            latest_value_run_id,
            int(args.max_mib * 1024 * 1024),
        )
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    print(json.dumps({"output": str(output), **report}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
