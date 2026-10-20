import pandas as pd, json, re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from countries import country, parent_country
DATA = os.path.join(HERE, '..', 'data')
P = lambda *a: os.path.join(DATA, *a)

d = pd.read_csv(P('raw','sponsors_raw.csv'))
d = d[d.sponsor.notna()].copy()

# ---- normalise names ----
alias = {
    'Google DeepMind': 'Google', 'Microsoft': 'Microsoft', 'Oculus (Facebook)': 'Meta/Facebook', 'Bell Labs': 'Nokia Bell Labs', 'Intel ISTC-PC': 'Intel', 'Yahoo Labs': 'Yahoo/Verizon Media',
}
d['org'] = d.sponsor.replace(alias)
d['org'] = d.org.str.replace(r' \[.*\]$', '', regex=True)

# ---- sector classification ----
gov = {'NSF','NICT','ETRI','CSIRO Data61','Région Île-de-France','City of Yokohama','City of Espoo','Science Council of Japan',
       'Seoul Metropolitan Government','Korea Tourism Organization','VisitScotland','Singapore Tourism Board','GRAND NCE',
       'Digiteo','Inria','SICSA','KIPFA','work2future (San Jose)','Kayamori Foundation','Wellcome Trust',
       'TSV (Technology Industries of Finland Centennial Foundation)','Underwood Institute','Chen Institute','Language Grid',
       'MediaFutures (UiB)','Busan Tourism Organization','ERMES','Holden','GreenSense','EPSRC','CRA-W','User-Centric Networking (EU project)','TAF (Telecommunications Advancement Foundation)','SCAT','Osaka Convention & Tourism Bureau','IPSJ','Kansai METI','MIC Kinki Bureau of Telecommunications','Telecom Engineering Center Kinki','CKP (Ubiquitous Forum)','Human Interface Society','VRSJ','ZAI',
       # added with DIS / IUI / FAccT
       'Knight Foundation','MacArthur Foundation','Ford Foundation','Rockefeller Foundation','Sloan Foundation','Open Society Foundations','Schmidt Futures','Schmidt Sciences',
       'Luminate','Ethics and Governance of AI Initiative','Silicon Valley Community Foundation','Survival and Flourishing Fund','Athena Research Center','Tourisme Montréal',
       'Gesellschaft für Informatik (GI)','Cyprus Tourism Organisation','Business Events Sydney','Singapore Exhibition & Convention Bureau','Visit Brisbane','Visit Madeira',
       'Funchal City Council','HFESA','Australian Design Alliance','ANAT','Media Architecture Institute','Media Architecture Biennale'}
acad = {'University of Glasgow','University of Miami','Monash University','Yonsei University','Yonsei University ICS',
        'University of Toronto','Newcastle University','UMBC','UC Irvine','University of Maryland','Virginia Tech',
        'Université Paris-Dauphine','Telecom ParisTech','University of Michigan','University of Bari','University of Copenhagen DIKU',
        'IT University of Copenhagen','Northwestern University','Simon Fraser University','Drexel University','UCL',
        'University of Hawaii (HICHI)','University of Cambridge','Stevens Institute of Technology','MBZUAI',
        'Samsung Art and Design Institute','Hasso Plattner Institute','Georgia Tech','University of Cambridge','University of Toronto','UC San Diego','Dong-eui University','University of Virginia','UC San Diego (Qualcomm Institute)','University of Rochester','UNC Charlotte','Carnegie Mellon University','SAT (Société des arts technologiques)',
        'Vector Institute','RC Trust','Archimedes (Athena RC)','Texas A&M University','University of Cyprus','Rochester Institute of Technology','Deakin University',
        'Queensland University of Technology','ITI / LARSyS','NUS Division of Industrial Design'}
pub = {'Elsevier','Springer','Frontiers','eLearn Magazine (ACM)','ACM Interactions','MIT Press','Morgan & Claypool','MDPI','Science Robotics (AAAS)','AI Journal (AIJ)'}
def sector(o):
    if o in gov: return 'Government / foundation'
    if o in acad: return 'University / academic'
    if o in pub: return 'Publisher'
    if o.startswith('SCI'): return 'Unknown'
    return 'Industry'
d['sector'] = d.org.map(sector)

# ---- tier price schedules (USD, lower bound of tier) ----
def price(row):
    c, y, t = row.conference, row.year, row.tier
    if c == 'CHI':
        if y < 2006: return None, 'no price info'
        tbl = {'Hero':50000,'Champion':25000,'Contributor':10000,'Friend':1000}
        src = 'stated' if y in (2016,2021,2024,2025,2026) else 'assumed (CHI 2016–2026 schedule)'
        return tbl.get(t), src if t in tbl else 'n/a'
    if c == 'CSCW':
        if y <= 2022:
            tbl = {'Hero':15000,'Champion':15000,'Benefactor':10000,'Contributor':5000,'Friend':1000,'DC Supporter':1000}
            src = 'stated' if y in (2016,2018,2019) else 'assumed (CSCW 2016–2019 schedule)'
            if t == 'Unspecified': return None, 'tier not listed'
            return tbl.get(t), src
        if y in (2023, 2024):
            return 1000, 'assumed floor (no published price)'
        if y == 2025:
            tbl = {'Platinum':13000,'Gold':6250,'Silver':3000,'Bronze':1500,'Supporter':750}
            return tbl.get(t), 'stated'
        if y == 2026:
            tbl = {'Platinum':15000,'Gold':10000,'Silver':5000,'Bronze':3000,'Friend':2000,'Supporter':1000}
            return tbl.get(t), 'stated'
    if c == 'UIST':
        if y == 2007:
            tbl = {'Anniversary Champion':20000,'Champion':10000,'Benefactor':5000,'Donor':2500}; return tbl.get(t),'stated'
        if y <= 2016:
            tbl = {'Champion':20000,'Platinum':15000,'Gold':10000,'Silver':5000,'Bronze':2500,'Friend':1000,'Institution':1000}
            if y == 2008: tbl['Platinum']=20000
            return tbl.get(t), 'stated' if y in (2008,2011,2012,2015) else 'assumed (UIST 2015 schedule)'
        tbl = {'Platinum':20000,'Gold':15000,'Silver':10000,'Bronze':5000,'Exhibitor':3000,'Friend':1000}
        return tbl.get(t), 'stated' if y in (2017,2020,2022,2023,2024,2025) else 'assumed (UIST 2017–2025 schedule)'
    if c == 'UbiComp':
        if t in ('Unspecified','Special'): return None, 'tier not listed'
        if y in (2013,2014): tbl={'Gold':12000,'Silver':8000,'Bronze':4000}; return tbl.get(t),'stated' if y==2014 else 'assumed (UbiComp 2014 schedule)'
        if y in (2015,2016,2017,2018): tbl={'Platinum':15000,'Gold':10000,'Silver':5000,'Bronze':3000}; return tbl.get(t),'stated' if y!=2016 else 'assumed (2015 schedule)'
        if y == 2019: tbl={'Platinum':20000,'Gold':15000,'Silver':10000,'Bronze':5000}; return tbl.get(t),'stated'
        tbl={'Platinum':15000,'Gold':10000,'Silver':5000,'Bronze':2500,'Startup':1000}
        return tbl.get(t), 'stated' if y in (2022,2023) else 'assumed (UbiComp 2022–23 schedule)'
    if c == 'IUI':
        if t not in ('Platinum','Gold','Silver','Bronze'): return None, 'tier not listed'
        if y in (2015, 2016): tbl = {'Platinum':8000,'Gold':5000,'Silver':2500,'Bronze':1000}; return tbl[t], 'stated' if y == 2016 else 'assumed (IUI 2016 schedule)'
        if y == 2017: tbl = {'Platinum':7900,'Gold':4500,'Silver':2250,'Bronze':1100}; return tbl[t], 'stated in EUR (7k/4k/2k/1k), ×1.13'
        if y == 2021: tbl = {'Platinum':5000,'Gold':2500,'Silver':1000}; return tbl.get(t), 'stated'
        tbl = {'Platinum':10000,'Gold':5000,'Silver':2500,'Bronze':1000}
        return tbl[t], 'stated' if y in (2018,2019,2020,2022,2023,2024,2025) else 'assumed (IUI 2025 schedule)'
    if c == 'DIS':
        if y == 2019:
            tbl = {'Platinum':10000,'Silver':5000,'Friend':1000}; return tbl.get(t), 'stated'
        return None, 'no price info'
    if c == 'FAccT':
        if t != 'Unspecified': return None, 'n/a'
        if y >= 2023: return 10000, 'assumed floor (lowest published tier $10k; tiers not shown)'
        return 5000, 'assumed floor (lowest published tier $5k; tiers not shown)'
    return None, 'n/a'

pp = d.apply(price, axis=1, result_type='expand'); d['est_usd'] = pp[0]; d['price_basis'] = pp[1]

# exclude non-monetary / special-support rows from $ (keep in counts)
d.loc[d.tier.isin(['Special','Corporate','Contest Sponsor','Supporter (host)']), 'est_usd'] = None

# ---- attendance ----
att = {
 'CHI': {1996:2344,1998:2310,2006:2250,2007:2620,2008:2361,2009:2358,2010:2384,2011:2861,2012:2616,2013:3443,2014:3001,2015:2896,2016:3624,2017:2939,2018:3182,2019:3759,
         2020:3209,2021:5145,2022:4001,2023:4721,2024:4120,2025:5675},
 'CSCW': {2013:437,2014:505,2015:590,2016:757,2017:707,2018:783},
 'UIST': {2011:284,2012:410,2013:411,2014:461,2015:347,2016:648,2017:387,2018:560,2019:498},
 'UbiComp': {2011:383,2012:390,2013:730,2014:818,2016:601,2017:568,2018:755,2019:700},
}

# ---- outputs ----
d['country'] = d.org.map(country)
d['parent_country'] = d.org.map(parent_country)
listings = d[['conference','year','tier','sponsor','org','sector','est_usd','price_basis','source','country','parent_country']].copy()
listings.insert(0, 'id', range(1, len(listings) + 1))
listings.to_csv(P('sponsor_listings.csv'), index=False)

top = (d.groupby(['org','sector']).agg(appearances=('year','size'),
        conferences=('conference', lambda s: ', '.join(sorted(s.unique()))),
        est_usd=('est_usd','sum'), first=('year','min'), last=('year','max')).reset_index()
        .sort_values(['appearances','est_usd'], ascending=False))
top.to_csv(P('top_sponsors.csv'), index=False)

pcy = (d.groupby(['conference','year']).agg(n_sponsors=('org','nunique'),
        n_industry=('sector', lambda s: (s == 'Industry').sum()),
        est_usd=('est_usd','sum'), priced=('est_usd', lambda s: s.notna().sum())).reset_index())
# only report an estimate when at least half of the monetary listings have a known tier price
nonmon = {'Supporter','Special','Supporter (host)','Contest Sponsor','Corporate'}
mon = listings[~(listings.tier.isin(nonmon) & (listings.conference != 'CSCW'))]
den = mon.groupby(['conference','year']).size().rename('den').reset_index()
pcy = pcy.merge(den, on=['conference','year'], how='left')
bad = (pcy.priced == 0) | pcy.den.isna() | ((pcy.priced / pcy.den) < 0.5)
pcy.loc[bad, 'est_usd'] = float('nan')
pcy['attendance'] = pcy.apply(lambda r: att.get(r.conference, {}).get(r.year), axis=1)
pcy['usd_per_attendee'] = pcy.est_usd / pcy.attendance
pcy['key'] = pcy.conference + '-' + pcy.year.astype(str)
pcy[['conference','year','n_sponsors','n_industry','est_usd','priced','attendance','usd_per_attendee','key']].round(1).to_csv(P('per_conference_year.csv'), index=False)
print(f"{len(listings)} listings, {d.org.nunique()} organisations, {len(pcy)} conference-years")
