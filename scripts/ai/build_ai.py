"""Build AI-conference sponsor tables (NeurIPS / ICML / ICLR, 2013-2026)."""
import os, pandas as pd
from normalize import norm, SKIP
from ai_meta import sector, country, parent_country
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, '..', '..', 'data', 'ai', 'raw'); OUT = os.path.join(HERE, '..', '..', 'data', 'ai'); os.makedirs(OUT, exist_ok=True)

SRC_API = {'NeurIPS': 'https://neurips.cc/sponsors/api/sponsors/public/?year={y}', 'ICML': 'https://icml.cc/sponsors/api/sponsors/public/?year={y}',
           'ICLR': 'https://iclr.cc/sponsors/api/sponsors/public/?year={y}'}
ds = []
for f, c in [('neurips', 'NeurIPS'), ('icml', 'ICML'), ('iclr', 'ICLR')]:
    d = pd.read_csv(os.path.join(RAW, f + '_raw.tsv'), sep='\t', header=None, names=['year', 'loc', 'tier', 'sponsor', 'link'], quoting=3)
    d['conference'] = c
    d = d[d.tier.notna() & ~d.sponsor.isin(SKIP)].copy()
    d['source'] = d.apply(lambda r: r.link if str(r.link).startswith('https://media.nips.cc') or 'index.html' in str(r.link) or 'doku.php' in str(r.link)
                          else ('https://iclr.cc/virtual/2026/sponsor_list' if (c == 'ICLR' and r.year == 2026) else SRC_API[c].format(y=r.year)), axis=1)
    ds.append(d)
d = pd.concat(ds, ignore_index=True)
d['org'] = d.sponsor.map(norm)
d['tier'] = d.tier.str.strip()

# monetary rank of tiers (higher = bigger); used to keep one row per org per edition
RANK = {'Double Diamond': 10, 'Diamond': 9, 'Platinum': 8, 'Platinum 1': 8, 'Platinum 2': 8, 'Ruby': 5.5, 'Sapphire': 7.5, 'Gold': 7, 'Silver': 6,
        'Silver (+)': 6, 'Silver Pavilion': 5, 'Bronze': 4, 'Bronze (Non-Profit Only)': 4, 'Supporting': 3, 'Startup': 2, 'Start-Up Companies': 2,
        'Start-Up Companies +': 2, 'Exhibitor': 2, 'Mexico Sponsor Level': 2, 'De-Stress Puppy Lounge': 2,
        'Book Publisher': 1, 'Publisher': 1, 'Publishers of Scientific Research Journals and Books': 1, 'Unspecified': 0}
d['rank'] = d.tier.map(lambda t: 3 if 'DEI' in t or 'Participation Support' in t else RANK.get(t, 0))
d = (d.sort_values('rank', ascending=False).drop_duplicates(['conference', 'year', 'org'])
       .sort_values(['conference', 'year', 'rank', 'org'], ascending=[True, True, False, True]))
d['sector'] = d.org.map(sector)
d['country'] = d.org.map(country)
d['parent_country'] = d.org.map(parent_country)

# published price schedules (USD). NeurIPS 2024 and ICML 2026 are the only ones found publicly.
PRICES = {('NeurIPS', 2024): {'Diamond': 90000, 'Platinum': 50000, 'Gold': 35000, 'Silver': 22000, 'Bronze': 12000, 'Book Publisher': 1100},
          ('ICML', 2026): {'Diamond': 100000, 'Platinum': 80000, 'Gold': 45000, 'Silver': 30000, 'Bronze': 20000, 'Ruby': 18000, 'Book Publisher': 1000}}
USE = {('NeurIPS', 2023): ('NeurIPS', 2024), ('NeurIPS', 2024): ('NeurIPS', 2024), ('NeurIPS', 2025): ('NeurIPS', 2024),
       ('ICML', 2025): ('ICML', 2026), ('ICML', 2026): ('ICML', 2026)}
def price(r):
    k = USE.get((r.conference, r.year))
    if not k: return None, 'no price info'
    v = PRICES[k].get(r.tier)
    if v is None: return None, 'tier not priced'
    return v, 'stated' if k == (r.conference, r.year) else f'assumed ({k[0]} {k[1]} schedule)'
pp = d.apply(price, axis=1, result_type='expand'); d['est_usd'] = pp[0]; d['price_basis'] = pp[1]

ATT = {'NeurIPS': {2013: 1994, 2014: 2581, 2015: 3852, 2016: 5231, 2017: 8008, 2018: 8648, 2019: 13000, 2020: 22823, 2021: 17091, 2022: 15390,
                   2023: 16382, 2024: 19756, 2025: 18340},
       'ICML': {2017: 2429, 2018: 5019, 2019: 6483, 2020: 10806, 2021: 8863, 2022: 7103, 2023: 7921, 2024: 9095},
       'ICLR': {2018: 1950, 2019: 2600, 2020: 5600, 2021: 6300, 2022: 5200, 2023: 3758, 2024: 6533, 2025: 11039}}
ACTUAL = {('NeurIPS', 2019): 3700000}   # NeurIPS 2020 budget statement: 2019 sponsor income $3.7M

LV = lambda t: 'unknown' if t == 'Unspecified' else ('top' if t in ('Double Diamond', 'Diamond', 'Platinum', 'Platinum 1', 'Platinum 2') else
               'mid' if t in ('Gold', 'Silver', 'Silver (+)', 'Sapphire', 'Ruby') else 'low')
d['tier_level'] = d.tier.map(LV)
d.insert(0, 'id', range(1, len(d) + 1))
cols = ['id', 'conference', 'year', 'tier', 'sponsor', 'org', 'sector', 'country', 'parent_country', 'tier_level', 'est_usd', 'price_basis', 'source']
d[cols].to_csv(os.path.join(OUT, 'ai_sponsor_listings.csv'), index=False)

pcy = d.groupby(['conference', 'year']).agg(n_sponsors=('org', 'nunique'),
        n_finance=('sector', lambda s: (s == 'Finance / quant').sum()),
        n_industry=('sector', lambda s: s.isin(['Finance / quant', 'Tech & other industry']).sum()),
        est_usd=('est_usd', 'sum'), priced=('est_usd', lambda s: s.notna().sum())).reset_index()
pcy['est_usd'] = pcy.apply(lambda r: r.est_usd if r.priced >= 0.5 * r.n_sponsors else None, axis=1)
pcy['reported_sponsor_income_usd'] = pcy.apply(lambda r: ACTUAL.get((r.conference, r.year)), axis=1)
pcy['attendance'] = pcy.apply(lambda r: ATT.get(r.conference, {}).get(r.year), axis=1)
pcy['usd_per_attendee'] = pcy.est_usd / pcy.attendance
pcy.to_csv(os.path.join(OUT, 'ai_per_conference_year.csv'), index=False)

top = (d.groupby('org').agg(sector=('sector', 'first'), country=('country', 'first'), appearances=('year', 'size'),
        conferences=('conference', lambda s: ', '.join(sorted(s.unique()))), first=('year', 'min'), last=('year', 'max'),
        est_usd=('est_usd', 'sum')).reset_index().sort_values(['appearances', 'est_usd'], ascending=False))
top.to_csv(os.path.join(OUT, 'ai_top_sponsors.csv'), index=False)
SRCP = {('NeurIPS', 2024): 'https://dev.neurips.cc/Exhibitors/exhibitorinfo', ('ICML', 2026): 'https://icml.cc/sponsors/sponsorinfo'}
pr = pd.DataFrame([{'conference': k[0], 'years': str(k[1]), 'tier': t, 'min_usd': v, 'basis': 'stated · ' + SRCP[k]} for k, m in PRICES.items() for t, v in m.items()])
pr.insert(0, 'id', range(1, len(pr) + 1))
pr.to_csv(os.path.join(OUT, 'ai_tier_prices.csv'), index=False)
print(pcy.to_string()); print(top.head(30).to_string())
