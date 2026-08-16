# deeplugin.store 首页、增长循环与分发渠道 Benchmark

访问日期：2026-08-16

## 一句话结论

deeplugin.store 的首页应从“展示全部数据”改成“把一个任务送进可审查安装计划”：首屏只保留任务搜索、复制给 DeepSeek、自己安装三件事，下面用少量任务合集、真实 QA 案例和 `new` / `updated` 入口完成发现；成熟 Store 的共同做法也是把搜索、精选、稳定身份、详情证据和安装动作分层，而不是在首页展开整个目录。[skills.sh](https://www.skills.sh/)、[VS Code Marketplace 文档](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)、[Chrome Web Store 首页](https://chromewebstore.google.com/)、[npm 搜索文档](https://docs.npmjs.com/searching-for-and-choosing-packages-to-download/)、[Shopify App Store 首页](https://apps.shopify.com/)、[Vercel Integrations 文档](https://vercel.com/docs/integrations)

## 三条决策

1. **首页是决策面，不是数据库投影。** 当前 `docs/index.html` 为 16,561,754 bytes，并在初始 HTML 中渲染 14,406 个 `skill-card`；应把完整生态目录留在 `directories.html`，把完整可安装目录留在 `market.html`，首页首次响应只展示少量、可解释的任务入口。Chrome 首页使用合集、Top categories、Trending、Popular、New and notable 和 Editors' Picks 分层，而 Shopify 首页使用 Built for Shopify、Popular、Spotlight、案例与官方应用分层，两者都没有把全量目录直接铺在首页。[Chrome Web Store 首页](https://chromewebstore.google.com/)、[Shopify App Store 首页](https://apps.shopify.com/)
2. **增长北极星不是 pageview，也不是复制次数，而是用户是否看到并批准了准确计划。** VS Code 把发现、详情和安装放在编辑器内；Vercel 还让 CLI 与 AI Agent 直接添加 integration。deeplugin.store 对应的核心路径应是 `qualified_visit -> task_search -> result_open -> copy_agent_request -> plan_shown -> install_succeeded`，每一步分开，不得把前一步冒充后一步。[VS Code Marketplace 文档](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)、[Vercel Integrations 文档](https://vercel.com/docs/integrations)
3. **两小时采集只更新事实，不应变成两小时发帖。** 外部渠道只消费“实质更新”生成的版本化 distribution object；GitHub Discussion 适合周报、问答和公告，X 适合经人审的图文短稿，Show HN 只适合用户可以直接试用的重大产品发布，不适合列表、落地页和普通版本更新。[GitHub Discussions](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/about-discussions)、[X Create Posts API](https://docs.x.com/x-api/posts/create-post)、[Show HN 指南](https://news.ycombinator.com/showhn.html)

## 研究边界与当前基线

本文件是 `docs/research/plugin-store-growth-next-loop-2026-08-16.md` 的首页与分发增量研究。外部事实只采用产品官方首页、官方开发者文档、官方源码仓库和官方社区规则；没有把第三方“增长黑客”文章当作证据。所有外部关键结论在同一段或同一表格单元格中给出 URL。

当前仓库基线为提交 `90e0e07ab5a0ca2e06c612af1cbe1ceed29c0de9`。只读检查得到：

- `docs/index.html` 为 16,561,754 bytes，初始 HTML 含 14,406 张生态 `skill-card`、786 个 `<img>`，同时承载 Store hero、安装教程、四帧 QA 案例、Hot signals 和完整 Directory。
- `docs/market.html` 为 2,647,040 bytes，承载 1,116 个当前可安装插件；这才是完整 Store 浏览面的自然归属。
- 首屏已经具备任务搜索、“自己安装 / 交给 DeepSeek”两条安装路径和中英文 QA 案例；当前主要问题不是缺模块，而是首屏后的首页职责无限扩张。
- 当前页面已经有稳定 Registry ID、精确 install spec、来源 claim、详情页、`new` / `updated` Atom、per-plugin Feed 与 launch packet，因此本轮建议不重复建设这些基础设施。

## 六个成熟 Store 的可复用模式

### 1. skills.sh：一个搜索框、三个榜单视角、一个可复制安装动作

skills.sh 首页把 Search 放在榜单上方，只提供 All Time、Trending (24h) 和 Hot 三个视角；每行集中显示 skill、来源、活动趋势和安装量。官方说明榜单由 CLI 的匿名安装遥测驱动，badge 又把安装量带回作者 README；官方 CLI 同时支持 `find`、`add`、`use`、`update` 和跨多种 Agent 的统一来源格式，形成“安装 -> 排名 -> badge / 来源页 -> 新发现”的闭环。[skills.sh 首页](https://www.skills.sh/)、[skills.sh 文档](https://www.skills.sh/docs)、[vercel-labs/skills 官方源码](https://github.com/vercel-labs/skills)

**可直接借鉴：** 首页搜索优先；把 `new`、`updated` 与未来有真实成功安装回执后才能成立的 `popular` 分开；每个条目只显示来源、稳定 ID、精确动作和一个主 CTA；让作者复制自愿 badge 或 launch packet。[skills.sh 文档](https://www.skills.sh/docs)

**不可照搬：** deeplugin.store 目前没有经同意、可去重的成功安装回执，不能把卡片复制、GitHub stars 或 Registry 出现次数改名为 installs，也不能上线伪 Trending。skills.sh 自己也明确提醒目录无法保证每个 skill 的质量或安全，安装前应审查；deeplugin.store 更应保留 review-first。[skills.sh 文档](https://www.skills.sh/docs)

**具体建议：** 首页不展示一个“总榜”；先展示 3 个任务 Pack、6 个新插件、6 个实质更新。未来只有在 `install_succeeded` 事件定义、同意流程、去重、反作弊与样本边界公开后，才增加“Market Plugin confirmed installs”视角。

### 2. VS Code Marketplace：Store 在工作流里，详情紧邻安装

VS Code 的主要 Marketplace 体验不依赖独立营销首页，而在编辑器 Extensions view 内完成：Popular 列表的卡片显示简述、publisher、download count 与 rating；搜索匹配 title 或 metadata；详情页继续展示 README、Feature Contributions、Changelog、Dependencies 和 Extension Pack 成员，Install 按钮始终靠近决策。它还允许按 install count、rating、name、published date、updated date 排序，并提供 workspace recommendations。[VS Code Marketplace 文档](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)

稳定身份由 `publisher.extension` 定义；初次安装第三方 publisher 的扩展时，VS Code 会要求用户确认信任 publisher。发布方可查看 Acquisition Trend、Total Acquisitions、Ratings & Reviews，并可用 README、CHANGELOG、SUPPORT、icon 和 verified publisher 信息强化详情页。[发布 VS Code Extension](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)

**可直接借鉴：** 把网页 CTA 写成能直接进入 Agent 工作流的一条请求；详情页按“做什么、来源是谁、精确 spec、版本、变更、依赖/冲突、确认”组织；稳定 ID 比相似名称更醒目；任务 Pack 展开成员而不是隐藏批量安装内容。[VS Code Marketplace 文档](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)

**不可照搬：** VS Code 可以在受控客户端里直接安装并检查 publisher，deeplugin.store 是静态聚合站，不能把网页按钮写成未经审查的一键安装，也不能把 Registry Source 的 `verified` claim 等同于 publisher 信任、安全审计或兼容保证。

**具体建议：** Market Plugin 是 deeplugin.store 的“in-product Extensions view”。首页主 CTA 应为“复制给 DeepSeek”，详情页主 CTA 应为“让 Agent 展示计划”；CLI 自装降为同级次要路径，而不是增加第三种解释性文案。

### 3. Chrome Web Store：编辑精选负责发现，真实使用负责排序

Chrome 首页把发现拆成主题合集、Top categories、Top charts、Trending、Popular、New and notable、Editors' Picks 和场景专题；卡片只展示少量候选，用户再进入详情。[Chrome Web Store 首页](https://chromewebstore.google.com/)

Chrome 官方说明，搜索会使用 listing metadata；排名还考虑评分、downloads 相对 uninstalls 的长期表现、视觉设计、明确用途、真实需求、onboarding 与易用性。Featured 与 collection 是人工策展，不能购买，也没有开发者可以照单保证入选的 checklist；官方同时建议开发者独立推广，获得真实使用后才可能在排序与策展中上升。[Chrome Web Store Discovery](https://developer.chrome.com/docs/webstore/discovery/)

Listing 要先用一句简洁陈述说明产品做什么，再提供详细信息；支持 category、locale、最多五张截图、YouTube 演示视频、verified official URL、homepage 与 support URL。图片质量会影响 Store prominence，本地化描述、截图和视频应保持功能事实一致。[Chrome Web Store Listing](https://developer.chrome.com/docs/webstore/cws-dashboard-listing/)

**可直接借鉴：** 首页用任务合集和有限候选替代总表；将 `new`、`updated`、`popular` 语义分开；详情页给一张主视觉、最多若干事实图、来源主页、支持/问题入口和 locale 一致性检查。[Chrome Web Store 首页](https://chromewebstore.google.com/)、[Chrome Web Store Listing](https://developer.chrome.com/docs/webstore/cws-dashboard-listing/)

**不可照搬：** 本项目没有 Chrome 的编辑团队、卸载量、用户评分治理和 publisher 身份体系，不能使用 “Editors' Picks”“Featured badge”“Established Publisher” 或“用户最爱”这些暗示官方评审的标签。

**具体建议：** 用“任务合集 / 来源可追溯合集”代替“编辑精选”；每个合集公开 curator、成员理由、成员版本、`dataset_version` 和更新时间。任何“热门”都必须注明单一原生指标及窗口，不把 stars、likes、views 相加。

### 4. npm：搜索优先，详情页承担全部技术判断

npm 官方搜索使用 package title、description、README 和 keywords，默认按关键词匹配保持中立，只对 spam 或极新的包做最小降权；用户还可以按 downloads、dependents 和 last published 排序。新包可能延迟进入搜索，deprecated package 会从结果中排除。[npm 搜索与选择 package](https://docs.npmjs.com/searching-for-and-choosing-packages-to-download/)

`name + version` 构成唯一身份；description 和 keywords 明确服务于发现，homepage 与 repository 提供来源。README 在 package 详情页直接渲染，官方建议其中包含安装、配置和使用说明；README 只有随新版本 publish 才会更新。[npm package.json](https://docs.npmjs.com/cli/v11/configuring-npm/package-json)、[npm README 文档](https://docs.npmjs.com/about-package-readme-files/)

npm provenance 在详情页以可验证来源和透明日志帮助用户审计，但官方明确说 provenance 不保证没有恶意代码。停止维护时，npm 更推荐 deprecate 并给出迁移消息，而不是直接 unpublish；整包 deprecated 后会退出搜索但保留说明。[npm provenance](https://docs.npmjs.com/generating-provenance-statements/)、[查看 provenance](https://docs.npmjs.com/viewing-package-provenance/)、[npm deprecation](https://docs.npmjs.com/deprecating-and-undeprecating-packages-or-package-versions/)

**可直接借鉴：** 搜索排序默认保持可解释；稳定 ID、版本、来源、README/说明、变更、弃用状态和替代项进入详情；来源证明只说明“从哪里来”，不升级为“安全”。

**不可照搬：** npm download 与 dependents 是包管理器原生事件，GitHub stars 不是等价指标；不同 install spec 也不能因共享 repository 就合并成一个插件。npm 的 provenance 语义不能被借来包装 Registry Source 的自称 verified。

**具体建议：** 首页默认搜索按来源字段与可追溯 intent term 匹配，不让 repo stars 改写相关性；排序明确分为 relevance、recently materially updated、repository stars。inactive Listing 保留详情和历史，显示 replacement / source inactive，而不是静默消失。

### 5. Shopify App Store：从社会证明到完整安装漏斗

Shopify 首页先展示 Built for Shopify，再展示 Popular、Spotlight、商家案例、Made by Shopify 和 Store 的审查/推荐解释。卡片把 rating、review count、pricing 和一句商家收益并排；“Get that tech stack”直接用商家结果解释为什么组合应用。[Shopify App Store 首页](https://apps.shopify.com/)

官方把 listing 称为最重要的营销工具之一，并要求用 feature media、demo、screenshots、短 introduction、details、scannable feature list、integration 与 pricing 分层；视频或静态图要说明产品收益，介绍与功能描述要避免 keyword stuffing 和无法证明的结果。准确 category、tag、语言和 dedicated documentation 会影响发现与理解。[Shopify App Store best practices](https://shopify.dev/docs/apps/launch/shopify-app-store/best-practices)

Shopify 的增长循环是显式的：外部流量可帮助 Store 排名并进入 Trending；视频教程可被搜索引擎索引并复用于文档、社交和邮件；社区参与要先提供价值、避免 spam；listing 改动后要测量访问到安装的变化。它还区分 home、search、category、collection、story、app_details 等来源面，以及 view detail、click Install、finish install 等漏斗事件。[Shopify app marketing](https://shopify.dev/docs/apps/launch/marketing)、[Shopify listing traffic](https://shopify.dev/docs/apps/launch/marketing/track-listing-traffic)

评论只有已安装或卸载不超过 45 天的 merchant 才能留下；rating 会偏重近期、有用、可信的评论。官方禁止索要好评、激励评论和伪造评论，并要求在用户形成真实体验后再中性询问。[Shopify reviews](https://shopify.dev/docs/apps/launch/marketing/manage-app-reviews)

**可直接借鉴：** 首页用真实任务案例解释“这个插件组合解决什么”，并给每个首页 section、card position、locale 和 distribution object 稳定 campaign 字段；把 view、copy、plan、confirm、success 分开；中文内容优先采用可演示的任务结果，而不是目录广告。[Shopify listing traffic](https://shopify.dev/docs/apps/launch/marketing/track-listing-traffic)

**不可照搬：** deeplugin.store 没有 merchant 身份、统一 billing、安装验证、review moderation 或相似商家数据，不能做五星评论、个性化推荐、Built for Shopify 式质量徽章，也不能复制包含用户或工作区身份的跨站追踪。

**具体建议：** 先只保存公开、无用户标识的 campaign metadata；任何成功安装遥测必须另行完成 opt-in、隐私、去重和反作弊。没有真实已安装用户资格验证前，不上线 reviews，只保留来源平台的原生互动数字并明确平台。

### 6. Vercel Marketplace / Integrations：发现直接连接可执行入口

Vercel 把 Marketplace 定义为在项目中发现、接入和管理第三方方案的入口，强调 seamless authentication、unified billing 与 one-click deployments；文档同时提供 category 浏览、dashboard 安装和 `vercel integration add` CLI，并明确 CLI 可用于 CI 和 AI agents。[Vercel Marketplace](https://vercel.com/marketplace)、[Vercel Integrations](https://vercel.com/docs/integrations)

Integration listing 要有唯一 slug、developer、support、40 字以内 short description、说明 why / when 的 overview、category、documentation、privacy/support 链接和高质量 gallery；第一张 gallery 图会用于自动生成 Open Graph。审批 checklist 不只看页面，还要求新旧用户安装、外部 logged-out flow、配置、卸载和端到端真实功能都通过。[Vercel listing requirements](https://vercel.com/docs/integrations/create-integration/submit-integration)、[Vercel approval checklist](https://vercel.com/docs/integrations/create-integration/approval-checklist)

**可直接借鉴：** 卡片短、category 明确、详情解释 why / when；每个页面提供一条可复制到 Agent 的准确动作；主视觉同时服务详情、OG 与渠道稿；上线 CTA 前验证从查找到卸载的完整路径。[Vercel approval checklist](https://vercel.com/docs/integrations/create-integration/approval-checklist)

**不可照搬：** Vercel 的一键体验建立在账号、OAuth、billing、Marketplace API 和平台级资源管理上；deeplugin.store 不能用静态网页假装拥有相同保证，也不能绕过 DeepSeek Harness 的 plan / confirmation。

**具体建议：** 对 deeplugin.store，“one click”不是直接执行，而是“一次复制把精确 Registry ID 和 spec 送入 review-first Agent”。CTA 文案应写清“显示安装计划”，不要写“立即一键安装”。

## 跨案例共同规律

六个案例虽然规模和商业模式不同，但共同把页面分成五层：

| 层 | 成熟 Store 的做法 | deeplugin.store 对应实现 |
| --- | --- | --- |
| 意图层 | 搜索、category、task / collection；npm 与 VS Code 都让用户先输入工具或任务词。[npm 搜索](https://docs.npmjs.com/searching-for-and-choosing-packages-to-download/)、[VS Code Marketplace](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace) | 任务问句搜索 + 3 个任务 Pack + 8–12 个 category |
| 选择层 | 首页只给少量榜单、合集、popular/new/spotlight 候选。[Chrome 首页](https://chromewebstore.google.com/)、[Shopify 首页](https://apps.shopify.com/) | 每个 section 6 项以内，完整列表进入 `market.html` / `directories.html` |
| 证明层 | publisher、rating、version、README、gallery、support、provenance 各自承担不同证明。[npm provenance](https://docs.npmjs.com/viewing-package-provenance/)、[Vercel listing requirements](https://vercel.com/docs/integrations/create-integration/submit-integration) | Registry ID、spec、来源 Listing、raw snapshot、日期、版本、媒体 rights note 分栏，不合成“可信分” |
| 行动层 | Install / Add / CLI 与当前上下文紧邻；VS Code 和 Vercel 尤其把动作放进产品工作流。[VS Code Marketplace](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)、[Vercel Integrations](https://vercel.com/docs/integrations) | “复制给 DeepSeek”主 CTA + “自己安装”次 CTA，均展示 review-first 语义 |
| 反馈层 | 真实 install、uninstall、review、update、support 进入排序或运营，但每个平台都有事件与治理。[Chrome Discovery](https://developer.chrome.com/docs/webstore/discovery/)、[Shopify reviews](https://shopify.dev/docs/apps/launch/marketing/manage-app-reviews) | 先用实质更新与来源事实；未来只有 opt-in `install_succeeded` 才能产生本站需求信号 |

因此，deeplugin.store 最该借鉴的不是某一家视觉样式，而是**信息逐层解锁**：首页回答“我能做什么”，结果页回答“有哪些选择”，详情页回答“为什么选它、事实从哪里来”，Agent 回答“将执行什么”，用户最后才批准。

## 首页重构蓝图

### 推荐页面顺序

1. **Header：** Store、Packs、New、Updated、Sources、GitHub；Directory 与 Timeline 放入二级导航。
2. **Hero：** H1 直接问“你想让 DeepSeek 做什么？”；一个任务搜索框；主按钮“复制给 DeepSeek”，次按钮“自己安装”；不再增加解释 Store 是什么的第二段 lede。
3. **Starter Packs：** 只放 3 个任务型 Pack，每个显示任务、2–6 个成员、成员关系和“查看计划”。Chrome 与 Shopify 都用场景合集缩短选择，而 VS Code Extension Pack 会明确展示安装成员。[Chrome Web Store 首页](https://chromewebstore.google.com/)、[Shopify App Store 首页](https://apps.shopify.com/)、[VS Code Marketplace](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)
4. **QA Case：** 保留现有四帧 `ASK -> MATCH -> REVIEW -> USE`，桌面横排、移动端纵排；只用真实 Registry ID、spec 和当前来源事实。若不是实际录屏或实际 transcript，要明确写“流程示例”，不能把模拟结果冒充成功安装证据。
5. **New / Material updates：** 两栏各 6 条，分别链接现有 Atom；互动数字变化不进入 updated。skills.sh 区分 All Time / Trending / Hot，npm 与 VS Code 区分 published / updated，说明时间语义必须显式拆开。[skills.sh 首页](https://www.skills.sh/)、[npm 搜索](https://docs.npmjs.com/searching-for-and-choosing-packages-to-download/)、[VS Code Marketplace](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)
6. **Browse by task / category：** 8–12 个高覆盖 category 或 intent chip；点击进入带 canonical query 的 `market.html`，不在首页继续展开 1,116 个插件。
7. **How evidence works：** 用一张短卡解释 stable ID、exact spec、source claim、raw/date 与 review-first；链接 Sources、Schema、Register，不再在每个 section 重复相同免责声明。
8. **For authors：** “提交插件 / 复制 badge / 获取 launch packet”三个动作；作者分发是 supply loop，不影响收录和排序。
9. **Footer：** Dataset version、最后实质更新、Feed、SQLite、license、privacy、GitHub。

### 首屏文案约束

- H1 只说用户任务，不说项目自我介绍：`你想让 DeepSeek 做什么？ / What should DeepSeek do?`
- 首屏只保留一个说明句：`搜索插件，核对来源，批准后安装。 / Find a plugin, review its source, install after approval.`
- 主 CTA：`复制给 DeepSeek / Copy for DeepSeek`。
- 次 CTA：`自己安装 / Install it yourself`。
- Registry ID、install spec、版本号和 source slug 永不翻译；中英文只翻译解释字段。

Chrome 要求不同 locale 的描述、截图和视频保持功能事实一致，Shopify 也把翻译 listing 视为完整转化面而不是装饰；因此两个 locale 必须从同一 Registry / distribution object 生成，不能各自手写出不同事实。[Chrome localized listing](https://developer.chrome.com/docs/webstore/cws-dashboard-listing/)、[Shopify listing translation](https://shopify.dev/docs/apps/launch/shopify-app-store/best-practices)

### 首页性能与索引约束

- 初步工程目标：`docs/index.html` 初始 HTML 小于 500 KB、首屏后静态候选不超过 24 张卡；完整目录通过明确链接进入专页。该数字是本项目的验收目标，不是外部平台阈值。
- 首页 JSON-LD 只描述首页实际可见的 Store、task collections 和少量展示项；不要把 14,406 个不可见/延后内容塞入一个巨大 `ItemList`。
- 每个 plugin / Pack 详情页继续提供 canonical、可爬链接、真实来源和独立内容。Google 要求 people-first、原创增值、清晰来源与准确标题，并警告大量自动生成、只为搜索流量而存在的页面；SEO 应服务真实决策，而不是制造薄页。[Google people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- 使用用户会搜索的任务词放在 title、H1、link text 与 alt 中，保持内部链接可爬；图片、视频和 structured data 只描述页面真实内容。[Google Search Essentials](https://developers.google.com/search/docs/essentials)
- `SoftwareApplication` structured data 只能使用页面可验证的事实并通过 Rich Results Test；Google 不保证 rich result 展示，也不能用 spammy markup 补救薄内容。[Google SoftwareApplication structured data](https://developers.google.com/search/docs/appearance/structured-data/software-app)

## 建议采用的增长循环

### 循环 A：任务需求 -> 可审查计划 -> 成功使用

`task query -> explainable matches -> plugin detail -> copy Agent request -> plan shown -> user confirmation -> install succeeded -> first successful use`

VS Code 把搜索、详情、安装和使用放在同一产品上下文，Vercel CLI 明确支持 AI agents；这说明 deeplugin.store 的网页成功不应停在搜索 CTR，而应尽可能验证计划是否被正确展示。[VS Code Marketplace](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)、[Vercel Integrations](https://vercel.com/docs/integrations)

执行建议：

- 无接收端阶段：只生成带 `campaign_id`、`locale`、`plugin_id`、`dataset_version` 和 `material_event_id` 的公开 Agent request，不记录用户身份。
- 有合规接收端阶段：将 `qualified_view`、`search_performed`、`result_open`、`copy_agent_request`、`plan_shown`、`install_confirmed`、`install_succeeded`、`first_use_succeeded` 分开；只有最后两项可作为安装/使用信号。
- 关闭遥测时必须完全没有请求；不得发送 prompt、profile、workspace path、用户名、机器 ID、IP 哈希或错误日志正文。

### 循环 B：作者发布 -> Store 事实对象 -> 作者反向分发

`source release / listing -> immutable raw -> stable detail + feed + launch packet -> author badge / copy -> author README or social -> canonical traffic -> task search`

skills.sh 用 badge 把榜单数据带回作者 README，npm 用 package README / homepage / repository 承接判断，GitHub Release 则把 tagged 软件、release notes 和资产包装成可订阅版本。[skills.sh badge](https://www.skills.sh/docs)、[npm README](https://docs.npmjs.com/about-package-readme-files/)、[GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)

执行建议：每个实质更新生成一个 distribution object，统一驱动 Atom、launch packet、作者 badge、GitHub Discussion 草稿、X 中英草稿和中文案例素材；作者是否外发完全自愿，反向链接不影响排名。

### 循环 C：外部案例 -> 可归因入口 -> 下一轮内容

`problem-led case -> channel post -> canonical task / Pack URL -> result -> plan -> aggregate outcome -> next case`

Shopify 不是只测 listing pageview，而是区分 home、search、category、collection、story、app details、Install click 与 install finished；deeplugin.store 可以借用这种 surface / position / funnel 分层，但不能复制 Shopify 的 merchant / shop PII。[Shopify listing traffic](https://shopify.dev/docs/apps/launch/marketing/track-listing-traffic)

建议给每个公开素材保存以下非个人字段：

```text
campaign_id, channel, locale, asset_version, canonical_url,
plugin_or_pack_id, material_event_id, dataset_version,
surface_type, surface_detail, published_at, approval_status
```

### 循环 D：真实反馈 -> 修复 metadata / 使用路径 -> 更好匹配

Shopify 只允许真实安装用户评价，并要求中性询问、禁止激励；Chrome 也把卸载相对下载、onboarding 和易用性纳入发现。这说明反馈应该先修产品与 metadata，而不是直接变成一个无上下文总分。[Shopify reviews](https://shopify.dev/docs/apps/launch/marketing/manage-app-reviews)、[Chrome Discovery](https://developer.chrome.com/docs/webstore/discovery/)

在 deeplugin.store 有能力验证安装资格前，不建立本站评论系统。先把公开 issue、source changelog、inactive state、替代插件和有来源的支持链接结构化，并把失败归类为“spec 无法解析 / plan 不一致 / install 失败 / first use 失败”，保留事实边界。

## 发布渠道选择

### 渠道矩阵

| 渠道 | 最适合发布什么 | 推荐 CTA | 自动化边界 |
| --- | --- | --- | --- |
| deeplugin.store + Atom | 每个 `new` / `updated` 实质事实、稳定详情、Pack、Sources | 查看来源；复制给 Agent | 可随两小时构建自动发布；无实质变化不产生条目 |
| 作者 README / release notes | 单插件稳定链接、badge、精确 spec、变更卡、Pack 入选 | 查看 Store 证据；复制 request | 只生成 launch packet，由作者自愿采用；skills.sh 与 npm 都证明 README / badge 是高意图回流面。[skills.sh 文档](https://www.skills.sh/docs)、[npm README](https://docs.npmjs.com/about-package-readme-files/) |
| GitHub Releases | Store / Market Plugin 可部署版本、schema 或行为变化、release assets | 阅读 release notes；下载/安装版本 | 仅产品 release，不能把每次数据采集当 release；GitHub Release 基于 tag 并支持独立订阅。[GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) |
| GitHub Discussions | 每周 digest、任务 Pack 提案、FAQ、来源更正、重大公告 | 参与讨论；提交来源；查看 Pack | 可生成草稿，人工发布或低频审批发布；Discussion 原生支持公告、问答、投票与置顶。[GitHub Discussions](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/about-discussions) |
| X | 一个明确任务 + 一张独立视觉 + 一个插件/Pack + canonical；重大产品更新 | 打开 task / Pack；复制给 DeepSeek | 默认只生成中英草稿，授权账号人审后发布；API 支持 text、media 与 AI-media disclosure，但有 API 不等于应自动群发。[X Create Posts](https://docs.x.com/x-api/posts/create-post) |
| Hacker News | 可直接试用的 Store / Market Plugin 重大版本、开源技术复盘 | 直接试用；阅读源码；现场提问 | 永不自动提交。Show HN 不接受列表、newsletter、纯 landing page 或普通小版本，也禁止请求点赞；发布者应在场回答。[Show HN](https://news.ycombinator.com/showhn.html) |
| 小红书 / Bilibili / 微信公众号 | 中文任务案例、四帧聊天、1–3 分钟演示、完整教程；重点展示“提出任务 -> 计划 -> 批准 -> 使用” | 打开中文 task / Pack；复制中文 request | 作为本项目的人工内容策略，不宣称平台推荐机制；不自动发帖、不绕过登录/风控。视频可被搜索并复用于文档与社交的格式依据来自 Shopify 官方营销指南。[Shopify app marketing](https://shopify.dev/docs/apps/launch/marketing) |
| Reddit / Discord / 技术社区 | 回答一个已经存在的问题、公开实现细节、征求反馈；链接只作为答案证据 | 解决问题；查看可复现步骤 | 人工、answer-first；不跨社区复制同一广告。Shopify 官方同样建议通过持续对话先提供价值，并警告自我推广可能构成 spam。[Shopify app marketing](https://shopify.dev/docs/apps/launch/marketing) |
| Google Search | 稳定 plugin / Pack / task / source 页面、真实 changelog、带来源的案例 | 进入与查询意图完全一致的页面 | 站内自动生成，Search Console 操作人工；不得用批量薄页、伪新日期或关键词堆砌做增长。[Google people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)、[Google Search Essentials](https://developers.google.com/search/docs/essentials) |

### 推荐节奏

| 时间尺度 | 自动产物 | 外部动作 |
| --- | --- | --- |
| 每两小时 | raw / SQLite / index / Store projection / material Feed / launch packet 草稿 | 不发外部帖 |
| 每日 | 合并当天实质更新，生成候选案例和渠道草稿 | 仅在确有独立价值时人工批准 0–1 条 |
| 每周 | 新插件、实质更新、任务 Pack、来源变动 digest | 1 个 GitHub Discussion；从中选择最多 2 个 X 或中文案例，不重复同一文案 |
| 产品里程碑 | 可直接试用的 Store / Market Plugin release、完整技术说明、演示 | GitHub Release；符合条件时人工 Show HN；中文与 X 各自重写 |

数字是本项目初始运营上限，不是外部平台官方配额。目标是让每一条外发内容都有独立任务、独立事实和独立 canonical，而不是提高频次。

## 什么可以直接借鉴，什么必须拒绝

### 可直接借鉴

1. **搜索优先，完整目录后置。** npm、skills.sh 与 VS Code 都把 query 放在主要发现路径；Chrome 与 Shopify 再用有限合集补足用户不知道搜什么的场景。[npm 搜索](https://docs.npmjs.com/searching-for-and-choosing-packages-to-download/)、[skills.sh](https://www.skills.sh/)、[VS Code Marketplace](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)、[Chrome 首页](https://chromewebstore.google.com/)
2. **稳定身份、版本、变更和弃用是一套。** npm 的 `name + version`、provenance 与 deprecation，VS Code 的 `publisher.extension` 和 changelog 都证明：可安装对象必须能精确指认、更新和退出。[npm package.json](https://docs.npmjs.com/cli/v11/configuring-npm/package-json)、[npm deprecation](https://docs.npmjs.com/deprecating-and-undeprecating-packages-or-package-versions/)、[VS Code publishing](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
3. **主视觉应该解释结果，不只是装饰。** Chrome、Shopify、Vercel 都要求高质量截图/视频或 gallery，并把它们用于发现、详情和 OG；deeplugin.store 应优先使用有 rights note 的真实媒体，否则生成确定性文字卡。[Chrome Listing](https://developer.chrome.com/docs/webstore/cws-dashboard-listing/)、[Shopify best practices](https://shopify.dev/docs/apps/launch/shopify-app-store/best-practices)、[Vercel approval checklist](https://vercel.com/docs/integrations/create-integration/approval-checklist)
4. **每个发现面都要可归因，但不必追踪个人。** Shopify 的 `surface_type / detail / position` 是有用的数据模型；deeplugin.store 可把这些字段写入公开 campaign object，而不复制 shop/user 标识。[Shopify listing traffic](https://shopify.dev/docs/apps/launch/marketing/track-listing-traffic)
5. **外发内容从真实任务出发。** Shopify 的视频、community 与 case-study 路径，以及 Show HN 的“可直接试用”规则，都反对只发目录链接。[Shopify app marketing](https://shopify.dev/docs/apps/launch/marketing)、[Show HN](https://news.ycombinator.com/showhn.html)

### 必须拒绝

1. **拒绝伪 installs、伪 reviews、伪 Trending。** 没有成功安装事件就只显示来源平台自己的指标；Shopify 对评价资格和反激励有完整治理，Chrome 的发现还需要 downloads/uninstalls 与真实体验，不能只抄 UI 标签。[Shopify reviews](https://shopify.dev/docs/apps/launch/marketing/manage-app-reviews)、[Chrome Discovery](https://developer.chrome.com/docs/webstore/discovery/)
2. **拒绝把来源 claim 包装成本站背书。** npm provenance 只证明来源和发布链，也不保证无恶意代码；deeplugin.store 的 source-declared `verified` 更不能叫“安全认证”。[npm provenance](https://docs.npmjs.com/generating-provenance-statements/)
3. **拒绝网页直接静默安装。** VS Code / Vercel 的直接安装依赖客户端和平台控制；本站必须继续通过 Agent 展示精确命令与计划，用户明确批准后才执行。[VS Code Marketplace](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)、[Vercel approval checklist](https://vercel.com/docs/integrations/create-integration/approval-checklist)
4. **拒绝把 14,406 条目录记录当首页内容。** Chrome 与 Shopify 的首页是有限策展，完整浏览由搜索、category 和详情承接。[Chrome 首页](https://chromewebstore.google.com/)、[Shopify 首页](https://apps.shopify.com/)
5. **拒绝薄页 SEO 与伪更新时间。** Google 明确警告为搜索流量批量生产内容、用自动化覆盖大量主题、没有实质变化却修改日期；每个索引页必须有用户可见的独特任务、来源或变更价值。[Google people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
6. **拒绝让两小时采集节奏决定社交发布节奏。** Show HN 排除普通小更新，GitHub Discussion 适合低频公告与持续对话；外发需要实质阈值和人工责任人。[Show HN](https://news.ycombinator.com/showhn.html)、[GitHub Discussions](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/about-discussions)

## 90 天建议顺序

| 时间 | 交付 | 验收 |
| --- | --- | --- |
| 第 1–14 天 | 首页减重：去掉 14,406 卡片投影；首屏一个 search、两个 CTA；3 个 task Pack；保留四帧 QA；New / Updated 各 6 条 | 初始 HTML < 500 KB；首屏中英文事实一致；完整目录仍可从专页访问；无新遥测 |
| 第 15–30 天 | 每个首页 section / card / launch packet 加公开 campaign metadata；Pack / task canonical；逐插件确定性 OG 或 rights-cleared media | 同一 distribution object 在页面、Feed、草稿中的 ID、日期、版本一致；无 PII |
| 第 31–60 天 | 作者 launch packet、README badge、每周 GitHub Discussion digest；X / 中文案例人工试运行 | 至少 20 位多插件作者收到可选素材；每条外发指向独立 task / Pack；无重复群发 |
| 第 61–90 天 | 仅在隐私与治理完成后试点 opt-in `install_succeeded` 回执；固定任务查询回归与漏斗诊断 | copy、plan、confirm、success 不混用；关闭遥测无请求；异常事件不改公开排序 |

## 最强建议

先把 `docs/index.html` 从 16.56 MB、14,406 张卡片的聚合页缩成一个 Store router，再开始扩大分发。Chrome、Shopify、VS Code、npm、skills.sh 和 Vercel 的共同优势不是“首页更漂亮”，而是用户能在很少信息里完成一次明确决策；deeplugin.store 已经有稳定 ID、精确 spec、Feed、launch packet 和 review-first Market Plugin，当前成本最低、影响最大的增长动作，就是让这些能力成为首页唯一主线。[Chrome Web Store 首页](https://chromewebstore.google.com/)、[Shopify App Store 首页](https://apps.shopify.com/)、[VS Code Marketplace](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)、[npm 搜索](https://docs.npmjs.com/searching-for-and-choosing-packages-to-download/)、[skills.sh](https://www.skills.sh/)、[Vercel Marketplace](https://vercel.com/marketplace)

## 官方一手来源索引

- skills.sh：[首页](https://www.skills.sh/)、[文档](https://www.skills.sh/docs)、[Packs](https://www.skills.sh/docs/packs)、[官方 CLI 源码](https://github.com/vercel-labs/skills)
- VS Code：[Marketplace 使用文档](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)、[发布文档](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
- Chrome Web Store：[首页](https://chromewebstore.google.com/)、[Discovery](https://developer.chrome.com/docs/webstore/discovery/)、[Listing](https://developer.chrome.com/docs/webstore/cws-dashboard-listing/)、[Best listing](https://developer.chrome.com/docs/webstore/best-listing/)
- npm：[搜索与选择 package](https://docs.npmjs.com/searching-for-and-choosing-packages-to-download/)、[`package.json`](https://docs.npmjs.com/cli/v11/configuring-npm/package-json)、[README](https://docs.npmjs.com/about-package-readme-files/)、[生成 provenance](https://docs.npmjs.com/generating-provenance-statements/)、[查看 provenance](https://docs.npmjs.com/viewing-package-provenance/)、[deprecation](https://docs.npmjs.com/deprecating-and-undeprecating-packages-or-package-versions/)
- Shopify：[App Store 首页](https://apps.shopify.com/)、[best practices](https://shopify.dev/docs/apps/launch/shopify-app-store/best-practices)、[Built for Shopify](https://shopify.dev/docs/apps/launch/built-for-shopify)、[marketing](https://shopify.dev/docs/apps/launch/marketing)、[traffic attribution](https://shopify.dev/docs/apps/launch/marketing/track-listing-traffic)、[reviews](https://shopify.dev/docs/apps/launch/marketing/manage-app-reviews)
- Vercel：[Marketplace](https://vercel.com/marketplace)、[Integrations](https://vercel.com/docs/integrations)、[listing requirements](https://vercel.com/docs/integrations/create-integration/submit-integration)、[approval checklist](https://vercel.com/docs/integrations/create-integration/approval-checklist)、[Marketplace product](https://vercel.com/docs/integrations/create-integration/marketplace-product)
- 分发与搜索：[GitHub Discussions](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/about-discussions)、[GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)、[Show HN](https://news.ycombinator.com/showhn.html)、[X Create Posts](https://docs.x.com/x-api/posts/create-post)、[Google people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)、[Google Search Essentials](https://developers.google.com/search/docs/essentials)、[SoftwareApplication structured data](https://developers.google.com/search/docs/appearance/structured-data/software-app)
