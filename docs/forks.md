# DeepSeek Harness Fork Network

- Dataset version: `v20260816T002558Z`
- Public Fork records: **11,223**
- Ranking filter: **0+ stars**; observed Fork identities: **11,223**; filtered out of ranking: **0**.
- Ever deep-scanned: **515 / 11,223** (4.59%); pending: **10,708**; conservative backfill ETA: **67 daily runs**.
- Deep-scanned successfully in the current projection: **515**; compare responses retained: **515**
- Fork rows with public owner reputation observed: **400**; the current ranking pool applies a configurable minimum-Star filter.
- Scope: public Forks returned by GitHub REST API pagination for `deepseek-ai/deepseek-harness`.
- Raw evidence is collected under `data/raw/forks/`; the [latest compressed SQLite snapshot](https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin/releases/download/dataset-latest/aggregator-full.sqlite3.zst) includes the fork tables and raw JSON payloads. Unpack it with `zstd -d aggregator-full.sqlite3.zst -o aggregator-full.sqlite3`.
- Searchable browser: `docs/forks.html`; compact catalog: `docs/data/fork-catalog.json`; complete machine-readable ranking: `index/forks.jsonl`.
- `overall score = repository influence 60% + public-account reputation 40%` when the profile is observed; missing profile signals are not treated as zero. This is a public-signal ordering aid, not a quality, safety, integrity, or endorsement claim.

## GitHub star order

| Star rank | Fork | Stars | Composite rank | Audit | Evidence |
| ---: | --- | ---: | ---: | --- | --- |
| 1 | [salathleizhang/deepseek-harness-desktop](https://github.com/salathleizhang/deepseek-harness-desktop) | 98 | 1 | audited | 新增约 42 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“Native desktop app for DeepSeek Harness — an Electron shell that runs the harness locally and hosts the official Web GUI unchanged”。 |
| 2 | [Sakana-yuyu/deepseek-harness-desktop](https://github.com/Sakana-yuyu/deepseek-harness-desktop) | 22 | 7 | audited | 新增约 14 个提交并修改 81 个文件，主要涉及 配置、文档、CI/构建、UI/应用层；目标线索是“Rust构建的客户端，体积更小，更方便，Mac，win，linux已完成”。 |
| 3 | [G36maid/deepseek-harness](https://github.com/G36maid/deepseek-harness) | 12 | 6 | audited | 新增约 19 个提交并修改 300 个文件，主要涉及 配置、文档；目标线索是“DeepSeek Harness 繁體中文版 (zh-TW) — Everything is a Plugin”。 |
| 4 | [Skyearn/deepseek-harness-app](https://github.com/Skyearn/deepseek-harness-app) | 11 | 11 | audited | 新增约 24 个提交并修改 31 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness Desktop”。 |
| 5 | [rpmalouin/deepseek-harness](https://github.com/rpmalouin/deepseek-harness) | 9 | 13 | audited | 新增约 4 个提交并修改 31 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 6 | [yx54hego-cloud/deepseek-harness](https://github.com/yx54hego-cloud/deepseek-harness) | 7 | 147 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 7 | [Ajwyunsx/deepseek-harness-mobile](https://github.com/Ajwyunsx/deepseek-harness-mobile) | 4 | 3 | audited | 新增约 10 个提交并修改 40 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 8 | [happylin0x29a/deepseek-harness-desktop](https://github.com/happylin0x29a/deepseek-harness-desktop) | 4 | 21 | audited | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness desktop base on tauri”。 |
| 9 | [luolangaga/deepseek-harness](https://github.com/luolangaga/deepseek-harness) | 4 | 32 | audited | 新增约 11 个提交并修改 54 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 10 | [puppywang/deepseek-harness](https://github.com/puppywang/deepseek-harness) | 4 | 15 | audited | 新增约 10 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 11 | [sdkwork-ai/deepseek-harness-desktop](https://github.com/sdkwork-ai/deepseek-harness-desktop) | 4 | 12 | audited | 新增约 48 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 12 | [yazzang-homelab/deepseek-harness](https://github.com/yazzang-homelab/deepseek-harness) | 2 | 93 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 13 | [FSMargoo/deepseek-harness](https://github.com/FSMargoo/deepseek-harness) | 2 | 29 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 14 | [huiliyi37/deepseek-harness](https://github.com/huiliyi37/deepseek-harness) | 2 | 111 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 15 | [Kiowx/deepseek-harness](https://github.com/Kiowx/deepseek-harness) | 2 | 114 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 16 | [MarceloClaro/deepseek-harness](https://github.com/MarceloClaro/deepseek-harness) | 2 | 22 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 17 | [stophobia/deepseek-harness](https://github.com/stophobia/deepseek-harness) | 2 | 8 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 18 | [suiyuebaobao/deepseek-harness-gui](https://github.com/suiyuebaobao/deepseek-harness-gui) | 2 | 175 | audited | 新增约 2 个提交并修改 52 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“Windows desktop fork of DeepSeek Harness, packaged with Tauri while preserving the full Web profile and plugin runtime”。 |
| 19 | [Yihong89/deepseek-harness](https://github.com/Yihong89/deepseek-harness) | 2 | 60 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 20 | [srwang0506/deepseek-harness](https://github.com/srwang0506/deepseek-harness) | 1 | 80 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 21 | [xiaosenho/deepseek-harness](https://github.com/xiaosenho/deepseek-harness) | 1 | 131 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 22 | [007M7/deepseek-harness](https://github.com/007M7/deepseek-harness) | 1 | 180 | audited | 未观察到相对 upstream 的文件修改；目标线索是“我永远喜欢deepseek！！！”。 |
| 23 | [123prompt/deepseek-harness](https://github.com/123prompt/deepseek-harness) | 1 | 249 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 24 | [1486482143/deepseek-harness](https://github.com/1486482143/deepseek-harness) | 1 | 256 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 25 | [18217778896/deepseek-harness](https://github.com/18217778896/deepseek-harness) | 1 | 153 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 26 | [2404589803/deepseek-harness](https://github.com/2404589803/deepseek-harness) | 1 | 52 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 27 | [485524097/deepseek-harness](https://github.com/485524097/deepseek-harness) | 1 | 277 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 28 | [4evour/deepseek-harness](https://github.com/4evour/deepseek-harness) | 1 | 142 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 29 | [a907781273-a11y/deepseek-harness](https://github.com/a907781273-a11y/deepseek-harness) | 1 | 11167 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 30 | [achristofaro/deepseek-harness](https://github.com/achristofaro/deepseek-harness) | 1 | 55 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 31 | [AI-1-TOP/deepseek-harness](https://github.com/AI-1-TOP/deepseek-harness) | 1 | 11199 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 32 | [aimierbear/TinyWhale](https://github.com/aimierbear/TinyWhale) | 1 | 226 | audited | 新增约 18 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、CI/构建；目标线索是“TinyWhale — desktop-oriented MIT fork of DeepSeek Harness, with an Electron shell in desktop/”。 |
| 33 | [alexdeweb/deepseek-harness](https://github.com/alexdeweb/deepseek-harness) | 1 | 84 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 34 | [alexdolbun/deepseek-harness](https://github.com/alexdolbun/deepseek-harness) | 1 | 5 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 35 | [Alsdara/deepseek-harness](https://github.com/Alsdara/deepseek-harness) | 1 | 11155 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 36 | [Anyaoha/deepseek-harness](https://github.com/Anyaoha/deepseek-harness) | 1 | 49 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 37 | [Ashveil1/deepseek-harness-ares](https://github.com/Ashveil1/deepseek-harness-ares) | 1 | 236 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek harness for pentesting”。 |
| 38 | [athif23/deepseek-harness](https://github.com/athif23/deepseek-harness) | 1 | 28 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 39 | [ayushare/deepseek-harness](https://github.com/ayushare/deepseek-harness) | 1 | 11120 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 40 | [b3nk-x1/deepseek-harness](https://github.com/b3nk-x1/deepseek-harness) | 1 | 11173 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 41 | [badestgod/deepseek-harness](https://github.com/badestgod/deepseek-harness) | 1 | 94 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 42 | [Beam-wi/deepseek-harness](https://github.com/Beam-wi/deepseek-harness) | 1 | 170 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 43 | [ben-vargas/ai-deepseek-harness](https://github.com/ben-vargas/ai-deepseek-harness) | 1 | 17 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 44 | [biyan113/deepseek-harness](https://github.com/biyan113/deepseek-harness) | 1 | 128 | audited | 新增约 3 个提交并修改 55 个文件，主要涉及 CI/构建、UI/应用层、文档、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 45 | [BlackRosePetals/deepseek-harness](https://github.com/BlackRosePetals/deepseek-harness) | 1 | 136 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 46 | [BobcGn/deepseek-harness-app](https://github.com/BobcGn/deepseek-harness-app) | 1 | 145 | audited | 新增约 14 个提交并修改 31 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 47 | [bojieli/deepseek-harness](https://github.com/bojieli/deepseek-harness) | 1 | 4 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 48 | [boktoday/deepseek-harness](https://github.com/boktoday/deepseek-harness) | 1 | 48 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 49 | [BurtonQin/deepseek-harness](https://github.com/BurtonQin/deepseek-harness) | 1 | 20 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 50 | [CatchCatOoO/deepseek-harness](https://github.com/CatchCatOoO/deepseek-harness) | 1 | 198 | audited | 新增约 4 个提交并修改 300 个文件，主要涉及 文档、配置、agent/skill 能力；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 51 | [cFqr-lang/deepseek-harness](https://github.com/cFqr-lang/deepseek-harness) | 1 | 11162 | audited | 新增约 5 个提交并修改 57 个文件，主要涉及 UI/应用层、Harness 核心能力、配置、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 52 | [CH-HGod/deepseek-harness](https://github.com/CH-HGod/deepseek-harness) | 1 | 11141 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 53 | [chiekoschamburek-dev/deepseek-harness](https://github.com/chiekoschamburek-dev/deepseek-harness) | 1 | 11159 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 54 | [China-MY/deepseek-harness](https://github.com/China-MY/deepseek-harness) | 1 | 99 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 55 | [chyl00/deepseek-harness](https://github.com/chyl00/deepseek-harness) | 1 | 221 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 56 | [cioerp/deepseek-harness](https://github.com/cioerp/deepseek-harness) | 1 | 11193 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 57 | [codelife2020/deepseek-harness](https://github.com/codelife2020/deepseek-harness) | 1 | 209 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 58 | [coder-v0/deepseek-harness](https://github.com/coder-v0/deepseek-harness) | 1 | 86 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 59 | [cq2021-coder/deepseek-harness-desktop](https://github.com/cq2021-coder/deepseek-harness-desktop) | 1 | 96 | audited | 未观察到相对 upstream 的文件修改；目标线索是“使用 tauri 为 DeepSeek Harness 生态打造的现代化桌面端应用”。 |
| 60 | [criapa/deepseek-harness](https://github.com/criapa/deepseek-harness) | 1 | 37 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 61 | [Cute-chen/deepseek-harness-app](https://github.com/Cute-chen/deepseek-harness-app) | 1 | 202 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 62 | [Cyenoch/deepseek-harness](https://github.com/Cyenoch/deepseek-harness) | 1 | 61 | audited | 新增约 13 个提交并修改 300 个文件，主要涉及 配置、文档、agent/skill 能力、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 63 | [cyh7777/deepseek-harness](https://github.com/cyh7777/deepseek-harness) | 1 | 11143 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 64 | [dailin3/deepseek-harness](https://github.com/dailin3/deepseek-harness) | 1 | 127 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 65 | [DailyR/deepseek-harness](https://github.com/DailyR/deepseek-harness) | 1 | 31 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 66 | [ddd666j/deepseek-harness](https://github.com/ddd666j/deepseek-harness) | 1 | 11180 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 67 | [DeepThinkingZhouLiu/Deepseek-Harness-RSI](https://github.com/DeepThinkingZhouLiu/Deepseek-Harness-RSI) | 1 | 69 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 68 | [deveuper/deepseek-harness](https://github.com/deveuper/deepseek-harness) | 1 | 149 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 69 | [devin2255/deepseek-harness-desktop](https://github.com/devin2255/deepseek-harness-desktop) | 1 | 87 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 70 | [djhh555/deepseek-sightline](https://github.com/djhh555/deepseek-sightline) | 1 | 11151 | audited | 新增约 2 个提交并修改 43 个文件，主要涉及 文档、UI/应用层、依赖、Harness 核心能力；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 71 | [DogeJian/deepseek-harness](https://github.com/DogeJian/deepseek-harness) | 1 | 72 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 72 | [donstang/deepseek-harness](https://github.com/donstang/deepseek-harness) | 1 | 33 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 73 | [dorucioclea/deepseek-harness](https://github.com/dorucioclea/deepseek-harness) | 1 | 10 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 74 | [drscrewdriver/deepseek-harness](https://github.com/drscrewdriver/deepseek-harness) | 1 | 68 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 75 | [duliangkuan/deepseek-harness](https://github.com/duliangkuan/deepseek-harness) | 1 | 168 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 76 | [EdwardXIE6666/deepseek-harness](https://github.com/EdwardXIE6666/deepseek-harness) | 1 | 233 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 77 | [enbideren/deepseek-harness](https://github.com/enbideren/deepseek-harness) | 1 | 73 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 78 | [equable66/deepseek-harness](https://github.com/equable66/deepseek-harness) | 1 | 1009 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 79 | [Erichy777/deepseek-harness](https://github.com/Erichy777/deepseek-harness) | 1 | 219 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 80 | [Ericsongyl/deepseek-harness](https://github.com/Ericsongyl/deepseek-harness) | 1 | 25 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 81 | [ermao009/deepseek-harness](https://github.com/ermao009/deepseek-harness) | 1 | 266 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 82 | [exposir/deepseek-harness](https://github.com/exposir/deepseek-harness) | 1 | 27 | audited | 新增约 9 个提交并修改 13 个文件，主要涉及 文档、Harness 核心能力、测试；目标线索是“DeepSeek Harness”。 |
| 83 | [fage45029704-lgtm/deepseek-harness](https://github.com/fage45029704-lgtm/deepseek-harness) | 1 | 11165 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 84 | [faguangdeyueliang/deepseek-harness](https://github.com/faguangdeyueliang/deepseek-harness) | 1 | 238 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 85 | [fendouai/deepseek-harness-desktop](https://github.com/fendouai/deepseek-harness-desktop) | 1 | 9 | audited | 新增约 10 个提交并修改 123 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 86 | [fisher158163/deepseek-harness](https://github.com/fisher158163/deepseek-harness) | 1 | 23 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 87 | [flaqai/open-deepseek-harness-desktop](https://github.com/flaqai/open-deepseek-harness-desktop) | 1 | 181 | audited | 未观察到相对 upstream 的文件修改；目标线索是“Open Source Desktop for DeepSeek Harness. DeepSeek Harness: Everything is a Plugin”。 |
| 88 | [flowersea302/deepseek-harness](https://github.com/flowersea302/deepseek-harness) | 1 | 273 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 89 | [FlyingSama/deepseek-harness](https://github.com/FlyingSama/deepseek-harness) | 1 | 207 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 90 | [GavinDong-plaud/deepseek-harness](https://github.com/GavinDong-plaud/deepseek-harness) | 1 | 11140 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 91 | [GetSayAll/deepseek-harness-app](https://github.com/GetSayAll/deepseek-harness-app) | 1 | 11149 | audited | 新增约 25 个提交并修改 118 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek Harness”。 |
| 92 | [ghthh/deepseek-harness](https://github.com/ghthh/deepseek-harness) | 1 | 11118 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 93 | [GTC2080/deepseek-harness](https://github.com/GTC2080/deepseek-harness) | 1 | 176 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness 桌面端：基于 Tauri，支持 macOS 与 Windows；源码位于 desktop 分支”。 |
| 94 | [guihuatu2022/deepseek-harness](https://github.com/guihuatu2022/deepseek-harness) | 1 | 212 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 95 | [GZZ-523/deepseek-harness](https://github.com/GZZ-523/deepseek-harness) | 1 | 201 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 96 | [hanfengchiyi/deepseek-harness](https://github.com/hanfengchiyi/deepseek-harness) | 1 | 240 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 97 | [hanqi9622-eng/deepseek-harness](https://github.com/hanqi9622-eng/deepseek-harness) | 1 | 11178 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 98 | [HaoyanZhang123/deepseek-harness-live-preset-switch](https://github.com/HaoyanZhang123/deepseek-harness-live-preset-switch) | 1 | 11158 | audited | 新增约 2 个提交并修改 81 个文件，主要涉及 文档、agent/skill 能力、UI/应用层、Harness 核心能力；目标线索是“DeepSeek Harness with live agent-preset switching at turn boundaries”。 |
| 99 | [heleileimail-cmyk/deepseek-harness](https://github.com/heleileimail-cmyk/deepseek-harness) | 1 | 11156 | audited | 新增约 3 个提交并修改 22 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 100 | [HelloNicoo/deepseek-harness](https://github.com/HelloNicoo/deepseek-harness) | 1 | 116 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |

## Modification categories

| Category | Changed paths |
| --- | ---: |
| docs | 1,894 |
| harness-core | 1,093 |
| dependencies | 1,026 |
| ui-and-apps | 923 |
| configuration | 831 |
| tests | 480 |
| other | 169 |
| ci-and-build | 54 |
| tools-and-scripts | 51 |
| agents-and-skills | 38 |

## Influence order

| Rank | Fork | Stars | Owner reputation | Repo influence | Overall | Ahead | Changed files | Deep status | One-sentence evidence |
| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | --- | --- |
| 1 | [salathleizhang/deepseek-harness-desktop](https://github.com/salathleizhang/deepseek-harness-desktop) | 98 | 36.0 (observed) | 74.983 | 59.389 | 42 | 300 | ok | 新增约 42 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“Native desktop app for DeepSeek Harness — an Electron shell that runs the harness locally and hosts the official Web GUI unchanged”。 |
| 2 | [jasonkneen/deepseek-harness-plus](https://github.com/jasonkneen/deepseek-harness-plus) | 1 | 77.0 (observed) | 41.054 | 55.450 | 2 | 103 | ok | 新增约 2 个提交并修改 103 个文件，主要涉及 配置、文档、依赖、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 3 | [Ajwyunsx/deepseek-harness-mobile](https://github.com/Ajwyunsx/deepseek-harness-mobile) | 4 | 36.6 (observed) | 57.431 | 49.090 | 10 | 40 | ok | 新增约 10 个提交并修改 40 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 4 | [bojieli/deepseek-harness](https://github.com/bojieli/deepseek-harness) | 1 | 81.4 (observed) | 25.898 | 48.097 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 5 | [alexdolbun/deepseek-harness](https://github.com/alexdolbun/deepseek-harness) | 1 | 80.0 (observed) | 25.898 | 47.554 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 6 | [G36maid/deepseek-harness](https://github.com/G36maid/deepseek-harness) | 12 | 54.4 (observed) | 42.294 | 47.153 | 19 | 300 | ok | 新增约 19 个提交并修改 300 个文件，主要涉及 配置、文档；目标线索是“DeepSeek Harness 繁體中文版 (zh-TW) — Everything is a Plugin”。 |
| 7 | [Sakana-yuyu/deepseek-harness-desktop](https://github.com/Sakana-yuyu/deepseek-harness-desktop) | 22 | 35.5 (observed) | 54.722 | 47.038 | 14 | 81 | ok | 新增约 14 个提交并修改 81 个文件，主要涉及 配置、文档、CI/构建、UI/应用层；目标线索是“Rust构建的客户端，体积更小，更方便，Mac，win，linux已完成”。 |
| 8 | [stophobia/deepseek-harness](https://github.com/stophobia/deepseek-harness) | 2 | 70.7 (observed) | 29.428 | 45.920 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 9 | [fendouai/deepseek-harness-desktop](https://github.com/fendouai/deepseek-harness-desktop) | 1 | 72.1 (observed) | 26.001 | 44.434 | 10 | 123 | ok | 新增约 10 个提交并修改 123 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 10 | [dorucioclea/deepseek-harness](https://github.com/dorucioclea/deepseek-harness) | 1 | 71.8 (observed) | 25.898 | 44.241 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 11 | [Skyearn/deepseek-harness-app](https://github.com/Skyearn/deepseek-harness-app) | 11 | 34.3 (observed) | 49.082 | 43.178 | 24 | 31 | ok | 新增约 24 个提交并修改 31 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness Desktop”。 |
| 12 | [sdkwork-ai/deepseek-harness-desktop](https://github.com/sdkwork-ai/deepseek-harness-desktop) | 4 | 17.9 (observed) | 59.010 | 42.570 | 48 | 300 | ok | 新增约 48 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 13 | [rpmalouin/deepseek-harness](https://github.com/rpmalouin/deepseek-harness) | 9 | 34.9 (observed) | 47.488 | 42.453 | 4 | 31 | ok | 新增约 4 个提交并修改 31 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 14 | [lixun910/deepseek-harness](https://github.com/lixun910/deepseek-harness) | 1 | 64.0 (observed) | 25.898 | 41.129 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 15 | [puppywang/deepseek-harness](https://github.com/puppywang/deepseek-harness) | 4 | 49.7 (observed) | 33.947 | 40.263 | 10 | 300 | ok | 新增约 10 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 16 | [Sailfishc/deepseek-harness](https://github.com/Sailfishc/deepseek-harness) | 1 | 61.2 (observed) | 25.898 | 40.024 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 17 | [ben-vargas/ai-deepseek-harness](https://github.com/ben-vargas/ai-deepseek-harness) | 1 | 59.6 (observed) | 25.898 | 39.391 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 18 | [TKaxv-7S/deepseek-harness](https://github.com/TKaxv-7S/deepseek-harness) | 1 | 59.4 (observed) | 25.898 | 39.285 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 19 | [rferrari/deepseek-harness](https://github.com/rferrari/deepseek-harness) | 1 | 58.8 (observed) | 25.898 | 39.054 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 20 | [BurtonQin/deepseek-harness](https://github.com/BurtonQin/deepseek-harness) | 1 | 58.2 (observed) | 25.898 | 38.825 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 21 | [happylin0x29a/deepseek-harness-desktop](https://github.com/happylin0x29a/deepseek-harness-desktop) | 4 | 34.6 (observed) | 41.414 | 38.704 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness desktop base on tauri”。 |
| 22 | [MarceloClaro/deepseek-harness](https://github.com/MarceloClaro/deepseek-harness) | 2 | 50.6 (observed) | 29.428 | 37.888 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 23 | [fisher158163/deepseek-harness](https://github.com/fisher158163/deepseek-harness) | 1 | 54.9 (observed) | 25.898 | 37.519 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 24 | [risyasin/deepseek-harness](https://github.com/risyasin/deepseek-harness) | 0 | 63.5 (observed) | 19.995 | 37.401 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 25 | [Ericsongyl/deepseek-harness](https://github.com/Ericsongyl/deepseek-harness) | 1 | 54.5 (observed) | 25.898 | 37.332 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 26 | [manuelapetsi/deepseek-harness](https://github.com/manuelapetsi/deepseek-harness) | 1 | 54.3 (observed) | 25.898 | 37.247 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 27 | [exposir/deepseek-harness](https://github.com/exposir/deepseek-harness) | 1 | 52.3 (observed) | 25.942 | 36.477 | 9 | 13 | ok | 新增约 9 个提交并修改 13 个文件，主要涉及 文档、Harness 核心能力、测试；目标线索是“DeepSeek Harness”。 |
| 28 | [athif23/deepseek-harness](https://github.com/athif23/deepseek-harness) | 1 | 51.7 (observed) | 25.898 | 36.208 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 29 | [FSMargoo/deepseek-harness](https://github.com/FSMargoo/deepseek-harness) | 2 | 46.1 (observed) | 29.427 | 36.104 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 30 | [zchuhui/deepseek-harness](https://github.com/zchuhui/deepseek-harness) | 1 | 48.7 (observed) | 25.996 | 35.092 | 7 | 300 | ok | 新增约 7 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 31 | [DailyR/deepseek-harness](https://github.com/DailyR/deepseek-harness) | 1 | 48.7 (observed) | 25.898 | 35.037 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 32 | [luolangaga/deepseek-harness](https://github.com/luolangaga/deepseek-harness) | 4 | 36.4 (observed) | 33.919 | 34.900 | 11 | 54 | ok | 新增约 11 个提交并修改 54 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 33 | [donstang/deepseek-harness](https://github.com/donstang/deepseek-harness) | 1 | 48.0 (observed) | 25.898 | 34.745 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 34 | [LCYLYM/deepseek-harness](https://github.com/LCYLYM/deepseek-harness) | 1 | 47.7 (observed) | 25.898 | 34.602 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 35 | [Razor87/deepseek-harness](https://github.com/Razor87/deepseek-harness) | 1 | 47.6 (observed) | 25.898 | 34.598 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 36 | [lkngin/deepseek-harness](https://github.com/lkngin/deepseek-harness) | 1 | 47.5 (observed) | 25.898 | 34.520 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 37 | [criapa/deepseek-harness](https://github.com/criapa/deepseek-harness) | 1 | 47.3 (observed) | 25.898 | 34.469 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 38 | [cololi/deepseek-harness](https://github.com/cololi/deepseek-harness) | 0 | 55.9 (observed) | 19.984 | 34.365 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 39 | [zhanglunet/deepseek-harness](https://github.com/zhanglunet/deepseek-harness) | 0 | 55.7 (observed) | 19.993 | 34.278 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 40 | [himomohi/deepseek-harness](https://github.com/himomohi/deepseek-harness) | 1 | 46.5 (observed) | 26.003 | 34.210 | 36 | 300 | ok | 新增约 36 个提交并修改 300 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 41 | [yomaser/deepseek-harness](https://github.com/yomaser/deepseek-harness) | 1 | 46.3 (observed) | 25.898 | 34.039 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 42 | [nydia/deepseek-harness](https://github.com/nydia/deepseek-harness) | 1 | 46.2 (observed) | 25.898 | 34.005 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 43 | [MauricioPerera/deepseek-harness](https://github.com/MauricioPerera/deepseek-harness) | 0 | 54.9 (observed) | 19.994 | 33.964 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 44 | [179309463/deepseek-harness](https://github.com/179309463/deepseek-harness) | 0 | 39.5 (observed) | 29.783 | 33.682 | 1 | 20 | ok | 新增约 1 个提交并修改 20 个文件，主要涉及 文档、agent/skill 能力、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 45 | [winddyhe/deepseek-harness](https://github.com/winddyhe/deepseek-harness) | 0 | 53.6 (observed) | 19.985 | 33.432 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 46 | [jbwashington/deepseek-harness](https://github.com/jbwashington/deepseek-harness) | 0 | 53.5 (observed) | 19.996 | 33.397 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 47 | [odonzyk/deepseek-harness](https://github.com/odonzyk/deepseek-harness) | 1 | 44.4 (observed) | 25.898 | 33.318 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 48 | [boktoday/deepseek-harness](https://github.com/boktoday/deepseek-harness) | 1 | 44.2 (observed) | 25.898 | 33.201 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 49 | [Anyaoha/deepseek-harness](https://github.com/Anyaoha/deepseek-harness) | 1 | 44.0 (observed) | 25.898 | 33.122 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 50 | [ahmedsliman/deepseek-harness](https://github.com/ahmedsliman/deepseek-harness) | 0 | 52.8 (observed) | 19.985 | 33.115 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 51 | [vkn129/deepseek-harness](https://github.com/vkn129/deepseek-harness) | 1 | 43.9 (observed) | 25.898 | 33.099 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 52 | [2404589803/deepseek-harness](https://github.com/2404589803/deepseek-harness) | 1 | 43.8 (observed) | 25.898 | 33.057 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 53 | [shenyimings/deepseek-harness](https://github.com/shenyimings/deepseek-harness) | 1 | 43.7 (observed) | 25.898 | 33.022 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 54 | [roadlittledawn/deepseek-harness](https://github.com/roadlittledawn/deepseek-harness) | 1 | 42.9 (observed) | 25.898 | 32.692 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 55 | [achristofaro/deepseek-harness](https://github.com/achristofaro/deepseek-harness) | 1 | 42.6 (observed) | 25.898 | 32.579 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 56 | [leether/deepseek-harness](https://github.com/leether/deepseek-harness) | 0 | 51.1 (observed) | 19.984 | 32.420 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 57 | [mnky4a6/deepseek-harness](https://github.com/mnky4a6/deepseek-harness) | 1 | 42.1 (observed) | 25.898 | 32.397 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 58 | [phong711/deepseek-harness](https://github.com/phong711/deepseek-harness) | 1 | 42.1 (observed) | 25.898 | 32.390 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 59 | [BJTU-Netcomm/deepseek-harness-aiops](https://github.com/BJTU-Netcomm/deepseek-harness-aiops) | 0 | 39.4 (observed) | 27.364 | 32.195 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness for aiops: Everything is a Plugin”。 |
| 60 | [Yihong89/deepseek-harness](https://github.com/Yihong89/deepseek-harness) | 2 | 36.3 (observed) | 29.428 | 32.171 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 61 | [Cyenoch/deepseek-harness](https://github.com/Cyenoch/deepseek-harness) | 1 | 41.4 (observed) | 25.997 | 32.158 | 13 | 300 | ok | 新增约 13 个提交并修改 300 个文件，主要涉及 配置、文档、agent/skill 能力、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 62 | [pawaca/dsh-edge](https://github.com/pawaca/dsh-edge) | 0 | 50.1 (observed) | 20.000 | 32.054 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 63 | [missuzhang/deepseek-harness](https://github.com/missuzhang/deepseek-harness) | 1 | 41.2 (observed) | 25.898 | 32.003 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 64 | [Mike-7777777/deepseek-harness](https://github.com/Mike-7777777/deepseek-harness) | 1 | 40.6 (observed) | 25.898 | 31.790 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 65 | [GitHubxsy/deepseek-harness](https://github.com/GitHubxsy/deepseek-harness) | 0 | 49.4 (observed) | 19.999 | 31.775 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 66 | [mallocxw/deepseek-harness](https://github.com/mallocxw/deepseek-harness) | 1 | 40.0 (observed) | 25.898 | 31.531 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 67 | [xiaolangde/deepseek-harness](https://github.com/xiaolangde/deepseek-harness) | 1 | 39.7 (observed) | 25.948 | 31.436 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 68 | [drscrewdriver/deepseek-harness](https://github.com/drscrewdriver/deepseek-harness) | 1 | 38.7 (observed) | 25.898 | 31.009 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 69 | [DeepThinkingZhouLiu/Deepseek-Harness-RSI](https://github.com/DeepThinkingZhouLiu/Deepseek-Harness-RSI) | 1 | 38.3 (observed) | 26.018 | 30.911 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 70 | [Vitaminaq/deepseek-harness](https://github.com/Vitaminaq/deepseek-harness) | 1 | 38.0 (observed) | 25.932 | 30.740 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 71 | [Tyler-R-Kendrick/deepseek-harness](https://github.com/Tyler-R-Kendrick/deepseek-harness) | 1 | 38.0 (observed) | 25.898 | 30.724 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 72 | [DogeJian/deepseek-harness](https://github.com/DogeJian/deepseek-harness) | 1 | 37.9 (observed) | 25.898 | 30.682 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 73 | [enbideren/deepseek-harness](https://github.com/enbideren/deepseek-harness) | 1 | 37.8 (observed) | 25.898 | 30.675 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 74 | [xiansheng888/deepseek-harness](https://github.com/xiansheng888/deepseek-harness) | 1 | 37.4 (observed) | 25.898 | 30.513 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 75 | [mgrillo75/deepseek-harness](https://github.com/mgrillo75/deepseek-harness) | 1 | 37.3 (observed) | 25.898 | 30.461 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 76 | [realchenwenqiao/dash-fork](https://github.com/realchenwenqiao/dash-fork) | 1 | 37.1 (observed) | 25.935 | 30.406 | 35 | 38 | ok | 新增约 35 个提交并修改 38 个文件，主要涉及 文档、依赖、UI/应用层、其他文件；目标线索是“DASH — terminal-native TUI for DeepSeek Harness: Claude Code-style full-screen interface, multi-model switching, behavior-ledger rewind”。 |
| 77 | [v2hoping/deepseek-harness-desktop](https://github.com/v2hoping/deepseek-harness-desktop) | 1 | 36.4 (observed) | 26.018 | 30.164 | 15 | 73 | ok | 新增约 15 个提交并修改 73 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin. Supports desktop installation and DeepSeek account login”。 |
| 78 | [angry-shark/deepseek-harness](https://github.com/angry-shark/deepseek-harness) | 0 | 45.1 (observed) | 19.987 | 30.036 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 79 | [Linmoqian/deepseek-harness-cli](https://github.com/Linmoqian/deepseek-harness-cli) | 1 | 36.2 (observed) | 25.898 | 30.020 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness-cli版本”。 |
| 80 | [srwang0506/deepseek-harness](https://github.com/srwang0506/deepseek-harness) | 1 | 24.3 (observed) | 33.521 | 29.816 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 81 | [SamboHassan/deepseek-harness](https://github.com/SamboHassan/deepseek-harness) | 1 | 35.5 (observed) | 25.898 | 29.724 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 82 | [ouyangyipeng/dsh-desktop-upstream-archive](https://github.com/ouyangyipeng/dsh-desktop-upstream-archive) | 1 | 35.3 (observed) | 25.936 | 29.700 | 12 | 67 | ok | 新增约 12 个提交并修改 67 个文件，主要涉及 配置、文档、其他文件、依赖；目标线索是“Archived upstream fork that preceded the independent DS-Harness Desktop repository”。 |
| 83 | [BeiKeJieDeLiuLangMao/deepseek-harness-gestalt](https://github.com/BeiKeJieDeLiuLangMao/deepseek-harness-gestalt) | 0 | 44.2 (observed) | 19.990 | 29.687 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 84 | [alexdeweb/deepseek-harness](https://github.com/alexdeweb/deepseek-harness) | 1 | 35.0 (observed) | 25.898 | 29.525 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 85 | [rvndnishad-work/deepseek-harness](https://github.com/rvndnishad-work/deepseek-harness) | 1 | 34.9 (observed) | 25.898 | 29.515 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 86 | [coder-v0/deepseek-harness](https://github.com/coder-v0/deepseek-harness) | 1 | 34.9 (observed) | 25.898 | 29.511 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 87 | [devin2255/deepseek-harness-desktop](https://github.com/devin2255/deepseek-harness-desktop) | 1 | 34.6 (observed) | 25.898 | 29.397 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 88 | [JayTing511/deepseek-harness](https://github.com/JayTing511/deepseek-harness) | 1 | 34.3 (observed) | 25.898 | 29.267 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 89 | [luoxunhao/deepseek-harness](https://github.com/luoxunhao/deepseek-harness) | 1 | 34.0 (observed) | 25.898 | 29.131 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 90 | [Stool233/deepseek-harness](https://github.com/Stool233/deepseek-harness) | 0 | 42.8 (observed) | 19.986 | 29.117 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 91 | [playboy662/deepseek-harness](https://github.com/playboy662/deepseek-harness) | 1 | 33.7 (observed) | 25.898 | 29.017 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 92 | [zenghuan/deepseek-harness](https://github.com/zenghuan/deepseek-harness) | 1 | 33.4 (observed) | 25.898 | 28.915 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 93 | [yazzang-homelab/deepseek-harness](https://github.com/yazzang-homelab/deepseek-harness) | 2 | 16.5 (observed) | 36.928 | 28.765 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 94 | [badestgod/deepseek-harness](https://github.com/badestgod/deepseek-harness) | 1 | 33.0 (observed) | 25.898 | 28.755 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 95 | [houkang/deepseek-harness](https://github.com/houkang/deepseek-harness) | 1 | 32.8 (observed) | 25.898 | 28.677 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness”。 |
| 96 | [cq2021-coder/deepseek-harness-desktop](https://github.com/cq2021-coder/deepseek-harness-desktop) | 1 | 32.7 (observed) | 25.963 | 28.663 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“使用 tauri 为 DeepSeek Harness 生态打造的现代化桌面端应用”。 |
| 97 | [HybridMAS/deepseek-harness](https://github.com/HybridMAS/deepseek-harness) | 1 | 32.7 (observed) | 25.898 | 28.614 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 98 | [2938236819/deepseek-harness](https://github.com/2938236819/deepseek-harness) | 0 | 18.6 (observed) | 35.214 | 28.577 | 6 | 48 | ok | 新增约 6 个提交并修改 48 个文件，主要涉及 文档、依赖、Harness 核心能力、测试；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 99 | [China-MY/deepseek-harness](https://github.com/China-MY/deepseek-harness) | 1 | 32.6 (observed) | 25.898 | 28.566 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 100 | [ldsenow/deepseek-harness](https://github.com/ldsenow/deepseek-harness) | 0 | 41.3 (observed) | 19.984 | 28.522 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 101 | [tomchon/deepseek-harness](https://github.com/tomchon/deepseek-harness) | 1 | 32.0 (observed) | 25.898 | 28.339 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 102 | [youshen2/deepseek-harness](https://github.com/youshen2/deepseek-harness) | 1 | 31.8 (observed) | 25.965 | 28.310 | 3 | 51 | ok | 新增约 3 个提交并修改 51 个文件，主要涉及 配置、文档、其他文件、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 103 | [valentinshenfeld/deepseek-harness](https://github.com/valentinshenfeld/deepseek-harness) | 1 | 31.9 (observed) | 25.898 | 28.302 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 104 | [MasterToycode/deepseek-harness](https://github.com/MasterToycode/deepseek-harness) | 1 | 31.9 (observed) | 25.898 | 28.281 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 105 | [spgsroot/deepseek-harness](https://github.com/spgsroot/deepseek-harness) | 0 | 40.3 (observed) | 19.989 | 28.117 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 106 | [shdeng/deepseek-harness-app](https://github.com/shdeng/deepseek-harness-app) | 1 | 31.3 (observed) | 26.010 | 28.107 | 10 | 220 | ok | 新增约 10 个提交并修改 220 个文件，主要涉及 配置、文档、其他文件、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 107 | [HossamTabana/deepseek-harness](https://github.com/HossamTabana/deepseek-harness) | 1 | 31.3 (observed) | 25.898 | 28.071 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 108 | [gladmo/deepseek-harness](https://github.com/gladmo/deepseek-harness) | 0 | 39.9 (observed) | 19.987 | 27.963 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 109 | [Shengqi-Pan/deepseek-harness](https://github.com/Shengqi-Pan/deepseek-harness) | 0 | 39.5 (observed) | 19.985 | 27.797 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 110 | [slamsmart/deepseek-harness](https://github.com/slamsmart/deepseek-harness) | 1 | 30.6 (observed) | 25.898 | 27.782 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 111 | [huiliyi37/deepseek-harness](https://github.com/huiliyi37/deepseek-harness) | 2 | 25.1 (observed) | 29.428 | 27.707 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 112 | [maigadohcrypto/deepseek-harness](https://github.com/maigadohcrypto/deepseek-harness) | 1 | 30.2 (observed) | 25.898 | 27.633 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 113 | [wellfuture/deepseek-harness](https://github.com/wellfuture/deepseek-harness) | 1 | 30.1 (observed) | 25.898 | 27.568 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 114 | [Kiowx/deepseek-harness](https://github.com/Kiowx/deepseek-harness) | 2 | 24.6 (observed) | 29.470 | 27.510 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 115 | [HugoluizMTB/deepseek-harness](https://github.com/HugoluizMTB/deepseek-harness) | 1 | 29.9 (observed) | 25.898 | 27.482 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 116 | [HelloNicoo/deepseek-harness](https://github.com/HelloNicoo/deepseek-harness) | 1 | 29.7 (observed) | 25.898 | 27.417 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 117 | [misshehe/deepseek-harness](https://github.com/misshehe/deepseek-harness) | 1 | 29.7 (observed) | 25.898 | 27.408 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 118 | [tranvantrung95/deepseek-harness](https://github.com/tranvantrung95/deepseek-harness) | 1 | 29.3 (observed) | 25.898 | 27.251 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 119 | [zhonghui5207/deepseek-harness-desktop](https://github.com/zhonghui5207/deepseek-harness-desktop) | 1 | 29.0 (observed) | 26.010 | 27.219 | 19 | 300 | ok | 新增约 19 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“DSH Desktop — an installable desktop distribution of DeepSeek Harness for macOS, Windows, and Linux”。 |
| 120 | [lisihao/deepseek-solar-harness](https://github.com/lisihao/deepseek-solar-harness) | 0 | 38.0 (observed) | 20.000 | 27.218 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 121 | [NewMFF/deepseek-harness](https://github.com/NewMFF/deepseek-harness) | 1 | 29.1 (observed) | 25.898 | 27.181 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 122 | [zdy-ai/deepseek-harness](https://github.com/zdy-ai/deepseek-harness) | 1 | 29.0 (observed) | 25.898 | 27.157 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 123 | [oscarlius/deepseek-harness](https://github.com/oscarlius/deepseek-harness) | 1 | 28.9 (observed) | 25.898 | 27.105 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 124 | [TomYang1024/deepseek-harness](https://github.com/TomYang1024/deepseek-harness) | 1 | 28.8 (observed) | 25.898 | 27.047 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 125 | [KinomotoMio/deepseek-harness](https://github.com/KinomotoMio/deepseek-harness) | 1 | 28.7 (observed) | 25.898 | 27.021 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 126 | [linfunss/deepseek-harness](https://github.com/linfunss/deepseek-harness) | 1 | 28.4 (observed) | 25.898 | 26.909 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 127 | [dailin3/deepseek-harness](https://github.com/dailin3/deepseek-harness) | 1 | 28.2 (observed) | 25.898 | 26.822 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 128 | [biyan113/deepseek-harness](https://github.com/biyan113/deepseek-harness) | 1 | 28.1 (observed) | 25.938 | 26.820 | 3 | 55 | ok | 新增约 3 个提交并修改 55 个文件，主要涉及 CI/构建、UI/应用层、文档、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 129 | [stephenlzc/deepseek-harness](https://github.com/stephenlzc/deepseek-harness) | 0 | 37.1 (observed) | 19.986 | 26.815 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 130 | [zicowarn/deepseek-harness](https://github.com/zicowarn/deepseek-harness) | 0 | 36.6 (observed) | 20.000 | 26.635 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 131 | [xiaosenho/deepseek-harness](https://github.com/xiaosenho/deepseek-harness) | 1 | 16.3 (observed) | 33.453 | 26.598 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 132 | [zng8418/deepseek-harness](https://github.com/zng8418/deepseek-harness) | 1 | 27.6 (observed) | 25.898 | 26.593 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 133 | [markisaac/deepseek-harness](https://github.com/markisaac/deepseek-harness) | 1 | 27.5 (observed) | 25.898 | 26.553 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 134 | [iKing/deepseek-harness](https://github.com/iKing/deepseek-harness) | 1 | 27.5 (observed) | 25.898 | 26.521 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 135 | [pellera9/deepseek-harness](https://github.com/pellera9/deepseek-harness) | 1 | 27.4 (observed) | 25.898 | 26.503 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 136 | [BlackRosePetals/deepseek-harness](https://github.com/BlackRosePetals/deepseek-harness) | 1 | 27.3 (observed) | 25.898 | 26.453 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 137 | [t479842598/deepseek-harness](https://github.com/t479842598/deepseek-harness) | 1 | 26.7 (observed) | 26.006 | 26.302 | 16 | 13 | ok | 新增约 16 个提交并修改 13 个文件，主要涉及 Harness 核心能力、测试；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 138 | [imhieu/deepseek-harness](https://github.com/imhieu/deepseek-harness) | 1 | 26.7 (observed) | 25.898 | 26.235 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 139 | [Helpless5699/deepseek-harness](https://github.com/Helpless5699/deepseek-harness) | 1 | 26.7 (observed) | 25.898 | 26.213 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 140 | [Keryer/deepseek-harness](https://github.com/Keryer/deepseek-harness) | 0 | 35.4 (observed) | 19.989 | 26.170 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 141 | [melkharbili/deepseek-harness](https://github.com/melkharbili/deepseek-harness) | 1 | 26.5 (observed) | 25.898 | 26.151 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 142 | [4evour/deepseek-harness](https://github.com/4evour/deepseek-harness) | 1 | 26.5 (observed) | 25.898 | 26.125 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 143 | [SquabbyZ/deepseek-harness](https://github.com/SquabbyZ/deepseek-harness) | 0 | 34.8 (observed) | 19.990 | 25.897 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 144 | [KevinSCUTer/deepseek-harness](https://github.com/KevinSCUTer/deepseek-harness) | 1 | 25.8 (observed) | 25.898 | 25.875 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 145 | [BobcGn/deepseek-harness-app](https://github.com/BobcGn/deepseek-harness-app) | 1 | 25.7 (observed) | 25.998 | 25.871 | 14 | 31 | ok | 新增约 14 个提交并修改 31 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 146 | [QingGeLaiYe/deepseek-harness](https://github.com/QingGeLaiYe/deepseek-harness) | 1 | 25.6 (observed) | 25.898 | 25.764 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 147 | [yx54hego-cloud/deepseek-harness](https://github.com/yx54hego-cloud/deepseek-harness) | 7 | 7.0 (observed) | 38.062 | 25.643 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 148 | [WyrdWerk/deepseek-harness](https://github.com/WyrdWerk/deepseek-harness) | 1 | 25.1 (observed) | 26.020 | 25.638 | 13 | 272 | ok | 新增约 13 个提交并修改 272 个文件，主要涉及 配置、文档、CI/构建、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 149 | [deveuper/deepseek-harness](https://github.com/deveuper/deepseek-harness) | 1 | 25.0 (observed) | 25.910 | 25.558 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 150 | [yueyucaotian/deepseek-harness](https://github.com/yueyucaotian/deepseek-harness) | 1 | 24.8 (observed) | 25.898 | 25.444 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 151 | [aqiyoung/deepseek-harness](https://github.com/aqiyoung/deepseek-harness) | 0 | 33.5 (observed) | 19.999 | 25.403 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 152 | [MinerBin/deepseek-harness](https://github.com/MinerBin/deepseek-harness) | 1 | 24.5 (observed) | 25.898 | 25.342 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 153 | [18217778896/deepseek-harness](https://github.com/18217778896/deepseek-harness) | 1 | 24.2 (observed) | 25.898 | 25.230 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 154 | [leixiaochenShen/deepseek-harness](https://github.com/leixiaochenShen/deepseek-harness) | 1 | 24.0 (observed) | 25.898 | 25.144 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 155 | [liwuli/deepseek-harness-desktop](https://github.com/liwuli/deepseek-harness-desktop) | 1 | 23.9 (observed) | 25.952 | 25.118 | 2 | 28 | ok | 新增约 2 个提交并修改 28 个文件，主要涉及 CI/构建、其他文件、文档、依赖；目标线索是“DeepSeek Harness desktop”。 |
| 156 | [Yarpii/deepseek-harness](https://github.com/Yarpii/deepseek-harness) | 0 | 32.7 (observed) | 20.000 | 25.065 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 157 | [tzy168/deepseek-harness](https://github.com/tzy168/deepseek-harness) | 1 | 23.8 (observed) | 25.939 | 25.065 | 2 | 25 | ok | 新增约 2 个提交并修改 25 个文件，主要涉及 配置、文档、Harness 核心能力、测试；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 158 | [nostalgia296/deepseek-harness-termux](https://github.com/nostalgia296/deepseek-harness-termux) | 1 | 23.6 (observed) | 25.959 | 25.013 | 2 | 33 | ok | 新增约 2 个提交并修改 33 个文件，主要涉及 配置、文档、测试、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 159 | [zkh11123/deepseek-harness](https://github.com/zkh11123/deepseek-harness) | 1 | 23.3 (observed) | 25.898 | 24.860 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 160 | [lihaidog/deepseek-harness](https://github.com/lihaidog/deepseek-harness) | 1 | 23.1 (observed) | 25.898 | 24.760 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 161 | [w74srm/deepseek-harness](https://github.com/w74srm/deepseek-harness) | 1 | 22.9 (observed) | 25.898 | 24.712 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 162 | [0verL1nk/deepseek-harness](https://github.com/0verL1nk/deepseek-harness) | 0 | 31.6 (observed) | 19.968 | 24.633 | 29 | 59 | ok | 新增约 29 个提交并修改 59 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 163 | [xiaofeng930415/deepseek-harness](https://github.com/xiaofeng930415/deepseek-harness) | 1 | 22.7 (observed) | 25.898 | 24.627 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 164 | [Constantine3/table-forge](https://github.com/Constantine3/table-forge) | 0 | 31.4 (observed) | 19.985 | 24.566 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“一个通用的、LLM-native 的多人游戏引擎”，修改面待下一轮 compare/README 深扫。 |
| 165 | [HHHHH-GIT/Deepseek-HPD-Harness](https://github.com/HHHHH-GIT/Deepseek-HPD-Harness) | 1 | 22.4 (observed) | 25.982 | 24.555 | 2 | 133 | ok | 新增约 2 个提交并修改 133 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek HPD Harness: Everything is a Plugin. A more powerful Harness with HPD architecture”。 |
| 166 | [longman888/deepseek-harness](https://github.com/longman888/deepseek-harness) | 1 | 22.5 (observed) | 25.898 | 24.537 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 167 | [NeverOvO/deepseek-harness](https://github.com/NeverOvO/deepseek-harness) | 0 | 31.1 (observed) | 19.999 | 24.448 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 168 | [duliangkuan/deepseek-harness](https://github.com/duliangkuan/deepseek-harness) | 1 | 22.2 (observed) | 25.898 | 24.417 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 169 | [MixGeeker/deepseek-harness](https://github.com/MixGeeker/deepseek-harness) | 1 | 22.1 (observed) | 25.898 | 24.393 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 170 | [Beam-wi/deepseek-harness](https://github.com/Beam-wi/deepseek-harness) | 1 | 22.0 (observed) | 25.898 | 24.352 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 171 | [Octo-o-o-o/deepseek-harness-desktop](https://github.com/Octo-o-o-o/deepseek-harness-desktop) | 1 | 21.8 (observed) | 26.020 | 24.317 | 78 | 286 | ok | 新增约 78 个提交并修改 286 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“非官方桌面版 · Unofficial desktop shell for DeepSeek Harness — double-click, no Node, no terminal. Signed & notarized on macOS. Tauri shell, official MIT core untouched”。 |
| 172 | [Linyiwei895178/deepseek-harness](https://github.com/Linyiwei895178/deepseek-harness) | 1 | 21.7 (observed) | 25.898 | 24.214 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 173 | [porarrirr/deepseek-harness-japanese](https://github.com/porarrirr/deepseek-harness-japanese) | 0 | 19.3 (observed) | 27.387 | 24.162 | 2 | 88 | ok | 新增约 2 个提交并修改 88 个文件，主要涉及 配置、文档、UI/应用层、依赖；目标线索是“DeepSeek Harness”。 |
| 174 | [HTree-ZX/deepseek-harness](https://github.com/HTree-ZX/deepseek-harness) | 1 | 21.5 (observed) | 25.898 | 24.125 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 175 | [suiyuebaobao/deepseek-harness-gui](https://github.com/suiyuebaobao/deepseek-harness-gui) | 2 | 16.1 (observed) | 29.464 | 24.102 | 2 | 52 | ok | 新增约 2 个提交并修改 52 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“Windows desktop fork of DeepSeek Harness, packaged with Tauri while preserving the full Web profile and plugin runtime”。 |
| 176 | [GTC2080/deepseek-harness](https://github.com/GTC2080/deepseek-harness) | 1 | 21.2 (observed) | 25.985 | 24.059 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness 桌面端：基于 Tauri，支持 macOS 与 Windows；源码位于 desktop 分支”。 |
| 177 | [wingthedream/deepseek-harness](https://github.com/wingthedream/deepseek-harness) | 1 | 21.2 (observed) | 25.898 | 24.005 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 178 | [shr123456/deepseek-harness](https://github.com/shr123456/deepseek-harness) | 1 | 20.9 (observed) | 25.898 | 23.893 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 179 | [BILYHO/deepseek-harness](https://github.com/BILYHO/deepseek-harness) | 0 | 29.7 (observed) | 19.987 | 23.854 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 180 | [007M7/deepseek-harness](https://github.com/007M7/deepseek-harness) | 1 | 20.4 (observed) | 25.898 | 23.706 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“我永远喜欢deepseek！！！”。 |
| 181 | [flaqai/open-deepseek-harness-desktop](https://github.com/flaqai/open-deepseek-harness-desktop) | 1 | 20.4 (observed) | 25.898 | 23.701 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“Open Source Desktop for DeepSeek Harness. DeepSeek Harness: Everything is a Plugin”。 |
| 182 | [yyy1mu/deepseek-harness](https://github.com/yyy1mu/deepseek-harness) | 0 | 29.3 (observed) | 19.994 | 23.700 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 183 | [danlinyu/deepseek-harness](https://github.com/danlinyu/deepseek-harness) | 0 | 29.2 (observed) | 19.994 | 23.667 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 184 | [Captain-Dodger/deepseek-harness](https://github.com/Captain-Dodger/deepseek-harness) | 0 | 17.9 (observed) | 27.364 | 23.570 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 185 | [HarryMai/deepseek-harness](https://github.com/HarryMai/deepseek-harness) | 0 | 28.9 (observed) | 19.984 | 23.564 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 186 | [nathan5580/deepseek-harness](https://github.com/nathan5580/deepseek-harness) | 0 | 28.9 (observed) | 19.999 | 23.550 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 187 | [276397082/deepseek-harness](https://github.com/276397082/deepseek-harness) | 0 | 20.7 (observed) | 25.323 | 23.483 | 1 | 3 | ok | 新增约 1 个提交并修改 3 个文件，主要涉及 其他文件、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 188 | [xbzhangyq/deepseek-harness](https://github.com/xbzhangyq/deepseek-harness) | 1 | 19.7 (observed) | 25.898 | 23.419 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 189 | [x1095907352/deepseek-harness](https://github.com/x1095907352/deepseek-harness) | 1 | 19.5 (observed) | 25.898 | 23.352 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 190 | [Solizardking/deepseek-harness](https://github.com/Solizardking/deepseek-harness) | 0 | 28.3 (observed) | 19.994 | 23.311 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 191 | [Zguigo00/deepseek-harness](https://github.com/Zguigo00/deepseek-harness) | 1 | 19.2 (observed) | 25.898 | 23.219 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 192 | [MrGXxx/deepseek-harness](https://github.com/MrGXxx/deepseek-harness) | 1 | 19.2 (observed) | 25.898 | 23.216 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 193 | [Constantine1916/deepseek-harness](https://github.com/Constantine1916/deepseek-harness) | 0 | 28.0 (observed) | 19.986 | 23.178 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 194 | [zhanggoodbao/deepseek-harness](https://github.com/zhanggoodbao/deepseek-harness) | 1 | 18.7 (observed) | 25.898 | 23.031 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 195 | [tinhocdaimo2015/deepseek-harness](https://github.com/tinhocdaimo2015/deepseek-harness) | 1 | 18.6 (observed) | 25.898 | 22.971 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 196 | [peter13990/deepseek-harness](https://github.com/peter13990/deepseek-harness) | 1 | 18.6 (observed) | 25.898 | 22.963 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 197 | [WuJunNan-fjy/deepseek-harness](https://github.com/WuJunNan-fjy/deepseek-harness) | 1 | 18.5 (observed) | 25.898 | 22.947 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 198 | [CatchCatOoO/deepseek-harness](https://github.com/CatchCatOoO/deepseek-harness) | 1 | 18.4 (observed) | 25.908 | 22.921 | 4 | 300 | ok | 新增约 4 个提交并修改 300 个文件，主要涉及 文档、配置、agent/skill 能力；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 199 | [Lostsoul-namespace/deepseek-harness](https://github.com/Lostsoul-namespace/deepseek-harness) | 1 | 18.4 (observed) | 25.898 | 22.900 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 200 | [2373370715/deepseek-harness](https://github.com/2373370715/deepseek-harness) | 0 | 20.4 (observed) | 24.552 | 22.894 | 1 | 2 | ok | 新增约 1 个提交并修改 2 个文件，主要涉及 文档、Harness 核心能力；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |

> Showing the first 200 rows here; `11,223` rows are preserved in `index/forks.jsonl` and `docs/data/forks.json`.

## Interpretation

The collector records every public Fork returned by the paginated endpoint. Deep compare, recent commits, and README metadata are rotated by a per-run budget because GitHub rate limits make an unbounded daily deep audit impractical for a network of this size. Use `python3 scripts/collect_forks.py --deep-scan-all` only when the available token and request budget are sufficient.
