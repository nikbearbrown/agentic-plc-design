#!/usr/bin/env python3
"""Checksum-pinned source build. Default is a plan; --apply writes only .toolchain/."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / 'labs/toolchain.lock.json').read_text())
BASE = ROOT / '.toolchain'


def run(command, cwd, env, log):
    print('+', ' '.join(map(str, command)), flush=True)
    with log.open('a') as out:
        subprocess.run(command, cwd=cwd, env=env, stdout=out, stderr=subprocess.STDOUT, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--offline', action='store_true', help='only use already downloaded, checksum-checked archives')
    args = parser.parse_args()
    for package in LOCK['packages']:
        print(f"{package['name']} {package['version']} <- {package['url']}")
    if not args.apply:
        print(f'DRY RUN: would download, verify, extract and build under {BASE}; use --apply.')
        return
    for tool in ('make', 'cc', 'c++', 'flex', 'perl', 'curl'):
        if not shutil.which(tool):
            raise SystemExit(f'Missing prerequisite: {tool}. See labs/00-setup.md; no automatic system installs.')
    for name in ('downloads', 'src', 'prefix', 'logs'):
        (BASE / name).mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env['PATH'] = str(BASE / 'prefix/bin') + os.pathsep + env['PATH']
    # Host compiler/SDK are prerequisites; exact versions go in the execution ledger.
    for p in LOCK['packages']:
        archive = BASE / 'downloads' / p['file']
        if not archive.exists():
            if args.offline:
                raise SystemExit(f'Offline archive missing: {archive}')
            subprocess.run(['curl', '--fail', '--location', '--proto', '=https', p['url'], '-o', str(archive)], check=True)
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        if digest != p['sha256']:
            raise SystemExit(f'CHECKSUM MISMATCH: {archive}; refusing extraction/execution')
        stamp = BASE / 'logs' / (p['name'] + '.installed.json')
        if stamp.exists() and json.loads(stamp.read_text()).get('sha256') == digest:
            print('Already built:', p['name'])
            continue
        src = BASE / 'src' / (p['name'] + '-' + p['version'])
        if not src.exists():
            with tarfile.open(archive) as tf:
                tf.extractall(BASE / 'src', filter='data')
        log = BASE / 'logs' / (p['name'] + '.log')
        log.write_text('')
        if p['name'] == 'matiec':
            run(['autoreconf', '-i'], src, env, log)
        run(['./configure', '--prefix=' + str(BASE / 'prefix')], src, env, log)
        run(['make', '-j4'], src, env, log)
        run(['make', 'install'], src, env, log)
        stamp.write_text(json.dumps({'sha256': digest, 'source': str(src)}, indent=2) + '\n')
    print('READY: ' + str(BASE / 'prefix/bin/iec2c'))


if __name__ == '__main__':
    main()
