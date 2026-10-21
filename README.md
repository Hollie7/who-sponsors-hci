# Who Sponsors HCI and AI-Ethics Conferences

Sponsor lists, sponsorship tiers and published tier prices for academic conferences, compiled from their public websites, cleaned up, estimated and visualized. The aim is to give some data to the ongoing debate about industry's role in academic HCI.

- **HCI and AI ethics:** CHI, CSCW, UIST, UbiComp, DIS, IUI, FAccT, AIES. 983 sponsor listings, 298 organizations, 105 conference editions.
- **AI:** NeurIPS, ICML, ICLR. 1,907 listings, 578 organizations, 33 editions.
- **Compiled:** October 2026, by Holly Tianqi Song ([hollysong.site](https://hollysong.site)).

## Repository layout

```
data/
  raw/sponsors_raw.csv          one row per sponsor as listed on the page: conference, year, tier, name, source URL
  sponsor_listings.csv          cleaned listings (generated)
  per_conference_year.csv       totals per edition: sponsors, companies, estimated amount, attendance (generated)
  top_sponsors.csv              organizations ranked by editions sponsored (generated)
  tier_prices.csv               published sponsorship tier prices
  ai/raw/{neurips,icml,iclr}_raw.tsv  raw AI conference lists (EMPTY = no list found that year)
  ai/ai_*.csv                   cleaned AI tables (generated)
scripts/
  build.py, countries.py        build the HCI tables; organization → country
  ai/build_ai.py, normalize.py, ai_meta.py   build the AI tables; name merging, sector, country
  make_standalone.py            local preview of the dashboards (dashboard/**/standalone.html)
  build_site.py                 build the public website into docs/
dashboard/
  index.html, flags.js          HCI and AI-ethics dashboard (English / Chinese)
  ai/index.html                 AI conference dashboard
docs/                           the public website (generated)
site.config.json                author, links and analytics settings for the website
```

## Rebuilding

```bash
pip install pandas
python scripts/build.py            # HCI tables in data/
python scripts/ai/build_ai.py      # AI tables in data/ai/
python scripts/build_site.py       # website in docs/
python -m http.server 8000         # then open http://localhost:8000/docs/
```

## Columns in `sponsor_listings.csv`

| Column | Meaning |
|---|---|
| `conference`, `year` | Conference and year |
| `tier` | Tier name as shown on the site (Hero, Champion, Platinum, Gold, Friend, Supporter, Unspecified, …) |
| `sponsor` | Name as shown on the site, or inferred from the logo's file name or link |
| `org` | Merged organization name (e.g. Facebook / Meta / Oculus → `Meta/Facebook`) |
| `sector` | Industry, Government / foundation, University / academic, Publisher |
| `est_usd` | Lower-bound estimate from the tier's published floor price; empty when unknown |
| `price_basis` | `stated` (that year's published price), `assumed (…)` (a nearby year's prices), or why there is none |
| `country` | Headquarters of the sponsoring entity (ISO code; `EU` = an EU-funded project) |
| `parent_country` | Country of the parent company, where it differs (e.g. Toyota Research Institute → JP) |
| `source` | Page the listing came from |

## Method

**Sources.** Each edition's sponsor page, archived copies of it, and sponsor prospectuses. Some sites block automated access and were read by hand in a browser. Attendance comes from the SIGCHI conference history archive (Wikipedia for CHI 2024–2025), the NeurIPS fact sheet, ICML's statistics and Wikipedia for ICLR.

**Counting.**
- An organization counts once per edition, whatever its tier.
- Organizers are not sponsors: ACM, SIGCHI, SIGAI, SIGGRAPH, SIGMOBILE and AAAI are left out.
- Host universities and local government or society supporters are listed (`Supporter (host)`, `Special`) but not counted in amounts.
- Brands of one company are merged: Meta/Facebook/Oculus, Yahoo/Verizon Media/Oath, Tableau/Salesforce, Google with DeepMind. In the AI data also LinkedIn → Microsoft, Habana and Nervana → Intel, Xilinx → AMD, TikTok → ByteDance, Borealis AI → RBC, MosaicML → Databricks, TRI → Toyota.
- FAccT and AIES often show Google and DeepMind logos side by side; these were entered as one Google listing, so for those two conferences the data cannot tell which editions DeepMind paid for.

**Estimated amounts.**
- Every amount is a lower bound: each sponsor counts at its tier's published floor price. Themed sponsorships, booths and recruiting fees are ignored. These are not what conferences actually received.
- Years without published prices reuse the nearest year's prices (`price_basis` says which). Friend and Supporter tiers count as $1,000.
- An edition gets an estimate only when at least half of its paying sponsors have a known price.
- FAccT publishes tier prices but not who is in which tier, so every FAccT sponsor counts at the lowest tier ($5k before 2023, $10k from 2023).
- For the AI conferences only two price lists were found (NeurIPS 2024, ICML 2026), so only NeurIPS 2023–2025 and ICML 2025–2026 are estimated. For reference, NeurIPS's budget statement reports $3.7M in sponsor income for 2019.

**Countries.** Two attributions: the sponsoring entity's headquarters, or its parent company. About 40 small companies (mostly in the AI data) could not be located.

## Coverage and gaps

| Conference | Sponsor lists | Missing | Tier prices |
|---|---|---|---|
| CHI | 1996, 1998, 2006–2026 | 1997, 1999–2005; CHI 2012 Contributors (image only) | 2006–2026 (published 2016, 2021, 2024–2026) |
| CSCW | 2013–2026 | before 2013 (sites gone) | published 2016, 2018, 2019, 2025, 2026; 2023–2024 assumed $1k each |
| UIST | 2007–2025 | before 2007 | published 2007, 2008, 2011, 2012, 2015, 2017, 2020, 2022–2025 |
| UbiComp | 2013–2025 | — | published 2014, 2015, 2017–2019, 2022–2023; 2020–2024 lists have no tiers |
| DIS | 2016, 2019, 2022, 2024–2026 | 2014, 2017, 2018 (sites gone); 2020–2021 online, no sponsors shown | 2019 only |
| IUI | 2015–2026 | 2013–2014 | every year (2017 in euros, ×1.13) |
| FAccT | 2018–2026 | — | tiers published, not assigned (see above) |
| AIES | 2018–2026 | — | published 2023–2026; 2018–2019 have no tiers |
| NeurIPS | 2013–2026 | 2021 had no sponsorship | 2024 |
| ICML | 2015–2026 | 2013–2014 | 2026 |
| ICLR | 2017, 2020–2026 | 2013–2016, 2018–2019 | none found |

## Findings

**CHI, CSCW, UIST and UbiComp, 2013–2026**

1. **Corporate sponsorship of CSCW collapsed.** The estimate fell from about $61k per edition in 2013–2017 to about $9k in 2023–2026. Meta (top tier at almost every edition 2013–2022), Microsoft (after 2021) and IBM (after 2019) all left.
2. **Highly concentrated.** Most sponsors appear only once. Google, Microsoft, Meta, Adobe and Autodesk account for about a third of all organization-editions and about 41% of the estimated money.
3. **CHI grew faster than its sponsorship.** Sponsorship per attendee fell from about $70–94 in 2013–2019 to about $36–57 in 2020–2024.
4. **Turnover in who pays.** IBM, Yahoo and Bloomberg left; Apple, Toyota Research Institute, Meta Reality Labs and Huawei arrived, leaning toward XR, hardware and AI products.
5. **Mostly American, with host effects elsewhere.** About 40% of non-US sponsorship happens in years when the conference is held in that sponsor's country.

**DIS, IUI, FAccT and AIES**

- All four are small. IUI has about $6k–29k and 3–8 sponsors per edition; DIS often lists 1–5, many of them local tourism boards, city governments and host universities.
- **FAccT is unusually foundation-funded.** About 40% of its listings are foundations (MacArthur in 8 editions, Ford, Sloan, Luminate, Schmidt, Rockefeller, Open Society). Google sponsored every edition, Microsoft seven, OpenAI five since 2021.
- **AIES has a different mix.** Companies make up a similar share (about 58%), but its foundations are AI-safety and longtermist funders (Future of Life Institute, BERI, Founders Pledge, Survival and Flourishing Fund), and its companies lean toward enterprise and regulated firms: IBM (7 editions), PwC, JPMorgan Chase (2023–2025), Salesforce, Lenovo, Ericsson.
- **Google is the only organization that sponsored all eight conferences.**

**AI conferences compared with HCI**

1. **An order of magnitude larger.** NeurIPS 2025 is estimated at $5.8M or more from 148 sponsors; CHI 2025 at about $0.43M from 21.
2. **Finance is the second-largest group.** About 22% of AI listings and 28% of the estimated money come from trading and quant firms (Citadel, Jane Street, Jump, D. E. Shaw, Two Sigma, HRT, Optiver, G-Research). HCI conferences have almost none.
3. **The same companies split differently.** Google, Microsoft and Meta sponsor both sides; Adobe and Autodesk mostly HCI; Amazon, Baidu and ByteDance almost only AI.
4. **More Chinese sponsors.** About 9% of AI organization-editions are from mainland China, versus under 3% for HCI.
5. **New entrants are AI infrastructure and data companies** (Lambda, Together AI, Nebius, Cerebras, Scale AI, Toloka, Turing, Handshake), mostly since 2023.

## Website

`docs/` is a static site: `docs/index.html` (HCI and AI ethics, English / Chinese) and `docs/ai/index.html` (AI conferences).

1. Fill in `site.config.json`: `author`, `homepage`, `email` (optional), `github_repo`, `site_url` and `goatcounter` (optional).
2. Run `python scripts/build_site.py`.
3. Deploy: import the repository in Vercel (`vercel.json` already serves `docs/` with no build step), or use GitHub Pages, Netlify or Cloudflare Pages.

Page views are counted with [GoatCounter](https://www.goatcounter.com/), which uses no cookies. Tick "Allow adding visitor counts on your website" in its settings so the footer can show the count.

## License and disclaimer

The data in `data/` are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) and the code under the MIT License (see `LICENSE` and `data/LICENSE`). You may reuse and adapt them, including commercially, with credit. Suggested citation:

> Holly Tianqi Song (2026). *Who Sponsors HCI and AI-Ethics Conferences*. https://github.com/Hollie7/who-sponsors-hci

This is an independent project, not affiliated with or endorsed by ACM, SIGCHI, AAAI, any of the conferences or any organization listed. The lists were compiled by hand from public pages and may be incomplete or contain errors; corrections are welcome as GitHub issues. Organization names and logos belong to their owners. Flag icons are from [flag-icons](https://github.com/lipis/flag-icons) (MIT).
