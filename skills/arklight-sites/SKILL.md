---
name: arklight-sites
description: Build, fix, extend, or debug ARKlight sites (a Python-first static-site compiler, `pip install arklight`, CLI command `arklight`, pinned here to main v0.70.1). Use this whenever the user mentions ARKlight, runs `arklight build`/`arklight new`/`arklight pack`/`arklight deploy`, shares a `site.py` with `Page(...)`/`Site()`/`@site.page(...)`, or asks for a static site, landing page, portfolio, documentation site, dashboard, or small interactive widget "written in Python" that compiles to plain dependency-free HTML/CSS/JS with no client-side Python runtime. Consult this skill before writing or debugging any ARKlight site rather than guessing from the syntax alone — the gotchas and error messages below are not discoverable from the syntax or the error text alone. For "what does a real ARKlight project look like" / "find me an example of X", see the companion `arklight-examples` skill instead.
---

# ARKlight Sites

Pinned to **ARKlight main, v0.70.1** (`github.com/ARKlight-Ecosystem/ARKlight`,
PyPI `arklight==0.70.1` — one patch ahead of the `v0.70.0` this skill
was originally verified against; re-checked hands-on at `0.70.1` and
nothing below changed). Everything here was verified hands-on against
a real install and real third-party ARKlight projects — real builds
run, real errors reproduced, not copied from docs on faith. The
official `ARKlight` repo's own `v0.070.1` release notes now point
AI-assisted developers at this Skills repo directly, so treat this as
the canonical place to update, not a side project. Android/Desktop
packaging and a few newer APIs exist only on the **`alpha`** branch,
which runs ahead of `main` — see the `arklight-examples` skill's
`References/alpha-vs-main-and-data-viz.md` if the user's project needs
alpha specifically. See "Version drift" at the end if the installed
version differs.

## Treat ARKlight as a black box — this is not optional

ARKlight is a piece of software with a real, documented, agent-facing
contract: `arklight --help`, `arklight <command> --help`,
`arklight search <name>`, `docs/Foundational/` (or, per-task, this
skill), and hands-on `arklight build`. That contract is the thing to
use. Reading `arklight/compiler/*.py`, `arklight/parser/*.py`,
`arklight/ir/*.py`, or any other installed-package source file at
runtime, mid-task, is **not** part of normal ARKlight usage and should
not happen by default — same as nobody reads React's reconciler
source to understand `useState`, or Svelte's compiler internals to
write a component. Do it only if the user explicitly asks to inspect
ARKlight's source, or this skill's own "Debugging checklist" runs out
and genuinely requires it as a last resort (and say so, visibly, when
it happens).

This matters for a concrete reason, not a stylistic one: every gotcha,
error message, and schema fact in this file was already verified
against source **once**, up front, by whoever wrote or updated this
skill — that's what the citations like `arklight/ir/schema.py` below
are for. They're settled conclusions an agent can rely on, not an
invitation to go re-derive them per task. Re-reading compiler internals
mid-task to "double check" something this skill already states is
spending the user's tool calls and tokens on work that's already been
done — the correct move is to trust this file (or re-verify it against
the CLI/a real build, which is cheap), not to open the source tree. If
something here turns out to be wrong, that's a bug in the skill to fix
once, not a reason to make source-reading routine going forward.

ARKlight compiles a restricted, Python-flavored authoring syntax into
plain static HTML/CSS/JS. The browser never runs Python, and there's
no `eval`/`new Function`/string-executed-as-code anywhere in the
compiler or the shipped runtime. The single fact that explains almost
every gotcha below:

> **ARKlight parses your entry file as an AST and never executes it
> as Python to discover routes.** It looks for specific *syntax
> shapes* (`Site()`, `@site.page("/...")`), not runtime behavior.
> (Confirmed directly in `arklight/parser/discover.py`: `ast.parse` on
> the entry file's source only, before any user code runs.)

## Getting started

```bash
arklight --version                              # already installed?
pip install arklight                            # if not (needs Python >= 3.10)
ARKLIGHT_ACCEPT_LICENSE=1 arklight build site.py -o ARK --no-open   # build
ARKLIGHT_ACCEPT_LICENSE=1 arklight pack ARK -o mysite.ark           # optional: single-file bundle
arklight search Picture                         # look up a component's exact prop contract
```

That sequence — install, build, optionally pack, and `search` for
anything you're unsure of — covers the large majority of sessions.
`arklight search <name>` is the single highest-leverage command here:
it prints the compiler's own live schema for any component, behavior,
`Action.*`, `Derive.*`, `Predicate.*`, or `PlatformAPI.*` entry, with
typo-tolerant "did you mean" suggestions on a miss — prefer it over
recalling a prop name from memory.

**License, in one line:** `arklight` refuses to run non-interactively
(any scripted/CI/this-session context) without
`ARKLIGHT_ACCEPT_LICENSE=1` set — set it on every invocation here. A
git-checkout `pip install -e .` has a second, separate build-time gate
(`--config-settings=yes-i-agree-to-arklight-license=1`, or the same
env var). Read `LICENSE` (GPLv3 + attribution terms covering the
compiler and its embedded runtime file, not a user's own site source
or output) before setting it in anything meant to be distributed.

**Where the docs live:** a plain `pip install arklight` wheel does
**not** include the `docs/` folder (only the `arklight*` package is
shipped) — `arklight search --retrieve-doc` only works from a source
checkout (`git clone` + `pip install -e .`). From a wheel install, use
the PyPI project page (`pypi.org/project/arklight/`) for the version
history, or read `docs/` directly on GitHub
(`github.com/ARKlight-Ecosystem/ARKlight`). `arklight search <name>`
itself (the schema lookup, not `--retrieve-doc`) works either way —
it reads the installed package, not the `docs/` tree.

## The mental model, in one example

```python
# include <stdlib.ARKlight>

site = Site()

@site.page("/")
def home():
    return Page(
        Heading("ARKlight"),
        State("count", 0),
        Text(Bind("count")),
        Button("Increment", on_click=Action.increment("count")),
        title="Demo",
    )
```

Every entry file follows this shape: a leading
`# include <stdlib.ARKlight>`, `site = Site()`, and one
`@site.page("/route")`-decorated function per route returning a
`Page(...)` tree. Positional args to any component are children;
keyword args are props. Full component/action/derivation vocabulary,
pulled straight from `arklight/ir/schema.py` and `arklight/api.py`
source rather than copied from docs that may lag the code:
`References/component-vocabulary.md`.

## The gotchas that actually burn tool-call cycles

Each one confirmed by hand — built a real site, hit the failure, read
the fix in source.

### 1. The preamble directive is mandatory, not a comment

Every file using ARKlight's built-in vocabulary (`Site`, `Page`,
`Heading`, `State`, `Action`, ...) must start with
`# include <stdlib.ARKlight>` as its first line, above any code
(a docstring counts as code). Omit it and you get `name 'Site' is not
defined` — a plain Python-looking `NameError` with no hint that a
directive is missing. (`from arklight import *` still works but is
retired and logs a build-time notice; always write the include
instead, in *every* file ARKlight loads — the entry file, each
imported project module, and `arklight.config.py` each need their own.)

### 2. Routes need the literal `@site.page(...)` decorator syntax — not a call

```python
@site.page("/")
def home():
    ...
```

`site.page("/")(home)` — calling it like an ordinary higher-order
function, which is valid Python and *looks* equivalent — is **silently
ignored**: the build fails with `No pages registered on 'site'`.
Static discovery recognizes the decorator *syntax shape* in the AST
only; it does not execute your module to see what `site.page(...)`
actually does.

### 3. Route decorators must live in the file passed to `arklight build` — nowhere else

Discovery (`arklight.parser.discover`) only scans the **entry file's**
own source as an AST, before anything executes. A `@site.page(...)`
decorator inside an *imported* module (`pages/home.py`, say) is
silently invisible to that scan, even though the function it
decorates works fine when called directly. The correct pattern,
confirmed in every real multi-file ARKlight project:

```python
# site.py -- the entry file, passed to `arklight build`
# include <stdlib.ARKlight>
from pages.home import home

site = Site()

@site.page("/")          # decorator here, in the entry file
def home_page():
    return home()        # delegates to a plain function defined elsewhere
```

Everything *other* than route registration is ordinary Python —
importing helpers from your own `components/`, `pages/`, `content/`
modules to keep files small is normal and expected; just keep every
`@site.page(...)` itself in the entry file. See
`References/Field-notes-site.py` for a full real example of this
pattern plus `site.style(...)`/`site.style_selector(...)` CSS authoring.

### 4. `State(...)`/`Computed(...)` must be a child of `Page(...)`, not a bare statement

```python
# Wrong -- State(...) here is never attached to the page:
@site.page("/")
def home():
    State("count", 0)
    return Page(Text(Bind("count")))   # "state isn't declared on this page"

# Right -- State(...) is a positional child of Page(...):
@site.page("/")
def home():
    return Page(
        State("count", 0),
        Text(Bind("count")),
    )
```

State belongs to the page the same way `title=` does; ARKlight
discovers it by walking the returned `Page(...)` tree, not by running
statements in order. A `State(...)`/`Computed(...)` call left outside
that tree is simply never declared, and any `Bind(...)`/`bind_value=`
referencing it fails validation with "references state that isn't
declared on this page."

### 5. Over 30 components accept text-only children — nesting a component inside one fails validation

```python
# Wrong -- Code is a component, not text, and Heading is text-only:
Heading(Code("get_user()"))   # "Item can only contain text" — same
                               # rule, raised under whichever text-only
                               # parent you actually used

# Right -- keep text-only components to literal strings/Bind(...):
Heading("get_user()")
```

Confirmed directly against `arklight/ir/schema.py`'s `text_only_children=True`
flag: it's not just `Item` (the one case the official docs site's
gotchas page names) — `Heading`, `Text`, `Button`, `Link`, `Span`,
`Strong`, `Em`, `Code`, `Cite`, `Label`, `Caption`, `Summary`,
`FigCaption`, and 20+ others all carry the same restriction. Any of
them raises the identical validation error when given a non-text
child, not only `Item` — check `arklight search <name>` if unsure
whether a specific component is text-only before nesting something
inside it.

## Authoring patterns

- **Styling**: `class_name=`/`style={...}` on any component;
  `.nav`/`.card`/`.muted`/`.hidden` ship for free. `site.style(name,
  {css-property: value})` registers a new reusable *class* (plain
  dict, never a CSS string). `site.style_selector(selector, {...},
  allow_redefine=False)` goes further — combinators (`.a > .b`),
  grouped selectors (`h1, h2`), bare tag overrides, attribute
  selectors, pseudo-elements/classes including `:hover` and
  `:nth-child(...)` — everything a single flat `.name {}` block can't
  reach. This is the idiomatic way to do a hover state; there is no
  other mechanism for it. A bare-`.name` branch of a `style_selector`
  call gets the same duplicate-name protection `site.style()` has.
- **Responsive layout, no `@media`**: utility classes (`.stack`,
  `.cluster`, `.switcher`, `.grid`, `.sidebar`, `.center`, `.reel`,
  `.fluid-heading`) adapt from the *container's own* measured width,
  not viewport/device queries. `Site(...)` takes matching per-utility
  override kwargs beyond `max_width`/`bg`/`font_family`: `stack_space`,
  `cluster_space`, `sidebar_space`, `sidebar_width`, `switcher_space`,
  `switcher_threshold`, `grid_min`, `grid_space`, `center_gutter`,
  `reel_space` — set once at the site level instead of per-instance
  `style={}` overrides. `.switcher` is the classic "row on wide
  viewports, stacked column on narrow ones" layout, purely from
  container width. `Site(max_width=...)` is a real body-width
  override at this version — don't hand-roll one via a wrapper `<div>`
  custom property; a child element can never widen its own parent, so
  that pattern silently doesn't reach `<body>`.
- **Click behaviors, zero hand-written JS**: `on_click=...` +
  `behavior_target="#id"` is a closed set of **5** built-ins, not just
  the two usually mentioned — confirmed directly against
  `arklight/backend/js/behaviors/`:
  - `"toggle"` / `"scroll-to"` — accordions/disclosures/smooth-scroll.
  - `"copy"` — copies the target's text (or an `Input`/`Textarea`
    value) to the clipboard via `navigator.clipboard.writeText`, with
    a built-in "Copied!" label flash and a graceful fallback message
    if the Clipboard API isn't available.
  - `"paste"` — the read-side mirror of `copy`
    (`navigator.clipboard.readText()`); writing into an
    `Input`/`Textarea` also dispatches a real `input` event, so an
    element with `bind_value=Bind.model(...)` picks the pasted text
    up into `State(...)` automatically, exactly as if it had been
    typed.
  - `"dismiss"` — adds a class (default `hidden`, overridable via
    `data-ark-toggle-class` / the component's own dismiss-class prop)
    to every element matching `behavior_target`, for
    closeable banners/toasts/alerts with no state variable needed.

  All 5 are validated against this fixed vocabulary at build time;
  `arklight search copy` (etc.) prints the authoritative prop/arg
  contract for any one of them.
- **Reactive state**: `State`, `Computed`/`Derive.*`, `Watch`,
  `Show`/`Predicate.*`, `Repeat`/`RepeatItem`, `Action.*` — all a
  closed, described vocabulary (see gotcha #4 for the one rule that
  bites). Display a scalar state value with `Bind("name")` directly as
  a child; `Bind.model(...)` is specifically for two-way input
  binding; `Repeat`/`RepeatItem` is only for list-valued state.
- **Reusable components with their own local state**: `@component(props={...},
  default_style={...}, state={...})` registers a render function as a
  named component (`NavBar(active="home")`, checked against `props=`
  at expansion time, keyword props only). `state={"open": False}`
  gives it **instance-scoped** reactive state — two calls to the same
  component on one page never share one value — referenced exactly
  like page-level `State(...)`: `Bind(...)`, `on_click=Action.*(...)`,
  `bind_class=Bind.when(...)`, `bind_value=Bind.model(...)`, and
  `Show(Predicate.*(...))` all work against it. Worked example (two
  independent counters, verified to build):
  `References/cli-and-examples.md`.
- **Charts and dashboards**: ARKlight has no live charting library and
  never will — it's a permanent non-goal, not a current gap. Two real
  patterns cover "data visualization" requests:
  pre-rendered-image (matplotlib or similar, offline, embedded with
  `Picture`/`Image`) for actual charts, and the native `Meter`/
  `Progress` components for KPI/gauge-style numbers. Full pattern,
  with a real multi-chart dashboard example:
  `References/alpha-vs-main-and-data-viz.md`.
- **Genuinely new client-side JS**: `site.register_script_extension(cls)`
  with a `ScriptExtension` subclass whose `script` attribute is a
  literal `<script>...</script>` string — see the "7 registered
  experimental APIs" section below before reaching for this.
- **`arklight search <n>`** prints the authoritative, exact prop/arg
  contract for any component, behavior, `Action.*`, `Derive.*`,
  `Predicate.*`, or `PlatformAPI.*` entry — faster and more reliable
  than recalling it from memory, with typo-tolerant "did you mean"
  suggestions on a miss.

Full vocabulary table: `References/component-vocabulary.md`. Full CLI
flag reference (`build`/`pack`/`unpack`/`search`/`new`/`pwa`/
`live-streaming`/`deploy`), `arklight.config.py`, and worked
multi-page/state/component examples: `References/cli-and-examples.md`.

## When the closed vocabulary isn't enough: the 7 registered experimental APIs

ARKlight's default surface is **intrinsic-layout-only** — nothing
keyed to viewport width, device class, or browser engine, and no
arbitrary JS. Anything that steps outside that model is registered as
an experimental feature in `arklight/experimental.py`; every use
prints a warning both inline and in an end-of-build summary. There are
exactly **7** registered features at this version — if it's not in
this list, it isn't a sanctioned escape hatch:

| id | What it is | Gate reason |
|---|---|---|
| `css-media-queries` | `Site.media_query(...)` / per-node `responsive_style={...}` | Viewport-keyed, not intrinsic — a **deliberate permanent tradeoff**, not a missing-feature gap |
| `experimental-install-pwa` | `arklight pwa ... --install-button` | Depends on `beforeinstallprompt`, not a web standard, inconsistent browser support |
| `css-import` | `Site.import_style(url)` | Real `@import url(...)`, fetched/applied by the browser at request time, unvalidated by ARKlight; prefer `Page(links=[...])` where possible |
| `raw-postprocess` | `Site.raw_postprocess(fn)` | **Removed.** Calling it only logs a pointer to `script-extension`. Historical registry entry only. |
| `script-extension` | `arklight.backend.script_extension.ScriptExtension`, via `site.register_script_extension(...)` | The real escape hatch for hand-written JS — Svelte-SFC-style `<script>` block only, no `<template>`/`<style>`. Unchecked JS: no `eval`/`new Function`, but also no syntax guarantee. Reach for this only when a gap is structural, not temporary. |
| `provider-integration` | `Site(provider=Provider.declare(name=..., capabilities=[...]))` | Declares an external runtime service. `capabilities` checked against a finalized closed vocabulary (`auth`, `read`, `write`, `subscribe`) + `custom:` escape hatch. No vendor SDK shipped, no network calls made by ARKlight itself — a contract/discovery layer, not a general HTTP client. |
| `provider-scripts` | `Page(scripts=[{"src": "...", ...}])` | Loads a real vendor SDK `<script src>`; also needs the origin in `Site(trusted_script_origins=[...])` or the default `script-src 'self'` CSP blocks it. |

`script-extension` is the one you'll hit in practice for continuous
pointer tracking, canvas, clipboard access, or any platform capability
the closed vocabulary doesn't cover yet (confirmed against real
third-party projects: an Excalidraw-style canvas app,
`ARKlight-Test-Collections/Sketchboard`, puts ~45% of its total lines
inside a single `ScriptExtension` subclass for canvas/pointer
handling — see `References/cli-and-examples.md` for the minimal shape
of that registration). Prefer waiting on a roadmapped upstream feature
over reaching for it when the gap looks temporary rather than
structural. `Provider` is the thing to reach for if the user wants
ARKlight talking to a real backend service — not `script-extension`.

Outside these 7 (plus what's simply not built yet): no
server/database/auth/accounts, no general `fetch`/HTTP primitive, no
large-SPA-style persistent cross-navigation app state, no iOS target.

## Debugging checklist

If `arklight build` reports a page wasn't registered, a name like
`Site`/`Page` is undefined, or state "isn't declared on this page",
check in this order:

1. Is `# include <stdlib.ARKlight>` the first line of the entry file?
2. Is `@site.page("/...")` used as a literal decorator (not a call)?
3. Is that decorator actually in the file passed to `arklight build`,
   not in an imported module? (gotcha #3)
4. Is every `State(...)`/`Computed(...)` passed as a child of the
   returned `Page(...)`, not called as a bare statement first?
   (gotcha #4)
5. Is the failure actually the license gate (`ARKlight license terms
   not accepted` / a non-interactive-input error), not a site bug at
   all? Set `ARKLIGHT_ACCEPT_LICENSE=1` (read `LICENSE` first).
6. For anything else: `arklight build --debug` prints the full Python
   traceback instead of a one-line message.

| Error | Likely cause |
|---|---|
| `name 'X' is not defined` for a component name | Missing `# include <stdlib.ARKlight>` (gotcha #1) |
| `No pages registered on 'site'` | `site.page(...)` called instead of used as `@site.page(...)` (gotcha #2), or the decorator lives in an imported module (gotcha #3) |
| `"<state> isn't declared on this page"` | `State(...)` called as a bare statement instead of a `Page(...)` child (gotcha #4) |
| `"Item can only contain text"` (or the same message naming another component) | A component nested inside one of the 30+ text-only components — `Heading`, `Text`, `Button`, `Link`, `Span`, `Code`, `Strong`, etc., not only `Item` (gotcha #5) |
| `PreambleCollisionError` | Two `# include`s bind the same name differently, or your own code rebinds a name the preamble already bound |
| `BracketIndentationError` | A continuation line inside `(`/`[`/`{` isn't indented further than its opener, or nesting exceeds 8 levels |
| Component called with positional args, `ComponentError` | A `@component(...)`-registered component takes **keyword props only** — `Stat(label="x")`, never `Stat("x")` |
| Build halts on an unresolved link/asset | `Link(href="/typo")` or a `src=`/`favicon=` naming a file not under `assets/`; the narrow legitimate escape is `CONFIG = {"overdrive": True}` in `arklight.config.py` for a path a server genuinely supplies at runtime — not a default fix |

## Reference projects

For real, cloned-and-inspected third-party ARKlight projects (which
one to look at for a given pattern, their GitHub links, and — this
matters — how out of date each one's pinned ARKlight version is), see
the companion **`arklight-examples`** skill rather than duplicating
that index here. Short version: `Field-Notes` and `Sketchboard`
(`ARKlight-Test-Collections` org) are current enough to trust as-is;
the rest range from "mostly fine" to "30+ releases behind and
documenting workarounds for bugs that are long since fixed upstream"
— don't copy a pattern from an older example without checking it
against the CLI/compiler behavior you actually have installed.

## Version drift

If `arklight --version` doesn't report `0.70.1`, the five gotchas
above likely still hold (they're structural to the AST-only design),
but the experimental-feature list, CLI surface, and `Site(...)` kwargs
may have changed — re-check `arklight/experimental.py` and
`arklight/api.py`'s `Site.__init__` in the installed version's source,
or `PROGRESS.md`'s Snapshot table, rather than assuming this file is
current. If the user is specifically on an older **`alpha`** checkout,
the `arklight-examples` skill's
`References/alpha-vs-main-and-data-viz.md` documents how fast that
branch moves relative to `main` and what to re-check before trusting
any alpha-only feature claim. This isn't hypothetical: every example
project this skill set has inspected pins a different version, and the
oldest ones (~`v0.037`–`v0.054`) still document manual workarounds
(asset copying, "no custom CSS classes," "no asset-existence check")
for gaps the compiler closed version ago — check the installed
version's own source before trusting an example's claim about what
ARKlight can't do.
