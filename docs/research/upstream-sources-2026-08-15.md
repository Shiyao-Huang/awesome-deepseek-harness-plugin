# 上游来源一手研究：DeepSeek Harness 插件目录

- 采集时间：2026-08-15T15:10:27+08:00；GitHub API 时间字段保留 UTC。
- 研究范围：核对一篇微信公众号文章和三个公开 GitHub 目录仓库，记录其可追溯元数据、条目组织方式、最近提交和限制。
- 采集方法：公众号通过公开页面 DOM 读取；GitHub 使用官方 REST API 的仓库元数据、README、根目录、递归 Git tree、LICENSE 和 commits 接口。未执行任何候选插件代码，也未把本次结果写入 SQLite。

## 结论摘要

| 来源 | 一手内容 | 采集时观察到的规模 | 关键用途 |
| --- | --- | ---: | --- |
| [量子位微信公众号文章](https://mp.weixin.qq.com/s/O6u4JsV-cFl9mKF9t5SJqw) | 文章正文、公开元数据、媒体引用 | 正文点名约 18 个插件/项目 | 发现向导和媒体叙事来源 |
| [Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins](https://github.com/Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins) | README 双语表格 | 140 个表格行，9 个分类 | 按能力分类的轻量目录 |
| [beancookie/awesome-dsh-plugin](https://github.com/beancookie/awesome-dsh-plugin) | README 双语目录、`docs/plugins.json`、静态站分类页 | 275 个插件对象，11 个分类 | 当前最适合机器导入的目录源 |
| [walkinglabs/awesome-deepseek-harness-plugins](https://github.com/walkinglabs/awesome-deepseek-harness-plugins) | README 双语目录、`docs/INCLUSION_POLICY.md` | 102 个列表条目，其中 7 个是生态目录 | 带源码级收录和静态安全初筛规则的验证型目录 |

以上规模是本次采集时的快照，不代表插件仓库当前仍可访问、兼容或安全。

## 1. 微信公众号来源

### 识别信息

- 来源 URL：[mp.weixin.qq.com/s/O6u4JsV-cFl9mKF9t5SJqw](https://mp.weixin.qq.com/s/O6u4JsV-cFl9mKF9t5SJqw)。
- 标题：`DeepSeek Harness插件一夜燃爆GitHub：长期记忆、电子宠物、4399小游戏全来了`。
- 页面显示时间：`2026年8月15日 13:30`。
- 页面署名：`梦瑶 发自 凹非寺`；公众号标识为 `量子位 | 公众号 QbitAI`；公开 meta author 为 `关注前沿科技`。
- 页面摘要：`真把Harness玩成了赛博改装车了`。
- 公开封面：[og:image](https://mmbiz.qpic.cn/mmbiz_jpg/A6fTew8FFGGwFLbk37eok7XWVPo1QCM2U27jkZjibpocbBibbJrWDbeic6mgDwvtnxJRx2owuVWShpltrl3SWVOITic8j9WcuiceEqZtiaWQSMRCo/0?wx_fmt=jpeg)。正文还引用了 `mmbiz.qpic.cn` 和 `res.wx.qq.com` 的多张图片；本次未镜像受版权约束的媒体。

### 正文点名的插件/项目

以下名称均来自文章正文原文；文章中的多数名称不是可点击链接，因此不能仅凭文章 DOM 推断其 GitHub canonical URL。

- Agent 与工作流：`dsh-agent-teams`、`DSH Better Sidebar`。
- 输入、记忆与迁移：`dsh-at-file`、`dsh-memory-evolve`、`dsh-plugin-claude-bridge`、`dsh-claude-move`。
- 视觉与效率：`ModLens`、`dsh-github-connector`、`context-vista`、`dsh-undo`、`dsh-record-replay`、`dsh-obsidian-export`、`dsh-share`。
- UI、娱乐与个性化：`dsh-TUI`、`dsh-web-ui`、`dsh-ads`、`dsh-minigames`、`deepseek-manners`。

文章正文还声称 GitHub 上带 `dsh-plugin` 标签的公开仓库达到 `700+`；这是文章作者的叙述，不是本次重新从 GitHub topic API 计算出的数字，应在聚合数据库中作为“媒体来源声明”而不是精确仓库计数保存。

### 文章自身的参考链接

文章末尾列出：[`github.com/topics/dsh-plugin`](https://github.com/topics/dsh-plugin)、[`Dominic789654/awesome-deepseek-harness`](https://github.com/Dominic789654/awesome-deepseek-harness)、[`github.com/omdsh-dev`](https://github.com/omdsh-dev) 和 [`Alex-Yanggg/awesome-DSH-plugin`](https://github.com/Alex-Yanggg/awesome-DSH-plugin)。文章页面没有直接链接本研究中的三个 GitHub 仓库。

### 互动与限制

- 公开页面显示 `赞`、`在看/推荐` 和 `留言` 控件，但 DOM 没有公开数值；互动字段应记为 `NULL/未披露`，不能写成 0。
- 文章是编辑精选和体验式介绍，不提供每个插件的 owner/name、提交 SHA、许可证、版本或可复现验证结果。
- 文章正文中 `DSH Better Sidebar`、`ModLens` 等名称存在品牌/简称表达；在聚合时必须回到对应项目的 GitHub primary source 做 URL、许可证和代码验证。
- 本次可读取公开页面；未登录、未提交点赞/留言，也未绕过微信访问控制。

## 2. `Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins`

### 仓库元数据

- owner/name：`Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins`。
- 默认分支：`main`。
- GitHub API description：`null`；README 自述为 `A concise, curated list of plugins and extensions for DeepSeek Harness`，并声明收录标准为 public、useful、maintained、clearly built for DSH。
- 采集时 GitHub 统计：55 stars、5 forks、1 open issue；这些数字是动态快照，不写入插件本体的可信度判断。
- 许可证：MIT；仓库 `LICENSE` 文件明确为 MIT License，版权行是 `2026 Awesome DeepSeek Harness Plugins contributors`。

### 插件条目与路径

仓库根目录只有 `LICENSE`、`README.md` 和 `README.zh-CN.md`；没有插件子目录、JSON 清单或构建脚本。条目以 README 表格行存在，`README.zh-CN.md` 是中文镜像。按英文 README 的表格标题计数如下：

| README 分类 | 条目行数 |
| --- | ---: |
| Core | 1 |
| Models & Providers | 5 |
| Tools & Skills | 19 |
| Sessions & Storage | 15 |
| Loops & Scheduling | 7 |
| Runtime & Sandboxes | 6 |
| UI & Clients | 46 |
| Integrations | 17 |
| Developer & Operations | 24 |
| **合计** | **140** |

每行包含项目名、GitHub URL、文字描述、GitHub stars badge 和 `Referenced by` 页面引用数。示例条目包括 `dsh-advisor`、`dsh-at-file`、`dsh-memory-evolve`、`dsh-agent-teams`、`dsh-vision-toolkit` 和 `dsh-plugin-check`；这些是目录中的链接声明，不等同于本仓库对目标插件源代码的审计。

### 最近提交

- 最新提交：[`25fee635723c42e52a7c2c8af0bb841b74facdf3`](https://github.com/Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins/commit/25fee635723c42e52a7c2c8af0bb841b74facdf3)，时间 `2026-08-14T16:14:42Z`，subject 为 `update`。
- 提交历史接口：[GitHub commits API](https://api.github.com/repos/Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins/commits?sha=main&per_page=5)。

### 可追溯来源

- [仓库 API](https://api.github.com/repos/Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins)
- [根目录 API](https://api.github.com/repos/Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins/contents?ref=main)
- [递归 Git tree API](https://api.github.com/repos/Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins/git/trees/main?recursive=1)
- [README.md](https://github.com/Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins/blob/main/README.md)、[README.zh-CN.md](https://github.com/Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins/blob/main/README.zh-CN.md)、[LICENSE](https://github.com/Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins/blob/main/LICENSE)

### 限制

- API description 为空；分类、描述和 stars badge 都来自 README 文档，不能视为 GitHub 对每个插件的验证。
- 没有机器可读的本地目录清单；后续导入需要解析 Markdown 表格，并保留 README commit SHA 作为 provenance。
- `Referenced by` 统计是该目录自己的引用计数，无法替代目标插件的下载量、活跃度或安全审查。

## 3. `beancookie/awesome-dsh-plugin`

### 仓库元数据

- owner/name：`beancookie/awesome-dsh-plugin`。
- 默认分支：`main`。
- GitHub API description：`Awesome DeepSeek Harness (DSH) Plugin`。
- 采集时 GitHub 统计：16 stars、7 forks、2 open issues。
- 许可证：CC0 1.0 Universal；GitHub API 的 SPDX 标识为 `CC0-1.0`，仓库 `LICENSE` 也明确为 CC0 1.0。

### 插件条目与路径

该仓库同时有 Markdown 源和静态站数据源：

- [`README.md`](https://github.com/beancookie/awesome-dsh-plugin/blob/main/README.md)：中文目录，按 11 个分类列出 275 个插件链接和描述。
- [`README.en.md`](https://github.com/beancookie/awesome-dsh-plugin/blob/main/README.en.md)：英文目录。
- [`docs/plugins.json`](https://github.com/beancookie/awesome-dsh-plugin/blob/main/docs/plugins.json)：当前最明确的机器可读清单；顶层 `count=275`，每个对象包含 `name`、`owner`、`url`、`category`、中英文 `description`、`npm`、`install` 和 `added`。
- [`data/added-dates.json`](https://github.com/beancookie/awesome-dsh-plugin/blob/main/data/added-dates.json) 和 [`data/npm-map.json`](https://github.com/beancookie/awesome-dsh-plugin/blob/main/data/npm-map.json)：站点/导入辅助数据。
- 静态站分类页位于 `docs/{ui,theme,session,memory,tools,skill,workflow,notify,model,dev,fun}/index.html`，入口为 [`docs/index.html`](https://github.com/beancookie/awesome-dsh-plugin/blob/main/docs/index.html)，英文入口为 `docs/en/index.html`。

`docs/plugins.json` 在本次采集时的分类计数为：`ui=57`、`theme=5`、`session=14`、`memory=14`、`tools=69`、`skill=3`、`workflow=20`、`notify=14`、`model=7`、`dev=52`、`fun=20`，合计 275。对象中的 `install` 字段还提供了如 `dsh plugin --profile web add github:<owner>/<repo>` 的安装建议，应作为目录声明保存，不能自动执行。

### 最近提交

- 最新提交：[`c5d444234432be070feb3d64482e296059fd4943`](https://github.com/beancookie/awesome-dsh-plugin/commit/c5d444234432be070feb3d64482e296059fd4943)，时间 `2026-08-15T05:13:20Z`，subject 为 `Update canonical site URL in JSON-LD to GitHub Pages`。
- 最近历史还包括移动端布局修复、分类/计数工作流文档和搜索过滤修复；提交列表见 [GitHub commits API](https://api.github.com/repos/beancookie/awesome-dsh-plugin/commits?sha=main&per_page=5)。

### 可追溯来源

- [仓库 API](https://api.github.com/repos/beancookie/awesome-dsh-plugin)
- [根目录 API](https://api.github.com/repos/beancookie/awesome-dsh-plugin/contents?ref=main)
- [递归 Git tree API](https://api.github.com/repos/beancookie/awesome-dsh-plugin/git/trees/main?recursive=1)
- [README.md](https://github.com/beancookie/awesome-dsh-plugin/blob/main/README.md)、[README.en.md](https://github.com/beancookie/awesome-dsh-plugin/blob/main/README.en.md)、[plugins.json](https://github.com/beancookie/awesome-dsh-plugin/blob/main/docs/plugins.json)、[LICENSE](https://github.com/beancookie/awesome-dsh-plugin/blob/main/LICENSE)

### 限制

- `plugins.json` 是目录维护者提供的清单，不是 GitHub 官方插件注册表；`npm`、安装命令、`added` 日期都需要到目标仓库二次核验。
- 分类页是构建产物，可能与 README 或 JSON 在提交之间短暂不同；聚合时优先保存 JSON 文件的 commit SHA，再记录 README/站点 URL。
- CC0 只描述该目录仓库自身的权利放弃，不自动授予被列出插件、logo、截图或视频的使用权。

## 4. `walkinglabs/awesome-deepseek-harness-plugins`

### 仓库元数据

- owner/name：`walkinglabs/awesome-deepseek-harness-plugins`。
- 默认分支：`main`。
- GitHub API description：`A curated, bilingual list of verified plugins, tools, design workflows, and learning resources for DeepSeek Harness (DSH).`
- 采集时 GitHub 统计：4 stars、5 forks、6 open issues。
- 许可证：仓库 `LICENSE` 明文为 CC0 1.0 Universal；GitHub API 显示 `Other` / `NOASSERTION`，说明 GitHub 未把文件映射为 SPDX 标识。两者都保留，不能只写成“无许可证”。

### 插件条目与路径

仓库根目录没有 JSON 插件清单；条目主要在 [`README.md`](https://github.com/walkinglabs/awesome-deepseek-harness-plugins/blob/main/README.md)，中文镜像为 [`README.zh.md`](https://github.com/walkinglabs/awesome-deepseek-harness-plugins/blob/main/README.zh.md)。README 还包含安装教程、架构/工具调用/会话日志说明和收录政策链接。

按 README 的分类标题统计，列表共有 102 条 bullet：

| README 分类 | 条目数 | 说明 |
| --- | ---: | --- |
| Productivity & Agent Workflow | 14 | 插件与工作流 |
| Context, Memory & Observability | 12 | 记忆、上下文、观测 |
| Tools, Integrations & Automation | 8 | 工具与集成 |
| Design & Creative Tools | 7 | 设计/视觉/媒体 |
| Browser, Computer Use & Remote Execution | 4 | 浏览器和电脑控制 |
| Interfaces & Web UI | 17 | Web/TUI/UI |
| Developer Tooling | 7 | 开发与审计工具 |
| Utilities | 11 | 工具包 |
| Creative & Personal | 8 | 个性化插件 |
| Games & Play | 1 | 游戏 |
| Launchers & Clients | 6 | 启动器/客户端 |
| Ecosystem Indexes | 7 | 其他目录源，不应计作插件 |
| **合计** | **102** | 其中前 11 类合计 95 条 |

目录中可直接追溯到 GitHub 的代表条目包括 `dsh-worktree`、`dsh-memory-evolve`、`dsh-custom-tool`、`dsh-openpencil`、`dsh-vision-toolkit`、`dsh-minigames`、`dsh-launcher` 和多个生态目录。真正导入时应按 URL 去重，并保留其所属分类与“插件/客户端/生态目录”类型。

收录规则位于 [`docs/INCLUSION_POLICY.md`](https://github.com/walkinglabs/awesome-deepseek-harness-plugins/blob/main/docs/INCLUSION_POLICY.md)，要求候选提供 DSH manifest、DSH/Cordis 扩展接缝、官方 DSH 资源或可检查的客户端/开发集成；同时要求静态安全初筛，明确“不执行候选代码或其安装/构建脚本”。

### 最近提交

- 最新提交：[`11f90e9b9b97eba6660c56d520c40ef9a59fb511`](https://github.com/walkinglabs/awesome-deepseek-harness-plugins/commit/11f90e9b9b97eba6660c56d520c40ef9a59fb511)，时间 `2026-08-15T07:09:52Z`，subject 为 `docs: add verification and telemetry plugins`。
- 提交列表见 [GitHub commits API](https://api.github.com/repos/walkinglabs/awesome-deepseek-harness-plugins/commits?sha=main&per_page=5)；最近历史还显示过“Revert manual integration of PR 3”和验证/遥测条目变更，说明目录在快速调整中。

### 可追溯来源

- [仓库 API](https://api.github.com/repos/walkinglabs/awesome-deepseek-harness-plugins)
- [根目录 API](https://api.github.com/repos/walkinglabs/awesome-deepseek-harness-plugins/contents?ref=main)
- [递归 Git tree API](https://api.github.com/repos/walkinglabs/awesome-deepseek-harness-plugins/git/trees/main?recursive=1)
- [README.md](https://github.com/walkinglabs/awesome-deepseek-harness-plugins/blob/main/README.md)、[README.zh.md](https://github.com/walkinglabs/awesome-deepseek-harness-plugins/blob/main/README.zh.md)、[INCLUSION_POLICY.md](https://github.com/walkinglabs/awesome-deepseek-harness-plugins/blob/main/docs/INCLUSION_POLICY.md)、[LICENSE](https://github.com/walkinglabs/awesome-deepseek-harness-plugins/blob/main/LICENSE)

### 限制

- README 是主要数据源，没有与其配套的机器可读 plugin manifest；需要解析 Markdown 链接并回查目标仓库。
- 102 条 bullet 混合插件、客户端、启动器、开发资源和生态目录；不能把总数直接称为“102 个插件”。
- “verified”是该目录依据自身政策做的收录标签，不是官方 DeepSeek 背书，也不是完整恶意代码审计、兼容性认证或可靠性认证。
- 快速提交和 revert 可能使同一 URL 在不同时间出现/消失；聚合数据库必须保存观察时间、源文件 URL 和 commit SHA。

## 5. 对聚合数据库的直接使用建议

1. 把四个来源作为 `source` 级记录：公众号用文章 URL，三个目录用仓库 URL；所有条目保留 `source_path`（例如 `README.md#tools--skills` 或 `docs/plugins.json`）和采集时间。
2. 对 GitHub 目录条目提取 `owner/name`、canonical URL、目录分类、目录原文描述、目录来源 commit SHA；再对目标插件仓库单独采集默认分支、许可证、最近提交、stars/forks 和 manifest 路径。
3. 将 `beancookie` 的 `docs/plugins.json` 作为结构化候选入口，将 `Zhiyuan-Fan` 和 `walkinglabs` 的 README 作为补充发现源；同一插件跨目录出现时按 canonical URL 合并，不把目录间的 stars 或“verified”相加。
4. 将公众号的 `700+` 和互动状态保存为媒体/文章 observation：`claim_type=editorial_statement`、`metric_value=NULL`，并链接到原文；不要把它转换成未经 API 复核的仓库总数。
5. 许可证只约束目录仓库本身；插件代码、文章图片、截图、视频和 logo 继续沿用各自上游权利信息。
