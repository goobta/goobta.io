# goobta.io — redesign direction review

Design exploration for the goobta.io landing page redesign. **Nothing here is wired into the
site yet** — `src/` is untouched. This is the pitch stage: five directions were produced, QA'd,
and ranked so one can be chosen and then implemented.

## Look at this first

Open [`board.html`](board.html) in a browser. Every panel is **live-rendered CSS**, not an
image — the same markup that would ship. Each has a *Replay* button to watch its load
animation.

## Results

| Direction | avg | taste | fit | craft | top-pick votes |
|---|---|---|---|---|---|
| **The Index Page** (`d1`) | 8.17 | 8.5 | 8 | 8 | 3/3 |
| **Structural Grid** (`d4`) | 6.5 | 7.5 | 7 | 5 | 0/3 |
| **Prompt Line** (`d2`) | 5.83 | 4.5 | 6 | 7 | 0/3 |
| **Kinetic Minimal** (`d5`) | 5.67 | 6 | 4.5 | 6.5 | 0/3 |
| **Depth and Grain** (`d3`) | 5.17 | 5.5 | 3 | 7 | 0/3 |

**The Index Page (`d1`) won unanimously** — first on every individual lens and 3/3 top-pick
votes, which is unusual for a panel this adversarial. The stated reason all three judges
converged: it is the only direction that would still read as a designed object printed flat in
one color with no interaction at all. The other four lean on a surface treatment (phosphor,
bloom + grain, motion, a violet spine) to carry a weaker underlying composition.

## How this was produced

1. **5 designers**, working independently from one brief, never seeing each other's work.
2. **5 QA passes** — one per direction. Each re-derived every WCAG contrast ratio by hand,
   checked CSS scoping and keyframe collisions, and returned corrected code.
3. **3 judges**, each with a single lens (visual taste / fitness-for-purpose / front-end
   craft), ranking the whole set.

13 agents total. Full per-direction data — palettes with measured contrast ratios, risks,
QA reports, and Astro porting notes — is in [`directions.json`](directions.json).

## Known issues, not yet fixed

Carried forward from the judges so they don't get lost:

- **`d1` accent is too thin.** At rest on a phone (no hover) the entire brand color is one
  period glyph. Cheapest fix is grafting `d4`'s move: put the favicon's violet `g` on the page.
- **`d1` is the least memorable of the five.** It wins on permanence and loses on charm. If
  the priority is "nice site" over "never touch it again", `d4` fits better — but a seventh
  link would force a `d4` redesign.
- **`d4` ordinals are column-major** — they render 01, 04 / 02, 05 / 03, 06, so the numbering
  defeats itself. Must go row-major or drop the ordinals.
- **`d2`/`d3` don't declare `color-scheme: dark`** while `Base.astro` declares `light dark`,
  so UA scrollbars would render light against near-black.
- **The `:root[data-theme=...]` blocks are preview scaffolding.** The real site has no theme
  toggle and no JS; on port they must collapse to a single `prefers-color-scheme` query or
  they will drift.
- **Venmo mark.** The current asset draws its `V` as SVG `<text>` with `font-family` as a
  presentation attribute, so it renders as Georgia bold-italic among five geometric marks —
  and differently per platform. `icons.json` here substitutes a hand-authored path as a
  stopgap; the real fix is a drawn path (or a proper Venmo icon) in `index.astro`.

## Bugs already fixed in `d1`

Three verified one-liners, applied before the board was rendered and disclosed on the board
itself:

- Removed `white-space: nowrap` from the colophon — at `html{font-size:32px}` it turned a
  graceful wrap into 64px of horizontal overflow (WCAG 1.4.10).
- Added `flex-wrap: wrap` to the colophon.
- Added `margin-inline: auto` to `.page` — it was pinning left above 544px viewports.

## Reproducing the board

```bash
python3 assemble.py   # reads panel data + icons.json -> board.html
```

`assemble.py` substitutes the six real icon SVGs for `{{ICON:name}}` placeholders and
rewrites each direction's `SCOPE` selector token to `.pb-stage.dN`, so five competing visual
identities coexist on one page without leaking into each other.

## Next step

Pick a direction, then implement it in `src/layouts/Base.astro` (token layer) and
`src/pages/index.astro` (markup). Each direction's `astroNotes` field in `directions.json`
describes how it maps onto those two files and what changes at true full-viewport scale.
