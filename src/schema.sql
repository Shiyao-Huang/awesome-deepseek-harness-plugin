PRAGMA foreign_keys = ON;
PRAGMA user_version = 2;

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY,
    platform TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    base_url TEXT NOT NULL,
    collection_mode TEXT NOT NULL,
    terms_url TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS collection_runs (
    id INTEGER PRIMARY KEY,
    dataset_version TEXT NOT NULL UNIQUE,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    scheduled_for TEXT,
    trigger TEXT NOT NULL,
    status TEXT NOT NULL,
    raw_files_seen INTEGER NOT NULL DEFAULT 0,
    raw_files_skipped INTEGER NOT NULL DEFAULT 0,
    observations_seen INTEGER NOT NULL DEFAULT 0,
    item_observations INTEGER NOT NULL DEFAULT 0,
    new_items INTEGER NOT NULL DEFAULT 0,
    existing_items INTEGER NOT NULL DEFAULT 0,
    new_metrics INTEGER NOT NULL DEFAULT 0,
    duplicate_metrics INTEGER NOT NULL DEFAULT 0,
    error_message TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS raw_snapshots (
    id INTEGER PRIMARY KEY,
    collection_run_id INTEGER REFERENCES collection_runs(id),
    raw_sha256 TEXT NOT NULL UNIQUE,
    raw_path TEXT NOT NULL,
    collected_at TEXT NOT NULL,
    byte_size INTEGER NOT NULL,
    payload_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS upstream_repositories (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL UNIQUE,
    source_url TEXT NOT NULL UNIQUE,
    default_branch TEXT NOT NULL,
    description TEXT,
    license_spdx TEXT,
    stars INTEGER,
    forks INTEGER,
    open_issues INTEGER,
    pushed_at TEXT,
    last_checked_at TEXT NOT NULL,
    readme_path TEXT,
    readme_sha TEXT,
    source_kind TEXT NOT NULL DEFAULT 'community-index',
    status TEXT NOT NULL DEFAULT 'ok',
    raw_snapshot_id INTEGER REFERENCES raw_snapshots(id)
);

CREATE TABLE IF NOT EXISTS upstream_entries (
    id INTEGER PRIMARY KEY,
    repository_id INTEGER NOT NULL REFERENCES upstream_repositories(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES items(id) ON DELETE SET NULL,
    entry_name TEXT NOT NULL,
    entry_url TEXT NOT NULL,
    entry_kind TEXT NOT NULL DEFAULT 'candidate',
    category TEXT,
    description TEXT,
    install_hint TEXT,
    source_path TEXT,
    source_line INTEGER,
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    UNIQUE(repository_id, entry_url, category)
);

CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES sources(id),
    collection_run_id INTEGER REFERENCES collection_runs(id),
    raw_snapshot_id INTEGER REFERENCES raw_snapshots(id),
    query TEXT NOT NULL,
    source_url TEXT NOT NULL,
    collected_at TEXT NOT NULL,
    collector TEXT NOT NULL,
    method TEXT NOT NULL,
    status TEXT NOT NULL,
    result_count INTEGER,
    notes TEXT,
    raw_path TEXT,
    raw_sha256 TEXT,
    UNIQUE(source_id, query, source_url, collected_at)
);

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    platform TEXT NOT NULL,
    external_id TEXT NOT NULL,
    canonical_url TEXT NOT NULL UNIQUE,
    item_type TEXT NOT NULL,
    title TEXT,
    author TEXT,
    author_url TEXT,
    published_at TEXT,
    published_label TEXT,
    content_text TEXT,
    language TEXT,
    category TEXT NOT NULL,
    relevance TEXT NOT NULL DEFAULT 'candidate',
    media_kind TEXT NOT NULL DEFAULT 'none',
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    first_seen_run_id INTEGER REFERENCES collection_runs(id),
    last_seen_run_id INTEGER REFERENCES collection_runs(id),
    raw_json TEXT NOT NULL,
    UNIQUE(platform, external_id)
);

CREATE TABLE IF NOT EXISTS index_records (
    id TEXT PRIMARY KEY,
    item_id INTEGER NOT NULL UNIQUE REFERENCES items(id) ON DELETE CASCADE,
    summary TEXT,
    url TEXT NOT NULL UNIQUE,
    repo TEXT,
    context TEXT NOT NULL,
    picture TEXT NOT NULL,
    comment INTEGER,
    favor INTEGER,
    views INTEGER,
    refs TEXT NOT NULL,
    rank INTEGER NOT NULL,
    stars INTEGER,
    dataset_version TEXT NOT NULL,
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS item_observations (
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    observation_id INTEGER NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
    PRIMARY KEY(item_id, observation_id)
);

CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    collection_run_id INTEGER REFERENCES collection_runs(id),
    observed_at TEXT NOT NULL,
    likes INTEGER,
    replies INTEGER,
    reposts INTEGER,
    comments INTEGER,
    bookmarks INTEGER,
    views INTEGER,
    points INTEGER,
    stars INTEGER,
    forks INTEGER,
    open_issues INTEGER,
    subscribers INTEGER,
    favorites INTEGER,
    shares INTEGER,
    coins INTEGER,
    danmaku INTEGER,
    upvote_ratio REAL,
    metric_source TEXT NOT NULL,
    raw_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS media_assets (
    id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    kind TEXT NOT NULL,
    url TEXT NOT NULL,
    thumbnail_url TEXT,
    alt_text TEXT,
    rights_note TEXT,
    UNIQUE(item_id, kind, url)
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS item_tags (
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY(item_id, tag_id)
);

CREATE INDEX IF NOT EXISTS idx_items_platform ON items(platform);
CREATE INDEX IF NOT EXISTS idx_items_category ON items(category);
CREATE INDEX IF NOT EXISTS idx_items_last_seen ON items(last_seen_at);
CREATE INDEX IF NOT EXISTS idx_index_records_item ON index_records(item_id);
CREATE INDEX IF NOT EXISTS idx_index_records_rank ON index_records(rank);
CREATE INDEX IF NOT EXISTS idx_items_last_seen_run ON items(last_seen_run_id);
CREATE INDEX IF NOT EXISTS idx_observations_run ON observations(collection_run_id);
CREATE INDEX IF NOT EXISTS idx_observations_raw_hash ON observations(raw_sha256);
CREATE INDEX IF NOT EXISTS idx_raw_snapshots_collected ON raw_snapshots(collected_at);
CREATE INDEX IF NOT EXISTS idx_upstream_entries_repo ON upstream_entries(repository_id);
CREATE INDEX IF NOT EXISTS idx_upstream_entries_item ON upstream_entries(item_id);
CREATE INDEX IF NOT EXISTS idx_upstream_entries_kind ON upstream_entries(entry_kind);
CREATE INDEX IF NOT EXISTS idx_metrics_item_observed ON metrics(item_id, observed_at DESC);
CREATE INDEX IF NOT EXISTS idx_metrics_run ON metrics(collection_run_id);
CREATE INDEX IF NOT EXISTS idx_media_kind ON media_assets(kind);
CREATE UNIQUE INDEX IF NOT EXISTS idx_metrics_dedupe ON metrics(item_id, observed_at, metric_source);

DROP VIEW IF EXISTS v_latest_metrics;
CREATE VIEW v_latest_metrics AS
SELECT
    i.id AS item_id,
    i.platform,
    i.external_id,
    i.canonical_url,
    i.item_type,
    i.title,
    i.author,
    i.category,
    i.media_kind,
    i.published_at,
    i.published_label,
    i.last_seen_at,
    m.observed_at,
    m.likes,
    m.replies,
    m.reposts,
    m.comments,
    m.bookmarks,
    m.views,
    m.points,
    m.stars,
    m.forks,
    m.open_issues,
    m.favorites,
    m.shares,
    m.coins,
    m.danmaku,
    m.upvote_ratio
FROM items AS i
LEFT JOIN metrics AS m
  ON m.id = (
      SELECT m2.id FROM metrics AS m2
      WHERE m2.item_id = i.id
      ORDER BY m2.observed_at DESC, m2.id DESC
      LIMIT 1
  );

CREATE VIEW IF NOT EXISTS v_timeline AS
SELECT
    COALESCE(published_at, first_seen_at) AS event_at,
    platform,
    item_type,
    title,
    author,
    category,
    canonical_url,
    published_label
FROM items;

CREATE VIEW IF NOT EXISTS v_category_rollup AS
SELECT
    category,
    COUNT(*) AS item_count,
    COUNT(DISTINCT platform) AS platform_count,
    COUNT(*) FILTER (WHERE media_kind <> 'none') AS media_count
FROM items
GROUP BY category;

DROP VIEW IF EXISTS v_collection_history;
CREATE VIEW v_collection_history AS
SELECT
    dataset_version,
    started_at,
    finished_at,
    scheduled_for,
    trigger,
    status,
    raw_files_seen,
    raw_files_skipped,
    observations_seen,
    item_observations,
    new_items,
    existing_items,
    new_metrics,
    duplicate_metrics,
    error_message,
    notes
FROM collection_runs
ORDER BY started_at DESC;

DROP VIEW IF EXISTS v_current_dataset;
CREATE VIEW v_current_dataset AS
SELECT *
FROM collection_runs
WHERE id = (
    SELECT id FROM collection_runs
    WHERE trigger <> 'legacy-migration'
    ORDER BY id DESC
    LIMIT 1
);
