"""Generate dashboard/ai/index.html (NeurIPS / ICML / ICLR) from the HCI page,
so both pages share one layout, style and set of controls.

    python scripts/make_ai_page.py

It swaps in the AI conferences, sectors, headline numbers, notes, summary and
method text, and adds a section comparing AI and HCI sponsorship.
"""
import os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = os.path.join(ROOT, 'dashboard', 'index.html')
OUT = os.path.join(ROOT, 'dashboard', 'ai', 'index.html')
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
    """Replace the first note after the heading with this id."""
    sub(r'(<h2 id="' + section_id + r'">.*?</h2>\s*<p class="note">).*?(</p>)', None) if False else None
    global s
    m = re.search(r'<h2 id="' + section_id + r'">.*?</h2>\s*<p class="note">(.*?)</p>', s, re.S)
    assert m, section_id
    s = s[:m.start(1)] + L(en, zh) + s[m.end(1):]


# ---- header -----------------------------------------------------------------
rep(L('Who Sponsors HCI Conferences', '谁在赞助 HCI 会议'), L('Who Sponsors AI Conferences', '谁在赞助 AI 会议'))
rep('CHI · CSCW · UIST · UbiComp · DIS · IUI · FAccT · AIES</p>', 'NeurIPS · ICML · ICLR</p>')
rep(L('Who pays for the main HCI conferences, and how that has changed over the years. The sponsor lists were compiled by hand from each conference’s website.',
      '谁在为主要的 HCI 会议出钱，以及这些年的变化。赞助商名单根据各会议官网手工整理。'),
    L('Who pays for the three largest machine-learning conferences, and how that compares with HCI. The sponsor lists come from each conference’s public sponsor pages and archives.',
      '谁在为三大机器学习会议出钱，以及和 HCI 会议相比有何不同。赞助商名单来自各会议公开的赞助页和存档。'))

# ---- contents rail: add the comparison section -------------------------------
rep('      <li><a href="#summary" data-target="summary">',
    '      <li><a href="#vs-hci" data-target="vs-hci">' + L('Compared with HCI', '和 HCI 会议比') + '</a></li>\n      <li><a href="#summary" data-target="summary">')

# ---- notes --------------------------------------------------------------------
note('timeline',
     'One row per organization, one column per year. A filled cell means the organization sponsored that year; darker means a higher tier (Diamond or Platinum / Gold or Silver / Bronze and others; NeurIPS 2013–2014 lists have no tiers). Grey columns are years with no sponsor list; NeurIPS 2021 had no sponsorship. Sorting by last appearance puts current sponsors at the top; further down stopped earlier.',
     '每行一家机构，每列一年；有色格子表示当年赞助，颜色越深等级越高（Diamond/Platinum、Gold/Silver、Bronze 及其他；NeurIPS 2013–2014 的名单没有等级）。灰色列是没拿到名单的年份；NeurIPS 2021 没有设赞助。按“最后出现”排序时，最近仍在赞助的机构排在最上面，越往下停得越早。')
note('by-conference',
     'For the selected years, organizations ranked by how many editions they sponsored (one count per organization per edition). Pick a conference or all three together, and how many to show. The label shows editions and the year span; hover for tiers and estimated totals.',
     '所选年份内，按赞助届数给机构排名（同一机构在一届会议计 1 次）。可以选单个会议或三个会议合计，以及显示前几名。右侧是届数和年份跨度，悬停查看各等级次数和估算金额。')
note('countries',
     'Each cell is the share of a conference’s sponsors (organization × edition, selected years) that come from that country; the number is the count. Darker means a larger share.',
     '每格是该会议（所选年份内的“机构 × 届次”）中来自该国家/地区的比例，格内数字是条数，颜色越深占比越高。')
note('sectors',
     'Share of each conference’s sponsor listings by type of organization, for the selected years. Finance includes hedge funds, trading firms, banks, financial data companies and venture capital.',
     '所选年份内，各会议赞助条目按机构类型的占比。“金融 / 量化”包括对冲基金、做市商、银行、金融数据公司和风险投资。')
note('per-attendee',
     'Estimated sponsorship divided by registrations. Prices were found only for NeurIPS 2024 and ICML 2026, so only NeurIPS 2023–2025 can be plotted.',
     '估算赞助额 ÷ 当届注册人数。只找到 NeurIPS 2024 和 ICML 2026 的价目，所以只有 NeurIPS 2023–2025 有点。')
note('money',
     'Each sponsor is counted at its tier’s published price and summed per edition, so these are lower bounds. Only nearby years are estimated (NeurIPS 2023–2025 with 2024 prices, ICML 2025–2026 with 2026 prices). For reference, NeurIPS reported $3.7M in sponsor income for 2019.',
     '每家赞助商按其等级的公开价计，加总得到每届的估算下限；只估算相邻年份（NeurIPS 2023–2025 用 2024 价目，ICML 2025–2026 用 2026 价目）。作为参照，NeurIPS 官方预算说明中 2019 年的赞助收入为 $3.7M。')
rep('<span lang="en">Only prices found on official sites or sponsor prospectuses. Each tier is a floor price; actual amounts may be higher.</span><span lang="zh">只列官网/招商书上能找到的价目；每个等级是“起步价”，实际金额可能更高。</span>',
    L('The three conferences do not publish prices on their sponsor pages; these two lists come from archived exhibitor pages. Actual deals may include discounts or extras.',
      '三个会议的赞助页都不公开价目，只在招商页存档里找到这两份；实际成交价可能有折扣或附加项。'))

# ---- constants ------------------------------------------------------------------
rep("const CONF = ['CHI','CSCW','UIST','UbiComp','DIS','IUI','FAccT','AIES'];",
    "const CONF = ['NeurIPS','ICML','ICLR'];\nconst HCONF = ['CHI','CSCW','UIST','UbiComp'];")
rep("window.HX = {C, T, cc, CONF,", "window.HX = {C, T, cc, CONF, HCONF,")
sub(r"const SECT = \[.*?\];", "const SECT = ['Tech & other industry','Finance / quant','Government / academic / non-profit','Publisher'];")
sub(r"const SECT_ZH0 = \{.*?\};", "const SECT_ZH0 = {'Tech & other industry':'科技及其他企业','Finance / quant':'金融 / 量化','Government / academic / non-profit':'政府 / 学术 / 非营利','Publisher':'出版社'};")
sub(r"const SECT_EN0 = \{.*?\};", "const SECT_EN0 = {'Tech & other industry':'Tech and other companies','Finance / quant':'Finance / quant','Government / academic / non-profit':'Government / academic / non-profit','Publisher':'Publisher'};")
EXTRA_ZH = "RU:'俄罗斯',SA:'沙特阿拉伯',IL:'以色列',VN:'越南',TH:'泰国',BR:'巴西',MX:'墨西哥',BG:'保加利亚',BE:'比利时',ZA:'南非',CZ:'捷克',IE:'爱尔兰','??':'未知',"
EXTRA_EN = "RU:'Russia',SA:'Saudi Arabia',IL:'Israel',VN:'Vietnam',TH:'Thailand',BR:'Brazil',MX:'Mexico',BG:'Bulgaria',BE:'Belgium',ZA:'South Africa',CZ:'Czechia',IE:'Ireland','??':'Unknown',"
rep("const CTY_ZH0 = {", "const CTY_ZH0 = {" + EXTRA_ZH)
rep("const CTY_EN0 = {", "const CTY_EN0 = {" + EXTRA_EN)

# ---- headline numbers: replace the two calcs --------------------------------------
sub(r"dash\.calc\('kpis', \{.*?\n\}\);\n\ndash\.calc\('cscw_trend', \{.*?\n\}\);", """dash.calc('kpis', {
  inputs: ['listings'], title: 'Headline counts (all years)',
  description: 'Counts listings, distinct organisations, conference-years, HQ countries, and the share of listings from finance / quant firms.',
  fn: (listings) => [
    {metric:'listings', value: String(listings.length)},
    {metric:'orgs', value: String(new Set(listings.map(r => r.org)).size)},
    {metric:'confyears', value: String(new Set(listings.map(r => r.conference + '-' + r.year)).size)},
    {metric:'countries', value: String(new Set(listings.map(r => r.country).filter(c => c && c !== '??')).size)},
    {metric:'finshare', value: Math.round(100 * listings.filter(r => r.sector === 'Finance / quant').length / listings.length) + '%'},
  ]
});

dash.calc('money_cmp', {
  inputs: ['pcy', 'hci_pcy'], title: 'NeurIPS vs CHI estimated sponsorship, 2025',
  description: 'Estimated sponsorship lower bound for NeurIPS 2025 and CHI 2025, from published tier prices.',
  fn: (pcy, hci_pcy) => {
    const v = (rows, c) => { const r = rows.find(x => x.conference === c && +x.year === 2025); return r && r.est_usd !== '' ? +r.est_usd : null; };
    const f = x => x == null ? '—' : x >= 1e6 ? '$' + (x / 1e6).toFixed(1) + 'M' : '$' + Math.round(x / 1000) + 'k';
    return [{metric:'neurips2025', value: f(v(pcy, 'NeurIPS'))}, {metric:'chi2025', value: f(v(hci_pcy, 'CHI'))}];
  }
});""")
rep("['kpis','cscw_trend'].forEach(id => {\n    const st = dash.data(id); const k = id === 'kpis' ? 'metric' : 'period';",
    "['kpis','money_cmp'].forEach(id => {\n    const st = dash.data(id); const k = 'metric';")

# ---- timeline levels by tier name ---------------------------------------------------
rep("const LEVELS = [['high', '≥ $20k', 1], ['mid', '$5k–20k', 0.6], ['low', '< $5k', 0.3], ['unknown', null, 0]];",
    "const LEVELS = [['high', 'Diamond / Platinum', 1], ['mid', 'Gold / Silver', 0.6], ['low', null, 0.3], ['unknown', null, 0]];")
rep("sp.append(i, lab || H.T('Price unknown', '价格未知')); lg.append(sp);",
    "sp.append(i, lab || (k === 'low' ? H.T('Bronze and others', 'Bronze 及其他') : H.T('No tier listed', '未标等级'))); lg.append(sp);")
rep("let conf = 'CSCW', sort = 'last', all = false;", "let conf = 'NeurIPS', sort = 'last', all = false;")
rep("const level = r => r.est_usd === '' ? 'unknown' : +r.est_usd >= 20000 ? 'high' : +r.est_usd >= 5000 ? 'mid' : 'low';",
    "const level = r => ({top: 'high', mid: 'mid', low: 'low'})[r.tier_level] || 'unknown';")
rep("H.T('Price unknown', '价格未知') : H.T(`Floor price ${H.fmtUSD(+d.est_usd)}`, `起步价 ${H.fmtUSD(+d.est_usd)}`)",
    "H.T('No price for that year', '没有当年价目') : H.T(`Estimate ${H.fmtUSD(+d.est_usd)}`, `估算 ${H.fmtUSD(+d.est_usd)}`)")

rep('<div class="tlbox"><div id="c-tl"', '<div class="tlbox" style="max-height:44rem;overflow:auto"><div id="c-tl"')

# ---- top sponsors: three conferences ---------------------------------------------------
rep("e.textContent = 'All eight';", "e.textContent = 'All three';")
rep("z.textContent = '八个会议合计';", "z.textContent = '三个会议合计';")

# ---- countries: '??' is unknown -----------------------------------------------------------
rep("const unknown = by.find(d => !d.cc);\n  const known = by.filter(d => d.cc);",
    "const unknown = by.find(d => !d.cc || d.cc === '??');\n  const known = by.filter(d => d.cc && d.cc !== '??');")

# ---- summary -----------------------------------------------------------------------------
m_ = lambda w: f'<b data-source="money_cmp" data-field="value" data-where="metric={w}" class="dash-skeleton">—</b>'
k_ = lambda w: f'<b data-source="kpis" data-field="value" data-where="metric={w}" class="dash-skeleton">—</b>'
sub(r'(<h2 id="summary">.*?</h2>\n).*?(  </section>)', None) if False else None
m = re.search(r'(<h2 id="summary">.*?</h2>\n)(.*?)(  </section>)', s, re.S)
summary = f'''    <ul class="summary" lang="en">
        <li><strong>An order of magnitude more money than HCI.</strong> At published tier prices, NeurIPS 2025 drew at least {m_("neurips2025")} from sponsors, against about {m_("chi2025")} for CHI 2025.</li>
        <li><strong>Finance is the second-largest group.</strong> {k_("finshare")} of all listings come from hedge funds, trading firms and banks such as Citadel, Jane Street, Jump, D. E. Shaw and Two Sigma. They hardly appear at HCI conferences.</li>
        <li><strong>Same companies, different priorities.</strong> Google, Microsoft and Meta sponsor both fields; Adobe and Autodesk mostly HCI; Amazon, Baidu and ByteDance almost only AI. Since 2023, AI infrastructure and data companies (Lambda, Together AI, Nebius, Scale AI) have poured in.</li>
    </ul>
    <ul class="summary" lang="zh">
        <li><strong>赞助规模比 HCI 大一个数量级。</strong>按公开等级价估算，NeurIPS 2025 的赞助至少 {m_("neurips2025")}，同年 CHI 约 {m_("chi2025")}。</li>
        <li><strong>金融机构是第二大赞助群体。</strong>全部赞助条目中 {k_("finshare")} 来自对冲基金、做市商和银行，如 Citadel、Jane Street、Jump、D. E. Shaw、Two Sigma；它们在 HCI 会议里几乎看不到。</li>
        <li><strong>同一批公司，侧重不同。</strong>Google、Microsoft、Meta 两边都赞助；Adobe、Autodesk 主要在 HCI；Amazon、百度、字节几乎只在 AI。2023 年后，Lambda、Together AI、Nebius、Scale AI 等 AI 基础设施和数据公司大量进入。</li>
    </ul>
'''
s = s[:m.start(2)] + summary + s[m.end(2):]

# ---- comparison section, before the summary ------------------------------------------------------
cmp = f'''  <section class="card" id="vs-card">
    <h2 id="vs-hci">{L('Compared with HCI', '和 HCI 会议比')}</h2>
    <p class="note">{L('Left: sponsors per edition (each organization once), solid lines for AI conferences and dashed lines for CHI, CSCW, UIST and UbiComp. Right: companies that sponsored both fields, and how many editions of each they sponsored in the selected years.',
                       '左：每届赞助方数量（同一机构在一届只计 1 次），实线是 AI 会议，虚线是 CHI、CSCW、UIST、UbiComp。右：两边都赞助过的企业，在所选年份内分别赞助了多少届 AI 会议和 HCI 会议。')}</p>
    <div class="grid" style="gap:2.5rem">
      <div><div class="legend" id="lg-cmp"></div><div id="c-cmp" data-source="pcy hci_pcy" style="min-height:260px"></div></div>
      <div><div class="legend" id="lg-ov"></div><div id="c-ov" data-source="listings hci_listings" style="min-height:420px"></div></div>
    </div>
  </section>

'''
rep('  <section class="card" id="summary-card">', cmp + '  <section class="card" id="summary-card">')

CMP_JS = r'''
<script>
// AI vs HCI: sponsors per edition
window.HX.on(() => {
  const H = window.HX;
  const el = document.getElementById('c-cmp'), lg = document.getElementById('lg-cmp');
  const a = dash.data('pcy'), b = dash.data('hci_pcy');
  const st = a.status !== 'ok' ? a : b; lg.replaceChildren();
  if (H.failOrWait(el, st)) return;
  const ALL = [...H.CONF, ...H.HCONF];
  const col = c => H.C[ALL.indexOf(c)];
  const rows = [...a.data, ...b.data].filter(r => ALL.includes(r.conference) && +r.year >= 2013 && H.inRange(r.year)).map(r => ({c: r.conference, y: +r.year, v: +r.n_sponsors}));
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
    const hci = H.HCONF.includes(c);
    svg.append('path').datum(s).attr('fill', 'none').attr('stroke', col(c)).attr('stroke-width', hci ? 1.5 : 2).attr('stroke-dasharray', hci ? '4 3' : null)
      .attr('d', d3.line(d => x(d.y), d => y(d.v)).defined((d, i) => i === 0 || d.y - s[i - 1].y === 1));
    svg.append('g').selectAll('circle').data(s).join('circle').attr('cx', d => x(d.y)).attr('cy', d => y(d.v)).attr('r', 3).attr('fill', col(c)).attr('stroke', 'var(--color-bg)').attr('stroke-width', 1.5)
      .on('mousemove', (ev, d) => H.showTip(ev, [['t', `${c} ${d.y}`], ['', H.T(`${d.v} sponsors`, `${d.v} 家赞助方`)]])).on('mouseleave', H.hideTip);
    const last = s[s.length - 1]; ends.push({c, x: x(last.y) + 7, y: y(last.v)});
  });
  ends.sort((p, q) => p.y - q.y); for (let i = 1; i < ends.length; i++) if (ends[i].y - ends[i - 1].y < 11) ends[i].y = ends[i - 1].y + 11;
  const over = ends.length ? ends[ends.length - 1].y - (Ht - m.b) : 0;
  if (over > 0) { ends[ends.length - 1].y -= over; for (let i = ends.length - 2; i >= 0; i--) if (ends[i + 1].y - ends[i].y < 11) ends[i].y = ends[i + 1].y - 11; }
  ends.forEach(e => svg.append('text').attr('x', e.x).attr('y', e.y).attr('dy', '.35em').attr('font-size', 10).attr('fill', 'var(--color-fg-muted)').text(e.c));
});

// companies on both sides
window.HX.on(() => {
  const H = window.HX;
  const ALIAS = {'Commonwealth Bank of Australia':'Commonwealth Bank','Disney Research':'Disney','Naver':'NAVER','Nokia Bell Labs':'Nokia','Tableau/Salesforce':'Salesforce',
    'Telefonica':'Telefonca I+D','Toyota Research Institute':'Toyota','United Technologies Research Center':'UTRC (RTX)','Yahoo/Verizon Media':'Yahoo','eBay/PayPal':'eBay',
    'Sony CSL':'Sony','NTT Docomo':'NTT','SK Planet':'SK Group','Recruit':'Recruit Communications','Optum':'Optum Labs'};
  const el = document.getElementById('c-ov'), lg = document.getElementById('lg-ov');
  const a = dash.data('listings'), b = dash.data('hci_listings');
  const st = a.status !== 'ok' ? a : b; lg.replaceChildren();
  if (H.failOrWait(el, st)) return;
  const ai = a.data.filter(r => H.inRange(r.year) && r.sector !== 'Publisher' && r.sector !== 'Government / academic / non-profit');
  const hc = b.data.filter(r => H.inRange(r.year) && r.sector === 'Industry' && H.HCONF.includes(r.conference)).map(r => ({...r, org: ALIAS[r.org] || r.org}));
  const cnt = rows => d3.rollup(rows, v => new Set(v.map(r => r.conference + '-' + r.year)).size, r => r.org);
  const A = cnt(ai), Hm = cnt(hc);
  const ctry = new Map(ai.map(r => [r.org, H.cc(r)]));
  const items = [...A.keys()].filter(o => Hm.has(o)).map(o => ({org: o, ai: A.get(o), hci: Hm.get(o), country: ctry.get(o)}))
    .sort((p, q) => (q.ai + q.hci) - (p.ai + p.hci) || p.org.localeCompare(q.org)).slice(0, 16);
  const cA = H.C[0], cH = H.C[3];
  H.legend(lg, [[cA, H.T('AI conference editions', 'AI 会议届次')], [cH, H.T('HCI conference editions', 'HCI 会议届次')]]);
  const W = el.clientWidth || 400, rowH = 26, Ht = items.length * rowH + 22;
  const svg = d3.select(el).append('svg').attr('width', '100%').attr('viewBox', `0 0 ${W} ${Math.max(Ht, 30)}`);
  if (!items.length) { svg.append('text').attr('y', 14).attr('font-size', 12).attr('fill', 'var(--color-fg-muted)').text(H.T('No company sponsored both fields in the selected years', '所选年份内没有两边都赞助的企业')); return; }
  const lw = H.measure(svg, items.map(d => d.org), 12) + 10 + H.flagGap();
  const x = d3.scaleLinear([0, d3.max(items, d => Math.max(d.ai, d.hci))], [lw, W - 28]);
  const y = d3.scaleBand(items.map(d => d.org), [18, Ht]).padding(0.2);
  svg.append('g').selectAll('text').data(x.ticks(5)).join('text').attr('x', d => x(d)).attr('y', 10).attr('text-anchor', 'middle').attr('font-size', 10).attr('fill', 'var(--color-fg-muted)').text(d => d);
  const g = svg.append('g').selectAll('g').data(items).join('g');
  g.append('text').attr('x', lw - 8 - H.flagGap()).attr('y', d => y(d.org) + y.bandwidth() / 2).attr('dy', '.35em').attr('text-anchor', 'end').attr('font-size', 12).attr('fill', 'var(--color-fg)').text(d => d.org);
  if (H.state.flags) g.each(function (d) { H.flagSvg(d3.select(this), d.country, lw - 6 - H.FW, y(d.org) + y.bandwidth() / 2); });
  const bh = y.bandwidth() / 2 - 1;
  g.append('rect').attr('x', lw).attr('y', d => y(d.org)).attr('height', bh).attr('width', d => Math.max(1, x(d.ai) - lw)).attr('rx', 3).attr('fill', cA);
  g.append('rect').attr('x', lw).attr('y', d => y(d.org) + bh + 2).attr('height', bh).attr('width', d => Math.max(d.hci ? 1 : 0, x(d.hci) - lw)).attr('rx', 3).attr('fill', cH);
  g.append('text').attr('x', d => x(d.ai) + 4).attr('y', d => y(d.org) + bh / 2).attr('dy', '.35em').attr('font-size', 10).attr('fill', 'var(--color-fg-muted)').text(d => d.ai);
  g.append('text').attr('x', d => x(d.hci) + 4).attr('y', d => y(d.org) + bh * 1.5 + 2).attr('dy', '.35em').attr('font-size', 10).attr('fill', 'var(--color-fg-muted)').text(d => d.hci);
  g.append('rect').attr('x', 0).attr('width', W).attr('y', d => y(d.org)).attr('height', y.bandwidth()).attr('fill', 'transparent')
    .on('mousemove', (ev, d) => H.showTip(ev, [['t', d.org], ['', H.T(`AI conferences: ${d.ai} editions`, `AI 会议：${d.ai} 届`)], ['', H.T(`HCI conferences: ${d.hci} editions`, `HCI 会议：${d.hci} 届`)]])).on('mouseleave', H.hideTip);
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


cov = [('NeurIPS', '2013–2026', 'NeurIPS 2021 had no sponsorship (careers page only)', 'NeurIPS 2021 没有设赞助（只有招聘页）', '2024 (2023 and 2025 reuse it)', '2024 年（2023、2025 年沿用）', '2013–2025'),
       ('ICML', '2015–2026', '2013–2014', '2013–2014', '2026 (2025 reuses it)', '2026 年（2025 年沿用）', '2017–2024'),
       ('ICLR', '2017, 2020–2026', '2013–2016, 2018–2019', '2013–2016、2018–2019', 'none found', '未找到', '2018–2025')]
rows = '\n'.join(f'            <tr><td>{c}</td><td>{y}</td><td>{L(me, mz)}</td><td>{L(pe, pz)}</td><td>{a}</td></tr>' for c, y, me, mz, pe, pz, a in cov)
method = '\n'.join([
    '    <p class="note">' + L('Click a heading to expand it.', '点击标题展开。') + '</p>',
    det('Where the data come from', '数据来源', ul([
        ('From 2015 on, each conference’s public sponsor API (neurips.cc, icml.cc, iclr.cc). NeurIPS 2013–2014 come from the printed conference books, ICML 2015–2016 and ICLR 2017 from archived conference sites, ICLR 2026 from its sponsor list page.',
         '2015 年起来自各会议公开的赞助接口（neurips.cc、icml.cc、iclr.cc）。NeurIPS 2013–2014 来自会议手册，ICML 2015–2016 和 ICLR 2017 来自旧官网存档，ICLR 2026 来自其赞助商列表页。'),
        ('Attendance: the NeurIPS fact sheet (2020–2021 were virtual; 2025 includes online attendees), ICML’s published statistics, and Wikipedia for ICLR.',
         '注册人数：NeurIPS 官方 fact sheet（2020–2021 为线上；2025 含线上），ICML 官方统计，ICLR 来自 Wikipedia。')])),
    det('Coverage by conference', '各会议的覆盖范围', f'''<div class="tbox" style="max-height:none">
      <table class="cov">
        <thead><tr><th>{L('Conference', '会议')}</th><th>{L('Sponsor lists', '有名单的年份')}</th><th>{L('Missing', '缺失')}</th><th>{L('Tier prices', '等级价格')}</th><th>{L('Attendance', '注册人数')}</th></tr></thead>
        <tbody>
{rows}
        </tbody>
      </table>
    </div>'''),
    det('How sponsors are counted', '怎么计数', ul([
        ('An organization counts once per conference edition, at its highest tier. NeurIPS 2026 was held in several places; an organization present at more than one counts once.',
         '同一机构在一届会议只计 1 次，取最高等级。NeurIPS 2026 有多个举办地，同一机构只计一次。'),
        ('Brands of one company are merged: DeepMind, Google Research and Kaggle into Google; LinkedIn into Microsoft; Habana and Nervana into Intel; Xilinx into AMD; TikTok into ByteDance; Borealis AI into RBC; MosaicML into Databricks; Toyota Research Institute into Toyota. Diversity-fund sponsorships are merged with regular ones.',
         '同一公司的品牌已合并：DeepMind、Google Research、Kaggle 计入 Google；LinkedIn 计入 Microsoft；Habana、Nervana 计入 Intel；Xilinx 计入 AMD；TikTok 计入 ByteDance；Borealis AI 计入 RBC；MosaicML 计入 Databricks；TRI 计入 Toyota。DEI 基金类赞助与普通赞助合并。'),
        ('Finance / quant covers hedge funds, trading firms, banks, financial data companies and venture capital.',
         '“金融 / 量化”包括对冲基金、做市商、银行、金融数据公司和风险投资。')])),
    det('Estimated amounts', '估算金额', ul([
        ('Only two price lists were found: NeurIPS 2024 (Diamond $90k, Platinum $50k, Gold $35k, Silver $22k, Bronze $12k) and ICML 2026 (Diamond $100k, Platinum $80k, Gold $45k, Silver $30k, Bronze $20k). Only nearby years are estimated; ICLR is not.',
         '只找到两份价目：NeurIPS 2024（Diamond $90k、Platinum $50k、Gold $35k、Silver $22k、Bronze $12k）和 ICML 2026（Diamond $100k、Platinum $80k、Gold $45k、Silver $30k、Bronze $20k）。只估算相邻年份；ICLR 不估算。'),
        ('Tiers without a published price (Silver Pavilion, Startup and similar) are not counted, so every amount is a lower bound. For reference, NeurIPS reported $3.7M in sponsor income for 2019.',
         'Silver Pavilion、Startup 等没有价格的等级不计入，所以所有金额都是下限。作为参照，NeurIPS 官方预算说明中 2019 年的赞助收入为 $3.7M。')])),
    det('Countries', '国家 / 地区', ul([
        ('Two modes, switchable at the top: the sponsoring entity’s headquarters, or its parent company. About 40 small companies could not be located; they stay in the lists but get no country row.',
         '两种口径，可在顶部切换：赞助实体总部所在地，或母公司国籍。约 40 家小公司无法确定所在地，仍计入名单，但不单列国家。'),
        ('Flags come from the open-source flag-icons set.', '国旗图形来自开源的 flag-icons 图标库。')])),
])
s = s[:m.end(1)] + method + '\n' + s[m.end(2) - len('  </section>'):]

open(OUT, 'w', encoding='utf-8').write(s)
print('wrote', os.path.relpath(OUT, ROOT))
