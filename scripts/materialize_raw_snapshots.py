#!/usr/bin/env python3
"""Restore immutable raw files and unique paths from the authoritative SQLite archive."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sqlite3
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "aggregator.sqlite3"


@dataclass(frozen=True)
class Repair:
    """Describe one raw snapshot that must move to an immutable physical path."""

    snapshot_id: int
    old_path: str
    new_path: str
    raw_sha256: str
    payload: bytes


def sha256_bytes(payload: bytes) -> str:
    """Return the SHA-256 digest of a byte string."""

    return hashlib.sha256(payload).hexdigest()


def resolve_raw_path(root: Path, raw_path: str) -> Path:
    """Resolve one database path and require it to remain under data/raw."""

    relative = Path(raw_path)
    if relative.is_absolute():
        raise RuntimeError(f"raw path must be relative: {raw_path}")
    raw_root = (root / "data" / "raw").resolve()
    resolved = (root / relative).resolve()
    if not resolved.is_relative_to(raw_root):
        raise RuntimeError(f"raw path escapes data/raw: {raw_path}")
    return resolved


def replacement_path(path: Path, collected_at: str, raw_sha256: str) -> Path:
    """Return a deterministic collision-free sibling path for a historical snapshot."""

    timestamp = re.sub(r"[^0-9A-Za-z]", "", collected_at)
    suffix = path.suffix or ".json"
    stem = path.name[:-len(path.suffix)] if path.suffix else path.name
    return path.with_name(f"{stem}--{timestamp}--{raw_sha256[:12]}{suffix}")


def plan_repairs(
    connection: sqlite3.Connection,
    root: Path,
    *,
    include_forks: bool = False,
) -> list[Repair]:
    """Return repairs for missing, overwritten, or path-colliding raw snapshots."""

    repairs: list[Repair] = []
    digest_cache: dict[Path, str | None] = {}
    rows = connection.execute(
        "SELECT id, raw_path, collected_at, raw_sha256, payload_json "
        "FROM raw_snapshots ORDER BY raw_path, collected_at, id"
    ).fetchall()
    for snapshot_id, raw_path, collected_at, expected_digest, payload_json in rows:
        relative = Path(str(raw_path))
        if not include_forks and relative.parts[:3] == ("data", "raw", "forks"):
            continue
        path = resolve_raw_path(root, str(raw_path))
        if path not in digest_cache:
            digest_cache[path] = sha256_bytes(path.read_bytes()) if path.is_file() else None
        if digest_cache[path] == expected_digest:
            continue
        if payload_json == "{}":
            raise RuntimeError(
                f"snapshot {snapshot_id} needs repair but its payload was stripped; use the full archive"
            )
        payload = str(payload_json).encode("utf-8")
        actual_digest = sha256_bytes(payload)
        if actual_digest != expected_digest:
            raise RuntimeError(
                f"snapshot {snapshot_id} payload digest {actual_digest} != {expected_digest}"
            )
        target = replacement_path(path, str(collected_at), str(expected_digest))
        target_relative = target.relative_to(root.resolve()).as_posix()
        if target.is_file() and sha256_bytes(target.read_bytes()) != expected_digest:
            raise RuntimeError(f"repair target contains different bytes: {target_relative}")
        repairs.append(
            Repair(int(snapshot_id), str(raw_path), target_relative, str(expected_digest), payload)
        )
    return repairs


def write_atomic(path: Path, payload: bytes) -> None:
    """Write one raw payload atomically without replacing an existing file."""

    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        if path.exists():
            raise RuntimeError(f"repair target appeared during write: {path}")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def materialize(db_path: Path, root: Path, *, include_forks: bool = False) -> list[Repair]:
    """Write recoverable raw payloads and update their SQLite paths transactionally."""

    connection = sqlite3.connect(db_path)
    try:
        repairs = plan_repairs(connection, root, include_forks=include_forks)
        for repair in repairs:
            target = resolve_raw_path(root, repair.new_path)
            write_atomic(target, repair.payload)
            connection.execute(
                "UPDATE raw_snapshots SET raw_path = ? WHERE id = ? AND raw_sha256 = ?",
                (repair.new_path, repair.snapshot_id, repair.raw_sha256),
            )
        connection.commit()
        return repairs
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--include-forks",
        action="store_true",
        help="also expand release-only Fork API payloads under ignored data/raw/forks",
    )
    return parser.parse_args()


def main() -> int:
    """Restore mismatched raw paths and report every materialized snapshot."""

    args = parse_args()
    repairs = materialize(
        args.db.resolve(),
        args.root.resolve(),
        include_forks=args.include_forks,
    )
    for repair in repairs:
        print(f"snapshot {repair.snapshot_id}: {repair.old_path} -> {repair.new_path}")
    print(f"materialized {len(repairs)} raw snapshot(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
