#!/usr/bin/env python3
"""Claude Code PreToolUse hook: refuse to edit a reference table the human has verified.

Reads the hook JSON on stdin. Exit 2 blocks the tool call and shows stderr to the agent.
A verified table is the +1's signed work (AI1 P2/P4); the agent appends evidence elsewhere,
it never overwrites.
"""
import json
import re
import sys
from pathlib import Path

PROTECTED = ("nec-extracts.toml", "catalog.toml")

try:
    event = json.load(sys.stdin)
except Exception:
    sys.exit(0)

path = (event.get("tool_input") or {}).get("file_path", "")
if Path(path).name in PROTECTED and Path(path).exists():
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    if re.search(r"(?m)^verified\s*=\s*true\b", text):
        sys.stderr.write(
            f"BLOCKED: {Path(path).name} is marked verified = true. A human signed it. "
            "Propose the change in a note and stop; do not edit a verified table.\n")
        sys.exit(2)
sys.exit(0)
