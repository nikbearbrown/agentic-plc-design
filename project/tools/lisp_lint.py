"""Static safety check for AutoLISP files. Cheap, strict, and not a substitute for a dry run on a copy.

Fails on: unbalanced parentheses/quotes, calls that delete, purge, write files or shell out,
and any entmod/entupdate not guarded by *APD-APPLY*.
"""
from __future__ import annotations

import re
import sys

FORBIDDEN = [
    (r"\(\s*command\b", "command: scripted AutoCAD commands can erase, purge or explode without asking"),
    (r"\(\s*vl-cmdf\b", "vl-cmdf: same as command"),
    (r"\(\s*entdel\b", "entdel: deletes objects"),
    (r"\(\s*vl-file-delete\b", "vl-file-delete: deletes files"),
    (r"\(\s*vl-file-rename\b", "vl-file-rename: moves files"),
    (r"\(\s*startapp\b", "startapp: launches programs"),
    (r"\(\s*vl-registry-write\b", "registry write"),
    (r"\(\s*open\b[^)]*\"[wa]\"", "open for writing"),
    (r"\(\s*vlax-invoke(-method)?\b", "ActiveX invoke: not allowed in this course's scripts"),
    (r"(?i)_?\.?-?purge", "purge"),
]


def strip(src: str) -> str:
    """Remove comments and string contents so paren counting is honest."""
    out, i, in_str = [], 0, False
    while i < len(src):
        c = src[i]
        if in_str:
            if c == "\\" and i + 1 < len(src):
                i += 2
                continue
            if c == '"':
                in_str = False
                out.append('"')
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append('"')
        elif c == ";":
            while i < len(src) and src[i] != "\n":
                i += 1
            continue
        else:
            out.append(c)
        i += 1
    if in_str:
        raise ValueError("unterminated string")
    return "".join(out)


def lint(src: str) -> list[str]:
    problems = []
    try:
        clean = strip(src)
    except ValueError as e:
        return [str(e)]
    depth = 0
    for ch in clean:
        depth += (ch == "(") - (ch == ")")
        if depth < 0:
            problems.append("extra closing parenthesis")
            break
    if depth > 0:
        problems.append(f"{depth} unclosed parenthesis")
    for pat, why in FORBIDDEN:
        if re.search(pat, clean):
            problems.append(f"forbidden: {why}")
    writes = len(re.findall(r"\(\s*(entmod|entupdate)\b", clean))
    guarded = len(re.findall(r"\(\s*if\s+\*APD-APPLY\*\s*\(\s*(entmod|entupdate)\b", clean))
    if writes != guarded:
        problems.append(f"{writes - guarded} entmod/entupdate call(s) not guarded by (if *APD-APPLY* ...)")
    return problems


def main(argv=None):
    paths = (argv if argv is not None else sys.argv[1:])
    bad = 0
    for p in paths:
        probs = lint(open(p, encoding="utf-8").read())
        print(f"{p}: {'OK' if not probs else 'FAIL'}")
        for pr in probs:
            print("   -", pr)
        bad += bool(probs)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
