# deeplugin.store 增量增长机制：从目录到可复用增长网络

访问日期：2026-08-16

## 一句话结论

当前最值得先做的不是继续扩充首页文案，而是上线“任务型插件包”：让一个可分享 URL 把用户意图转换为一组精确 Registry ID 的可审查安装计划；随后再用匿名安装回执、作者归属页和更新发布管线形成可测量的循环。[S1][S2][S4][S14]

## 研究边界与当前基线

本文件是对 `docs/research/plugin-store-growth-loops-2026-08-16.md` 的增量研究，不重复已经实现的稳定插件详情页、canonical、Open Graph 基础标签和 README 徽章。外部证据只采用产品官方文档、官方产品页和官方源码仓库；没有采用二手营销博客。

仓库现状以提交 `b65aae68bc8a0823b36b81b8ded42e90161dce92` 为基线。对生成物和生成器的只读核对得到：

- 已有 1,116 个 `docs/plugins/deeplugin-*.html` 稳定详情页和可复制的单插件 Agent 请求。
- 1,116 个插件详情页的 `og:image` 全部指向同一张 `media/screenshots/official.png`，还没有逐插件或逐更新的分享视觉。
- Registry 中有 704 个不同的 `author` 字符串，但没有 `authors/` 或 `publishers/` 路由；作者目前不能把多个插件汇聚到自己的 Store 落地页。
- 没有插件包/合集路由，没有 RSS、Atom 或 JSON Feed 路由，也没有成功安装遥测或聚合安装量。
- Store 搜索已索引名称、作者、精确 spec、描述、tags 和来源，但没有单独保存来源声明的 command title、subtitle、keywords 及其 raw provenance。

以上缺口决定了本轮只研究五个尚未落地、可由现有 SQLite 与静态生成管线承接的机制。

## 建议排序

| 排名 | 机制 | 为什么现在做 | 自动化程度 | 主要依赖 |
| --- | --- | --- | --- | --- |
| 1 | 任务型、可审查的 Plugin Packs | 直接缩短“我想做什么”到“Agent 展示一组安装计划”的路径；静态站即可上线 | 高 | Registry ID、Market Plugin 计划/确认 |
| 2 | 来源可追溯的意图索引 | 让首页问题式搜索真正命中 command/capability，而不只匹配包名和描述 | 高 | package/manifest raw、搜索索引 |
| 3 | 每次实质更新的分发对象 | 一次生成独立视觉、Feed 条目、GitHub Discussion 与渠道草稿，减少重复运营 | 高；外部发布保留审批 | 版本差异、媒体权利、发布阈值 |
| 4 | 作者归属页与来源证明的 claim 流程 | 把作者的多个插件、徽章和更新汇到同一可反向链接页面 | 高 | GitHub/npm 可解析身份、raw 证明 |
| 5 | 自愿匿名的成功安装回执 | 产生目录自身的真实需求信号，支持趋势和后续选题 | 中 | 非静态接收端、隐私与反作弊治理 |

## 机制 1：任务型、可审查的 Plugin Packs

### 一手证据

- skills.sh 官方把 Pack 定义为“用一个安装命令分享一组 skills”，Pack 可以混合多个公开来源；更新后，新安装自动取当前内容，已有安装可用更新命令只拉取变化项。[S2]
- VS Code 的 `extensionPack` 允许一个扩展列出多个完整 extension ID；官方给出的用途包括把收藏分享给朋友、按语言/任务组合工具，以及为专题文章建立合集。[S4]
- Vercel Deploy Button 把一个分享入口连接到 clone、项目创建和可配置的后续流程；官方同时允许用 Demo Card 展示完成后的结果。[S14]

这些产品的共同点不是“批量安装”本身，而是把多个稳定对象压缩成一个可传播入口，并保留对象列表和后续更新语义。

### 对本仓库的实现建议

1. 新增版本化 Pack 数据，而不是把 Pack 写死在首页 HTML。每个 Pack 至少保存 `pack_id`、`slug`、中英文名称/任务描述、成员 `deeplugin_id`、成员加入原因、`dataset_version`、`first_seen_at`、`last_updated_at` 和维护者。
2. 首批只生成 6–10 个有明确任务边界的 Pack，例如“联网研究”“会话记忆”“移动端 UI”“插件开发工具链”；每个 Pack 保持 2–6 个成员，并说明成员是否替代、互补或需要二选一。
3. Pack 页面只复制一条 review-first Agent 请求。Market Plugin 必须逐个解析 Registry ID、展示精确 spec、来源、版本缺失、重复项和潜在冲突；用户确认前不执行，确认粒度至少到每个成员。
4. Pack URL、成员列表和 `dataset_version` 进入 sitemap、JSON-LD、SQLite 和机器可读 JSON。分享 URL 永远指向稳定 `pack_id`，当前成员集合由版本字段解释。
5. 首页 hero 下只展示 3 个任务 Pack，并以“查看计划”而不是“安装全部”作为 CTA；详情页提供“加入自定义 Pack”的纯客户端分享链接，先不做账号系统。

### 验收信号

- `pack_view -> copy_pack_request -> plan_shown -> member_confirmed` 四阶段可区分；网页复制不能记成安装。
- 一个 Pack 在重复构建时成员顺序、URL 和版本完全确定；失效成员让构建失败或把 Pack 标为不可安装，不能静默删除。
- 任何 Pack 都能从成员回溯到 Listing、raw snapshot 和观察日期。

### 风险与停止线

- “同一任务”不等于“互相兼容”。页面必须写成 curated collection，不得声称经过兼容、安全或质量认证。
- Pack 会放大错误 spec 的影响；任一成员无法解析、来源失活或安装计划与页面不一致时，整包停止公开 CTA。
- 不复制 skills.sh 的 unlisted 隐私表述：skills.sh 明确提醒 unlisted URL 不是访问控制；本仓库若未来允许私有 Pack，必须使用真正鉴权，不能靠难猜 URL。[S2]

## 机制 2：来源可追溯的意图索引

### 一手证据

- Raycast manifest 允许给 command 声明 `title`、`subtitle`、`description` 和搜索 `keywords`；官方说明 subtitle 也被索引，command title 应直接表达用户动作。[S6][S7]
- npm 官方说明 `description` 和 `keywords` 会帮助包在 `npm search` 中被发现；`npm search` 还能用 `=maintainer` 精确过滤维护者。[S9][S10]
- VS Code Marketplace 按 title 或 metadata 搜索，并以 `publisher.extension` 作为唯一扩展 ID。[S5]
- Chrome 的 listing 指南要求先用简洁陈述解释产品作用，并允许按 locale 提供描述、截图和视频；关键词堆砌会损害体验并可能触发政策问题。[S12]

目录首页的高转化搜索因此不是“更智能地猜”，而是先把作者已经声明的动作、关键词和语言字段变成结构化检索事实。

### 对本仓库的实现建议

1. 在 SQLite 增加可追溯的搜索词投影：`plugin_id`、`term`、`term_kind`、`locale`、`source_url`、`raw_snapshot_id`、`observed_at`。`term_kind` 限定为 `name`、`command_title`、`command_subtitle`、`keyword`、`category`、`maintainer` 和小规模人工维护的 `intent_alias`。
2. 优先从已保存的 package/manifest raw 中提取 DSH command 标题、描述、npm keywords 和仓库内结构化 metadata；不能从仓库名自动编造能力词。
3. 首页搜索提供 6–8 个可复算的任务 chips。初期由有足够候选的 command/category 频次生成；有安装回执后再用匿名聚合需求排序，但不让查询次数直接改变质量排序。
4. 中英转换只使用版本化小词典，并把机器生成和来源原文分开。每个搜索命中可解释“命中 command title / keyword / category”，方便发现垃圾 metadata。
5. 零结果查询只在用户明确同意分析时保存聚合短语；不保存完整会话、IP、用户标识或随后安装历史。

### 验收信号

- 用 30–50 个真实任务问句建立固定回归集，记录 top-5 命中率和零结果率；每条期望结果说明对应来源字段。
- 搜索索引可从 SQLite/raw 完整重建，重复词、大小写和 locale 归一化结果确定。
- 首页任务 chips 至少有 3 个真实候选，且点击后产生可复制、可分享、带 canonical 的查询 URL。

### 风险与停止线

- 作者 metadata 可能包含 keyword spam。每个字段设上限，重复词不加权，异常关键词只保留 raw、不进入公开索引。
- 自动翻译可能扩大错误语义。没有可靠来源或人工词典时保留原文，不为了中英文覆盖编造同义词。
- 搜索成功率不能替代安装成功率；如果 query CTR 上升而 `plan_shown` 不升，应回退词表或结果模板。

## 机制 3：每次实质更新生成一个可分发对象

### 一手证据

- Raycast 要求 Store listing 提供高质量 icon、screenshots 和可选 changelog；官方建议至少三张截图，并在扩展发布后提供复制链接，再分享到 X、Slack 社区或团队。[S7][S8]
- Chrome listing 支持最多五张截图、YouTube 演示视频，以及按 locale 提供描述、截图和视频。[S12]
- Vercel Marketplace 的官方检查表要求高质量 gallery images，并明确第一张图会用于自动生成 Open Graph image。[S13]
- PyPI 官方把更新订阅拆成 Newest Packages、Latest Updates 和单项目 Releases 三种 RSS，而不是把所有变化塞进一个流。[S15]
- GitHub Discussions GraphQL API 可以创建、更新和删除 discussion；Discussion 本身适合分享更新和开放讨论。[S16]
- X API 支持代表已授权用户创建带文本和媒体的 Post，但需要用户授权。[S18]
- Show HN 只接受别人能够直接试用、发布者本人愿意在场讨论的实质作品；普通版本小更新、列表、落地页和拉票不适合 Show HN。[S17]

### 对本仓库的实现建议

把“一个实质更新”物化为一个版本化 distribution object，而不是在两小时采集任务里直接发帖。对象至少包括：

- canonical 插件/Pack URL、Registry ID、来源、版本、变更观察时间和 `dataset_version`；
- 中英文一句话、三条事实差异和一个 review-first CTA；
- 一张逐插件独立的 1200×630 分享图：优先使用权利允许的来源媒体；没有媒体时从名称、类别、来源和观察日期生成确定性文字卡；
- `new`、`updated` 和 per-plugin Atom/JSON Feed entry；
- GitHub Discussion 正文、X 草稿和普通 HN 标题草稿，全部引用同一事实对象和 campaign；
- `material_change` 判定，例如首次公开、声明版本变化、成员变化或新增权利允许的演示媒体。stars/likes/views 的普通波动不触发外发。

自动化边界：Feed 和站内页面可自动发布；GitHub Discussion 只按周或明确 release 阈值创建；X 默认只生成待批准草稿；Show HN 永不自动提交，只在可直接试用的重大 Store/Market Plugin 版本上由维护者手工发布并现场回复。

### 验收信号

- 1,116 个插件不再共用一张 `og:image`；每张生成卡的输入、locale 和媒体权利来源可追溯。
- 同一 distribution object 在 Feed、Discussion 和渠道草稿中的 Registry ID、URL、版本与日期一致。
- 两小时采集没有实质变化时不产生新的 Feed entry、Discussion 或渠道草稿。

### 风险与停止线

- 外部图片可能有版权、热链和失效风险；未记录权利许可时只能链接来源或生成文字卡，不能镜像素材。
- 自动发帖容易触发平台风控和社区反感。任何渠道投诉、moderation 删除或事实不一致都应暂停该渠道自动化。
- 更新卡不能把来源的 `verified` 声明升级成本站安全背书，也不能把旧截图表现成当前版本。

## 机制 4：作者归属页与来源证明的 claim 流程

### 一手证据

- Chrome Web Store 的 publisher 可以拥有多个 items，并通过成员角色分别管理 metadata、package、分发、analytics 和 publisher 设置。[S11]
- VS Code Marketplace 用 publisher 与 extension ID 组成唯一标识，并在详情中显示 publisher；publisher verification 还有独立、明确的域名与历史要求。[S5]
- Raycast 要求 manifest 的 author 使用 Raycast 账号 username，也允许列出实际维护贡献者；所有更新通过 PR 进入公开仓库。[S6][S8]
- npm 的 package metadata 支持 author/maintainer 信息，`npm search` 支持按 maintainer 精确查找。[S9][S10]

共同模式是“作者/发布者是目录中的一等聚合对象”，但不同平台的身份验证含义并不等价。

### 对本仓库的实现建议

1. 只为可解析的来源身份生成稳定 publisher hub，例如 GitHub owner、npm scope/maintainer；普通 `author` 文本先作为 attributed label，不自动合并同名字符串。
2. 页面展示该来源身份下的插件、版本/观察日期、来源仓库、公开支持链接、Pack 出现位置、Feed 和可复制的 publisher badge。至少两个插件或完成 claim 的身份才生成可索引页面，避免 700 多个薄页。
3. claim 不依赖本站账号：作者在来源仓库加入最小 `deeplugin-store.json` 或 README 链接，collector 保存 commit URL、raw snapshot、SHA 和观察日期；页面只标记“claimed via source commit”，不写 `verified publisher`。
4. claim 成功后自动返回 launch packet：publisher hub、所有插件稳定链接、单插件/作者 badge、缺失媒体和 metadata 清单。反向链接完全自愿，不影响收录和排序。
5. 团队项目允许多个来源账号，但展示角色必须来自 source-declared metadata；成员离开或证明文件删除时保留历史 raw，并把当前 claim 标为 inactive。

### 验收信号

- 每个 hub 的成员插件都能由 GitHub owner、npm scope/ownership 或 raw claim 证明，不能靠大小写相似名称合并。
- canonical、sitemap 和内部链接稳定；同一 identity 的新插件在下一次成功采集后自动进入 hub。
- claim 状态包含方法、source URL、commit/SHA、首次/最近观察日期和 dataset version。

### 风险与停止线

- `author` 是来源字段，不天然代表法律身份、维护权限或安全信誉；页面必须明确证明类型。
- GitHub 组织、个人、npm maintainer 和品牌名可能不一致。不能建立跨平台统一身份，除非来源仓库主动声明关联。
- 删除证明不应抹去历史，但必须停止显示当前 claim；不能因网络失败把 claim 误判为撤销。

## 机制 5：自愿匿名的成功安装回执

### 一手证据

- skills.sh 官方说明 leaderboard 基于 skills CLI 的匿名安装遥测；只跟踪安装了哪些 skills，不收集个人信息或使用模式。[S1]
- Vercel 的官方 Agent Skills 指南说明，skill 通过 `npx skills add` 被安装后可以自动出现在 skills.sh，无需单独 registry submission。[S3]
- skills.sh 同时把安装量用于 leaderboard，并提供带安装数的作者 badge，形成“安装 → 排名/徽章 → 新发现”的闭环。[S1]

这比 GitHub stars 更接近 Store 内真实需求，但 deeplugin.store 必须把遥测定义得更窄：只报告 Market Plugin 已确认且成功的安装，不报告复制、查看或 Agent 计划。

### 对本仓库的实现建议

1. Market Plugin 首次使用时明确询问是否发送匿名成功回执，默认可拒绝且之后可关闭。事件只包含 `deeplugin_id`、安装 spec 的 SHA-256、声明版本、结果、Market Plugin 版本、UTC 日桶和 dataset version。
2. 不发送 prompt、profile 名、工作区路径、用户名、机器 ID、IP 哈希、失败日志正文或跨事件持久标识。接收端关闭原始访问日志或设置极短保留，并公开数据字典和删除周期。
3. 公共仓库只保存按日/周聚合的 `confirmed_installs_via_market_plugin`，附窗口、生成时间、接收端版本和样本限制；不把它命名为总下载量。
4. Trending 只比较同一事件定义的相邻窗口，设置最小样本和冷却期；GitHub stars、平台 likes/views 与安装回执继续分栏，不合成总分。
5. 聚合变化可以触发机制 2 的 homepage intent chips 和机制 3 的周报选题，但不得自动把未知 spec 变成公开可安装 Listing。

### 验收信号

- `copy_request`、`plan_shown`、`install_confirmed` 和 `install_succeeded` 不混用；只有最后一项进入公开安装聚合。
- 关闭遥测后没有网络请求；离线、重试和重复执行使用本地 event id 去重，但 event id 不上传为长期用户标识。
- 公布丢失率、采样范围和“仅覆盖同意遥测的 Market Plugin 安装”限制。

### 风险与停止线

- 这需要静态 GitHub Pages 之外的接收端，是五项中治理成本最高的一项。隐私政策、同意流程和日志配置未完成前不能上线。
- 匿名事件容易被刷；只能把聚合安装量当需求信号，不能当质量、安全或真实用户数。异常突增应隔离，不直接改变首页。
- 遥测样本有明显选择偏差。不同版本、渠道和是否同意遥测的用户不能被推断为同一总体。

## 90 天落地顺序

| 时间 | 交付 | 通过标准 |
| --- | --- | --- |
| 第 1–14 天 | 3 个静态 Pack + provenance-aware 搜索词表 + 固定查询回归集 | Pack 成员全可回溯；Agent 展示逐项计划；30–50 条任务查询有可解释 top-5 |
| 第 15–30 天 | 逐插件确定性 OG 卡 + `new`/`updated` Feed + distribution object JSON | 不再共用一张 OG 图；无实质变化不发 entry；所有渠道事实一致 |
| 第 31–60 天 | publisher hub + 来源仓库 claim pilot | 先邀请 20 位多插件作者；无错误合并；claim 证明可回溯 raw/commit |
| 第 61–90 天 | opt-in 安装回执小流量试点 | 同意/关闭可验证；无 PII；重复率和丢失率可量化；榜单明确样本边界 |

最早的增长验证应比较单插件入口和 Pack 入口的 `plan_shown / qualified_view`，而不是只看 pageview。若 Pack 有点击但没有计划展示，先修成员选择和 Agent 请求；不要用更多外部发帖掩盖产品转化问题。

## 社区分发规则

- GitHub Discussions：只发布可复算的周 digest 或实质 release，使用 GraphQL API 创建，正文链接到 distribution object；修订时更新同一 discussion，不重复开帖。[S16]
- X：生成带唯一视觉和 canonical 的中英文草稿；只有账号授权并经人审后调用 Create Post API，不把两小时采集节奏变成发帖节奏。[S18]
- Hacker News：普通数据更新走普通 submission；只有用户能直接试用的重大 Store/Market Plugin 版本才考虑 Show HN，并由实际维护者发布、在场回答，不请求点赞。[S17]
- 作者渠道：claim/提交完成后自动生成作者自己的插件页、Pack 位置、badge 和短文案；是否发布完全由作者决定。

## 一手来源

以下来源均于 2026-08-16 直接访问并返回可读官方页面。

| 编号 | 官方来源 | URL | 用于证明 |
| --- | --- | --- | --- |
| S1 | skills.sh Documentation | https://www.skills.sh/docs | 匿名安装遥测、leaderboard、安装数 badge |
| S2 | skills.sh Packs | https://www.skills.sh/docs/packs | 多来源 Pack、单命令分享、更新与 unlisted 限制 |
| S3 | Vercel：Agent Skills 指南 | https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context | 安装遥测可让 skill 自动进入目录、无需单独提交 |
| S4 | VS Code Extension Manifest | https://code.visualstudio.com/api/references/extension-manifest | `extensionPack`、稳定 extension ID 与 metadata 字段 |
| S5 | VS Code Extension Marketplace | https://code.visualstudio.com/docs/configure/extensions/extension-marketplace | publisher.extension 唯一标识、metadata 搜索、详情与 CLI 安装 |
| S6 | Raycast Manifest | https://developers.raycast.com/information/manifest | author/contributors、command title/subtitle/keywords |
| S7 | Raycast：Prepare an Extension for Store | https://developers.raycast.com/basics/prepare-an-extension-for-store | 搜索命名、categories、screenshots、changelog |
| S8 | Raycast：Publish an Extension | https://developers.raycast.com/basics/publish-an-extension | PR 自动发布、复制链接、X/Slack/团队分享 |
| S9 | npm package.json | https://docs.npmjs.com/cli/v11/configuring-npm/package-json | description、keywords、author/homepage 等发现字段 |
| S10 | npm search | https://docs.npmjs.com/cli/v11/commands/npm-search | metadata 搜索与 maintainer 过滤 |
| S11 | Chrome Web Store：Share ownership | https://developer.chrome.com/docs/webstore/share-ownership | publisher 多 item、成员角色和 analytics 权限 |
| S12 | Chrome Web Store：Complete your listing information | https://developer.chrome.com/docs/webstore/cws-dashboard-listing | category、locale、screenshots、视频与 listing 内容 |
| S13 | Vercel Integration Approval Checklist | https://vercel.com/docs/integrations/create-integration/approval-checklist | gallery 质量、第一张图用于 OG、文档与分类检查 |
| S14 | Vercel Deploy Button | https://vercel.com/docs/deploy-button | 单入口 clone/deploy 流程与完成后的 Demo Card |
| S15 | PyPI RSS Feeds | https://docs.pypi.org/api/feeds | newest、latest updates、per-project releases 三类 feed |
| S16 | GitHub Discussions GraphQL API | https://docs.github.com/en/graphql/guides/using-the-graphql-api-for-discussions | Discussion 的创建、更新、读取和删除自动化 |
| S17 | Hacker News Show HN Guidelines | https://news.ycombinator.com/showhn.html | 可试用、在场讨论、禁止普通小更新与拉票 |
| S18 | X Create or Edit Post API | https://docs.x.com/x-api/posts/create-post | 经授权创建文字/媒体 Post 的官方接口 |

## 最强建议

先实现 3 个 review-first Packs，而不是先接社交账号或遥测服务。它复用现有 Registry ID、稳定详情页和 Market Plugin，不需要新账号系统或动态后端，却能同时产生首页任务入口、可分享链接、作者分发素材和可测量的 `plan_shown` 转化；这是当前成本最低、离真实安装最近的新增增长循环。[S2][S4][S14]
