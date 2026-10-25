# CLAUDE.md

@AGENTS.md

Claude Code specifics: the hook in `.claude/settings.json` runs `scripts/guard.py` before every Edit or Write and blocks edits to a reference table the human has marked `verified = true`. The skill `variant-check` and the subagent `panel-reviewer` live in `.claude/`; Module 10 teaches how they were built.
