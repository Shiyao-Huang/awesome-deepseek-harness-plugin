PRAGMA foreign_keys = ON;
PRAGMA user_version = 4;

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

CREATE TABLE IF NOT EXISTS fork_networks (
    id INTEGER PRIMARY KEY,
    upstream_full_name TEXT NOT NULL UNIQUE,
    upstream_url TEXT NOT NULL UNIQUE,
    api_url TEXT NOT NULL,
    node_id TEXT,
    default_branch TEXT NOT NULL,
    description TEXT,
    license_spdx TEXT,
    stars INTEGER,
    forks INTEGER,
    open_issues INTEGER,
    watchers INTEGER,
    subscribers INTEGER,
    pushed_at TEXT,
    updated_at TEXT,
    last_checked_at TEXT NOT NULL,
    raw_snapshot_id INTEGER REFERENCES raw_snapshots(id),
    created_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS github_user_profiles (
    id INTEGER PRIMARY KEY,
    login TEXT NOT NULL UNIQUE,
    html_url TEXT,
    api_url TEXT,
    node_id TEXT,
    type TEXT,
    public_repos INTEGER,
    public_gists INTEGER,
    followers INTEGER,
    following INTEGER,
    created_at TEXT,
    updated_at TEXT,
    fetched_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'unobserved',
    raw_snapshot_id INTEGER REFERENCES raw_snapshots(id),
    raw_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS fork_repositories (
    id INTEGER PRIMARY KEY,
    network_id INTEGER NOT NULL REFERENCES fork_networks(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES items(id) ON DELETE SET NULL,
    full_name TEXT NOT NULL UNIQUE,
    html_url TEXT NOT NULL UNIQUE,
    api_url TEXT NOT NULL,
    node_id TEXT,
    owner_login TEXT NOT NULL,
    owner_type TEXT,
    owner_profile_id INTEGER REFERENCES github_user_profiles(id),
    owner_profile_status TEXT NOT NULL DEFAULT 'unobserved',
    owner_profile_checked_at TEXT,
    parent_full_name TEXT,
    source_full_name TEXT,
    default_branch TEXT NOT NULL,
    description TEXT,
    license_spdx TEXT,
    visibility TEXT,
    is_fork INTEGER NOT NULL DEFAULT 1 CHECK (is_fork IN (0, 1)),
    archived INTEGER NOT NULL DEFAULT 0 CHECK (archived IN (0, 1)),
    disabled INTEGER NOT NULL DEFAULT 0 CHECK (disabled IN (0, 1)),
    stars INTEGER,
    forks INTEGER,
    open_issues INTEGER,
    watchers INTEGER,
    subscribers INTEGER,
    size_kb INTEGER,
    forked_at TEXT,
    created_at TEXT,
    updated_at TEXT,
    pushed_at TEXT,
    last_checked_at TEXT NOT NULL,
    latest_commit_sha TEXT,
    latest_commit_message TEXT,
    latest_commit_at TEXT,
    readme_sha TEXT,
    change_summary TEXT,
    status TEXT NOT NULL DEFAULT 'ok',
    raw_snapshot_id INTEGER REFERENCES raw_snapshots(id),
    first_seen_run_id INTEGER REFERENCES collection_runs(id),
    last_seen_run_id INTEGER REFERENCES collection_runs(id),
    last_deep_checked_at TEXT,
    detail_status TEXT NOT NULL DEFAULT 'metadata-only',
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fork_snapshots (
    id INTEGER PRIMARY KEY,
    fork_id INTEGER NOT NULL REFERENCES fork_repositories(id) ON DELETE CASCADE,
    collection_run_id INTEGER NOT NULL REFERENCES collection_runs(id) ON DELETE CASCADE,
    raw_snapshot_id INTEGER REFERENCES raw_snapshots(id),
    dataset_version TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    stars INTEGER,
    forks INTEGER,
    open_issues INTEGER,
    watchers INTEGER,
    subscribers INTEGER,
    pushed_at TEXT,
    updated_at TEXT,
    compare_status TEXT,
    ahead_by INTEGER,
    behind_by INTEGER,
    total_commits INTEGER,
    changed_files INTEGER,
    additions INTEGER,
    deletions INTEGER,
    modification_categories TEXT NOT NULL,
    change_summary TEXT,
    latest_commit_sha TEXT,
    latest_commit_message TEXT,
    latest_commit_at TEXT,
    readme_sha TEXT,
    tree_sha TEXT,
    status TEXT NOT NULL DEFAULT 'ok',
    notes TEXT,
    UNIQUE(fork_id, collection_run_id)
);

CREATE TABLE IF NOT EXISTS fork_commits (
    id INTEGER PRIMARY KEY,
    fork_id INTEGER NOT NULL REFERENCES fork_repositories(id) ON DELETE CASCADE,
    snapshot_id INTEGER NOT NULL REFERENCES fork_snapshots(id) ON DELETE CASCADE,
    collection_run_id INTEGER NOT NULL REFERENCES collection_runs(id) ON DELETE CASCADE,
    sha TEXT NOT NULL,
    html_url TEXT,
    message TEXT NOT NULL,
    author_login TEXT,
    committer_login TEXT,
    authored_at TEXT,
    committed_at TEXT,
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    raw_json TEXT NOT NULL,
    UNIQUE(fork_id, sha)
);

CREATE TABLE IF NOT EXISTS fork_file_changes (
    id INTEGER PRIMARY KEY,
    snapshot_id INTEGER NOT NULL REFERENCES fork_snapshots(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    status TEXT,
    additions INTEGER,
    deletions INTEGER,
    changes INTEGER,
    previous_filename TEXT,
    category TEXT NOT NULL,
    blob_url TEXT,
    raw_url TEXT,
    raw_json TEXT NOT NULL,
    UNIQUE(snapshot_id, filename)
);

CREATE TABLE IF NOT EXISTS fork_rankings (
    fork_id INTEGER NOT NULL REFERENCES fork_repositories(id) ON DELETE CASCADE,
    collection_run_id INTEGER NOT NULL REFERENCES collection_runs(id) ON DELETE CASCADE,
    ranking_version TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    rank INTEGER NOT NULL,
    influence_score REAL NOT NULL,
    overall_score REAL NOT NULL DEFAULT 0,
    reputation_score REAL,
    reputation_coverage REAL NOT NULL DEFAULT 0,
    reputation_status TEXT NOT NULL DEFAULT 'unobserved',
    stars_component REAL NOT NULL,
    forks_component REAL NOT NULL,
    watchers_component REAL NOT NULL,
    activity_component REAL NOT NULL,
    divergence_component REAL NOT NULL,
    change_component REAL NOT NULL,
    reputation_followers_component REAL,
    reputation_repos_component REAL,
    reputation_age_component REAL,
    reputation_gists_component REAL,
    reputation_following_component REAL,
    repository_weight REAL NOT NULL DEFAULT 0.6,
    reputation_weight REAL NOT NULL DEFAULT 0.4,
    rationale TEXT NOT NULL,
    components_json TEXT NOT NULL,
    PRIMARY KEY(fork_id, collection_run_id, ranking_version)
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

CREATE TABLE IF NOT EXISTS item_details (
    item_id INTEGER PRIMARY KEY REFERENCES items(id) ON DELETE CASCADE,
    method TEXT NOT NULL,
    fetched_at TEXT NOT NULL,
    url TEXT,
    content TEXT NOT NULL,
    char_count INTEGER NOT NULL,
    language TEXT,
    status TEXT NOT NULL DEFAULT 'ok',
    notes TEXT
);

CREATE TABLE IF NOT EXISTS value_assessments (
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    collection_run_id INTEGER NOT NULL REFERENCES collection_runs(id) ON DELETE CASCADE,
    dataset_version TEXT NOT NULL,
    scoring_version TEXT NOT NULL,
    assessed_at TEXT NOT NULL,
    utility_score REAL NOT NULL CHECK (utility_score >= 0 AND utility_score <= 100),
    evidence_score REAL NOT NULL CHECK (evidence_score >= 0 AND evidence_score <= 100),
    traction_score REAL NOT NULL CHECK (traction_score >= 0 AND traction_score <= 100),
    ecosystem_score REAL NOT NULL CHECK (ecosystem_score >= 0 AND ecosystem_score <= 100),
    freshness_score REAL NOT NULL CHECK (freshness_score >= 0 AND freshness_score <= 100),
    reviewability_score REAL NOT NULL CHECK (reviewability_score >= 0 AND reviewability_score <= 100),
    value_score REAL NOT NULL CHECK (value_score >= 0 AND value_score <= 100),
    confidence_score REAL NOT NULL CHECK (confidence_score >= 0 AND confidence_score <= 100),
    value_band TEXT NOT NULL CHECK (value_band IN ('A', 'B', 'C', 'D')),
    evidence_count INTEGER NOT NULL DEFAULT 0,
    source_count INTEGER NOT NULL DEFAULT 0,
    risk_flags TEXT NOT NULL,
    components_json TEXT NOT NULL,
    PRIMARY KEY(item_id, collection_run_id, scoring_version)
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
CREATE INDEX IF NOT EXISTS idx_details_status ON item_details(status);
CREATE INDEX IF NOT EXISTS idx_value_assessments_run ON value_assessments(collection_run_id, value_score DESC);
CREATE INDEX IF NOT EXISTS idx_value_assessments_item ON value_assessments(item_id, assessed_at DESC);
CREATE INDEX IF NOT EXISTS idx_items_last_seen_run ON items(last_seen_run_id);
CREATE INDEX IF NOT EXISTS idx_observations_run ON observations(collection_run_id);
CREATE INDEX IF NOT EXISTS idx_observations_raw_hash ON observations(raw_sha256);
CREATE INDEX IF NOT EXISTS idx_raw_snapshots_collected ON raw_snapshots(collected_at);
CREATE INDEX IF NOT EXISTS idx_github_user_profiles_fetched ON github_user_profiles(fetched_at);
CREATE INDEX IF NOT EXISTS idx_fork_repositories_owner_profile ON fork_repositories(owner_profile_id);
CREATE INDEX IF NOT EXISTS idx_fork_rankings_overall ON fork_rankings(collection_run_id, overall_score DESC);
CREATE INDEX IF NOT EXISTS idx_upstream_entries_repo ON upstream_entries(repository_id);
CREATE INDEX IF NOT EXISTS idx_upstream_entries_item ON upstream_entries(item_id);
CREATE INDEX IF NOT EXISTS idx_upstream_entries_kind ON upstream_entries(entry_kind);
CREATE INDEX IF NOT EXISTS idx_fork_networks_checked ON fork_networks(last_checked_at);
CREATE INDEX IF NOT EXISTS idx_fork_repositories_network ON fork_repositories(network_id);
CREATE INDEX IF NOT EXISTS idx_fork_repositories_stars ON fork_repositories(stars DESC);
CREATE INDEX IF NOT EXISTS idx_fork_repositories_last_seen ON fork_repositories(last_seen_at);
CREATE INDEX IF NOT EXISTS idx_fork_snapshots_fork_observed ON fork_snapshots(fork_id, observed_at DESC);
CREATE INDEX IF NOT EXISTS idx_fork_snapshots_run ON fork_snapshots(collection_run_id);
CREATE INDEX IF NOT EXISTS idx_fork_commits_fork_date ON fork_commits(fork_id, committed_at DESC);
CREATE INDEX IF NOT EXISTS idx_fork_file_changes_snapshot ON fork_file_changes(snapshot_id);
CREATE INDEX IF NOT EXISTS idx_fork_file_changes_category ON fork_file_changes(category);
CREATE INDEX IF NOT EXISTS idx_fork_rankings_run_score ON fork_rankings(collection_run_id, influence_score DESC);
CREATE INDEX IF NOT EXISTS idx_fork_rankings_fork_date ON fork_rankings(fork_id, observed_at DESC);
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

DROP VIEW IF EXISTS v_current_value_matrix;
CREATE VIEW v_current_value_matrix AS
SELECT va.*
FROM value_assessments AS va
WHERE va.collection_run_id = (
    SELECT id FROM collection_runs
    WHERE trigger <> 'legacy-migration'
    ORDER BY id DESC
    LIMIT 1
);

DROP VIEW IF EXISTS v_latest_fork_snapshots;
CREATE VIEW v_latest_fork_snapshots AS
SELECT fs.*
FROM fork_snapshots AS fs
WHERE fs.id = (
    SELECT fs2.id
    FROM fork_snapshots AS fs2
    WHERE fs2.fork_id = fs.fork_id
    ORDER BY fs2.observed_at DESC, fs2.id DESC
    LIMIT 1
);

DROP VIEW IF EXISTS v_current_fork_rankings;
CREATE VIEW v_current_fork_rankings AS
SELECT fr.*, fp.full_name, fp.html_url, fp.owner_login, fp.description,
       fp.parent_full_name, fp.source_full_name, fp.default_branch,
       fp.archived, fp.disabled, fp.stars, fp.forks, fp.open_issues,
       fp.pushed_at, fp.latest_commit_sha, fp.latest_commit_message,
       fp.latest_commit_at
FROM fork_rankings AS fr
JOIN fork_repositories AS fp ON fp.id = fr.fork_id
WHERE fr.collection_run_id = (
    SELECT fr2.collection_run_id
    FROM fork_rankings AS fr2
    JOIN collection_runs AS cr ON cr.id = fr2.collection_run_id
    WHERE cr.status = 'succeeded'
    ORDER BY fr2.observed_at DESC, fr2.collection_run_id DESC
    LIMIT 1
);
