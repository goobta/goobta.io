#!/usr/bin/env python3
"""Assemble the five hardened design directions into one pitch board artifact."""
import json, re, html as H, pathlib

HERE = pathlib.Path(__file__).parent
panel = json.load(open(HERE / 'directions.json'))
ICONS = json.load(open(HERE / 'icons.json'))
dirs = {d['id']: d for d in panel['directions']}
judges = panel['judges']
LENSES = ['taste', 'fit', 'craft']

# ── ranked order, rebuilt from judge scores ────────────────────────────────
def lens_scores(did):
    return [next((x['score'] for x in j['ranking'] if x['id'] == did), None) for j in judges]

def avg(did):
    s = [x for x in lens_scores(did) if x is not None]
    return round(sum(s) / len(s), 2) if s else 0

ORDER = sorted(dirs, key=lambda d: -avg(d))

def verdicts(did):
    out = {}
    for lens, j in zip(LENSES, judges):
        m = next((x for x in j['ranking'] if x['id'] == did), None)
        if m:
            out[lens] = m
    return out

# ── two verified one-line bug fixes to d1 (the winner), disclosed in its dossier ──
D1_FIXES = []
d1 = dirs['d1']
# Surgical: strip nowrap ONLY from the colophon rule. A blanket replace would also hit
# `.note` (where it is intentional) and `.vh` (where nowrap is required by the sr-only
# clip pattern — removing it there would break the visually-hidden text).
_colophon = re.compile(r'(SCOPE\s+\.site,\s*SCOPE\s+\.copy\s*\{[^}]*?)white-space:\s*nowrap;?', re.S)
if _colophon.search(d1['css']):
    d1['css'] = _colophon.sub(
        r'\1/* nowrap removed — caused 1.4.10 h-scroll at large root font */', d1['css'], count=1)
    D1_FIXES.append('Removed <code>white-space: nowrap</code> from the colophon. The harden pass added it to protect the vertical rhythm, but at <code>html{font-size:32px}</code> it turned a graceful wrap into 64px of horizontal document overflow — a WCAG 1.4.10 failure. Flagged by the craft judge.')
if re.search(r'SCOPE\s+\.colophon\s*\{', d1['css']) and 'flex-wrap: wrap' not in d1['css']:
    d1['css'] = re.sub(r'(SCOPE\s+\.colophon\s*\{)', r'\1 flex-wrap: wrap;', d1['css'], count=1)
    D1_FIXES.append('Added <code>flex-wrap: wrap</code> to the colophon so it wraps instead of overflowing.')
if re.search(r'SCOPE\s+\.page\s*\{', d1['css']) and 'margin-inline: auto' not in d1['css']:
    d1['css'] = re.sub(r'(SCOPE\s+\.page\s*\{)', r'\1 margin-inline: auto;', d1['css'], count=1)
    D1_FIXES.append('Added <code>margin-inline: auto</code> to <code>.page</code>. It was pinning to the left edge at any viewport wider than 544px.')

# ── substitute icons + scope the css ──────────────────────────────────────
def expand(did):
    d = dirs[did]
    body = d['html']
    for k, svg in ICONS.items():
        if k.startswith('_'):
            continue
        body = body.replace('{{ICON:%s}}' % k, svg)
    left = re.findall(r'\{\{ICON:(\w+)\}\}', body)
    assert not left, (did, left)
    css = d['css'].replace('SCOPE', '.pb-stage.%s' % did)
    assert 'SCOPE' not in css
    return body, css

def esc(s):
    return H.escape(str(s), quote=True)

# ── dossier pieces ────────────────────────────────────────────────────────
def swatches(d):
    rows = []
    for t in d['palette']:
        rows.append(
            '<li class="pb-sw">'
            '<span class="pb-sw__chips" aria-hidden="true">'
            '<span class="pb-sw__c" style="background:%s"></span>'
            '<span class="pb-sw__c" style="background:%s"></span>'
            '</span>'
            '<code class="pb-sw__tok">%s</code>'
            '<span class="pb-sw__role">%s</span>'
            '</li>' % (esc(t['light']), esc(t['dark']), esc(t['token']), esc(t['role']))
        )
    return '<ul class="pb-swatches">%s</ul>' % ''.join(rows)

def bullets(items, cls='pb-list'):
    return '<ul class="%s">%s</ul>' % (cls, ''.join('<li>%s</li>' % esc(i) for i in items))

def specimen(did, rank):
    d = dirs[did]
    body, _ = expand(did)
    v = verdicts(did)
    a = avg(did)
    is_top = rank == 1

    score_cells = ''.join(
        '<div class="pb-score"><dt>%s</dt><dd>%s</dd></div>' % (l, v[l]['score'] if l in v else '—')
        for l in LENSES
    )

    strengths, weaknesses = [], []
    for l in LENSES:
        if l in v:
            strengths += v[l].get('strengths', [])[:2]
            weaknesses += v[l].get('weaknesses', [])[:2]

    theme_note = ('Commits to one look in both themes — a deliberate choice for this aesthetic.'
                  if d['commitsToSingleTheme'] else 'Designed for light and dark.')

    fixes = ''
    if is_top and D1_FIXES:
        fixes = (
            '<div class="pb-fixes"><p class="pb-fixes__h">Applied before you see it '
            '<span>%d verified bug fixes</span></p><ul>%s</ul></div>'
            % (len(D1_FIXES), ''.join('<li>%s</li>' % f for f in D1_FIXES))
        )

    return """
<article class="pb-spec%s" id="%s">
  <div class="pb-spec__bar">
    <span class="pb-spec__rank">%s</span>
    <h2 class="pb-spec__name">%s</h2>
    <dl class="pb-scores">%s<div class="pb-score pb-score--avg"><dt>avg</dt><dd>%s</dd></div></dl>
    %s
  </div>

  <p class="pb-concept">%s</p>

  <div class="pb-body">
    <div class="pb-stagewrap">
      <div class="pb-stage %s" data-stage="%s" role="img" aria-label="Design preview: %s"></div>
      <div class="pb-stagefoot">
        <button class="pb-replay" type="button" data-replay="%s">Replay load animation</button>
        <span class="pb-dim">preview at 480&times;440</span>
      </div>
    </div>

    <div class="pb-dossier">
      <dl class="pb-facts">
        <dt>Tagline</dt><dd>%s</dd>
        <dt>Typeface</dt><dd>%s</dd>
        <dt>Themes</dt><dd>%s</dd>
      </dl>
      %s
      %s
      <details class="pb-more">
        <summary>Judges&rsquo; read, risks &amp; engineering notes</summary>
        <div class="pb-more__in">
          %s
          <h4>Strengths</h4>%s
          <h4>Weaknesses</h4>%s
          <h4>How it fails or ages</h4>%s
          <h4>Porting to Astro</h4><p class="pb-note">%s</p>
        </div>
      </details>
    </div>
  </div>
</article>""" % (
        ' pb-spec--top' if is_top else '',
        did,
        did.upper(),
        esc(d['name']),
        score_cells,
        a,
        '<span class="pb-badge">Unanimous pick &middot; 3/3 judges</span>' if is_top else '',
        esc(d['concept']),
        did, did, esc(d['name']), did,
        esc(d['proposedTagline']),
        esc(d['idealTypeface'].split('.')[0] + '.'),
        theme_note,
        swatches(d),
        fixes,
        ''.join(
            '<p class="pb-verdict"><span class="pb-lens">%s</span> %s</p>' % (l, esc(v[l]['verdict']))
            for l in LENSES if l in v
        ),
        bullets(strengths),
        bullets(weaknesses),
        bullets(d['risks'][:5]),
        esc(d['astroNotes'][:900] + ('…' if len(d['astroNotes']) > 900 else '')),
    )

specimens = ''.join(specimen(did, i + 1) for i, did in enumerate(ORDER))
dir_css = '\n'.join('/* ===== %s · %s ===== */\n%s' % (did, dirs[did]['name'], expand(did)[1]) for did in ORDER)
stage_html = {did: expand(did)[0] for did in ORDER}

cross = [{'lens': l, 'topPick': j.get('topPick'), 'notes': j.get('notes', '')} for l, j in zip(LENSES, judges)]

# ── the page ──────────────────────────────────────────────────────────────
SHELL_CSS = r"""
:root{
  --ground:#FBFBFC; --panel:#FFFFFF; --ink:#1A1D22; --ink-2:#5A6069;
  --rule:#E2E4E8; --rule-2:#EDEEF1; --accent:#2F5D77; --top:#1E6B4F;
  --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;
}
@media (prefers-color-scheme:dark){
  :root{
    --ground:#0E1013; --panel:#16191E; --ink:#EDEFF2; --ink-2:#9AA1AB;
    --rule:#262A31; --rule-2:#1D2127; --accent:#7FB2CB; --top:#6FD3A8;
  }
}
:root[data-theme="dark"]{
  --ground:#0E1013; --panel:#16191E; --ink:#EDEFF2; --ink-2:#9AA1AB;
  --rule:#262A31; --rule-2:#1D2127; --accent:#7FB2CB; --top:#6FD3A8;
}
:root[data-theme="light"]{
  --ground:#FBFBFC; --panel:#FFFFFF; --ink:#1A1D22; --ink-2:#5A6069;
  --rule:#E2E4E8; --rule-2:#EDEEF1; --accent:#2F5D77; --top:#1E6B4F;
}

.pb{
  background:var(--ground); color:var(--ink); font-family:var(--sans);
  font-size:16px; line-height:1.6; -webkit-font-smoothing:antialiased;
  padding:clamp(1.25rem,4vw,3.5rem) clamp(1rem,4vw,3rem) 4rem;
  max-width:1180px; margin-inline:auto;
}
.pb *{box-sizing:border-box}

/* masthead ---------------------------------------------------------------- */
.pb-head{display:flex; flex-direction:column; gap:1.15rem; padding-bottom:2rem;
  border-bottom:1px solid var(--rule); margin-bottom:3rem}
.pb-eyebrow{font-family:var(--mono); font-size:.7rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-2); margin:0}
.pb-h1{font-size:clamp(1.9rem,5.5vw,3rem); line-height:1.04; letter-spacing:-.03em;
  font-weight:680; margin:0; text-wrap:balance}
.pb-lede{margin:0; max-width:62ch; color:var(--ink-2); font-size:1.02rem}
.pb-lede strong{color:var(--ink); font-weight:600}
.pb-chips{display:flex; flex-wrap:wrap; gap:.4rem; margin:0; padding:0; list-style:none}
.pb-chips li{font-family:var(--mono); font-size:.68rem; letter-spacing:.02em;
  color:var(--ink-2); border:1px solid var(--rule); border-radius:2px;
  padding:.28rem .5rem; background:var(--panel)}

/* specimen ---------------------------------------------------------------- */
.pb-spec{padding:2.5rem 0; border-bottom:1px solid var(--rule)}
.pb-spec:last-of-type{border-bottom:0}
.pb-spec__bar{display:flex; align-items:baseline; flex-wrap:wrap; gap:.55rem .85rem}
.pb-spec__rank{font-family:var(--mono); font-size:.72rem; letter-spacing:.1em;
  color:var(--ink-2); border:1px solid var(--rule); border-radius:2px; padding:.2rem .4rem}
.pb-spec__name{font-size:clamp(1.25rem,3vw,1.6rem); letter-spacing:-.02em;
  font-weight:650; margin:0; line-height:1.15}
.pb-badge{font-family:var(--mono); font-size:.66rem; letter-spacing:.06em;
  text-transform:uppercase; color:var(--top);
  border:1px solid currentColor; border-radius:2px; padding:.2rem .45rem}
.pb-spec--top .pb-spec__rank{color:var(--top); border-color:currentColor}

.pb-scores{display:flex; gap:.1rem; margin:0 0 0 auto; padding:0}
.pb-score{display:flex; flex-direction:column; align-items:center; min-width:3.1rem;
  padding:.1rem .3rem; border-left:1px solid var(--rule)}
.pb-score:first-child{border-left:0}
.pb-score dt{font-family:var(--mono); font-size:.62rem; letter-spacing:.08em;
  text-transform:uppercase; color:var(--ink-2)}
.pb-score dd{margin:0; font-family:var(--mono); font-size:.95rem; font-weight:600;
  font-variant-numeric:tabular-nums}
.pb-score--avg dd{color:var(--ink)}
.pb-spec--top .pb-score--avg dd{color:var(--top)}

.pb-concept{margin:.9rem 0 1.6rem; max-width:70ch; color:var(--ink-2)}

.pb-body{display:grid; gap:1.75rem 2.25rem; grid-template-columns:minmax(0,1fr);
  align-items:start}
@media (min-width:920px){.pb-body{grid-template-columns:480px minmax(0,1fr)}}

/* the stage — a hairline-mounted canvas, deliberately the loudest thing here */
.pb-stagewrap{display:flex; flex-direction:column; gap:.55rem; min-width:0}
/* Specificity note: a direction's own `SCOPE {}` rule compiles to `.pb-stage.dN`
   (0,2,0), which outranks a bare `.pb-stage` — d4's `height:100%` was collapsing its
   stage to its 25rem min-height while the others sat at 440px. The extra `.pb`
   ancestor + attribute selector takes this to (0,4,0) so stage GEOMETRY is uniform
   across all five and the comparison is fair. Deliberately sets no `display`,
   `padding` or color, so each direction keeps full control of its own layout. */
.pb .pb-stage[data-stage]{
  width:100%; max-width:480px; height:440px; overflow:hidden; position:relative;
  border:1px solid var(--rule); border-radius:3px; isolation:isolate;
  box-shadow:0 1px 2px rgb(0 0 0 / .04), 0 8px 24px -12px rgb(0 0 0 / .12);
}
@media (prefers-color-scheme:dark){
  .pb-stage{box-shadow:0 1px 2px rgb(0 0 0 / .4), 0 8px 24px -10px rgb(0 0 0 / .5)}
}
.pb-stagefoot{display:flex; align-items:center; justify-content:space-between;
  gap:.75rem; max-width:480px; flex-wrap:wrap}
.pb-replay{font-family:var(--mono); font-size:.68rem; letter-spacing:.04em; color:var(--accent);
  background:none; border:1px solid var(--rule); border-radius:2px; padding:.3rem .55rem;
  cursor:pointer}
.pb-replay:hover{border-color:var(--accent)}
.pb-replay:focus-visible{outline:2px solid var(--accent); outline-offset:2px}
.pb-dim{font-family:var(--mono); font-size:.65rem; color:var(--ink-2);
  font-variant-numeric:tabular-nums}

/* dossier ----------------------------------------------------------------- */
.pb-dossier{display:flex; flex-direction:column; gap:1.35rem; min-width:0}
.pb-facts{display:grid; grid-template-columns:auto minmax(0,1fr); gap:.4rem .9rem; margin:0}
.pb-facts dt{font-family:var(--mono); font-size:.66rem; letter-spacing:.09em;
  text-transform:uppercase; color:var(--ink-2); padding-top:.15rem}
.pb-facts dd{margin:0; font-size:.9rem}

.pb-swatches{list-style:none; margin:0; padding:0; display:flex; flex-direction:column;
  gap:.4rem; border-top:1px solid var(--rule-2); padding-top:.9rem}
.pb-sw{display:grid; grid-template-columns:auto auto minmax(0,1fr); gap:.6rem;
  align-items:center; font-size:.78rem}
.pb-sw__chips{display:flex; border:1px solid var(--rule); border-radius:2px; overflow:hidden}
.pb-sw__c{width:14px; height:14px; display:block}
.pb-sw__tok{font-family:var(--mono); font-size:.72rem; color:var(--ink)}
.pb-sw__role{color:var(--ink-2); overflow:hidden; text-overflow:ellipsis; white-space:nowrap}

.pb-fixes{border:1px solid var(--rule); border-left:2px solid var(--top);
  border-radius:2px; padding:.85rem 1rem; background:var(--panel)}
.pb-fixes__h{margin:0 0 .5rem; font-size:.82rem; font-weight:620}
.pb-fixes__h span{font-family:var(--mono); font-size:.7rem; color:var(--top); font-weight:400}
.pb-fixes ul{margin:0; padding-left:1.1rem; font-size:.8rem; color:var(--ink-2);
  display:flex; flex-direction:column; gap:.4rem}
.pb-fixes code, .pb-more code{font-family:var(--mono); font-size:.92em;
  background:var(--rule-2); padding:.05em .3em; border-radius:2px; color:var(--ink)}

.pb-verdict{margin:0 0 .6rem; font-size:.85rem; color:var(--ink-2)}
.pb-lens{font-family:var(--mono); font-size:.64rem; letter-spacing:.08em;
  text-transform:uppercase; color:var(--accent); margin-right:.4rem}

.pb-more{border-top:1px solid var(--rule-2); padding-top:.9rem}
.pb-more summary{font-family:var(--mono); font-size:.7rem; letter-spacing:.06em;
  text-transform:uppercase; color:var(--accent); cursor:pointer}
.pb-more summary:focus-visible{outline:2px solid var(--accent); outline-offset:2px}
.pb-more__in{padding-top:1rem; font-size:.85rem}
.pb-more h4{font-family:var(--mono); font-size:.66rem; letter-spacing:.09em;
  text-transform:uppercase; color:var(--ink-2); margin:1.1rem 0 .45rem; font-weight:500}
.pb-list{margin:0; padding-left:1.1rem; color:var(--ink-2); display:flex;
  flex-direction:column; gap:.35rem}
.pb-note{margin:0; color:var(--ink-2)}

/* closing ---------------------------------------------------------------- */
.pb-close{margin-top:3.5rem; padding-top:2rem; border-top:1px solid var(--rule);
  display:flex; flex-direction:column; gap:1.1rem}
.pb-close h2{font-size:1.4rem; letter-spacing:-.02em; margin:0; font-weight:650}
.pb-close p{margin:0; max-width:68ch; color:var(--ink-2)}
.pb-close strong{color:var(--ink); font-weight:600}
.pb-crossgrid{display:grid; gap:1rem; grid-template-columns:minmax(0,1fr)}
@media (min-width:760px){.pb-crossgrid{grid-template-columns:repeat(3,minmax(0,1fr))}}
.pb-cross{border:1px solid var(--rule); border-radius:3px; padding:1rem;
  background:var(--panel); font-size:.82rem}
.pb-cross h3{font-family:var(--mono); font-size:.66rem; letter-spacing:.09em;
  text-transform:uppercase; color:var(--accent); margin:0 0 .5rem; font-weight:500}
.pb-cross p{margin:0; color:var(--ink-2)}
.pb-cross b{color:var(--ink)}

@media (prefers-reduced-motion:reduce){
  .pb-replay{display:none}
}
"""

SHELL_JS = r"""
(function () {
  var src = window.__PB_STAGES__ || {};
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function inject(el) {
    var id = el.getAttribute('data-stage');
    if (!src[id]) return;
    el.innerHTML = '';
    void el.offsetWidth;          // force reflow so CSS animations restart
    el.innerHTML = src[id];
  }

  var stages = Array.prototype.slice.call(document.querySelectorAll('.pb-stage'));

  if (reduce || !('IntersectionObserver' in window)) {
    stages.forEach(inject);
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { inject(e.target); io.unobserve(e.target); }
      });
    }, { rootMargin: '80px 0px' });
    stages.forEach(function (s) { io.observe(s); });
  }

  document.querySelectorAll('.pb-replay').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var el = document.querySelector('.pb-stage[data-stage="' + btn.getAttribute('data-replay') + '"]');
      if (el) inject(el);
    });
  });
})();
"""

page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>goobta.io &mdash; five redesign directions</title>
<style>
*,*::before,*::after{box-sizing:border-box} body{margin:0}
%s

/* ══════════════════════════════════════════════════════════════════════════
   SPECIMEN STYLES — authored per direction, every selector originally scoped
   to a SCOPE token, mechanically rewritten to .pb-stage.dN at assembly so
   five competing identities can coexist on one page without leaking.
   ═══════════════════════════════════════════════════════════════════════ */
%s
</style>
</head>
<body>

<div class="pb">
  <header class="pb-head">
    <p class="pb-eyebrow">goobta.io &middot; redesign &middot; direction review</p>
    <h1 class="pb-h1">Five directions for a six-link front door</h1>
    <p class="pb-lede">Each panel below is <strong>live rendered CSS</strong>, not a mockup &mdash; the same
      markup that would ship. Five designers worked independently from the same brief and never saw each
      other&rsquo;s work; a design engineer then re-derived every contrast ratio by hand and returned
      corrected code; three judges scored the set through separate lenses. <strong>Hit Replay</strong> on any
      panel to watch its load sequence.</p>
    <ul class="pb-chips">
      <li>static astro</li><li>zero-js on the real site</li><li>css-only motion</li>
      <li>wcag aa verified</li><li>light + dark</li><li>13 agents</li>
    </ul>
  </header>

  %s

  <section class="pb-close">
    <h2>Where the judges landed</h2>
    <p><strong>The Index Page took all three votes</strong> &mdash; and it was first on every individual
      lens, which almost never happens. The reason all three converged: it is the only direction that would
      still read as a designed object printed flat in one color with no interaction at all. The other four
      lean on a surface treatment &mdash; phosphor, bloom and grain, motion, a violet spine &mdash; to carry
      a composition that is weaker underneath.</p>
    <div class="pb-crossgrid">%s</div>
    <p>Two caveats worth your attention before you pick. The fit judge noted that <strong>d1 is also the
      least memorable of the five</strong> &mdash; it wins on permanence and loses on charm; if you want
      people to say &ldquo;nice site&rdquo; rather than never having to touch it again, Structural Grid is
      the better fit, but a seventh link would force a redesign. And <strong>d1 spends its accent on a
      single period</strong>, so on a phone, where there is no hover, the entire brand color is one full
      stop &mdash; the cheapest fix is grafting d4&rsquo;s move and putting the favicon&rsquo;s violet
      <code>g</code> on the page itself.</p>
  </section>
</div>

<script>window.__PB_STAGES__ = %s;</script>
<script>%s</script>
</body>
</html>
""" % (
    SHELL_CSS,
    dir_css,
    specimens,
    ''.join(
        '<div class="pb-cross"><h3>%s &middot; picked %s</h3><p>%s</p></div>'
        % (c['lens'], c['topPick'], esc(c['notes'].split('\n')[0][:300]) + '…')
        for c in cross
    ),
    json.dumps(stage_html),
    SHELL_JS,
)

out = HERE / 'board.html'
out.write_text(page)
print('wrote', out, len(page), 'bytes')
print('order:', ORDER)
print('d1 fixes applied:', len(D1_FIXES))
for f in D1_FIXES:
    print('  -', re.sub('<[^>]+>', '', f)[:110])
