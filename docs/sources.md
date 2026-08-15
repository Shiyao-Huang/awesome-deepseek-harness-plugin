# Monitored upstream indexes

这些仓库是聚合器的源，不等同于项目质量背书。每次监测保存 README/结构化目录 raw，并把公开条目链接到 SQLite 中的去重 item；安装前仍应回到插件仓库审查代码、权限和兼容性。

| 源仓库 | stars | forks | 开放 issue | 当前条目 | 插件候选 | 最近检查 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins](https://github.com/Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins) | 58 | 9 | 4 | 181 | 98 | 2026-08-15T10:38:39Z · [raw](../data/raw/upstreams/20260815T103838Z.json) |
| [beancookie/awesome-dsh-plugin](https://github.com/beancookie/awesome-dsh-plugin) | 21 | 10 | 2 | 280 | 280 | 2026-08-15T10:38:39Z · [raw](../data/raw/upstreams/20260815T103838Z.json) |
| [walkinglabs/awesome-deepseek-harness-plugins](https://github.com/walkinglabs/awesome-deepseek-harness-plugins) | 4 | 7 | 2 | 114 | 91 | 2026-08-15T10:38:39Z · [raw](../data/raw/upstreams/20260815T103838Z.json) |

## Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins

Curated DeepSeek Harness (DSH) plugins, extensions, tools, skills, clients, runtimes, integrations, and verified references — English and Chinese.

展示前 20 个插件候选；完整目录在 `upstream_entries` 表和对应 raw 中。

| 插件 | 类别 | 描述 | 安装提示 |
| --- | --- | --- | --- |
| [dsh-balance](https://github.com/crazywoola/dsh-balance) | Developer &amp; Operations | dsh-balance | `—` |
| [dsh-context-doctor](https://github.com/Zhenyu98/dsh-context-doctor) | Developer &amp; Operations | dsh-context-doctor | `—` |
| [dsh-continual-evolve](https://github.com/ZK-Andy/dsh-continual-evolve) | Developer &amp; Operations | dsh-continual-evolve | `—` |
| [dsh-cost-meter](https://github.com/Han-1413141/dsh-cost-meter) | Developer &amp; Operations | dsh-cost-meter | `—` |
| [dsh-doublecheck](https://github.com/PerryLink/dsh-doublecheck) | Developer &amp; Operations | dsh-doublecheck | `—` |
| [dsh-evolve](https://github.com/william-jin-cmu/dsh-evolve) | Developer &amp; Operations | dsh-evolve | `—` |
| [dsh-fail-logger](https://github.com/Areium/dsh-fail-logger) | Developer &amp; Operations | dsh-fail-logger | `—` |
| [dsh-git-identity](https://github.com/LoserFox/dsh-git-identity) | Developer &amp; Operations | dsh-git-identity | `—` |
| [dsh-gitflow](https://github.com/lonelymoon87/dsh-gitflow) | Developer &amp; Operations | dsh-gitflow | `—` |
| [dsh-harness-ops](https://github.com/fakechris/dsh-harness-ops) | Developer &amp; Operations | dsh-harness-ops | `—` |
| [dsh-market](https://github.com/dsh-market/dsh-market) | Developer &amp; Operations | dsh-market | `—` |
| [dsh-notification](https://github.com/omdsh-dev/dsh-notification) | Developer &amp; Operations | dsh-notification | `—` |
| [dsh-plugin-check](https://github.com/omdsh-dev/dsh-plugin-check) | Developer &amp; Operations | dsh-plugin-check | `—` |
| [dsh-plugin-dev](https://github.com/omdsh-dev/dsh-plugin-dev) | Developer &amp; Operations | dsh-plugin-dev | `—` |
| [dsh-plugin-skills](https://github.com/omdsh-dev/dsh-plugin-skills) | Developer &amp; Operations | dsh-plugin-skills | `—` |
| [dsh-plugin-workshop](https://github.com/yyyyukari/dsh-plugin-workshop) | Developer &amp; Operations | dsh-plugin-workshop | `—` |
| [dsh-postmortem](https://github.com/zzh-newlearner/dsh-postmortem) | Developer &amp; Operations | dsh-postmortem | `—` |
| [dsh-recommend](https://github.com/zp-home/dsh-recommend) | Developer &amp; Operations | dsh-recommend | `—` |
| [dsh-revive](https://github.com/omdsh-dev/dsh-revive) | Developer &amp; Operations | dsh-revive | `—` |
| [dsh-security-audit](https://github.com/omdsh-dev/dsh-security-audit) | Developer &amp; Operations | dsh-security-audit | `—` |

## beancookie/awesome-dsh-plugin

Awesome DeepSeek Harness (DSH) Plugin

展示前 20 个插件候选；完整目录在 `upstream_entries` 表和对应 raw 中。

| 插件 | 类别 | 描述 | 安装提示 |
| --- | --- | --- | --- |
| [deepseek-harness-action](https://github.com/Lixiaoyiao/deepseek-harness-action) | dev | GitHub Action 运行 DSH 做 PR 审查、CI 诊断与受信任修复。 | `dsh plugin --profile web add github:Lixiaoyiao/deepseek-harness-action` |
| [dsh-agent-budget](https://github.com/vibeinging/dsh-agent-budget) | dev | agent 树 token 预算管理。 | `dsh plugin --profile web add github:vibeinging/dsh-agent-budget` |
| [dsh-annotate](https://github.com/BrambleXu/dsh-annotate) | dev | 面向 Vibe Coding 的浏览器元素标注插件：直接选取页面元素，并将结构化视觉反馈发送给 DeepSeek Harness Agent。 | `dsh plugin --profile web add github:BrambleXu/dsh-annotate` |
| [dsh-context-doctor](https://github.com/Zhenyu98/dsh-context-doctor) | dev | 上下文注入审计：统计指令链/技能目录/工具 schema 的 token 成本，检测重复与冲突。 | `dsh plugin --profile web add github:Zhenyu98/dsh-context-doctor` |
| [dsh-cost-tracker](https://github.com/yflmq001/dsh-cost-tracker) | dev | 按模型追踪 token 成本：可配置缓存命中/未命中、输出与高峰时段单价，实时会话花费条，并标记未配置价格的模型。 | `dsh plugin --profile web add github:yflmq001/dsh-cost-tracker` |
| [dsh-desktop](https://github.com/foolgry/dsh-desktop) | dev | 开箱即用的 Electron 桌面版，自动跟随上游发版。 | `dsh plugin --profile web add github:foolgry/dsh-desktop` |
| [dsh-doctor](https://github.com/asdf17128/dsh-doctor) | dev | Profile 体检：检出 patch 丢失字段、不存在的 entry id 与工具重名冲突。 | `dsh plugin --profile web add github:asdf17128/dsh-doctor` |
| [dsh-eval-harness](https://github.com/BiBoyang/dsh-eval-harness) | dev | DSH 插件评测框架：YAML 用例驱动真实 headless agent，断言工具调用/参数/返回与 token 用量，baseline 门禁做 CI 回归。 | `dsh plugin --profile web add github:BiBoyang/dsh-eval-harness` |
| [dsh-evolve](https://github.com/william-jin-cmu/dsh-evolve) | dev | 自进化：agent 在会话内给自己热挂载/卸载持久化插件。 | `dsh plugin --profile web add github:william-jin-cmu/dsh-evolve` |
| [dsh-fail-logger](https://github.com/Areium/dsh-fail-logger) | dev | 全模式调用工具失败自动实录：把原生工具 / PTC run_code / 代码内嵌工具调用的失败错因去重计数后写入 skill，越用越少错。 | `dsh plugin --profile web add github:Areium/dsh-fail-logger` |
| [dsh-git-identity](https://github.com/LoserFox/dsh-git-identity) | dev | git 提交固定使用环境自身作者身份，环境变量注入压过一切 `git config` 设置。 | `dsh plugin --profile web add github:LoserFox/dsh-git-identity` |
| [dsh-gitflow](https://github.com/lonelymoon87/dsh-gitflow) | dev | 增加需要审批的 Git 状态、diff、日志、提交、分支和可选检查点工具。 | `dsh plugin --profile web add github:lonelymoon87/dsh-gitflow` |
| [dsh-guardian](https://github.com/lonelymoon87/dsh-guardian) | dev | 增加危险操作策略检查、输出脱敏和安全审查工作流。 | `dsh plugin --profile web add github:lonelymoon87/dsh-guardian` |
| [dsh-harmony](https://github.com/CH4ACKO3/dsh-harmony) | dev | 让一个 DSH 插件在运行时修改另一个插件的代码，并提供 Patch 排序、冲突检查和热重载。 | `dsh plugin --profile web add dsh-harmony` |
| [dsh-lan-access](https://github.com/Leon0555/dsh-lan-access) | dev | 局域网访问：Web GUI 绑定 0.0.0.0 + crypto.randomUUID polyfill（修复非安全上下文下 RPC 崩溃）。 | `dsh plugin --profile web add dsh-lan-access` |
| [dsh-mcp-manager](https://github.com/hyqhyq3/dsh-mcp-manager) | dev | MCP 服务器管理器：OAuth 或静态 token 认证 + 设置页。 | `dsh plugin --profile web add github:hyqhyq3/dsh-mcp-manager` |
| [dsh-mcp-panel](https://github.com/PerryLink/dsh-mcp-panel) | dev | 官方 MCP 客户端（dsh-mcp-client）的只读运行时管理面板：/mcp 命令与设置页 MCP 页签展示连接状态、已注册工具、错误与重连计数，脱敏展示并提供启停 patch 建议。 | `dsh plugin --profile web add github:PerryLink/dsh-mcp-panel` |
| [dsh-multica-runtime](https://github.com/forrestchang/dsh-multica-runtime) | dev | 让 dsh 运行时跑在 Multica 上。 | `dsh plugin --profile web add github:forrestchang/dsh-multica-runtime` |
| [dsh-pain-point-check](https://github.com/ICCuse/dsh-pain-point-check) | dev | 强制痛点检查：同一问题连续 2 个实验未收敛后注入三问、拦截非调查类工具调用直到答出、阻止同方向重试。 | `dsh plugin --profile web add github:ICCuse/dsh-pain-point-check` |
| [dsh-passwords](https://github.com/slywalker2006/dsh-passwords) | dev | DSH Web UI 登录网关：首次配置、bcrypt + 静态加密（AES-256-GCM/HMAC）、防爆破、审计日志、TLS 1.2+ 与 80→443 跳转、CSRF 与防嵌框。 | `dsh plugin --profile web add github:slywalker2006/dsh-passwords` |

## walkinglabs/awesome-deepseek-harness-plugins

A curated, bilingual list of verified plugins, tools, design workflows, and learning resources for DeepSeek Harness (DSH).

展示前 20 个插件候选；完整目录在 `upstream_entries` 表和对应 raw 中。

| 插件 | 类别 | 描述 | 安装提示 |
| --- | --- | --- | --- |
| [dsh-better-browser](https://github.com/titanwings/dsh-better-browser) | Browser, Computer Use &amp; Remote Execution | Signed-in browser access through Kimi WebBridge tools. | `—` |
| [dsh-browser](https://github.com/Lum1104/dsh-browser) | Browser, Computer Use &amp; Remote Execution | Chrome sidebar extension for direct browser operation without vision capabilities. | `—` |
| [dsh-computer-use](https://github.com/Anionex/dsh-computer-use) | Browser, Computer Use &amp; Remote Execution | Accessibility-first macOS computer-use bundle with scoped permissions and freshness checks. | `—` |
| [Nowledge Mem for DSH](https://github.com/nowledge-co/nowledge-mem-deepseek-harness) | Context, Memory &amp; Observability | Community memory-plugin bundle built around Nowledge Mem. | `—` |
| [dsh-compaction-instant](https://github.com/KitDoesIt/dsh-compaction-instant) | Context, Memory &amp; Observability | Offline, deterministic replacement for DSH&#x27;s basic compaction seam, with recall tools for the append-only session log. | `—` |
| [dsh-context-doctor](https://github.com/Zhenyu98/dsh-context-doctor) | Context, Memory &amp; Observability | Audit instruction, skill, and tool-schema token cost, duplication, and conflicts. | `—` |
| [dsh-cost-meter](https://github.com/Han-1413141/dsh-cost-meter) | Context, Memory &amp; Observability | Per-session and daily API cost, budget, and official-balance tracking for the DSH Web UI, with a history dashboard and one-click official price sync (built against the current dsh web bundle). | `—` |
| [dsh-explain](https://github.com/yuezengwu/dsh-explain) | Context, Memory &amp; Observability | Local-first learning mode with global learning threads and explainable context. | `—` |
| [dsh-memory-evolve](https://github.com/csyangwen/dsh-memory-evolve) | Context, Memory &amp; Observability | Cross-session memory, branch awareness, session search, and self-evolving skills. | `—` |
| [dsh-postmortem](https://github.com/zzh-newlearner/dsh-postmortem) | Context, Memory &amp; Observability | Local-first failure postmortems for DSH sessions. | `—` |
| [dsh-sentinel](https://github.com/fuhefei/dsh-sentinel) | Context, Memory &amp; Observability | Durable file, command, HTTP, process, and webhook watches that wake an agent. | `—` |
| [dsh-session-health](https://github.com/omdsh-dev/dsh-session-health) | Context, Memory &amp; Observability | Read-only diagnostics for multi-frame zstd session files. | `—` |
| [dsh-session-search](https://github.com/Tieboyh/dsh-session-search) | Context, Memory &amp; Observability | Index-free cross-agent session search. | `—` |
| [dsh-telemetry-redactor](https://github.com/030611/dsh-telemetry-redactor) | Context, Memory &amp; Observability | Redacts supported secret patterns from the exported session-telemetry/record copy without changing the canonical session log; audited against DSH commit 47f943859bef60e4160492346772ded9b24f765a and tested with dsh-session-telemetry rc.6. | `—` |
| [dsh-trace](https://github.com/vibeinging/dsh-trace) | Context, Memory &amp; Observability | Export DSH turns, model steps, and tool calls to yiTrace over HTTP. | `—` |
| [dsh-verification-receipt](https://github.com/030611/dsh-verification-receipt) | Context, Memory &amp; Observability | Writes local JSONL summaries of per-turn tool outcomes and heuristic verification signals without storing prompts, tool arguments, or result text; audited against DSH commit 47f943859bef60e4160492346772ded9b24f765a and tested with dsh-session rc.6. | `—` |
| [dsh-annotation](https://github.com/omdsh-dev/dsh-annotation) | Creative &amp; Personal | Select text, attach annotations, and send structured feedback with a message. | `—` |
| [dsh-fun-ticker](https://github.com/omdsh-dev/dsh-fun-ticker) | Creative &amp; Personal | Configurable crypto, FX, A-share, index, and stock ticker. | `—` |
| [dsh-fun-typewriter](https://github.com/omdsh-dev/dsh-fun-typewriter) | Creative &amp; Personal | WebAudio typing ambience with plugin settings. | `—` |
| [dsh-fun-weather](https://github.com/omdsh-dev/dsh-fun-weather) | Creative &amp; Personal | Open-Meteo weather tab and weather-following themes. | `—` |
