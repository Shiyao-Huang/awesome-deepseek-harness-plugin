# 小红书发布稿

## 标题

别再按 Star 装 DSH 插件了

## 正文

我把 deeplugin.store 里 1055 个可安装插件、来源和指标重新跑了一遍。

最意外的是：按 Star 排，前几名未必是“最火的 DSH 插件”。例如 OpenViking 的 DSH memory plugin 显示 28.5k Star，但这是整个父仓的 Star，不是这个 adapter 的独立采用度。

我又翻了几篇高赞笔记的评论区，大家反复卡住的其实不是“插件太少”，而是：GitHub 找到了不会装、看不懂权限、怕不兼容、装坏了不知道怎么退。

所以我会按能力层选，而不是抄一份 Top 10：

1. 交互层：dsh-web-ui-all / DSH Browser
2. 能力层：OpenViking memory plugin / dsh-agent-teams
3. 防线：dsh-plugin-check

我的判断是，DSH 更像 Agent 的 Linux。它不一定比 Codex 更开箱即用，但它把 Agent 底盘拆成了可以替换、组合和审计的插件。

真正的门槛不是插件少，而是发现、验证、安装、回滚还没连成一条路。

完整来源、精确安装 spec 和历史指标放在 deeplugin.store。这个 Store 和 Market Plugin 是我们自己维护的，这里明确披露；不安装，也能直接查数据。

你现在最想补的是 UI、浏览器、记忆，还是多 Agent？我继续拆下一篇。

#DeepSeekHarness #DSH #AI工具 #AI编程 #AIAgent #开源项目 #效率工具
