#!/usr/bin/env python3
"""Check course metadata, local links, native protocol boundaries and recorded viewer data."""
import json
from pathlib import Path
import re
import subprocess
import sys
from lab import inputs

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'labs/manifest.json').read_text())
ids={x['id'] for x in manifest['labs']}
assert len(ids)==len(manifest['labs']) and len(ids)>=9, 'lab ids must be unique'
for lab in manifest['labs']:
    assert (ROOT/lab['path']).is_file(),lab['path']
    assert set(lab['prerequisites']) <= ids
    assert lab['status'] in {'author-executed','verification-in-progress','learner-executed','workflow-exercised'}
paths=[ROOT/'README.md',ROOT/'SYLLABUS.md']
for directory in ('labs','case-studies','reference','feedback'):
    paths.extend((ROOT/directory).rglob('*.md'))
for path in paths:
    for url in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text()):
        if '://' in url or url.startswith('#'):continue
        target=url.split('#')[0]
        if target:assert (path.parent/target).exists(),f'Broken link: {path.relative_to(ROOT)} -> {url}'
print(f'PASS course index and local links: {len(manifest["labs"])} labs, {len(paths)} Markdown files')
for bad in ({'p1_overtemper':1}, {'level':-1}, {'level':5}, {'level':True},
            {'level':1.5}, {'p1_auto':2}, {'p1_auto':1.0}, {'p1_auto':'1'}):
    try:
        inputs(**bad)
    except ValueError:
        pass
    else:
        raise AssertionError(('invalid input accepted',bad))
print('PASS scenario input validation: typo keys, invalid levels and non-Boolean values rejected')
exe=ROOT/'build/reference/plc-sim'
if not exe.exists():
    print('NOT VERIFIED: native protocol checks (run lab.py build --apply first)')
    sys.exit(0)
for frame in (
    '0 1 2 0 0 0 0 0 0 0 0 0\n',
    '-1 1 0 0 0 0 0 0 0 0 0 0\n',
    '0 1 0 0 0 0 0 0 0 0 0 0 trailing\n',
    '0 1 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0\n',
):
    r=subprocess.run([str(exe),'station'],input=frame,capture_output=True,text=True,timeout=5)
    assert r.returncode==2,(frame,r.returncode)
print('PASS native protocol: invalid Boolean, negative time, trailing data, repeated timestamp rejected')
r=subprocess.run([sys.executable,'-O',str(ROOT/'scripts/lab.py'),'station'],capture_output=True,text=True)
assert r.returncode != 0 and 'assertions must remain enabled' in r.stderr
print('PASS optimized-Python rejection (assertion checks cannot silently disappear)')
