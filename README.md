# ARKlight Skill Collections

An [Agent Skill](https://www.anthropic.com/news/skills) that teaches
Claude (or any SKILL.md-compatible agent) how to actually build with
[ARKlight](https://github.com/ARKlight-Ecosystem/ARKlight), a
Python-first static-site compiler (`pip install arklight`).

ARKlight's authoring syntax looks like ordinary Python but is
**statically parsed, not executed** — several things that work in
normal Python fail silently in ARKlight. This skill exists because
those failure modes aren't visible from the error messages alone; an
agent without it will burn real tool-call cycles rediscovering them
from scratch.

Pinned to **ARKlight main, v0.70.0** (`github.com/ARKlight-Ecosystem/ARKlight`,
commit `1f536e8`). See "Version drift" in `SKILL.md` for what to do if
the installed version differs.

## What's inside

- **`SKILL.md`** — the skill itself: setup and the two license gates,
  the mental model, the four gotchas that actually bite (confirmed
  against `arklight/parser/discover.py` and real builds, not
  guessed), styling/responsive/reactivity authoring patterns, all 7
  registered experimental APIs (with exactly which is which —
  `script-extension` vs. the `Provider` SDK are easy to conflate), and
  a debugging checklist with the exact error text to match on.
- **`References/component-vocabulary.md`** — the full closed component/
  action/derivation/predicate vocabulary, cross-checked straight
  against `arklight/ir/schema.py` and `arklight/api.py` source, not
  copied from docs that may lag the code.
- **`References/cli-and-examples.md`** — every `arklight` subcommand
  and flag, plus three worked `site.py` examples (shared nav + toggle,
  a counter widget, a to-do list) that were actually built with
  `arklight build` to confirm they compile, not just hand-written.
- **`References/Field-notes-site.py`** — one real, unmodified `site.py`
  from a third-party ARKlight project (`ARKlight-Test-Collections/Field-Notes`),
  kept as a worked example of the "route decorators live in the entry
  file only" pattern plus `site.style(...)`/`site.style_selector(...)`
  CSS authoring at real-project scale.

## Provenance

Everything here was verified against source, not taken on faith from
write-ups about the project: cloned `github.com/ARKlight-Ecosystem/ARKlight`
(main, v0.70.0, commit `1f536e8`), installed the real PyPI package into
a venv, and actually ran `arklight build` — including deliberately
broken files — to confirm every error message and gotcha quoted here
matches what the compiler actually says, rather than what the docs
claim it says. The component vocabulary and experimental-API table are
generated from `arklight/ir/schema.py` / `arklight/api.py` /
`arklight/experimental.py` directly. The Sketchboard line-count claim
(script-extension blocks making up ~45% of its lines) was checked
against the actual file.

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

### Claude Code

```sh
git clone https://github.com/ARKlight-Ecosystem/Skills ~/.claude/skills/arklight-sites
```

Or per-project: `.claude/skills/arklight-sites`. Also works with the
cross-agent installer: `npx skills add https://github.com/ARKlight-Ecosystem/Skills`.

### Claude.ai (claude.ai / the Claude apps)

Upload `SKILL.md` (and the `References/` folder) as project files, or
use the in-app "Save skill" flow if your org has skill creation
enabled.

### Cursor / OpenAI Codex / Windsurf

Same pattern, different folder:

```sh
git clone https://github.com/ARKlight-Ecosystem/Skills ~/.cursor/skills/arklight-sites
git clone https://github.com/ARKlight-Ecosystem/Skills ~/.codex/skills/arklight-sites
git clone https://github.com/ARKlight-Ecosystem/Skills .windsurf/skills/arklight-sites
```

Restart the agent (or start a new session) so it picks up the skill.

## License

The Skill and the repo itself is MIT Licence.

Plz, Check the [license file](https://github.com/ARKlight-Ecosystem/Skills/blob/main/License) For more information.
