# Claude Code and Codex: a working cheat sheet

## Executive summary

The handful of agent-CLI concepts this course uses, with what each is for and where it lives. Product names, flags and menus change often; the concepts have been stable. When this sheet and `claude --help` or `codex --help` disagree, the help output wins and this sheet needs a fix.

## Concepts that carry across tools

| Concept | What it is | In Claude Code | In Codex |
|---|---|---|---|
| Instruction file | Standing rules read at session start | `CLAUDE.md` (can import `AGENTS.md` with `@AGENTS.md`) | `AGENTS.md` |
| Permission/approval level | What the agent may do without asking | Permission modes; start restrictive | Approval modes; start restrictive |
| Plan before acting | Agent proposes steps first | Plan mode | Ask it to plan and stop |
| Skill | Packaged instructions loaded on demand | `.claude/skills/<name>/SKILL.md` | Skills/prompts as supported by your version |
| Hook | Program the tool runs at set moments | `.claude/settings.json` hooks | Check your version's docs |
| Subagent | Separate agent with fresh context | `.claude/agents/<name>.md` | Run a second session as reviewer |
| Connector (MCP) | Standard link to outside tools/data | MCP servers | MCP servers |

## Habits that matter more than any flag

1. **Start in a clean git repo** so every agent change is a diff you can review and throw away.
2. **Write the rules down** in the instruction file, then check the agent obeyed them.
3. **Ask for a plan first** on anything that edits more than one file.
4. **Run the checks yourself** (`./check.sh`). Do not accept "tests pass" from the agent without seeing it.
5. **Never give it a live system.** Exports, copies and simulators only.
6. **Review the diff** before you accept. If you cannot explain a change, reject it.
7. **Keep sessions small.** One task, one session, then a commit.

## A minimal safe session

```bash
cd agentic-plc-design
git status            # clean?
claude                # or: codex
# first message: "Read AGENTS.md and STATUS.md. Do not change anything. Tell me the rules you will follow."
```
