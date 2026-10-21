"""Generate dashboard/nlp/index.html (ACL / EMNLP / NAACL) from the HCI page,
so all pages share one layout, style and set of controls.

    python scripts/make_nlp_page.py

It swaps in the NLP conferences, sectors, headline numbers, notes, summary and
method text, replaces the per-attendee chart (NLP attendance is not published
consistently) with a check of the estimates against reported sponsorship
income, and adds a section comparing NLP with ML and HCI sponsorship.
"""
import os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = os.path.join(ROOT, 'dashboard', 'index.html')
OUT = os.path.join(ROOT, 'dashboard', 'nlp', 'index.html')
L = lambda en, zh: f'<span lang="en">{en}</span><span lang="zh">{zh}</span>'

s = open(SRC, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:90])
    s = s.replace(a, b)


def sub(pattern, b):
    global s
    s, k = re.subn(pattern, lambda m: b, s, count=1, flags=re.S)
    assert k == 1, pattern[:90]


def note(section_id, en, zh):
    global s
    m = re.search(r'<h2 id="' + section_id + r'">.*?</h2>\s*<p class="note">(.*?)</p>', s, re.S)
    assert m, section_id
    s = s[:m.start(1)] + L(en, zh) + s[m.end(1):]


# ---- header -----------------------------------------------------------------
rep(L('Who Sponsors HCI Conferences', '谁在赞助 HCI 会议'), L('Who Sponsors NLP Conferences', '谁在赞助自然语言处理会议'))
rep('CHI · CSCW · UIST · UbiComp · DIS · IUI · FAccT · AIES</p>', 'ACL · EMNLP · NAACL</p>')
rep(L('Who pays for the main HCI conferences, and how that has changed over the years. The sponsor lists were compiled by hand from each conference’s website.',
      '谁在为主要的 HCI 会议出钱，以及这些年的变化。赞助商名单根据各会议官网手工整理。'),
    L('Who pays for the three main natural-language-processing conferences, and how that compares with machine learning and HCI. The sponsor lists come from each conference’s website and its archived copies.',
      '谁在为三大自然语言处理会议出钱，以及和机器学习、HCI 会议相比有何不同。赞助商名单来自各会议官网及其存档。'))
rep('<button data-v="2006"><span lang="en">2006+</span><span lang="zh">2006 起</span></button>',
    '<button data-v="2018"><span lang="en">2018+</span><span lang="zh">2018 起</span></button>')

# ---- contents rail ---------------------------------------------------------------
rep('<li><a href="#per-attendee" data-target="per-attendee">' + L('Per attendee', '人均赞助额') + '</a></li>',
    '<li><a href="#check" data-target="check">' + L('Estimates vs reported', '估算与实际收入') + '</a></li>')
rep('      <li><a href="#summary" data-target="summary">',
    '      <li><a href="#vs-others" data-target="vs-others">' + L('Compared with ML and HCI', '和机器学习、HCI 会议比') + '</a></li>\n      <li><a href="#summary" data-target="summary">')

# ---- notes --------------------------------------------------------------------
note('timeline',
     'One row per organization, one column per year. A filled cell means the organization sponsored that year; darker means a higher tier (Diamond or Platinum / Gold or Silver / Bronze and others; ACL 2016 lists no tiers). Grey columns are years with no edition or no sponsor list: NAACL was not held in 2014, 2017, 2020, 2023 or 2026. Sorting by last appearance puts current sponsors at the top.',
     '每行一家机构，每列一年；有色格子表示当年赞助，颜色越深等级越高（Diamond/Platinum、Gold/Silver、Bronze 及其他；ACL 2016 没标等级）。灰色列是当年没有举办或没拿到名单：NAACL 在 2014、2017、2020、2023、2026 年没有举办。按“最后出现”排序时，最近仍在赞助的机构排在最上面。')
note('by-conference',
     'For the selected years, organizations ranked by how many editions they sponsored (one count per organization per edition). Pick a conference or all three together, and how many to show. The label shows editions and the year span; hover for tiers and estimated totals.',
     '所选年份内，按赞助届数给机构排名（同一机构在一届会议计 1 次）。可以选单个会议或三个会议合计，以及显示前几名。右侧是届数和年份跨度，悬停查看各等级次数和估算金额。')
note('countries',
     'Each cell is the share of a conference’s sponsors (organization × edition, selected years) that come from that country; the number is the count. Darker means a larger share. Host effects show up too: Thai sponsors at ACL 2021 and 2024 (Bangkok), Gulf institutions at EMNLP 2014 (Doha) and 2022 (Abu Dhabi).',
     '每格是该会议（所选年份内的“机构 × 届次”）中来自该国家/地区的比例，格内数字是条数，颜色越深占比越高。也能看到东道主效应：ACL 2021、2024（曼谷）的泰国赞助方，EMNLP 2014（多哈）和 2022（阿布扎比）的海湾国家机构。')
note('sectors',
     'Share of each conference’s sponsor listings by type of organization, for the selected years. Finance includes trading firms, banks and financial data companies (Bloomberg, Two Sigma, Capital One, JPMorgan Chase).',
     '所选年份内，各会议赞助条目按机构类型的占比。“金融 / 量化”包括交易公司、银行和金融数据公司（Bloomberg、Two Sigma、Capital One、JPMorgan Chase）。')
note('money',
     'Each sponsor is counted at its tier’s published price and summed per edition. ACL, EMNLP and NAACL share one sponsorship program with booklets from 2019 on; 2018 reuses the 2019 prices, and earlier years are not estimated. Multi-conference packages are discounted, so a few sponsors paid less than the single-conference price.',
     '每家赞助商按其等级的公开价计，加总得到每届的估算。ACL、EMNLP、NAACL 共用一套赞助方案，2019 年起有招商手册；2018 年沿用 2019 年价格，更早的年份不估算。多会议打包有折扣，所以少数赞助商实际付款低于单会议价格。')
rep(L('Estimated sponsorship per edition (lower bound)', '每届估算赞助额（下限）'), L('Estimated sponsorship per edition', '每届估算赞助额'))
rep("H.T(`Estimated total (lower bound): ${H.fmtUSD(d.est)}`, `估算下限合计：${H.fmtUSD(d.est)}`)", "H.T(`Estimated total: ${H.fmtUSD(d.est)}`, `估算合计：${H.fmtUSD(d.est)}`)")
rep("H.T(`Estimate (lower bound): ${H.fmtUSD(d.v)}`, `估算下限 ${H.fmtUSD(d.v)}`)", "H.T(`Estimate: ${H.fmtUSD(d.v)}`, `估算 ${H.fmtUSD(d.v)}`)")
rep('<span lang="en">Only prices found on official sites or sponsor prospectuses. Each tier is a floor price; actual amounts may be higher.</span><span lang="zh">只列官网/招商书上能找到的价目；每个等级是“起步价”，实际金额可能更高。</span>',
    L('From the ACL sponsorship booklets, which price each conference separately. From 2023 the booklets no longer list a Supporter tier; this site assumes $2,000 for it.',
      '来自 ACL 的赞助手册，每个会议单独定价。2023 年起手册不再列 Supporter 等级，本站按 $2,000 计。'))

# ---- per-attendee card -> estimates vs reported income -----------------------------
m = re.search(r'      <h2 id="per-attendee">.*?<div id="c-pa" data-source="pcy" style="min-height:240px"></div>', s, re.S)
assert m
s = s[:m.start()] + f'''      <h2 id="check">{L('Do the estimates hold up?', '估算靠谱吗？')}</h2>
      <p class="note">{L('For five editions the ACL sponsorship director reported the income actually raised (main conference, excluding workshops). Bars are this site’s estimates; dots are the reported figures.',
                         'ACL 赞助主管的报告给出了五届会议的实际赞助收入（主会，不含 workshop）。柱子是本站估算，圆点是报告的数字。')}</p>
      <div class="legend" id="lg-conf"></div>
      <div id="c-pa" data-source="pcy" style="min-height:240px"></div>''' + s[m.end():]

# ---- constants ------------------------------------------------------------------
rep("const CONF = ['CHI','CSCW','UIST','UbiComp','DIS','IUI','FAccT','AIES'];",
    "const CONF = ['ACL','EMNLP','NAACL'];\nconst MCONF = ['NeurIPS','ICML','ICLR'];\nconst HCONF = ['CHI','CSCW','UIST','UbiComp'];")
rep("window.HX = {C, T, cc, CONF,", "window.HX = {C, T, cc, CONF, MCONF, HCONF,")
sub(r"const SECT = \[.*?\];", "const SECT = ['Tech & other industry','Finance / quant','Government / academic / non-profit','Publisher'];")
sub(r"const SECT_ZH0 = \{.*?\};", "const SECT_ZH0 = {'Tech & other industry':'科技及其他企业','Finance / quant':'金融 / 量化','Government / academic / non-profit':'政府 / 学术 / 非营利','Publisher':'出版社'};")
sub(r"const SECT_EN0 = \{.*?\};", "const SECT_EN0 = {'Tech & other industry':'Tech and other companies','Finance / quant':'Finance / quant','Government / academic / non-profit':'Government / academic / non-profit','Publisher':'Publisher'};")
EXTRA_ZH = "RU:'俄罗斯',SA:'沙特阿拉伯',IL:'以色列',TH:'泰国',BG:'保加利亚',BE:'比利时',QA:'卡塔尔',PL:'波兰',HK:'中国香港',SV:'萨尔瓦多','??':'未知',"
EXTRA_EN = "RU:'Russia',SA:'Saudi Arabia',IL:'Israel',TH:'Thailand',BG:'Bulgaria',BE:'Belgium',QA:'Qatar',PL:'Poland',HK:'Hong Kong',SV:'El Salvador','??':'Unknown',"
rep("const CTY_ZH0 = {", "const CTY_ZH0 = {" + EXTRA_ZH)
rep("const CTY_EN0 = {", "const CTY_EN0 = {" + EXTRA_EN)

# ---- headline numbers -----------------------------------------------------------
sub(r"dash\.calc\('kpis', \{.*?\n\}\);\n\ndash\.calc\('cscw_trend', \{.*?\n\}\);", """dash.calc('kpis', {
  inputs: ['listings', 'ml_listings', 'hci_listings'], title: 'Headline counts (all years)',
  description: 'Counts listings, distinct organisations, conference-years and HQ countries; share of 2022–2026 listings from mainland China in NLP, ML and HCI; share of NLP listings from finance.',
  fn: (listings, ml, hci) => {
    const cn = rows => { const r = rows.filter(x => +x.year >= 2022); return Math.round(100 * r.filter(x => x.country === 'CN').length / r.length) + '%'; };
    return [
      {metric:'listings', value: String(listings.length)},
      {metric:'orgs', value: String(new Set(listings.map(r => r.org)).size)},
      {metric:'confyears', value: String(new Set(listings.map(r => r.conference + '-' + r.year)).size)},
      {metric:'countries', value: String(new Set(listings.map(r => r.country).filter(c => c && c !== '??' && c !== 'EU')).size)},
      {metric:'cn_nlp', value: cn(listings)},
      {metric:'cn_ml', value: cn(ml)},
      {metric:'cn_hci', value: cn(hci.filter(r => ['CHI','CSCW','UIST','UbiComp'].includes(r.conference)))},
      {metric:'finshare', value: Math.round(100 * listings.filter(r => r.sector === 'Finance / quant').length / listings.length) + '%'},
    ];
  }
});

dash.calc('money_cmp', {
  inputs: ['pcy', 'ml_pcy', 'hci_pcy'], title: 'Estimated sponsorship, 2018 vs 2025',
  description: 'Estimated sponsorship for ACL 2018 and 2025, NeurIPS 2025 and CHI 2025, from published tier prices.',
  fn: (pcy, ml, hci) => {
    const v = (rows, c, y) => { const r = rows.find(x => x.conference === c && +x.year === y); return r && r.est_usd !== '' ? +r.est_usd : null; };
    const f = x => x == null ? '—' : x >= 1e6 ? '$' + (x / 1e6).toFixed(1) + 'M' : '$' + Math.round(x / 1000) + 'k';
    return [{metric:'acl2018', value: f(v(pcy, 'ACL', 2018))}, {metric:'acl2025', value: f(v(pcy, 'ACL', 2025))},
            {metric:'neurips2025', value: f(v(ml, 'NeurIPS', 2025))}, {metric:'chi2025', value: f(v(hci, 'CHI', 2025))}];
  }
});""")
rep("['kpis','cscw_trend'].forEach(id => {\n    const st = dash.data(id); const k = id === 'kpis' ? 'metric' : 'period';",
    "['kpis','money_cmp'].forEach(id => {\n    const st = dash.data(id); const k = 'metric';")

# ---- timeline levels by tier name ---------------------------------------------------
rep("const LEVELS = [['high', '≥ $20k', 1], ['mid', '$5k–20k', 0.6], ['low', '< $5k', 0.3], ['unknown', null, 0]];",
    "const LEVELS = [['high', 'Diamond / Platinum', 1], ['mid', 'Gold / Silver', 0.6], ['low', null, 0.3], ['unknown', null, 0]];")
rep("sp.append(i, lab || H.T('Price unknown', '价格未知')); lg.append(sp);",
    "sp.append(i, lab || (k === 'low' ? H.T('Bronze and others', 'Bronze 及其他') : H.T('No tier listed', '未标等级'))); lg.append(sp);")
rep("let conf = 'CSCW', sort = 'last', all = false;", "let conf = 'ACL', sort = 'last', all = false;")
rep("const level = r => r.est_usd === '' ? 'unknown' : +r.est_usd >= 20000 ? 'high' : +r.est_usd >= 5000 ? 'mid' : 'low';",
    "const level = r => ({top: 'high', mid: 'mid', low: 'low'})[r.tier_level] || 'unknown';")
rep("H.T('Price unknown', '价格未知') : H.T(`Floor price ${H.fmtUSD(+d.est_usd)}`, `起步价 ${H.fmtUSD(+d.est_usd)}`)",
    "H.T('No price for that year', '没有当年价目') : H.T(`Estimate ${H.fmtUSD(+d.est_usd)}`, `估算 ${H.fmtUSD(+d.est_usd)}`)")
rep('<div class="tlbox"><div id="c-tl"', '<div class="tlbox" style="max-height:44rem;overflow:auto"><div id="c-tl"')

# ---- top sponsors, countries -----------------------------------------------------------
rep("e.textContent = 'All eight';", "e.textContent = 'All three';")
rep("z.textContent = '八个会议合计';", "z.textContent = '三个会议合计';")
rep("const unknown = by.find(d => !d.cc);\n  const known = by.filter(d => d.cc);",
    "const unknown = by.find(d => !d.cc || d.cc === '??');\n  const known = by.filter(d => d.cc && d.cc !== '??');")

# ---- money tooltip: reported income instead of registrations -----------------------------
rep("d.attendance ? H.T(`${d3.format(',')(+d.attendance)} registrations`, `注册 ${d3.format(',')(+d.attendance)} 人`) : H.T('Registrations not published', '注册人数未公开')",
    "d.reported_sponsor_income_usd ? H.T(`Reported income: ${H.fmtUSD(+d.reported_sponsor_income_usd)}`, `报告的实际收入 ${H.fmtUSD(+d.reported_sponsor_income_usd)}`) : ''")
rep("['', H.T(`${d.n_sponsors} sponsors (${d.n_industry} companies)`, `${d.n_sponsors} 家赞助方（企业 ${d.n_industry}）`)], ['', d.reported",
    "['', H.T(`${d.n_sponsors} sponsors (${d.n_industry} companies)`, `${d.n_sponsors} 家赞助方（企业 ${d.n_industry}）`)], ...(d.reported_sponsor_income_usd ? [['', d.reported")
rep("`报告的实际收入 ${H.fmtUSD(+d.reported_sponsor_income_usd)}`) : '']]))",
    "`报告的实际收入 ${H.fmtUSD(+d.reported_sponsor_income_usd)}`) : '']] : [])]))")

# ---- per-attendee script -> estimate check -------------------------------------------------
m = re.search(r'// per attendee\nwindow\.HX\.on\(\(\) => \{.*?\n\}\);\n(?=</script>)', s, re.S)
assert m
CHECK_JS = r'''// estimates vs reported income
window.HX.on(() => {
  const H = window.HX;
  const el = document.getElementById('c-pa'), lg = document.getElementById('lg-conf'); const st = dash.data('pcy');
  lg.replaceChildren(); if (H.failOrWait(el, st)) return;
  const rows = st.data.filter(r => r.reported_sponsor_income_usd !== '' && r.est_usd !== '').map(r => ({c: r.conference, y: +r.year, est: +r.est_usd, rep: +r.reported_sponsor_income_usd}))
    .sort((a, b) => a.y - b.y || H.CONF.indexOf(a.c) - H.CONF.indexOf(b.c));
  H.legend(lg, [[H.C[0], H.T('Estimate from tier prices', '按等级价估算')], ['var(--color-fg)', H.T('Reported income', '报告的实际收入')]]);
  const W = el.clientWidth || 500, Ht = 240, m = {l: 44, r: 8, t: 10, b: 36};
  const svg = d3.select(el).append('svg').attr('width', '100%').attr('viewBox', `0 0 ${W} ${Ht}`);
  if (!rows.length) return;
  const key = d => `${d.c} ${d.y}`;
  const x = d3.scaleBand(rows.map(key), [m.l, W - m.r]).padding(0.35);
  const y = d3.scaleLinear([0, d3.max(rows, r => Math.max(r.est, r.rep)) * 1.1], [Ht - m.b, m.t]).nice();
  svg.append('g').selectAll('line').data(y.ticks(4)).join('line').attr('x1', m.l).attr('x2', W - m.r).attr('y1', d => y(d)).attr('y2', d => y(d)).attr('stroke', 'var(--cds-chart-grid)');
  svg.append('g').attr('transform', `translate(${m.l},0)`).call(d3.axisLeft(y).ticks(4).tickSize(0).tickFormat(H.fmtK)).attr('font-size', null).attr('font-family', null)
    .call(g => { g.select('.domain').remove(); g.selectAll('text').attr('fill', 'var(--color-fg-muted)').attr('font-size', 10); });
  svg.append('g').attr('transform', `translate(0,${Ht - m.b})`).call(d3.axisBottom(x).tickSize(0)).attr('font-size', null).attr('font-family', null)
    .call(g => { g.select('.domain').attr('stroke', 'var(--cds-chart-axis)'); g.selectAll('text').attr('fill', 'var(--color-fg-muted)').attr('font-size', 10).attr('dy', '1em')
      .each(function () { const t = d3.select(this), [c, yy] = t.text().split(' '); t.text(null); t.append('tspan').attr('x', 0).text(c); t.append('tspan').attr('x', 0).attr('dy', '1.15em').text(yy); }); });
  const g = svg.append('g').selectAll('g').data(rows).join('g');
  g.append('rect').attr('x', d => x(key(d))).attr('width', x.bandwidth()).attr('y', d => y(d.est)).attr('height', d => y(0) - y(d.est)).attr('rx', 3).attr('fill', d => H.C[H.CONF.indexOf(d.c)]).attr('opacity', 0.85);
  g.append('line').attr('x1', d => x(key(d)) - 4).attr('x2', d => x(key(d)) + x.bandwidth() + 4).attr('y1', d => y(d.rep)).attr('y2', d => y(d.rep)).attr('stroke', 'var(--color-fg)').attr('stroke-width', 1.5);
  g.append('circle').attr('cx', d => x(key(d)) + x.bandwidth() / 2).attr('cy', d => y(d.rep)).attr('r', 4).attr('fill', 'var(--color-fg)').attr('stroke', 'var(--color-bg)').attr('stroke-width', 1.5);
  g.append('rect').attr('x', d => x(key(d)) - x.step() * x.paddingInner() / 2).attr('width', x.step()).attr('y', m.t).attr('height', Ht - m.t - m.b).attr('fill', 'transparent')
    .on('mousemove', (ev, d) => H.showTip(ev, [['t', key(d)], ['', H.T(`Estimate: ${H.fmtUSD(d.est)}`, `估算 ${H.fmtUSD(d.est)}`)], ['', H.T(`Reported: ${H.fmtUSD(d.rep)}`, `报告 ${H.fmtUSD(d.rep)}`)],
      ['', H.T(`Estimate is ${d3.format('+.0%')(d.est / d.rep - 1)} off`, `估算偏差 ${d3.format('+.0%')(d.est / d.rep - 1)}`)]])).on('mouseleave', H.hideTip);
});
'''
s = s[:m.start()] + CHECK_JS + s[m.end():]

# ---- summary -----------------------------------------------------------------------------
m_ = lambda w: f'<b data-source="money_cmp" data-field="value" data-where="metric={w}" class="dash-skeleton">—</b>'
k_ = lambda w: f'<b data-source="kpis" data-field="value" data-where="metric={w}" class="dash-skeleton">—</b>'
m = re.search(r'(<h2 id="summary">.*?</h2>\n)(.*?)(  </section>)', s, re.S)
summary = f'''    <ul class="summary" lang="en">
        <li><strong>Between HCI and ML in size, and growing.</strong> At published tier prices ACL went from about {m_("acl2018")} in 2018 to {m_("acl2025")} in 2025. That is close to what the ACL reports actually raising, but still far below NeurIPS ({m_("neurips2025")}) and well above CHI ({m_("chi2025")}).</li>
        <li><strong>Many more Chinese sponsors.</strong> Since 2022, {k_("cn_nlp")} of NLP sponsor listings come from mainland Chinese companies (Baidu, ByteDance, Alibaba, Ant Group, Tencent, Meituan, Xiaomi), against {k_("cn_ml")} at the ML conferences and {k_("cn_hci")} at CHI, CSCW, UIST and UbiComp.</li>
        <li><strong>A field with its own industry.</strong> Besides the big tech companies, language-technology firms sponsor year after year: Grammarly, Babelscape, Nuance, Duolingo, Translated, LivePerson and ASAPP, and data vendors such as DataOcean AI, Appen and Toloka. Finance makes up {k_("finshare")} of listings, led by Bloomberg.</li>
    </ul>
    <ul class="summary" lang="zh">
        <li><strong>规模介于 HCI 和机器学习之间，并且在增长。</strong>按公开等级价估算，ACL 从 2018 年的约 {m_("acl2018")} 增长到 2025 年的 {m_("acl2025")}，和 ACL 报告的实际收入相当接近；但仍远低于 NeurIPS（{m_("neurips2025")}），远高于 CHI（{m_("chi2025")}）。</li>
        <li><strong>中国企业多得多。</strong>2022 年以来，NLP 会议的赞助条目中有 {k_("cn_nlp")} 来自中国大陆企业（百度、字节、阿里、蚂蚁、腾讯、美团、小米），机器学习会议是 {k_("cn_ml")}，CHI、CSCW、UIST、UbiComp 只有 {k_("cn_hci")}。</li>
        <li><strong>有自己的一批行业赞助方。</strong>除了大科技公司，语言技术公司年年赞助：Grammarly、Babelscape、Nuance、Duolingo、Translated、LivePerson、ASAPP，还有数据服务商 DataOcean AI、Appen、Toloka。金融机构占 {k_("finshare")}，以 Bloomberg 为首。</li>
    </ul>
'''
s = s[:m.start(2)] + summary + s[m.end(2):]

# ---- comparison section, before the summary ------------------------------------------------------
cmp = f'''  <section class="card" id="vs-card">
    <h2 id="vs-others">{L('Compared with ML and HCI', '和机器学习、HCI 会议比')}</h2>
    <p class="note">{L('Left: sponsors per edition (each organization once); solid lines are the NLP conferences, dashed lines NeurIPS and CHI, the largest conference in each of the other two fields. Right: share of sponsor listings from mainland China, per year, for each field.',
                       '左：每届赞助方数量（同一机构在一届只计 1 次），实线是 NLP 会议，虚线是另外两个领域各自最大的会议 NeurIPS 和 CHI。右：每年赞助条目中来自中国大陆的比例，按领域分。')}</p>
    <div class="grid" style="gap:2.5rem">
      <div><div class="legend" id="lg-cmp"></div><div id="c-cmp" data-source="pcy ml_pcy hci_pcy" style="min-height:260px"></div></div>
      <div><div class="legend" id="lg-cn"></div><div id="c-cn" data-source="listings ml_listings hci_listings" style="min-height:260px"></div></div>
    </div>
    <p class="note" style="margin-top:2rem">{L('Companies that sponsor NLP and at least one of the other two fields, by the number of editions they sponsored in each (selected years). HCI counts CHI, CSCW, UIST and UbiComp.',
                       '赞助 NLP 会议、并至少赞助过另外一个领域的企业，以及在所选年份内各领域赞助的届数。HCI 只计 CHI、CSCW、UIST、UbiComp。')}</p>
    <div class="legend" id="lg-ov"></div><div id="c-ov" data-source="listings ml_listings hci_listings" style="min-height:420px"></div>
  </section>

'''
rep('  <section class="card" id="summary-card">', cmp + '  <section class="card" id="summary-card">')

CMP_JS = r'''
<script>
// NLP vs ML vs HCI: sponsors per edition
window.HX.on(() => {
  const H = window.HX;
  const el = document.getElementById('c-cmp'), lg = document.getElementById('lg-cmp');
  const sts = ['pcy', 'ml_pcy', 'hci_pcy'].map(k => dash.data(k));
  const st = sts.find(x => x.status !== 'ok') || sts[0]; lg.replaceChildren();
  if (H.failOrWait(el, st)) return;
  const ALL = [...H.CONF, 'NeurIPS', 'CHI'];
  const col = c => H.C[ALL.indexOf(c)];
  const rows = sts.flatMap(x => x.data).filter(r => ALL.includes(r.conference) && +r.year >= 2013 && H.inRange(r.year)).map(r => ({c: r.conference, y: +r.year, v: +r.n_sponsors}));
  H.legend(lg, ALL.filter(c => rows.some(r => r.c === c)).map(c => [col(c), c]));
  const W = el.clientWidth || 500, Ht = 260, m = {l: 34, r: 64, t: 10, b: 24};
  const svg = d3.select(el).append('svg').attr('width', '100%').attr('viewBox', `0 0 ${W} ${Ht}`);
  if (!rows.length) { svg.append('text').attr('y', 14).attr('font-size', 12).attr('fill', 'var(--color-fg-muted)').text(H.T('No data in the selected years', '所选年份内没有数据')); return; }
  const ext = d3.extent(rows, r => r.y); if (ext[0] === ext[1]) { ext[0] -= 1; ext[1] += 1; }
  const x = d3.scaleLinear(ext, [m.l, W - m.r]);
  const y = d3.scaleLinear([0, d3.max(rows, r => r.v) * 1.08], [Ht - m.b, m.t]).nice();
  svg.append('g').selectAll('line').data(y.ticks(5)).join('line').attr('x1', m.l).attr('x2', W - m.r).attr('y1', d => y(d)).attr('y2', d => y(d)).attr('stroke', 'var(--cds-chart-grid)');
  svg.append('g').attr('transform', `translate(${m.l},0)`).call(d3.axisLeft(y).ticks(5).tickSize(0)).attr('font-size', null).attr('font-family', null)
    .call(g => { g.select('.domain').remove(); g.selectAll('text').attr('fill', 'var(--color-fg-muted)').attr('font-size', 10); });
  svg.append('g').attr('transform', `translate(0,${Ht - m.b})`).call(d3.axisBottom(x).tickValues(x.ticks(Math.min(8, Math.floor(W / 60))).filter(Number.isInteger)).tickFormat(d3.format('d')).tickSize(0)).attr('font-size', null).attr('font-family', null)
    .call(g => { g.select('.domain').attr('stroke', 'var(--cds-chart-axis)'); g.selectAll('text').attr('fill', 'var(--color-fg-muted)').attr('font-size', 10).attr('dy', '1em'); });
  const ends = [];
  ALL.forEach(c => {
    const s = rows.filter(r => r.c === c).sort((p, q) => p.y - q.y); if (!s.length) return;
    const other = !H.CONF.includes(c);
    // NAACL skips years, so only join consecutive editions of the annual conferences
    const gap = c === 'NAACL' ? 3 : 1;
    svg.append('path').datum(s).attr('fill', 'none').attr('stroke', col(c)).attr('stroke-width', other ? 1.5 : 2).attr('stroke-dasharray', other ? '4 3' : null)
      .attr('d', d3.line(d => x(d.y), d => y(d.v)).defined((d, i) => i === 0 || d.y - s[i - 1].y <= gap));
    svg.append('g').selectAll('circle').data(s).join('circle').attr('cx', d => x(d.y)).attr('cy', d => y(d.v)).attr('r', 3).attr('fill', col(c)).attr('stroke', 'var(--color-bg)').attr('stroke-width', 1.5)
      .on('mousemove', (ev, d) => H.showTip(ev, [['t', `${c} ${d.y}`], ['', H.T(`${d.v} sponsors`, `${d.v} 家赞助方`)]])).on('mouseleave', H.hideTip);
    const last = s[s.length - 1]; ends.push({c, x: x(last.y) + 7, y: y(last.v)});
  });
  ends.sort((p, q) => p.y - q.y); for (let i = 1; i < ends.length; i++) if (ends[i].y - ends[i - 1].y < 11) ends[i].y = ends[i - 1].y + 11;
  const over = ends.length ? ends[ends.length - 1].y - (Ht - m.b) : 0;
  if (over > 0) { ends[ends.length - 1].y -= over; for (let i = ends.length - 2; i >= 0; i--) if (ends[i + 1].y - ends[i].y < 11) ends[i].y = ends[i + 1].y - 11; }
  ends.forEach(e => svg.append('text').attr('x', e.x).attr('y', e.y).attr('dy', '.35em').attr('font-size', 10).attr('fill', 'var(--color-fg-muted)').text(e.c));
});

// share of listings from mainland China, by field and year
window.HX.on(() => {
  const H = window.HX;
  const el = document.getElementById('c-cn'), lg = document.getElementById('lg-cn');
  const sts = ['listings', 'ml_listings', 'hci_listings'].map(k => dash.data(k));
  const st = sts.find(x => x.status !== 'ok') || sts[0]; lg.replaceChildren();
  if (H.failOrWait(el, st)) return;
  const F = [['NLP', sts[0].data, H.C[0]], ['ML', sts[1].data, H.C[3]], ['HCI', sts[2].data.filter(r => H.HCONF.includes(r.conference)), H.C[4]]];
  const key = H.state.cmode === 'parent' ? 'parent_country' : 'country';
  const series = F.map(([f, rows, c]) => ({f, c, pts: d3.rollups(rows.filter(r => +r.year >= 2013 && H.inRange(r.year)), v => ({n: v.filter(r => (r[key] || r.country) === 'CN').length, t: v.length}), r => +r.year)
    .filter(([, v]) => v.t >= 5).map(([y, v]) => ({y, n: v.n, t: v.t, v: v.n / v.t})).sort((a, b) => a.y - b.y)}));
  H.legend(lg, series.map(s => [s.c, s.f]));
  const all = series.flatMap(s => s.pts);
  const W = el.clientWidth || 500, Ht = 260, m = {l: 38, r: 40, t: 10, b: 24};
  const svg = d3.select(el).append('svg').attr('width', '100%').attr('viewBox', `0 0 ${W} ${Ht}`);
  if (!all.length) { svg.append('text').attr('y', 14).attr('font-size', 12).attr('fill', 'var(--color-fg-muted)').text(H.T('No data in the selected years', '所选年份内没有数据')); return; }
  const ext = d3.extent(all, r => r.y); if (ext[0] === ext[1]) { ext[0] -= 1; ext[1] += 1; }
  const x = d3.scaleLinear(ext, [m.l, W - m.r]);
  const y = d3.scaleLinear([0, Math.max(0.1, d3.max(all, r => r.v) * 1.1)], [Ht - m.b, m.t]).nice();
  svg.append('g').selectAll('line').data(y.ticks(5)).join('line').attr('x1', m.l).attr('x2', W - m.r).attr('y1', d => y(d)).attr('y2', d => y(d)).attr('stroke', 'var(--cds-chart-grid)');
  svg.append('g').attr('transform', `translate(${m.l},0)`).call(d3.axisLeft(y).ticks(5).tickSize(0).tickFormat(d3.format('.0%'))).attr('font-size', null).attr('font-family', null)
    .call(g => { g.select('.domain').remove(); g.selectAll('text').attr('fill', 'var(--color-fg-muted)').attr('font-size', 10); });
  svg.append('g').attr('transform', `translate(0,${Ht - m.b})`).call(d3.axisBottom(x).tickValues(x.ticks(Math.min(8, Math.floor(W / 60))).filter(Number.isInteger)).tickFormat(d3.format('d')).tickSize(0)).attr('font-size', null).attr('font-family', null)
    .call(g => { g.select('.domain').attr('stroke', 'var(--cds-chart-axis)'); g.selectAll('text').attr('fill', 'var(--color-fg-muted)').attr('font-size', 10).attr('dy', '1em'); });
  series.forEach(s => {
    if (!s.pts.length) return;
    svg.append('path').datum(s.pts).attr('fill', 'none').attr('stroke', s.c).attr('stroke-width', 2).attr('d', d3.line(d => x(d.y), d => y(d.v)));
    svg.append('g').selectAll('circle').data(s.pts).join('circle').attr('cx', d => x(d.y)).attr('cy', d => y(d.v)).attr('r', 3).attr('fill', s.c).attr('stroke', 'var(--color-bg)').attr('stroke-width', 1.5)
      .on('mousemove', (ev, d) => H.showTip(ev, [['t', `${s.f} ${d.y}`], ['', H.T(`${d.n} of ${d.t} listings (${d3.format('.0%')(d.v)})`, `${d.t} 条中的 ${d.n} 条（${d3.format('.0%')(d.v)}）`)]])).on('mouseleave', H.hideTip);
    const last = s.pts[s.pts.length - 1]; svg.append('text').attr('x', x(last.y) + 7).attr('y', y(last.v)).attr('dy', '.35em').attr('font-size', 10).attr('fill', 'var(--color-fg-muted)').text(s.f);
  });
});

// companies on more than one side
window.HX.on(() => {
  const H = window.HX;
  const ALIAS = {'Commonwealth Bank of Australia':'Commonwealth Bank','Disney Research':'Disney','Naver':'NAVER','Nokia Bell Labs':'Nokia','Tableau/Salesforce':'Salesforce',
    'Toyota Research Institute':'Toyota','Yahoo/Verizon Media':'Yahoo','eBay/PayPal':'eBay','Sony CSL':'Sony','NTT Docomo':'NTT','SK Planet':'SK Group','Recruit':'Recruit',
    'Optum':'Optum 360','Bloomberg L.P.':'Bloomberg','JPMorgan':'JPMorgan Chase','J.P. Morgan':'JPMorgan Chase'};
  const el = document.getElementById('c-ov'), lg = document.getElementById('lg-ov');
  const sts = ['listings', 'ml_listings', 'hci_listings'].map(k => dash.data(k));
  const st = sts.find(x => x.status !== 'ok') || sts[0]; lg.replaceChildren();
  if (H.failOrWait(el, st)) return;
  const biz = r => r.sector === 'Tech & other industry' || r.sector === 'Finance / quant' || r.sector === 'Industry';
  const N = sts[0].data.filter(r => H.inRange(r.year) && biz(r));
  const M = sts[1].data.filter(r => H.inRange(r.year) && biz(r));
  const Hc = sts[2].data.filter(r => H.inRange(r.year) && biz(r) && H.HCONF.includes(r.conference)).map(r => ({...r, org: ALIAS[r.org] || r.org}));
  const cnt = rows => d3.rollup(rows, v => new Set(v.map(r => r.conference + '-' + r.year)).size, r => r.org);
  const cN = cnt(N), cM = cnt(M), cH = cnt(Hc);
  const ctry = new Map(N.map(r => [r.org, H.cc(r)]));
  const items = [...cN.keys()].filter(o => cM.has(o) || cH.has(o)).map(o => ({org: o, n: cN.get(o), m: cM.get(o) || 0, h: cH.get(o) || 0, country: ctry.get(o)}))
    .sort((p, q) => (q.n + q.m + q.h) - (p.n + p.m + p.h) || p.org.localeCompare(q.org)).slice(0, 18);
  const cols = [H.C[0], H.C[3], H.C[4]];
  H.legend(lg, [[cols[0], H.T('NLP editions', 'NLP 会议届次')], [cols[1], H.T('ML editions', '机器学习会议届次')], [cols[2], H.T('HCI editions', 'HCI 会议届次')]]);
  const W = el.clientWidth || 400, rowH = 30, Ht = items.length * rowH + 22;
  const svg = d3.select(el).append('svg').attr('width', '100%').attr('viewBox', `0 0 ${W} ${Math.max(Ht, 30)}`);
  if (!items.length) { svg.append('text').attr('y', 14).attr('font-size', 12).attr('fill', 'var(--color-fg-muted)').text(H.T('No company sponsored more than one field in the selected years', '所选年份内没有跨领域赞助的企业')); return; }
  const lw = H.measure(svg, items.map(d => d.org), 12) + 10 + H.flagGap();
  const x = d3.scaleLinear([0, d3.max(items, d => Math.max(d.n, d.m, d.h))], [lw, W - 28]);
  const y = d3.scaleBand(items.map(d => d.org), [18, Ht]).padding(0.15);
  svg.append('g').selectAll('text').data(x.ticks(5)).join('text').attr('x', d => x(d)).attr('y', 10).attr('text-anchor', 'middle').attr('font-size', 10).attr('fill', 'var(--color-fg-muted)').text(d => d);
  const g = svg.append('g').selectAll('g').data(items).join('g');
  g.append('text').attr('x', lw - 8 - H.flagGap()).attr('y', d => y(d.org) + y.bandwidth() / 2).attr('dy', '.35em').attr('text-anchor', 'end').attr('font-size', 12).attr('fill', 'var(--color-fg)').text(d => d.org);
  if (H.state.flags) g.each(function (d) { H.flagSvg(d3.select(this), d.country, lw - 6 - H.FW, y(d.org) + y.bandwidth() / 2); });
  const bh = (y.bandwidth() - 2) / 3;
  ['n', 'm', 'h'].forEach((k, i) => {
    g.append('rect').attr('x', lw).attr('y', d => y(d.org) + i * (bh + 1)).attr('height', bh).attr('width', d => Math.max(d[k] ? 1 : 0, x(d[k]) - lw)).attr('rx', 2).attr('fill', cols[i]);
    g.append('text').attr('x', d => x(d[k]) + 4).attr('y', d => y(d.org) + i * (bh + 1) + bh / 2).attr('dy', '.35em').attr('font-size', 9).attr('fill', 'var(--color-fg-muted)').text(d => d[k] || '');
  });
  g.append('rect').attr('x', 0).attr('width', W).attr('y', d => y(d.org)).attr('height', y.bandwidth()).attr('fill', 'transparent')
    .on('mousemove', (ev, d) => H.showTip(ev, [['t', d.org], ['', H.T(`NLP: ${d.n} editions`, `NLP：${d.n} 届`)], ['', H.T(`ML: ${d.m} editions`, `机器学习：${d.m} 届`)], ['', H.T(`HCI: ${d.h} editions`, `HCI：${d.h} 届`)]])).on('mouseleave', H.hideTip);
});
</script>
'''
s = s.rstrip() + '\n' + CMP_JS

# ---- method section ------------------------------------------------------------------------------
m = re.search(r'(<section class="card method">\n    <h2 id="caveats">.*?</h2>\n).*?(  </section>)', s, re.S)


def ul(items):
    return '<ul class="caveats">\n' + '\n'.join(f'        <li>{L(en, zh)}</li>' for en, zh in items) + '\n      </ul>'


def det(en, zh, body):
    return f'    <details>\n      <summary>{L(en, zh)}</summary>\n      <div class="dbody">{body}\n      </div>\n    </details>'


cov = [('ACL', '2013–2026', 'ACL 2016 lists no tiers', 'ACL 2016 没有标等级'),
       ('EMNLP', '2013–2026', 'EMNLP 2026 (November) taken from its sponsor page in October 2026', 'EMNLP 2026（11 月举办）取自 2026 年 10 月的赞助页'),
       ('NAACL', '2013, 2015, 2016, 2018, 2019, 2021, 2022, 2024, 2025', 'not held in 2014, 2017, 2020, 2023, 2026', '2014、2017、2020、2023、2026 年没有举办')]
rows = '\n'.join(f'            <tr><td>{c}</td><td>{y}</td><td>{L(me, mz)}</td><td>{L("2019–2026 (2018 reuses 2019)", "2019–2026（2018 年沿用 2019 年）")}</td></tr>' for c, y, me, mz in cov)
method = '\n'.join([
    '    <p class="note">' + L('Click a heading to expand it.', '点击标题展开。') + '</p>',
    det('Where the data come from', '数据来源', ul([
        ('Each edition’s sponsor page, read from archived copies on the Internet Archive (EMNLP 2026 from the live page). ACL 2022’s page shows logos without names, so its tiers come from the ACL Sponsorship Director’s report, which lists every sponsor by tier.',
         '各届官网的赞助页，通过 Internet Archive 的存档读取（EMNLP 2026 取自当前网页）。ACL 2022 的赞助页只有不带名字的 logo，所以用的是 ACL 赞助主管报告里按等级列出的名单。'),
        ('Prices come from the sponsorship booklets ACL publishes for its conferences (2019–2026). Reported income comes from the Sponsorship Director’s reports on the ACL admin wiki (2023 Q1 and 2024 Q1).',
         '价格来自 ACL 为旗下会议发布的赞助手册（2019–2026）。实际收入来自 ACL admin wiki 上赞助主管的报告（2023 年第一季度、2024 年第一季度）。')])),
    det('Coverage by conference', '各会议的覆盖范围', f'''<div class="tbox" style="max-height:none">
      <table class="cov">
        <thead><tr><th>{L('Conference', '会议')}</th><th>{L('Sponsor lists', '有名单的年份')}</th><th>{L('Notes', '说明')}</th><th>{L('Tier prices', '等级价格')}</th></tr></thead>
        <tbody>
{rows}
        </tbody>
      </table>
    </div>'''),
    det('How sponsors are counted', '怎么计数', ul([
        ('An organization counts once per conference edition, at its highest tier. Diversity and inclusion sponsorships, local and destination partners (tourism boards, city governments), award and student-volunteer sponsors are listed but have no price, so they do not add to the estimates.',
         '同一机构在一届会议只计 1 次，取最高等级。多元与包容（D&I）赞助、本地和目的地合作方（旅游局、市政府）、奖项和学生志愿者赞助都列出，但没有价格，不计入估算。'),
        ('Brands of one company are merged with the same rules as the ML page: DeepMind into Google; LinkedIn and Microsoft Translator into Microsoft; Toutiao into ByteDance; Naver Labs Europe into NAVER; Alibaba Cloud and Taobao into Alibaba (Ant Group kept separate); A9 into Amazon. HLTCOE and CLSP count as Johns Hopkins University, ISI as USC.',
         '同一公司的品牌按机器学习页面的规则合并：DeepMind 计入 Google；LinkedIn、Microsoft Translator 计入 Microsoft；今日头条计入字节；Naver Labs Europe 计入 NAVER；阿里云、淘天计入阿里巴巴（蚂蚁单列）；A9 计入 Amazon。HLTCOE 和 CLSP 计入约翰斯·霍普金斯大学，ISI 计入 USC。'),
        ('Finance / quant covers trading firms, banks and financial data companies.', '“金融 / 量化”包括交易公司、银行和金融数据公司。')])),
    det('Estimated amounts', '估算金额', ul([
        ('Each sponsor counts at its tier’s price for that conference and year. 2018 uses the 2019 prices, which were the first published; editions before 2018 are not estimated. From 2023 the Supporter tier is no longer listed and counts as $2,000.',
         '每家赞助商按当年该会议该等级的价格计。2018 年用 2019 年（最早公开的一份）价格；2018 年以前不估算。2023 年起手册不再列 Supporter 等级，按 $2,000 计。'),
        ('The estimates come within about 10% of the reported income for the five editions where both exist (2022–2023). Sponsors buying several conferences at once get a discount, and some deals include extras, so single editions can be off in either direction.',
         '在同时有估算和实际收入的五届（2022–2023）里，估算和实际相差约 10% 以内。同时赞助多个会议的打包有折扣，有些合同还有附加项，所以单届估算可能偏高也可能偏低。')])),
    det('Countries', '国家 / 地区', ul([
        ('Two modes, switchable at the top: the sponsoring entity’s headquarters, or its parent company (for example Megagon Labs is in the US, its parent Recruit in Japan). A few small companies could not be located; they stay in the lists but get no country row.',
         '两种口径，可在顶部切换：赞助实体总部所在地，或母公司国籍（例如 Megagon Labs 在美国，母公司 Recruit 在日本）。少数小公司无法确定所在地，仍计入名单，但不单列国家。'),
        ('Flags come from the open-source flag-icons set.', '国旗图形来自开源的 flag-icons 图标库。')])),
])
s = s[:m.end(1)] + method + '\n' + s[m.end(2) - len('  </section>'):]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(s)
print('wrote', os.path.relpath(OUT, ROOT))
