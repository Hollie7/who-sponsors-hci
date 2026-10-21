# 学术会议赞助商数据集：HCI（CHI / CSCW / UIST / UbiComp / DIS / IUI / FAccT / AIES）与 AI（NeurIPS / ICML / ICLR）

收集四个 ACM HCI 会议历年官网上公开的赞助商名单、赞助等级与公开价目，并做了整理、估算和可视化，用于讨论学术会议与产业界的关系。

- **覆盖**：983 条赞助记录，298 家机构，105 个会议届次
  - CHI：1996、1998、2006–2026
  - CSCW：2013–2026
  - UIST：2007–2025（缺 2008 年以前和少数年份）
  - UbiComp / ISWC：2013–2025
  - DIS：2016、2019、2022、2024–2026（2014、2017、2018 旧官网失效或域名被占用；2020–2021 线上会议未见赞助名单）
  - IUI：2015–2026（缺 2013–2014）
  - FAccT：2018–2026（官网只列名单、不分等级）
  - AIES：2018–2026（2023 年起公开价目 $30k / $20k / $10k / $5k）
- **数据整理时间**：2026 年 10 月

## 目录

```
data/
  raw/sponsors_raw.csv        # 手工/半自动录入的原始记录：会议、年份、等级、机构名、来源网页
  tier_prices.csv             # 官网/招商书上公开的赞助等级起步价
  sponsor_listings.csv        # 清洗后的明细（build.py 生成）
  per_conference_year.csv     # 每届汇总：赞助方数、企业数、估算金额、注册人数（build.py 生成）
  top_sponsors.csv            # 机构排名（build.py 生成）
scripts/
  build.py                    # 由 raw 数据生成上面三个文件
  countries.py                # 机构 → 总部所在国家/地区、母公司国籍
  make_standalone.py          # 生成可直接在浏览器打开的 dashboard/standalone.html
dashboard/
  index.html, flags.js        # 交互式 dashboard（原为 Claude Dashboard artifact 编写；英文 / 中文可切换，默认英文）
  standalone.html             # 独立版本，可用 GitHub Pages 或本地 http 服务打开
```

## 重新生成

```bash
pip install pandas
python scripts/build.py            # 重新生成 data/ 下的派生文件
python scripts/make_standalone.py  # 重新生成 dashboard/standalone.html
python -m http.server 8000         # 然后打开 http://localhost:8000/dashboard/standalone.html
```

## 字段说明（`sponsor_listings.csv`）

| 字段 | 含义 |
|---|---|
| `conference`, `year` | 会议与年份 |
| `tier` | 官网上的赞助等级原名（Hero / Champion / Platinum / Gold / Friend / Supporter / Unspecified 等） |
| `sponsor` | 官网上的机构名（或 logo 文件名推断出的名称） |
| `org` | 归一化后的机构名（如 Facebook / Meta / Oculus → `Meta/Facebook`） |
| `sector` | Industry / Government / foundation / University / academic / Publisher |
| `est_usd` | 按该等级的公开起步价估算的最低金额；未知为空 |
| `price_basis` | `stated`（当年公开价）或 `assumed (...)`（沿用相邻年份价目）等 |
| `country` | 赞助实体自身总部所在地（ISO 代码；`EU` 为欧盟资助项目） |
| `parent_country` | 母公司国籍（仅 TRI、FXPAL、MERL、Megagon Labs、Nokia Bell Labs 与 `country` 不同） |
| `source` | 数据来源网页 |

## 方法与口径

- **来源**：各届官网的赞助页、招商书（Invitation to Sponsor / Call for Sponsors）、SIGCHI 历史存档（注册人数）。部分站点禁止自动抓取，是用浏览器人工打开后读取的。
- **机构名**：很多 logo 没有替代文字，机构名由图片文件名或链接推断；无法判断的保留原样或标为未知。
- **金额是下限估算，不是会议实际收入**：每家赞助商按其等级的公开起步价计；不含主题赞助、展位、招聘、广告等额外付费；未公布价格的年份沿用相邻年份价目；Friend / Supporter 一律按 $1,000 计；CSCW 2023–2024 没有公开价目，按每家 $1,000 的假设计。
- **每届估算只在至少一半赞助条目有价格时才给出**；UbiComp 2020–2024、CSCW 2014/2020、CHI 1996/1998 因等级缺失不给金额。
- **非货币支持**（UbiComp 2015 的日本学会/政府 Supporter、UIST 2025 的 Special Support 等）计入名单，不计入金额。
- **主办方不计为赞助商**：ACM、SIGCHI、SIGGRAPH、SIGMOBILE。
- **Google DeepMind / DeepMind 计入 Google**：同一届两者都出现时只计一次。FAccT 和 AIES 的官网常把两个 logo 并列，录入时合并成一条 Google，因此这两个会议看不出哪一届是 DeepMind 出资（待补“子品牌”一列）。
- **注册人数**：CHI 来自 SIGCHI 存档与 Wikipedia（2024、2025）；CSCW 仅到 2018，UIST、UbiComp 仅到 2019。

### DIS / IUI / FAccT 的口径

- **IUI** 每年公开等级价（2016：$8k / $5k / $2.5k / $1k；2018 年起：$10k / $5k / $2.5k / $1k；2021 线上：$5k / $2.5k / $1k；2017 为欧元价，按 1.13 折算）。
- **DIS** 只有 2019 年公开价目（$10k / $5k / $1k），其他年份不估算金额。
- **FAccT** 的赞助政策公开了 5 档价格（2021–2022：$5k–$75k；2023 年起：$10k–$75k），但赞助商页面不标等级，所以每家按当年最低一档估算，是“下限的下限”。2018–2020 年按 $5k 计。
- 主办学会（ACM、SIGCHI、SIGAI）不计；承办高校标为 `Supporter (host)`，计入名单但不计金额。

## 已知缺口

- CHI 1997、1999–2005；CHI 2012 的 Contributor 只以图片呈现，未收录。
- CSCW 2012 年以前：早年官网已失效。
- UbiComp 2025 的 One Ring、SUSTAIN、SparQi Lab 所属地未知。

## 主要发现（2013–2026）

1. **CSCW 的企业赞助大幅下滑**：估算赞助额从 2013–2017 年平均约 $61k/届降到 2023–2026 年约 $9k/届；Meta（2013–2022 年几乎每届最高等级）、Microsoft（2021 年后）、IBM（2019 年后）先后退出。
2. **高度集中**：181 家赞助机构中 131 家只出现一届；Google、Microsoft、Meta、Adobe、Autodesk 占约 1/3 的“机构 × 届次”和约 41% 的估算金额。
3. **CHI 规模扩大但赞助没跟上**：人均赞助从 2013–2019 年约 $70–94 降到 2020–2024 年约 $36–57。
4. **赞助方换血**：IBM、Yahoo、Bloomberg 退出；Apple、Toyota Research Institute、Meta Reality Labs、Huawei 进入，偏向 XR / 硬件 / AI 产品方向。
5. **以美国机构为主，非美国赞助多为东道主效应**：非美国的“机构 × 届次”约 40% 出现在会议恰好在该国举办的年份。

### 补充：DIS / IUI / FAccT

- 三个会议的赞助规模都很小：IUI 每届估算约 $6k–$29k，通常 3–8 家；DIS 的名单常常只有 1–5 家，且很多是当地旅游局、市政府和承办高校。
- **FAccT 的资金结构很特别**：约 40% 的赞助条目来自基金会（MacArthur 8 届、Ford、Sloan、Luminate、Schmidt、Rockefeller、Open Society 等），这在其他 HCI 会议里很少见；企业方面 Google（含 DeepMind）每届都在，Microsoft 7 届，OpenAI 从 2021 年起 5 届，近两年还有 TikTok。
- **Google 是唯一在七个会议里都出现的企业**，并且是 IUI（10 届）和 FAccT（9 届）的头号赞助方。
- **AIES 与 FAccT 对比**：两边约 58% 的条目来自企业，但构成不同。FAccT 的基金会以 MacArthur、Ford、Sloan、Luminate 等社会公正/公民社会方向为主；AIES 的基金会则是 Future of Life Institute、BERI、Founders Pledge、Survival and Flourishing Fund 等 AI 安全/长期主义方向。企业方面，FAccT 有 OpenAI、Microsoft；AIES 则更多是 IBM（7 届）、PwC、JPMorgan Chase（2023–2025）、Salesforce、Lenovo、Ericsson 这类卖企业服务或受监管的公司。AIES 的估算赞助在 2023 年达到约 $160k 后回落到 2026 年的约 $45k。
- IUI 2023 年起企业赞助明显减少，NSF、MDPI、MBZUAI 等非企业机构成为主要支持方。

## AI 会议部分（NeurIPS / ICML / ICLR，2013–2026）

```
data/ai/raw/{neurips,icml,iclr}_raw.tsv   # 原始名单：年份、举办地、等级、机构名、链接（EMPTY = 当年没取得名单）
data/ai/ai_sponsor_listings.csv          # 清洗后明细（同一机构在一届只保留最高等级）
data/ai/ai_per_conference_year.csv       # 每届汇总：赞助方数、金融机构数、估算金额、注册人数
data/ai/ai_top_sponsors.csv              # 机构排名
data/ai/ai_tier_prices.csv               # 找到的两份公开价目
scripts/ai/build_ai.py                   # 由 raw 生成以上文件（python scripts/ai/build_ai.py）
scripts/ai/normalize.py, ai_meta.py      # 机构名归一化；行业类型与国家归属
dashboard/ai/                            # AI 会议 dashboard（含与 HCI 的对比）
```

- **覆盖**：1,907 条赞助记录，578 家机构，33 个会议届次。NeurIPS 2013–2026（2021 年没有设赞助）、ICML 2015–2026、ICLR 2017、2020–2026。
- **来源**：2015 年起来自 neurips.cc / icml.cc / iclr.cc 的公开赞助接口 `/sponsors/api/sponsors/public/?year=Y`；NeurIPS 2013–2014 来自会议手册 PDF；ICML 2015–2016、ICLR 2017 来自旧官网存档；ICLR 2026 来自其赞助商列表页。
- **缺口**：ICML 2013–2014、ICLR 2013–2016 与 2018–2019。
- **机构合并**：DeepMind / Google Research / Kaggle → Google；LinkedIn → Microsoft；Habana、Nervana → Intel；Xilinx → AMD；TikTok → ByteDance；Borealis AI → RBC；MosaicML → Databricks；TRI → Toyota。
- **行业类型**：科技及其他企业 / 金融·量化（对冲基金、做市商、银行、金融数据、VC）/ 政府·学术·非营利 / 出版社。
- **金额**：只找到 NeurIPS 2024 与 ICML 2026 的公开价目，只给相邻年份（NeurIPS 2023–2025、ICML 2025–2026）估算；Silver Pavilion、Startup 等无价等级不计。参照：NeurIPS 官方预算说明中 2019 年赞助收入为 $3.7M。
- **注册人数**：NeurIPS fact sheet、ICML 官方统计、ICLR 来自 Wikipedia。
- **国家**：按赞助实体总部；约 40 家小公司无法确定，标为 `??`。

### 主要发现（与 HCI 对比）

1. **规模差一个数量级**：NeurIPS 2025 估算赞助下限约 $5.8M、148 家赞助方；同年 CHI 约 $0.43M、21 家。
2. **金融/量化是第二大赞助群体**：约 22% 的赞助条目、约 28% 的可估算金额来自 Citadel、Jane Street、Jump、D. E. Shaw、Two Sigma、HRT、Optiver、G-Research 等，比例多年稳定；HCI 会议几乎没有。
3. **同一批大厂两边分配不同**：Google、Microsoft、Meta 两边都长期赞助；Adobe、Autodesk 主要在 HCI；Amazon、Baidu、ByteDance 几乎只在 AI。
4. **中国机构占比更高**：AI 会议约 9% 的“机构 × 届次”来自中国大陆（百度、字节、阿里、蚂蚁、腾讯、华为、宽德、明汯、聚宽等量化机构），HCI 不到 3%。
5. **新进入者是 AI 基础设施与数据公司**：Lambda、Together AI、Nebius、Cerebras、Scale AI、Toloka、Turing、Handshake 等 2023 年后大量出现，一半以上机构只出现过一届。

## 许可

数据整理自公开网页，仅供研究使用；各机构名称与 logo 归其所有者。国旗图标来自 [flag-icons](https://github.com/lipis/flag-icons)（MIT）。
