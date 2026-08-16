# DeepSeek Harness Plugin Aggregator

> 一个可重复更新的公开资料聚合体：仓库、插件、索引、文章、帖子、图片缩略图和视频链接。原始观测保留在 `data/raw/`，SQLite 是可查询的派生索引。

当前数据集版本：**v20260816T055031Z**，完成时间：**2026-08-16T05:50:31Z**。共 **13,045** 条去重记录，覆盖 **14** 个平台，外部媒体资产 **1,068** 条。

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
| github | 12,625 | public REST API |
| hacker_news | 102 | Algolia public search API |
| xiaohongshu | 102 | ego-browser visible DOM |
| x | 90 | ego-browser visible DOM |
| reddit | 47 | ego-browser visible DOM |
| youtube | 28 | ego-browser visible DOM |
| web | 21 | public page metadata |
| bilibili | 18 | public web metadata API |
| wechat | 6 | ego-browser visible DOM |
| linuxdo | 2 | ego-browser visible DOM |
| official | 1 | ego-browser visible DOM |
| v2ex | 1 | ego-browser visible DOM |
| weibo | 1 | ego-browser visible DOM |
| zhihu | 1 | ego-browser visible DOM |

## 主题分布

| 分类 | 记录 | 带媒体 |
| --- | ---: | ---: |
| deepseek-harness-forks | 11,254 | 0 |
| core-and-ecosystem | 1,215 | 187 |
| index-and-marketplace | 176 | 40 |
| ui-and-desktop | 164 | 5 |
| operations-and-safety | 102 | 1 |
| multimedia-and-vision | 73 | 6 |
| docs-and-learning | 40 | 9 |
| agents-and-orchestration | 21 | 4 |

## 价值衡量摘要

价值分数用于安排复核和进一步研究，不是安全、质量或销量背书。

| 平台 | 记录 | value | band | confidence | 分类 |
| --- | --- | ---: | :---: | ---: | --- |
| github | [deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 78.71 | B | 100.00 | core-and-ecosystem |
| github | [dsh-web-ui#packages/dsh-web-ui-all](https://github.com/zhu1090093659/dsh-web-ui) | 77.55 | B | 100.00 | ui-and-desktop |
| github | [modlens](https://github.com/liustack/modlens) | 76.96 | B | 100.00 | multimedia-and-vision |
| github | [DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) | 76.32 | B | 100.00 | ui-and-desktop |
| github | [dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI) | 76.28 | B | 100.00 | ui-and-desktop |
| github | [dsh-deep-whale#maid-atelier](https://github.com/Small-tailqwq/dsh-deep-whale) | 75.70 | B | 100.00 | core-and-ecosystem |
| github | [treg](https://github.com/superdesigndev/treg) | 75.37 | B | 100.00 | operations-and-safety |
| github | [sandbase-harness](https://github.com/sandbaseai/sandbase-harness) | 74.94 | B | 100.00 | core-and-ecosystem |
| github | [dsh-vision-toolkit](https://github.com/Anionex/dsh-vision-toolkit) | 74.48 | B | 100.00 | multimedia-and-vision |
| github | [dsh-ads](https://github.com/Nagi-ovo/dsh-ads) | 74.39 | B | 100.00 | core-and-ecosystem |

## 高互动/高关注记录

| 平台 | 标题 | 作者 | 指标 | 分类 |
| --- | --- | --- | --- | --- |
| github | [ollama/ollama](https://github.com/ollama/ollama) | ollama | 178,620 ★, 17,422 forks | core-and-ecosystem |
| github | [deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | deepseek-ai | 118,951 ★, 11,691 forks | core-and-ecosystem |
| github | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | Graphify-Labs | 106,785 ★, 10,388 forks | core-and-ecosystem |
| github | [open-design](https://github.com/nexu-io/open-design) | nexu-io | 87,046 ★, 10,122 forks | core-and-ecosystem |
| github | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | bytedance | 80,063 ★, 10,960 forks | agents-and-orchestration |
| github | [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) | shareAI-lab | 74,326 ★, 12,035 forks | core-and-ecosystem |
| github | [headroom](https://github.com/headroomlabs-ai/headroom) | headroomlabs-ai | 66,438 ★, 5,097 forks | core-and-ecosystem |
| github | [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | shanraisshan | 64,541 ★, 6,412 forks | core-and-ecosystem |
| github | [rust-unofficial/awesome-rust](https://github.com/rust-unofficial/awesome-rust) | rust-unofficial | 58,845 ★, 3,540 forks | index-and-marketplace |
| github | [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) | CherryHQ | 50,527 ★, 4,785 forks | core-and-ecosystem |
| github | [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) | diegosouzapw | 48,668 ★, 6,622 forks | ui-and-desktop |
| github | [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) | hugohe3 | 47,107 ★, 3,815 forks | core-and-ecosystem |
| github | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | Imbad0202 | 42,614 ★, 3,393 forks | core-and-ecosystem |
| youtube | [DeepSeek Harness: The End of Claude Code?](https://www.youtube.com/watch?v=qg9EyGOZd9U) | NeuralNine | 42,000 views | docs-and-learning |
| github | [amruthpillai/reactive-resume](https://github.com/amruthpillai/reactive-resume) | amruthpillai | 40,418 ★, 4,592 forks | core-and-ecosystem |
| youtube | [DeepSeek Harness 正式发布！ 开源一天狂揽 6.8 万星！V4 Pro 模型低调上线，AI Agent 部署与实测 \| 零度解说](https://www.youtube.com/watch?v=5G_afoTB1gs) | 零度解说 | 37,000 views | core-and-ecosystem |
| github | [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) | HKUDS | 30,948 ★, 5,019 forks | core-and-ecosystem |
| github | [BigPizzaV3/CodexPlusPlus](https://github.com/BigPizzaV3/CodexPlusPlus) | BigPizzaV3 | 28,989 ★, 1,840 forks | core-and-ecosystem |
| github | [Hannibal046/Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM) | Hannibal046 | 27,266 ★, 2,672 forks | index-and-marketplace |
| github | [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory) | rohitg00 | 27,059 ★, 2,311 forks | core-and-ecosystem |
