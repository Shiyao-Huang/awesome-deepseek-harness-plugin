# awesome-deepseek-harness-plugin

DeepSeek Harness / DSH 插件生态的公开资料聚合 repo：把 GitHub 仓库、Hacker News、X、小红书、YouTube、哔哩哔哩、Reddit、知乎、微信公众号、LINUX DO、V2EX、微博和开放网页统一到一个可回溯索引。

从 [docs/index.md](docs/index.md) 开始浏览；[docs/timeline.md](docs/timeline.md) 是时间轴，[docs/categories.md](docs/categories.md) 是启发式归类，[docs/sources.md](docs/sources.md) 是上游目录监测，[docs/report.html](docs/report.html) 是带 SVG 图表和高关注条目的富媒体报告。

## 当前快照

本地 SQLite 当前包含 **848 条去重记录**、**13 个来源平台**、**909 条指标历史**、**613 个媒体资产引用**和 **81 个去重 raw snapshot**。raw snapshot 不是摘要：`raw_snapshots.payload_json` 保存原始 JSON 文本本身，并同时保存 SHA-256、原始路径、字节数、采集时间和采集批次。

| 来源 | 去重记录 | 采集内容 |
| --- | ---: | --- |
| GitHub | 684 | 官方仓库、`dsh-plugin` topic、社区索引候选、stars/forks/issues |
| X | 43 | 公开帖子、图片/视频链接、replies/reposts/likes/bookmarks/views |
| Hacker News | 44 | 精确短语与扩展搜索、points/comments、帖子链接 |
| 小红书 | 25 | 搜索卡片、作者、相对时间、点赞、缩略图；详情页限制保留在 provenance |
| Open Web | 22 | 文章/教程/报道的公开元数据和摘要 |
| YouTube | 13 | 视频标题、频道、观看数、视频链接和缩略图 |
| 哔哩哔哩 | 6 | 视频元数据、播放/点赞/投币/收藏/转发/弹幕/评论 |
| Reddit、LINUX DO、官方站、V2EX、微信公众号、微博 | 11 | 讨论、文章和公开页面补充证据 |

## 数据模型

```text
collection_runs ──< raw_snapshots
       ├──────< observations ──< item_observations >── items ──< metrics
       └───────────────────────────────────────────────────────├──< media_assets
       └──< item_tags >── tags
```

上游目录关系单独保存在 `upstream_repositories ──< upstream_entries ──> items`：源仓库的 README/结构化目录是 raw 证据，条目只作为候选引用，安装和安全判断回到插件仓库本身。

- `items`：以 canonical URL 去重的公开对象。
- `collection_runs`：每一批采集的 `dataset_version`、开始/结束时间、计划时间、触发方式、状态和统计结果。
- `raw_snapshots`：每个不同 SHA-256 的完整原始 JSON 文本；同一个 raw 文件重复导入时只保留一份。
- `observations`：平台、查询、来源 URL、采集时间、方法、状态、raw 文件、SHA-256 和 collection run。
- `metrics`：按 `item_id + observed_at + metric_source` 去重的指标历史，不把不同平台计数相加。
- `media_assets`：外部图片、视频、缩略图和文档 URL；默认只保存链接，不镜像受版权保护的媒体。
- `upstream_repositories` / `upstream_entries`：三个社区 Awesome 目录的版本化元数据、插件链接、分类、安装提示和与去重 item 的关系。
- `index_records`：与 `index/records.jsonl` 同构的登记层，保存 `id/url/repo/context/picture/comment/favor/views/refs/rank/stars` 以及版本和日期字段。

权威数据库是 [data/aggregator.sqlite3](data/aggregator.sqlite3)，schema 在 [src/schema.sql](src/schema.sql)。

## Workspace 登记规则

原始证据位于 `data/raw/`，不可改写；登记索引位于 [index/records.jsonl](index/records.jsonl)，字段规范位于 [index/schema.json](index/schema.json)。索引的一条记录对应 SQLite 的 `index_records` 一行，使用 `id` 追溯到 `items`、`observations`、`raw_snapshots` 和原始文件。索引由 `python3 scripts/build_index.py` 生成，不手工编辑。

## 图文与视频

首轮公开页面截图放在 `media/screenshots/`，可用于人工复核；外部图片/视频/缩略图 URL 和媒体权利说明在 SQLite 的 `media_assets` 中。示例：

![X 官宣帖](media/screenshots/x-deepseek-ai-announce.png)
![小红书搜索页](media/screenshots/xiaohongshu-search.png)
![官方开发者预览页](media/screenshots/official.png)
![知乎问题页](media/screenshots/zhihu-question.png)

截图、平台原图和作者内容仍受原平台及作者权利约束；本 repo 只做公开资料研究索引。

## 更新

从已审核 raw 重建数据库并刷新 index：

```sh
python3 scripts/collect.py init
python3 scripts/collect.py seed
python3 scripts/build_views.py
python3 scripts/validate.py
```

抓取公开 GitHub/HN API，并可同时导入新的 ego-browser 快照：

```sh
python3 scripts/collect.py update --raw data/raw/new-egolite.json
python3 scripts/build_views.py
```

监测配置中的社区源仓库并导入上游插件目录：

```sh
python3 scripts/monitor_sources.py --raw-output data/raw/upstreams/$(date -u +%Y%m%dT%H%M%SZ).json
python3 scripts/build_index.py
python3 scripts/build_views.py
```

公开仓库的 [refresh-index workflow](.github/workflows/refresh-index.yml) 每两小时运行一次（UTC 的每个偶数小时第 17 分钟），先监测三个上游 Awesome 仓库，再更新 GitHub/Hacker News 公共 API，保留 `data/raw/upstreams/` 和带时间戳的 `data/raw/api/` 完整快照，并提交 SQLite、`index/` 和派生页面。每次运行都会生成一个数据库内的 `dataset_version`；如果 raw SHA 已存在，则跳过 raw 和条目重复导入，但不同日期的互动指标仍作为历史观测保存。

X、小红书、Reddit、微信公众号等需要登录态或浏览器可见 DOM 的来源，不会在 CI 中绕过登录、验证码或访问限制；继续通过 ego-browser 保存完整可见证据 JSON、截图路径和媒体 URL 后，用 `--raw` 导入。定时任务会自动收集它有权限公开访问的 API 数据，浏览器来源仍以合法可见的 raw 输入为准。

ego-browser 采集约定：只保存公开可见 DOM、标题、作者、页面显示的互动数字、公开链接和缩略图；不绕过登录、验证码、扫码或访问限制。遇到拦截页，raw 保留原始证据，observation 使用 `blocked` 状态，不伪造标题或互动数。

`data/raw/auto/` 只用于本地 API 快照，默认不进入 git；公开定时任务写入 `data/raw/api/`。需要发表的本地快照请复制到日期命名的已审核 raw 文件。

## SQLite 查询示例

```sh
sqlite3 data/aggregator.sqlite3 \
  "SELECT platform, title, stars, likes, views FROM v_latest_metrics ORDER BY COALESCE(stars, likes, views, 0) DESC LIMIT 20;"

sqlite3 data/aggregator.sqlite3 \
  "SELECT event_at, platform, title FROM v_timeline ORDER BY event_at DESC LIMIT 50;"

sqlite3 data/aggregator.sqlite3 \
  "SELECT category, COUNT(*) FROM items GROUP BY category ORDER BY COUNT(*) DESC;"

sqlite3 data/aggregator.sqlite3 \
  "SELECT dataset_version, started_at, status, raw_files_seen, raw_files_skipped FROM v_collection_history LIMIT 20;"

sqlite3 data/aggregator.sqlite3 \
  "SELECT raw_path, raw_sha256, byte_size, collected_at, length(payload_json) FROM raw_snapshots ORDER BY collected_at DESC LIMIT 20;"
```

## License

代码和 schema 使用 MIT。采集到的元数据、截图、缩略图、视频和文章仍受各平台条款及原作者权利约束；如需删除或更正，请提交来源 URL 和理由。
