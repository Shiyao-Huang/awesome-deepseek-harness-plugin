# DeepSeek Harness Plugin Aggregator

> 一个可重复更新的公开资料聚合体：仓库、插件、索引、文章、帖子、图片缩略图和视频链接。原始观测保留在 `data/raw/`，SQLite 是可查询的派生索引。

当前数据集版本：**v20260818T131329Z**，完成时间：**2026-08-18T13:13:34Z**。共 **14,897** 条去重记录，覆盖 **14** 个平台，外部媒体资产 **1,285** 条。

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
| github | 14,406 | public REST API |
| xiaohongshu | 157 | ego-browser visible DOM |
| hacker_news | 112 | Algolia public search API |
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
| core-and-ecosystem | 1,755 | 240 |
| index-and-marketplace | 227 | 43 |
| ui-and-desktop | 223 | 6 |
| operations-and-safety | 145 | 1 |
| multimedia-and-vision | 111 | 7 |
| docs-and-learning | 53 | 9 |
| agents-and-orchestration | 30 | 4 |
| ecosystem | 1 | 1 |

## 价值衡量摘要

价值分数用于安排复核和进一步研究，不是安全、质量或销量背书。

| 平台 | 记录 | value | band | confidence | 分类 |
| --- | --- | ---: | :---: | ---: | --- |
| github | [zhu1090093659/dsh-web-ui](https://github.com/zhu1090093659/dsh-web-ui) | 80.79 | A | 100.00 | ui-and-desktop |
| github | [liustack/modlens](https://github.com/liustack/modlens) | 80.14 | A | 100.00 | multimedia-and-vision |
| github | [omdsh-dev/DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) | 79.55 | B | 100.00 | ui-and-desktop |
| github | [ccch1mneyyy/dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI) | 79.40 | B | 100.00 | ui-and-desktop |
| github | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 79.18 | B | 100.00 | core-and-ecosystem |
| github | [ysr666/dsh-vision-router](https://github.com/ysr666/dsh-vision-router) | 77.78 | B | 100.00 | multimedia-and-vision |
| github | [Anionex/dsh-vision-toolkit](https://github.com/Anionex/dsh-vision-toolkit) | 77.69 | B | 100.00 | ui-and-desktop |
| github | [superdesigndev/superdesign-skill](https://github.com/superdesigndev/superdesign-skill) | 76.63 | B | 100.00 | core-and-ecosystem |
| github | [bowenliang123/dsh-context](https://github.com/bowenliang123/dsh-context) | 76.35 | B | 100.00 | core-and-ecosystem |
| github | [Small-tailqwq/dsh-deep-whale](https://github.com/Small-tailqwq/dsh-deep-whale) | 76.28 | B | 100.00 | core-and-ecosystem |

## 高互动/高关注记录

| 平台 | 标题 | 作者 | 指标 | 分类 |
| --- | --- | --- | --- | --- |
| github | [ollama/ollama](https://github.com/ollama/ollama) | ollama | 178,864 ★, 17,451 forks | core-and-ecosystem |
| github | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | deepseek-ai | 158,031 ★, 16,431 forks | core-and-ecosystem |
| github | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | Graphify-Labs | 107,730 ★, 10,464 forks | core-and-ecosystem |
| github | [nexu-io/open-design](https://github.com/nexu-io/open-design) | nexu-io | 88,720 ★, 10,241 forks | ui-and-desktop |
| github | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | bytedance | 80,240 ★, 10,998 forks | agents-and-orchestration |
| github | [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) | shareAI-lab | 74,549 ★, 12,060 forks | core-and-ecosystem |
| github | [headroom](https://github.com/headroomlabs-ai/headroom) | headroomlabs-ai | 66,438 ★, 5,097 forks | core-and-ecosystem |
| github | [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | shanraisshan | 64,650 ★, 6,426 forks | core-and-ecosystem |
| github | [rust-unofficial/awesome-rust](https://github.com/rust-unofficial/awesome-rust) | rust-unofficial | 58,881 ★, 3,548 forks | index-and-marketplace |
| github | [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) | CherryHQ | 50,715 ★, 4,810 forks | core-and-ecosystem |
| github | [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) | diegosouzapw | 50,206 ★, 6,833 forks | ui-and-desktop |
| github | [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) | hugohe3 | 47,687 ★, 3,849 forks | core-and-ecosystem |
| github | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | Imbad0202 | 42,906 ★, 3,409 forks | core-and-ecosystem |
| youtube | [DeepSeek Harness: The End of Claude Code?](https://www.youtube.com/watch?v=qg9EyGOZd9U) | NeuralNine | 42,000 views | docs-and-learning |
| github | [amruthpillai/reactive-resume](https://github.com/amruthpillai/reactive-resume) | amruthpillai | 40,954 ★, 4,617 forks | core-and-ecosystem |
| github | [Hmbown/CodeWhale](https://github.com/Hmbown/CodeWhale) | Hmbown | 40,828 ★, 3,532 forks | core-and-ecosystem |
| youtube | [DeepSeek Harness 正式发布！ 开源一天狂揽 6.8 万星！V4 Pro 模型低调上线，AI Agent 部署与实测 \| 零度解说](https://www.youtube.com/watch?v=5G_afoTB1gs) | 零度解说 | 37,000 views | core-and-ecosystem |
| github | [esengine/DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) | esengine | 34,753 ★, 2,308 forks | core-and-ecosystem |
| github | [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) | HKUDS | 31,182 ★, 5,065 forks | core-and-ecosystem |
| github | [BigPizzaV3/CodexPlusPlus](https://github.com/BigPizzaV3/CodexPlusPlus) | BigPizzaV3 | 29,157 ★, 1,857 forks | core-and-ecosystem |
