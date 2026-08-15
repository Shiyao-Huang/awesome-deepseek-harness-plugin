# DeepSeek Harness Plugin Aggregator

> 一个可重复更新的公开资料聚合体：仓库、插件、索引、文章、帖子、图片缩略图和视频链接。原始观测保留在 `data/raw/`，SQLite 是可查询的派生索引。

当前数据集版本：**v20260815T075255Z**，完成时间：**2026-08-15T07:52:58Z**。共 **896** 条去重记录，覆盖 **13** 个平台，外部媒体资产 **646** 条。

## 三句话结论

1. 传播核心仍是 GitHub：官方仓库与一批插件/桌面端/目录项目在短时间内形成明显的生态簇。
2. 讨论扩散到 HN、X、小红书和 YouTube；互动指标必须按平台分别解释，不能把星标、点赞、观看数直接相加。
3. 本项目把“可验证来源 + 观测时间 + 原始快照 + 指标历史”作为第一等数据，方便之后持续更新和回溯。

## 导航

- [按来源浏览](timeline.md)
- [按主题归类](categories.md)
- [上游源仓库与插件关系](sources.md)
- [可视化报告](report.html)
- [采集与更新说明](../README.md#更新)

## 来源分布

| 平台 | 去重记录 | 采集方式 |
| --- | ---: | --- |
| github | 687 | public REST API |
| hacker_news | 89 | Algolia public search API |
| x | 43 | ego-browser visible DOM |
| xiaohongshu | 25 | ego-browser visible DOM |
| web | 22 | public page metadata |
| youtube | 13 | ego-browser visible DOM |
| bilibili | 6 | public web metadata API |
| reddit | 5 | ego-browser visible DOM |
| linuxdo | 2 | ego-browser visible DOM |
| official | 1 | ego-browser visible DOM |
| v2ex | 1 | ego-browser visible DOM |
| wechat | 1 | ego-browser visible DOM |
| weibo | 1 | ego-browser visible DOM |

## 主题分布

| 分类 | 记录 | 带媒体 |
| --- | ---: | ---: |
| core-and-ecosystem | 557 | 69 |
| index-and-marketplace | 112 | 16 |
| ui-and-desktop | 97 | 2 |
| operations-and-safety | 54 | 1 |
| multimedia-and-vision | 36 | 2 |
| docs-and-learning | 25 | 4 |
| agents-and-orchestration | 15 | 0 |

## 高互动/高关注记录

| 平台 | 标题 | 作者 | 指标 | 分类 |
| --- | --- | --- | --- | --- |
| github | [ollama/ollama](https://github.com/ollama/ollama) | ollama | 178,533 ★, 17,407 forks | core-and-ecosystem |
| github | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | Graphify-Labs | 106,451 ★, 10,360 forks | core-and-ecosystem |
| github | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | deepseek-ai | 103,427 ★, 9,847 forks | core-and-ecosystem |
| github | [nexu-io/open-design](https://github.com/nexu-io/open-design) | nexu-io | 86,541 ★, 10,091 forks | ui-and-desktop |
| github | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | bytedance | 80,027 ★, 10,955 forks | agents-and-orchestration |
| github | [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) | shareAI-lab | 74,270 ★, 12,028 forks | core-and-ecosystem |
| github | [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | shanraisshan | 64,487 ★, 6,406 forks | core-and-ecosystem |
| github | [rust-unofficial/awesome-rust](https://github.com/rust-unofficial/awesome-rust) | rust-unofficial | 58,839 ★, 3,538 forks | index-and-marketplace |
| github | [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) | CherryHQ | 50,494 ★, 4,782 forks | core-and-ecosystem |
| github | [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) | diegosouzapw | 48,177 ★, 6,538 forks | ui-and-desktop |
| github | [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) | hugohe3 | 46,936 ★, 3,809 forks | core-and-ecosystem |
| github | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | Imbad0202 | 42,531 ★, 3,387 forks | core-and-ecosystem |
| youtube | [DeepSeek Harness: The End of Claude Code?](https://www.youtube.com/watch?v=qg9EyGOZd9U) | NeuralNine | 39,000 views | core-and-ecosystem |
| github | [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) | HKUDS | 30,875 ★, 5,009 forks | core-and-ecosystem |
| github | [BigPizzaV3/CodexPlusPlus](https://github.com/BigPizzaV3/CodexPlusPlus) | BigPizzaV3 | 28,942 ★, 1,837 forks | core-and-ecosystem |
| github | [Hannibal046/Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM) | Hannibal046 | 27,263 ★, 2,671 forks | index-and-marketplace |
| github | [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory) | rohitg00 | 27,028 ★, 2,307 forks | core-and-ecosystem |
| github | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | OthmanAdi | 26,167 ★, 2,188 forks | index-and-marketplace |
| github | [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi) | can1357 | 24,889 ★, 2,388 forks | agents-and-orchestration |
| github | [micro/go-micro](https://github.com/micro/go-micro) | micro | 23,013 ★, 2,414 forks | core-and-ecosystem |
