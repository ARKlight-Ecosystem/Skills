# ARKlight CLI reference and worked examples

## CLI reference

**License gate** — see SKILL.md's Setup section; set
`ARKLIGHT_ACCEPT_LICENSE=1` for any non-interactive/scripted use.

### `arklight build`

```bash
arklight build <entry.py> [-o OUTPUT_DIR] [--open | --no-open] [--verbose] [--debug] [--narrate]
    [--max-width VALUE] [--bg VALUE] [--font-family VALUE] [--button-text VALUE] [--lang TAG]
    [--emit-arklight[=PATH]]
```

- `entry.py` must define `site = Site()` and at least one
  `@site.page("/route")`-decorated function, both in that same file
  (see SKILL.md gotcha #3).
- `-o, --output` — output directory, default `ARK/`.
- A top-level `assets/` folder next to `entry.py` is copied into
  `<output>/assets` automatically.
- `--open` (default) opens `index.html` after building; always pass
  `--no-open` from an automated/headless context.
- `--verbose` prints each pipeline stage as it runs; `--debug` implies
  `--verbose` and prints the full Python traceback on failure instead
  of a one-line message — reach for this first when an error isn't
  self-explanatory.
- `--narrate` — same progress, as `[Rei] ...` narrated sentences
  instead of `[ARKlight] ...` lines. Mutually exclusive with
  `--verbose`/`--debug`. Deterministic, no network/LLM involved.
- `--max-width`/`--bg`/`--font-family`/`--button-text`/`--lang` —
  override the matching `Site(...)` tokens from the command line
  without editing the site file (e.g. for a CI variant build).
- `--emit-arklight[=PATH]` — also writes the compiled IR as a binary
  `.arklight` snapshot. Rarely needed for ordinary site work.
- **Overdrive escape hatch** (`arklight.config.py`, not a flag): by
  default the build halts on any internal link or asset it can't
  resolve. `CONFIG = {"overdrive": True}` lets through only the two
  categories that are genuinely unverifiable at build time (a route or
  asset a server might supply at runtime) — a typo'd route or a
  missing `assets/` file stays fatal regardless. Not a general way to
  silence link-check errors.

After a successful build, the CLI prints a one-line summary and every
file written:

```
ARKlight v0.70.0 built 5 file(s) -> ARK/
  ARK/index.html
  ARK/about.html
  ARK/styles.css
  ARK/arklight.js
  ARK/sbom.txt
```

Two more things print unconditionally when they apply (not gated
behind `--verbose`): experimental-feature warnings (see SKILL.md's
7-entry table) and `[ARKlight LIMITATION]` warnings.

### `arklight pack` / `arklight unpack`

```bash
arklight pack <build-dir> [-o OUTPUT.ark] [--plain] [--passphrase PASSPHRASE]
arklight unpack <bundle.ark> [-o OUTPUT_DIR] [--passphrase PASSPHRASE]
```

Packs an existing build output directory into a single `.ark` file: an
HTML/archive polyglot that opens directly as a web page *and* contains
the full build as an archive. **Sealed by default** (opaque to generic
archive tools) — `--passphrase` derives a real confidentiality key;
`--plain` opts out for a freely-openable ZIP tail. `unpack` reverses
it, auto-detecting sealed vs. plain.

### `arklight search`

```bash
arklight search <name> [--limit N] [--near NAME] [--accept]
arklight search --serve
arklight search --retrieve-doc [index | --<folder> [--file NAME] [--section QUERY]] [--color auto|always|never]
```

The authoritative lookup for a component/behavior/`Action.*`/
`Derive.*`/`Predicate.*`/`PlatformAPI.*` entry's exact prop/arg
contract — faster and more reliable than recalling it from memory.
Checked in order: built-in components → project's own `@component`s →
`on_click`/`on_reveal` behaviors → `Action.*` → event modifiers →
`Derive.*` → `Predicate.*` → `PlatformAPI.*`. A dotted authoring form
(`Action.increment`) and its bare registry key (`increment`) resolve
to the same entry. On a miss, prints up to 5 typo-tolerant "did you
mean" suggestions.

```bash
arklight search Picture
arklight search pictur            # -> "Did you mean: Picture, PictureSource?"
arklight search toggle            # on_click behavior
arklight search Derive.sum
arklight search notify            # PlatformAPI.notify, incl. permissions + backends
```

`--retrieve-doc` switches to doc-tree retrieval: prints exact,
unmodified `docs/` contents (source checkout only, not a plain
`pip install`).

### `arklight new`

```bash
arklight new <name> [--template simple|production] [--dir PATH] [--explain-architecture]
```

Scaffolds a new project. `simple` (default) is a single `site.py`.
`production` adds `components/`/`pages/`/`content/`/`assets/` for a
site that outgrows one file — route decorators still only go in the
entry file (gotcha #3). `--explain-architecture` prints guidance on
structuring a larger project (can run alone, no `name`).

### `arklight pwa`

```bash
arklight pwa <build-dir> --name "My Site" [--short-name NAME] [--start-url URL]
    [--theme-color COLOR] [--background-color COLOR]
    [--display standalone|fullscreen|minimal-ui|browser]
    [--icon SRC:SIZES[:TYPE]]... [--install-button]
```

Turns an existing build directory into an installable PWA
(`manifest.json` + service worker + injected links). `--icon` is
repeatable. Idempotent — safe to re-run after every build.
`--install-button` is EXPERIMENTAL (`experimental-install-pwa`).

### `arklight live-streaming`

```bash
arklight live-streaming --subscribe <entry.py> [-o OUTPUT_DIR] [--host HOST] [--port PORT]
    [--channel [PORT]] [--route ROUTE]
arklight live-streaming --status [entry.py] [--status-pin]
arklight live-streaming --unsubscribe [entry.py]
```

Development-only file-watch + auto-rebuild + live browser reload.
**Blocks the terminal** until `Ctrl-C`/`--unsubscribe` — for the user
to run themselves while editing, not a one-shot command to invoke
here. `--channel` additionally streams a page's live `State` over SSE.

### `arklight deploy`

```bash
arklight deploy [cloudflare] [entry] [-o OUTPUT_DIR] [--name NAME] [--skip-build] [--dry-run]
```

Builds the site, then hands the build directory to Wrangler for a
Cloudflare Workers deploy (only provider today; bare `arklight deploy`
means `arklight deploy cloudflare`). Requires `wrangler` already
installed and logged in — **ARKlight never installs or authenticates
Wrangler** and never runs `npm`. `--dry-run` builds and prints the
exact Wrangler command without running it. `--skip-build` deploys an
existing `--output` directory as-is.

### Misc

```bash
arklight --version
arklight --upgrade-alpha   # git-checkout/editable installs only
arklight --help            # or a bare `arklight` with no subcommand
```

## Worked example: multi-page site with shared nav + toggle

Verified to build cleanly with `arklight build`.

```python
# include <stdlib.ARKlight>

site = Site()


def nav():
    """Plain Python function composition is how reusable pieces work
    in ARKlight -- call another function, splice its return value in.
    No special "include a partial" mechanism is needed for this. The
    current page's nav link is highlighted automatically at runtime."""
    return Container(
        Link("Home", href="/"),
        Link("About", href="/about"),
        class_name="nav",
    )


@site.page("/")
def home():
    return Page(
        nav(),
        Heading("ARKlight"),
        Text("Build websites with Python.", class_name="muted"),
        Container(
            Button(
                "Show details",
                on_click="toggle",
                behavior_target="#more-details",
                toggle_class="hidden",
            ),
            Container(
                Text("Revealed via the built-in toggle behavior -- no hand-written JS."),
                id="more-details",
                class_name="hidden",
            ),
            class_name="card",
        ),
        title="ARKlight",
    )


@site.page("/about")
def about():
    return Page(
        nav(),
        Heading("About", level=2),
        Link("Back home", href="/"),
        title="About",
    )
```

```bash
ARKLIGHT_ACCEPT_LICENSE=1 arklight build site.py -o ARK --no-open --verbose
```

## Worked example: a counter widget (State/Action/Bind pattern)

Verified to build cleanly. This is the idiomatic shape for "small
stateful widget" requests — reach for it instead of `script-extension`.

```python
# include <stdlib.ARKlight>

site = Site()

@site.page("/")
def home():
    return Page(
        State("count", 0),          # must be a Page(...) child -- gotcha #4
        Heading("Counter"),
        Text(Bind("count")),        # scalar display -- plain Bind(...), not Repeat
        Button("-", on_click=Action.decrement("count")),
        Button("Reset", on_click=Action.reset("count")),
        Button("+", on_click=Action.increment("count")),
        title="Counter",
    )
```

## Worked example: a to-do list (State + Repeat + Bind.model pattern)

```python
# include <stdlib.ARKlight>

site = Site()

@site.page("/")
def home():
    return Page(
        State("draft", ""),
        State("tasks", []),
        Heading("To-do"),
        Input(bind_value=Bind.model("draft"), placeholder="New task"),
        Button("Add", on_click=Action.append("tasks", Bind("draft"))),
        Watch("tasks", then=Action.reset("draft")),      # empty the input after adding
        Repeat("tasks", template=lambda: Text(RepeatItem.value())),
        title="To-do",
    )
```

## Worked example: a component with its own instance-scoped state

Verified against a real multi-instance build
(`Rae-ARK/Data_Viz_With_ARKlight_Alpha_Compiler`, `pages/playground.py`)
— two `Counter()` calls on one page, each tracking its own `"count"`
independently, with no manually-threaded state key:

```python
# include <stdlib.ARKlight>

site = Site()

@component(
    props={"label": Prop(default="Live counter"), "start": Prop(default=0)},
    state={"count": 0, "milestone": 5},
)
def Counter(label="Live counter", start=0):
    return Container(
        Text(label, class_name="muted"),
        Heading(Bind("count"), level=2),
        Button("+", on_click=Action.increment("count")),
        Button("Reset", on_click=Action.reset("count")),
        Show(
            Predicate.gte("count", "milestone"),
            Text("Milestone reached!", class_name="muted"),
        ),
    )

@site.page("/")
def home():
    return Page(
        Heading("Two independent counters"),
        Counter(label="First"),
        Counter(label="Second"),    # its own "count" -- clicking this never touches the first
        title="Playground",
    )
```

`props=` are checked at expansion time (unknown/missing props fail the
build with a clear message, not a Python `TypeError`); `state=` gives
each call site its own copy, referenced the same way page-level
`State(...)` is — `Bind(...)`, `on_click=Action.*(...)`,
`bind_class=Bind.when(...)`, `bind_value=Bind.model(...)`, and
`Show(Predicate.*(...))` all work against it directly.

## Worked example: registering a real `script-extension` (the Sketchboard shape)

Minimal real shape, from `ARKlight-Test-Collections/Sketchboard`
(whose actual extension runs to 1,300+ lines of canvas/pointer-gesture
JS — this is the registration skeleton it uses, not the full file):

```python
# include <stdlib.ARKlight>

from arklight.backend.script_extension import ScriptExtension

class SketchboardRuntime(ScriptExtension):
    script = r"""<script>
(function () {
    "use strict";
    function start() {
        var host = document.getElementById("drawing-host");
        if (!host || host.dataset.ready) return;
        host.dataset.ready = "true";
        // ... canvas setup, pointer event wiring, undo history, etc.
    }
    document.addEventListener("DOMContentLoaded", start);
})();
</script>"""

site = Site()
site.register_script_extension(SketchboardRuntime)

@site.page("/")
def home():
    return Page(Container(id="drawing-host"), title="Sketchboard")
```

A `ScriptExtension` subclass's `script` attribute is a literal
`<script>...</script>` string — no `<template>`/`<style>` sections,
unlike a Svelte SFC proper. ARKlight doesn't check the JS inside it
for correctness (no `eval`/`new Function` either, it's just emitted
verbatim) — this is the registered escape hatch of last resort, not a
first choice; see `SKILL.md`'s experimental-APIs section before
reaching for it.

## `arklight.config.py`: project-level overrides

Optional, and every site works fine without one. Must be named exactly
`arklight.config.py` and sit next to the entry file — not searched for
in parent directories; an unrecognized section/key prints a
"did you mean" warning rather than being silently ignored or rejected
outright. Confirmed real shape (from a real project's checked-in,
all-defaults-commented-out file):

```python
# include <stdlib.ARKlight>

CONFIG = {
    # Only read by `arklight live-streaming --subscribe`.
    # "live_streaming": {"host": "127.0.0.1", "port": 8347, "poll_interval": 0.5},

    # Force the Content-Security-Policy on/off for every build from this
    # project, regardless of any individual Site(strict_csp=...).
    # None (the default) means "no override".
    # "csp": {"strict_csp": None},

    # Default build narration when no --verbose/--narrate flag is passed:
    # "plain", "verbose", or "narrate".
    # "rei": {"default_mode": "plain"},

    # Silence experimental-API warnings once you've made peace with one.
    # "experimental": {"heavy_reliance_nudge": True, "devtools_console_reminder": True},

    # The narrow, genuinely-legitimate escape from the build halting on an
    # unresolved link/asset -- see SKILL.md's debugging checklist.
    # "overdrive": True,
}
```
