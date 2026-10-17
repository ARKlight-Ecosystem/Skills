# ARKlight component vocabulary (v0.70 / main branch)

Generated/cross-checked directly against `arklight/ir/schema.py` (the
closed node registry) and `arklight/api.py` (reactive/interactive
functions + classes) from a clone of `github.com/ARKlight-Ecosystem/ARKlight`
(main, commit `1f536e8`) — not copied from docs that may lag the code.
Everything here is bound into scope by `# include <stdlib.ARKlight>`.
Positional args are children; keyword args are props. When unsure
whether a prop is required or whether a component accepts children,
`arklight search <Name>` prints the authoritative, live answer from
the compiler's own schema — faster and safer than this table alone for
anything subtle.

## Structural / HTML-tag components

`Page` is required as the root of every route's return value.
"Text-only" means a component may only contain plain strings, not
nested components (enforced at build time).

**Structure & layout**

| Component | Renders as | Notes |
|---|---|---|
| `Page` | -- | Root node every page function must return |
| `Container` | `<div>` | Generic grouping element |
| `Header` / `Footer` / `Main` | `<header>`/`<footer>`/`<main>` | |
| `Nav` | `<nav>` | Its `<a>` children get an automatic `is-active` class on the current page |
| `Section` / `Article` / `Aside` / `Figure` | matching tags | |
| `FigCaption` | `<figcaption>` | Text-only |
| `Details` / `Summary` | `<details>`/`<summary>` | `Summary` text-only |
| `Dialog` | `<dialog>` | Zero-JS |

**Text & typography** (all text-only unless noted)

`Heading` (`<h1>`-`<h6>`, `level=1..6`), `Text` (`<p>`), `Strong`,
`Em`, `Small`, `Mark`, `Code`, `Cite`, `Abbr`, `Dfn`, `Sub`, `Sup`,
`Span`, `Time`, `Kbd`, `Samp`, `Var`, `Data` (requires `value`), `Q`,
`Bdi`, `Bdo`, `Rt`, `Rp` -- plus `HorizontalRule`/`LineBreak`/`Wbr`
(no children), and `Pre`/`Blockquote`/`Ins`/`Del`/`Address`/`Ruby`
(allow children).

**Links & media**

| Component | Renders as | Notes |
|---|---|---|
| `Link` | `<a>` | Text-only. Requires `href` -- internal routes checked at build time |
| `Image` | `<img>` | No children. Requires `src`, checked against `assets/` |
| `Video` / `Audio` | matching tags | |
| `Source` | `<source>` | No children. Requires `src` |
| `Picture` / `PictureSource` | `<picture>`/`<source>` | `PictureSource` requires `srcset`, no children |
| `Track` | `<track>` | No children. Requires `src` |
| `Map` / `Area` | `<map>`/`<area>` | `Map` requires `name`; `Area` no children |
| `IFrame` | `<iframe>` | No children. Requires `src` |

**Lists**: `List` (`<ul>`), `OrderedList` (`<ol>`), `Item` (`<li>`,
text-only), `DescriptionList`/`DescriptionTerm`/`DescriptionDetails`
(`<dl>`/`<dt>`/`<dd>`).

**Forms**

| Component | Renders as | Notes |
|---|---|---|
| `Form` | `<form>` | |
| `Input` | `<input>` | No children. Two-way binding: `bind_value=Bind.model(...)` |
| `Textarea` | `<textarea>` | Text-only |
| `Select` / `Option` / `OptGroup` | matching tags | `Option` text-only |
| `Label` | `<label>` | Text-only. Use `for_=` (Python keyword clash) |
| `FieldSet` / `Legend` | `<fieldset>`/`<legend>` | `Legend` text-only |
| `Datalist` / `Output` / `Progress` / `Meter` | matching tags | `Output`/`Progress`/`Meter` text-only |

**Tables**: `Table`, `Caption` (text-only), `ColGroup`, `Col` (no
children), `TableHead`/`TableBody`/`TableFoot`, `TableRow`,
`TableHeaderCell`/`TableCell`.

**Interactive & misc**: `Button` (`<button>`, text-only, add
`on_click=...` for a built-in behavior), `NoScript`.

**Reactive (state-driven, not static markup)**: `Show` (requires
`predicate`), `Repeat` (requires `name`, renders `template=` per item
in a `State(...)` list).

**Fallback rule**: an unrecognized keyword prop on a component (`id`,
`class`, `href`, `src`, `style`, ...) is emitted as a `data-*` HTML
attribute rather than silently dropped.

## Reactive / interactive (`arklight/api.py`)

| Name | Signature (key args) | What it does |
|---|---|---|
| `State(name, initial, ...)` | `persist`, `media`, `query`, `history` | Declare page-scoped reactive state. **Must be passed as a child of `Page(...)`**, not a bare statement (see SKILL.md gotcha #4) |
| `Bind(name)` | | Reference a `State(...)`/`Computed(...)` value where a literal would go -- `Text(Bind("count"))` displays a scalar directly |
| `Bind.model(name)` | | Two-way binding target for `Input(bind_value=...)` specifically |
| `Computed(name, deps=(...), derive=...)` | | Declare a derived value, also a `Page(...)` child |
| `Derive` | class, closed set of ops | `sum`, `subtract`, `multiply`, `divide`, `max`, `min`, `count`, `join`, `compare`, `format`, `trim`, `uppercase`, more -- used as `Computed(..., derive=Derive.multiply(...))` |
| `Action` | class, closed set of ops | `Action.set`, `.increment`/`.decrement` (`delta=`), `.append`, `.remove`, `.reset`, `.toggle_bool`, `.geolocate`, more -- used as `on_click=...`. Only `set`/`append` accept a `Bind(...)` as their value arg |
| `Watch(name, then=...)` | | Side effect when a state value changes |
| `Repeat(name, template=...)` | pairs with `RepeatItem` | Per-item list rendering only -- not for a scalar value, use `Bind(...)` for that |
| `Show(predicate, *children)` | pairs with `Predicate` | Conditional rendering |
| `Predicate` | class, closed set of conditions | e.g. `Predicate.truthy(name)` -- used as `Show(...)`'s `predicate` |
| `PlatformAPI` | class, v0.065+ | Closed vocabulary of platform capabilities (`notify`, `clipboard_write`, `db`, ...) |
| `Provider` | class, EXPERIMENTAL | External-service *declaration* (`auth`/`read`/`write`/`subscribe` + `custom:`), not a general HTTP client -- see SKILL.md's experimental-APIs table |
| `component(...)` | decorator | Register a render function as a reusable named component (`props={...}`, `default_style={...}`). Calls take **keyword props only**. `state={local_name: initial}` gives it **instance-scoped** reactive state (independent per call site), referenced exactly like page-level `State(...)` -- `Bind`, `on_click=Action.*`, `bind_class=Bind.when(...)`, `bind_value=Bind.model(...)`, `Show(Predicate.*(...))`. Worked example: `References/cli-and-examples.md` |
| `Site(...)` | class | The application object. `name=`, `max_width=`, `bg=`, `font_family=`, `button_text=`, `lang=`, `stack_space=`, `cluster_space=`, `sidebar_space=`, `sidebar_width=`, `switcher_space=`, `switcher_threshold=`, `grid_min=`, `grid_space=`, `center_gutter=`, `reel_space=`, `app_shell=`, `strict_csp=`, `trusted_script_origins=`, `provider=`. Also owns `site.style(name, rules)` (one flat `.name {}` class) and `site.style_selector(selector, rules, allow_redefine=False)` (arbitrary selectors: combinators, grouped selectors, bare tags, attribute selectors, pseudo-classes/elements including `:hover` -- the only way to reach those) |

All of `Action.*`/`Derive.*`/`Predicate.*` are **closed, described
vocabularies** -- there is no arbitrary-expression form, no `eval`.
When nothing here covers what's needed, see SKILL.md's "When the
closed vocabulary isn't enough" section (the 7 registered experimental
APIs, principally `script-extension` for genuinely novel client JS and
`Provider` for talking to a real backend).

## Where this came from

Cross-checked by reading `arklight/ir/schema.py` and `arklight/api.py`
directly from a clone of `github.com/ARKlight-Ecosystem/ARKlight`
(main branch, commit `1f536e8`), and by actually building and running
`arklight build` against real site files to confirm error messages and
behavior rather than trusting the source comments alone. Re-derive if
the installed version differs -- check `arklight --version`.
