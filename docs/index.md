# DeepSeek Harness Plugin Aggregator

> 一个可重复更新的公开资料聚合体：仓库、插件、索引、文章、帖子、图片缩略图和视频链接。原始观测保留在 `data/raw/`，SQLite 是可查询的派生索引。

当前数据集版本：**v20260815T203024Z**，完成时间：**2026-08-15T20:30:24Z**。共 **12,536** 条去重记录，覆盖 **14** 个平台，外部媒体资产 **871** 条。

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
| github | 12,197 | public REST API |
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
| deepseek-harness-forks | 11,093 | 0 |
| core-and-ecosystem | 890 | 135 |
| ui-and-desktop | 165 | 4 |
| index-and-marketplace | 163 | 34 |
| operations-and-safety | 89 | 1 |
| multimedia-and-vision | 67 | 6 |
| docs-and-learning | 39 | 7 |
| agents-and-orchestration | 30 | 3 |

## 价值衡量摘要

价值分数用于安排复核和进一步研究，不是安全、质量或销量背书。

| 平台 | 记录 | value | band | confidence | 分类 |
| --- | --- | ---: | :---: | ---: | --- |
| github | [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) | 83.63 | A | 100.00 | core-and-ecosystem |
| github | [dsh-web-ui](https://github.com/zhu1090093659/dsh-web-ui) | 77.42 | B | 100.00 | ui-and-desktop |
| github | [modlens](https://github.com/liustack/modlens) | 76.84 | B | 100.00 | multimedia-and-vision |
| github | [dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI) | 76.16 | B | 100.00 | ui-and-desktop |
| github | [DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) | 76.15 | B | 100.00 | ui-and-desktop |
| github | [dsh-deep-whale](https://github.com/Small-tailqwq/dsh-deep-whale) | 75.62 | B | 100.00 | core-and-ecosystem |
| github | [dsh-vision-toolkit](https://github.com/Anionex/dsh-vision-toolkit) | 74.40 | B | 100.00 | multimedia-and-vision |
| github | [dsh-genui](https://github.com/omdsh-dev/dsh-genui) | 74.35 | B | 100.00 | core-and-ecosystem |
| github | [dsh-ads](https://github.com/Nagi-ovo/dsh-ads) | 74.32 | B | 100.00 | core-and-ecosystem |
| github | [dsh-agent-teams](https://github.com/NanmiCoder/dsh-agent-teams) | 73.98 | B | 100.00 | core-and-ecosystem |

## 高互动/高关注记录

| 平台 | 标题 | 作者 | 指标 | 分类 |
| --- | --- | --- | --- | --- |
| github | [ollama/ollama](https://github.com/ollama/ollama) | ollama | 178,587 ★, 17,419 forks | core-and-ecosystem |
| github | [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) | deepseek-ai | 113,588 ★, 11,037 forks | core-and-ecosystem |
| github | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | Graphify-Labs | 106,619 ★, 10,371 forks | core-and-ecosystem |
| github | [open-design](https://github.com/nexu-io/open-design) | nexu-io | 86,879 ★, 10,111 forks | core-and-ecosystem |
| github | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | bytedance | 80,044 ★, 10,958 forks | agents-and-orchestration |
| github | [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) | shareAI-lab | 74,301 ★, 12,032 forks | core-and-ecosystem |
| github | [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | shanraisshan | 64,503 ★, 6,411 forks | core-and-ecosystem |
| github | [rust-unofficial/awesome-rust](https://github.com/rust-unofficial/awesome-rust) | rust-unofficial | 58,842 ★, 3,539 forks | index-and-marketplace |
| github | [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) | CherryHQ | 50,514 ★, 4,782 forks | core-and-ecosystem |
| github | [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) | diegosouzapw | 48,491 ★, 6,601 forks | ui-and-desktop |
| github | [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) | hugohe3 | 47,058 ★, 3,815 forks | core-and-ecosystem |
| github | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | Imbad0202 | 42,587 ★, 3,392 forks | core-and-ecosystem |
| youtube | [DeepSeek Harness: The End of Claude Code?](https://www.youtube.com/watch?v=qg9EyGOZd9U) | NeuralNine | 42,000 views | docs-and-learning |
| youtube | [DeepSeek Harness 正式发布！ 开源一天狂揽 6.8 万星！V4 Pro 模型低调上线，AI Agent 部署与实测 \| 零度解说](https://www.youtube.com/watch?v=5G_afoTB1gs) | 零度解说 | 37,000 views | core-and-ecosystem |
| github | [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) | HKUDS | 30,916 ★, 5,014 forks | core-and-ecosystem |
| github | [BigPizzaV3/CodexPlusPlus](https://github.com/BigPizzaV3/CodexPlusPlus) | BigPizzaV3 | 28,978 ★, 1,840 forks | core-and-ecosystem |
| github | [Hannibal046/Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM) | Hannibal046 | 27,266 ★, 2,672 forks | index-and-marketplace |
| github | [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory) | rohitg00 | 27,041 ★, 2,308 forks | core-and-ecosystem |
| github | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | OthmanAdi | 26,177 ★, 2,189 forks | index-and-marketplace |
| github | [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi) | can1357 | 25,002 ★, 2,407 forks | agents-and-orchestration |
