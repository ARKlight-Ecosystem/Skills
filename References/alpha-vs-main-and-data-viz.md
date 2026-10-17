# The `alpha` branch, and building charts/dashboards in ARKlight

Both topics come from the same real project,
`Rae-ARK/Data_Viz_With_ARKlight_Alpha_Compiler` — an 11-page
"ARKlight vs. traditional frontend frameworks" comparison site, built
*in* ARKlight, shipped as a sealed `.ark` bundle. Cloned and read
directly, not summarized from its own claims alone.

## `alpha` moves faster than `main` — don't trust a stale feature table

ARKlight develops on an `alpha` branch that lands features before
`main` picks them up, sometimes much later. The project above tracked
this live across several re-checks of its own compatibility table, and
every feature it once called "alpha-only" (`Site.style`, `Page(...)`
head metadata, `arklight search`/`--help`) **eventually shipped on
`main` too** — except one: `component(...)`/`Prop`/`ComponentState`
(the "user-defined, reusable components" milestone), which **did**
reach `main` by the time this skill's own v0.70.0 pin was checked (see
`SKILL.md`'s "Reusable components with their own local state" bullet).

The takeaway isn't any specific version number — those are already
stale by the time you read this — it's the **method**: never trust a
remembered "X is alpha-only" claim without checking the *installed*
version's own source. The project's own
`services/compatibility.py` does exactly this at import time: it
inspects whatever ARKlight is actually installed for the specific
names a build needs (not `arklight.__version__`, which doesn't by
itself tell you which features shipped) and fails fast with a clear
message — `"This site (site.py) requires ARKlight's 'alpha'
branch..."` plus the exact fix — instead of a raw `AttributeError`
partway through a build. That pattern (a feature-presence guard, not a
version-number guard) is worth reusing in any ARKlight project that
depends on something not yet confirmed to be on every target branch.

To build against `alpha` specifically:

```bash
git clone --branch alpha https://github.com/ARKlight-Ecosystem/ARKlight.git
cd ARKlight
pip install -e .   # same two-gate license flow as main, see SKILL.md Getting started
```

A plain `pip install arklight` from PyPI is always the `main` line —
if a site needs an alpha-only feature, PyPI alone won't build it;
clone alpha and install editable instead.

One real, still-useful gotcha from this project's build, independent
of either branch's version number: **a module-level import can behave
differently from the same import written inside a page function**,
because ARKlight's compiler runs a site's top-level code and its page
functions in different pipeline stages. If a value computed from an
import looks right at module scope but wrong (or missing) inside a
`@site.page(...)` function, that staging split — not a typo — is the
first thing to check.

## Data visualization and dashboards: the actual pattern

ARKlight has **no live charting library and never will** — accepting
arbitrary rendering JS is a permanent non-goal of the project, the
same way `css-media-queries` is a deliberate tradeoff rather than a
gap (see `SKILL.md`'s experimental-APIs table). A request for "a chart"
or "a dashboard" has exactly two real building blocks, both already
in ARKlight's closed vocabulary:

1. **Pre-rendered images for actual charts.** Generate the chart
   offline with a real plotting library (matplotlib, in the reference
   project) in a separate script, drop the PNG into `assets/`, and
   embed it with `Picture`/`Image` like any other image. ARKlight never
   touches the plotting library directly — it only ever sees the
   finished image file. This is a genuine two-step process (chart
   generation, then a normal ARKlight build), not a shortcut:

   ```python
   # generate_assets.py -- run once, separately, before `arklight build`
   import matplotlib.pyplot as plt
   from data import BUNDLE_SIZES

   fig, ax = plt.subplots()
   ax.bar(BUNDLE_SIZES.keys(), BUNDLE_SIZES.values())
   fig.savefig("assets/bundle-size-bar.png", dpi=200, bbox_inches="tight")
   ```

   ```python
   # site.py -- include <stdlib.ARKlight> preamble omitted here for brevity
   Picture(
       PictureSource(srcset="assets/bundle-size-bar.png"),
       Image(src="assets/bundle-size-bar.png", alt="Bundle size by framework"),
   )
   ```

2. **`Meter`/`Progress` for native KPI numbers.** For a single
   value-against-a-range reading (a percentage, a score, "12 of 50"),
   ARKlight already has zero-JS schema support — no image step needed:

   ```python
   Container(
       Text("Adoption", class_name="muted"),
       Heading("64%", level=2),
       Meter("adoption", value=64, min=0, max=100),
       class_name="kpi-card",
   )
   ```

   A row of these (one `Container`+`Meter` pair per metric) is the
   idiomatic "KPI strip" at the top of a dashboard page — see
   `components/meters.py` in the reference project for the exact
   reusable-function shape (a plain Python helper, not a `@component`,
   though either works).

A build that mixes both — `Meter` strips for live-feeling numbers,
matplotlib PNGs for anything that needs an actual plotted shape (bars,
pies, lines) — covers the overwhelming majority of "data visualization
in ARKlight" requests. If a request specifically needs *live*,
interactive charting (hover tooltips, client-side filtering of chart
data), say plainly that ARKlight doesn't support that and the nearest
honest alternative is a static image regenerated at build time, not a
`script-extension` workaround — a hand-rolled canvas charting library
inside unchecked JS is exactly the kind of "temporary-looking but
actually structural" gap `SKILL.md`'s experimental-APIs section warns
against reaching for.

### `component(state={...})`, if targeting `alpha` and `main` predates it

`main` v0.70.0 already has `component(..., state={...})` (see
`SKILL.md`). If working against an older `main` that doesn't, this was
an `alpha`-only feature for a while — the reference project's
`/playground` page is the real worked example (two independent
`Counter()` instances, each with its own `"count"` value, built with
zero manual state-key plumbing). Full source in that project's
`pages/playground.py`, the same `@component(props={...}, state={...})`
shape documented in `References/cli-and-examples.md` here.
