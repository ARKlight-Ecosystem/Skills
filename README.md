# ARKlight Skill Collections

[Agent Skills](https://www.anthropic.com/news/skills) that teach
Claude (or any SKILL.md-compatible agent) how to actually build with
[ARKlight](https://github.com/ARKlight-Ecosystem/ARKlight), a
Python-first static-site compiler (`pip install arklight`).

ARKlight's authoring syntax looks like ordinary Python but is
**statically parsed, not executed** — several things that work in
normal Python fail silently in ARKlight. This skill exists because
those failure modes aren't visible from the error messages alone; an
agent without it will burn real tool-call cycles rediscovering them
from scratch.

Pinned to **ARKlight main, v0.70.1** (`github.com/ARKlight-Ecosystem/ARKlight`).
The official ARKlight repo's own `v0.070.1` release notes point
AI-assisted developers at this repo directly — see "Version drift" in
`skills/arklight-sites/SKILL.md` for what to do if the installed
version differs.

## Two skills, not one

Everything doesn't fit cleanly in a single `SKILL.md`, so this repo
ships two, each with its own trigger condition:

- **`skills/arklight-sites/`** — the authoring/debugging skill: setup
  and the two license gates, the mental model, the five gotchas that
  actually bite (confirmed against `arklight/parser/discover.py` and
  real builds, not guessed), styling/responsive/reactivity authoring
  patterns, all 7 registered experimental APIs, and a debugging
  checklist with the exact error text to match on. Use this when
  writing, fixing, or debugging an ARKlight site.
- **`skills/arklight-examples/`** — an index of real, first-party
  ARKlight projects and official project links (the compiler repo,
  this skill repo, the official docs site source and its live
  deployment), each with a version-drift trust rating so an older
  example's now-fixed "limitation" doesn't get copied as current
  advice. Use this when looking for a real-world precedent, not when
  writing a site from scratch.

Both read from this repo's own `References/` subfolders; neither
duplicates the other's content.

## Provenance

Everything here was verified against source, not taken on faith from
write-ups about the project: cloned `github.com/ARKlight-Ecosystem/ARKlight`
(main, v0.70.1), installed the real PyPI package into a venv, and
actually ran `arklight build` — including deliberately broken files —
to confirm every error message and gotcha quoted here matches what the
compiler actually says, rather than what the docs claim it says. The
component vocabulary and experimental-API table are generated from
`arklight/ir/schema.py` / `arklight/api.py` / `arklight/experimental.py`
directly. The Sketchboard line-count claim (script-extension blocks
making up ~45% of its lines) was checked against the actual file. The
example index in `arklight-examples` was built by cloning all 7
`ARKlight-Test-Collections` repos directly (not just the 2–3 that
looked Python-flagged at a glance) and checking each one's own version
signal rather than assuming they're all current.

**Eval'd once** — three test prompts (a portfolio site with a
toggle-revealed section, a stateful counter widget, and fixing a
broken `site.py`) run both with and without this skill. Both
configurations reached a correct, cleanly-building result on every
test, but the skill-equipped run used meaningfully less time and
fewer tokens per task by skipping the "read the installed package's
source to reverse-engineer the API" step baseline runs otherwise took.
Not a large-scale benchmark — meant to be exercised and refined
further as real usage turns up more edge cases.

## Install

### As a plugin (Claude Code / Cowork, both skills at once)

```sh
claude plugin marketplace add ARKlight-Ecosystem/Skills
claude plugin install arklight-skills@Skills
```

### Manual, Claude Code / Cursor / Codex / Windsurf (per-skill)

```sh
git clone https://github.com/ARKlight-Ecosystem/Skills /tmp/arklight-skills
cp -r /tmp/arklight-skills/skills/arklight-sites ~/.claude/skills/arklight-sites
cp -r /tmp/arklight-skills/skills/arklight-examples ~/.claude/skills/arklight-examples
```

Swap `~/.claude/skills` for `~/.cursor/skills`, `~/.codex/skills`, or
`.windsurf/skills` as needed, or `.claude/skills/` for a per-project
install. Also works with the cross-agent installer:
`npx skills add https://github.com/ARKlight-Ecosystem/Skills`.

### Claude.ai (claude.ai / the Claude apps)

Upload both `skills/arklight-sites/SKILL.md` and
`skills/arklight-examples/SKILL.md` (with their `References/` folders)
as project files, or use the in-app "Save skill" flow if your org has
skill creation enabled.

## License

The Skill and the repo itself is MIT Licence.

Plz, Check the [license file](https://github.com/ARKlight-Ecosystem/Skills/blob/main/License) For more information.
