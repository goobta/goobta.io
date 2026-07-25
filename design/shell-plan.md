# Pitch board — design plan

## The read
This is a **studio pitch board**, not a landing page. Audience of one (Ankur). Its single job:
let him compare five competing visual identities and pick one. Utilitarian-leaning treatment —
polished, real hierarchy, no hero.

**The governing constraint:** the board is about to hold five loud, competing visual identities.
Any identity the *board itself* asserts will fight all five specimens and corrupt the comparison.
So the board's design decision is deliberate self-effacement — its craft goes into being an
impeccable neutral mount, like a gallery wall or a mounted print. That is the one real call here,
and it's why there is no hero, no accent rail, no card ornament.

## Color
Achromatic-with-a-whisper-of-blue. Chosen, not defaulted: a warm neutral would clash with the
phosphor/purple accents coming in the specimens; a fully neutral grey reads unconsidered. Slight
blue bias sits behind everything without taking a side. Shell accent is deliberately desaturated
slate — it must never read as brighter than a specimen.

| token     | light   | dark    | role                          |
|-----------|---------|---------|-------------------------------|
| --ground  | #FBFBFC | #0E1013 | page ground                   |
| --panel   | #FFFFFF | #16191E | dossier surface / stage mount |
| --ink     | #1A1D22 | #EDEFF2 | primary text                  |
| --ink-2   | #5A6069 | #9AA1AB | secondary text (6.13 / 7.31:1)|
| --rule    | #E2E4E8 | #262A31 | hairlines                     |
| --accent  | #2F5D77 | #7FB2CB | links, focus ring, score bar  |

Contrast computed with the real relative-luminance formula, not eyeballed:
- `--ink-2` on `--ground`: **6.13:1** light, **7.31:1** dark — both pass AA for body text.

## Type
No webfont: the CSP blocks font CDNs and I have no face to inline as a data URI, so linking one
would risk a silent fallback. System stacks used deliberately, with tracking and optical sizing
doing the differentiation.
- **Display** — sans stack, 650–700 weight, `letter-spacing: -0.03em`. The studio voice.
- **Body** — same sans, 400, 1.62 leading, ~62ch measure.
- **Utility** — mono for every piece of data: direction ids, scores, contrast ratios, chips.
  `font-variant-numeric: tabular-nums` so scores align in a column and are scannable.

## Layout
Masthead states the brief and the constraints as mono chips. Then one specimen row per direction:
the live preview in a hairline-mounted **stage** (max 560px, min-height 440px — matching the box
the directions were designed against) on the left, its dossier on the right; stacks under 900px.
The stage is intentionally the loudest thing on the page.

## Animation review affordance
Each stage gets a **Replay** control that re-injects the stage's markup to restart CSS animations,
plus an IntersectionObserver that holds injection until the stage first scrolls into view. This is
so the load sequences can actually be judged instead of all firing before he scrolls down.
**This JS lives only in the review board — the Astro site it's pitching stays zero-JS.**

## Cascade discipline
Every shell rule is class-scoped (`.pb-*`). No bare element selectors anywhere in the shell — a
bare `h2` or `a` rule would reach inside the stages and silently corrupt the specimens. Direction
CSS arrives with every selector prefixed `SCOPE`, substituted to `.pb-stage.dN`.
