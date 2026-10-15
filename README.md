# arklight-sites

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

- **`SKILL.md`** — the skill itself: the four gotchas that actually
  bite, the full closed component vocabulary, all 7 registered
  experimental APIs (with exactly which is which — `script-extension`
  vs. the `Provider` SDK are easy to conflate), and a debugging
  checklist.
- **`references/component-vocabulary.md`** — every built-in
  component/action/derive, extracted straight from `arklight/ir/schema.py`
  and `arklight/api.py` source, not copied from docs that may lag the
  code.
- **`references/field-notes-site.py`** — one real, unmodified `site.py`
  from a third-party ARKlight project (`ARKlight-Test-Collections/Field-Notes`),
  kept as a worked example of the "route decorators live in the entry
  file only" pattern.

## Provenance

Everything here was verified against source this session, not taken
on faith from write-ups about the project: cloned
`github.com/ARKlight-Ecosystem/ARKlight` (main, v0.70.0) and the alpha
branch, built real sites with both, and recorded the actual failures
hit along the way. The component vocabulary and experimental-API table
are generated from `arklight/ir/schema.py` / `arklight/api.py` /
`arklight/experimental.py` directly. The Sketchboard line-count claim
(1,311 of 2,945 lines in `script-extension` blocks) was checked
against the actual file and confirmed exact.

**Not yet tested as a skill** — no eval loop has been run comparing
an agent with this skill against one without it. First version, meant
to be exercised and refined.

## Install

### Claude Code

```sh
git clone https://github.com/ARKlight-Exosystem/arklight-sites ~/.claude/skills/arklight-sites
```

Or per-project: `.claude/skills/arklight-sites`. Also works with the
cross-agent installer: `npx skills add https://github.com/<your-username>/arklight-sites`.

### Claude.ai (claude.ai / the Claude apps)

Upload `SKILL.md` (and the `references/` folder) as project files, or
use the in-app "Save skill" flow if your org has skill creation
enabled.

### Cursor / OpenAI Codex / Windsurf

Same pattern, different folder:

```sh
git clone https://github.com/ARKlight-Ecosystem/arklight-sites ~/.cursor/skills/arklight-sites
git clone https://github.com/ARKlight-Ecosystem/arklight-sites ~/.codex/skills/arklight-sites
git clone https://github.com/ARKlight-Ecosystem/arklight-sites .windsurf/skills/arklight-sites
```

Restart the agent (or start a new session) so it picks up the skill.

## License

Plz, Check the [license file](https://github.com/ARKlight-Ecosystem/Skills/blob/main/License) For more information.
