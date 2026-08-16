# DeepSeek Harness Plugin Aggregator

> 一个可重复更新的公开资料聚合体：仓库、插件、索引、文章、帖子、图片缩略图和视频链接。原始观测保留在 `data/raw/`，SQLite 是可查询的派生索引。

当前数据集版本：**v20260816T002558Z**，完成时间：**2026-08-16T00:26:44Z**。共 **12,880** 条去重记录，覆盖 **14** 个平台，外部媒体资产 **873** 条。

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
| github | 12,541 | public REST API |
| hacker_news | 101 | Algolia public search API |
| x | 77 | ego-browser visible DOM |
| xiaohongshu | 51 | ego-browser visible DOM |
| reddit | 35 | ego-browser visible DOM |
| youtube | 28 | ego-browser visible DOM |
| web | 21 | public page metadata |
| bilibili | 18 | public web metadata API |
| linuxdo | 2 | ego-browser visible DOM |
| wechat | 2 | ego-browser visible DOM |
| official | 1 | ego-browser visible DOM |
| v2ex | 1 | ego-browser visible DOM |
| weibo | 1 | ego-browser visible DOM |
| zhihu | 1 | ego-browser visible DOM |

## 主题分布

| 分类 | 记录 | 带媒体 |
| --- | ---: | ---: |
| deepseek-harness-forks | 11,254 | 0 |
| core-and-ecosystem | 964 | 135 |
| ui-and-desktop | 222 | 4 |
| index-and-marketplace | 179 | 34 |
| operations-and-safety | 101 | 1 |
| multimedia-and-vision | 85 | 6 |
| docs-and-learning | 40 | 7 |
| agents-and-orchestration | 35 | 3 |

## 价值衡量摘要

价值分数用于安排复核和进一步研究，不是安全、质量或销量背书。

| 平台 | 记录 | value | band | confidence | 分类 |
| --- | --- | ---: | :---: | ---: | --- |
| github | [zhu1090093659/dsh-web-ui](https://github.com/zhu1090093659/dsh-web-ui) | 79.95 | B | 100.00 | ui-and-desktop |
| github | [liustack/modlens](https://github.com/liustack/modlens) | 79.37 | B | 100.00 | multimedia-and-vision |
| github | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 78.65 | B | 100.00 | core-and-ecosystem |
| github | [sandbaseai/sandbase-harness](https://github.com/sandbaseai/sandbase-harness) | 77.44 | B | 100.00 | operations-and-safety |
| github | [Anionex/dsh-vision-toolkit](https://github.com/Anionex/dsh-vision-toolkit) | 76.92 | B | 100.00 | ui-and-desktop |
| github | [ccch1mneyyy/dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI) | 76.19 | B | 100.00 | ui-and-desktop |
| github | [omdsh-dev/DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) | 76.19 | B | 100.00 | ui-and-desktop |
| github | [Small-tailqwq/dsh-deep-whale](https://github.com/Small-tailqwq/dsh-deep-whale) | 75.64 | B | 100.00 | core-and-ecosystem |
| github | [superdesigndev/superdesign-skill](https://github.com/superdesigndev/superdesign-skill) | 75.36 | B | 100.00 | core-and-ecosystem |
| github | [Lum1104/dsh-browser](https://github.com/Lum1104/dsh-browser) | 75.30 | B | 100.00 | ui-and-desktop |

## 高互动/高关注记录

| 平台 | 标题 | 作者 | 指标 | 分类 |
| --- | --- | --- | --- | --- |
| github | [ollama/ollama](https://github.com/ollama/ollama) | ollama | 178,607 ★, 17,419 forks | core-and-ecosystem |
| github | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | deepseek-ai | 115,046 ★, 11,209 forks | core-and-ecosystem |
| github | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | Graphify-Labs | 106,719 ★, 10,379 forks | core-and-ecosystem |
| github | [nexu-io/open-design](https://github.com/nexu-io/open-design) | nexu-io | 86,927 ★, 10,115 forks | ui-and-desktop |
| github | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | bytedance | 80,053 ★, 10,958 forks | agents-and-orchestration |
| github | [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) | shareAI-lab | 74,307 ★, 12,032 forks | core-and-ecosystem |
| github | [headroom](https://github.com/headroomlabs-ai/headroom) | headroomlabs-ai | 66,438 ★, 5,097 forks | core-and-ecosystem |
| github | [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | shanraisshan | 64,519 ★, 6,411 forks | core-and-ecosystem |
| github | [rust-unofficial/awesome-rust](https://github.com/rust-unofficial/awesome-rust) | rust-unofficial | 58,843 ★, 3,540 forks | index-and-marketplace |
| github | [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) | CherryHQ | 50,519 ★, 4,783 forks | core-and-ecosystem |
| github | [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) | diegosouzapw | 48,577 ★, 6,612 forks | ui-and-desktop |
| github | [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) | hugohe3 | 47,062 ★, 3,814 forks | core-and-ecosystem |
| github | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | Imbad0202 | 42,595 ★, 3,392 forks | core-and-ecosystem |
| youtube | [DeepSeek Harness: The End of Claude Code?](https://www.youtube.com/watch?v=qg9EyGOZd9U) | NeuralNine | 42,000 views | docs-and-learning |
| youtube | [DeepSeek Harness 正式发布！ 开源一天狂揽 6.8 万星！V4 Pro 模型低调上线，AI Agent 部署与实测 \| 零度解说](https://www.youtube.com/watch?v=5G_afoTB1gs) | 零度解说 | 37,000 views | core-and-ecosystem |
| github | [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) | HKUDS | 30,927 ★, 5,016 forks | core-and-ecosystem |
| github | [BigPizzaV3/CodexPlusPlus](https://github.com/BigPizzaV3/CodexPlusPlus) | BigPizzaV3 | 28,980 ★, 1,840 forks | core-and-ecosystem |
| github | [Hannibal046/Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM) | Hannibal046 | 27,266 ★, 2,672 forks | index-and-marketplace |
| github | [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory) | rohitg00 | 27,049 ★, 2,310 forks | core-and-ecosystem |
| github | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | OthmanAdi | 26,180 ★, 2,189 forks | index-and-marketplace |
