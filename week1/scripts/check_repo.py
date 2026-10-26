#!/usr/bin/env python3
"""Conservative check of staged file *names* and staged contents before GitHub push.
This is only a basic heuristic; manually inspect everything too.
"""
import re
import subprocess
import sys
from pathlib import Path

BAD_SUFFIXES = {'.pem', '.key', '.p12', '.pfx', '.jks', '.crt', '.cer', '.csr', '.vmdk', '.vmem', '.vmx', '.vmsn', '.vmsd', '.vmss'}
BAD_BASE = {'docker-compose.yml', '.env', 'id_rsa', 'id_ed25519', 'ossec.conf', 'internal_users.yml'}
BLOCK_CONTENT = [
    re.compile(rb'-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----'),
    re.compile(rb'INDEXER_PASSWORD\s*='),
    re.compile(rb'SecretPassword'),
    re.compile(rb'AKIA[0-9A-Z]{16}'),
]

def git(*args):
    p = subprocess.run(['git', *args], capture_output=True, check=True)
    return p.stdout

def main():
    try:
        entries = [x for x in git('diff', '--cached', '--name-only', '-z').decode().split('\0') if x]
    except Exception:
        print('ERROR: Run from a Git repository with staged changes.'); return 2
    if not entries:
        print('No staged files. Run git add . and re-check before commit.'); return 2
    problems = []
    for filename in entries:
        p = Path(filename)
        lower = filename.lower()
        if p.suffix.lower() in BAD_SUFFIXES or p.name.lower() in BAD_BASE or '/wazuh-docker/' in f'/{lower}' or 'ssl_certs' in lower:
            problems.append(f'BLOCKED FILENAME: {filename}')
        # Read the staged content, not just working tree (files might differ).
        try:
            blob = git('show', f':{filename}')
        except Exception:
            problems.append(f'COULD NOT READ STAGED FILE: {filename}'); continue
        if p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.svg', '.gif', '.pdf'}:
            continue  # Screen captures/images need *manual* visual review.
        if filename == 'scripts/check_repo.py':
            continue  # Contains example detection patterns, not real credentials.
        for pat in BLOCK_CONTENT:
            if pat.search(blob): problems.append(f'POTENTIAL SECRET in {filename} ({pat.pattern.decode(errors="replace")})')
    print(f'Inspected {len(entries)} staged file(s).')
    if problems:
        print('\n'.join(problems)); print('STOP: remove/redact before committing.'); return 1
    print('Basic staged-file scan passed. MANUALLY inspect images, docs, and configuration before pushing.')
    return 0

if __name__ == '__main__': sys.exit(main())
