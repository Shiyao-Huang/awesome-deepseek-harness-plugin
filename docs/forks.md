# DeepSeek Harness Fork Network

- Dataset version: `v20260815T214302Z`
- Public Fork records: **11,117**
- Ranking filter: **0+ stars**; observed Fork identities: **11,117**; filtered out of ranking: **0**.
- Ever deep-scanned: **317 / 11,117** (2.85%); pending: **10,800**; conservative backfill ETA: **68 daily runs**.
- Deep-scanned successfully in the current projection: **317**; compare responses retained: **317**
- Fork rows with public owner reputation observed: **300**; the current ranking pool applies a configurable minimum-Star filter.
- Scope: public Forks returned by GitHub REST API pagination for `deepseek-ai/deepseek-harness`.
- Raw evidence is collected under `data/raw/forks/`; the [latest compressed SQLite snapshot](https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin/releases/download/dataset-latest/aggregator-full.sqlite3.zst) includes the fork tables and raw JSON payloads. Unpack it with `zstd -d aggregator-full.sqlite3.zst -o aggregator-full.sqlite3`.
- Searchable browser: `docs/forks.html`; compact catalog: `docs/data/fork-catalog.json`; complete machine-readable ranking: `index/forks.jsonl`.
- `overall score = repository influence 60% + public-account reputation 40%` when the profile is observed; missing profile signals are not treated as zero. This is a public-signal ordering aid, not a quality, safety, integrity, or endorsement claim.

## GitHub star order

| Star rank | Fork | Stars | Composite rank | Audit | Evidence |
| ---: | --- | ---: | ---: | --- | --- |
| 1 | [salathleizhang/deepseek-harness-desktop](https://github.com/salathleizhang/deepseek-harness-desktop) | 97 | 1 | audited | 新增约 42 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“Native desktop app for DeepSeek Harness — an Electron shell that runs the harness locally and hosts the official Web GUI unchanged”。 |
| 2 | [Sakana-yuyu/deepseek-harness-desktop](https://github.com/Sakana-yuyu/deepseek-harness-desktop) | 21 | 8 | audited | 新增约 14 个提交并修改 81 个文件，主要涉及 配置、文档、CI/构建、UI/应用层；目标线索是“Rust构建的客户端，体积更小，更方便，Mac，win，linux已完成”。 |
| 3 | [G36maid/deepseek-harness](https://github.com/G36maid/deepseek-harness) | 12 | 7 | audited | 新增约 19 个提交并修改 300 个文件，主要涉及 配置、文档；目标线索是“DeepSeek Harness 繁體中文版 (zh-TW) — Everything is a Plugin”。 |
| 4 | [Skyearn/deepseek-harness-app](https://github.com/Skyearn/deepseek-harness-app) | 11 | 12 | audited | 新增约 24 个提交并修改 31 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness Desktop”。 |
| 5 | [rpmalouin/deepseek-harness](https://github.com/rpmalouin/deepseek-harness) | 8 | 14 | audited | 新增约 4 个提交并修改 31 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 6 | [yx54hego-cloud/deepseek-harness](https://github.com/yx54hego-cloud/deepseek-harness) | 7 | 136 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 7 | [Ajwyunsx/deepseek-harness-mobile](https://github.com/Ajwyunsx/deepseek-harness-mobile) | 4 | 22 | audited | 新增约 7 个提交并修改 40 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 8 | [happylin0x29a/deepseek-harness-desktop](https://github.com/happylin0x29a/deepseek-harness-desktop) | 4 | 27 | audited | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness desktop base on tauri”。 |
| 9 | [luolangaga/deepseek-harness](https://github.com/luolangaga/deepseek-harness) | 4 | 41 | audited | 新增约 11 个提交并修改 54 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 10 | [puppywang/deepseek-harness](https://github.com/puppywang/deepseek-harness) | 4 | 20 | audited | 新增约 10 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 11 | [sdkwork-ai/deepseek-harness-desktop](https://github.com/sdkwork-ai/deepseek-harness-desktop) | 4 | 108 | audited | 新增约 43 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 12 | [yazzang-homelab/deepseek-harness](https://github.com/yazzang-homelab/deepseek-harness) | 2 | 93 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 13 | [FSMargoo/deepseek-harness](https://github.com/FSMargoo/deepseek-harness) | 2 | 36 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 14 | [huiliyi37/deepseek-harness](https://github.com/huiliyi37/deepseek-harness) | 2 | 106 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 15 | [Kiowx/deepseek-harness](https://github.com/Kiowx/deepseek-harness) | 2 | 110 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 16 | [MarceloClaro/deepseek-harness](https://github.com/MarceloClaro/deepseek-harness) | 2 | 28 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 17 | [stophobia/deepseek-harness](https://github.com/stophobia/deepseek-harness) | 2 | 9 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 18 | [suiyuebaobao/deepseek-harness-gui](https://github.com/suiyuebaobao/deepseek-harness-gui) | 2 | 159 | audited | 新增约 2 个提交并修改 52 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“Windows desktop fork of DeepSeek Harness, packaged with Tauri while preserving the full Web profile and plugin runtime”。 |
| 19 | [Yihong89/deepseek-harness](https://github.com/Yihong89/deepseek-harness) | 2 | 66 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 20 | [srwang0506/deepseek-harness](https://github.com/srwang0506/deepseek-harness) | 1 | 83 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 21 | [xiaosenho/deepseek-harness](https://github.com/xiaosenho/deepseek-harness) | 1 | 123 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 22 | [007M7/deepseek-harness](https://github.com/007M7/deepseek-harness) | 1 | 163 | audited | 未观察到相对 upstream 的文件修改；目标线索是“我永远喜欢deepseek！！！”。 |
| 23 | [123prompt/deepseek-harness](https://github.com/123prompt/deepseek-harness) | 1 | 211 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 24 | [1486482143/deepseek-harness](https://github.com/1486482143/deepseek-harness) | 1 | 214 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 25 | [18217778896/deepseek-harness](https://github.com/18217778896/deepseek-harness) | 1 | 141 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 26 | [2404589803/deepseek-harness](https://github.com/2404589803/deepseek-harness) | 1 | 56 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 27 | [485524097/deepseek-harness](https://github.com/485524097/deepseek-harness) | 1 | 224 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 28 | [4evour/deepseek-harness](https://github.com/4evour/deepseek-harness) | 1 | 131 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 29 | [a907781273-a11y/deepseek-harness](https://github.com/a907781273-a11y/deepseek-harness) | 1 | 11088 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 30 | [achristofaro/deepseek-harness](https://github.com/achristofaro/deepseek-harness) | 1 | 60 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 31 | [AI-1-TOP/deepseek-harness](https://github.com/AI-1-TOP/deepseek-harness) | 1 | 11114 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 32 | [aimierbear/TinyWhale](https://github.com/aimierbear/TinyWhale) | 1 | 37 | audited | 新增约 18 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、CI/构建；目标线索是“TinyWhale — desktop-oriented MIT fork of DeepSeek Harness, with an Electron shell in desktop/”。 |
| 33 | [alexdeweb/deepseek-harness](https://github.com/alexdeweb/deepseek-harness) | 1 | 85 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 34 | [alexdolbun/deepseek-harness](https://github.com/alexdolbun/deepseek-harness) | 1 | 5 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 35 | [Alsdara/deepseek-harness](https://github.com/Alsdara/deepseek-harness) | 1 | 11079 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 36 | [Anyaoha/deepseek-harness](https://github.com/Anyaoha/deepseek-harness) | 1 | 53 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 37 | [Ashveil1/deepseek-harness-ares](https://github.com/Ashveil1/deepseek-harness-ares) | 1 | 202 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek harness for pentesting”。 |
| 38 | [athif23/deepseek-harness](https://github.com/athif23/deepseek-harness) | 1 | 35 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 39 | [ayushare/deepseek-harness](https://github.com/ayushare/deepseek-harness) | 1 | 11056 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 40 | [b3nk-x1/deepseek-harness](https://github.com/b3nk-x1/deepseek-harness) | 1 | 11093 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 41 | [badestgod/deepseek-harness](https://github.com/badestgod/deepseek-harness) | 1 | 94 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 42 | [Beam-wi/deepseek-harness](https://github.com/Beam-wi/deepseek-harness) | 1 | 154 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 43 | [ben-vargas/ai-deepseek-harness](https://github.com/ben-vargas/ai-deepseek-harness) | 1 | 23 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 44 | [biyan113/deepseek-harness](https://github.com/biyan113/deepseek-harness) | 1 | 38 | audited | 新增约 3 个提交并修改 55 个文件，主要涉及 CI/构建、UI/应用层、文档、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 45 | [BlackRosePetals/deepseek-harness](https://github.com/BlackRosePetals/deepseek-harness) | 1 | 127 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 46 | [BobcGn/deepseek-harness-app](https://github.com/BobcGn/deepseek-harness-app) | 1 | 133 | audited | 新增约 14 个提交并修改 31 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 47 | [bojieli/deepseek-harness](https://github.com/bojieli/deepseek-harness) | 1 | 4 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 48 | [boktoday/deepseek-harness](https://github.com/boktoday/deepseek-harness) | 1 | 51 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 49 | [BurtonQin/deepseek-harness](https://github.com/BurtonQin/deepseek-harness) | 1 | 26 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 50 | [CatchCatOoO/deepseek-harness](https://github.com/CatchCatOoO/deepseek-harness) | 1 | 176 | audited | 新增约 4 个提交并修改 300 个文件，主要涉及 文档、配置、agent/skill 能力；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 51 | [cFqr-lang/deepseek-harness](https://github.com/cFqr-lang/deepseek-harness) | 1 | 119 | audited | 新增约 5 个提交并修改 57 个文件，主要涉及 UI/应用层、Harness 核心能力、配置、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 52 | [CH-HGod/deepseek-harness](https://github.com/CH-HGod/deepseek-harness) | 1 | 11067 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 53 | [chiekoschamburek-dev/deepseek-harness](https://github.com/chiekoschamburek-dev/deepseek-harness) | 1 | 11082 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 54 | [China-MY/deepseek-harness](https://github.com/China-MY/deepseek-harness) | 1 | 98 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 55 | [chyl00/deepseek-harness](https://github.com/chyl00/deepseek-harness) | 1 | 191 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 56 | [cioerp/deepseek-harness](https://github.com/cioerp/deepseek-harness) | 1 | 11108 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 57 | [codelife2020/deepseek-harness](https://github.com/codelife2020/deepseek-harness) | 1 | 185 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 58 | [coder-v0/deepseek-harness](https://github.com/coder-v0/deepseek-harness) | 1 | 87 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 59 | [cq2021-coder/deepseek-harness-desktop](https://github.com/cq2021-coder/deepseek-harness-desktop) | 1 | 96 | audited | 未观察到相对 upstream 的文件修改；目标线索是“使用 tauri 为 DeepSeek Harness 生态打造的现代化桌面端应用”。 |
| 60 | [criapa/deepseek-harness](https://github.com/criapa/deepseek-harness) | 1 | 46 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 61 | [Cute-chen/deepseek-harness-app](https://github.com/Cute-chen/deepseek-harness-app) | 1 | 179 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 62 | [Cyenoch/deepseek-harness](https://github.com/Cyenoch/deepseek-harness) | 1 | 67 | audited | 新增约 13 个提交并修改 300 个文件，主要涉及 配置、文档、agent/skill 能力、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 63 | [cyh7777/deepseek-harness](https://github.com/cyh7777/deepseek-harness) | 1 | 11069 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 64 | [dailin3/deepseek-harness](https://github.com/dailin3/deepseek-harness) | 1 | 122 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 65 | [DailyR/deepseek-harness](https://github.com/DailyR/deepseek-harness) | 1 | 40 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 66 | [ddd666j/deepseek-harness](https://github.com/ddd666j/deepseek-harness) | 1 | 11100 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 67 | [DeepThinkingZhouLiu/Deepseek-Harness-RSI](https://github.com/DeepThinkingZhouLiu/Deepseek-Harness-RSI) | 1 | 74 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 68 | [deveuper/deepseek-harness](https://github.com/deveuper/deepseek-harness) | 1 | 138 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 69 | [devin2255/deepseek-harness-desktop](https://github.com/devin2255/deepseek-harness-desktop) | 1 | 88 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 70 | [djhh555/deepseek-sightline](https://github.com/djhh555/deepseek-sightline) | 1 | 135 | audited | 新增约 2 个提交并修改 43 个文件，主要涉及 文档、UI/应用层、依赖、Harness 核心能力；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 71 | [DogeJian/deepseek-harness](https://github.com/DogeJian/deepseek-harness) | 1 | 77 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 72 | [donstang/deepseek-harness](https://github.com/donstang/deepseek-harness) | 1 | 42 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 73 | [dorucioclea/deepseek-harness](https://github.com/dorucioclea/deepseek-harness) | 1 | 11 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 74 | [drscrewdriver/deepseek-harness](https://github.com/drscrewdriver/deepseek-harness) | 1 | 73 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 75 | [duliangkuan/deepseek-harness](https://github.com/duliangkuan/deepseek-harness) | 1 | 152 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 76 | [EdwardXIE6666/deepseek-harness](https://github.com/EdwardXIE6666/deepseek-harness) | 1 | 199 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 77 | [enbideren/deepseek-harness](https://github.com/enbideren/deepseek-harness) | 1 | 78 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 78 | [equable66/deepseek-harness](https://github.com/equable66/deepseek-harness) | 1 | 970 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 79 | [Erichy777/deepseek-harness](https://github.com/Erichy777/deepseek-harness) | 1 | 189 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 80 | [Ericsongyl/deepseek-harness](https://github.com/Ericsongyl/deepseek-harness) | 1 | 30 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 81 | [ermao009/deepseek-harness](https://github.com/ermao009/deepseek-harness) | 1 | 219 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 82 | [exposir/deepseek-harness](https://github.com/exposir/deepseek-harness) | 1 | 10 | audited | 新增约 9 个提交并修改 13 个文件，主要涉及 文档、Harness 核心能力、测试；目标线索是“DeepSeek Harness”。 |
| 83 | [fage45029704-lgtm/deepseek-harness](https://github.com/fage45029704-lgtm/deepseek-harness) | 1 | 11086 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 84 | [faguangdeyueliang/deepseek-harness](https://github.com/faguangdeyueliang/deepseek-harness) | 1 | 203 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 85 | [fendouai/deepseek-harness-desktop](https://github.com/fendouai/deepseek-harness-desktop) | 1 | 2 | audited | 新增约 10 个提交并修改 123 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 86 | [fisher158163/deepseek-harness](https://github.com/fisher158163/deepseek-harness) | 1 | 29 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 87 | [flaqai/open-deepseek-harness-desktop](https://github.com/flaqai/open-deepseek-harness-desktop) | 1 | 164 | audited | 未观察到相对 upstream 的文件修改；目标线索是“Open Source Desktop for DeepSeek Harness. DeepSeek Harness: Everything is a Plugin”。 |
| 88 | [flowersea302/deepseek-harness](https://github.com/flowersea302/deepseek-harness) | 1 | 222 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 89 | [FlyingSama/deepseek-harness](https://github.com/FlyingSama/deepseek-harness) | 1 | 183 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 90 | [GavinDong-plaud/deepseek-harness](https://github.com/GavinDong-plaud/deepseek-harness) | 1 | 11066 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 91 | [GetSayAll/deepseek-harness-app](https://github.com/GetSayAll/deepseek-harness-app) | 1 | 11074 | audited | 新增约 25 个提交并修改 118 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek Harness”。 |
| 92 | [ghthh/deepseek-harness](https://github.com/ghthh/deepseek-harness) | 1 | 11055 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 93 | [GTC2080/deepseek-harness](https://github.com/GTC2080/deepseek-harness) | 1 | 160 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness 桌面端：基于 Tauri，支持 macOS 与 Windows；源码位于 desktop 分支”。 |
| 94 | [guihuatu2022/deepseek-harness](https://github.com/guihuatu2022/deepseek-harness) | 1 | 186 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 95 | [GZZ-523/deepseek-harness](https://github.com/GZZ-523/deepseek-harness) | 1 | 178 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 96 | [hanfengchiyi/deepseek-harness](https://github.com/hanfengchiyi/deepseek-harness) | 1 | 205 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 97 | [hanqi9622-eng/deepseek-harness](https://github.com/hanqi9622-eng/deepseek-harness) | 1 | 11098 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 98 | [HaoyanZhang123/deepseek-harness-live-preset-switch](https://github.com/HaoyanZhang123/deepseek-harness-live-preset-switch) | 1 | 11081 | audited | 新增约 2 个提交并修改 81 个文件，主要涉及 文档、agent/skill 能力、UI/应用层、Harness 核心能力；目标线索是“DeepSeek Harness with live agent-preset switching at turn boundaries”。 |
| 99 | [heleileimail-cmyk/deepseek-harness](https://github.com/heleileimail-cmyk/deepseek-harness) | 1 | 143 | audited | 新增约 3 个提交并修改 22 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 100 | [HelloNicoo/deepseek-harness](https://github.com/HelloNicoo/deepseek-harness) | 1 | 112 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |

## Modification categories

| Category | Changed paths |
| --- | ---: |
| docs | 1,848 |
| harness-core | 1,023 |
| dependencies | 1,016 |
| ui-and-apps | 911 |
| configuration | 812 |
| tests | 466 |
| other | 140 |
| ci-and-build | 53 |
| tools-and-scripts | 50 |
| agents-and-skills | 37 |

## Influence order

| Rank | Fork | Stars | Owner reputation | Repo influence | Overall | Ahead | Changed files | Deep status | One-sentence evidence |
| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | --- | --- |
| 1 | [salathleizhang/deepseek-harness-desktop](https://github.com/salathleizhang/deepseek-harness-desktop) | 97 | 36.0 (observed) | 74.989 | 59.393 | 42 | 300 | ok | 新增约 42 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“Native desktop app for DeepSeek Harness — an Electron shell that runs the harness locally and hosts the official Web GUI unchanged”。 |
| 2 | [fendouai/deepseek-harness-desktop](https://github.com/fendouai/deepseek-harness-desktop) | 1 | 72.1 (observed) | 45.330 | 56.032 | 10 | 123 | ok | 新增约 10 个提交并修改 123 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 3 | [himomohi/deepseek-harness](https://github.com/himomohi/deepseek-harness) | 1 | 46.5 (observed) | 51.023 | 49.221 | 36 | 300 | ok | 新增约 36 个提交并修改 300 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 4 | [bojieli/deepseek-harness](https://github.com/bojieli/deepseek-harness) | 1 | 81.4 (observed) | 25.918 | 48.108 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 5 | [alexdolbun/deepseek-harness](https://github.com/alexdolbun/deepseek-harness) | 1 | 80.0 (observed) | 25.918 | 47.566 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 6 | [zchuhui/deepseek-harness](https://github.com/zchuhui/deepseek-harness) | 1 | 48.7 (observed) | 46.774 | 47.559 | 7 | 300 | ok | 新增约 7 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 7 | [G36maid/deepseek-harness](https://github.com/G36maid/deepseek-harness) | 12 | 54.4 (observed) | 42.350 | 47.186 | 19 | 300 | ok | 新增约 19 个提交并修改 300 个文件，主要涉及 配置、文档；目标线索是“DeepSeek Harness 繁體中文版 (zh-TW) — Everything is a Plugin”。 |
| 8 | [Sakana-yuyu/deepseek-harness-desktop](https://github.com/Sakana-yuyu/deepseek-harness-desktop) | 21 | 35.5 (observed) | 54.401 | 46.845 | 14 | 81 | ok | 新增约 14 个提交并修改 81 个文件，主要涉及 配置、文档、CI/构建、UI/应用层；目标线索是“Rust构建的客户端，体积更小，更方便，Mac，win，linux已完成”。 |
| 9 | [stophobia/deepseek-harness](https://github.com/stophobia/deepseek-harness) | 2 | 70.7 (observed) | 29.455 | 45.936 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 10 | [exposir/deepseek-harness](https://github.com/exposir/deepseek-harness) | 1 | 52.3 (observed) | 39.274 | 44.476 | 9 | 13 | ok | 新增约 9 个提交并修改 13 个文件，主要涉及 文档、Harness 核心能力、测试；目标线索是“DeepSeek Harness”。 |
| 11 | [dorucioclea/deepseek-harness](https://github.com/dorucioclea/deepseek-harness) | 1 | 71.8 (observed) | 25.918 | 44.253 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 12 | [Skyearn/deepseek-harness-app](https://github.com/Skyearn/deepseek-harness-app) | 11 | 34.3 (observed) | 49.137 | 43.210 | 24 | 31 | ok | 新增约 24 个提交并修改 31 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness Desktop”。 |
| 13 | [realchenwenqiao/dash-fork](https://github.com/realchenwenqiao/dash-fork) | 1 | 37.1 (observed) | 45.508 | 42.150 | 35 | 38 | ok | 新增约 35 个提交并修改 38 个文件，主要涉及 文档、依赖、UI/应用层、其他文件；目标线索是“DASH — terminal-native TUI for DeepSeek Harness: Claude Code-style full-screen interface, multi-model switching, behavior-ledger rewind”。 |
| 14 | [rpmalouin/deepseek-harness](https://github.com/rpmalouin/deepseek-harness) | 8 | 34.9 (observed) | 46.620 | 41.931 | 4 | 31 | ok | 新增约 4 个提交并修改 31 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 15 | [v2hoping/deepseek-harness-desktop](https://github.com/v2hoping/deepseek-harness-desktop) | 1 | 36.4 (observed) | 45.028 | 41.570 | 15 | 73 | ok | 新增约 15 个提交并修改 73 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin. Supports desktop installation and DeepSeek account login”。 |
| 16 | [zhonghui5207/deepseek-harness-desktop](https://github.com/zhonghui5207/deepseek-harness-desktop) | 1 | 29.0 (observed) | 49.326 | 41.208 | 19 | 300 | ok | 新增约 19 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“DSH Desktop — an installable desktop distribution of DeepSeek Harness for macOS, Windows, and Linux”。 |
| 17 | [lixun910/deepseek-harness](https://github.com/lixun910/deepseek-harness) | 1 | 64.0 (observed) | 25.918 | 41.141 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 18 | [ouyangyipeng/dsh-desktop-upstream-archive](https://github.com/ouyangyipeng/dsh-desktop-upstream-archive) | 1 | 35.3 (observed) | 44.149 | 40.627 | 12 | 67 | ok | 新增约 12 个提交并修改 67 个文件，主要涉及 配置、文档、其他文件、依赖；目标线索是“Archived upstream fork that preceded the independent DS-Harness Desktop repository”。 |
| 19 | [shdeng/deepseek-harness-app](https://github.com/shdeng/deepseek-harness-app) | 1 | 31.3 (observed) | 46.858 | 40.615 | 10 | 220 | ok | 新增约 10 个提交并修改 220 个文件，主要涉及 配置、文档、其他文件、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 20 | [puppywang/deepseek-harness](https://github.com/puppywang/deepseek-harness) | 4 | 49.7 (observed) | 33.985 | 40.285 | 10 | 300 | ok | 新增约 10 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 21 | [Sailfishc/deepseek-harness](https://github.com/Sailfishc/deepseek-harness) | 1 | 61.2 (observed) | 25.918 | 40.036 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 22 | [Ajwyunsx/deepseek-harness-mobile](https://github.com/Ajwyunsx/deepseek-harness-mobile) | 4 | 36.6 (observed) | 41.535 | 39.552 | 7 | 40 | ok | 新增约 7 个提交并修改 40 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 23 | [ben-vargas/ai-deepseek-harness](https://github.com/ben-vargas/ai-deepseek-harness) | 1 | 59.6 (observed) | 25.918 | 39.402 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 24 | [TKaxv-7S/deepseek-harness](https://github.com/TKaxv-7S/deepseek-harness) | 1 | 59.4 (observed) | 25.918 | 39.297 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 25 | [rferrari/deepseek-harness](https://github.com/rferrari/deepseek-harness) | 1 | 58.8 (observed) | 25.918 | 39.066 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 26 | [BurtonQin/deepseek-harness](https://github.com/BurtonQin/deepseek-harness) | 1 | 58.2 (observed) | 25.918 | 38.837 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 27 | [happylin0x29a/deepseek-harness-desktop](https://github.com/happylin0x29a/deepseek-harness-desktop) | 4 | 34.6 (observed) | 41.452 | 38.726 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness desktop base on tauri”。 |
| 28 | [MarceloClaro/deepseek-harness](https://github.com/MarceloClaro/deepseek-harness) | 2 | 50.6 (observed) | 29.455 | 37.904 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 29 | [fisher158163/deepseek-harness](https://github.com/fisher158163/deepseek-harness) | 1 | 54.9 (observed) | 25.918 | 37.530 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 30 | [Ericsongyl/deepseek-harness](https://github.com/Ericsongyl/deepseek-harness) | 1 | 54.5 (observed) | 25.918 | 37.343 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 31 | [manuelapetsi/deepseek-harness](https://github.com/manuelapetsi/deepseek-harness) | 1 | 54.3 (observed) | 25.918 | 37.258 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 32 | [youshen2/deepseek-harness](https://github.com/youshen2/deepseek-harness) | 1 | 31.8 (observed) | 40.209 | 36.856 | 3 | 51 | ok | 新增约 3 个提交并修改 51 个文件，主要涉及 配置、文档、其他文件、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 33 | [0verL1nk/deepseek-harness](https://github.com/0verL1nk/deepseek-harness) | 0 | 31.6 (observed) | 40.154 | 36.744 | 29 | 59 | ok | 新增约 29 个提交并修改 59 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 34 | [lamost423/dsh-codex-experience](https://github.com/lamost423/dsh-codex-experience) | 1 | 16.4 (observed) | 49.410 | 36.223 | 29 | 204 | ok | 新增约 29 个提交并修改 204 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“Community DeepSeek Harness fork with Codex-style annotations, ephemeral side chat, and todo freshness enforcement”。 |
| 35 | [athif23/deepseek-harness](https://github.com/athif23/deepseek-harness) | 1 | 51.7 (observed) | 25.918 | 36.220 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 36 | [FSMargoo/deepseek-harness](https://github.com/FSMargoo/deepseek-harness) | 2 | 46.1 (observed) | 29.455 | 36.120 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 37 | [aimierbear/TinyWhale](https://github.com/aimierbear/TinyWhale) | 1 | 16.4 (observed) | 49.166 | 36.054 | 18 | 300 | ok | 新增约 18 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、CI/构建；目标线索是“TinyWhale — desktop-oriented MIT fork of DeepSeek Harness, with an Electron shell in desktop/”。 |
| 38 | [biyan113/deepseek-harness](https://github.com/biyan113/deepseek-harness) | 1 | 28.1 (observed) | 40.377 | 35.483 | 3 | 55 | ok | 新增约 3 个提交并修改 55 个文件，主要涉及 CI/构建、UI/应用层、文档、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 39 | [t479842598/deepseek-harness](https://github.com/t479842598/deepseek-harness) | 1 | 26.7 (observed) | 40.808 | 35.183 | 16 | 13 | ok | 新增约 16 个提交并修改 13 个文件，主要涉及 Harness 核心能力、测试；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 40 | [DailyR/deepseek-harness](https://github.com/DailyR/deepseek-harness) | 1 | 48.7 (observed) | 25.918 | 35.049 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 41 | [luolangaga/deepseek-harness](https://github.com/luolangaga/deepseek-harness) | 4 | 36.4 (observed) | 33.956 | 34.922 | 11 | 54 | ok | 新增约 11 个提交并修改 54 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 42 | [donstang/deepseek-harness](https://github.com/donstang/deepseek-harness) | 1 | 48.0 (observed) | 25.918 | 34.756 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 43 | [LCYLYM/deepseek-harness](https://github.com/LCYLYM/deepseek-harness) | 1 | 47.7 (observed) | 25.917 | 34.613 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 44 | [Razor87/deepseek-harness](https://github.com/Razor87/deepseek-harness) | 1 | 47.6 (observed) | 25.918 | 34.609 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 45 | [lkngin/deepseek-harness](https://github.com/lkngin/deepseek-harness) | 1 | 47.5 (observed) | 25.918 | 34.531 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 46 | [criapa/deepseek-harness](https://github.com/criapa/deepseek-harness) | 1 | 47.3 (observed) | 25.918 | 34.480 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 47 | [zhanglunet/deepseek-harness](https://github.com/zhanglunet/deepseek-harness) | 0 | 55.7 (observed) | 19.999 | 34.281 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 48 | [yomaser/deepseek-harness](https://github.com/yomaser/deepseek-harness) | 1 | 46.2 (observed) | 25.918 | 34.051 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 49 | [nydia/deepseek-harness](https://github.com/nydia/deepseek-harness) | 1 | 46.2 (observed) | 25.918 | 34.017 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 50 | [odonzyk/deepseek-harness](https://github.com/odonzyk/deepseek-harness) | 1 | 44.4 (observed) | 25.918 | 33.330 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 51 | [boktoday/deepseek-harness](https://github.com/boktoday/deepseek-harness) | 1 | 44.2 (observed) | 25.918 | 33.212 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 52 | [lasme-ephrem/LasmeX](https://github.com/lasme-ephrem/LasmeX) | 1 | 16.8 (observed) | 44.073 | 33.175 | 2 | 300 | ok | 新增约 2 个提交并修改 300 个文件，主要涉及 配置、文档；目标线索是“Harness agentique open source, extensible et francophone par défaut”。 |
| 53 | [Anyaoha/deepseek-harness](https://github.com/Anyaoha/deepseek-harness) | 1 | 44.0 (observed) | 25.918 | 33.134 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 54 | [vkn129/deepseek-harness](https://github.com/vkn129/deepseek-harness) | 1 | 43.9 (observed) | 25.918 | 33.110 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 55 | [porarrirr/deepseek-harness-japanese](https://github.com/porarrirr/deepseek-harness-japanese) | 0 | 19.3 (observed) | 42.233 | 33.070 | 2 | 88 | ok | 新增约 2 个提交并修改 88 个文件，主要涉及 配置、文档、UI/应用层、依赖；目标线索是“DeepSeek Harness”。 |
| 56 | [2404589803/deepseek-harness](https://github.com/2404589803/deepseek-harness) | 1 | 43.8 (observed) | 25.918 | 33.069 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 57 | [shenyimings/deepseek-harness](https://github.com/shenyimings/deepseek-harness) | 1 | 43.7 (observed) | 25.918 | 33.033 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 58 | [warm-maple/deepseek-harness_exe](https://github.com/warm-maple/deepseek-harness_exe) | 0 | 8.8 (observed) | 49.096 | 32.961 | 10 | 300 | ok | 新增约 10 个提交并修改 300 个文件，主要涉及 配置、文档、agent/skill 能力、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 59 | [roadlittledawn/deepseek-harness](https://github.com/roadlittledawn/deepseek-harness) | 1 | 42.9 (observed) | 25.918 | 32.704 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 60 | [achristofaro/deepseek-harness](https://github.com/achristofaro/deepseek-harness) | 1 | 42.6 (observed) | 25.918 | 32.591 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 61 | [nostalgia296/deepseek-harness-termux](https://github.com/nostalgia296/deepseek-harness-termux) | 1 | 23.6 (observed) | 38.290 | 32.411 | 2 | 33 | ok | 新增约 2 个提交并修改 33 个文件，主要涉及 配置、文档、测试、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 62 | [mnky4a6/deepseek-harness](https://github.com/mnky4a6/deepseek-harness) | 1 | 42.1 (observed) | 25.918 | 32.408 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 63 | [phong711/deepseek-harness](https://github.com/phong711/deepseek-harness) | 1 | 42.1 (observed) | 25.918 | 32.402 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 64 | [liwuli/deepseek-harness-desktop](https://github.com/liwuli/deepseek-harness-desktop) | 1 | 23.9 (observed) | 37.865 | 32.266 | 2 | 28 | ok | 新增约 2 个提交并修改 28 个文件，主要涉及 CI/构建、其他文件、文档、依赖；目标线索是“DeepSeek Harness desktop”。 |
| 65 | [BJTU-Netcomm/deepseek-harness-aiops](https://github.com/BJTU-Netcomm/deepseek-harness-aiops) | 0 | 39.4 (observed) | 27.371 | 32.199 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness for aiops: Everything is a Plugin”。 |
| 66 | [Yihong89/deepseek-harness](https://github.com/Yihong89/deepseek-harness) | 2 | 36.3 (observed) | 29.455 | 32.187 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 67 | [Cyenoch/deepseek-harness](https://github.com/Cyenoch/deepseek-harness) | 1 | 41.4 (observed) | 26.016 | 32.170 | 13 | 300 | ok | 新增约 13 个提交并修改 300 个文件，主要涉及 配置、文档、agent/skill 能力、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 68 | [tzy168/deepseek-harness](https://github.com/tzy168/deepseek-harness) | 1 | 23.8 (observed) | 37.564 | 32.040 | 2 | 25 | ok | 新增约 2 个提交并修改 25 个文件，主要涉及 配置、文档、Harness 核心能力、测试；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 69 | [missuzhang/deepseek-harness](https://github.com/missuzhang/deepseek-harness) | 1 | 41.2 (observed) | 25.918 | 32.014 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 70 | [Mike-7777777/deepseek-harness](https://github.com/Mike-7777777/deepseek-harness) | 1 | 40.6 (observed) | 25.918 | 31.801 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 71 | [mallocxw/deepseek-harness](https://github.com/mallocxw/deepseek-harness) | 1 | 40.0 (observed) | 25.918 | 31.543 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 72 | [xiaolangde/deepseek-harness](https://github.com/xiaolangde/deepseek-harness) | 1 | 39.7 (observed) | 25.967 | 31.447 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 73 | [drscrewdriver/deepseek-harness](https://github.com/drscrewdriver/deepseek-harness) | 1 | 38.7 (observed) | 25.918 | 31.021 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 74 | [DeepThinkingZhouLiu/Deepseek-Harness-RSI](https://github.com/DeepThinkingZhouLiu/Deepseek-Harness-RSI) | 1 | 38.3 (observed) | 26.037 | 30.923 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 75 | [Vitaminaq/deepseek-harness](https://github.com/Vitaminaq/deepseek-harness) | 1 | 38.0 (observed) | 25.951 | 30.752 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 76 | [Tyler-R-Kendrick/deepseek-harness](https://github.com/Tyler-R-Kendrick/deepseek-harness) | 1 | 38.0 (observed) | 25.918 | 30.735 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 77 | [DogeJian/deepseek-harness](https://github.com/DogeJian/deepseek-harness) | 1 | 37.9 (observed) | 25.918 | 30.694 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 78 | [enbideren/deepseek-harness](https://github.com/enbideren/deepseek-harness) | 1 | 37.8 (observed) | 25.918 | 30.687 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 79 | [Yuan-lai-ru-ci/deepseek-harness-desktop](https://github.com/Yuan-lai-ru-ci/deepseek-harness-desktop) | 1 | 16.2 (observed) | 40.132 | 30.570 | 8 | 21 | ok | 新增约 8 个提交并修改 21 个文件，主要涉及 文档、UI/应用层、依赖；目标线索是“随手做的DSH桌面版，需要下载原包，在桌面上方便打开，可以装插件”。 |
| 80 | [xiansheng888/deepseek-harness](https://github.com/xiansheng888/deepseek-harness) | 1 | 37.4 (observed) | 25.918 | 30.525 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 81 | [mgrillo75/deepseek-harness](https://github.com/mgrillo75/deepseek-harness) | 1 | 37.3 (observed) | 25.918 | 30.473 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 82 | [Linmoqian/deepseek-harness-cli](https://github.com/Linmoqian/deepseek-harness-cli) | 1 | 36.2 (observed) | 25.918 | 30.032 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness-cli版本”。 |
| 83 | [srwang0506/deepseek-harness](https://github.com/srwang0506/deepseek-harness) | 1 | 24.3 (observed) | 33.541 | 29.828 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 84 | [SamboHassan/deepseek-harness](https://github.com/SamboHassan/deepseek-harness) | 1 | 35.5 (observed) | 25.918 | 29.735 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 85 | [alexdeweb/deepseek-harness](https://github.com/alexdeweb/deepseek-harness) | 1 | 35.0 (observed) | 25.918 | 29.536 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 86 | [rvndnishad-work/deepseek-harness](https://github.com/rvndnishad-work/deepseek-harness) | 1 | 34.9 (observed) | 25.918 | 29.526 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 87 | [coder-v0/deepseek-harness](https://github.com/coder-v0/deepseek-harness) | 1 | 34.9 (observed) | 25.918 | 29.523 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 88 | [devin2255/deepseek-harness-desktop](https://github.com/devin2255/deepseek-harness-desktop) | 1 | 34.6 (observed) | 25.918 | 29.409 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 89 | [JayTing511/deepseek-harness](https://github.com/JayTing511/deepseek-harness) | 1 | 34.3 (observed) | 25.918 | 29.278 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 90 | [luoxunhao/deepseek-harness](https://github.com/luoxunhao/deepseek-harness) | 1 | 34.0 (observed) | 25.918 | 29.142 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 91 | [playboy662/deepseek-harness](https://github.com/playboy662/deepseek-harness) | 1 | 33.7 (observed) | 25.918 | 29.029 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 92 | [zenghuan/deepseek-harness](https://github.com/zenghuan/deepseek-harness) | 1 | 33.4 (observed) | 25.918 | 28.926 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 93 | [yazzang-homelab/deepseek-harness](https://github.com/yazzang-homelab/deepseek-harness) | 2 | 16.5 (observed) | 36.955 | 28.781 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 94 | [badestgod/deepseek-harness](https://github.com/badestgod/deepseek-harness) | 1 | 33.0 (observed) | 25.918 | 28.766 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 95 | [houkang/deepseek-harness](https://github.com/houkang/deepseek-harness) | 1 | 32.8 (observed) | 25.918 | 28.688 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness”。 |
| 96 | [cq2021-coder/deepseek-harness-desktop](https://github.com/cq2021-coder/deepseek-harness-desktop) | 1 | 32.7 (observed) | 25.983 | 28.674 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“使用 tauri 为 DeepSeek Harness 生态打造的现代化桌面端应用”。 |
| 97 | [HybridMAS/deepseek-harness](https://github.com/HybridMAS/deepseek-harness) | 1 | 32.7 (observed) | 25.918 | 28.625 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 98 | [China-MY/deepseek-harness](https://github.com/China-MY/deepseek-harness) | 1 | 32.6 (observed) | 25.918 | 28.578 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 99 | [monikalnbo/deepseek-harness](https://github.com/monikalnbo/deepseek-harness) | 1 | 16.9 (observed) | 36.231 | 28.519 | 4 | 8 | ok | 新增约 4 个提交并修改 8 个文件，主要涉及 文档、其他文件、Harness 核心能力；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 100 | [Zn070515/deepseek-harness](https://github.com/Zn070515/deepseek-harness) | 1 | 13.4 (observed) | 38.513 | 28.462 | 5 | 17 | ok | 新增约 5 个提交并修改 17 个文件，主要涉及 Harness 核心能力、测试；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 101 | [tomchon/deepseek-harness](https://github.com/tomchon/deepseek-harness) | 1 | 32.0 (observed) | 25.918 | 28.351 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 102 | [valentinshenfeld/deepseek-harness](https://github.com/valentinshenfeld/deepseek-harness) | 1 | 31.9 (observed) | 25.918 | 28.313 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 103 | [MasterToycode/deepseek-harness](https://github.com/MasterToycode/deepseek-harness) | 1 | 31.9 (observed) | 25.918 | 28.292 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 104 | [HossamTabana/deepseek-harness](https://github.com/HossamTabana/deepseek-harness) | 1 | 31.3 (observed) | 25.918 | 28.083 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 105 | [slamsmart/deepseek-harness](https://github.com/slamsmart/deepseek-harness) | 1 | 30.6 (observed) | 25.918 | 27.794 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 106 | [huiliyi37/deepseek-harness](https://github.com/huiliyi37/deepseek-harness) | 2 | 25.1 (observed) | 29.455 | 27.723 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 107 | [maigadohcrypto/deepseek-harness](https://github.com/maigadohcrypto/deepseek-harness) | 1 | 30.2 (observed) | 25.918 | 27.645 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 108 | [sdkwork-ai/deepseek-harness-desktop](https://github.com/sdkwork-ai/deepseek-harness-desktop) | 4 | 17.9 (observed) | 34.029 | 27.581 | 43 | 300 | ok | 新增约 43 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 109 | [wellfuture/deepseek-harness](https://github.com/wellfuture/deepseek-harness) | 1 | 30.1 (observed) | 25.918 | 27.580 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 110 | [Kiowx/deepseek-harness](https://github.com/Kiowx/deepseek-harness) | 2 | 24.6 (observed) | 29.497 | 27.527 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 111 | [HugoluizMTB/deepseek-harness](https://github.com/HugoluizMTB/deepseek-harness) | 1 | 29.9 (observed) | 25.918 | 27.494 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 112 | [HelloNicoo/deepseek-harness](https://github.com/HelloNicoo/deepseek-harness) | 1 | 29.7 (observed) | 25.918 | 27.428 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 113 | [misshehe/deepseek-harness](https://github.com/misshehe/deepseek-harness) | 1 | 29.7 (observed) | 25.918 | 27.420 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 114 | [tranvantrung95/deepseek-harness](https://github.com/tranvantrung95/deepseek-harness) | 1 | 29.3 (observed) | 25.918 | 27.262 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 115 | [NewMFF/deepseek-harness](https://github.com/NewMFF/deepseek-harness) | 1 | 29.1 (observed) | 25.918 | 27.192 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 116 | [zdy-ai/deepseek-harness](https://github.com/zdy-ai/deepseek-harness) | 1 | 29.0 (observed) | 25.918 | 27.169 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 117 | [oscarlius/deepseek-harness](https://github.com/oscarlius/deepseek-harness) | 1 | 28.9 (observed) | 25.918 | 27.116 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 118 | [TomYang1024/deepseek-harness](https://github.com/TomYang1024/deepseek-harness) | 1 | 28.8 (observed) | 25.918 | 27.058 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 119 | [cFqr-lang/deepseek-harness](https://github.com/cFqr-lang/deepseek-harness) | 1 | 5.1 (observed) | 41.657 | 27.045 | 5 | 57 | ok | 新增约 5 个提交并修改 57 个文件，主要涉及 UI/应用层、Harness 核心能力、配置、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 120 | [KinomotoMio/deepseek-harness](https://github.com/KinomotoMio/deepseek-harness) | 1 | 28.7 (observed) | 25.918 | 27.033 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 121 | [linfunss/deepseek-harness](https://github.com/linfunss/deepseek-harness) | 1 | 28.4 (observed) | 25.918 | 26.921 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 122 | [dailin3/deepseek-harness](https://github.com/dailin3/deepseek-harness) | 1 | 28.2 (observed) | 25.918 | 26.834 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 123 | [xiaosenho/deepseek-harness](https://github.com/xiaosenho/deepseek-harness) | 1 | 16.3 (observed) | 33.472 | 26.610 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 124 | [zng8418/deepseek-harness](https://github.com/zng8418/deepseek-harness) | 1 | 27.6 (observed) | 25.918 | 26.605 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 125 | [markisaac/deepseek-harness](https://github.com/markisaac/deepseek-harness) | 1 | 27.5 (observed) | 25.918 | 26.564 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 126 | [iKing/deepseek-harness](https://github.com/iKing/deepseek-harness) | 1 | 27.5 (observed) | 25.918 | 26.533 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 127 | [BlackRosePetals/deepseek-harness](https://github.com/BlackRosePetals/deepseek-harness) | 1 | 27.3 (observed) | 25.918 | 26.464 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 128 | [imhieu/deepseek-harness](https://github.com/imhieu/deepseek-harness) | 1 | 26.7 (observed) | 25.918 | 26.247 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 129 | [Helpless5699/deepseek-harness](https://github.com/Helpless5699/deepseek-harness) | 1 | 26.7 (observed) | 25.918 | 26.225 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 130 | [melkharbili/deepseek-harness](https://github.com/melkharbili/deepseek-harness) | 1 | 26.5 (observed) | 25.918 | 26.163 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 131 | [4evour/deepseek-harness](https://github.com/4evour/deepseek-harness) | 1 | 26.5 (observed) | 25.918 | 26.137 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 132 | [KevinSCUTer/deepseek-harness](https://github.com/KevinSCUTer/deepseek-harness) | 1 | 25.8 (observed) | 25.918 | 25.887 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 133 | [BobcGn/deepseek-harness-app](https://github.com/BobcGn/deepseek-harness-app) | 1 | 25.7 (observed) | 26.018 | 25.882 | 14 | 31 | ok | 新增约 14 个提交并修改 31 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 134 | [QingGeLaiYe/deepseek-harness](https://github.com/QingGeLaiYe/deepseek-harness) | 1 | 25.6 (observed) | 25.918 | 25.775 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 135 | [djhh555/deepseek-sightline](https://github.com/djhh555/deepseek-sightline) | 1 | 5.8 (observed) | 39.020 | 25.737 | 2 | 43 | ok | 新增约 2 个提交并修改 43 个文件，主要涉及 文档、UI/应用层、依赖、Harness 核心能力；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 136 | [yx54hego-cloud/deepseek-harness](https://github.com/yx54hego-cloud/deepseek-harness) | 7 | 7.0 (observed) | 38.108 | 25.670 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 137 | [WyrdWerk/deepseek-harness](https://github.com/WyrdWerk/deepseek-harness) | 1 | 25.1 (observed) | 26.040 | 25.650 | 13 | 272 | ok | 新增约 13 个提交并修改 272 个文件，主要涉及 配置、文档、CI/构建、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 138 | [deveuper/deepseek-harness](https://github.com/deveuper/deepseek-harness) | 1 | 25.0 (observed) | 25.929 | 25.570 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 139 | [yueyucaotian/deepseek-harness](https://github.com/yueyucaotian/deepseek-harness) | 1 | 24.8 (observed) | 25.918 | 25.455 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 140 | [MinerBin/deepseek-harness](https://github.com/MinerBin/deepseek-harness) | 1 | 24.5 (observed) | 25.918 | 25.353 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 141 | [18217778896/deepseek-harness](https://github.com/18217778896/deepseek-harness) | 1 | 24.2 (observed) | 25.918 | 25.242 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 142 | [leixiaochenShen/deepseek-harness](https://github.com/leixiaochenShen/deepseek-harness) | 1 | 24.0 (observed) | 25.918 | 25.156 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 143 | [heleileimail-cmyk/deepseek-harness](https://github.com/heleileimail-cmyk/deepseek-harness) | 1 | 5.6 (observed) | 38.085 | 25.087 | 3 | 22 | ok | 新增约 3 个提交并修改 22 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 144 | [zkh11123/deepseek-harness](https://github.com/zkh11123/deepseek-harness) | 1 | 23.3 (observed) | 25.918 | 24.872 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 145 | [jackma5477001/deepseek-harness-desktop](https://github.com/jackma5477001/deepseek-harness-desktop) | 1 | 2.4 (observed) | 39.762 | 24.816 | 2 | 58 | ok | 新增约 2 个提交并修改 58 个文件，主要涉及 配置、文档、其他文件、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 146 | [lihaidog/deepseek-harness](https://github.com/lihaidog/deepseek-harness) | 1 | 23.1 (observed) | 25.918 | 24.772 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 147 | [w74srm/deepseek-harness](https://github.com/w74srm/deepseek-harness) | 1 | 22.9 (observed) | 25.918 | 24.724 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 148 | [xiaofeng930415/deepseek-harness](https://github.com/xiaofeng930415/deepseek-harness) | 1 | 22.7 (observed) | 25.918 | 24.638 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 149 | [wuyuanjiang1/dsh2wechat_plugin](https://github.com/wuyuanjiang1/dsh2wechat_plugin) | 1 | 9.1 (observed) | 34.967 | 24.623 | 1 | 14 | ok | 新增约 1 个提交并修改 14 个文件，主要涉及 文档、Harness 核心能力、配置、依赖；目标线索是“deepseek-harness”。 |
| 150 | [HHHHH-GIT/Deepseek-HPD-Harness](https://github.com/HHHHH-GIT/Deepseek-HPD-Harness) | 1 | 22.4 (observed) | 26.001 | 24.566 | 2 | 133 | ok | 新增约 2 个提交并修改 133 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek HPD Harness: Everything is a Plugin. A more powerful Harness with HPD architecture”。 |
| 151 | [longman888/deepseek-harness](https://github.com/longman888/deepseek-harness) | 1 | 22.5 (observed) | 25.918 | 24.548 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 152 | [duliangkuan/deepseek-harness](https://github.com/duliangkuan/deepseek-harness) | 1 | 22.2 (observed) | 25.918 | 24.428 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 153 | [MixGeeker/deepseek-harness](https://github.com/MixGeeker/deepseek-harness) | 1 | 22.1 (observed) | 25.918 | 24.404 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 154 | [Beam-wi/deepseek-harness](https://github.com/Beam-wi/deepseek-harness) | 1 | 22.0 (observed) | 25.918 | 24.364 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 155 | [Octo-o-o-o/deepseek-harness-desktop](https://github.com/Octo-o-o-o/deepseek-harness-desktop) | 1 | 21.8 (observed) | 26.040 | 24.329 | 78 | 286 | ok | 新增约 78 个提交并修改 286 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“非官方桌面版 · Unofficial desktop shell for DeepSeek Harness — double-click, no Node, no terminal. Signed & notarized on macOS. Tauri shell, official MIT core untouched”。 |
| 156 | [liyuera/deepseek-harness](https://github.com/liyuera/deepseek-harness) | 1 | 12.7 (observed) | 31.909 | 24.232 | 2 | 2 | ok | 新增约 2 个提交并修改 2 个文件，主要涉及 文档；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 157 | [Linyiwei895178/deepseek-harness](https://github.com/Linyiwei895178/deepseek-harness) | 1 | 21.7 (observed) | 25.918 | 24.226 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 158 | [HTree-ZX/deepseek-harness](https://github.com/HTree-ZX/deepseek-harness) | 1 | 21.5 (observed) | 25.918 | 24.137 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 159 | [suiyuebaobao/deepseek-harness-gui](https://github.com/suiyuebaobao/deepseek-harness-gui) | 2 | 16.1 (observed) | 29.492 | 24.118 | 2 | 52 | ok | 新增约 2 个提交并修改 52 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“Windows desktop fork of DeepSeek Harness, packaged with Tauri while preserving the full Web profile and plugin runtime”。 |
| 160 | [GTC2080/deepseek-harness](https://github.com/GTC2080/deepseek-harness) | 1 | 21.2 (observed) | 26.004 | 24.070 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness 桌面端：基于 Tauri，支持 macOS 与 Windows；源码位于 desktop 分支”。 |
| 161 | [wingthedream/deepseek-harness](https://github.com/wingthedream/deepseek-harness) | 1 | 21.2 (observed) | 25.918 | 24.016 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 162 | [shr123456/deepseek-harness](https://github.com/shr123456/deepseek-harness) | 1 | 20.9 (observed) | 25.918 | 23.905 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 163 | [007M7/deepseek-harness](https://github.com/007M7/deepseek-harness) | 1 | 20.4 (observed) | 25.918 | 23.717 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“我永远喜欢deepseek！！！”。 |
| 164 | [flaqai/open-deepseek-harness-desktop](https://github.com/flaqai/open-deepseek-harness-desktop) | 1 | 20.4 (observed) | 25.918 | 23.713 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“Open Source Desktop for DeepSeek Harness. DeepSeek Harness: Everything is a Plugin”。 |
| 165 | [yyy1mu/deepseek-harness](https://github.com/yyy1mu/deepseek-harness) | 0 | 29.3 (observed) | 20.000 | 23.704 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 166 | [Captain-Dodger/deepseek-harness](https://github.com/Captain-Dodger/deepseek-harness) | 0 | 17.9 (observed) | 27.371 | 23.573 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 167 | [xbzhangyq/deepseek-harness](https://github.com/xbzhangyq/deepseek-harness) | 1 | 19.7 (observed) | 25.918 | 23.431 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 168 | [x1095907352/deepseek-harness](https://github.com/x1095907352/deepseek-harness) | 1 | 19.5 (observed) | 25.918 | 23.364 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 169 | [Solizardking/deepseek-harness](https://github.com/Solizardking/deepseek-harness) | 0 | 28.3 (observed) | 20.000 | 23.315 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 170 | [Zguigo00/deepseek-harness](https://github.com/Zguigo00/deepseek-harness) | 1 | 19.2 (observed) | 25.918 | 23.230 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 171 | [MrGXxx/deepseek-harness](https://github.com/MrGXxx/deepseek-harness) | 1 | 19.2 (observed) | 25.918 | 23.227 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 172 | [zhanggoodbao/deepseek-harness](https://github.com/zhanggoodbao/deepseek-harness) | 1 | 18.7 (observed) | 25.918 | 23.043 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 173 | [tinhocdaimo2015/deepseek-harness](https://github.com/tinhocdaimo2015/deepseek-harness) | 1 | 18.6 (observed) | 25.918 | 22.982 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 174 | [peter13990/deepseek-harness](https://github.com/peter13990/deepseek-harness) | 1 | 18.6 (observed) | 25.918 | 22.974 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 175 | [WuJunNan-fjy/deepseek-harness](https://github.com/WuJunNan-fjy/deepseek-harness) | 1 | 18.5 (observed) | 25.918 | 22.959 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 176 | [CatchCatOoO/deepseek-harness](https://github.com/CatchCatOoO/deepseek-harness) | 1 | 18.4 (observed) | 25.927 | 22.933 | 4 | 300 | ok | 新增约 4 个提交并修改 300 个文件，主要涉及 文档、配置、agent/skill 能力；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 177 | [Lostsoul-namespace/deepseek-harness](https://github.com/Lostsoul-namespace/deepseek-harness) | 1 | 18.4 (observed) | 25.918 | 22.912 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 178 | [GZZ-523/deepseek-harness](https://github.com/GZZ-523/deepseek-harness) | 1 | 18.3 (observed) | 25.918 | 22.854 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 179 | [Cute-chen/deepseek-harness-app](https://github.com/Cute-chen/deepseek-harness-app) | 1 | 18.2 (observed) | 25.918 | 22.816 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 180 | [jinchao-bst/deepseek-harness](https://github.com/jinchao-bst/deepseek-harness) | 1 | 18.2 (observed) | 25.918 | 22.814 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 181 | [ousers/deepseek-harness](https://github.com/ousers/deepseek-harness) | 1 | 18.0 (observed) | 25.918 | 22.758 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 182 | [ling0zero0/deepseek-harness](https://github.com/ling0zero0/deepseek-harness) | 1 | 18.0 (observed) | 25.918 | 22.739 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 183 | [FlyingSama/deepseek-harness](https://github.com/FlyingSama/deepseek-harness) | 1 | 17.9 (observed) | 25.918 | 22.729 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 184 | [lucy971326/deepseek-harness](https://github.com/lucy971326/deepseek-harness) | 1 | 17.8 (observed) | 25.918 | 22.690 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 185 | [codelife2020/deepseek-harness](https://github.com/codelife2020/deepseek-harness) | 1 | 17.8 (observed) | 25.918 | 22.668 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 186 | [guihuatu2022/deepseek-harness](https://github.com/guihuatu2022/deepseek-harness) | 1 | 17.6 (observed) | 25.918 | 22.580 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 187 | [DreamShepherd2006/deepseek-harness](https://github.com/DreamShepherd2006/deepseek-harness) | 0 | 15.3 (observed) | 27.371 | 22.550 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 188 | [studioburnside/deepseek-harness-internal](https://github.com/studioburnside/deepseek-harness-internal) | 1 | 17.3 (observed) | 25.918 | 22.451 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 189 | [Erichy777/deepseek-harness](https://github.com/Erichy777/deepseek-harness) | 1 | 16.9 (observed) | 25.918 | 22.293 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 190 | [zilaliang/deepseek-harness](https://github.com/zilaliang/deepseek-harness) | 1 | 16.8 (observed) | 25.918 | 22.272 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 191 | [chyl00/deepseek-harness](https://github.com/chyl00/deepseek-harness) | 1 | 16.7 (observed) | 25.918 | 22.247 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 192 | [Lyowisee/deepseek-harness](https://github.com/Lyowisee/deepseek-harness) | 1 | 16.7 (observed) | 25.918 | 22.221 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 193 | [wolone/deepseek-harness-desktop](https://github.com/wolone/deepseek-harness-desktop) | 0 | 25.5 (observed) | 20.000 | 22.218 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 194 | [MK6657/deepseek-harness](https://github.com/MK6657/deepseek-harness) | 1 | 16.6 (observed) | 25.918 | 22.209 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“小男梁agent”。 |
| 195 | [zy220/deepseek-harness](https://github.com/zy220/deepseek-harness) | 1 | 16.5 (observed) | 25.918 | 22.145 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“zy的ds-harness个人仓”。 |
| 196 | [yuzih888/deepseek-harness](https://github.com/yuzih888/deepseek-harness) | 1 | 16.5 (observed) | 25.918 | 22.143 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 197 | [MrNQC/deepseek-harness](https://github.com/MrNQC/deepseek-harness) | 1 | 16.4 (observed) | 25.918 | 22.091 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 198 | [SpxZhu/deepseek-harness](https://github.com/SpxZhu/deepseek-harness) | 1 | 16.1 (observed) | 25.954 | 22.028 | 2 | 24 | ok | 新增约 2 个提交并修改 24 个文件，主要涉及 CI/构建、UI/应用层、文档、配置；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 199 | [EdwardXIE6666/deepseek-harness](https://github.com/EdwardXIE6666/deepseek-harness) | 1 | 16.2 (observed) | 25.918 | 22.012 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 200 | [shijiejintoulwh/deepseek-harness](https://github.com/shijiejintoulwh/deepseek-harness) | 1 | 15.9 (observed) | 26.028 | 21.965 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |

> Showing the first 200 rows here; `11,117` rows are preserved in `index/forks.jsonl` and `docs/data/forks.json`.

## Interpretation

The collector records every public Fork returned by the paginated endpoint. Deep compare, recent commits, and README metadata are rotated by a per-run budget because GitHub rate limits make an unbounded daily deep audit impractical for a network of this size. Use `python3 scripts/collect_forks.py --deep-scan-all` only when the available token and request budget are sufficient.
