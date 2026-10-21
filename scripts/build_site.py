"""Build the public GitHub Pages site into docs/.

    python scripts/build_site.py

Reads site.config.json (author, homepage, email, github_repo "owner/repo",
site_url where the site is published, goatcounter code) and writes:
    docs/index.html        HCI and AI-ethics conferences (English / 中文)
    docs/ai/index.html     NeurIPS / ICML / ICLR
    docs/data/...          the CSV files both pages load
Empty config fields are simply left out of the footer.
"""
import html, json, os, re, shutil, datetime
from make_standalone import HEAD, TAIL

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DOCS = os.path.join(ROOT, 'docs')
cfg = json.load(open(os.path.join(ROOT, 'site.config.json'), encoding='utf-8'))
e = lambda v: html.escape(v or '', quote=True)
repo = cfg.get('github_repo') or ''
owner, _, name = repo.partition('/')
site_url = cfg.get('site_url') or ''   # e.g. https://whosponsorshci.vercel.app/
year = datetime.date.today().year

def footer(bilingual, page_rel_root):
    L = (lambda en, zh: f'<span lang="en">{en}</span><span lang="zh">{zh}</span>') if bilingual else (lambda en, zh: zh)
    who = []
    if cfg.get('author'): who.append(f'<b>{e(cfg["author"])}</b>')
    if cfg.get('homepage'): who.append(f'<a href="{e(cfg["homepage"])}" target="_blank" rel="noopener">{L("Homepage", "个人主页")}</a>')
    if cfg.get('email'): who.append(f'<span class="mail">{e(cfg["email"])}</span>')
    if repo: who.append(f'<a href="https://github.com/{e(repo)}" target="_blank" rel="noopener">{L("Source and data on GitHub", "GitHub 上的代码和数据")}</a>')
    other = (f'<a href="{page_rel_root}ai/">{L("AI conferences (NeurIPS / ICML / ICLR)", "AI 会议（NeurIPS / ICML / ICLR）")}</a>' if not page_rel_root
             else f'<a href="{page_rel_root}">{L("HCI conferences", "HCI 会议")}</a>')
    cite_who = e(cfg.get('author') or 'the author')
    cite = f'{cite_who} ({year}). <i>Who Sponsors HCI Conferences</i>.' + (f' {e(site_url)}' if site_url else '')
    issues = f'https://github.com/{e(repo)}/issues' if repo else ''
    fix = (L(f'Corrections are welcome as a <a href="{issues}" target="_blank" rel="noopener">GitHub issue</a>.', f'欢迎在 <a href="{issues}" target="_blank" rel="noopener">GitHub issue</a> 里指出错误。') if issues
           else L('Corrections are welcome.', '欢迎指出错误。'))
    gc = cfg.get('goatcounter') or ''
    views = ''
    if gc:
        views = f'''<p class="views" id="views" hidden></p>
<script>window.goatcounter = {{path: p => location.host + p}};</script>
<script data-goatcounter="https://{e(gc)}.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
<script>
(() => {{
  const el = document.getElementById('views');
  fetch('https://{e(gc)}.goatcounter.com/counter/' + encodeURIComponent(location.host + location.pathname) + '.json')
    .then(r => r.ok ? r.json() : null).then(d => {{ if (!d || !d.count) return;
      const n = document.createElement('span'); n.textContent = d.count;
      el.append(n, document.createTextNode(' ')); const t = document.createElement('span'); t.className = 'vt';
      t.innerHTML = {json.dumps(L('views', '次浏览'))}; el.append(t); el.hidden = false; }}).catch(() => {{}});
}})();
</script>'''
    lic = L('Data <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a>, code MIT: free to reuse with credit.',
            '数据 <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a>，代码 MIT：注明出处即可转载使用。')
    disc = L('Independent project, not affiliated with ACM, SIGCHI, AAAI or any organization listed. Compiled by hand from public pages; amounts are lower-bound estimates.',
             '独立项目，与 ACM、SIGCHI、AAAI 及所列机构无关。名单根据公开网页手工整理，金额为估算下限。')
    fixl = (L(f'Spot an error? <a href="{issues}" target="_blank" rel="noopener">Open an issue</a>.', f'发现错误？欢迎<a href="{issues}" target="_blank" rel="noopener">提 issue</a>。') if issues else '')
    return f'''
<footer class="site-foot">
  <p>{" · ".join([*who, other])}</p>
  <p>{lic} {disc} {fixl}</p>
  {views}
</footer>'''

FOOT_CSS = '''<style>
.site-foot{border-top:1px solid var(--color-border-line);margin-top:1rem;padding-top:1.5rem;color:var(--color-fg-muted);font-size:13px;line-height:1.7;display:flex;flex-direction:column;gap:var(--cds-gap-sm)}
.site-foot p{margin:0;max-width:52rem}
.site-foot b{color:var(--color-fg);font-weight:600;margin-right:.35em}
.site-foot a{color:var(--color-fg);text-underline-offset:2px}
.site-foot .mail{user-select:all}
.site-foot .views{opacity:.75;font-variant-numeric:tabular-nums}
</style>
'''

PAGES = [
    # (source page, output, title, datasets relative to the output page, bilingual, path back to site root)
    ('dashboard/index.html', 'index.html', 'Who Sponsors HCI Conferences',
     {'listings': 'data/sponsor_listings.csv', 'pcy': 'data/per_conference_year.csv', 'prices': 'data/tier_prices.csv'}, True, ''),
    ('dashboard/ai/index.html', 'ai/index.html', 'Who Sponsors AI Conferences',
     {'listings': '../data/ai/ai_sponsor_listings.csv', 'pcy': '../data/ai/ai_per_conference_year.csv', 'prices': '../data/ai/ai_tier_prices.csv',
      'hci_listings': '../data/sponsor_listings.csv', 'hci_pcy': '../data/per_conference_year.csv'}, True, '../'),
]

if __name__ == '__main__':
    if os.path.isdir(DOCS): shutil.rmtree(DOCS)
    shutil.copytree(os.path.join(ROOT, 'data'), os.path.join(DOCS, 'data'))
    # d3 is served from the site itself so the pages load without a third-party CDN
    shutil.copytree(os.path.join(ROOT, 'vendor'), os.path.join(DOCS, 'vendor'))
    for src, out, title, files, bi, back in PAGES:
        body = open(os.path.join(ROOT, src), encoding='utf-8').read()
        body = re.sub(r'<script>(.*?)</script>', lambda m: '<script>(() => {' + m.group(1) + '})();</script>', body, flags=re.S)
        foot = footer(bi, back)
        anchor = '<div class="tip" id="tip"></div>'
        assert anchor in body, src
        body = body.replace(anchor, foot + '\n  ' + anchor, 1)
        flags_src = os.path.join(ROOT, os.path.dirname(src), 'flags.js')
        head = (HEAD.replace('__FILES__', json.dumps(files))
                .replace('https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js', back + 'vendor/d3.min.js').replace('<title>HCI Conference Sponsorship</title>', f'<title>{e(title)}</title>')
                .replace('</head>', FOOT_CSS + '</head>'))
        dest = os.path.join(DOCS, out); os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'w', encoding='utf-8').write(head + body + TAIL)
        shutil.copy(flags_src, os.path.join(os.path.dirname(dest), 'flags.js'))
        print('wrote', os.path.relpath(dest, ROOT))
    open(os.path.join(DOCS, '.nojekyll'), 'w').close()
