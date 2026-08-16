# DeepSeek Harness Plugin Aggregator

> 一个可重复更新的公开资料聚合体：仓库、插件、索引、文章、帖子、图片缩略图和视频链接。原始观测保留在 `data/raw/`，SQLite 是可查询的派生索引。

当前数据集版本：**v20260816T185105Z**，完成时间：**2026-08-16T18:51:06Z**。共 **14,459** 条去重记录，覆盖 **14** 个平台，外部媒体资产 **1,255** 条。

## 三句话结论

1. 传播核心仍是 GitHub：官方仓库与一批插件/桌面端/目录项目在短时间内形成明显的生态簇。
2. 讨论扩散到 HN、X、小红书和 YouTube；互动指标必须按平台分别解释，不能把星标、点赞、观看数直接相加。
3. 本项目把“可验证来源 + 观测时间 + 原始快照 + 指标历史”作为第一等数据，方便之后持续更新和回溯。

## 导航

- [按来源浏览](timeline.md)
- [按主题归类](categories.md)
- [价值衡量矩阵](value-matrix.md)
- [可视化报告](report.html)
- [趋势与增速](trends.md)
- [采集与更新说明](../README.md#更新)

## 来源分布

| 平台 | 去重记录 | 采集方式 |
| --- | ---: | --- |
| github | 13,977 | public REST API |
| xiaohongshu | 157 | ego-browser visible DOM |
| hacker_news | 103 | Algolia public search API |
| x | 90 | ego-browser visible DOM |
| reddit | 51 | ego-browser visible DOM |
| youtube | 29 | ego-browser visible DOM |
| web | 21 | public page metadata |
| bilibili | 18 | public web metadata API |
| wechat | 7 | ego-browser visible DOM |
| linuxdo | 2 | ego-browser visible DOM |
| official | 1 | ego-browser visible DOM |
| v2ex | 1 | ego-browser visible DOM |
| weibo | 1 | ego-browser visible DOM |
| zhihu | 1 | ego-browser visible DOM |

## 主题分布

| 分类 | 记录 | 带媒体 |
| --- | ---: | ---: |
| deepseek-harness-forks | 12,352 | 0 |
| core-and-ecosystem | 1,465 | 240 |
| index-and-marketplace | 199 | 43 |
| ui-and-desktop | 180 | 6 |
| operations-and-safety | 114 | 1 |
| multimedia-and-vision | 84 | 7 |
| docs-and-learning | 41 | 9 |
| agents-and-orchestration | 23 | 4 |
| ecosystem | 1 | 1 |

## 价值衡量摘要

价值分数用于安排复核和进一步研究，不是安全、质量或销量背书。

| 平台 | 记录 | value | band | confidence | 分类 |
| --- | --- | ---: | :---: | ---: | --- |
| github | [deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 78.86 | B | 100.00 | core-and-ecosystem |
| github | [dsh-web-ui#packages/dsh-web-ui-all](https://github.com/zhu1090093659/dsh-web-ui) | 77.83 | B | 100.00 | ui-and-desktop |
| github | [modlens](https://github.com/liustack/modlens) | 77.22 | B | 100.00 | multimedia-and-vision |
| github | [treg](https://github.com/superdesigndev/treg) | 76.89 | B | 100.00 | operations-and-safety |
| github | [DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) | 76.60 | B | 100.00 | ui-and-desktop |
| github | [dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI) | 76.52 | B | 100.00 | ui-and-desktop |
| github | [OpenViking#examples/dsh-memory-plugin](https://github.com/volcengine/OpenViking) | 76.11 | B | 75.00 | core-and-ecosystem |
| github | [dsh-deep-whale#maid-atelier](https://github.com/Small-tailqwq/dsh-deep-whale) | 75.94 | B | 100.00 | core-and-ecosystem |
| github | [Aegis](https://github.com/GanyuanRan/Aegis) | 75.85 | B | 100.00 | core-and-ecosystem |
| github | [dsh-market](https://github.com/dsh-market/dsh-market) | 74.82 | B | 100.00 | core-and-ecosystem |

## 高互动/高关注记录

| 平台 | 标题 | 作者 | 指标 | 分类 |
| --- | --- | --- | --- | --- |
| github | [ollama/ollama](https://github.com/ollama/ollama) | ollama | 178,698 ★, 17,434 forks | core-and-ecosystem |
| github | [deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | deepseek-ai | 129,904 ★, 12,975 forks | core-and-ecosystem |
| github | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | Graphify-Labs | 107,033 ★, 10,408 forks | core-and-ecosystem |
| github | [open-design](https://github.com/nexu-io/open-design) | nexu-io | 87,438 ★, 10,149 forks | core-and-ecosystem |
| github | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | bytedance | 80,094 ★, 10,965 forks | agents-and-orchestration |
| github | [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) | shareAI-lab | 74,377 ★, 12,042 forks | core-and-ecosystem |
| github | [headroom](https://github.com/headroomlabs-ai/headroom) | headroomlabs-ai | 66,438 ★, 5,097 forks | core-and-ecosystem |
| github | [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | shanraisshan | 64,569 ★, 6,412 forks | core-and-ecosystem |
| github | [rust-unofficial/awesome-rust](https://github.com/rust-unofficial/awesome-rust) | rust-unofficial | 58,852 ★, 3,542 forks | index-and-marketplace |
| github | [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) | CherryHQ | 50,551 ★, 4,791 forks | core-and-ecosystem |
| github | [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) | diegosouzapw | 49,056 ★, 6,691 forks | ui-and-desktop |
| github | [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) | hugohe3 | 47,250 ★, 3,830 forks | core-and-ecosystem |
| github | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | Imbad0202 | 42,696 ★, 3,398 forks | core-and-ecosystem |
| youtube | [DeepSeek Harness: The End of Claude Code?](https://www.youtube.com/watch?v=qg9EyGOZd9U) | NeuralNine | 42,000 views | docs-and-learning |
| github | [amruthpillai/reactive-resume](https://github.com/amruthpillai/reactive-resume) | amruthpillai | 40,557 ★, 4,598 forks | core-and-ecosystem |
| youtube | [DeepSeek Harness 正式发布！ 开源一天狂揽 6.8 万星！V4 Pro 模型低调上线，AI Agent 部署与实测 \| 零度解说](https://www.youtube.com/watch?v=5G_afoTB1gs) | 零度解说 | 37,000 views | core-and-ecosystem |
| github | [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) | HKUDS | 31,023 ★, 5,033 forks | core-and-ecosystem |
| github | [BigPizzaV3/CodexPlusPlus](https://github.com/BigPizzaV3/CodexPlusPlus) | BigPizzaV3 | 29,033 ★, 1,844 forks | core-and-ecosystem |
| github | [OpenViking#examples/dsh-memory-plugin](https://github.com/volcengine/OpenViking) | volcengine | 28,652 ★, 2,264 forks | core-and-ecosystem |
| github | [Hannibal046/Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM) | Hannibal046 | 27,269 ★, 2,672 forks | index-and-marketplace |
