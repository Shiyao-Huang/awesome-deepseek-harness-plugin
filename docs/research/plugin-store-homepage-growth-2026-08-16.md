# Plugin Store 首页与增长调研

访问日期：2026-08-16

## 结论

`deeplugin.store` 的首屏不应继续解释“这是一个聚合 Store”。最强的首页结构是：一句任务导向标题、一个意图搜索框、一个带 `自己安装 / 交给 DeepSeek` 双标签的 Market Plugin 安装区，然后立即进入榜单和分类。`skills.sh` 已经在单个 skill 详情页同时提供 `Command` 与 `Prompt`，SkillsMP 则把 review-first prompt 作为默认安装路径；这不是概念提案，而是已经上线的 AI skill 目录转化模式。[S1][S2][S3][S4]

增长不应等同于每两小时自动发一条推广。两小时采集服务数据新鲜度；对外分发应把同一批真实数据加工成各平台原生内容，并遵守各平台规则：GitHub 承载源码、Release 与可信来源，X 发布短演示和更新，小红书发布无站外导流的真实教程，微信公众号发布完整长文，HN 只在产品可直接试用且团队能在线回答时做一次 Show HN。[S12][S13][S14][S15][S16][S17][S18][S19][S20]

## 竞品模式

| 产品 | 首页发现方式 | 详情页转化 | 对 deeplugin.store 的直接启示 |
| --- | --- | --- | --- |
| skills.sh | 搜索置顶；`All Time / Trending (24h) / Hot` 榜单；行内显示安装量与仓库 | `Command / Prompt` 双标签、可复制；同时展示摘要、原始 `SKILL.md`、相关 skill、安装量、GitHub stars、首次发现时间和安全审计 | 把“双安装路径”做成同一安装组件，不写第二段解释文字；榜单直接服务选择 [S1][S2] |
| SkillsMP | 用任务、创作者、职业和分类探索；首页先给搜索和 popular picks | 默认 review-first prompt，可切换直接命令或本地下载；先展示仓库、最近活动、stars/forks，再要求检查 `SKILL.md` 和伴随文件 | 把“来源可追溯”放在安装动作旁，而不是放在长篇品牌宣言里 [S3][S4] |
| npm | 搜索读取 title、description、README 和 keywords；支持按匹配、下载量、依赖者和最近发布时间排序 | 安装标识就是 package name；官方文档给出 `npm install <package_name>` 与 scoped package 的精确形式 | 搜索字段和排序逻辑要公开；插件身份必须是可复制的精确 spec，不是模糊仓库名 [S5][S6] |
| VS Code Marketplace | 编辑器内搜索；列表显示简述、publisher、下载量和评分；支持按安装量、评分、名称、发布日期和更新时间排序 | 详情首区有 `Install`、复制 Quick Open 命令、安装量、评分、价格和简介；第三方 publisher 首次安装会要求信任确认；CLI 使用完整 `publisher.extension` id | 详情页的第一动作是安装，身份、信任和版本选择紧贴动作；确认不是阻力，而是产品可信度的一部分 [S7][S8] |
| GitHub Marketplace | 首页短描述和分类负责扫描，详情页负责深入说明 | 官方建议首页短描述保持 40-80 字符；详情用 1-2 句简介、3-5 个价值点和最多 5 张同尺寸高分辨率产品截图；Insights 分开统计 landing、checkout 和 subscription 转化 | 首页文字必须短；案例图应展示真实 UI；漏斗事件要分开记录，而不是只看页面访问量 [S9][S11] |

GitHub Marketplace 不能被当成任何开源目录都能提交的分发渠道。其 app listing 要求产品与 GitHub 平台有超出登录的集成、公开可用、具备有效支持与链接，并满足 Marketplace app 的技术和品牌要求；只有当 deeplugin.store 另行成为合格的 GitHub App 或 GitHub Action 时才应申请 listing。[S10]

## 1. 首页信息架构与首屏 CTA

推荐首屏只有以下层次：

```text
DeepSeek Harness Plugin Store                         中文 / EN

搜索插件，复制命令，或交给 DeepSeek 安装。
[ 你想让 DeepSeek 做什么？                         ] [搜索]

安装 Market Plugin
[自己安装] [交给 DeepSeek]
[ dsh plugin --profile web add github:...#path:/plugin ] [复制]

热门 · 趋势 · 最新                         [浏览全部插件]
```

中英文首屏文案应使用同一信息层级：

| 元素 | 中文 | English |
| --- | --- | --- |
| H1 | `DeepSeek Harness Plugin Store` | `DeepSeek Harness Plugin Store` |
| 副标题 | `搜索插件，复制命令，或交给 DeepSeek 安装。` | `Find a plugin, copy the command, or hand it to DeepSeek.` |
| 搜索占位 | `你想让 DeepSeek 做什么？` | `What should DeepSeek do?` |
| 安装标签 | `自己安装` / `交给 DeepSeek` | `Install yourself` / `Ask DeepSeek` |
| 次要入口 | `浏览全部插件` | `Browse all plugins` |

删除首屏中“我们把市面上公开可安装的插件聚合到一个 Store”与“这是 DeepSeek Harness 的 Plugin Store”这类重复定义。来源、版本和精确安装标识仍然重要，但应变成安装区下的一行信任信息与详情页字段；GitHub 的 listing 指南同样要求首页短描述只说功能，不重复产品名，也不把短描述写成 CTA。[S9]

首屏以下按转化顺序排列：`热门/趋势/最新` 三段榜单、六至八个任务分类、四幕 QA 案例、最近新增、数据与来源说明。完整时间轴、Sources、Directories、Forks 和方法论保留在导航或页尾，不与首屏主任务竞争。skills.sh 的时间维度榜单、SkillsMP 的职业/创作者探索、npm 与 VS Code 的多排序证明：搜索解决“我知道要什么”，分类解决“我只知道任务”，榜单解决“我不知道先看什么”。[S1][S3][S5][S7]

## 2. 搜索、分类、榜单与详情页转化

### 搜索

- 默认搜索自然语言任务，同时匹配名称、中英文描述、tags、category、author、精确 install spec 和 Registry Source；高级搜索再开放稳定 id 与 exact spec。npm 公开其 title、description、README、keywords 匹配字段，VS Code 支持按 metadata 搜索和 `@id:` 精确查找，这种可解释性可以降低“为什么搜到它”的疑虑。[S5][S7]
- 每个结果显示“命中的能力词”，不要只给一个不可解释的总分。默认排序为任务覆盖度，其后才是来源声明、活跃度和 stars；不要把不同平台的 likes、stars、views 相加成一个伪精确热度。
- 无结果页直接提供三个动作：换一个任务描述、浏览相邻分类、提交插件。不要用品牌介绍填充空状态。

### 分类与榜单

- 一级分类使用用户任务，而不是内部 package group，例如：`搜索与研究`、`编码与代码审查`、`数据与文档`、`浏览器与自动化`、`多 Agent 与工作流`、`模型与 Provider`。
- 榜单只保留三个用户可理解的维度：`热门`（稳定累计信号）、`趋势`（明确时间窗内变化）、`最新`（首次收录时间）。每个标题旁公开计算口径和时间窗。skills.sh 将 all-time、24h trending、hot 分开，npm 和 VS Code 也把匹配、下载量、依赖数、评分、发布/更新时间作为不同排序，不混成一个无法解释的分数。[S1][S5][S7]
- 榜单卡片只显示名称、一句话能力、来源、版本/更新时间、一个原生指标和安装入口。详情页承担完整证据，不在卡片中堆字段。

### 详情页

详情页首屏按以下顺序固定：名称与一句话能力、作者/来源、稳定 id、精确 install spec、声明版本与观测日期、`自己安装 / 交给 DeepSeek`、确认提示。第二屏再放功能说明、真实截图/视频、Registry Source 归属、README/仓库、版本历史、原生指标、相关插件和安全说明。VS Code 将 publisher、安装量、评分、价格、Install 与 Quick Open 命令放在同一首区；skills.sh 在安装区之后再展开内容和相关项；SkillsMP 在安装前强调仓库与文件审查。[S2][S4][S7][S8]

`verified=true` 必须继续显示为“来源 Registry 的有限声明”，不能渲染成 deeplugin.store 的安全背书。安装前显示来源、精确 spec、目标 profile 和将执行的命令；安装、更新和删除都等待 DSH 确认。这个行为已经由本仓库的 Market Plugin 与 Agent 注册协议明确约束。[S23][S24]

## 3. 两种安装路径

两个路径共用一个安装组件和同一精确 spec，只改变“谁执行”。`skills.sh` 的对应实现是：`Command` 复制 `npx skills add ...`，`Prompt` 则复制一段要求 Agent 运行 `npx skills use ...` 并遵循结果的完整指令。[S2]

### 路径 A：自己安装

按钮：`复制安装命令 / Copy install command`

```sh
dsh plugin --profile web add github:Shiyao-Huang/awesome-deepseek-harness-plugin#path:/plugin
```

复制后只显示两步状态：在终端运行；重启所选 DSH profile。不要再加一段解释 Market Plugin 是什么，因为命令上方的标题已经说明目的。该命令来自 Market Plugin 自己的安装文档。[S23]

### 路径 B：交给 DeepSeek

按钮：`复制给 DeepSeek / Copy for DeepSeek`

中文 prompt：

```text
为我的 DeepSeek Harness web profile 安装 deeplugin Market Plugin。
公开来源和精确安装标识是：
github:Shiyao-Huang/awesome-deepseek-harness-plugin#path:/plugin

先核对来源，展示将执行的完整命令、目标 profile 和影响；等待我确认后再安装。安装完成后告诉我是否需要重启，不要自动安装任何其他插件。
```

English prompt：

```text
Install the deeplugin Market Plugin into my DeepSeek Harness web profile.
Its public source and exact install spec are:
github:Shiyao-Huang/awesome-deepseek-harness-plugin#path:/plugin

First verify the source and show the full command, target profile, and impact. Wait for my confirmation before installing. Afterward, tell me whether a restart is required, and do not install any other plugin automatically.
```

复制 prompt 不等于授权安装。它必须保留“展示计划、等待确认”的语句，因为 Market Plugin 的正式流程要求 `requiresConfirmation: true`，拒绝后不得修改 profile。[S23][S24]

Market Plugin 安装后，首页可再给一个更短的任务 prompt：

```text
找一个能搜索公开网页并返回引用的插件。先给出前三个候选的来源、版本、稳定 id 和精确安装标识；不要安装。等我选中后再生成安装计划并等待确认。
```

## 4. QA 聊天案例

案例不要做成一张带大量注释的功能图，而应是四张连续、同尺寸的真实聊天界面截图。GitHub Marketplace 建议截图展示尽可能多的真实 UI、使用一致尺寸，并用短 caption 提供上下文；这个案例应遵循同样规则。[S9]

以下脚本使用 2026-08-16 市场快照中的 `ModSearch` 作为可复现示例：稳定 id `deeplugin-c39668d81007d2defdf8`、install spec `github:liustack/modsearch`、来源声明版本 `5.4.2`。截图必须标注“示例对话”，不要把来源 Registry 的 `verified` 声明画成 Store 背书。[S25]

| 幕 | 中文界面 | English UI | 画面必须出现的证据 |
| --- | --- | --- | --- |
| 1. 提问 | 用户：`我需要搜索公开网页并返回可点击引用，帮我找插件，先不要安装。` | User: `I need public web search with clickable citations. Find a plugin, but don't install it yet.` | 真实用户目标；不先讲 Market Plugin |
| 2. 搜索 | Agent：`找到 3 个候选。ModSearch 匹配 web/search；来源 zoahdev/dsh-subscribe；版本 5.4.2；稳定 id deeplugin-c39668d81007d2defdf8；安装标识 github:liustack/modsearch。` | Agent: `I found 3 candidates. ModSearch matches web/search; source: zoahdev/dsh-subscribe; version: 5.4.2; stable id: deeplugin-c39668d81007d2defdf8; install spec: github:liustack/modsearch.` | 三个结果、命中原因、来源、版本、id、spec |
| 3. 计划与确认 | Agent：`将安装到 web profile。计划命令：dsh plugin --profile web add github:liustack/modsearch。是否确认？` 用户：`确认。` | Agent: `This will install into the web profile. Planned command: dsh plugin --profile web add github:liustack/modsearch. Confirm?` User: `Confirm.` | 明确 profile、完整命令、确认按钮/回复 |
| 4. 使用结果 | Agent：`安装完成。现在我可以用它搜索“DeepSeek Harness plugin registry”，并把结果和引用返回给你。` | Agent: `Installed. I can now search for “DeepSeek Harness plugin registry” and return the results with citations.` | 安装结果、下一步真实能力；不要只显示绿色成功勾 |

每种语言单独渲染一套截图，不在同一气泡中堆叠双语。切换语言后标题、按钮、空状态、确认文案和 caption 一起切换；稳定 id、install spec、命令和 Registry 名称保持原样。四幕案例的主 CTA 是 `复制这段提问 / Copy this request`，它把浏览者直接送入已有 Agent 工作流。

## 5. 增长与内容分发

| 渠道 | 适合发布 | 执行动作 | 明确不要做 |
| --- | --- | --- | --- |
| GitHub | 源码、可复现数据、Release、路线图、贡献入口、真实截图 | 完善 description、topics、social preview；每周发布一份“新增插件 + 数据变化 + 3 个值得试的插件”Release；用 Issues/Discussions 接收提交；为 `deepseek-harness`、`dsh-plugin`、`plugin-registry` 等真实主题建立可发现入口 | 不要仅为了曝光创建无实质内容的仓库；不要把当前静态目录冒充符合要求的 GitHub Marketplace App。GitHub topics 用于发现相关解决方案，social preview 用于跨平台识别项目 [S10][S12][S13] |
| X | 简洁更新、15 秒内安装/搜索演示、数据图、开发过程和问答 | 每周 2-3 条不同内容：一条新插件、一条四幕 demo、一条数据洞察；文案简短、口语化、明确 CTA，视频加字幕；参与相关对话并个性化回复 | 不要批量、重复、无关或未经请求地发同一链接，不刷互动，不用多个账号放大。X 官方同时建议少用重文字图片、视频不超过 15 秒，并禁止批量重复内容扰乱体验 [S16][S17] |
| Hacker News | 可直接试用的 Store、开源实现、技术细节、数据方法 | 产品达到无需登录即可搜索、打开详情和复制安装后，做一次 `Show HN: deeplugin.store – a provenance-first plugin store for DeepSeek Harness`；正文解释为什么做、数据如何去重、安装为何确认；发布者全天在线用本人语言回答 | 静态列表、博客、newsletter 和 signup page 不能作为 Show HN；小版本更新通常不够；不拉朋友投票或评论；不要用生成式文本代替真人评论 [S14][S15] |
| 小红书 | 原生图文教程、真实使用体验、前后对比、四幕聊天案例、插件专题 | 每周 1-2 篇：`我让 DeepSeek 自己找并安装网页搜索插件`、`5 个 DSH 插件实测`；首图展示结果，正文完整讲步骤、失败与限制；使用平台内可读的截图和字幕 | 不要在笔记放站外 URL、二维码、水印、手机号或微信号导流；不要批量/高频/机器发布；不要照抄宣传话术或虚构体验。官方规范明确不鼓励营销导流，并禁止无真实体验、外部链接/二维码导流和非正常机器发布 [S18] |
| 微信公众号 | 完整长文、版本复盘、技术教程、数据故事、开发者访谈 | 每周或双周一篇可独立读完的文章：问题、真实对话截图、安装命令、来源和结果；链接只作为补充，不以“转发/关注后解锁”交换内容；商业推广按规则标识 | 不诱导分享、关注或跳转，不用题文不符按钮，不批量高频发送机器生成链接；若推销商品/服务并附购买方式，要显著标明“广告” [S19][S20] |
| Google / 自有站 | 任务型详情页、分类页、原始来源、图片/视频索引 | 每个可安装插件生成唯一标题、简述、来源、版本、spec 和相关项；分类页内部链接到详情；图片靠近说明并有 alt；提交包含图片/视频信息的 sitemap；用 Search Console 看覆盖和查询 | 不生成只有名字不同的薄页，不把 sitemap 当作收录保证。Google 强调 helpful、reliable、people-first 内容、清晰独特标题和内部链接；sitemap 只帮助发现，不保证抓取或索引 [S21][S22] |

### 内容生产系统

一次真实采集只产生一份事实包：新增插件、版本变化、来源、原生指标、截图/视频权利状态和可复现查询。各渠道只重新编排，不重新发明事实：GitHub Release 保留完整变更；站内生成可搜索详情；X 使用一个 15 秒动作；小红书使用四至六张原生步骤图；公众号使用完整教程；HN 只在重大可试用版本发布。任何渠道没有合适的新事实时就不发。

两小时采集任务不应直接触发社交发布。建议节奏是：站内和 SQLite 每两小时更新；GitHub 数据提交按既有流程；X 每周 2-3 条；小红书每周 1-2 篇；公众号每周或双周 1 篇；HN 只在首次公开可用或重大重构时发布一次。这样既保留“永恒采集”，又不触发 X、小红书和微信对批量重复内容的限制。[S15][S17][S18][S19]

### 30 天执行顺序

1. 第 1 周：重做首屏，删除重复介绍，发布搜索框与双安装标签；给所有 CTA 加独立事件名。
2. 第 1 周：详情页补齐 source、stable id、exact spec、version、observed date、确认提示和相关插件；建立 `热门 / 趋势 / 最新` 三套独立口径。
3. 第 2 周：制作中英文四幕聊天案例和 15 秒无声可读演示；GitHub 设置 topics 与 1280×640 social preview。[S9][S13][S16]
4. 第 2 周：发布第一份 GitHub Release 与一篇完整公众号教程；X 和小红书分别使用平台原生版本，不做相同文案搬运。
5. 第 3 周：确认无需登录即可完成搜索、详情与复制流程后发布 Show HN；发布者本人在线回答。[S14][S15]
6. 第 4 周：按漏斗数据调整首屏默认标签、搜索样例和榜单顺序，不以总访问量代替转化判断。

### 指标

核心漏斗应记录：`home_view -> search_submit -> result_open -> copy_command | copy_prompt -> install_plan_shown -> install_confirmed`。同时记录 locale、referrer、campaign 和 plugin id，但不要把 `copy_prompt` 当作已经安装；它只是离开网页后的可观察代理指标。

首页实验只比较一个变量：默认显示 `自己安装` 还是 `交给 DeepSeek`。主要指标是每百次详情访问产生的 `copy_command + copy_prompt`，次要指标是安装计划和确认；防护指标是无结果率、复制后立即返回率和安装拒绝率。GitHub Marketplace Insights 也把 landing page、checkout page 和 new subscriptions 分开统计，说明真正的转化分析需要逐步漏斗，而不是一个 pageview 数字。[S11]

## 一手来源

以下来源均于 2026-08-16 访问；未使用二手博客作为关键证据。

| 编号 | 来源 | 精确 URL | 访问日期 |
| --- | --- | --- | --- |
| S1 | skills.sh 首页 | https://skills.sh/ | 2026-08-16 |
| S2 | skills.sh skill 详情页 | https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices | 2026-08-16 |
| S3 | SkillsMP 首页 | https://skillsmp.com/ | 2026-08-16 |
| S4 | SkillsMP skill 详情页 | https://skillsmp.com/skills/juanlamadrid20-dbrx-multi-agent-retail-intelligence-claude-skills-mosaic-ai-agent-skill-md | 2026-08-16 |
| S5 | npm：搜索与选择 package | https://docs.npmjs.com/searching-for-and-choosing-packages-to-download/ | 2026-08-16 |
| S6 | npm：本地安装 package | https://docs.npmjs.com/downloading-and-installing-packages-locally/ | 2026-08-16 |
| S7 | VS Code Extension Marketplace 文档 | https://code.visualstudio.com/docs/editor/extension-marketplace | 2026-08-16 |
| S8 | Visual Studio Marketplace：Python extension | https://marketplace.visualstudio.com/items?itemName=ms-python.python | 2026-08-16 |
| S9 | GitHub Marketplace listing description 指南 | https://docs.github.com/en/apps/github-marketplace/listing-an-app-on-github-marketplace/writing-a-listing-description-for-your-app | 2026-08-16 |
| S10 | GitHub Marketplace app listing 要求 | https://docs.github.com/en/apps/github-marketplace/creating-apps-for-github-marketplace/requirements-for-listing-an-app | 2026-08-16 |
| S11 | GitHub Marketplace listing metrics | https://docs.github.com/en/apps/github-marketplace/creating-apps-for-github-marketplace/viewing-metrics-for-your-listing | 2026-08-16 |
| S12 | GitHub repository topics | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics | 2026-08-16 |
| S13 | GitHub social media preview | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview | 2026-08-16 |
| S14 | Hacker News Show HN 指南 | https://news.ycombinator.com/showhn.html | 2026-08-16 |
| S15 | Hacker News Guidelines | https://news.ycombinator.com/newsguidelines.html | 2026-08-16 |
| S16 | X Organic best practices | https://business.x.com/en/basics/organic-best-practices | 2026-08-16 |
| S17 | X Authenticity policy | https://help.x.com/en/rules-and-policies/authenticity | 2026-08-16 |
| S18 | 小红书社区规范 | https://agree.xiaohongshu.com/h5/terms/ZXXY20221213003/-1 | 2026-08-16 |
| S19 | 微信外部链接内容管理规范 | https://weixin.qq.com/cgi-bin/readtemplate?t=weixin_external_links_content_management_specification | 2026-08-16 |
| S20 | 微信公众平台：关于微信公众号营销内容合规规范的通知 | https://mp.weixin.qq.com/s/xrv89bsLqXfjIzGSj8_TWA | 2026-08-16 |
| S21 | Google Search SEO Starter Guide | https://developers.google.com/search/docs/fundamentals/seo-starter-guide | 2026-08-16 |
| S22 | Google Search sitemap overview | https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview | 2026-08-16 |
| S23 | deeplugin Market Plugin README | https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin/blob/main/plugin/README.md | 2026-08-16 |
| S24 | deeplugin Agent registration protocol | https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin/blob/main/docs/register-agent.md | 2026-08-16 |
| S25 | deeplugin public Market registry snapshot | https://deeplugin.store/data/market-registry.json | 2026-08-16 |
