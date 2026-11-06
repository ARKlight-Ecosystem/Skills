---
name: arklight-examples
description: Find a real, working ARKlight project to use as a pattern reference — "show me a real example", "has anyone built X in ARKlight", "is there a project using the alpha branch", or when writing/fixing ARKlight code and a citable real-world precedent would help beyond the synthetic examples in the `arklight-sites` skill. Also the place to find links to the official ARKlight project, its documentation site, and the live deployed docs site. Use alongside `arklight-sites`, not instead of it — this skill is an index of where to look, not the authoring reference itself.
---

# ARKlight: ecosystem & first-party examples

An index of real ARKlight projects and official project links, verified
by cloning/fetching directly — not assumed from a repo name or
description alone. Every entry below notes **when it was last checked
against the installed version** so a stale claim doesn't get repeated
as current. Current ARKlight is `v0.70.1`.

## Official project links

| What | Link |
|---|---|
| Compiler source | `github.com/ARKlight-Ecosystem/ARKlight` |
| This skill repo | `github.com/ARKlight-Ecosystem/Skills` |
| Official website source (built *in* ARKlight, pinned to v0.70.1) | `github.com/ARKlight-Ecosystem/ARKlight.dev` |
| Official website, live | `arklight.arklight-compiler.workers.dev` |
| PyPI package | `pypi.org/project/arklight/` |

`ARKlight.dev`'s own README is explicit about scope: it covers "what
is it, how do I start, what are the rules, what are the limits" and
deliberately does **not** try to be a full docs site — for anything
deeper, the `docs/Foundational/` tree in the compiler repo itself is
still the primary source. Its own honest-gaps note also says the
layout was verified from generated HTML output, not by eyeballing it
in a real browser — worth knowing before treating its rendered pages
as a pixel-perfect reference.

## First-party examples: `ARKlight-Test-Collections` org

All 7 repos in this org use ARKlight somewhere, even the ones whose
primary language tag (Kotlin, C++, TypeScript) makes that non-obvious
from the repo list alone — check the actual tree, not just the
language badge, before assuming a repo isn't relevant.

| Repo | What it's for | ARKlight version signal | Trust level |
|---|---|---|---|
| [`Field-Notes`](https://github.com/ARKlight-Test-Collections/Field-Notes) | Multi-page product-catalog site | Labeled "made with ARKlight v0.70.0" | **Current** — primary reference for gotcha #3 (route decorators in entry file) and `site.style(...)`/`site.style_selector(...)` CSS, vendored in full at `arklight-sites/References/Field-notes-site.py` |
| [`Sketchboard`](https://github.com/ARKlight-Test-Collections/Sketchboard) | Excalidraw-style drawing app | No inline version string; structurally current (uses `ScriptExtension`, `register_script_extension`) | **Current** — canonical `script-extension` example, ~45% of its 1,311-line runtime file is hand-written JS for canvas/pointer handling |
| [`Product-Showcase`](https://github.com/ARKlight-Test-Collections/Product-Showcase) | Phone comparison/catalog site | README pins `arklight 0.37`; comments reference `v0.003`–`v0.042` | **Old — ~30+ releases behind.** Documents workarounds (manual `assets/` copy, "ARKlight has no custom CSS class mechanism," "no asset-existence check") for things the compiler now does natively. Don't copy its workarounds; the *shape* of its service-oriented layout (`components/`, `pages/`, `content/`, `content/validate.py`) is still fine to reuse. |
| [`News-Website`](https://github.com/ARKlight-Test-Collections/News-Website) | News/article site | Comments reference `v0.010`, `v0.048`, `v0.054` | **Old.** Same caveat as Product-Showcase — check any claimed limitation against the current compiler before repeating it. |
| [`Clipboard-Reader-For-Markdown-Files`](https://github.com/ARKlight-Test-Collections/Clipboard-Reader-For-Markdown-Files) | Clipboard → rendered Markdown reader | Comment references `v0.0438` | **Old-ish**, but the pattern it demonstrates (clipboard access + text-to-speech via `script-extension`) is still the correct escape hatch today |
| [`Notepad-for-Linux`](https://github.com/ARKlight-Test-Collections/Notepad-for-Linux) | Linux notepad app, ARKlight frontend + Flask backend | No version markers found | Architecture-level reference: "ARKlight owns UI, a real backend owns state" — the pattern to recommend over faking a backend with `script-extension` |
| [`Petit-Four`](https://github.com/ARKlight-Test-Collections/Petit-Four) | Video-sharing app, Kotlin + Flask backend + `src/ARKlight-Frontend/` | No version markers found | Another frontend/backend split example; not yet deeply inspected — check before citing specifics |

## `Rae-ARK` personal account: not citable examples

Not ready for prime time — skip for reference/examples. `Rae-ARK/ARKlight`
is a 2-commit stub (README only, no package code); treat
`ARKlight-Ecosystem/ARKlight` as the only canonical compiler repo.
`Rae-ARK/Product-Showcase` is the same repo as
`ARKlight-Test-Collections/Product-Showcase` under a transfer redirect —
use that link, not this one. The rest
(`ARKlight-Experiemental-Env`, `C_ARKlight`, `ARKlight-Teachers-Kit`)
are unrelated side projects or design-doc-only, not build patterns.

Chart/dashboard and `alpha`-branch example:
[`ARKlight-Ecosystem/Data_Viz_With_ARKlight_Alpha_Compiler`](https://github.com/ARKlight-Ecosystem/Data_Viz_With_ARKlight_Alpha_Compiler)
(confirmed live). Full pattern in `References/alpha-vs-main-and-data-viz.md`.

## How to use an example safely

1. Check the version signal (inline comments, README, repo
   description) before trusting anything the project *says* about
   ARKlight's limits — several of the above are old enough that their
   documented workarounds are now obsolete.
2. Prefer `Field-Notes` and `Sketchboard` when a pattern needs to be
   current; treat the others as "architecture is probably still fine,
   specific limitation claims need re-checking."
3. A project's own code comment claiming a gap ("ARKlight does not
   check X") is a claim about the version *that project* was built
   against, not about the version currently installed — verify with
   `arklight --version` and, if needed, a real build, same as this
   skill set's own methodology throughout. That verification stays at
   the CLI/build level — it is not license to go read
   `arklight/ir/*.py` mid-task; see `arklight-sites/SKILL.md`'s
   "Treat ARKlight as a black box" section, which applies here too.

Full `alpha`-branch-vs-`main` methodology and the chart/dashboard
pattern (matplotlib-PNG-via-`Picture` + `Meter` KPIs for
"data visualization" requests): `References/alpha-vs-main-and-data-viz.md`.
