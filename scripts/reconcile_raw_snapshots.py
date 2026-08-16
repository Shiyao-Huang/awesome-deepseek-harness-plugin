#!/usr/bin/env python3
"""Import checked-in raw files missing from an existing full database."""

from __future__ import annotations

import argparse
from pathlib import Path

import collect


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"


def checked_in_raw_paths(raw_dir: Path) -> list[Path]:
    """Return raw JSON candidates that belong in the authoritative database."""

    return [
        path
        for path in sorted(raw_dir.rglob("*.json"))
        if "auto" not in path.parts and "forks" not in path.parts
    ]


def reconcile(database: Path, raw_dir: Path = RAW_DIR) -> tuple[str | None, collect.ImportStats]:
    """Import missing raw SHA-256 values and avoid an empty collection run."""

    collect.init_db(database)
    stats = collect.ImportStats()
    with collect.connect(database) as connection:
        known_hashes = {
            str(row[0])
            for row in connection.execute("SELECT raw_sha256 FROM raw_snapshots")
        }
        paths = [
            path
            for path in checked_in_raw_paths(raw_dir)
            if collect.sha256_file(path) not in known_hashes
        ]
        if not paths:
            return None, stats
        run_id, version, _ = collect.begin_collection_run(connection, "reconcile")
        try:
            for path in paths:
                try:
                    stats.add(collect.import_files(connection, [path], run_id))
                except Exception:
                    stats.raw_files_seen += 1
                    raise
            collect.finish_collection_run(connection, run_id, stats)
        except Exception as error:
            collect.finish_collection_run(connection, run_id, stats, "error", str(error))
            connection.commit()
            raise
    return version, stats


def main() -> int:
    """Run checked-in raw reconciliation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=collect.DB_PATH)
    args = parser.parse_args()
    version, stats = reconcile(args.database)
    if version is None:
        print(f"no unregistered checked-in raw files in {args.database}")
    else:
        print(
            f"reconciled {stats.item_observations} item observations from "
            f"{stats.raw_files_seen} raw file(s) in {version} into {args.database}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
