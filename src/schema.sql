PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY,
    platform TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    base_url TEXT NOT NULL,
    collection_mode TEXT NOT NULL,
    terms_url TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES sources(id),
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
    raw_json TEXT NOT NULL,
    UNIQUE(platform, external_id)
);

CREATE TABLE IF NOT EXISTS item_observations (
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    observation_id INTEGER NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
    PRIMARY KEY(item_id, observation_id)
);

CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
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
CREATE INDEX IF NOT EXISTS idx_metrics_item_observed ON metrics(item_id, observed_at DESC);
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
