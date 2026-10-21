"""Build NLP-conference sponsor tables (ACL / EMNLP / NAACL, 2013-2026).

    python scripts/nlp/build_nlp.py

Reads data/nlp/raw/nlp_raw.tsv (one row per sponsor as listed, with the tier
name normalised to Diamond / Platinum / Gold / Silver / Bronze / Supporter /
D&I / Special / Exhibitor / Publisher / Unspecified) and writes data/nlp/nlp_*.csv.
Name merging, sector and country rules are shared with the ML tables
(scripts/ai/normalize.py and ai_meta.py), plus the NLP-specific additions below.
"""
import os, sys, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ai'))
import normalize, ai_meta
from normalize import norm

RAW = os.path.join(HERE, '..', '..', 'data', 'nlp', 'raw', 'nlp_raw.tsv')
OUT = os.path.join(HERE, '..', '..', 'data', 'nlp')

# ---- names ------------------------------------------------------------------------------
normalize.ALIAS.update({
    'microsoft translator': 'Microsoft', 'ibm watson': 'IBM', 'yahoo labs': 'Yahoo', 'toutiao': 'ByteDance', 'toutiao/bytedance': 'ByteDance',
    'naver line': 'NAVER', 'a9.com': 'Amazon', 'appen butler hill': 'Appen', 'j.p. morgan': 'JPMorgan Chase', 'jpmorgan chase': 'JPMorgan Chase',
    'hltcoe': 'Johns Hopkins University', 'johns hopkins university (clsp)': 'Johns Hopkins University',
    'isi': 'USC / ISI', 'usc': 'USC / ISI', 'recruit institute of technology': 'Recruit', 'recruit technologies': 'Recruit',
    'rakuten institute of technology': 'Rakuten', 'xerox research centre europe': 'Xerox',
    'cair (nyu abu dhabi)': 'NYU Abu Dhabi', 'new york university abu dhabi': 'NYU Abu Dhabi',
    'king salman global academy for the arabic language': 'King Salman Global Academy for Arabic', 'megagon labs': 'Megagon Labs', 'megagon': 'Megagon Labs',
    'cohere': 'Cohere', 'jd.com': 'JD.com', 'didi': 'DiDi', 'dataocean ai': 'DataOcean AI', 'toloka ai': 'Toloka', 'hpc-ai tech': 'HPC-AI Tech',
    'kaust': 'KAUST', 'mohamed bin zayed university of artificial intelligence': 'MBZUAI', 'chen institute': 'Chen Institute',
    'monash university': 'Monash University', 'visit melbourne': 'City of Melbourne', 'melbourne convention bureau': 'Melbourne Convention Bureau',
    'csiro data61': 'CSIRO', 'naver labs europe': 'NAVER', 'nec': 'NEC', 'sap': 'SAP', 'thomson reuters': 'Thomson Reuters',
    'lg ai research': 'LG', 'sony': 'Sony', 'samsung': 'Samsung', 'bosch': 'Bosch', 'huawei': 'Huawei', 'xiaomi': 'Xiaomi',
    'goldman sachs': 'Goldman Sachs', 'millennium': 'Millennium', 'natwest group': 'NatWest', 'capital one': 'Capital One', 'capital group': 'Capital Group',
    'ai2': 'Allen Institute for AI', 'text iq': 'Text IQ', 'datamundi': 'DATAmundi', 'neptune.ai': 'neptune.ai', 'rednote': 'rednote',
    'otter.ai': 'Otter.ai', 'gptzero': 'GPTZero', 'iflytek': 'iFlytek', 'nyu': 'New York University',
})

# ---- sector -----------------------------------------------------------------------------
ai_meta.FIN |= {'Goldman Sachs', 'Millennium', 'Jane Street', 'Capital Group', 'Vanguard', 'TIAA', 'Kensho', 'CreditEase', 'Ubiquant', 'Tether',
                'Krungthai Bank', 'KBTG', 'SCB 10X', 'Citadel', 'Two Sigma', 'Morgan Stanley', 'G-Research'}
ai_meta.PUB |= {'Elsevier', 'Morgan & Claypool', 'Springer'}
ai_meta.NONIND |= set('''University of Washington|Brandeis University|Columbia University|New York University|Johns Hopkins University|USC / ISI|Tulane University|
UC Santa Cruz|Florida International University|Monash University|KU Leuven|Research Foundation Flanders|Carnegie Mellon University Qatar|
Qatar Computing Research Institute|Qatar National Research Fund|NYU Abu Dhabi|MBZUAI|Technology Innovation Institute|KAUST|King Salman Global Academy for Arabic|
RIKEN AIP|COLIPS|Zhongguancun Academy|Chen Institute|Allen Institute for AI|HPLT Project|META-NET|MultilingualWeb-LT (W3C)|NSF|CRA Computing Community Consortium|
Chinese Information Processing Society of China|Bulgarian Academy of Sciences|Sofia Municipality|TCEB|NECTEC|AIAT|ETDA|AI Thailand|DST Group|CSIRO|DHCRC|
Melbourne Convention Bureau|City of Melbourne|Visit Brussels|Hong Kong Tourism Board|Singapore Exhibition & Convention Bureau|Meeting Destination Vienna|
Abu Dhabi Convention and Exhibition Bureau|Lisbon City Council|Turismo de Lisboa|INESC-ID|Instituto de Telecomunicações|Instituto Superior Técnico|IDEA Toscana'''
                         .replace('\n', '').split('|'))

# ---- country (headquarters; default US) ---------------------------------------------------
NLP_COUNTRY = {
    'CN': 'CreditEase|SinoVoice|Sogou|TP-Link|CVTE|Yitu|Shannon AI|Zhuiyi|GTCOM|Flitto|Xiaomi|Meituan|Kuaishou|StepFun|MiniMax|Ubiquant|MiroMind|ModelBest|'
          'Magic Data|Nexdata|Zhongguancun Academy|rednote|Chinese Information Processing Society of China|Bailu|Unix AI|Abaka AI',
    'GB': 'Spotify|Deloitte|KPMG|Babelscape|PolyAI|Trustpilot|Unbabel|Textkernel|Unsilo|Siteimprove|Wizkids|Ontotext|Mtel|Publicis MARC Group|Bulgarian Academy of Sciences|'
          'Sofia Municipality|Defined AI|DATAmundi|Speak|Keenable|Oruk|Alice|Thomson Reuters',
    'IT': 'Translated|Almawave|Expert System|IDEA Toscana|Babelscape|aiXplain',
    'DE': 'Zalando|Nyonic|BMW|Elsevier',
    'NL': 'Booking.com|Elsevier|Textkernel|Zeta Alpha',
    'DK': 'Siteimprove|Trustpilot|Unsilo|Wizkids',
    'PT': 'Priberam|Unbabel|Lisbon City Council|Turismo de Lisboa|INESC-ID|Instituto de Telecomunicações|Instituto Superior Técnico|TAP Air Portugal|DigitalGenius',
    'BG': 'Ontotext|Mtel|Publicis MARC Group|Bulgarian Academy of Sciences|Sofia Municipality',
    'BE': 'Visit Brussels|KU Leuven|Research Foundation Flanders',
    'AT': 'Meeting Destination Vienna',
    'JP': 'Rakuten|Recruit|LegalForce|Mercari|Hitachi|Baobab|RIKEN AIP|Megagon Labs',
    'KR': 'Flitto|LG|NAVER',
    'IN': 'Josh Talks',
    'TH': 'TCEB|Backyard|Krungthai Bank|AIS|NECTEC|AIAT|KBTG|ETDA|AI Thailand|SCB 10X',
    'QA': 'Qatar Computing Research Institute|Qatar National Research Fund|Carnegie Mellon University Qatar|iHorizons',
    'AE': 'NYU Abu Dhabi|MBZUAI|Technology Innovation Institute|Beyond Limits|Abu Dhabi Convention and Exhibition Bureau',
    'SA': 'KAUST|King Salman Global Academy for Arabic|SCAI',
    'SG': 'COLIPS|Singapore Exhibition & Convention Bureau|Ahrefs|HPC-AI Tech|Sahara AI',
    'HK': 'Hong Kong Tourism Board',
    'AU': 'Monash University|DST Group|CSIRO|DHCRC|Melbourne Convention Bureau|City of Melbourne|Sintelix|Appen|Roam Analytics',
    'CA': 'Maluuba|Cohere|NextAI|Borealis AI|GPTZero',
    'FR': 'Naver Labs Europe',
    'NO': 'Iris.ai',
    'FI': 'HPLT Project',
    'IL': 'Alice',
    'SV': 'Tether',
    'EU': 'META-NET|MultilingualWeb-LT (W3C)',
}
# a few above are deliberately overridden in order (last wins); fix the ones that need a single answer
FIX = {'Babelscape': 'IT', 'aiXplain': 'US', 'Textkernel': 'NL', 'Elsevier': 'NL', 'Siteimprove': 'DK', 'Trustpilot': 'DK', 'Unsilo': 'DK', 'Wizkids': 'DK',
       'Unbabel': 'PT', 'Ontotext': 'BG', 'Mtel': 'BG', 'Publicis MARC Group': 'BG', 'Bulgarian Academy of Sciences': 'BG', 'Sofia Municipality': 'BG',
       'Flitto': 'KR', 'Megagon Labs': 'US', 'Thomson Reuters': 'CA', 'Alice': 'IL', 'Roam Analytics': 'US', 'Appen': 'AU', 'Tether': 'SV',
       'Sahara AI': 'US', 'HPC-AI Tech': 'SG', 'DigitalGenius': 'GB', 'Bailu': '??', 'SDL': 'GB', 'VocalIQ': 'GB', 'neptune.ai': 'PL',
       'Speak': 'US', 'DATAmundi': 'PL', 'GPTZero': 'US', 'Keensight': '??', 'Keenable': '??', 'Oruk': '??', 'Unix AI': '??'}
for code, names in NLP_COUNTRY.items():
    for n in names.split('|'): ai_meta.COUNTRY[n] = code
ai_meta.COUNTRY.update(FIX)
ai_meta.PARENT.update({'Megagon Labs': 'JP', 'Naver Labs Europe': 'KR', 'Borealis AI': 'CA', 'DigitalGenius': 'GB', 'Thomson Reuters': 'CA',
                       'Toloka': 'NL', 'NYU Abu Dhabi': 'AE', 'Carnegie Mellon University Qatar': 'QA', 'Elsevier': 'NL', 'Kensho': 'US'})

# ---- load ---------------------------------------------------------------------------------
d = pd.read_csv(RAW, sep='\t', quoting=3)
d['org'] = d.sponsor.map(norm)
RANK = {'Diamond': 9, 'Platinum': 8, 'Gold': 7, 'Silver': 6, 'Bronze': 4, 'Supporter': 3, 'D&I': 2.5, 'Exhibitor': 2, 'Publisher': 1, 'Special': 0.5, 'Unspecified': 0}
assert set(d.tier) <= set(RANK), set(d.tier) - set(RANK)
d['rank'] = d.tier.map(RANK)
d = (d.sort_values('rank', ascending=False).drop_duplicates(['conference', 'year', 'org'])
       .sort_values(['conference', 'year', 'rank', 'org'], ascending=[True, True, False, True]))
d['sector'] = d.org.map(ai_meta.sector)
d['country'] = d.org.map(ai_meta.country)
d['parent_country'] = d.org.map(ai_meta.parent_country)

# ---- prices (USD; floor price of each tier) ---------------------------------------------------
T = lambda *v: dict(zip(['Diamond', 'Platinum', 'Gold', 'Silver', 'Bronze', 'Supporter'], v))
PRICES = {
    # ACL 2019 sponsorship booklet (one booklet for NAACL-HLT, ACL and EMNLP 2019)
    ('ACL', 2019): T(23775, 14500, 8000, 4400, 2400, 1280), ('EMNLP', 2019): T(20225, 12200, 6800, 3750, 2050, 1090), ('NAACL', 2019): T(15400, 9300, 5200, 2850, 1550, 850),
    ('ACL', 2020): T(30000, 18800, 10400, 5500, 3015, 1880), ('EMNLP', 2020): T(22000, 13500, 7500, 3900, 2130, 1340),
    ('ACL', 2021): T(30000, 20000, 10000, 6000, 3000, 2000), ('EMNLP', 2021): T(22000, 14000, 8000, 4000, 2000, 1500), ('NAACL', 2021): T(15000, 10000, 5000, 2500, 1250, 850),
    ('ACL', 2022): T(30000, 20000, 10000, 6000, 3000, 2000), ('EMNLP', 2022): T(30000, 20000, 10000, 6000, 3000, 2000), ('NAACL', 2022): T(22500, 15000, 7500, 4500, 2250, 1500),
    ('ACL', 2023): T(30000, 20000, 10000, 6000, 3000), ('EMNLP', 2023): T(30000, 20000, 10000, 6000, 3000),
    ('ACL', 2024): T(40000, 27500, 15000, 9000, 4500), ('EMNLP', 2024): T(40000, 27500, 15000, 9000, 4500), ('NAACL', 2024): T(30000, 20000, 10000, 6000, 3000),
    ('ACL', 2025): T(40000, 27500, 15000, 9000, 4500), ('EMNLP', 2025): T(40000, 27500, 15000, 9000, 4500), ('NAACL', 2025): T(30000, 20000, 10000, 6000, 3000),
    ('ACL', 2026): T(50000, 35000, 20000, 12000, 7500), ('EMNLP', 2026): T(50000, 35000, 20000, 12000, 7500),
}
SRCP = {2019: 'http://www.acl2019.org/medias/358-sponsorship-2019-booklet.pdf (archived)', 2020: 'https://acl2020.org/downloads/Sponsorship-2020-booklet.pdf',
        2021: 'https://2021.eacl.org/downloads/ACL-2021-Sponsorship-booklet.pdf', 2022: 'https://2022.naacl.org/downloads/Sponsorship-2022-booklet.pdf',
        2023: 'https://2023.aclweb.org/downloads/Sponsorship_Brochure-ACL2023-20230505.pdf',
        2024: 'https://2024.eacl.org/downloads/Sponsorship-brochure-for-ACL-2024-conferences-2023-12-19.pdf',
        2025: 'https://2025.aclweb.org/assets/Sponsorship brochure for ACL 2025 conferences - 2025-01-03.pdf',
        2026: 'https://2026.aclweb.org/assets/Sponsorship brochure for ACL 2026 Conferences - 2026-04-23.pdf'}
# years without a booklet reuse a nearby schedule
USE = {('ACL', 2018): ('ACL', 2019), ('EMNLP', 2018): ('EMNLP', 2019), ('NAACL', 2018): ('NAACL', 2019)}
SUPPORTER_FALLBACK = 2000   # 2023+ booklets no longer list a Supporter tier


def price(r):
    k = (r.conference, r.year) if (r.conference, r.year) in PRICES else USE.get((r.conference, r.year))
    if not k: return None, 'no price info'
    v = PRICES[k].get(r.tier)
    if v is None and r.tier == 'Supporter' and k[1] >= 2023: return SUPPORTER_FALLBACK, 'assumed (Supporter tier no longer listed)'
    if v is None: return None, 'tier not priced'
    return v, 'stated' if k == (r.conference, r.year) else f'assumed ({k[0]} {k[1]} schedule)'


pp = d.apply(price, axis=1, result_type='expand'); d['est_usd'] = pp[0]; d['price_basis'] = pp[1]

# sponsorship income reported by the ACL Sponsorship Director (main conference only, excludes workshops)
ACTUAL = {('ACL', 2022): 382000, ('NAACL', 2022): 278000, ('EMNLP', 2022): 400000, ('ACL', 2023): 557600, ('EMNLP', 2023): 481600}
ACTUAL_SRC = 'ACL admin wiki, Sponsorship Director reports 2023Q1 and 2024Q1'

LV = lambda t: 'unknown' if t == 'Unspecified' else 'top' if t in ('Diamond', 'Platinum') else 'mid' if t in ('Gold', 'Silver') else 'low'
d['tier_level'] = d.tier.map(LV)
d.insert(0, 'id', range(1, len(d) + 1))
cols = ['id', 'conference', 'year', 'tier', 'sponsor', 'org', 'sector', 'country', 'parent_country', 'tier_level', 'est_usd', 'price_basis', 'source']
d[cols].to_csv(os.path.join(OUT, 'nlp_sponsor_listings.csv'), index=False)

paid = ~d.tier.isin(['Special', 'Unspecified', 'Exhibitor', 'Publisher', 'D&I'])
pcy = d.groupby(['conference', 'year']).agg(n_sponsors=('org', 'nunique'),
        n_finance=('sector', lambda s: (s == 'Finance / quant').sum()),
        n_industry=('sector', lambda s: s.isin(['Finance / quant', 'Tech & other industry']).sum()),
        est_usd=('est_usd', 'sum'), priced=('est_usd', lambda s: s.notna().sum())).reset_index()
npaid = d[paid].groupby(['conference', 'year']).org.nunique()
pcy['est_usd'] = pcy.apply(lambda r: r.est_usd if r.priced >= 0.5 * npaid.get((r.conference, r.year), 0) and r.priced > 0 else None, axis=1)
pcy['reported_sponsor_income_usd'] = pcy.apply(lambda r: ACTUAL.get((r.conference, r.year)), axis=1)
pcy['attendance'] = None
pcy['usd_per_attendee'] = None
pcy.to_csv(os.path.join(OUT, 'nlp_per_conference_year.csv'), index=False)

top = (d.groupby('org').agg(sector=('sector', 'first'), country=('country', 'first'), appearances=('year', 'size'),
        conferences=('conference', lambda s: ', '.join(sorted(s.unique()))), first=('year', 'min'), last=('year', 'max'),
        est_usd=('est_usd', 'sum')).reset_index().sort_values(['appearances', 'est_usd'], ascending=False))
top.to_csv(os.path.join(OUT, 'nlp_top_sponsors.csv'), index=False)

pr = pd.DataFrame([{'conference': k[0], 'years': str(k[1]), 'tier': t, 'min_usd': v, 'basis': 'stated · ' + SRCP[k[1]]}
                   for k, m in sorted(PRICES.items(), key=lambda kv: (kv[0][1], kv[0][0])) for t, v in m.items()])
pr.insert(0, 'id', range(1, len(pr) + 1))
pr.to_csv(os.path.join(OUT, 'nlp_tier_prices.csv'), index=False)

if __name__ == '__main__':
    pd.set_option('display.width', 200)
    print(pcy.to_string()); print(top.head(30).to_string())
    print(d[d.country == 'US'].org.value_counts().index.tolist())
