# deeplugin-market

Agent-facing access to [deeplugin.store](https://deeplugin.store), a public Store that brings attributed DeepSeek Harness plugin listings from community registries and direct submissions into one searchable catalog. Install this Market Plugin once, then ask your Agent in natural language to discover, inspect, install, list, update, or remove plugins. Conversational Chinese and English searches discard request boilerplate, match capabilities across names, tags, descriptions, install specs, and attributed registries, then rank by term coverage before GitHub stars.

## Install

```sh
dsh plugin --profile web add github:Shiyao-Huang/awesome-deepseek-harness-plugin#path:/plugin
```

Restart the selected DSH profile. The plugin registers six tools:

| Tool | Behavior |
| --- | --- |
| `deeplugin_search` | Search by intent, name, author, tags, category, or bilingual description; return ranked Top N results |
| `deeplugin_details` | Resolve one stable registry id or exact install spec and show all source attributions |
| `deeplugin_stats` | Show current counts, categories, update date, and source verification claims |
| `deeplugin_install_plan` | Build a reviewable plan with exact identities and source attribution |
| `deeplugin_install` | Match a registry id to its exact spec, then install after DSH asks for user approval |
| `deeplugin_manage` | List installed plugins, or update/remove an exact package after approval |

Try requests such as:

```text
Find a plugin for public web search and show me where it came from.
Install deeplugin-… into my web profile.
List the plugins installed in my web profile.
Update @owner/plugin, then remove it when I am done.
```

`verified=true` is a source curator's limited claim, not a deeplugin.store security or compatibility endorsement. The Agent shows the attributed source and exact install identity before installation. DSH asks for approval on every install, update, and removal; rejection leaves the profile unchanged. Listing installed plugins is read-only.

The plugin tries the live registry for five seconds and then falls back to the snapshot bundled in the installed package.

The runtime invokes `dsh plugin` with argument arrays and never constructs a shell command. Source-launched DSH installations may set `DSH_MARKET_DSH_COMMAND` to the absolute `dsh` executable path.

## 中文

把 [deeplugin.store](https://deeplugin.store) 接入 DeepSeek Harness。这个 Store 将社区 Registry 和直接提交中的插件聚合成一个带来源、可搜索、可安装的目录。Market Plugin 只需安装一次，之后就可以直接用自然语言让 Agent 搜索、核对来源、安装和管理其他插件。中英文口语化查询会去掉“帮我找一个插件”之类请求套话，在名称、标签、中英文描述、安装 spec 和来源 Registry 中按关键能力覆盖度排序。

```sh
dsh plugin --profile web add github:Shiyao-Huang/awesome-deepseek-harness-plugin#path:/plugin
```

例如直接告诉 Agent：“找一个能搜索公开网页的插件，先告诉我来源，再安装到 web profile。”Agent 会先展示来源和精确安装标识；安装、更新和卸载均由 DSH 弹出批准请求，只有批准后才执行。`deeplugin_manage` 还可以列出已安装插件。

`verified=true` 只表示某个来源维护者声明做过有限验证，不代表 deeplugin.store 的安全或兼容性背书。拒绝批准不会修改 profile。
