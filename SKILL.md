---
name: arklight-sites
description: Build, fix, extend, or debug ARKlight sites (a Python-first static-site compiler, `pip install arklight`, CLI command `arklight`, pinned here to main v0.70.0). Use this whenever the user mentions ARKlight, runs `arklight build`/`arklight new`/`arklight pack`/`arklight deploy`, shares a `site.py` with `Page(...)`/`Site()`/`@site.page(...)`, or asks for a static site written in Python that compiles to plain HTML/CSS/JS with no client-side Python runtime. ARKlight's authoring syntax looks like ordinary Python but is statically parsed, not executed — several things that work in normal Python (dynamic route registration, routes declared outside the entry file, bare imports without the preamble) fail silently here. Consult this skill before writing or debugging any ARKlight site rather than guessing from the syntax alone — the gotchas below are not discoverable from error messages.
---

# ARKlight Sites

Pinned to **ARKlight main, v0.70.0** (`github.com/ARKlight-Ecosystem/ARKlight`,
commit `1f536e8`, PyPI `arklight==0.70.0`). Android/Desktop packaging
backends are **not part of `main`** at this version — they exist only
on the alpha branch. If the user is specifically working from alpha
(`arklight android`, `arklight desktop`, `arklight live-streaming`),
say so explicitly and flag that behavior may differ from what's
documented here.

ARKlight compiles a restricted, Python-flavored authoring syntax into
plain static HTML/CSS/JS. The browser never runs Python. The single
fact that explains almost every gotcha below:

> **ARKlight parses your entry file as an AST and never executes it
> as Python to discover routes.** It looks for specific *syntax
> shapes* (`Site()`, `@site.page("/...")`), not runtime behavior.

## The four gotchas that will burn real tool-call cycles

These are confirmed by hand — built real sites, hit each failure,
read the fix in source — not taken from documentation alone.

### 1. The preamble directive is mandatory, not a comment

Every file using ARKlight's built-in vocabulary (`Site`, `Page`,
`Heading`, `State`, `Action`, ...) must start with:

```python
# include <stdlib.ARKlight>
```

Omit it and you get `name 'Site' is not defined` — a plain
Python-looking NameError with no hint that a special directive is
missing.

### 2. Routes need the literal `@site.page(...)` decorator — not a call

```python
@site.page("/")
def home():
    ...
```

`site.page("/")(home)` — calling it like a normal higher-order
function, which is valid Python and *looks* equivalent — is **silently
ignored**. Static discovery recognizes the decorator syntax shape
only; it does not execute your module to see what `site.page(...)`
actually returns or does.

### 3. Route decorators must live in the file passed to `arklight build` — nowhere else

Discovery (`arklight.parser.discover`) only scans the **entry file**
itself. A `@site.page(...)` decorator inside an *imported* module
(`pages/home.py`, say) is silently ignored, even though the function
it decorates works fine when called directly. The correct pattern,
confirmed in every real multi-file ARKlight project:

```python
# site.py -- the entry file, passed to `arklight build`
# include <stdlib.ARKlight>
from pages.home import home

site = Site()

@site.page("/")          # decorator here, in the entry file
def home_page():
    return home()        # delegates to a plain function, defined elsewhere
```

Everything *other* than route registration is ordinary Python —
importing helpers from your own `components/`, `pages/`, `content/`
modules to keep files small is normal and expected.

### 4. There are two separate license gates, and they need two separate answers

- **Build-time** (installing from a git checkout): `pip install -e .`
  stops with a notice unless you pass
  `--config-settings=yes-i-agree-to-arklight-license=1` or set
  `ARKLIGHT_ACCEPT_LICENSE=1` in the environment.
- **Runtime** (first `arklight <command>` invocation): asks
  interactively, or honors the same `ARKLIGHT_ACCEPT_LICENSE=1` for
  non-interactive/CI use.
- A plain `pip install arklight` from PyPI (prebuilt wheel) skips the
  build-time check entirely but still hits the runtime one.
- Read `LICENSE` (GPLv3 + additional attribution terms) before setting
  the env var in anything you intend to distribute — the additional
  terms require an "ARKlight-based" attribution on conveyed copies of
  the compiler itself, but explicitly do **not** extend to a user's
  own site source or compiled output except one specific runtime file.

## Core authoring vocabulary

Closed vocabulary only — no arbitrary JS, no `eval`, no `new
Function`. Full list with exact signatures, pulled directly from
`arklight/ir/schema.py` and `arklight/api.py` source: see
`references/component-vocabulary.md`.

Minimal working example:

```python
# include <stdlib.ARKlight>

site = Site()

@site.page("/")
def home():
    return Page(
        Heading("Hello"),
        State("count", 0),
        Text(Bind("count")),
        Button("Increment", on_click=Action.increment("count")),
        title="Demo",
    )
```

```bash
arklight build site.py -o ARK --no-open
```

## Experimental APIs (the full registered list, v0.70.0)

ARKlight's default surface is **intrinsic-layout-only** — nothing
keyed to viewport width, device class, or browser engine. Anything
that steps outside that model is registered as an experimental
feature in `arklight/experimental.py`, and every use prints a warning
both inline and in an end-of-run summary. There are exactly **7**
registered features at this version — if it's not in this list, it
isn't a sanctioned escape hatch:

| id | What it is | Gate reason |
|---|---|---|
| `css-media-queries` | `Site.media_query(...)` / per-node `responsive_style={...}` | Viewport-keyed, not intrinsic — a **deliberate permanent tradeoff**, not a missing-feature gap (`upstream_candidate=False`) |
| `experimental-install-pwa` | `arklight pwa ... --install-button` | Depends on `beforeinstallprompt`, not a web standard, inconsistent browser support |
| `css-import` | `Site.import_style(url)` | Real `@import url(...)` — fetched and applied by the browser at request time, unvalidated by ARKlight; prefer `Page(links=[...])` where possible |
| `raw-postprocess` | `Site.raw_postprocess(fn)` | **Removed.** Calling it only logs a pointer to `script-extension`. Historical registry entry only. |
| `script-extension` | `arklight.backend.script_extension.ScriptExtension`, via `site.register_script_extension(...)` | The real escape hatch for hand-written JS. Subclass-based; `script` restricted to a Svelte-SFC-style `<script>` block only (no `<template>`/`<style>`). Unchecked JS — no `eval`/`new Function`, but also no syntax guarantee. Expects a `#include <expapilib.ARKlight>` marker comment (warning-only if absent). |
| `provider-integration` | `Site(provider=Provider.declare(name=..., capabilities=[...]))` | Declares an external runtime service (db, auth, API). `capabilities` checked against a **finalized** closed vocabulary (`auth`, `read`, `write`, `subscribe`) + `custom:`-prefixed escape hatch. No vendor SDK shipped, no network calls made by ARKlight. Excluded from the "heavy use = missing feature" nudge — it's a deliberate boundary. |
| `provider-scripts` | `Page(scripts=[{"src": "...", ...}])` | Provider SDK stage 4/6 — loads a real vendor SDK `<script src>`. Also needs the origin added to `Site(trusted_script_origins=[...])` or the default `script-src 'self'` CSP blocks it. Same `upstream_candidate=False` reasoning as `provider-integration`. |

`script-extension` is the one you'll hit in practice for anything
needing continuous pointer tracking, canvas, clipboard access, or
platform APIs the closed vocabulary doesn't cover yet. Prefer waiting
on a roadmapped upstream feature over reaching for it when the gap is
temporary rather than structural — see the reference projects below
for both calls made in real code.

`Provider` (`provider-integration`/`provider-scripts`) is the full
six-rung SDK ladder, **fully shipped as of v0.070** — it's the thing
to reach for if the user wants ARKlight talking to a real backend
service, not `script-extension`.

## Reference projects (ARKlight-Test-Collections, real, kept light)

Genuine third-party ARKlight projects — referenced for patterns, not
vendored in full:

- `references/field-notes-site.py` — clean multi-page `site.py` entry
  file. The clearest real example of gotcha #3 (decorators-in-entry-
  file-only) and of `site.style(...)`/`site.style_selector(...)` CSS
  authoring.
- **Sketchboard** (`github.com/ARKlight-Test-Collections/Sketchboard`)
  — an Excalidraw clone. 1,311 of its 2,945 total lines (44.5%) sit
  inside `script-extension` blocks for canvas/pointer handling — the
  canonical real example of hitting the closed-vocabulary wall on a
  drawing app, verified directly against the file.
- **Clipboard-Reader-For-Markdown-Files** — hits the same wall for
  clipboard access and text-to-speech, same escape hatch.
- **Notepad-for-Linux** — ARKlight frontend + Flask backend, a real
  example of the "ARKlight owns UI, a real backend owns state" split
  the project's own docs recommend.

## Debugging checklist

If `arklight build` reports a page wasn't registered, or a name like
`Site`/`Page` is undefined, check in this order:

1. Is `# include <stdlib.ARKlight>` the first line of the entry file?
2. Is `@site.page("/...")` used as a literal decorator (not a call)?
3. Is that decorator in the file actually passed to `arklight build`,
   not in an imported module?
4. Is the failure actually the license gate (`ARKlight license terms
   not accepted` / non-interactive-input error), not a site bug at
   all? Set `ARKLIGHT_ACCEPT_LICENSE=1` (read `LICENSE` first).

## Version drift

If `arklight --version` doesn't report `0.70.0`, the gotchas above
likely still hold (they're structural to the AST-only design) but the
experimental-feature list and CLI surface may have changed — re-check
`arklight/experimental.py` and `PROGRESS.md`'s Snapshot table in the
installed version's source rather than assuming this file is current.
