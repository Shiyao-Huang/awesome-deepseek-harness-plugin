# DeepSeek Harness Fork Network

- Dataset version: `v20260816T110748Z`
- Public Fork records: **12,302**
- Ranking filter: **0+ stars**; observed Fork identities: **12,302**; filtered out of ranking: **0**.
- Ever deep-scanned: **691 / 12,302** (5.62%); pending: **11,611**; conservative backfill ETA: **73 daily runs**.
- Deep-scanned successfully in the current projection: **691**; compare responses retained: **691**
- Fork rows with public owner reputation observed: **499**; the current ranking pool applies a configurable minimum-Star filter.
- Scope: public Forks returned by GitHub REST API pagination for `deepseek-ai/deepseek-harness`.
- Raw evidence is collected under `data/raw/forks/`; the [latest compressed SQLite snapshot](https://github.com/Shiyao-Huang/awesome-deepseek-harness-plugin/releases/download/dataset-latest/aggregator-full.sqlite3.zst) includes the fork tables and raw JSON payloads. Unpack it with `zstd -d aggregator-full.sqlite3.zst -o aggregator-full.sqlite3`.
- Searchable browser: `docs/forks.html`; compact catalog: `docs/data/fork-catalog.json`; complete machine-readable ranking: `index/forks.jsonl`.
- `overall score = repository influence 60% + public-account reputation 40%` when the profile is observed; missing profile signals are not treated as zero. This is a public-signal ordering aid, not a quality, safety, integrity, or endorsement claim.

## GitHub star order

| Star rank | Fork | Stars | Composite rank | Audit | Evidence |
| ---: | --- | ---: | ---: | --- | --- |
| 1 | [salathleizhang/deepseek-harness-desktop](https://github.com/salathleizhang/deepseek-harness-desktop) | 103 | 1 | audited | 新增约 42 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“Native desktop app for DeepSeek Harness — an Electron shell that runs the harness locally and hosts the official Web GUI unchanged”。 |
| 2 | [Sakana-yuyu/deepseek-harness-desktop](https://github.com/Sakana-yuyu/deepseek-harness-desktop) | 26 | 6 | audited | 新增约 14 个提交并修改 81 个文件，主要涉及 配置、文档、CI/构建、UI/应用层；目标线索是“Rust构建的客户端，体积更小，更方便，Mac，win，linux已完成”。 |
| 3 | [G36maid/deepseek-harness](https://github.com/G36maid/deepseek-harness) | 12 | 7 | audited | 新增约 19 个提交并修改 300 个文件，主要涉及 配置、文档；目标线索是“DeepSeek Harness 繁體中文版 (zh-TW) — Everything is a Plugin”。 |
| 4 | [rpmalouin/deepseek-harness](https://github.com/rpmalouin/deepseek-harness) | 11 | 17 | audited | 新增约 4 个提交并修改 31 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 5 | [Skyearn/deepseek-harness-app](https://github.com/Skyearn/deepseek-harness-app) | 11 | 18 | audited | 新增约 24 个提交并修改 31 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness Desktop”。 |
| 6 | [Ajwyunsx/deepseek-harness-mobile](https://github.com/Ajwyunsx/deepseek-harness-mobile) | 10 | 9 | audited | 新增约 10 个提交并修改 40 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 7 | [yx54hego-cloud/deepseek-harness](https://github.com/yx54hego-cloud/deepseek-harness) | 9 | 167 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 8 | [happylin0x29a/deepseek-harness-desktop](https://github.com/happylin0x29a/deepseek-harness-desktop) | 4 | 33 | audited | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness desktop base on tauri”。 |
| 9 | [luolangaga/deepseek-harness](https://github.com/luolangaga/deepseek-harness) | 4 | 49 | audited | 新增约 11 个提交并修改 54 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 10 | [sdkwork-ai/deepseek-harness-desktop](https://github.com/sdkwork-ai/deepseek-harness-desktop) | 4 | 148 | audited | 新增约 48 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 11 | [shijiejintoulwh/deepseek-harness](https://github.com/shijiejintoulwh/deepseek-harness) | 4 | 105 | audited | 新增约 1 个提交并修改 3 个文件，主要涉及 CI/构建、测试；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 12 | [jasonkneen/deepseek-harness-plus](https://github.com/jasonkneen/deepseek-harness-plus) | 3 | 2 | audited | 新增约 2 个提交并修改 103 个文件，主要涉及 配置、文档、依赖、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 13 | [puppywang/deepseek-harness](https://github.com/puppywang/deepseek-harness) | 3 | 29 | audited | 新增约 10 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 14 | [yazzang-homelab/deepseek-harness](https://github.com/yazzang-homelab/deepseek-harness) | 2 | 136 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 15 | [BobcGn/deepseek-harness-app](https://github.com/BobcGn/deepseek-harness-app) | 2 | 35 | audited | 新增约 16 个提交并修改 37 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 16 | [FSMargoo/deepseek-harness](https://github.com/FSMargoo/deepseek-harness) | 2 | 45 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 17 | [huiliyi37/deepseek-harness](https://github.com/huiliyi37/deepseek-harness) | 2 | 145 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 18 | [Kiowx/deepseek-harness](https://github.com/Kiowx/deepseek-harness) | 2 | 149 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 19 | [MarceloClaro/deepseek-harness](https://github.com/MarceloClaro/deepseek-harness) | 2 | 34 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 20 | [stophobia/deepseek-harness](https://github.com/stophobia/deepseek-harness) | 2 | 8 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 21 | [suiyuebaobao/deepseek-harness-gui](https://github.com/suiyuebaobao/deepseek-harness-gui) | 2 | 217 | audited | 新增约 2 个提交并修改 52 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“Windows desktop fork of DeepSeek Harness, packaged with Tauri while preserving the full Web profile and plugin runtime”。 |
| 22 | [Yihong89/deepseek-harness](https://github.com/Yihong89/deepseek-harness) | 2 | 79 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 23 | [srwang0506/deepseek-harness](https://github.com/srwang0506/deepseek-harness) | 1 | 114 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 24 | [xiaosenho/deepseek-harness](https://github.com/xiaosenho/deepseek-harness) | 1 | 184 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 25 | [007M7/deepseek-harness](https://github.com/007M7/deepseek-harness) | 1 | 223 | audited | 未观察到相对 upstream 的文件修改；目标线索是“我永远喜欢deepseek！！！”。 |
| 26 | [123bawanglong/deepseek-harness](https://github.com/123bawanglong/deepseek-harness) | 1 | 12216 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 27 | [123prompt/deepseek-harness](https://github.com/123prompt/deepseek-harness) | 1 | 296 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 28 | [1486482143/deepseek-harness](https://github.com/1486482143/deepseek-harness) | 1 | 304 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 29 | [18217778896/deepseek-harness](https://github.com/18217778896/deepseek-harness) | 1 | 194 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 30 | [2404589803/deepseek-harness](https://github.com/2404589803/deepseek-harness) | 1 | 70 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 31 | [485524097/deepseek-harness](https://github.com/485524097/deepseek-harness) | 1 | 433 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 32 | [4evour/deepseek-harness](https://github.com/4evour/deepseek-harness) | 1 | 183 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 33 | [A1pha3/deepseek-harness](https://github.com/A1pha3/deepseek-harness) | 1 | 119 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 34 | [a907781273-a11y/deepseek-harness](https://github.com/a907781273-a11y/deepseek-harness) | 1 | 12221 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 35 | [achristofaro/deepseek-harness](https://github.com/achristofaro/deepseek-harness) | 1 | 75 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 36 | [AI-1-TOP/deepseek-harness](https://github.com/AI-1-TOP/deepseek-harness) | 1 | 12261 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 37 | [aimierbear/TinyWhale](https://github.com/aimierbear/TinyWhale) | 1 | 269 | audited | 新增约 18 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、CI/构建；目标线索是“TinyWhale — desktop-oriented MIT fork of DeepSeek Harness, with an Electron shell in desktop/”。 |
| 38 | [alexdeweb/deepseek-harness](https://github.com/alexdeweb/deepseek-harness) | 1 | 109 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 39 | [alexdolbun/deepseek-harness](https://github.com/alexdolbun/deepseek-harness) | 1 | 4 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 40 | [Alsdara/deepseek-harness](https://github.com/Alsdara/deepseek-harness) | 1 | 12206 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 41 | [Anyaoha/deepseek-harness](https://github.com/Anyaoha/deepseek-harness) | 1 | 68 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 42 | [Ashveil1/deepseek-harness-ares](https://github.com/Ashveil1/deepseek-harness-ares) | 1 | 279 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek harness for pentesting”。 |
| 43 | [athif23/deepseek-harness](https://github.com/athif23/deepseek-harness) | 1 | 44 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 44 | [ayushare/deepseek-harness](https://github.com/ayushare/deepseek-harness) | 1 | 12162 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 45 | [b3nk-x1/deepseek-harness](https://github.com/b3nk-x1/deepseek-harness) | 1 | 12230 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 46 | [badestgod/deepseek-harness](https://github.com/badestgod/deepseek-harness) | 1 | 120 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 47 | [Beam-wi/deepseek-harness](https://github.com/Beam-wi/deepseek-harness) | 1 | 211 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 48 | [beiluo0z0/deepseek-harness](https://github.com/beiluo0z0/deepseek-harness) | 1 | 12182 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 49 | [ben-vargas/ai-deepseek-harness](https://github.com/ben-vargas/ai-deepseek-harness) | 1 | 25 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 50 | [biyan113/deepseek-harness](https://github.com/biyan113/deepseek-harness) | 1 | 166 | audited | 新增约 3 个提交并修改 55 个文件，主要涉及 CI/构建、UI/应用层、文档、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 51 | [BlackRosePetals/deepseek-harness](https://github.com/BlackRosePetals/deepseek-harness) | 1 | 176 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 52 | [bojieli/deepseek-harness](https://github.com/bojieli/deepseek-harness) | 1 | 3 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 53 | [boktoday/deepseek-harness](https://github.com/boktoday/deepseek-harness) | 1 | 66 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 54 | [brandy2015/deepseek-harness](https://github.com/brandy2015/deepseek-harness) | 1 | 37 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 55 | [BurtonQin/deepseek-harness](https://github.com/BurtonQin/deepseek-harness) | 1 | 31 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 56 | [CatchCatOoO/deepseek-harness](https://github.com/CatchCatOoO/deepseek-harness) | 1 | 240 | audited | 新增约 4 个提交并修改 300 个文件，主要涉及 文档、配置、agent/skill 能力；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 57 | [cFqr-lang/deepseek-harness](https://github.com/cFqr-lang/deepseek-harness) | 1 | 151 | audited | 新增约 10 个提交并修改 62 个文件，主要涉及 UI/应用层、文档、Harness 核心能力、配置；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 58 | [CH-HGod/deepseek-harness](https://github.com/CH-HGod/deepseek-harness) | 1 | 12188 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 59 | [chiekoschamburek-dev/deepseek-harness](https://github.com/chiekoschamburek-dev/deepseek-harness) | 1 | 12210 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 60 | [China-MY/deepseek-harness](https://github.com/China-MY/deepseek-harness) | 1 | 128 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 61 | [chyl00/deepseek-harness](https://github.com/chyl00/deepseek-harness) | 1 | 264 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 62 | [chzxu/deepseek-harness](https://github.com/chzxu/deepseek-harness) | 1 | 12186 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 63 | [cioerp/deepseek-harness](https://github.com/cioerp/deepseek-harness) | 1 | 12255 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 64 | [codelife2020/deepseek-harness](https://github.com/codelife2020/deepseek-harness) | 1 | 253 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 65 | [coder-v0/deepseek-harness](https://github.com/coder-v0/deepseek-harness) | 1 | 111 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 66 | [coolman1984/deepseek-harness](https://github.com/coolman1984/deepseek-harness) | 1 | 186 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 67 | [cq2021-coder/deepseek-harness-desktop](https://github.com/cq2021-coder/deepseek-harness-desktop) | 1 | 124 | audited | 未观察到相对 upstream 的文件修改；目标线索是“使用 tauri 为 DeepSeek Harness 生态打造的现代化桌面端应用”。 |
| 68 | [criapa/deepseek-harness](https://github.com/criapa/deepseek-harness) | 1 | 54 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 69 | [Cute-chen/deepseek-harness-app](https://github.com/Cute-chen/deepseek-harness-app) | 1 | 244 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 70 | [Cyenoch/deepseek-harness](https://github.com/Cyenoch/deepseek-harness) | 1 | 10 | audited | 新增约 14 个提交并修改 300 个文件，主要涉及 配置、文档、agent/skill 能力、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 71 | [cyh7777/deepseek-harness](https://github.com/cyh7777/deepseek-harness) | 1 | 12192 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 72 | [dailin3/deepseek-harness](https://github.com/dailin3/deepseek-harness) | 1 | 165 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 73 | [DailyR/deepseek-harness](https://github.com/DailyR/deepseek-harness) | 1 | 47 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 74 | [DarrenHoo-10/oh-my-dsh](https://github.com/DarrenHoo-10/oh-my-dsh) | 1 | 41 | audited | 新增约 8 个提交并修改 249 个文件，主要涉及 配置、文档、其他文件、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 75 | [ddd666j/deepseek-harness](https://github.com/ddd666j/deepseek-harness) | 1 | 12240 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 76 | [DeepThinkingZhouLiu/Deepseek-Harness-RSI](https://github.com/DeepThinkingZhouLiu/Deepseek-Harness-RSI) | 1 | 91 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 77 | [deveuper/deepseek-harness](https://github.com/deveuper/deepseek-harness) | 1 | 190 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 78 | [devin2255/deepseek-harness-desktop](https://github.com/devin2255/deepseek-harness-desktop) | 1 | 112 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 79 | [DogeJian/deepseek-harness](https://github.com/DogeJian/deepseek-harness) | 1 | 97 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 80 | [donstang/deepseek-harness](https://github.com/donstang/deepseek-harness) | 1 | 50 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 81 | [dorucioclea/deepseek-harness](https://github.com/dorucioclea/deepseek-harness) | 1 | 14 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 82 | [drscrewdriver/deepseek-harness](https://github.com/drscrewdriver/deepseek-harness) | 1 | 90 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 83 | [duliangkuan/deepseek-harness](https://github.com/duliangkuan/deepseek-harness) | 1 | 209 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 84 | [EdwardXIE6666/deepseek-harness](https://github.com/EdwardXIE6666/deepseek-harness) | 1 | 276 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 85 | [enbideren/deepseek-harness](https://github.com/enbideren/deepseek-harness) | 1 | 98 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 86 | [equable66/deepseek-harness](https://github.com/equable66/deepseek-harness) | 1 | 1262 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 87 | [Erichy777/deepseek-harness](https://github.com/Erichy777/deepseek-harness) | 1 | 261 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 88 | [Ericsongyl/deepseek-harness](https://github.com/Ericsongyl/deepseek-harness) | 1 | 39 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 89 | [ermao009/deepseek-harness](https://github.com/ermao009/deepseek-harness) | 1 | 318 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 90 | [exposir/deepseek-harness](https://github.com/exposir/deepseek-harness) | 1 | 42 | audited | 新增约 9 个提交并修改 13 个文件，主要涉及 文档、Harness 核心能力、测试；目标线索是“DeepSeek Harness”。 |
| 91 | [FadingLight9291117/deepseek-harness-desktop](https://github.com/FadingLight9291117/deepseek-harness-desktop) | 1 | 15 | audited | 新增约 21 个提交并修改 169 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 92 | [fage45029704-lgtm/deepseek-harness](https://github.com/fage45029704-lgtm/deepseek-harness) | 1 | 12218 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 93 | [faguangdeyueliang/deepseek-harness](https://github.com/faguangdeyueliang/deepseek-harness) | 1 | 282 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 94 | [fake111594/deepseek-harness](https://github.com/fake111594/deepseek-harness) | 1 | 12241 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 95 | [fendouai/deepseek-harness-desktop](https://github.com/fendouai/deepseek-harness-desktop) | 1 | 13 | audited | 新增约 10 个提交并修改 123 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 96 | [fisher158163/deepseek-harness](https://github.com/fisher158163/deepseek-harness) | 1 | 36 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 97 | [flaqai/open-deepseek-harness-desktop](https://github.com/flaqai/open-deepseek-harness-desktop) | 1 | 225 | audited | 未观察到相对 upstream 的文件修改；目标线索是“Open Source Desktop for DeepSeek Harness. DeepSeek Harness: Everything is a Plugin”。 |
| 98 | [flowersea302/deepseek-harness](https://github.com/flowersea302/deepseek-harness) | 1 | 331 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 99 | [FlyingSama/deepseek-harness](https://github.com/FlyingSama/deepseek-harness) | 1 | 249 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 100 | [frankpeyer33-glitch/deepseek-harness](https://github.com/frankpeyer33-glitch/deepseek-harness) | 1 | 12252 | audited | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |

## Modification categories

| Category | Changed paths |
| --- | ---: |
| docs | 2,113 |
| harness-core | 1,268 |
| dependencies | 1,047 |
| ui-and-apps | 986 |
| configuration | 920 |
| tests | 571 |
| other | 243 |
| tools-and-scripts | 66 |
| ci-and-build | 62 |
| agents-and-skills | 48 |

## Influence order

| Rank | Fork | Stars | Owner reputation | Repo influence | Overall | Ahead | Changed files | Deep status | One-sentence evidence |
| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | --- | --- |
| 1 | [salathleizhang/deepseek-harness-desktop](https://github.com/salathleizhang/deepseek-harness-desktop) | 103 | 36.0 (observed) | 74.958 | 59.375 | 42 | 300 | ok | 新增约 42 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“Native desktop app for DeepSeek Harness — an Electron shell that runs the harness locally and hosts the official Web GUI unchanged”。 |
| 2 | [jasonkneen/deepseek-harness-plus](https://github.com/jasonkneen/deepseek-harness-plus) | 3 | 77.0 (observed) | 31.906 | 49.961 | 2 | 103 | ok | 新增约 2 个提交并修改 103 个文件，主要涉及 配置、文档、依赖、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 3 | [bojieli/deepseek-harness](https://github.com/bojieli/deepseek-harness) | 1 | 81.4 (observed) | 25.810 | 48.045 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 4 | [alexdolbun/deepseek-harness](https://github.com/alexdolbun/deepseek-harness) | 1 | 80.0 (observed) | 25.810 | 47.502 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 5 | [zchuhui/deepseek-harness](https://github.com/zchuhui/deepseek-harness) | 1 | 48.7 (observed) | 46.345 | 47.302 | 10 | 300 | ok | 新增约 10 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 6 | [Sakana-yuyu/deepseek-harness-desktop](https://github.com/Sakana-yuyu/deepseek-harness-desktop) | 26 | 35.5 (observed) | 54.750 | 47.055 | 14 | 81 | ok | 新增约 14 个提交并修改 81 个文件，主要涉及 配置、文档、CI/构建、UI/应用层；目标线索是“Rust构建的客户端，体积更小，更方便，Mac，win，linux已完成”。 |
| 7 | [G36maid/deepseek-harness](https://github.com/G36maid/deepseek-harness) | 12 | 54.4 (observed) | 42.033 | 46.997 | 19 | 300 | ok | 新增约 19 个提交并修改 300 个文件，主要涉及 配置、文档；目标线索是“DeepSeek Harness 繁體中文版 (zh-TW) — Everything is a Plugin”。 |
| 8 | [stophobia/deepseek-harness](https://github.com/stophobia/deepseek-harness) | 2 | 70.7 (observed) | 29.302 | 45.845 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 9 | [Ajwyunsx/deepseek-harness-mobile](https://github.com/Ajwyunsx/deepseek-harness-mobile) | 10 | 36.6 (observed) | 50.866 | 45.152 | 10 | 40 | ok | 新增约 10 个提交并修改 40 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 10 | [Cyenoch/deepseek-harness](https://github.com/Cyenoch/deepseek-harness) | 1 | 41.4 (observed) | 47.060 | 44.796 | 14 | 300 | ok | 新增约 14 个提交并修改 300 个文件，主要涉及 配置、文档、agent/skill 能力、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 11 | [tjweir/deepseek-harness](https://github.com/tjweir/deepseek-harness) | 1 | 72.7 (observed) | 25.810 | 44.580 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 12 | [skywalk163/deepseek-harness](https://github.com/skywalk163/deepseek-harness) | 1 | 49.9 (observed) | 41.018 | 44.566 | 13 | 31 | ok | 新增约 13 个提交并修改 31 个文件，主要涉及 其他文件、文档、UI/应用层、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 13 | [fendouai/deepseek-harness-desktop](https://github.com/fendouai/deepseek-harness-desktop) | 1 | 72.1 (observed) | 25.912 | 44.382 | 10 | 123 | ok | 新增约 10 个提交并修改 123 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 14 | [dorucioclea/deepseek-harness](https://github.com/dorucioclea/deepseek-harness) | 1 | 71.8 (observed) | 25.810 | 44.189 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 15 | [FadingLight9291117/deepseek-harness-desktop](https://github.com/FadingLight9291117/deepseek-harness-desktop) | 1 | 40.3 (observed) | 46.421 | 43.991 | 21 | 169 | ok | 新增约 21 个提交并修改 169 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 16 | [qiayue/deepseek-harness](https://github.com/qiayue/deepseek-harness) | 1 | 68.6 (observed) | 25.810 | 42.921 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 17 | [rpmalouin/deepseek-harness](https://github.com/rpmalouin/deepseek-harness) | 11 | 34.9 (observed) | 47.782 | 42.630 | 4 | 31 | ok | 新增约 4 个提交并修改 31 个文件，主要涉及 文档、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 18 | [Skyearn/deepseek-harness-app](https://github.com/Skyearn/deepseek-harness-app) | 11 | 34.3 (observed) | 47.789 | 42.403 | 24 | 31 | ok | 新增约 24 个提交并修改 31 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness Desktop”。 |
| 19 | [lixun910/deepseek-harness](https://github.com/lixun910/deepseek-harness) | 1 | 64.0 (observed) | 25.810 | 41.077 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 20 | [chenshuai2144/deepseek-harness](https://github.com/chenshuai2144/deepseek-harness) | 0 | 72.7 (observed) | 19.995 | 41.065 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 21 | [v2hoping/deepseek-harness-desktop](https://github.com/v2hoping/deepseek-harness-desktop) | 1 | 36.4 (observed) | 44.012 | 40.962 | 19 | 73 | ok | 新增约 19 个提交并修改 73 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin. Supports desktop installation and DeepSeek account login”。 |
| 22 | [zhonghui5207/deepseek-harness-desktop](https://github.com/zhonghui5207/deepseek-harness-desktop) | 1 | 29.0 (observed) | 47.696 | 40.231 | 19 | 300 | ok | 新增约 19 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“DSH Desktop — an installable desktop distribution of DeepSeek Harness for macOS, Windows, and Linux”。 |
| 23 | [Sailfishc/deepseek-harness](https://github.com/Sailfishc/deepseek-harness) | 1 | 61.2 (observed) | 25.810 | 39.972 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 24 | [molodiuc/deepseek-harness](https://github.com/molodiuc/deepseek-harness) | 1 | 60.6 (observed) | 25.810 | 39.730 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 25 | [ben-vargas/ai-deepseek-harness](https://github.com/ben-vargas/ai-deepseek-harness) | 1 | 59.6 (observed) | 25.810 | 39.338 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 26 | [Octo-o-o-o/deepseek-harness-desktop](https://github.com/Octo-o-o-o/deepseek-harness-desktop) | 1 | 21.8 (observed) | 50.956 | 39.279 | 84 | 300 | ok | 新增约 84 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、依赖；目标线索是“非官方桌面版 · Unofficial desktop shell for DeepSeek Harness — double-click, no Node, no terminal. Signed & notarized on macOS. Tauri shell, official MIT core untouched”。 |
| 27 | [TKaxv-7S/deepseek-harness](https://github.com/TKaxv-7S/deepseek-harness) | 1 | 59.4 (observed) | 25.810 | 39.233 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 28 | [179309463/deepseek-harness](https://github.com/179309463/deepseek-harness) | 0 | 39.5 (observed) | 38.858 | 39.128 | 18 | 104 | ok | 新增约 18 个提交并修改 104 个文件，主要涉及 文档、agent/skill 能力、其他文件、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 29 | [puppywang/deepseek-harness](https://github.com/puppywang/deepseek-harness) | 3 | 49.7 (observed) | 31.853 | 39.007 | 10 | 300 | ok | 新增约 10 个提交并修改 300 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 30 | [rferrari/deepseek-harness](https://github.com/rferrari/deepseek-harness) | 1 | 58.8 (observed) | 25.810 | 39.001 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 31 | [BurtonQin/deepseek-harness](https://github.com/BurtonQin/deepseek-harness) | 1 | 58.2 (observed) | 25.810 | 38.773 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 32 | [luoxunhao/deepseek-harness](https://github.com/luoxunhao/deepseek-harness) | 1 | 34.0 (observed) | 41.121 | 38.265 | 11 | 37 | ok | 新增约 11 个提交并修改 37 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 33 | [happylin0x29a/deepseek-harness-desktop](https://github.com/happylin0x29a/deepseek-harness-desktop) | 4 | 34.6 (observed) | 40.201 | 37.977 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness desktop base on tauri”。 |
| 34 | [MarceloClaro/deepseek-harness](https://github.com/MarceloClaro/deepseek-harness) | 2 | 50.6 (observed) | 29.302 | 37.813 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 35 | [BobcGn/deepseek-harness-app](https://github.com/BobcGn/deepseek-harness-app) | 2 | 25.7 (observed) | 45.396 | 37.510 | 16 | 37 | ok | 新增约 16 个提交并修改 37 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 36 | [fisher158163/deepseek-harness](https://github.com/fisher158163/deepseek-harness) | 1 | 55.0 (observed) | 25.810 | 37.466 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 37 | [brandy2015/deepseek-harness](https://github.com/brandy2015/deepseek-harness) | 1 | 54.8 (observed) | 25.810 | 37.403 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 38 | [risyasin/deepseek-harness](https://github.com/risyasin/deepseek-harness) | 0 | 63.5 (observed) | 19.970 | 37.387 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 39 | [Ericsongyl/deepseek-harness](https://github.com/Ericsongyl/deepseek-harness) | 1 | 54.5 (observed) | 25.810 | 37.279 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 40 | [manuelapetsi/deepseek-harness](https://github.com/manuelapetsi/deepseek-harness) | 1 | 54.3 (observed) | 25.810 | 37.195 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 41 | [DarrenHoo-10/oh-my-dsh](https://github.com/DarrenHoo-10/oh-my-dsh) | 1 | 24.0 (observed) | 45.415 | 36.864 | 8 | 249 | ok | 新增约 8 个提交并修改 249 个文件，主要涉及 配置、文档、其他文件、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 42 | [exposir/deepseek-harness](https://github.com/exposir/deepseek-harness) | 1 | 52.3 (observed) | 25.853 | 36.425 | 9 | 13 | ok | 新增约 9 个提交并修改 13 个文件，主要涉及 文档、Harness 核心能力、测试；目标线索是“DeepSeek Harness”。 |
| 43 | [0verL1nk/deepseek-harness](https://github.com/0verL1nk/deepseek-harness) | 0 | 31.6 (observed) | 39.354 | 36.265 | 39 | 66 | ok | 新增约 39 个提交并修改 66 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 44 | [athif23/deepseek-harness](https://github.com/athif23/deepseek-harness) | 1 | 51.7 (observed) | 25.810 | 36.156 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 45 | [FSMargoo/deepseek-harness](https://github.com/FSMargoo/deepseek-harness) | 2 | 46.1 (observed) | 29.301 | 36.029 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 46 | [winkyao/deepseek-harness](https://github.com/winkyao/deepseek-harness) | 0 | 58.9 (observed) | 20.000 | 35.571 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 47 | [DailyR/deepseek-harness](https://github.com/DailyR/deepseek-harness) | 1 | 48.7 (observed) | 25.810 | 34.985 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 48 | [HHHHH-GIT/Deepseek-HPD-Harness](https://github.com/HHHHH-GIT/Deepseek-HPD-Harness) | 1 | 22.4 (observed) | 43.117 | 34.837 | 3 | 208 | ok | 新增约 3 个提交并修改 208 个文件，主要涉及 配置、文档、agent/skill 能力、依赖；目标线索是“DeepSeek HPD Harness: Everything is a Plugin. A more powerful Harness with HPD architecture”。 |
| 49 | [luolangaga/deepseek-harness](https://github.com/luolangaga/deepseek-harness) | 4 | 36.4 (observed) | 33.746 | 34.797 | 11 | 54 | ok | 新增约 11 个提交并修改 54 个文件，主要涉及 配置、文档、CI/构建、其他文件；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 50 | [donstang/deepseek-harness](https://github.com/donstang/deepseek-harness) | 1 | 48.0 (observed) | 25.810 | 34.693 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 51 | [LCYLYM/deepseek-harness](https://github.com/LCYLYM/deepseek-harness) | 1 | 47.7 (observed) | 25.809 | 34.549 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 52 | [Razor87/deepseek-harness](https://github.com/Razor87/deepseek-harness) | 1 | 47.6 (observed) | 25.810 | 34.546 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 53 | [lkngin/deepseek-harness](https://github.com/lkngin/deepseek-harness) | 1 | 47.5 (observed) | 25.810 | 34.468 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 54 | [criapa/deepseek-harness](https://github.com/criapa/deepseek-harness) | 1 | 47.3 (observed) | 25.810 | 34.416 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 55 | [cololi/deepseek-harness](https://github.com/cololi/deepseek-harness) | 0 | 55.9 (observed) | 19.960 | 34.351 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 56 | [zhanglunet/deepseek-harness](https://github.com/zhanglunet/deepseek-harness) | 0 | 55.7 (observed) | 19.978 | 34.269 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 57 | [himomohi/deepseek-harness](https://github.com/himomohi/deepseek-harness) | 1 | 46.5 (observed) | 25.915 | 34.157 | 36 | 300 | ok | 新增约 36 个提交并修改 300 个文件，主要涉及 配置、文档、依赖、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 58 | [yomaser/deepseek-harness](https://github.com/yomaser/deepseek-harness) | 1 | 46.3 (observed) | 25.810 | 33.987 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 59 | [nydia/deepseek-harness](https://github.com/nydia/deepseek-harness) | 1 | 46.2 (observed) | 25.810 | 33.953 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 60 | [MauricioPerera/deepseek-harness](https://github.com/MauricioPerera/deepseek-harness) | 0 | 54.9 (observed) | 19.970 | 33.950 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 61 | [winddyhe/deepseek-harness](https://github.com/winddyhe/deepseek-harness) | 0 | 53.6 (observed) | 19.960 | 33.418 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 62 | [jbwashington/deepseek-harness](https://github.com/jbwashington/deepseek-harness) | 0 | 53.5 (observed) | 19.972 | 33.383 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 63 | [odonzyk/deepseek-harness](https://github.com/odonzyk/deepseek-harness) | 1 | 44.5 (observed) | 25.810 | 33.266 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 64 | [LosEcher/deepseek-harness](https://github.com/LosEcher/deepseek-harness) | 0 | 53.0 (observed) | 19.996 | 33.180 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 65 | [lasme-ephrem/LasmeX](https://github.com/lasme-ephrem/LasmeX) | 1 | 16.8 (observed) | 44.068 | 33.173 | 3 | 300 | ok | 新增约 3 个提交并修改 300 个文件，主要涉及 配置、文档；目标线索是“Harness agentique open source, extensible et francophone par défaut”。 |
| 66 | [boktoday/deepseek-harness](https://github.com/boktoday/deepseek-harness) | 1 | 44.2 (observed) | 25.810 | 33.148 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 67 | [ahmedsliman/deepseek-harness](https://github.com/ahmedsliman/deepseek-harness) | 0 | 52.8 (observed) | 19.961 | 33.101 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 68 | [Anyaoha/deepseek-harness](https://github.com/Anyaoha/deepseek-harness) | 1 | 44.0 (observed) | 25.810 | 33.070 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 69 | [vkn129/deepseek-harness](https://github.com/vkn129/deepseek-harness) | 1 | 43.9 (observed) | 25.810 | 33.046 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 70 | [2404589803/deepseek-harness](https://github.com/2404589803/deepseek-harness) | 1 | 43.8 (observed) | 25.810 | 33.005 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 71 | [shenyimings/deepseek-harness](https://github.com/shenyimings/deepseek-harness) | 1 | 43.7 (observed) | 25.810 | 32.969 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 72 | [baibizhe/deepseek-harness](https://github.com/baibizhe/deepseek-harness) | 0 | 51.9 (observed) | 19.996 | 32.776 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 73 | [roadlittledawn/deepseek-harness](https://github.com/roadlittledawn/deepseek-harness) | 1 | 42.9 (observed) | 25.810 | 32.640 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 74 | [WSQS/deepseek-harness](https://github.com/WSQS/deepseek-harness) | 0 | 51.6 (observed) | 19.996 | 32.627 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 75 | [achristofaro/deepseek-harness](https://github.com/achristofaro/deepseek-harness) | 1 | 42.6 (observed) | 25.810 | 32.527 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 76 | [leether/deepseek-harness](https://github.com/leether/deepseek-harness) | 0 | 51.1 (observed) | 19.959 | 32.405 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 77 | [mnky4a6/deepseek-harness](https://github.com/mnky4a6/deepseek-harness) | 1 | 42.1 (observed) | 25.810 | 32.345 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 78 | [phong711/deepseek-harness](https://github.com/phong711/deepseek-harness) | 1 | 42.1 (observed) | 25.810 | 32.338 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 79 | [Yihong89/deepseek-harness](https://github.com/Yihong89/deepseek-harness) | 2 | 36.3 (observed) | 29.302 | 32.096 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 80 | [Giuliao/deepseek-harness](https://github.com/Giuliao/deepseek-harness) | 0 | 50.2 (observed) | 19.999 | 32.071 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 81 | [pawaca/dsh-edge](https://github.com/pawaca/dsh-edge) | 0 | 50.1 (observed) | 19.993 | 32.050 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 82 | [dfkai/deepseek-harness](https://github.com/dfkai/deepseek-harness) | 0 | 50.1 (observed) | 19.995 | 32.043 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 83 | [missuzhang/deepseek-harness](https://github.com/missuzhang/deepseek-harness) | 1 | 41.2 (observed) | 25.810 | 31.950 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 84 | [GitHubxsy/deepseek-harness](https://github.com/GitHubxsy/deepseek-harness) | 0 | 49.4 (observed) | 19.975 | 31.761 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 85 | [Mike-7777777/deepseek-harness](https://github.com/Mike-7777777/deepseek-harness) | 1 | 40.6 (observed) | 25.810 | 31.738 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 86 | [BJTU-Netcomm/deepseek-harness-aiops](https://github.com/BJTU-Netcomm/deepseek-harness-aiops) | 0 | 39.4 (observed) | 26.300 | 31.557 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness for aiops: Everything is a Plugin”。 |
| 87 | [mallocxw/deepseek-harness](https://github.com/mallocxw/deepseek-harness) | 1 | 40.0 (observed) | 25.810 | 31.479 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 88 | [xiaolangde/deepseek-harness](https://github.com/xiaolangde/deepseek-harness) | 1 | 39.7 (observed) | 25.859 | 31.383 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 89 | [SandersNeo/deepseek-harness](https://github.com/SandersNeo/deepseek-harness) | 1 | 38.7 (observed) | 25.810 | 30.967 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 90 | [drscrewdriver/deepseek-harness](https://github.com/drscrewdriver/deepseek-harness) | 1 | 38.7 (observed) | 25.810 | 30.957 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 91 | [DeepThinkingZhouLiu/Deepseek-Harness-RSI](https://github.com/DeepThinkingZhouLiu/Deepseek-Harness-RSI) | 1 | 38.3 (observed) | 25.929 | 30.859 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 92 | [hari-bhandari/deepseek-harness](https://github.com/hari-bhandari/deepseek-harness) | 0 | 47.0 (observed) | 19.995 | 30.804 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 93 | [eyyoung/deepseek-harness](https://github.com/eyyoung/deepseek-harness) | 0 | 47.0 (observed) | 19.999 | 30.798 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 94 | [lululu811/deepseek-harness-owern](https://github.com/lululu811/deepseek-harness-owern) | 0 | 46.9 (observed) | 19.997 | 30.747 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 95 | [Vitaminaq/deepseek-harness](https://github.com/Vitaminaq/deepseek-harness) | 1 | 38.0 (observed) | 25.843 | 30.688 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 96 | [Tyler-R-Kendrick/deepseek-harness](https://github.com/Tyler-R-Kendrick/deepseek-harness) | 1 | 38.0 (observed) | 25.810 | 30.671 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 97 | [DogeJian/deepseek-harness](https://github.com/DogeJian/deepseek-harness) | 1 | 37.9 (observed) | 25.810 | 30.630 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 98 | [enbideren/deepseek-harness](https://github.com/enbideren/deepseek-harness) | 1 | 37.8 (observed) | 25.810 | 30.623 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 99 | [xiansheng888/deepseek-harness](https://github.com/xiansheng888/deepseek-harness) | 1 | 37.4 (observed) | 25.810 | 30.461 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 100 | [mgrillo75/deepseek-harness](https://github.com/mgrillo75/deepseek-harness) | 1 | 37.3 (observed) | 25.810 | 30.409 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 101 | [realchenwenqiao/dash-fork](https://github.com/realchenwenqiao/dash-fork) | 1 | 37.1 (observed) | 25.847 | 30.354 | 35 | 38 | ok | 新增约 35 个提交并修改 38 个文件，主要涉及 文档、依赖、UI/应用层、其他文件；目标线索是“DASH — terminal-native TUI for DeepSeek Harness: Claude Code-style full-screen interface, multi-model switching, behavior-ledger rewind”。 |
| 102 | [NzSN/deepseek-harness](https://github.com/NzSN/deepseek-harness) | 0 | 45.4 (observed) | 19.996 | 30.140 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 103 | [angry-shark/deepseek-harness](https://github.com/angry-shark/deepseek-harness) | 0 | 45.1 (observed) | 19.979 | 30.032 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 104 | [Linmoqian/deepseek-harness-cli](https://github.com/Linmoqian/deepseek-harness-cli) | 1 | 36.2 (observed) | 25.810 | 29.968 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness-cli版本”。 |
| 105 | [shijiejintoulwh/deepseek-harness](https://github.com/shijiejintoulwh/deepseek-harness) | 4 | 15.9 (observed) | 39.052 | 29.781 | 1 | 3 | ok | 新增约 1 个提交并修改 3 个文件，主要涉及 CI/构建、测试；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 106 | [BeiKeJieDeLiuLangMao/deepseek-harness-gestalt](https://github.com/BeiKeJieDeLiuLangMao/deepseek-harness-gestalt) | 0 | 44.2 (observed) | 19.998 | 29.693 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 107 | [SamboHassan/deepseek-harness](https://github.com/SamboHassan/deepseek-harness) | 1 | 35.5 (observed) | 25.810 | 29.671 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 108 | [ouyangyipeng/dsh-desktop-upstream-archive](https://github.com/ouyangyipeng/dsh-desktop-upstream-archive) | 1 | 35.3 (observed) | 25.848 | 29.648 | 12 | 67 | ok | 新增约 12 个提交并修改 67 个文件，主要涉及 配置、文档、其他文件、依赖；目标线索是“Archived upstream fork that preceded the independent DS-Harness Desktop repository”。 |
| 109 | [alexdeweb/deepseek-harness](https://github.com/alexdeweb/deepseek-harness) | 1 | 35.0 (observed) | 25.810 | 29.472 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 110 | [rvndnishad-work/deepseek-harness](https://github.com/rvndnishad-work/deepseek-harness) | 1 | 34.9 (observed) | 25.810 | 29.462 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 111 | [coder-v0/deepseek-harness](https://github.com/coder-v0/deepseek-harness) | 1 | 34.9 (observed) | 25.810 | 29.459 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 112 | [devin2255/deepseek-harness-desktop](https://github.com/devin2255/deepseek-harness-desktop) | 1 | 34.6 (observed) | 25.810 | 29.345 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 113 | [JayTing511/deepseek-harness](https://github.com/JayTing511/deepseek-harness) | 1 | 34.3 (observed) | 25.810 | 29.214 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 114 | [srwang0506/deepseek-harness](https://github.com/srwang0506/deepseek-harness) | 1 | 24.3 (observed) | 32.425 | 29.159 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 115 | [skyhancloud/deepseek-harness](https://github.com/skyhancloud/deepseek-harness) | 0 | 42.8 (observed) | 19.997 | 29.117 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 116 | [Stool233/deepseek-harness](https://github.com/Stool233/deepseek-harness) | 0 | 42.8 (observed) | 19.980 | 29.114 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 117 | [playboy662/deepseek-harness](https://github.com/playboy662/deepseek-harness) | 1 | 33.7 (observed) | 25.810 | 28.965 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 118 | [zenghuan/deepseek-harness](https://github.com/zenghuan/deepseek-harness) | 1 | 33.4 (observed) | 25.810 | 28.862 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 119 | [A1pha3/deepseek-harness](https://github.com/A1pha3/deepseek-harness) | 1 | 33.1 (observed) | 25.810 | 28.730 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 120 | [badestgod/deepseek-harness](https://github.com/badestgod/deepseek-harness) | 1 | 33.0 (observed) | 25.810 | 28.703 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 121 | [samcaicn/deepseek-harness](https://github.com/samcaicn/deepseek-harness) | 0 | 41.8 (observed) | 20.000 | 28.701 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 122 | [yunlongwen/deepseek-harness](https://github.com/yunlongwen/deepseek-harness) | 0 | 41.7 (observed) | 19.997 | 28.677 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 123 | [houkang/deepseek-harness](https://github.com/houkang/deepseek-harness) | 1 | 32.8 (observed) | 25.810 | 28.624 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“deepseek-harness”。 |
| 124 | [cq2021-coder/deepseek-harness-desktop](https://github.com/cq2021-coder/deepseek-harness-desktop) | 1 | 32.7 (observed) | 25.875 | 28.611 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“使用 tauri 为 DeepSeek Harness 生态打造的现代化桌面端应用”。 |
| 125 | [HybridMAS/deepseek-harness](https://github.com/HybridMAS/deepseek-harness) | 1 | 32.7 (observed) | 25.810 | 28.561 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 126 | [Xyc2016/deepseek-harness](https://github.com/Xyc2016/deepseek-harness) | 0 | 41.3 (observed) | 19.999 | 28.539 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 127 | [ldsenow/deepseek-harness](https://github.com/ldsenow/deepseek-harness) | 0 | 41.3 (observed) | 19.998 | 28.531 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 128 | [China-MY/deepseek-harness](https://github.com/China-MY/deepseek-harness) | 1 | 32.6 (observed) | 25.810 | 28.514 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 129 | [stevessr/deepseek-harness](https://github.com/stevessr/deepseek-harness) | 0 | 40.8 (observed) | 19.997 | 28.325 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 130 | [peter123023/deepseek-work](https://github.com/peter123023/deepseek-work) | 0 | 40.7 (observed) | 19.998 | 28.291 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness桌面版”，修改面待下一轮 compare/README 深扫。 |
| 131 | [tomchon/deepseek-harness](https://github.com/tomchon/deepseek-harness) | 1 | 32.0 (observed) | 25.810 | 28.287 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 132 | [youshen2/deepseek-harness](https://github.com/youshen2/deepseek-harness) | 1 | 31.8 (observed) | 25.877 | 28.258 | 3 | 51 | ok | 新增约 3 个提交并修改 51 个文件，主要涉及 配置、文档、其他文件、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 133 | [valentinshenfeld/deepseek-harness](https://github.com/valentinshenfeld/deepseek-harness) | 1 | 31.9 (observed) | 25.810 | 28.250 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 134 | [MasterToycode/deepseek-harness](https://github.com/MasterToycode/deepseek-harness) | 1 | 31.9 (observed) | 25.810 | 28.228 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 135 | [spgsroot/deepseek-harness](https://github.com/spgsroot/deepseek-harness) | 0 | 40.3 (observed) | 19.965 | 28.103 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 136 | [yazzang-homelab/deepseek-harness](https://github.com/yazzang-homelab/deepseek-harness) | 2 | 16.5 (observed) | 35.762 | 28.067 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 137 | [shdeng/deepseek-harness-app](https://github.com/shdeng/deepseek-harness-app) | 1 | 31.3 (observed) | 25.921 | 28.054 | 10 | 220 | ok | 新增约 10 个提交并修改 220 个文件，主要涉及 配置、文档、其他文件、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 138 | [HossamTabana/deepseek-harness](https://github.com/HossamTabana/deepseek-harness) | 1 | 31.3 (observed) | 25.810 | 28.019 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 139 | [gladmo/deepseek-harness](https://github.com/gladmo/deepseek-harness) | 0 | 39.9 (observed) | 19.992 | 27.967 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 140 | [Shengqi-Pan/deepseek-harness](https://github.com/Shengqi-Pan/deepseek-harness) | 0 | 39.5 (observed) | 19.960 | 27.784 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 141 | [slamsmart/deepseek-harness](https://github.com/slamsmart/deepseek-harness) | 1 | 30.6 (observed) | 25.810 | 27.730 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 142 | [bkcarlos/deepseek-harness](https://github.com/bkcarlos/deepseek-harness) | 0 | 39.3 (observed) | 19.994 | 27.716 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 143 | [MrNQC/deepseek-harness](https://github.com/MrNQC/deepseek-harness) | 1 | 16.4 (observed) | 35.256 | 27.695 | 1 | 18 | ok | 新增约 1 个提交并修改 18 个文件，主要涉及 配置、依赖、文档、Harness 核心能力；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 144 | [yuanguangshan/deepseek-harness](https://github.com/yuanguangshan/deepseek-harness) | 0 | 39.2 (observed) | 19.997 | 27.678 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 145 | [huiliyi37/deepseek-harness](https://github.com/huiliyi37/deepseek-harness) | 2 | 25.1 (observed) | 29.302 | 27.632 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 146 | [maigadohcrypto/deepseek-harness](https://github.com/maigadohcrypto/deepseek-harness) | 1 | 30.2 (observed) | 25.810 | 27.581 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 147 | [wellfuture/deepseek-harness](https://github.com/wellfuture/deepseek-harness) | 1 | 30.1 (observed) | 25.810 | 27.516 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 148 | [sdkwork-ai/deepseek-harness-desktop](https://github.com/sdkwork-ai/deepseek-harness-desktop) | 4 | 17.9 (observed) | 33.837 | 27.467 | 48 | 300 | ok | 新增约 48 个提交并修改 300 个文件，主要涉及 配置、文档、其他文件、CI/构建；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 149 | [Kiowx/deepseek-harness](https://github.com/Kiowx/deepseek-harness) | 2 | 24.6 (observed) | 29.344 | 27.436 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 150 | [HugoluizMTB/deepseek-harness](https://github.com/HugoluizMTB/deepseek-harness) | 1 | 29.9 (observed) | 25.810 | 27.430 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 151 | [cFqr-lang/deepseek-harness](https://github.com/cFqr-lang/deepseek-harness) | 1 | 5.1 (observed) | 42.239 | 27.395 | 10 | 62 | ok | 新增约 10 个提交并修改 62 个文件，主要涉及 UI/应用层、文档、Harness 核心能力、配置；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 152 | [HelloNicoo/deepseek-harness](https://github.com/HelloNicoo/deepseek-harness) | 1 | 29.7 (observed) | 25.810 | 27.364 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 153 | [misshehe/deepseek-harness](https://github.com/misshehe/deepseek-harness) | 1 | 29.7 (observed) | 25.810 | 27.356 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 154 | [shiaho777/deepseek-harness](https://github.com/shiaho777/deepseek-harness) | 0 | 38.4 (observed) | 19.994 | 27.343 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 155 | [Ladyj003/deepseek-harness](https://github.com/Ladyj003/deepseek-harness) | 1 | 29.5 (observed) | 25.810 | 27.297 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 156 | [lisihao/deepseek-solar-harness](https://github.com/lisihao/deepseek-solar-harness) | 0 | 38.0 (observed) | 19.985 | 27.210 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 157 | [tranvantrung95/deepseek-harness](https://github.com/tranvantrung95/deepseek-harness) | 1 | 29.3 (observed) | 25.810 | 27.198 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 158 | [NewMFF/deepseek-harness](https://github.com/NewMFF/deepseek-harness) | 1 | 29.1 (observed) | 25.810 | 27.128 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 159 | [zdy-ai/deepseek-harness](https://github.com/zdy-ai/deepseek-harness) | 1 | 29.0 (observed) | 25.810 | 27.105 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 160 | [oscarlius/deepseek-harness](https://github.com/oscarlius/deepseek-harness) | 1 | 28.9 (observed) | 25.810 | 27.052 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 161 | [TomYang1024/deepseek-harness](https://github.com/TomYang1024/deepseek-harness) | 1 | 28.8 (observed) | 25.810 | 26.994 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 162 | [KinomotoMio/deepseek-harness](https://github.com/KinomotoMio/deepseek-harness) | 1 | 28.7 (observed) | 25.810 | 26.969 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 163 | [linfunss/deepseek-harness](https://github.com/linfunss/deepseek-harness) | 1 | 28.4 (observed) | 25.810 | 26.857 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 164 | [stephenlzc/deepseek-harness](https://github.com/stephenlzc/deepseek-harness) | 0 | 37.1 (observed) | 19.962 | 26.801 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 165 | [dailin3/deepseek-harness](https://github.com/dailin3/deepseek-harness) | 1 | 28.2 (observed) | 25.810 | 26.770 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 166 | [biyan113/deepseek-harness](https://github.com/biyan113/deepseek-harness) | 1 | 28.1 (observed) | 25.850 | 26.767 | 3 | 55 | ok | 新增约 3 个提交并修改 55 个文件，主要涉及 CI/构建、UI/应用层、文档、依赖；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 167 | [yx54hego-cloud/deepseek-harness](https://github.com/yx54hego-cloud/deepseek-harness) | 9 | 7.0 (observed) | 39.767 | 26.667 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 168 | [Rostopher/deepseek-harness](https://github.com/Rostopher/deepseek-harness) | 1 | 27.8 (observed) | 25.810 | 26.622 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 169 | [zicowarn/deepseek-harness](https://github.com/zicowarn/deepseek-harness) | 0 | 36.6 (observed) | 19.975 | 26.621 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 170 | [AIxITC/deepseek-harness](https://github.com/AIxITC/deepseek-harness) | 0 | 16.1 (observed) | 33.610 | 26.604 | 2 | 70 | ok | 新增约 2 个提交并修改 70 个文件，主要涉及 配置、文档、UI/应用层、Harness 核心能力；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 171 | [zng8418/deepseek-harness](https://github.com/zng8418/deepseek-harness) | 1 | 27.6 (observed) | 25.810 | 26.541 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 172 | [markisaac/deepseek-harness](https://github.com/markisaac/deepseek-harness) | 1 | 27.5 (observed) | 25.810 | 26.501 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 173 | [iKing/deepseek-harness](https://github.com/iKing/deepseek-harness) | 1 | 27.5 (observed) | 25.810 | 26.469 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 174 | [pellera9/deepseek-harness](https://github.com/pellera9/deepseek-harness) | 1 | 27.4 (observed) | 25.810 | 26.450 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 175 | [lizhenshuai/deepseek-harness-desktop](https://github.com/lizhenshuai/deepseek-harness-desktop) | 1 | 17.0 (observed) | 32.683 | 26.414 | 3 | 3 | ok | 新增约 3 个提交并修改 3 个文件，主要涉及 配置、文档；目标线索是“DeepSeek Harness 桌面客户端（Windows）”。 |
| 176 | [BlackRosePetals/deepseek-harness](https://github.com/BlackRosePetals/deepseek-harness) | 1 | 27.3 (observed) | 25.810 | 26.401 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 177 | [yiyualt/deepseek-harness](https://github.com/yiyualt/deepseek-harness) | 0 | 35.9 (observed) | 19.994 | 26.361 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 178 | [t479842598/deepseek-harness](https://github.com/t479842598/deepseek-harness) | 1 | 26.7 (observed) | 25.918 | 26.250 | 16 | 13 | ok | 新增约 16 个提交并修改 13 个文件，主要涉及 Harness 核心能力、测试；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 179 | [imhieu/deepseek-harness](https://github.com/imhieu/deepseek-harness) | 1 | 26.7 (observed) | 25.810 | 26.183 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 180 | [Keryer/deepseek-harness](https://github.com/Keryer/deepseek-harness) | 0 | 35.4 (observed) | 19.983 | 26.167 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 181 | [Helpless5699/deepseek-harness](https://github.com/Helpless5699/deepseek-harness) | 1 | 26.7 (observed) | 25.810 | 26.161 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 182 | [melkharbili/deepseek-harness](https://github.com/melkharbili/deepseek-harness) | 1 | 26.5 (observed) | 25.810 | 26.099 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 183 | [4evour/deepseek-harness](https://github.com/4evour/deepseek-harness) | 1 | 26.5 (observed) | 25.810 | 26.073 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 184 | [xiaosenho/deepseek-harness](https://github.com/xiaosenho/deepseek-harness) | 1 | 16.3 (observed) | 32.412 | 25.975 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 185 | [SquabbyZ/deepseek-harness](https://github.com/SquabbyZ/deepseek-harness) | 0 | 34.8 (observed) | 19.985 | 25.895 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 186 | [coolman1984/deepseek-harness](https://github.com/coolman1984/deepseek-harness) | 1 | 25.9 (observed) | 25.810 | 25.861 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 187 | [KevinSCUTer/deepseek-harness](https://github.com/KevinSCUTer/deepseek-harness) | 1 | 25.8 (observed) | 25.810 | 25.823 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 188 | [QingGeLaiYe/deepseek-harness](https://github.com/QingGeLaiYe/deepseek-harness) | 1 | 25.6 (observed) | 25.810 | 25.711 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness”。 |
| 189 | [WyrdWerk/deepseek-harness](https://github.com/WyrdWerk/deepseek-harness) | 1 | 25.1 (observed) | 25.932 | 25.586 | 13 | 272 | ok | 新增约 13 个提交并修改 272 个文件，主要涉及 配置、文档、CI/构建、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 190 | [deveuper/deepseek-harness](https://github.com/deveuper/deepseek-harness) | 1 | 25.0 (observed) | 25.821 | 25.506 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 191 | [aqiyoung/deepseek-harness](https://github.com/aqiyoung/deepseek-harness) | 0 | 33.5 (observed) | 19.994 | 25.401 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 192 | [yueyucaotian/deepseek-harness](https://github.com/yueyucaotian/deepseek-harness) | 1 | 24.8 (observed) | 25.810 | 25.391 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 193 | [MinerBin/deepseek-harness](https://github.com/MinerBin/deepseek-harness) | 1 | 24.5 (observed) | 25.810 | 25.290 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 194 | [18217778896/deepseek-harness](https://github.com/18217778896/deepseek-harness) | 1 | 24.2 (observed) | 25.810 | 25.178 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 195 | [leixiaochenShen/deepseek-harness](https://github.com/leixiaochenShen/deepseek-harness) | 1 | 24.0 (observed) | 25.810 | 25.092 | 0 | 0 | ok | 未观察到相对 upstream 的文件修改；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 196 | [icatw/deepseek-harness](https://github.com/icatw/deepseek-harness) | 0 | 32.7 (observed) | 19.996 | 25.070 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“DeepSeek Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 197 | [liwuli/deepseek-harness-desktop](https://github.com/liwuli/deepseek-harness-desktop) | 1 | 23.9 (observed) | 25.864 | 25.066 | 2 | 28 | ok | 新增约 2 个提交并修改 28 个文件，主要涉及 CI/构建、其他文件、文档、依赖；目标线索是“DeepSeek Harness desktop”。 |
| 198 | [Yarpii/deepseek-harness](https://github.com/Yarpii/deepseek-harness) | 0 | 32.7 (observed) | 19.976 | 25.051 | — | — | metadata-only | 当前仅确认这是 upstream 的公开 Fork；公开描述目标线索是“Harness: Everything is a Plugin”，修改面待下一轮 compare/README 深扫。 |
| 199 | [tzy168/deepseek-harness](https://github.com/tzy168/deepseek-harness) | 1 | 23.8 (observed) | 25.851 | 25.012 | 2 | 25 | ok | 新增约 2 个提交并修改 25 个文件，主要涉及 配置、文档、Harness 核心能力、测试；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |
| 200 | [nostalgia296/deepseek-harness-termux](https://github.com/nostalgia296/deepseek-harness-termux) | 1 | 23.6 (observed) | 25.871 | 24.961 | 2 | 33 | ok | 新增约 2 个提交并修改 33 个文件，主要涉及 配置、文档、测试、UI/应用层；目标线索是“DeepSeek Harness: Everything is a Plugin”。 |

> Showing the first 200 rows here; `12,302` rows are preserved in `index/forks.jsonl` and `docs/data/forks.json`.

## Interpretation

The collector records every public Fork returned by the paginated endpoint. Deep compare, recent commits, and README metadata are rotated by a per-run budget because GitHub rate limits make an unbounded daily deep audit impractical for a network of this size. Use `python3 scripts/collect_forks.py --deep-scan-all` only when the available token and request budget are sufficient.
