# DeepSeek Harness Fork Network

- Dataset version: `v20260815T212955Z`
- Public Fork records: **11,113**
- Ranking filter: **0+ stars**; observed Fork identities: **11,113**; filtered out of ranking: **0**.
- Ever deep-scanned: **317 / 11,113** (2.85%); pending: **10,796**; conservative backfill ETA: **68 daily runs**.
- Deep-scanned successfully in the current projection: **171**; compare responses retained: **317**
- Fork rows with public owner reputation observed: **300**; the current ranking pool applies a configurable minimum-Star filter.
- Scope: public Forks returned by GitHub REST API pagination for `deepseek-ai/deepseek-harness`.
- Raw evidence is collected under `data/raw/forks/`; the [latest compressed SQLite snapshot](https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin/releases/download/dataset-latest/aggregator-full.sqlite3.zst) includes the fork tables and raw JSON payloads. Unpack it with `zstd -d aggregator-full.sqlite3.zst -o aggregator-full.sqlite3`.
- Searchable browser: `docs/forks.html`; compact catalog: `docs/data/fork-catalog.json`; complete machine-readable ranking: `index/forks.jsonl`.
- `overall score = repository influence 60% + public-account reputation 40%` when the profile is observed; missing profile signals are not treated as zero. This is a public-signal ordering aid, not a quality, safety, integrity, or endorsement claim.

## GitHub star order

| Star rank | Fork | Stars | Composite rank | Audit | Evidence |
| ---: | --- | ---: | ---: | --- | --- |
| 1 | [salathleizhang/deepseek-harness-desktop](https://github.com/salathleizhang/deepseek-harness-desktop) | 97 | 1 | audited | 新增约 42 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“Native desktop app for DeepSeek Harness — an Electron shell that runs the harness locally and hosts the official Web GUI unchanged”。 |
| 2 | [Sakana-yuyu/deepseek-harness-desktop](https://github.com/Sakana-yuyu/deepseek-harness-desktop) | 21 | 6 | audited | 新增约 14 个提交并修改 81 个文件，主要涉及 配置、文档、CI/构建、UI/应用层；目标线索是“Rust构建的客户端，体积更小，更方便，Mac，win，linux已完成”。 |
| 3 | [G36maid/deepseek-harness](https://github.com/G36maid/deepseek-harness) | 12 | 5 | audited | 新增约 19 个提交并修改 300 个文件，主要涉及 配置、文档；目标线索是“DeepSeek Harness 繁體中文版 (zh-TW) — Everything is a Plugin”。 |
| 4 | [Skyearn/deepseek-harness-app](https://github.com/Skyearn/deepseek-harness-app) | 11 | 11 | audited | 新增约 24 个提交并修改 31 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness Desktop”。 |
| 5 | [rpmalouin/deepseek-harness](https://github.com/rpmalouin/deepseek-harness) | 8 | 13 | audited | 新增约 4 个提交并修改 31 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 6 | [yx54hego-cloud/deepseek-harness](https://github.com/yx54hego-cloud/deepseek-harness) | 7 | 128 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 7 | [Ajwyunsx/deepseek-harness-mobile](https://github.com/Ajwyunsx/deepseek-harness-mobile) | 4 | 18 | audited | 新增约 7 个提交并修改 40 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 8 | [happylin0x29a/deepseek-harness-desktop](https://github.com/happylin0x29a/deepseek-harness-desktop) | 4 | 23 | audited | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness desktop base on tauri”。 |
| 9 | [luolangaga/deepseek-harness](https://github.com/luolangaga/deepseek-harness) | 4 | 36 | audited | 新增约 11 个提交并修改 54 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 10 | [puppywang/deepseek-harness](https://github.com/puppywang/deepseek-harness) | 4 | 16 | audited | 新增约 10 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 11 | [sdkwork-ai/deepseek-harness-desktop](https://github.com/sdkwork-ai/deepseek-harness-desktop) | 4 | 102 | audited | 新增约 43 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 12 | [yazzang-homelab/deepseek-harness](https://github.com/yazzang-homelab/deepseek-harness) | 2 | 87 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 13 | [FSMargoo/deepseek-harness](https://github.com/FSMargoo/deepseek-harness) | 2 | 30 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 14 | [huiliyi37/deepseek-harness](https://github.com/huiliyi37/deepseek-harness) | 2 | 100 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 15 | [Kiowx/deepseek-harness](https://github.com/Kiowx/deepseek-harness) | 2 | 104 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 16 | [MarceloClaro/deepseek-harness](https://github.com/MarceloClaro/deepseek-harness) | 2 | 24 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 17 | [stophobia/deepseek-harness](https://github.com/stophobia/deepseek-harness) | 2 | 7 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 18 | [suiyuebaobao/deepseek-harness-gui](https://github.com/suiyuebaobao/deepseek-harness-gui) | 2 | 149 | audited | 新增约 2 个提交并修改 52 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“Windows desktop fork of DeepSeek Harness, packaged with Tauri while preserving the full Web profile and plugin runtime”。 |
| 19 | [Yihong89/deepseek-harness](https://github.com/Yihong89/deepseek-harness) | 2 | 58 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 20 | [srwang0506/deepseek-harness](https://github.com/srwang0506/deepseek-harness) | 1 | 76 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 21 | [xiaosenho/deepseek-harness](https://github.com/xiaosenho/deepseek-harness) | 1 | 116 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 22 | [007M7/deepseek-harness](https://github.com/007M7/deepseek-harness) | 1 | 153 | audited | 未观察到相对 upstream 的文件修改；目标线索是“我永远喜欢deepseek！！！”。 |
| 23 | [123prompt/deepseek-harness](https://github.com/123prompt/deepseek-harness) | 1 | 202 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 24 | [1486482143/deepseek-harness](https://github.com/1486482143/deepseek-harness) | 1 | 206 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 25 | [18217778896/deepseek-harness](https://github.com/18217778896/deepseek-harness) | 1 | 133 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 26 | [2404589803/deepseek-harness](https://github.com/2404589803/deepseek-harness) | 1 | 50 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 27 | [485524097/deepseek-harness](https://github.com/485524097/deepseek-harness) | 1 | 218 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 28 | [4evour/deepseek-harness](https://github.com/4evour/deepseek-harness) | 1 | 124 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 29 | [a907781273-a11y/deepseek-harness](https://github.com/a907781273-a11y/deepseek-harness) | 1 | 11083 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 30 | [achristofaro/deepseek-harness](https://github.com/achristofaro/deepseek-harness) | 1 | 53 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 31 | [AI-1-TOP/deepseek-harness](https://github.com/AI-1-TOP/deepseek-harness) | 1 | 11110 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 32 | [aimierbear/TinyWhale](https://github.com/aimierbear/TinyWhale) | 1 | 31 | audited | 新增约 18 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、CI/构建；目标线索是“TinyWhale — desktop-oriented MIT fork of DeepSeek Harness, with an Electron shell in desktop/”。 |
| 33 | [alexdeweb/deepseek-harness](https://github.com/alexdeweb/deepseek-harness) | 1 | 79 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 34 | [alexdolbun/deepseek-harness](https://github.com/alexdolbun/deepseek-harness) | 1 | 4 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 35 | [Alsdara/deepseek-harness](https://github.com/Alsdara/deepseek-harness) | 1 | 11072 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 36 | [Anyaoha/deepseek-harness](https://github.com/Anyaoha/deepseek-harness) | 1 | 47 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 37 | [Ashveil1/deepseek-harness-ares](https://github.com/Ashveil1/deepseek-harness-ares) | 1 | 193 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek harness for pentesting”。 |
| 38 | [athif23/deepseek-harness](https://github.com/athif23/deepseek-harness) | 1 | 29 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 39 | [ayushare/deepseek-harness](https://github.com/ayushare/deepseek-harness) | 1 | 11047 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 40 | [b3nk-x1/deepseek-harness](https://github.com/b3nk-x1/deepseek-harness) | 1 | 11088 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 41 | [badestgod/deepseek-harness](https://github.com/badestgod/deepseek-harness) | 1 | 88 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 42 | [Beam-wi/deepseek-harness](https://github.com/Beam-wi/deepseek-harness) | 1 | 145 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 43 | [ben-vargas/ai-deepseek-harness](https://github.com/ben-vargas/ai-deepseek-harness) | 1 | 19 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 44 | [biyan113/deepseek-harness](https://github.com/biyan113/deepseek-harness) | 1 | 32 | audited | 新增约 3 个提交并修改 55 个文件，主要涉及 CI/构建、UI/应用层、文档、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 45 | [BlackRosePetals/deepseek-harness](https://github.com/BlackRosePetals/deepseek-harness) | 1 | 120 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 46 | [BobcGn/deepseek-harness-app](https://github.com/BobcGn/deepseek-harness-app) | 1 | 126 | audited | 新增约 14 个提交并修改 31 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 47 | [bojieli/deepseek-harness](https://github.com/bojieli/deepseek-harness) | 1 | 3 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 48 | [boktoday/deepseek-harness](https://github.com/boktoday/deepseek-harness) | 1 | 46 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 49 | [BurtonQin/deepseek-harness](https://github.com/BurtonQin/deepseek-harness) | 1 | 22 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 50 | [CatchCatOoO/deepseek-harness](https://github.com/CatchCatOoO/deepseek-harness) | 1 | 164 | audited | 新增约 4 个提交并修改 300 个文件，主要涉及 文档、配置、agent/skill 能力；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 51 | [cFqr-lang/deepseek-harness](https://github.com/cFqr-lang/deepseek-harness) | 1 | 11079 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 52 | [CH-HGod/deepseek-harness](https://github.com/CH-HGod/deepseek-harness) | 1 | 11059 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 53 | [chiekoschamburek-dev/deepseek-harness](https://github.com/chiekoschamburek-dev/deepseek-harness) | 1 | 11076 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 54 | [China-MY/deepseek-harness](https://github.com/China-MY/deepseek-harness) | 1 | 92 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 55 | [chyl00/deepseek-harness](https://github.com/chyl00/deepseek-harness) | 1 | 181 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 56 | [cioerp/deepseek-harness](https://github.com/cioerp/deepseek-harness) | 1 | 11104 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 57 | [codelife2020/deepseek-harness](https://github.com/codelife2020/deepseek-harness) | 1 | 173 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 58 | [coder-v0/deepseek-harness](https://github.com/coder-v0/deepseek-harness) | 1 | 81 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 59 | [cq2021-coder/deepseek-harness-desktop](https://github.com/cq2021-coder/deepseek-harness-desktop) | 1 | 90 | audited | 未观察到相对 upstream 的文件修改；目标线索是“使用 tauri 为 DeepSeek Harness 生态打造的现代化桌面端应用”。 |
| 60 | [criapa/deepseek-harness](https://github.com/criapa/deepseek-harness) | 1 | 41 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 61 | [Cute-chen/deepseek-harness-app](https://github.com/Cute-chen/deepseek-harness-app) | 1 | 167 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 62 | [Cyenoch/deepseek-harness](https://github.com/Cyenoch/deepseek-harness) | 1 | 59 | audited | 新增约 13 个提交并修改 300 个文件，主要涉及 配置、文档、agent/skill 能力、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 63 | [cyh7777/deepseek-harness](https://github.com/cyh7777/deepseek-harness) | 1 | 11061 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 64 | [dailin3/deepseek-harness](https://github.com/dailin3/deepseek-harness) | 1 | 115 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 65 | [DailyR/deepseek-harness](https://github.com/DailyR/deepseek-harness) | 1 | 35 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 66 | [ddd666j/deepseek-harness](https://github.com/ddd666j/deepseek-harness) | 1 | 11095 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 67 | [DeepThinkingZhouLiu/Deepseek-Harness-RSI](https://github.com/DeepThinkingZhouLiu/Deepseek-Harness-RSI) | 1 | 66 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 68 | [deveuper/deepseek-harness](https://github.com/deveuper/deepseek-harness) | 1 | 130 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 69 | [devin2255/deepseek-harness-desktop](https://github.com/devin2255/deepseek-harness-desktop) | 1 | 82 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 70 | [djhh555/deepseek-sightline](https://github.com/djhh555/deepseek-sightline) | 1 | 11068 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 71 | [DogeJian/deepseek-harness](https://github.com/DogeJian/deepseek-harness) | 1 | 69 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 72 | [donstang/deepseek-harness](https://github.com/donstang/deepseek-harness) | 1 | 37 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 73 | [dorucioclea/deepseek-harness](https://github.com/dorucioclea/deepseek-harness) | 1 | 10 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 74 | [drscrewdriver/deepseek-harness](https://github.com/drscrewdriver/deepseek-harness) | 1 | 65 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 75 | [duliangkuan/deepseek-harness](https://github.com/duliangkuan/deepseek-harness) | 1 | 143 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 76 | [EdwardXIE6666/deepseek-harness](https://github.com/EdwardXIE6666/deepseek-harness) | 1 | 190 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 77 | [enbideren/deepseek-harness](https://github.com/enbideren/deepseek-harness) | 1 | 70 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 78 | [equable66/deepseek-harness](https://github.com/equable66/deepseek-harness) | 1 | 966 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 79 | [Erichy777/deepseek-harness](https://github.com/Erichy777/deepseek-harness) | 1 | 179 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 80 | [Ericsongyl/deepseek-harness](https://github.com/Ericsongyl/deepseek-harness) | 1 | 26 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 81 | [ermao009/deepseek-harness](https://github.com/ermao009/deepseek-harness) | 1 | 213 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 82 | [exposir/deepseek-harness](https://github.com/exposir/deepseek-harness) | 1 | 8 | audited | 新增约 9 个提交并修改 13 个文件，主要涉及 文档、Harness 核心能力、测试；目标线索是“DeepSeek Harness”。 |
| 83 | [fage45029704-lgtm/deepseek-harness](https://github.com/fage45029704-lgtm/deepseek-harness) | 1 | 11081 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 84 | [faguangdeyueliang/deepseek-harness](https://github.com/faguangdeyueliang/deepseek-harness) | 1 | 194 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 85 | [fendouai/deepseek-harness-desktop](https://github.com/fendouai/deepseek-harness-desktop) | 1 | 9 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 86 | [fisher158163/deepseek-harness](https://github.com/fisher158163/deepseek-harness) | 1 | 25 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 87 | [flaqai/open-deepseek-harness-desktop](https://github.com/flaqai/open-deepseek-harness-desktop) | 1 | 154 | audited | 未观察到相对 upstream 的文件修改；目标线索是“Open Source Desktop for DeepSeek Harness. DeepSeek Harness: Everything is a Plugin”。 |
| 88 | [flowersea302/deepseek-harness](https://github.com/flowersea302/deepseek-harness) | 1 | 216 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 89 | [FlyingSama/deepseek-harness](https://github.com/FlyingSama/deepseek-harness) | 1 | 171 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 90 | [GavinDong-plaud/deepseek-harness](https://github.com/GavinDong-plaud/deepseek-harness) | 1 | 11058 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 91 | [GetSayAll/deepseek-harness-app](https://github.com/GetSayAll/deepseek-harness-app) | 1 | 11066 | audited | 新增约 25 个提交并修改 118 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek Harness”。 |
| 92 | [ghthh/deepseek-harness](https://github.com/ghthh/deepseek-harness) | 1 | 11046 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 93 | [GTC2080/deepseek-harness](https://github.com/GTC2080/deepseek-harness) | 1 | 150 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness 桌面端：基于 Tauri，支持 macOS 与 Windows；源码位于 desktop 分支”。 |
| 94 | [guihuatu2022/deepseek-harness](https://github.com/guihuatu2022/deepseek-harness) | 1 | 174 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 95 | [GZZ-523/deepseek-harness](https://github.com/GZZ-523/deepseek-harness) | 1 | 166 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 96 | [hanfengchiyi/deepseek-harness](https://github.com/hanfengchiyi/deepseek-harness) | 1 | 196 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 97 | [hanqi9622-eng/deepseek-harness](https://github.com/hanqi9622-eng/deepseek-harness) | 1 | 11093 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 98 | [HaoyanZhang123/deepseek-harness-live-preset-switch](https://github.com/HaoyanZhang123/deepseek-harness-live-preset-switch) | 1 | 11075 | audited | 新增约 2 个提交并修改 81 个文件，主要涉及 文档、agent/skill 能力、UI/应用层、Harness 核心能力；目标线索是“DeepSeek Harness with live agent-preset switching at turn boundaries”。 |
| 99 | [heleileimail-cmyk/deepseek-harness](https://github.com/heleileimail-cmyk/deepseek-harness) | 1 | 11073 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 100 | [HelloNicoo/deepseek-harness](https://github.com/HelloNicoo/deepseek-harness) | 1 | 106 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |

## Modification categories

| Category | Changed paths |
| --- | ---: |
| docs | 1,231 |
| dependencies | 929 |
| harness-core | 734 |
| configuration | 584 |
| ui-and-apps | 488 |
| tests | 311 |
| other | 108 |
| ci-and-build | 47 |
| tools-and-scripts | 31 |
| agents-and-skills | 20 |

## Influence order

| Rank | Fork | Stars | Owner reputation | Repo influence | Overall | Ahead | Changed files | Deep status | One-sentence evidence |
| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | --- | --- |
| 1 | [salathleizhang/deepseek-harness-desktop](https://github.com/salathleizhang/deepseek-harness-desktop) | 97 | 36.0 (observed) | 74.989 | 59.393 | 42 | 300 | ok | 新增约 42 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“Native desktop app for DeepSeek Harness — an Electron shell that runs the harness locally and hosts the official Web GUI unchanged”。 |
| 2 | [himomohi/deepseek-harness](https://github.com/himomohi/deepseek-harness) | 1 | 46.5 (observed) | 51.023 | 49.221 | 36 | 300 | metadata-only | 新增约 36 个提交并修改 300 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 3 | [bojieli/deepseek-harness](https://github.com/bojieli/deepseek-harness) | 1 | 81.4 (observed) | 25.918 | 48.109 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 4 | [alexdolbun/deepseek-harness](https://github.com/alexdolbun/deepseek-harness) | 1 | 80.0 (observed) | 25.918 | 47.566 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 5 | [G36maid/deepseek-harness](https://github.com/G36maid/deepseek-harness) | 12 | 54.4 (observed) | 42.350 | 47.186 | 19 | 300 | ok | 新增约 19 个提交并修改 300 个文件，主要涉及 配置、文档；目标线索是“DeepSeek Harness 繁體中文版 (zh-TW) — Everything is a Plugin”。 |
| 6 | [Sakana-yuyu/deepseek-harness-desktop](https://github.com/Sakana-yuyu/deepseek-harness-desktop) | 21 | 35.5 (observed) | 54.402 | 46.845 | 14 | 81 | ok | 新增约 14 个提交并修改 81 个文件，主要涉及 配置、文档、CI/构建、UI/应用层；目标线索是“Rust构建的客户端，体积更小，更方便，Mac，win，linux已完成”。 |
| 7 | [stophobia/deepseek-harness](https://github.com/stophobia/deepseek-harness) | 2 | 70.7 (observed) | 29.455 | 45.937 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 8 | [exposir/deepseek-harness](https://github.com/exposir/deepseek-harness) | 1 | 52.3 (observed) | 39.275 | 44.476 | 9 | 13 | ok | 新增约 9 个提交并修改 13 个文件，主要涉及 文档、Harness 核心能力、测试；目标线索是“DeepSeek Harness”。 |
| 9 | [fendouai/deepseek-harness-desktop](https://github.com/fendouai/deepseek-harness-desktop) | 1 | 72.1 (observed) | 26.021 | 44.446 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 10 | [dorucioclea/deepseek-harness](https://github.com/dorucioclea/deepseek-harness) | 1 | 71.8 (observed) | 25.918 | 44.253 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 11 | [Skyearn/deepseek-harness-app](https://github.com/Skyearn/deepseek-harness-app) | 11 | 34.3 (observed) | 49.137 | 43.211 | 24 | 31 | ok | 新增约 24 个提交并修改 31 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness Desktop”。 |
| 12 | [realchenwenqiao/dash-fork](https://github.com/realchenwenqiao/dash-fork) | 1 | 37.1 (observed) | 45.508 | 42.150 | 35 | 38 | ok | 新增约 35 个提交并修改 38 个文件，主要涉及 文档、依赖、UI/应用层、其他文件；目标线索是“DASH — terminal-native TUI for DeepSeek Harness: Claude Code-style full-screen interface, multi-model switching, behavior-ledger rewind”。 |
| 13 | [rpmalouin/deepseek-harness](https://github.com/rpmalouin/deepseek-harness) | 8 | 34.9 (observed) | 46.620 | 41.932 | 4 | 31 | ok | 新增约 4 个提交并修改 31 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 14 | [zhonghui5207/deepseek-harness-desktop](https://github.com/zhonghui5207/deepseek-harness-desktop) | 1 | 29.0 (observed) | 49.326 | 41.208 | 19 | 300 | ok | 新增约 19 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“DSH Desktop — an installable desktop distribution of DeepSeek Harness for macOS, Windows, and Linux”。 |
| 15 | [lixun910/deepseek-harness](https://github.com/lixun910/deepseek-harness) | 1 | 64.0 (observed) | 25.918 | 41.141 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 16 | [puppywang/deepseek-harness](https://github.com/puppywang/deepseek-harness) | 4 | 49.7 (observed) | 33.985 | 40.286 | 10 | 300 | ok | 新增约 10 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 17 | [Sailfishc/deepseek-harness](https://github.com/Sailfishc/deepseek-harness) | 1 | 61.2 (observed) | 25.918 | 40.036 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 18 | [Ajwyunsx/deepseek-harness-mobile](https://github.com/Ajwyunsx/deepseek-harness-mobile) | 4 | 36.6 (observed) | 41.535 | 39.552 | 7 | 40 | ok | 新增约 7 个提交并修改 40 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 19 | [ben-vargas/ai-deepseek-harness](https://github.com/ben-vargas/ai-deepseek-harness) | 1 | 59.6 (observed) | 25.918 | 39.402 | 0 | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 20 | [TKaxv-7S/deepseek-harness](https://github.com/TKaxv-7S/deepseek-harness) | 1 | 59.4 (observed) | 25.918 | 39.297 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 21 | [rferrari/deepseek-harness](https://github.com/rferrari/deepseek-harness) | 1 | 58.8 (observed) | 25.918 | 39.066 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 22 | [BurtonQin/deepseek-harness](https://github.com/BurtonQin/deepseek-harness) | 1 | 58.2 (observed) | 25.918 | 38.837 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 23 | [happylin0x29a/deepseek-harness-desktop](https://github.com/happylin0x29a/deepseek-harness-desktop) | 4 | 34.6 (observed) | 41.452 | 38.727 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness desktop base on tauri”。 |
| 24 | [MarceloClaro/deepseek-harness](https://github.com/MarceloClaro/deepseek-harness) | 2 | 50.6 (observed) | 29.455 | 37.904 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 25 | [fisher158163/deepseek-harness](https://github.com/fisher158163/deepseek-harness) | 1 | 54.9 (observed) | 25.918 | 37.530 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 26 | [Ericsongyl/deepseek-harness](https://github.com/Ericsongyl/deepseek-harness) | 1 | 54.5 (observed) | 25.918 | 37.344 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 27 | [manuelapetsi/deepseek-harness](https://github.com/manuelapetsi/deepseek-harness) | 1 | 54.3 (observed) | 25.918 | 37.259 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 28 | [0verL1nk/deepseek-harness](https://github.com/0verL1nk/deepseek-harness) | 0 | 31.6 (observed) | 40.155 | 36.745 | 29 | 59 | ok | 新增约 29 个提交并修改 59 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 29 | [athif23/deepseek-harness](https://github.com/athif23/deepseek-harness) | 1 | 51.7 (observed) | 25.918 | 36.220 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 30 | [FSMargoo/deepseek-harness](https://github.com/FSMargoo/deepseek-harness) | 2 | 46.1 (observed) | 29.455 | 36.120 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 31 | [aimierbear/TinyWhale](https://github.com/aimierbear/TinyWhale) | 1 | 16.4 (observed) | 49.166 | 36.054 | 18 | 300 | ok | 新增约 18 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、CI/构建；目标线索是“TinyWhale — desktop-oriented MIT fork of DeepSeek Harness, with an Electron shell in desktop/”。 |
| 32 | [biyan113/deepseek-harness](https://github.com/biyan113/deepseek-harness) | 1 | 28.1 (observed) | 40.378 | 35.483 | 3 | 55 | metadata-only | 新增约 3 个提交并修改 55 个文件，主要涉及 CI/构建、UI/应用层、文档、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 33 | [t479842598/deepseek-harness](https://github.com/t479842598/deepseek-harness) | 1 | 26.7 (observed) | 40.809 | 35.183 | 16 | 13 | ok | 新增约 16 个提交并修改 13 个文件，主要涉及 Harness 核心能力、测试；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 34 | [zchuhui/deepseek-harness](https://github.com/zchuhui/deepseek-harness) | 1 | 48.7 (observed) | 26.016 | 35.104 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 35 | [DailyR/deepseek-harness](https://github.com/DailyR/deepseek-harness) | 1 | 48.7 (observed) | 25.918 | 35.049 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 36 | [luolangaga/deepseek-harness](https://github.com/luolangaga/deepseek-harness) | 4 | 36.4 (observed) | 33.957 | 34.922 | 11 | 54 | ok | 新增约 11 个提交并修改 54 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 37 | [donstang/deepseek-harness](https://github.com/donstang/deepseek-harness) | 1 | 48.0 (observed) | 25.918 | 34.757 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 38 | [LCYLYM/deepseek-harness](https://github.com/LCYLYM/deepseek-harness) | 1 | 47.7 (observed) | 25.918 | 34.614 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 39 | [Razor87/deepseek-harness](https://github.com/Razor87/deepseek-harness) | 1 | 47.6 (observed) | 25.918 | 34.610 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 40 | [lkngin/deepseek-harness](https://github.com/lkngin/deepseek-harness) | 1 | 47.5 (observed) | 25.918 | 34.532 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 41 | [criapa/deepseek-harness](https://github.com/criapa/deepseek-harness) | 1 | 47.3 (observed) | 25.918 | 34.480 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 42 | [zhanglunet/deepseek-harness](https://github.com/zhanglunet/deepseek-harness) | 0 | 55.7 (observed) | 20.000 | 34.282 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 43 | [yomaser/deepseek-harness](https://github.com/yomaser/deepseek-harness) | 1 | 46.2 (observed) | 25.918 | 34.051 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 44 | [nydia/deepseek-harness](https://github.com/nydia/deepseek-harness) | 1 | 46.2 (observed) | 25.918 | 34.017 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 45 | [odonzyk/deepseek-harness](https://github.com/odonzyk/deepseek-harness) | 1 | 44.4 (observed) | 25.918 | 33.330 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 46 | [boktoday/deepseek-harness](https://github.com/boktoday/deepseek-harness) | 1 | 44.2 (observed) | 25.918 | 33.212 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 47 | [Anyaoha/deepseek-harness](https://github.com/Anyaoha/deepseek-harness) | 1 | 44.0 (observed) | 25.918 | 33.134 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 48 | [vkn129/deepseek-harness](https://github.com/vkn129/deepseek-harness) | 1 | 43.9 (observed) | 25.918 | 33.110 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 49 | [porarrirr/deepseek-harness-japanese](https://github.com/porarrirr/deepseek-harness-japanese) | 0 | 19.3 (observed) | 42.233 | 33.070 | 2 | 88 | ok | 新增约 2 个提交并修改 88 个文件，主要涉及 配置、文档、UI/应用层、依赖；目标线索是“DeepSeek Harness”。 |
| 50 | [2404589803/deepseek-harness](https://github.com/2404589803/deepseek-harness) | 1 | 43.8 (observed) | 25.918 | 33.069 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 51 | [shenyimings/deepseek-harness](https://github.com/shenyimings/deepseek-harness) | 1 | 43.7 (observed) | 25.918 | 33.033 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 52 | [roadlittledawn/deepseek-harness](https://github.com/roadlittledawn/deepseek-harness) | 1 | 42.9 (observed) | 25.918 | 32.704 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 53 | [achristofaro/deepseek-harness](https://github.com/achristofaro/deepseek-harness) | 1 | 42.6 (observed) | 25.918 | 32.591 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 54 | [nostalgia296/deepseek-harness-termux](https://github.com/nostalgia296/deepseek-harness-termux) | 1 | 23.6 (observed) | 38.290 | 32.411 | 2 | 33 | ok | 新增约 2 个提交并修改 33 个文件，主要涉及 配置、文档、测试、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 55 | [mnky4a6/deepseek-harness](https://github.com/mnky4a6/deepseek-harness) | 1 | 42.1 (observed) | 25.918 | 32.409 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 56 | [phong711/deepseek-harness](https://github.com/phong711/deepseek-harness) | 1 | 42.1 (observed) | 25.918 | 32.402 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 57 | [BJTU-Netcomm/deepseek-harness-aiops](https://github.com/BJTU-Netcomm/deepseek-harness-aiops) | 0 | 39.4 (observed) | 27.371 | 32.199 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness for aiops: Everything is a Plugin”。 |
| 58 | [Yihong89/deepseek-harness](https://github.com/Yihong89/deepseek-harness) | 2 | 36.3 (observed) | 29.455 | 32.187 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 59 | [Cyenoch/deepseek-harness](https://github.com/Cyenoch/deepseek-harness) | 1 | 41.4 (observed) | 26.017 | 32.170 | 13 | 300 | ok | 新增约 13 个提交并修改 300 个文件，主要涉及 配置、文档、agent/skill 能力、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 60 | [tzy168/deepseek-harness](https://github.com/tzy168/deepseek-harness) | 1 | 23.8 (observed) | 37.565 | 32.040 | 2 | 25 | ok | 新增约 2 个提交并修改 25 个文件，主要涉及 配置、文档、Harness 核心能力、测试；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 61 | [missuzhang/deepseek-harness](https://github.com/missuzhang/deepseek-harness) | 1 | 41.2 (observed) | 25.918 | 32.014 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 62 | [Mike-7777777/deepseek-harness](https://github.com/Mike-7777777/deepseek-harness) | 1 | 40.6 (observed) | 25.918 | 31.802 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 63 | [mallocxw/deepseek-harness](https://github.com/mallocxw/deepseek-harness) | 1 | 40.0 (observed) | 25.918 | 31.543 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 64 | [xiaolangde/deepseek-harness](https://github.com/xiaolangde/deepseek-harness) | 1 | 39.7 (observed) | 25.968 | 31.447 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 65 | [drscrewdriver/deepseek-harness](https://github.com/drscrewdriver/deepseek-harness) | 1 | 38.7 (observed) | 25.918 | 31.021 | 0 | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 66 | [DeepThinkingZhouLiu/Deepseek-Harness-RSI](https://github.com/DeepThinkingZhouLiu/Deepseek-Harness-RSI) | 1 | 38.3 (observed) | 26.038 | 30.923 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 67 | [Vitaminaq/deepseek-harness](https://github.com/Vitaminaq/deepseek-harness) | 1 | 38.0 (observed) | 25.952 | 30.752 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 68 | [Tyler-R-Kendrick/deepseek-harness](https://github.com/Tyler-R-Kendrick/deepseek-harness) | 1 | 38.0 (observed) | 25.918 | 30.735 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 69 | [DogeJian/deepseek-harness](https://github.com/DogeJian/deepseek-harness) | 1 | 37.9 (observed) | 25.918 | 30.694 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 70 | [enbideren/deepseek-harness](https://github.com/enbideren/deepseek-harness) | 1 | 37.8 (observed) | 25.918 | 30.687 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 71 | [Yuan-lai-ru-ci/deepseek-harness-desktop](https://github.com/Yuan-lai-ru-ci/deepseek-harness-desktop) | 1 | 16.2 (observed) | 40.133 | 30.570 | 8 | 21 | ok | 新增约 8 个提交并修改 21 个文件，主要涉及 文档、UI/应用层、依赖；目标线索是“随手做的DSH桌面版，需要下载原包，在桌面上方便打开，可以装插件”。 |
| 72 | [xiansheng888/deepseek-harness](https://github.com/xiansheng888/deepseek-harness) | 1 | 37.4 (observed) | 25.918 | 30.525 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 73 | [mgrillo75/deepseek-harness](https://github.com/mgrillo75/deepseek-harness) | 1 | 37.3 (observed) | 25.918 | 30.473 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 74 | [v2hoping/deepseek-harness-desktop](https://github.com/v2hoping/deepseek-harness-desktop) | 1 | 36.4 (observed) | 26.038 | 30.176 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin. Supports desktop installation and DeepSeek account login”。 |
| 75 | [Linmoqian/deepseek-harness-cli](https://github.com/Linmoqian/deepseek-harness-cli) | 1 | 36.2 (observed) | 25.918 | 30.032 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness-cli版本”。 |
| 76 | [srwang0506/deepseek-harness](https://github.com/srwang0506/deepseek-harness) | 1 | 24.3 (observed) | 33.541 | 29.828 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 77 | [SamboHassan/deepseek-harness](https://github.com/SamboHassan/deepseek-harness) | 1 | 35.5 (observed) | 25.918 | 29.735 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 78 | [ouyangyipeng/dsh-desktop-upstream-archive](https://github.com/ouyangyipeng/dsh-desktop-upstream-archive) | 1 | 35.3 (observed) | 25.956 | 29.712 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“Archived upstream fork that preceded the independent DS-Harness Desktop repository”。 |
| 79 | [alexdeweb/deepseek-harness](https://github.com/alexdeweb/deepseek-harness) | 1 | 35.0 (observed) | 25.918 | 29.537 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 80 | [rvndnishad-work/deepseek-harness](https://github.com/rvndnishad-work/deepseek-harness) | 1 | 34.9 (observed) | 25.918 | 29.526 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 81 | [coder-v0/deepseek-harness](https://github.com/coder-v0/deepseek-harness) | 1 | 34.9 (observed) | 25.918 | 29.523 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 82 | [devin2255/deepseek-harness-desktop](https://github.com/devin2255/deepseek-harness-desktop) | 1 | 34.6 (observed) | 25.918 | 29.409 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 83 | [JayTing511/deepseek-harness](https://github.com/JayTing511/deepseek-harness) | 1 | 34.3 (observed) | 25.918 | 29.278 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 84 | [luoxunhao/deepseek-harness](https://github.com/luoxunhao/deepseek-harness) | 1 | 34.0 (observed) | 25.918 | 29.142 | 0 | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 85 | [playboy662/deepseek-harness](https://github.com/playboy662/deepseek-harness) | 1 | 33.7 (observed) | 25.918 | 29.029 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 86 | [zenghuan/deepseek-harness](https://github.com/zenghuan/deepseek-harness) | 1 | 33.4 (observed) | 25.918 | 28.927 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 87 | [yazzang-homelab/deepseek-harness](https://github.com/yazzang-homelab/deepseek-harness) | 2 | 16.5 (observed) | 36.955 | 28.782 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 88 | [badestgod/deepseek-harness](https://github.com/badestgod/deepseek-harness) | 1 | 33.0 (observed) | 25.918 | 28.767 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 89 | [houkang/deepseek-harness](https://github.com/houkang/deepseek-harness) | 1 | 32.8 (observed) | 25.918 | 28.688 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness”。 |
| 90 | [cq2021-coder/deepseek-harness-desktop](https://github.com/cq2021-coder/deepseek-harness-desktop) | 1 | 32.7 (observed) | 25.983 | 28.675 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“使用 tauri 为 DeepSeek Harness 生态打造的现代化桌面端应用”。 |
| 91 | [HybridMAS/deepseek-harness](https://github.com/HybridMAS/deepseek-harness) | 1 | 32.7 (observed) | 25.918 | 28.625 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 92 | [China-MY/deepseek-harness](https://github.com/China-MY/deepseek-harness) | 1 | 32.6 (observed) | 25.918 | 28.578 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 93 | [tomchon/deepseek-harness](https://github.com/tomchon/deepseek-harness) | 1 | 32.0 (observed) | 25.918 | 28.351 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 94 | [youshen2/deepseek-harness](https://github.com/youshen2/deepseek-harness) | 1 | 31.8 (observed) | 25.986 | 28.322 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 95 | [valentinshenfeld/deepseek-harness](https://github.com/valentinshenfeld/deepseek-harness) | 1 | 31.9 (observed) | 25.918 | 28.314 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 96 | [MasterToycode/deepseek-harness](https://github.com/MasterToycode/deepseek-harness) | 1 | 31.9 (observed) | 25.918 | 28.292 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 97 | [shdeng/deepseek-harness-app](https://github.com/shdeng/deepseek-harness-app) | 1 | 31.3 (observed) | 26.030 | 28.118 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 98 | [HossamTabana/deepseek-harness](https://github.com/HossamTabana/deepseek-harness) | 1 | 31.3 (observed) | 25.918 | 28.083 | — | 0 | partial | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 99 | [slamsmart/deepseek-harness](https://github.com/slamsmart/deepseek-harness) | 1 | 30.6 (observed) | 25.918 | 27.794 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 100 | [huiliyi37/deepseek-harness](https://github.com/huiliyi37/deepseek-harness) | 2 | 25.1 (observed) | 29.455 | 27.723 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 101 | [maigadohcrypto/deepseek-harness](https://github.com/maigadohcrypto/deepseek-harness) | 1 | 30.2 (observed) | 25.918 | 27.645 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 102 | [sdkwork-ai/deepseek-harness-desktop](https://github.com/sdkwork-ai/deepseek-harness-desktop) | 4 | 17.9 (observed) | 34.030 | 27.581 | 43 | 300 | ok | 新增约 43 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 103 | [wellfuture/deepseek-harness](https://github.com/wellfuture/deepseek-harness) | 1 | 30.1 (observed) | 25.918 | 27.580 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 104 | [Kiowx/deepseek-harness](https://github.com/Kiowx/deepseek-harness) | 2 | 24.6 (observed) | 29.498 | 27.527 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 105 | [HugoluizMTB/deepseek-harness](https://github.com/HugoluizMTB/deepseek-harness) | 1 | 29.9 (observed) | 25.918 | 27.494 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 106 | [HelloNicoo/deepseek-harness](https://github.com/HelloNicoo/deepseek-harness) | 1 | 29.7 (observed) | 25.918 | 27.429 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 107 | [misshehe/deepseek-harness](https://github.com/misshehe/deepseek-harness) | 1 | 29.7 (observed) | 25.918 | 27.420 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 108 | [tranvantrung95/deepseek-harness](https://github.com/tranvantrung95/deepseek-harness) | 1 | 29.3 (observed) | 25.918 | 27.262 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 109 | [NewMFF/deepseek-harness](https://github.com/NewMFF/deepseek-harness) | 1 | 29.1 (observed) | 25.918 | 27.193 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 110 | [zdy-ai/deepseek-harness](https://github.com/zdy-ai/deepseek-harness) | 1 | 29.0 (observed) | 25.918 | 27.169 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 111 | [oscarlius/deepseek-harness](https://github.com/oscarlius/deepseek-harness) | 1 | 28.9 (observed) | 25.918 | 27.116 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 112 | [TomYang1024/deepseek-harness](https://github.com/TomYang1024/deepseek-harness) | 1 | 28.8 (observed) | 25.918 | 27.058 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 113 | [KinomotoMio/deepseek-harness](https://github.com/KinomotoMio/deepseek-harness) | 1 | 28.7 (observed) | 25.918 | 27.033 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 114 | [linfunss/deepseek-harness](https://github.com/linfunss/deepseek-harness) | 1 | 28.4 (observed) | 25.918 | 26.921 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 115 | [dailin3/deepseek-harness](https://github.com/dailin3/deepseek-harness) | 1 | 28.2 (observed) | 25.918 | 26.834 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 116 | [xiaosenho/deepseek-harness](https://github.com/xiaosenho/deepseek-harness) | 1 | 16.3 (observed) | 33.473 | 26.610 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 117 | [zng8418/deepseek-harness](https://github.com/zng8418/deepseek-harness) | 1 | 27.6 (observed) | 25.918 | 26.605 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 118 | [markisaac/deepseek-harness](https://github.com/markisaac/deepseek-harness) | 1 | 27.5 (observed) | 25.918 | 26.565 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 119 | [iKing/deepseek-harness](https://github.com/iKing/deepseek-harness) | 1 | 27.5 (observed) | 25.918 | 26.533 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 120 | [BlackRosePetals/deepseek-harness](https://github.com/BlackRosePetals/deepseek-harness) | 1 | 27.3 (observed) | 25.918 | 26.465 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 121 | [imhieu/deepseek-harness](https://github.com/imhieu/deepseek-harness) | 1 | 26.7 (observed) | 25.918 | 26.247 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 122 | [Helpless5699/deepseek-harness](https://github.com/Helpless5699/deepseek-harness) | 1 | 26.7 (observed) | 25.918 | 26.225 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 123 | [melkharbili/deepseek-harness](https://github.com/melkharbili/deepseek-harness) | 1 | 26.5 (observed) | 25.918 | 26.163 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 124 | [4evour/deepseek-harness](https://github.com/4evour/deepseek-harness) | 1 | 26.5 (observed) | 25.918 | 26.137 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 125 | [KevinSCUTer/deepseek-harness](https://github.com/KevinSCUTer/deepseek-harness) | 1 | 25.8 (observed) | 25.918 | 25.887 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 126 | [BobcGn/deepseek-harness-app](https://github.com/BobcGn/deepseek-harness-app) | 1 | 25.7 (observed) | 26.019 | 25.883 | 14 | 31 | ok | 新增约 14 个提交并修改 31 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 127 | [QingGeLaiYe/deepseek-harness](https://github.com/QingGeLaiYe/deepseek-harness) | 1 | 25.6 (observed) | 25.918 | 25.775 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 128 | [yx54hego-cloud/deepseek-harness](https://github.com/yx54hego-cloud/deepseek-harness) | 7 | 7.0 (observed) | 38.108 | 25.670 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 129 | [WyrdWerk/deepseek-harness](https://github.com/WyrdWerk/deepseek-harness) | 1 | 25.1 (observed) | 26.040 | 25.650 | 13 | 272 | ok | 新增约 13 个提交并修改 272 个文件，主要涉及 配置、文档、CI/构建、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 130 | [deveuper/deepseek-harness](https://github.com/deveuper/deepseek-harness) | 1 | 25.0 (observed) | 25.930 | 25.570 | 0 | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 131 | [yueyucaotian/deepseek-harness](https://github.com/yueyucaotian/deepseek-harness) | 1 | 24.8 (observed) | 25.918 | 25.455 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 132 | [MinerBin/deepseek-harness](https://github.com/MinerBin/deepseek-harness) | 1 | 24.5 (observed) | 25.918 | 25.354 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 133 | [18217778896/deepseek-harness](https://github.com/18217778896/deepseek-harness) | 1 | 24.2 (observed) | 25.918 | 25.242 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 134 | [leixiaochenShen/deepseek-harness](https://github.com/leixiaochenShen/deepseek-harness) | 1 | 24.0 (observed) | 25.918 | 25.156 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 135 | [liwuli/deepseek-harness-desktop](https://github.com/liwuli/deepseek-harness-desktop) | 1 | 23.9 (observed) | 25.972 | 25.130 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness desktop”。 |
| 136 | [zkh11123/deepseek-harness](https://github.com/zkh11123/deepseek-harness) | 1 | 23.3 (observed) | 25.918 | 24.872 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 137 | [lihaidog/deepseek-harness](https://github.com/lihaidog/deepseek-harness) | 1 | 23.1 (observed) | 25.918 | 24.772 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 138 | [w74srm/deepseek-harness](https://github.com/w74srm/deepseek-harness) | 1 | 22.9 (observed) | 25.918 | 24.724 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 139 | [xiaofeng930415/deepseek-harness](https://github.com/xiaofeng930415/deepseek-harness) | 1 | 22.7 (observed) | 25.918 | 24.639 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 140 | [wuyuanjiang1/dsh2wechat_plugin](https://github.com/wuyuanjiang1/dsh2wechat_plugin) | 1 | 9.1 (observed) | 34.968 | 24.624 | 1 | 14 | metadata-only | 新增约 1 个提交并修改 14 个文件，主要涉及 文档、Harness 核心能力、配置、依赖；目标线索是“deepseek-harness”。 |
| 141 | [HHHHH-GIT/Deepseek-HPD-Harness](https://github.com/HHHHH-GIT/Deepseek-HPD-Harness) | 1 | 22.4 (observed) | 26.002 | 24.567 | 2 | 133 | ok | 新增约 2 个提交并修改 133 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek HPD Harness: Everything is a Plugin. A more powerful Harness with HPD architecture”。 |
| 142 | [longman888/deepseek-harness](https://github.com/longman888/deepseek-harness) | 1 | 22.5 (observed) | 25.918 | 24.548 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 143 | [duliangkuan/deepseek-harness](https://github.com/duliangkuan/deepseek-harness) | 1 | 22.2 (observed) | 25.918 | 24.428 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 144 | [MixGeeker/deepseek-harness](https://github.com/MixGeeker/deepseek-harness) | 1 | 22.1 (observed) | 25.918 | 24.405 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 145 | [Beam-wi/deepseek-harness](https://github.com/Beam-wi/deepseek-harness) | 1 | 22.0 (observed) | 25.918 | 24.364 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 146 | [Octo-o-o-o/deepseek-harness-desktop](https://github.com/Octo-o-o-o/deepseek-harness-desktop) | 1 | 21.8 (observed) | 26.040 | 24.329 | 78 | 286 | ok | 新增约 78 个提交并修改 286 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“非官方桌面版 · Unofficial desktop shell for DeepSeek Harness — double-click, no Node, no terminal. Signed & notarized on macOS. Tauri shell, official MIT core untouched”。 |
| 147 | [Linyiwei895178/deepseek-harness](https://github.com/Linyiwei895178/deepseek-harness) | 1 | 21.7 (observed) | 25.918 | 24.226 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 148 | [HTree-ZX/deepseek-harness](https://github.com/HTree-ZX/deepseek-harness) | 1 | 21.5 (observed) | 25.918 | 24.137 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 149 | [suiyuebaobao/deepseek-harness-gui](https://github.com/suiyuebaobao/deepseek-harness-gui) | 2 | 16.1 (observed) | 29.492 | 24.118 | 2 | 52 | ok | 新增约 2 个提交并修改 52 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“Windows desktop fork of DeepSeek Harness, packaged with Tauri while preserving the full Web profile and plugin runtime”。 |
| 150 | [GTC2080/deepseek-harness](https://github.com/GTC2080/deepseek-harness) | 1 | 21.2 (observed) | 26.005 | 24.071 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness 桌面端：基于 Tauri，支持 macOS 与 Windows；源码位于 desktop 分支”。 |
| 151 | [wingthedream/deepseek-harness](https://github.com/wingthedream/deepseek-harness) | 1 | 21.2 (observed) | 25.918 | 24.017 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 152 | [shr123456/deepseek-harness](https://github.com/shr123456/deepseek-harness) | 1 | 20.9 (observed) | 25.918 | 23.905 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 153 | [007M7/deepseek-harness](https://github.com/007M7/deepseek-harness) | 1 | 20.4 (observed) | 25.918 | 23.718 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“我永远喜欢deepseek！！！”。 |
| 154 | [flaqai/open-deepseek-harness-desktop](https://github.com/flaqai/open-deepseek-harness-desktop) | 1 | 20.4 (observed) | 25.918 | 23.713 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“Open Source Desktop for DeepSeek Harness. DeepSeek Harness: Everything is a Plugin”。 |
| 155 | [Captain-Dodger/deepseek-harness](https://github.com/Captain-Dodger/deepseek-harness) | 0 | 17.9 (observed) | 27.371 | 23.574 | — | 0 | partial | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 156 | [xbzhangyq/deepseek-harness](https://github.com/xbzhangyq/deepseek-harness) | 1 | 19.7 (observed) | 25.918 | 23.431 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 157 | [x1095907352/deepseek-harness](https://github.com/x1095907352/deepseek-harness) | 1 | 19.5 (observed) | 25.918 | 23.364 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 158 | [Zguigo00/deepseek-harness](https://github.com/Zguigo00/deepseek-harness) | 1 | 19.2 (observed) | 25.918 | 23.231 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 159 | [MrGXxx/deepseek-harness](https://github.com/MrGXxx/deepseek-harness) | 1 | 19.2 (observed) | 25.918 | 23.228 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 160 | [zhanggoodbao/deepseek-harness](https://github.com/zhanggoodbao/deepseek-harness) | 1 | 18.7 (observed) | 25.918 | 23.043 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 161 | [tinhocdaimo2015/deepseek-harness](https://github.com/tinhocdaimo2015/deepseek-harness) | 1 | 18.6 (observed) | 25.918 | 22.983 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 162 | [peter13990/deepseek-harness](https://github.com/peter13990/deepseek-harness) | 1 | 18.6 (observed) | 25.918 | 22.975 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 163 | [WuJunNan-fjy/deepseek-harness](https://github.com/WuJunNan-fjy/deepseek-harness) | 1 | 18.5 (observed) | 25.918 | 22.959 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 164 | [CatchCatOoO/deepseek-harness](https://github.com/CatchCatOoO/deepseek-harness) | 1 | 18.4 (observed) | 25.928 | 22.933 | 4 | 300 | ok | 新增约 4 个提交并修改 300 个文件，主要涉及 文档、配置、agent/skill 能力；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 165 | [Lostsoul-namespace/deepseek-harness](https://github.com/Lostsoul-namespace/deepseek-harness) | 1 | 18.4 (observed) | 25.918 | 22.912 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 166 | [GZZ-523/deepseek-harness](https://github.com/GZZ-523/deepseek-harness) | 1 | 18.3 (observed) | 25.918 | 22.854 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 167 | [Cute-chen/deepseek-harness-app](https://github.com/Cute-chen/deepseek-harness-app) | 1 | 18.2 (observed) | 25.918 | 22.817 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 168 | [jinchao-bst/deepseek-harness](https://github.com/jinchao-bst/deepseek-harness) | 1 | 18.2 (observed) | 25.918 | 22.814 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 169 | [ousers/deepseek-harness](https://github.com/ousers/deepseek-harness) | 1 | 18.0 (observed) | 25.918 | 22.758 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 170 | [ling0zero0/deepseek-harness](https://github.com/ling0zero0/deepseek-harness) | 1 | 18.0 (observed) | 25.918 | 22.739 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 171 | [FlyingSama/deepseek-harness](https://github.com/FlyingSama/deepseek-harness) | 1 | 17.9 (observed) | 25.918 | 22.729 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 172 | [lucy971326/deepseek-harness](https://github.com/lucy971326/deepseek-harness) | 1 | 17.8 (observed) | 25.918 | 22.690 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 173 | [codelife2020/deepseek-harness](https://github.com/codelife2020/deepseek-harness) | 1 | 17.8 (observed) | 25.918 | 22.668 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 174 | [guihuatu2022/deepseek-harness](https://github.com/guihuatu2022/deepseek-harness) | 1 | 17.6 (observed) | 25.918 | 22.581 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 175 | [DreamShepherd2006/deepseek-harness](https://github.com/DreamShepherd2006/deepseek-harness) | 0 | 15.3 (observed) | 27.371 | 22.551 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 176 | [studioburnside/deepseek-harness-internal](https://github.com/studioburnside/deepseek-harness-internal) | 1 | 17.3 (observed) | 25.918 | 22.452 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 177 | [monikalnbo/deepseek-harness](https://github.com/monikalnbo/deepseek-harness) | 1 | 16.9 (observed) | 26.000 | 22.380 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 178 | [lasme-ephrem/LasmeX](https://github.com/lasme-ephrem/LasmeX) | 1 | 16.8 (observed) | 26.031 | 22.350 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“Harness agentique open source, extensible et francophone par défaut”。 |
| 179 | [Erichy777/deepseek-harness](https://github.com/Erichy777/deepseek-harness) | 1 | 16.9 (observed) | 25.918 | 22.293 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 180 | [zilaliang/deepseek-harness](https://github.com/zilaliang/deepseek-harness) | 1 | 16.8 (observed) | 25.918 | 22.272 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 181 | [chyl00/deepseek-harness](https://github.com/chyl00/deepseek-harness) | 1 | 16.7 (observed) | 25.918 | 22.247 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 182 | [Lyowisee/deepseek-harness](https://github.com/Lyowisee/deepseek-harness) | 1 | 16.7 (observed) | 25.918 | 22.221 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 183 | [MK6657/deepseek-harness](https://github.com/MK6657/deepseek-harness) | 1 | 16.6 (observed) | 25.918 | 22.209 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“小男梁agent”。 |
| 184 | [lamost423/dsh-codex-experience](https://github.com/lamost423/dsh-codex-experience) | 1 | 16.4 (observed) | 26.001 | 22.178 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“Community DeepSeek Harness fork with Codex-style annotations, ephemeral side chat, and todo freshness enforcement”。 |
| 185 | [Eric-LLMs/deepseek-harness](https://github.com/Eric-LLMs/deepseek-harness) | 0 | 25.4 (observed) | 19.999 | 22.146 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 186 | [zy220/deepseek-harness](https://github.com/zy220/deepseek-harness) | 1 | 16.5 (observed) | 25.918 | 22.146 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“zy的ds-harness个人仓”。 |
| 187 | [yuzih888/deepseek-harness](https://github.com/yuzih888/deepseek-harness) | 1 | 16.5 (observed) | 25.918 | 22.143 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 188 | [MrNQC/deepseek-harness](https://github.com/MrNQC/deepseek-harness) | 1 | 16.4 (observed) | 25.918 | 22.091 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 189 | [SpxZhu/deepseek-harness](https://github.com/SpxZhu/deepseek-harness) | 1 | 16.1 (observed) | 25.954 | 22.028 | 2 | 24 | ok | 新增约 2 个提交并修改 24 个文件，主要涉及 CI/构建、UI/应用层、文档、配置；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 190 | [EdwardXIE6666/deepseek-harness](https://github.com/EdwardXIE6666/deepseek-harness) | 1 | 16.2 (observed) | 25.918 | 22.012 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 191 | [shijiejintoulwh/deepseek-harness](https://github.com/shijiejintoulwh/deepseek-harness) | 1 | 15.9 (observed) | 26.029 | 21.965 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 192 | [Yuan227719/deepseek-harness](https://github.com/Yuan227719/deepseek-harness) | 1 | 15.8 (observed) | 25.918 | 21.882 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 193 | [Ashveil1/deepseek-harness-ares](https://github.com/Ashveil1/deepseek-harness-ares) | 1 | 15.6 (observed) | 26.030 | 21.860 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek harness for pentesting”。 |
| 194 | [faguangdeyueliang/deepseek-harness](https://github.com/faguangdeyueliang/deepseek-harness) | 1 | 15.0 (observed) | 25.918 | 21.564 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 195 | [ITMAXOS/deepseek-harness](https://github.com/ITMAXOS/deepseek-harness) | 1 | 14.9 (observed) | 25.918 | 21.523 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 196 | [hanfengchiyi/deepseek-harness](https://github.com/hanfengchiyi/deepseek-harness) | 1 | 14.9 (observed) | 25.918 | 21.494 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 197 | [iMocking/deepseek-harness](https://github.com/iMocking/deepseek-harness) | 1 | 14.8 (observed) | 25.918 | 21.484 | — | 0 | metadata-only | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 198 | [Peter1Griffen/deepseek-harness](https://github.com/Peter1Griffen/deepseek-harness) | 1 | 14.7 (observed) | 25.918 | 21.435 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 199 | [znxiaoqi275/deepseek-harness](https://github.com/znxiaoqi275/deepseek-harness) | 1 | 14.6 (observed) | 25.946 | 21.425 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“梁帝永远的神”。 |
| 200 | [refengSGL/deepseek-harness](https://github.com/refengSGL/deepseek-harness) | 1 | 14.7 (observed) | 25.918 | 21.422 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |

> Showing the first 200 rows here; `11,113` rows are preserved in `index/forks.jsonl` and `docs/data/forks.json`.

## Interpretation

The collector records every public Fork returned by the paginated endpoint. Deep compare, recent commits, and README metadata are rotated by a per-run budget because GitHub rate limits make an unbounded daily deep audit impractical for a network of this size. Use `python3 scripts/collect_forks.py --deep-scan-all` only when the available token and request budget are sufficient.
