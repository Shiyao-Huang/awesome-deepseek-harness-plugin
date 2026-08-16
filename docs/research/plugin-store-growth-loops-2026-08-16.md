# deeplugin.store 下一阶段增长循环调研

访问日期：2026-08-16

## 一句话结论

`deeplugin.store` 下一阶段不应把主要投入放在继续重排首页，而应把每个插件变成一个可分享、可嵌入、可更新、可归因的增长节点，再让作者提交、版本发布、榜单和社区分发持续把新流量送回同一个详情页。[S3][S5][S7][S19][S25]

## 三句话摘要

1. 成熟 marketplace 的共同机制是稳定详情 URL、明确版本和安装动作；Chrome 允许知道 URL 的用户安装 unlisted item，VS Code 以稳定 extension id 连接详情与安装，PyPI 则同时提供项目页、版本页和 release feed。[S1][S3][S19][S20]
2. 最便宜的站外增长不是运营账号持续发帖，而是让作者在 README、文档和发布页放一个可归因的 Store 链接或徽章；Chrome 官方直接提供“Available in the Chrome Web Store”站外徽章，JetBrains 会单列 plugin page referrals。[S5][S7]
3. 排名、发布和分析必须组成一条可解释漏斗：Homebrew 公布固定时间窗的 install-on-request 榜单及 JSON，GitHub Marketplace 分开计算 landing、checkout 和 subscription，Atlassian 也用 click、install、app request 等事件连接完整漏斗。[S10][S22][S23][S25]

## 研究边界与判断标准

本次比较 9 个成熟开发者生态：VS Code Marketplace、Chrome Web Store、JetBrains Marketplace、Atlassian Marketplace、WordPress Plugin Directory、npm、PyPI、Homebrew Formulae 和 GitHub Marketplace。只采用官方首页、官方文档或官方仓库；不把二手增长文章、聚合榜单或第三方 SEO 工具作为关键证据。

判断标准不是“首页长什么样”，而是一个机制能否形成可重复循环：`作者或事件产生入口 -> 用户进入稳定详情页 -> 用户执行可观察动作 -> 数据反馈给下一轮分发`。影响等级表示该机制能覆盖的插件和渠道范围；工作量是基于当前静态生成站点的研究估算，不是经过代码排期后的承诺。

## 9 个生态的可复用机制

| 生态 | 一手观察 | 可迁移到 deeplugin.store 的增长机制 | 适用边界 |
| --- | --- | --- | --- |
| VS Code Marketplace | Extension details 由稳定 `publisher.extension` 标识连接 Marketplace、IDE 内搜索和安装；搜索支持 popular、recently published、rating、published date、update date 等独立维度。发布工具把 README、CHANGELOG、icon 和受信 badge provider 纳入 listing 内容。[S1][S2] | 详情页使用稳定 id；把“最新”“最近更新”“热门”拆开；作者元数据直接生成展示页和嵌入代码。 | badge 只陈述可验证事实，不复制 VS Code 的 verified publisher 含义。[S2] |
| Chrome Web Store | Public item 进入搜索，unlisted item 仍可凭精确 Store URL 安装；测试版可与生产版并行。官方提供站外 Store badge、publisher page、daily installs/uninstalls 和 GA4 listing metrics。[S3][S4][S5][S6] | 让每个插件拥有可分享深链；提供官方样式的作者徽章；区分公开、试验和隐藏状态；把获客与流失分开看。 | deeplugin 深链只能打开详情或复制计划，不能绕过 DSH 确认自动安装。 |
| JetBrains Marketplace | Analytics 分开显示 page visitors、referrals、downloads，并可按产品和时间段过滤；upload API 支持 stable、nightly 等 channel；平台更新通知和 nurturing email 会把用户带回 plugin page、文档和 bug tracker。[S7][S8][S9] | 保存 referrer/campaign；支持 stable/beta 标签；把版本变化变成详情页、changelog 和作者可转发素材。 | 直接营销需要用户明确同意；不要复制平台拥有的邮件权限。[S9] |
| Atlassian Marketplace | Segment integration 的目标是连接 Marketplace 与 partner infrastructure 的完整漏斗，事件示例包含 click、install 和 app request，并携带 partner/plugin id；Reports 再区分 evaluation、conversion、renewal 和 churn。[S10][S11] | 网站事件和 Market Plugin 事件共用 `plugin_id`、`campaign` 和阶段名；分别报告发现、复制、计划、确认。 | 不用一个“conversion”吞掉不同阶段，也不引入跨站匿名身份拼接。[S10][S11] |
| WordPress Plugin Directory | `readme.txt` 直接生成公开插件页，Stable Tag 决定稳定版本；独立 assets 目录管理 icon、banner 和 screenshot；官方提交流程把文档、review、首次发布和后续维护串起来。[S13][S14][S16] | 让一个提交事实包同时生成详情、版本、媒体、徽章和发布条目；作者只维护一个来源。 | 不以高频小更新冲榜，不做 keyword stuffing、强制 backlink 或未经同意的 tracking。[S15] |
| npm | 包 README 会渲染到 package page，并被官方描述为帮助开发者发现和使用 package；dist-tag 用 `latest`、`beta`、`canary` 等人类可读标签连接发布和安装。[S17][S18] | 从来源 README/结构化字段生成详情内容；版本 channel 进入筛选、详情和变更流。 | README 更新应绑定真实发布，不把无版本事实的文案变动冒充 release。[S17] |
| PyPI | 官方同时提供 newest packages、latest updates 和单项目 releases 三种 RSS；JSON API 暴露 canonical project/release URL、summary、version、project links 和 release metadata。[S19][S20] | 提供全站新增、全站更新和单插件发布 feed；从结构化数据生成唯一详情与版本页。 | “verified project URL”只代表上传时验证，不能升级成持续安全背书。[S21] |
| Homebrew Formulae | Formulae 站公开 30 天 install-on-request 榜单及对应 JSON；单 formula/cask API 带 analytics 和 generation date；新版本可通过标准 PR 与 bump 命令提交。[S22][S23][S24] | 榜单公开窗口、指标来源和生成时间；提交/更新走可审查 PR；详情和榜单由同一结构化事实生成。 | 只比较同一原生指标，不把 stars、likes、views 和 installs 相加。 |
| GitHub Marketplace | Insights 分开统计 unique landing visitors、checkout visitors 和 new subscriptions；Action 通过公开仓库的 metadata、tag 和 release 发布到独立 Marketplace page，版本会显示在详情页；GitHub Release 可带 release notes、contributors 和 discussion。[S25][S26][S27] | 采用逐步漏斗；一次有效 release 同时更新版本页、changelog、贡献者和社区分发入口。 | 不能把当前目录冒充符合 GitHub Marketplace 要求的 App；这里只借鉴机制。[S25][S26] |

## 最强 5 个可实现机制

排序按预期 impact/effort 比，而不是按功能完整度。先做第 1、2 项可以立即形成站外入口；第 3、4 项让入口持续更新；第 5 项在已有高质量详情数据上扩大非品牌发现。

| 排名 | 机制 | 增长循环 | 预期影响 | 估算工作量 | 实现范围与验收 |
| --- | --- | --- | --- | --- | --- |
| 1 | 可分享规范详情页 + 归因深链 | 用户/作者分享 `stable_id` URL -> 新用户打开同一插件证据页 -> 复制命令或 Agent prompt -> referrer/campaign 回流 | 高 | 2-4 工程日 | 为每个可安装插件输出唯一 canonical、share preview metadata、source、version、observed date、exact install spec、changelog 摘要和相关插件；`?ref=`/`?campaign=` 只参与分析，不进入 install spec。Chrome 的 unlisted URL、VS Code 的稳定 extension id 和 PyPI 的 project/release URL 都证明稳定深链是跨入口复用的基础；Google 同样要求每页有清晰、独特的标题和可抓取链接。[S1][S3][S20][S28] |
| 2 | 作者徽章与嵌入包 | 作者把 badge 放进 README/docs -> badge 点击进入带 `ref=badge` 的详情页 -> Store 将流量归因到插件/作者 -> 作者看到结果后继续保留 badge | 中高 | 1-2 工程日 | 生成静态 SVG、Markdown、HTML 三种片段；默认文案只写 `Listed on deeplugin.store` 或声明版本，不写 `verified`、`safe`、下载量；badge 目标始终是详情页。Chrome 的官方站外 badge 和 JetBrains 的 referral 报告给出了完整样板。[S5][S7] |
| 3 | 提交 -> 自动发布 -> 作者分发 | 作者提交/更新 -> 校验通过 -> 自动生成详情、badge、changelog 和分享链接 -> 作者转发 -> 带归因的新访问带来更多作者 | 高 | 4-7 工程日 | 在现有 human/Agent 提交之后返回一个 launch packet：详情 URL、badge、中文/英文短文案、精确 install spec 和 release entry；首发与更新都走同一来源事实。WordPress、Homebrew 和 GitHub Action 分别用规范文件、PR、tag/release 把作者操作变成目录更新。[S13][S16][S24][S26] |
| 4 | 变更事件驱动的 changelog、RSS 与透明榜单 | 新增/更新/趋势变化 -> 进入 feed、榜单和 GitHub Release -> 社区或订阅者回访详情 -> 行为反馈下一期内容 | 中高 | 3-5 工程日 | 输出 `new`、`updated` 和每插件 release feed；榜单固定显示指标、source、窗口、generated_at；每周只在有事实变化时生成一份 GitHub Release。PyPI 拆分三类 RSS，Homebrew 公开 30 天榜单与 JSON，VS Code 拆分 recent/published/update/popular。[S1][S19][S22][S23][S27] |
| 5 | 有限集合的任务/分类程序化页 | 来源事实 -> 生成高差异任务页 -> 搜索或社区问题命中 -> 用户比较 3-8 个真实候选 -> 进入详情和安装代理动作 | 中高 | 5-8 工程日 | 首批只做 10-12 个有至少 3 个真实候选的任务页；每页必须有唯一 intent、筛选依据、候选差异、来源日期和内部链接，不能仅替换关键词。npm/PyPI 用结构化 metadata 生成独立项目内容，WordPress 用单一 readme 生成公开详情，Atlassian 和 Google 都要求自然、独特、面向用户的内容而非关键词堆砌。[S12][S13][S17][S20][S28] |

### 前置测量地基

五个机制共用一条事件链：`detail_view -> share_action | badge_referral -> copy_command | copy_prompt -> install_plan_shown -> install_confirmed`。网页只能把 `copy_command`/`copy_prompt` 记为 activation proxy；只有 Market Plugin 实际写出的计划和确认事件才进入安装漏斗，二者不能合并。[S10][S25]

每个事件只需要 `plugin_id`、`event_name`、`referrer_class`、`campaign`、`locale`、`variant` 和时间；默认不采集 PII、指纹或跨站 user id。若未来需要持久身份或营销联系，先取得明确同意；WordPress 和 JetBrains 的官方规则都把外部 tracking/营销同意列为限制。[S9][S15]

核心比率定义如下：

- `activation_proxy_rate = unique(copy_command or copy_prompt) / unique(detail_view)`。
- `confirmed_install_rate = unique(install_confirmed) / unique(install_plan_shown)`；没有 Market Plugin 回传时显示“无数据”，不以复制替代。
- `share_rate = unique(share_action) / unique(detail_view)`。
- `attributed_activation_rate = unique activation proxies from one ref/campaign / qualified sessions from that ref/campaign`。

## 不该做的增长方式

| 不做 | 原因与停止线 |
| --- | --- |
| 批量生成只有插件名/关键词不同的薄页 | Atlassian 要求名称、tagline、summary 自然表达价值并明确反对 keyword stuffing；WordPress 禁止 black-hat SEO、竞品 tags 和关键词堆砌。任何任务页没有至少 3 个可比较候选和独立选择依据就不发布。[S12][S15] |
| 把来源声明、URL 所有权或作者身份画成安全认证 | PyPI 的 verified URL 只说明上传时的控制权；VS Code、Chrome 和 JetBrains 的 badge 都有各自审核含义。deeplugin badge 只陈述“已收录”和带日期的来源事实，不写 `safe`、`official` 或 `verified by deeplugin`。[S2][S6][S21] |
| 用高频微小更新占据“最近更新”，或付费/私下换榜单位置 | WordPress 明确把快速小提交冲 Recently Updated 视为 gaming；Chrome Editors' Picks 不能付费获得。榜单只由公开规则和固定窗口生成，商业合作不能改 rank。[S6][S15] |
| 合并不同平台的 stars、likes、views、downloads 得出一个“增长分” | JetBrains 分开 page visitors、referrals 和 downloads，GitHub 分开 landing、checkout 和 subscriptions，Homebrew 的榜单只使用 install-on-request。deeplugin 也应保留原生指标和 source，而不是制造不可解释总分。[S7][S22][S25] |
| 强制作者 backlink、诱导评价、自动注入推广链接 | WordPress 禁止未经同意的外部 credits/links、affiliate spam、虚假 reviews 和搜索操纵。badge 必须自愿，提交通过与否不依赖作者是否嵌入。[S15] |
| 每两小时采集一次就同步群发一次，或为无事实变化生成 release | GitHub Release 的单位是带 tag、notes 和可选 discussion 的项目迭代；PyPI/WordPress 也把 release 与真实版本事件绑定。采集频率与社区发布频率必须解耦。[S13][S19][S27] |
| 用详情深链绕过安装确认 | Chrome 的 URL 可以直接进入 Store 安装路径，但 deeplugin 的增长链接应停在可审查详情与复制动作；任何 ref/campaign 都不得改变精确 install spec 或触发自动安装。[S3] |

## 30 天实验矩阵

实验从同一事件字典开始，站内 variant 按稳定 session hash 分流；同一 session 同时只进入一个站内展示实验。第 22 天后冻结站内 variant 再做社区分发，避免把产品改动误判成渠道效果。每个比率在 100 个 eligible detail sessions 前只报告方向；到第 30 天仍未达到样本门槛则标记 `inconclusive`，不把它写成成功。

| 天数 | 实验 | 处理与对照 | 成功指标 | 护栏 | 停止条件 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| 1-3 | E0：事件与归因 A/A | 两个完全相同 variant 只验证事件；对照访问日志、网站事件和 Market Plugin 阶段 | 事件 `plugin_id`/`event_name` 完整率 >=95%；A/A 流量在 45/55 内；pageview 与访问日志差异 <=5%；复制、计划、确认可分开 | 不采集 PII；campaign 不进入命令/spec | 任一 install spec 被归因参数污染、缺失率 >5%、重复事件 >1% 或确认被误记为复制，立即停掉后续实验 | Atlassian 和 GitHub 都按阶段定义漏斗，而不是只看 pageview。[S10][S25] |
| 4-10 | E1：详情页分享/深链组件 | 50% 详情页增加 copy link/native share 与中英文分享文案；50% 保留现状 | `share_rate >=5%`，且产生 >=30 次 share action、>=100 次 attributed detail sessions；这些流量的 activation proxy 不低于站点同期中位数 | canonical 去掉 campaign；分享内容保留 source/date，不声称安全 | 200 个 eligible sessions 后 `share_rate <1%`，或链接 404/错误插件率 >0.5% | Chrome unlisted URL 与 VS Code/PyPI 稳定详情 id 支持“一个对象、多个入口”。[S1][S3][S20] |
| 5-14 | E2：20 位作者 badge pilot | 向 20 个有公开 README 的作者提供已填好的 Markdown/HTML；未联系作者为自然对照 | >=5 个公开合并/采用，>=100 次 `ref=badge` sessions，`attributed_activation_rate >=8%` | badge 文案仅 `Listed on deeplugin.store`/版本；作者可随时移除 | 20 个可送达邀请后 <2 个采用，或 badge 资源错误率 >0.5%，停止扩量并访谈原因 | Chrome 提供站外 Store badge；JetBrains 直接报告 referrals。[S5][S7] |
| 8-18 | E3：提交后 launch packet | 所有通过校验的新提交/版本更新自动收到详情 URL、badge、双语短文案和 release entry；历史流程作基线 | >=5 个有效提交/更新；median submit-to-public <48h；>=40% 作者在 7 天内至少分享一个归因链接 | 校验 source、stable id、exact spec、version 后才发布；不因是否分享影响审核 | 错误 install spec 进入公开页 >=1 次立即停止；或人工处理 median >30 分钟/条时停止自动扩量 | WordPress 提交流程、Homebrew PR 和 GitHub Action release 都把作者动作直接连接到公开 listing。[S16][S24][S26] |
| 12-24 | E4：新增/更新/趋势 feed 与周 release | 发布 `new`、`updated`、per-plugin release feeds 和一份有真实变化的 GitHub Release；榜单标题显示窗口/指标/source | 榜单到详情 CTR >=15%；feed/release 带来 >=20 次 attributed detail sessions；这些 sessions 的 activation proxy >=站点同期中位数 | 不混指标；没有第二个同源快照就不判趋势；无变化不发 release | >10% 上榜项缺 source/window/generated_at，或出现无法复算的排名，立即撤下榜单 | PyPI 的三类 RSS、Homebrew 的 30 天 JSON 榜单和 GitHub Release 是可复用组合。[S19][S22][S23][S27] |
| 11-30 | E5：12 个任务型程序化页 | 只生成候选 >=3 的任务页；对照现有 generic category 页 | 12 页结构事实完整率 100%；到第 30 天 Search Console indexed >=70%；非品牌 impressions >=100；进入详情后的 activation proxy 不低于 generic category | 每页必须有唯一 intent、候选差异、source/date；canonical 唯一 | 任一页候选 <3 即不发布；已提交页面中 >20% 持续为 duplicate/soft-404/crawled-not-indexed，停止扩页并重写模板 | npm/PyPI/WordPress 从单一 metadata/readme 生成独立项目页；Atlassian 反对关键词堆砌；Google 官方文档把 Search Console 定位为监测抓取、索引和搜索表现的工具。[S12][S13][S17][S20][S28][S29] |
| 22-30 | E6：一次 release + 作者共同分发 | 冻结站内 variant；发布一份 GitHub Release，并让 E2/E3 已采用作者转发各自带 campaign 的详情链接 | >=200 attributed sessions，整体 attributed activation >=8%，且至少 3 个不同作者/来源贡献 >=10 sessions | 一份事实包按渠道改写，不批量复制文案；只发布真实新增/更新 | 200 sessions 后 activation <2%，或任何社区 moderation/作者投诉，立即停止该渠道模板；未到 200 sessions 只判 `inconclusive` | GitHub Release 支持 notes、contributors、discussion；JetBrains 更新通知始终回到详情、文档和支持入口。[S9][S27] |

### 30 天后的决策

只保留同时满足“可重复入口”和“有效 activation”的机制。E1/E2 若能带来流量但 activation 低，先修详情证据与安装动作，不扩渠道；E3 若作者愿意提交但不分享，保留提交自动化、删除营销包；E4/E5 若只有 impressions 没有详情点击，缩减 feed/任务页，不以曝光量宣布增长。分阶段判断沿用 GitHub、Atlassian 和 JetBrains 对 visitor/referral/download/install/subscription 的拆分方式。[S7][S10][S11][S25]

## 一手来源

以下 29 个来源均于 2026-08-16 访问；S1-S27 来自对应 marketplace/directory 的官方首页、官方文档或官方仓库，S28-S29 来自 Google Search 官方文档；未使用二手博客作为关键证据。

| 编号 | 来源 | 精确 URL | 访问日期 |
| --- | --- | --- | --- |
| S1 | VS Code：Extension Marketplace | https://code.visualstudio.com/docs/configure/extensions/extension-marketplace | 2026-08-16 |
| S2 | VS Code：Publishing Extensions | https://code.visualstudio.com/api/working-with-extensions/publishing-extension | 2026-08-16 |
| S3 | Chrome Web Store：set up distribution | https://developer.chrome.com/docs/webstore/cws-dashboard-distribution | 2026-08-16 |
| S4 | Chrome Web Store：listing metrics | https://developer.chrome.com/docs/webstore/metrics | 2026-08-16 |
| S5 | Chrome Web Store：branding / Store badge | https://developer.chrome.com/docs/webstore/branding | 2026-08-16 |
| S6 | Chrome Web Store：discovery | https://developer.chrome.com/docs/webstore/discovery | 2026-08-16 |
| S7 | JetBrains Marketplace：Analytics tab | https://plugins.jetbrains.com/docs/marketplace/analytics-tab.html | 2026-08-16 |
| S8 | JetBrains Marketplace：Plugin upload API | https://plugins.jetbrains.com/docs/marketplace/plugin-upload.html | 2026-08-16 |
| S9 | JetBrains Marketplace：sales-related emails and in-product notifications | https://plugins.jetbrains.com/docs/marketplace/sales-related-emails.html | 2026-08-16 |
| S10 | Atlassian Marketplace：Segment integration | https://developer.atlassian.com/platform/marketplace/marketplace-integration-with-segment/ | 2026-08-16 |
| S11 | Atlassian Marketplace：Reports | https://developer.atlassian.com/platform/marketplace/reports/ | 2026-08-16 |
| S12 | Atlassian Marketplace：app listing principles | https://developer.atlassian.com/platform/marketplace/marketplace-app-listing-principles/ | 2026-08-16 |
| S13 | WordPress Plugin Directory：Plugin Readmes | https://developer.wordpress.org/plugins/wordpress-org/how-your-readme-txt-works/ | 2026-08-16 |
| S14 | WordPress Plugin Directory：Plugin Assets | https://developer.wordpress.org/plugins/wordpress-org/plugin-assets/ | 2026-08-16 |
| S15 | WordPress Plugin Directory：Detailed Plugin Guidelines | https://developer.wordpress.org/plugins/wordpress-org/detailed-plugin-guidelines/ | 2026-08-16 |
| S16 | WordPress Plugin Directory：Planning, Submitting, and Maintaining Plugins | https://developer.wordpress.org/plugins/wordpress-org/planning-submitting-and-maintaining-plugins/ | 2026-08-16 |
| S17 | npm：About package README files | https://docs.npmjs.com/about-package-readme-files/ | 2026-08-16 |
| S18 | npm：Adding dist-tags to packages | https://docs.npmjs.com/adding-dist-tags-to-packages/ | 2026-08-16 |
| S19 | PyPI：RSS Feeds | https://docs.pypi.org/api/feeds/ | 2026-08-16 |
| S20 | PyPI：JSON API | https://docs.pypi.org/api/json/ | 2026-08-16 |
| S21 | PyPI：Project Metadata | https://docs.pypi.org/project_metadata/ | 2026-08-16 |
| S22 | Homebrew Formulae：install-on-request analytics, 30 days | https://formulae.brew.sh/analytics/install-on-request/30d/ | 2026-08-16 |
| S23 | Homebrew Formulae：JSON API | https://formulae.brew.sh/docs/api/ | 2026-08-16 |
| S24 | Homebrew：How to Open a Homebrew Pull Request | https://docs.brew.sh/How-To-Open-a-Homebrew-Pull-Request | 2026-08-16 |
| S25 | GitHub Marketplace：Viewing metrics for your listing | https://docs.github.com/en/apps/github-marketplace/creating-apps-for-github-marketplace/viewing-metrics-for-your-listing | 2026-08-16 |
| S26 | GitHub Marketplace：Publishing actions in GitHub Marketplace | https://docs.github.com/en/actions/how-tos/create-and-publish-actions/publish-in-github-marketplace | 2026-08-16 |
| S27 | GitHub：Managing releases in a repository | https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository | 2026-08-16 |
| S28 | Google Search：SEO Starter Guide | https://developers.google.com/search/docs/fundamentals/seo-starter-guide | 2026-08-16 |
| S29 | Google Search：Get started with Search Console | https://developers.google.com/search/docs/monitor-debug/search-console-start | 2026-08-16 |
