# deeplugin-market

Agent-facing access to the public [deeplugin.store](https://deeplugin.store) DeepSeek Harness registry. It searches the current aggregated catalog, shows complete source attribution, reports registry statistics, and builds reviewable install plans.

## Install

```sh
dsh plugin --profile web add github:Shiyao-Huang/awesome-deepseek-harness-plugin#path:/plugin
```

Restart the selected DSH profile. The plugin registers four tools:

| Tool | Behavior |
| --- | --- |
| `deeplugin_search` | Search by intent, name, author, tags, category, or bilingual description; return ranked Top N results |
| `deeplugin_details` | Resolve one stable registry id or exact install spec and show all source attributions |
| `deeplugin_stats` | Show current counts, categories, update date, and source verification claims |
| `deeplugin_install_plan` | Generate exact `dsh plugin add` commands for known ids; never execute them |

`verified=true` is a source curator's limited claim, not a deeplugin.store security or compatibility endorsement. Review the repository and attribution before installation. `deeplugin_install_plan` always returns `requiresConfirmation: true`; run commands only after explicit user confirmation.

The plugin tries the live registry for five seconds and then falls back to the snapshot bundled in the installed package.

## 中文

把 [deeplugin.store](https://deeplugin.store) 的聚合注册表接入 DeepSeek Harness。插件支持按意图搜索并返回 Top N、查看单个插件及全部来源、统计市场分类，以及为已登记插件生成安装计划。

```sh
dsh plugin --profile web add github:Shiyao-Huang/awesome-deepseek-harness-plugin#path:/plugin
```

`verified=true` 只表示某个来源维护者声明做过有限验证，不代表 deeplugin.store 的安全或兼容性背书。安装计划不会自动执行，必须先向用户展示来源和命令，并获得明确确认。
