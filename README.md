# awesome-deepseek-harness-plugin

DeepSeek Harness / DSH 插件生态的公开资料聚合 repo：把 GitHub 仓库、Hacker News、X、小红书、YouTube、哔哩哔哩、Reddit、知乎、微信公众号、LINUX DO、V2EX、微博和开放网页统一到一个可回溯索引。

从 [dsh store](docs/index.html) 开始浏览；它提供类似 skills.sh 的目录、搜索和分类页面，每条记录都有独立详情页。原始 Markdown 视图仍在 [docs/index.md](docs/index.md)、[docs/timeline.md](docs/timeline.md) 和 [docs/categories.md](docs/categories.md)，富媒体报告在 [docs/report.html](docs/report.html)。发布和 SEO 约定见 [docs/seo.md](docs/seo.md)。

<!-- landing:start -->
## Start here — the DSH signal desk

> 这里不是又一份静态 Awesome List，而是一张持续更新的 DeepSeek Harness 生态地图：先看最值得点开的仓库、帖子和视频，再沿着 raw、SQLite、时间轴回到证据。当前批次 **v20260820T045555Z**（2026-08-20）：**15,197** 条去重记录、**14** 个平台、**1,291** 个媒体引用。

[打开 dsh store](docs/index.html) · [看价值矩阵](docs/value-matrix.md) · [看趋势](docs/trends.md) · [下载查询 SQLite](https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin/releases/download/dataset-latest/aggregator.sqlite3)

![DeepSeek Harness official preview](media/screenshots/official.png)

### 先看这三个入口

| 入口 | 为什么值得看 | 当前信号 |
| --- | --- | ---: |
| [官方核心 · deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | DSH 的源头仓库；所有插件和能力最终回到这里核验。 | ★ stars 169,074 |
| [高关注插件 · zhu1090093659/dsh-web-ui](https://github.com/zhu1090093659/dsh-web-ui) | 真实可见的 UI / 桌面扩展，适合从“能不能直接用”开始。 | ★ stars 4,959 |
| [新文章 · 如何用 GLM 5.3，开发 DeepSeek Harness 插件](https://mp.weixin.qq.com/s/HrOgdg7ZBKQlvGM-xPeKtw) | 一篇文章串起模型接入、插件契约、skill、附件和 inspector；8 image · 1 video。 | counters NULL |

### 新：一篇文章与一项社区补充

> [如何用 GLM 5.3，开发 DeepSeek Harness 插件](https://mp.weixin.qq.com/s/HrOgdg7ZBKQlvGM-xPeKtw) · 金色传说大聪明 · 2026年8月15日 16:35 北京。文章报告作者用 GLM 5.3 为 DSH 补上 skill 索引、文件附件和约束/skill 检查能力；互动计数未公开，保持 `NULL`。相关历史报道：[DeepSeek Harness插件一夜燃爆GitHub：长期记忆、电子宠物、4399小游戏全来了](https://mp.weixin.qq.com/s/O6u4JsV-cFl9mKF9t5SJqw)。
> 另从 GitHub 的公开贡献记录补入 [CocoSgt/dsh-nsfw](https://github.com/CocoSgt/dsh-nsfw)：一个由仓库驱动的 DeepSeek 鲸鱼娘全年龄漫画收藏与分享站；当前 GitHub 快照为 10 stars、3 forks，详情以仓库 README 和 raw 记录为准。

| 插件 | 用途 |
| --- | --- |
| [CocoSgt/dsh-nsfw](https://github.com/CocoSgt/dsh-nsfw) | 由仓库驱动的 DeepSeek 鲸鱼娘全年龄漫画收藏与分享站。 · ★ stars 12 |
| [CocoSgt/dsh-skills](https://github.com/CocoSgt/dsh-skills) | 索引和加载项目里的 skill，支持完整 `.skill` 文件。 · ★ stars 13 |
| [CocoSgt/dsh-attachments](https://github.com/CocoSgt/dsh-attachments) | 为 DSH 增加文件/图片附件与继续引用能力。 · ★ stars 10 |
| [CocoSgt/dsh-inspector](https://github.com/CocoSgt/dsh-inspector) | 查看生效的约束文件和当前被索引的 skill。 · ★ stars 7 |

安装提示（文章原文，三个插件）：

```sh
dsh plugin --profile web add dsh-skills dsh-attachments dsh-inspector
```

### 大家正在关注什么

| 平台 | 记录 | 平台原生信号 | 为什么在首页 |
| --- | --- | ---: | --- |
| X | [DeepSeek Harness v0.1 is now available in Developer Preview!](https://x.com/deepseek_ai/status/2087887408440164663) | ♥ likes 19,518 · replies 740 | 官方发布与开发者传播 |
| YouTube | [DeepSeek Harness: The End of Claude Code?](https://www.youtube.com/watch?v=qg9EyGOZd9U) | views 42,000 | 长视频实测/解读 |
| 哔哩哔哩 | [【热门AI鉴定】DeepSeek Harness是什么？强在哪里？Harness实测效果如何？一口气搞懂！](https://www.bilibili.com/video/BV11CgF6uE4k) | views 446,982 · replies 656 | 中文教程与体验 |
| Hacker News | [DeepSeek Harness developer preview](https://news.ycombinator.com/item?id=49285244) | points 741 · comments 310 | 开发者讨论 |
| 小红书 | [DeepSeek Harness 保姆级安装教程](https://www.xiaohongshu.com/explore/6a7e2d740000000025017880) | ♥ likes 3,769 | 中文入门与教程 |

### 官方 Fork network：把分叉当作生态信号

沿 `deepseek-ai/deepseek-harness` 的公开分页，本批次登记 **12,302** 个 Fork（v20260816T110748Z）；按 **0+ stars** 进入排序的 **12,302** 个，深度盘点成功 **691** 个。它是公开信号和变体线索，不是质量、安全或诚信背书。

[打开 Fork 检索页](docs/forks.html) · [看 Fork 数据报告](docs/forks.md) · [下载完整压缩 SQLite 快照](https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin/releases/download/dataset-latest/aggregator-full.sqlite3.zst) · [看完整 JSONL 索引](index/forks.jsonl)

| Rank | Fork | stars | owner reputation | repo influence | overall | deep status | one-sentence evidence |
| ---: | --- | ---: | --- | ---: | ---: | --- | --- |
| 1 | [salathleizhang/deepseek-harness-desktop](https://github.com/salathleizhang/deepseek-harness-desktop) | 103 | 36.0 (observed) | 74.958 | 59.375 | ok | 新增约 42 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“Native desktop app for DeepSeek Harness — an Electron shell that runs the harness locally and hosts the official Web GUI unchanged”。 |
| 2 | [jasonkneen/deepseek-harness-plus](https://github.com/jasonkneen/deepseek-harness-plus) | 3 | 77.0 (observed) | 31.906 | 49.961 | ok | 新增约 2 个提交并修改 103 个文件，主要涉及 配置、文档、依赖、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 3 | [bojieli/deepseek-harness](https://github.com/bojieli/deepseek-harness) | 1 | 81.4 (observed) | 25.810 | 48.045 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 4 | [alexdolbun/deepseek-harness](https://github.com/alexdolbun/deepseek-harness) | 1 | 80.0 (observed) | 25.810 | 47.502 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 5 | [zchuhui/deepseek-harness](https://github.com/zchuhui/deepseek-harness) | 1 | 48.7 (observed) | 46.345 | 47.302 | ok | 新增约 10 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |

> 价值档当前分布：**A 2 · B 277 · C 2,246 · D 12,672**。分数只用于安排复核优先级；不同平台的 stars、likes、views、points 不相加，缺失互动数不补零。

<!-- landing:end -->

## 当前快照

<!-- snapshot:start -->
公开查询 SQLite 当前包含 **15,197 条去重记录**、**14 个来源平台**、**133,279 条指标历史**、**1,291 个媒体资产引用**、**306 条详情记录**和 **1,186 个去重 raw provenance**。当前批次 **v20260820T045555Z** 于 **2026-08-20T04:56:00Z** 完成；价值矩阵为当前批次的 15,197 条记录提供六维评分。完整原始 JSON 位于压缩权威 SQLite；公开查询库保留 raw SHA-256、路径、字节数、采集时间和批次，并去除可由 `data/raw/` 或完整库恢复的重复 JSON blob。

| 来源 | 去重记录 | 采集内容 |
| --- | ---: | --- |
| GitHub | 14,703 | 官方仓库、topic、社区索引候选和 stars/forks/issues |
| 小红书 | 157 | 搜索卡片、作者、点赞、缩略图和详情文本 |
| Hacker News | 115 | 精确短语搜索、points/comments 和讨论链接 |
| X | 90 | 公开帖子、图片/视频链接和 replies/reposts/likes/views |
| Reddit | 51 | 公开讨论、分数、评论和正文证据 |
| YouTube | 29 | 视频标题、频道、观看数和缩略图 |
| 开放网页 | 21 | 文章、教程和报道的公开元数据与摘要 |
| 哔哩哔哩 | 18 | 视频元数据、播放/点赞/投币/收藏/转发/弹幕/评论 |
| 微信公众号 | 7 | 公开文章、图像/视频外链和正文证据 |
| LINUX DO | 2 | 公开讨论页面和互动信息 |
| 官方站 | 1 | 官方页面和补充证据 |
| V2EX | 1 | 公开讨论页面和互动信息 |
| 微博 | 1 | 公开页面和互动信息 |
| 知乎 | 1 | 公开问题、回答和页面互动信息 |
<!-- snapshot:end -->

## 数据模型

```text
collection_runs ──< raw_snapshots
       ├──────< observations ──< item_observations >── items ──< metrics
       └───────────────────────────────────────────────────────├──< media_assets
       └──< item_tags >── tags
```

- `items`：以 canonical URL 去重的公开对象。
- `collection_runs`：每一批采集的 `dataset_version`、开始/结束时间、计划时间、触发方式、状态和统计结果。
- `raw_snapshots`：完整压缩库保存每个不同 SHA-256 的原始 JSON 文本；公开查询库保留同一组 SHA、路径、字节数、日期和批次 provenance，并把重复 JSON blob 置为 `{}`。
- `observations`：平台、查询、来源 URL、采集时间、方法、状态、raw 文件、SHA-256 和 collection run。
- `metrics`：按 `item_id + observed_at + metric_source` 去重的指标历史，不把不同平台计数相加。
- `media_assets`：外部图片、视频、缩略图和文档 URL；默认只保存链接，不镜像受版权保护的媒体。
- `item_details`：按 item 幂等保存的详情文本和 blocked/thin/failed provenance。
- `value_assessments`：按 collection run 和 scoring version 保存的六维价值矩阵；`v_current_value_matrix` 是当前批次视图。
- `fork_networks` / `fork_repositories` / `fork_snapshots`：官方仓库的公开 Fork 网络、日期指标、分页 raw、深度盘点和“一句话修改/目标线索”；完整 Fork-inclusive SQLite 由 [稳定 Release 资产](https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin/releases/download/dataset-latest/aggregator-full.sqlite3.zst) 提供。
- `github_user_profiles`：按 owner 去重的 GitHub 公开账号信号（followers、public repos、account age、gists、following），不保存 email 等隐私字段；profile 原始 API 响应进入 raw manifest 和 `raw_json`。
- `fork_commits` / `fork_file_changes` / `fork_rankings`：已观察提交、文件变更分类，以及“仓库影响力 + 用户公开信号 reputation”的版本化排序；轻量清单见 [index/forks.jsonl](index/forks.jsonl)，报告见 [docs/forks.md](docs/forks.md)。
- `index_records`：与 `index/records.jsonl` 同构的登记层，保存 `id/url/repo/context/picture/comment/favor/views/refs/rank/stars` 以及版本和日期字段。

权威数据库是 [最新完整压缩 SQLite](https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin/releases/download/dataset-latest/aggregator-full.sqlite3.zst)；[公开查询 SQLite](https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin/releases/download/dataset-latest/aggregator.sqlite3) 保留全部规范化记录、指标、版本、日期和 raw provenance。schema 在 [src/schema.sql](src/schema.sql)。

## Workspace 登记规则

原始证据位于 `data/raw/`，不可改写；登记索引位于 [index/records.jsonl](index/records.jsonl)，字段规范位于 [index/schema.json](index/schema.json)。索引的一条记录对应 SQLite 的 `index_records` 一行，使用 `id` 追溯到 `items`、`observations`、`raw_snapshots` 和原始文件。索引由 `python3 scripts/build_index.py` 生成，不手工编辑。

## Agent 市场注册表

公开 Market 数据可从 [线上 JSON](https://deeplugin.store/data/market-registry.json)、[JSON Schema](https://deeplugin.store/data/market-registry.schema.json) 或仓库内的 [index 镜像](index/market-registry.json) 读取；三份运行时镜像和三份 Schema 由 SQLite 统一生成并保持字节一致。[新增插件 Atom](https://deeplugin.store/feeds/new.atom.xml) 与 [实质更新 Atom](https://deeplugin.store/feeds/updated.atom.xml) 只在 Listing 首次出现或来源、版本、描述、分类等事实变化时产生条目，不把每两小时重复观测或互动数字波动误报成发布。每个插件详情页同时提供独立 Feed 和双语 launch packet。人类提交说明见 [docs/register.md](docs/register.md)，Agent 提交流程见 [docs/register-agent.md](docs/register-agent.md)。

把市场搜索工具安装到 DSH：

```sh
dsh plugin --profile web add github:Shiyao-Huang/awesome-deepseek-harness-plugin#path:/plugin
```

`verified=true` 只表示某个具名 Registry Source 声明了带版本的有限验证，不是 deeplugin.store 对安全性、兼容性、质量或官方身份的背书。`deeplugin_install_plan` 只生成可审查命令，始终要求用户明确确认，不会自动安装。

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
make build
make archive-full
make public-db
python3 scripts/validate.py
```

抓取公开 GitHub/HN API，并可同时导入新的 ego-browser 快照：

```sh
python3 scripts/collect.py update --raw data/raw/new-egolite.json
python3 scripts/build_views.py
```

刷新公开可访问的社区聚合项目、插件目录和发现工具：

```sh
python3 scripts/monitor_sources.py --raw-output data/raw/upstreams/$(date -u +%Y%m%dT%H%M%SZ).json
python3 scripts/build_index.py
python3 scripts/build_views.py
```

监测 `deepseek-ai/deepseek-harness` 的公开 fork network；默认保存完整分页 raw，并对影响力最高或最久未深扫的 fork 记录 compare、近期提交、README、owner profile 和变更分类。默认只让 `0+ stars` 进入排序；可以自行过滤，例如只看至少 10 stars 的 Fork：

```sh
python3 scripts/collect_forks.py
python3 scripts/collect_forks.py --min-stars 10
python3 scripts/build_fork_index.py
make archive-full
make public-db
```

Fork collector 的完整数据库会超过普通 Git 文件限制，因此固定 Release URL 提供完整压缩库和可直接查询的轻量库；每次刷新覆盖资产，不把 40–65 MiB 二进制重复写入 Git 历史。解压完整快照：`zstd -d aggregator-full.sqlite3.zst -o aggregator-full.sqlite3`。Star 过滤只影响排序和展示，低 Star Fork 仍保留在 raw、`fork_repositories` 和 `fork_snapshots`；`change_summary` 是基于 compare/README/description 的证据摘要，不是作者意图或质量背书。

计算价值矩阵并刷新全部派生视图：

```sh
python3 scripts/build_value_matrix.py
python3 scripts/build_index.py
python3 scripts/build_views.py
python3 scripts/build_readme.py
python3 scripts/validate.py
```

公开仓库的 [refresh-index workflow](.github/workflows/refresh-index.yml) 每两小时运行一次（UTC 的每个偶数小时第 17 分钟），监测上游 Awesome 仓库并更新 GitHub/Hacker News 公共 API，保留 `data/raw/upstreams/` 和带时间戳的 `data/raw/api/` 完整快照，提交 `index/` 与派生页面，并覆盖发布两个数据库 Release 资产。Fork network 使用独立的每日工作流。每次运行都会生成一个数据库内的 `dataset_version`；如果 raw SHA 已存在，则跳过 raw 和条目重复导入，但不同日期的互动指标仍作为历史观测保存。

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
  "SELECT raw_path, raw_sha256, byte_size, collected_at, collection_run_id FROM raw_snapshots ORDER BY collected_at DESC LIMIT 20;"
```

## 内容深度、质量评分与趋势

- **内容入库**：`scripts/enrich_content.py` 把 URL 背后的正文抓进 `item_details`（GitHub README ×150、HN 全评论树、新闻正文、知乎全文回答、Reddit 帖+评论、X 全文、B站简介、小红书笔记详情），当前 300+ 条、约 250 万字符，`status` 区分 ok/thin/blocked 并保留溯源。
- **质量评分**：`scripts/score.py`（入口指向 `build_value_matrix`）按 utility / evidence / traction / ecosystem / freshness / reviewability 六维打分，输出 `value_score`、`confidence_score`、`value_band` 与 `risk_flags`，查询入口 `v_current_value_matrix`，导出 `index/value-matrix.jsonl`。
- **趋势**：`make trends` 生成 [docs/trends.md](docs/trends.md) 与 4 张 SVG：生态增长（dsh-plugin 仓库/日 + 累计线）、全平台活跃度、价值档分布、互动/天增速榜；`metrics` 按 `observed_at` 去重形成时间序列，重复运行 `make update` 即可累积真实增量。

## License

代码和 schema 使用 MIT。采集到的元数据、截图、缩略图、视频和文章仍受各平台条款及原作者权利约束；如需删除或更正，请提交来源 URL 和理由。
