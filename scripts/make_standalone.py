"""Wrap dashboard/index.html (written for the Claude Dashboard artifact runtime)
into dashboard/standalone.html, which runs in any browser / on GitHub Pages.

It adds: d3 from a CDN, the design tokens the page uses, and a tiny `dash`
shim that loads the CSV files in ../data and calls the page's onData hooks.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DASH = os.path.join(HERE, '..', 'dashboard')

HEAD = r'''<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HCI Conference Sponsorship</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<style>
:root{
  --font-anthropic-sans: system-ui, -apple-system, "Segoe UI", "PingFang SC", "Noto Sans SC", sans-serif;
  --font-anthropic-serif: Georgia, "Songti SC", "Noto Serif SC", serif;
  --color-fg:#1f1e1d; --color-fg-muted:#6b6a66; --color-bg:#faf9f5; --color-panel:#ffffff; --color-border-line:#e5e3dc;
  --color-ok:#2e7d32; --color-warn:#b26a00; --color-bad:#c62828;
  --cds-chart-grid:#ecebe6; --cds-chart-axis:#c9c7bf; --cds-chart-reference:#9a988f; --cds-chart-muted:#c9c7bf;
  --cds-surface-popover:#ffffff; --cds-border:#e5e3dc; --cds-shadow-popover:0 4px 16px rgba(0,0,0,.12); --cds-text-secondary:#6b6a66;
  --cds-radius:8px; --cds-pad-xs:4px; --cds-pad-sm:8px; --cds-pad-md:12px; --cds-pad-lg:16px; --cds-pad-xl:24px;
  --cds-gap-xs:4px; --cds-gap-sm:8px; --cds-gap-md:16px; --cds-gap-lg:24px; --cds-gap-xl:32px;
  --cds-font-size-caption:12px; --cds-font-size-body:14px; --cds-font-size-heading:16px; --cds-font-size-title:28px;
  --cds-font-weight-medium:600;
}
@media (prefers-color-scheme: dark){
  :root{ --color-fg:#ecebe6; --color-fg-muted:#a3a19a; --color-bg:#1d1c1a; --color-panel:#262523; --color-border-line:#3a3936;
    --cds-chart-grid:#33322f; --cds-chart-axis:#55534e; --cds-surface-popover:#2d2c2a; --cds-border:#3a3936; --cds-text-secondary:#a3a19a; }
}
body{margin:0;background:var(--color-bg);color:var(--color-fg);font-family:var(--font-anthropic-sans);font-size:var(--cds-font-size-body)}
#dash-root{max-width:1200px;margin:0 auto;padding:24px 16px}
a{color:inherit}
.dash-skeleton{color:transparent;background:var(--cds-chart-grid);border-radius:4px}
</style>
<script>
// outside Claude: a plain browser download for the page's export button
window.claude = window.claude || {use: async n => n !== 'downloads' ? null : {save: async ({filename, data}) => {
  const url = URL.createObjectURL(data instanceof Blob ? data : new Blob([data], {type: 'text/csv;charset=utf-8'}));
  const a = document.createElement('a'); a.href = url; a.download = filename; document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000); return {status: 'saved'}; }}};
window.dash = (() => {
  const files = __FILES__;
  const store = {}; const calcs = {}; const subs = [];
  Object.keys(files).forEach(id => { store[id] = {status: 'loading', data: []}; });
  const run = () => {
    Object.entries(calcs).forEach(([id, c]) => {
      const ins = c.inputs.map(i => store[i]);
      store[id] = ins.every(s => s && s.status === 'ok') ? {status: 'ok', data: c.fn(...ins.map(s => s.data))} : {status: 'loading', data: []};
    });
    subs.forEach(fn => { try { fn(); } catch (e) { console.error(e); } });
  };
  Promise.all(Object.entries(files).map(([id, url]) => d3.csv(url)
    .then(rows => { store[id] = {status: 'ok', data: rows, columns: rows.columns}; })
    .catch(e => { store[id] = {status: 'error', data: [], message: String(e)}; })))
    .then(run);
  let t; window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(run, 150); });
  return {
    data: id => store[id] || {status: 'missing', data: []},
    onData: fn => { subs.push(fn); try { fn(); } catch (e) { console.error(e); } },
    calc: (id, c) => { calcs[id] = c; store[id] = {status: 'loading', data: []}; },
    colors: ['#2f6f9f', '#d1793f', '#3f9a6b', '#8b5fb0', '#c7a33a', '#5aa1b8', '#b5565a', '#7a7a72'],
    refresh: () => {}, params: () => ({}), setParams: () => {}, resetParams: () => {}, setLink: () => {},
  };
})();
</script>
</head>
<body>
<div id="dash-root">
'''

TAIL = '''
</div>
</body>
</html>
'''

import json
PAGES = {
    # dashboard folder -> (title, dataset id -> CSV path relative to that folder)
    '': ('HCI Conference Sponsorship', {'listings': '../data/sponsor_listings.csv', 'pcy': '../data/per_conference_year.csv', 'prices': '../data/tier_prices.csv'}),
    'ai': ('AI Conference Sponsorship', {'listings': '../../data/ai/ai_sponsor_listings.csv', 'pcy': '../../data/ai/ai_per_conference_year.csv',
            'prices': '../../data/ai/ai_tier_prices.csv', 'hci_listings': '../../data/sponsor_listings.csv', 'hci_pcy': '../../data/per_conference_year.csv'}),
}

if __name__ == '__main__':
    for sub, (title, files) in PAGES.items():
        d = os.path.join(DASH, sub)
        body = open(os.path.join(d, 'index.html'), encoding='utf-8').read()
        # the artifact runtime gives each <script> its own scope; emulate that
        body = re.sub(r'<script>(.*?)</script>', lambda m: '<script>(() => {' + m.group(1) + '})();</script>', body, flags=re.S)
        head = HEAD.replace('__FILES__', json.dumps(files)).replace('<title>HCI Conference Sponsorship</title>', f'<title>{title}</title>')
        open(os.path.join(d, 'standalone.html'), 'w', encoding='utf-8').write(head + body + TAIL)
        print('wrote', os.path.join('dashboard', sub, 'standalone.html'))
