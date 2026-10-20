# HCI 会议赞助商数据集：CHI / CSCW / UIST / UbiComp

收集四个 ACM HCI 会议历年官网上公开的赞助商名单、赞助等级与公开价目，并做了整理、估算和可视化，用于讨论学术会议与产业界的关系。

- **覆盖**：737 条赞助记录，216 家机构，69 个会议届次
  - CHI：1996、1998、2006–2026
  - CSCW：2013–2026
  - UIST：2007–2025（缺 2008 年以前和少数年份）
  - UbiComp / ISWC：2013–2025
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
  index.html, flags.js        # 交互式 dashboard（原为 Claude Dashboard artifact 编写）
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
- **注册人数**：CHI 来自 SIGCHI 存档与 Wikipedia（2024、2025）；CSCW 仅到 2018，UIST、UbiComp 仅到 2019。

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

## 许可

数据整理自公开网页，仅供研究使用；各机构名称与 logo 归其所有者。国旗图标来自 [flag-icons](https://github.com/lipis/flag-icons)（MIT）。
