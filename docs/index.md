# DeepSeek Harness Plugin Aggregator

> 一个可重复更新的公开资料聚合体：仓库、插件、索引、文章、帖子、图片缩略图和视频链接。原始观测保留在 `data/raw/`，SQLite 是可查询的派生索引。

当前快照：**2026-08-15T06:37:51Z**。共 **581** 条去重记录，覆盖 **14** 个平台，外部媒体资产 **550** 条。

## 三句话结论

1. 传播核心仍是 GitHub：官方仓库与一批插件/桌面端/目录项目在短时间内形成明显的生态簇。
2. 讨论扩散到 HN、X、小红书和 YouTube；互动指标必须按平台分别解释，不能把星标、点赞、观看数直接相加。
3. 本项目把“可验证来源 + 观测时间 + 原始快照 + 指标历史”作为第一等数据，方便之后持续更新和回溯。

## 导航

- [按来源浏览](timeline.md)
- [按主题归类](categories.md)
- [可视化报告](report.html)
- [采集与更新说明](../README.md#更新)

## 来源分布

| 平台 | 去重记录 | 采集方式 |
| --- | ---: | --- |
| github | 435 | public REST API |
| x | 43 | ego-browser visible DOM |
| hacker_news | 26 | Algolia public search API |
| xiaohongshu | 25 | ego-browser visible DOM |
| web | 21 | public page metadata |
| youtube | 13 | ego-browser visible DOM |
| bilibili | 6 | public web metadata API |
| reddit | 5 | ego-browser visible DOM |
| linuxdo | 2 | ego-browser visible DOM |
| official | 1 | ego-browser visible DOM |
| v2ex | 1 | ego-browser visible DOM |
| wechat | 1 | ego-browser visible DOM |
| weibo | 1 | ego-browser visible DOM |
| zhihu | 1 | ego-browser visible DOM |

## 主题分布

| 分类 | 记录 | 带媒体 |
| --- | ---: | ---: |
| core-and-ecosystem | 350 | 69 |
| ui-and-desktop | 79 | 2 |
| index-and-marketplace | 62 | 16 |
| operations-and-safety | 38 | 1 |
| multimedia-and-vision | 25 | 2 |
| docs-and-learning | 20 | 4 |
| agents-and-orchestration | 7 | 0 |

## 高互动/高关注记录

| 平台 | 标题 | 作者 | 指标 | 分类 |
| --- | --- | --- | --- | --- |
| github | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | deepseek-ai | 101,440 ★, 9,596 forks | core-and-ecosystem |
| github | [nexu-io/open-design](https://github.com/nexu-io/open-design) | nexu-io | 86,488 ★, 10,085 forks | ui-and-desktop |
| github | [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) | CherryHQ | 50,491 ★, 4,781 forks | core-and-ecosystem |
| youtube | [DeepSeek Harness: The End of Claude Code?](https://www.youtube.com/watch?v=qg9EyGOZd9U) | NeuralNine | 39,000 views | core-and-ecosystem |
| github | [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill) | titanwings | 22,153 ★, 2,045 forks | core-and-ecosystem |
| youtube | [DeepSeek Harness - Its a Big Deal!](https://www.youtube.com/watch?v=NPO2CwHnfmI) | Prompt Engineering | 20,000 views | core-and-ecosystem |
| x | [DeepSeek @deepseek_ai DeepSeek Harness v0.1 is now available in Developer Preview! We’re opening it up to developers building agent harnesse](https://x.com/deepseek_ai/status/2087887408440164663) |  | 18,976 ♥, 3,727,518 views, 717 replies | index-and-marketplace |
| github | [liyupi/ai-guide](https://github.com/liyupi/ai-guide) | liyupi | 18,404 ★, 2,094 forks | docs-and-learning |
| youtube | [实测DeepSeek Harness从基础到高级用法：WebUI、插件系统与任务分支](https://www.youtube.com/watch?v=Aqn7EP8shJw) | AI超元域 | 16,000 views | core-and-ecosystem |
| github | [tt-a1i/archify](https://github.com/tt-a1i/archify) | tt-a1i | 12,672 ★, 940 forks | docs-and-learning |
| bilibili | [【热门AI鉴定】DeepSeek Harness是什么？强在哪里？Harness实测效果如何？一口气搞懂！](https://www.bilibili.com/video/BV11CgF6uE4k) | Git源宝 | 12,206 ♥, 446,982 views, 656 replies, 7,015 favorites, 1,927 shares, 2,764 coins, 252 danmaku | core-and-ecosystem |
| youtube | [DeepSeek Just Dropped Its Own Harness… And It’s FAST!](https://www.youtube.com/watch?v=yiXSK7WvSv0) | Tech2WiLD | 5,188 views | core-and-ecosystem |
| youtube | [Deepseek Harness: Everything is a plugin](https://www.youtube.com/watch?v=xe-aHJLC5UU) | DevsKingdom | 4,940 views | docs-and-learning |
| github | [Devin-AXIS/iPolloWork](https://github.com/Devin-AXIS/iPolloWork) | Devin-AXIS | 4,045 ★, 812 forks | multimedia-and-vision |
| github | [crafter-station/petdex](https://github.com/crafter-station/petdex) | crafter-station | 3,803 ★, 181 forks | core-and-ecosystem |
| youtube | [DeepSeek Harness: Free Claude Code Rival Hits 24k Stars Day 1](https://www.youtube.com/watch?v=k2hi16y67Jo) | Prism Labs | 3,550 views | core-and-ecosystem |
| github | [strukto-ai/mirage](https://github.com/strukto-ai/mirage) | strukto-ai | 3,422 ★, 255 forks | core-and-ecosystem |
| youtube | [DeepSeek&#x27;s Latest Open-Source Project: DeepSeek Harness Is Officially Here](https://www.youtube.com/watch?v=CAb1PaVBCEM) | 鲲鹏Talk | 3,294 views | core-and-ecosystem |
| x | [Tianyi Cui @tianyi · Aug 1 如果你是 Agent Harness 相关开源项目的开发者，希望参加 DeepSeek Harness 的内测，可以回复或私信联系我。请附上 GitHub id 以及开源代表作。 1.2K 517 3K 981K](https://x.com/tianyi/status/2083519855203078320) |  | 3,071 ♥, 981,358 views, 1,218 replies | index-and-marketplace |
| github | [anywhere-labs/deepseek-harness-desktop](https://github.com/anywhere-labs/deepseek-harness-desktop) | anywhere-labs | 2,989 ★, 142 forks | ui-and-desktop |
