#!/usr/bin/env python3
"""Reproducible sandbox-only smoke test of three UNMODIFIED upstream helpers.

The smoke test never reads business data, uses no network and copies no
observations to GitHub. All child processes get an explicit minimal env.
"""
from __future__ import annotations
import concurrent.futures
import hashlib
import json
import os
import shutil
from pathlib import Path
import re
import subprocess
import tempfile
from datetime import date

BASE = Path(__file__).resolve().parents[2]
SCRIPTS = BASE / 'scripts'
SANDBOX = Path(tempfile.mkdtemp(prefix='task-observer-native-', dir='/tmp'))
EXPECTED = {
    'new-observation.sh': ('9ce7d716c9faef8f7b1c8ad65065e01006dd7224', 8882),
    'session-start-scan.sh': ('090aa2dfb8fd870ca39958ea0f383c94466d02b2', 10272),
    'skill-load.sh': ('5339b9b5dc3f7d37797f8e739336b395382b47d6', 5601),
}


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def check(message: str, condition: bool, details: str = '') -> None:
    result = {'test': message, 'result': 'PASS' if condition else 'FAIL', 'details': details}
    RECORD['checks'].append(result)
    if not condition:
        raise AssertionError(f'{message} failed: {details}')


def command(script: str, *args: str, workspace: Path, expected_exit: int = 0):
    run = subprocess.run(
        ['/usr/bin/bash', str(SCRIPTS / script), *map(str, args)],
        cwd=str(BASE), env=ENV, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20,
        check=False,
    )
    check(f'{script}: exit={expected_exit} (call {len(RECORD["commands"])+1})',
          run.returncode == expected_exit,
          f'actual={run.returncode}; stderr={run.stderr[:160]}')
    RECORD['commands'].append({
        'script': script, 'exit': run.returncode,
        'stdout': run.stdout.strip()[:1000], 'stderr': run.stderr.strip()[:500]
    })
    return run


def initialize(root: Path):
    d = root / 'skill-observations'
    (d / 'observation-log' / 'archive').mkdir(parents=True)
    (d / 'last-review-date.txt').write_text('never\n')
    (d / 'cross-cutting-principles.md').write_text(
        '# Cross-Cutting Principles\n\n'
        'Principles that apply to all skills. Read as a mandatory checklist during\n'
        'any skill creation or regeneration.\n\n---\n\n## Active Principles\n'
    )
    return d


def create_observation(root: Path, slug: str, skill: str, status: str = 'open'):
    stdout = command('new-observation.sh', slug, root, workspace=root).stdout.strip()
    p = Path(stdout)
    check('writer stays in synthetic workspace', p.parent == root / 'skill-observations/observation-log')
    match = re.match(r'^(\d{4})-[a-z0-9-]+\.md$', p.name)
    check('writer produced numbered observation path', match is not None, p.name)
    assert match
    number = int(match.group(1))
    # Entire record is invented and contains no workplace details.
    fm = '\n'.join([
        '---',
        f'id: {number}',
        f'title: "Synthetic {slug}"',
        f'status: {status}',
        'type: open-source',
        f'skill: [{skill}]',
        'proposes_skill: []',
        'target_file: []',
        'siblings_checked: "none: synthetic isolated example"',
        'area: "synthetic pilot"',
        f'date: {date.today().isoformat()}',
        'session_context: "No real user interactions"',
        'parked_until:',
        'resolved:',
        'resolution:',
        'reference:',
        'commands_verified: none',
        '---',
        '',
        '**Issue:** Synthetic correction in a fake workflow.',
        '**Suggested improvement:** Sample proposal, never apply.',
        '**Principle:** Retain explicit reviewer gate.',
        '',
        'BODY_CANARY_MUST_NOT_APPEAR_IN_SCAN',
        ''
    ])
    p.write_text(fm)
    return p


RECORD = {'scope': 'three genuine upstream shell helpers, no skill invocation',
          'upstream_commit': '07a7d926ad986548b8d5dac1db9fc9687c0060ef',
          'checks': [], 'commands': [], 'sandbox_paths': [],
          'runtime': {'network_requests': 0, 'agent_skills_installed': 0, 'external_writes': 0}}

try:
    for filename, (expected_sha, expected_size) in EXPECTED.items():
        source = (SCRIPTS / filename).read_bytes()
        check('authentic upstream blob ' + filename,
              git_blob(source) == expected_sha and len(source) == expected_size,
              f'blob={git_blob(source)} size={len(source)}')

    SANDBOX.mkdir(parents=True, exist_ok=True)
    temp_dir = SANDBOX / 'temp'
    temp_dir.mkdir(exist_ok=True)
    home_dir = SANDBOX / 'empty-home'
    home_dir.mkdir(exist_ok=True)
    ENV = {'PATH': '/usr/bin:/bin', 'HOME': str(home_dir), 'LANG': 'C',
           'TZ': 'UTC', 'TMPDIR': str(temp_dir)}
    check('minimal child environment has no token or connector variables',
          not any('TOKEN' in x or 'KEY' in x or 'GITHUB' in x or 'AZURE' in x for x in ENV),
          ','.join(sorted(ENV)))

    root = Path(tempfile.mkdtemp(prefix='observer space ', dir=SANDBOX))
    RECORD['sandbox_paths'].append(str(root))
    initialize(root)
    initial = command('session-start-scan.sh', root, workspace=root)
    check('genuine startup scan reports empty log', 'files: 0  parsed: 0' in initial.stdout)

    first = create_observation(root, 'fictional-user-correction', 'task-observer')
    assert first.name.startswith('0001-')
    scan = command('session-start-scan.sh', root, workspace=root)
    check('genuine scan reads persisted header', 'files: 1  parsed: 1' in scan.stdout)
    check('genuine scan withholds observation body', 'BODY_CANARY_MUST_NOT_APPEAR_IN_SCAN' not in scan.stdout)
    check('genuine scan reports no suspect YAML', 'suspect (awk, a floor): 0' in scan.stdout)

    found = command('skill-load.sh', root, 'plugin:task-observer', workspace=root)
    check('genuine per-skill lookup finds open fake observation',
          'plugin:task-observer: 1 open observations' in found.stdout and first.name in found.stdout)
    wrong = command('skill-load.sh', root, 'unrelated-skill', workspace=root)
    check('genuine lookup isolates unrelated skills', 'unrelated-skill: 0 open observations' in wrong.stdout)

    second = create_observation(root, 'fictional-recurrent-issue', 'synthetic-other-skill')
    check('second observation increments id', second.name.startswith('0002-'))
    # Synthetic resolved observation, using a safely old date to trigger archival-on-write.
    text = first.read_text().replace('status: open', 'status: actioned').replace('resolved:\n', 'resolved: 2020-01-01\n')
    first.write_text(text)
    third = create_observation(root, 'third-fake-signal', 'task-observer')
    check('archival-on-write moved old resolved observation',
          not first.exists() and (root / 'skill-observations/observation-log/archive' / first.name).is_file())
    check('id floor persisted beyond archived observation',
          third.name.startswith('0003-') and
          int((root / 'skill-observations/observation-log/archive/.id-floor').read_text()) >= 3)

    scan = command('session-start-scan.sh', root, workspace=root)
    check('scan reports two open records after archive', 'files: 2  parsed: 2' in scan.stdout)
    own = command('skill-load.sh', root, 'task-observer', workspace=root)
    check('lookups only open matching records',
          'task-observer: 1 open observations' in own.stdout and third.name in own.stdout)
    check('checkpoint entries persisted across separate subprocesses',
          'session-start scan:' in (root / 'skill-observations/checkpoints.log').read_text() and
          'loaded task-observer' in (root / 'skill-observations/checkpoints.log').read_text())

    d = root / 'skill-observations/observation-log'
    pre_files = sorted(x.name for x in d.glob('*.md'))
    err = command('new-observation.sh', 'bad slug', root, workspace=root, expected_exit=1)
    check('bad slug rejected with no new numbered file', sorted(x.name for x in d.glob('*.md')) == pre_files)

    # Separate concurrent issuance scenario, again synthetic only.
    concurrent_root = Path(tempfile.mkdtemp(prefix='observer concurrent space ', dir=SANDBOX))
    RECORD['sandbox_paths'].append(str(concurrent_root))
    initialize(concurrent_root)
    def writer(i):
        return subprocess.run(['/usr/bin/bash', str(SCRIPTS / 'new-observation.sh'),
                               f'parallel-fiction-{i}', str(concurrent_root)],
                              cwd=str(BASE), env=ENV, capture_output=True, text=True,
                              timeout=20)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(writer, range(4)))
    codes = [x.returncode for x in results]
    issued = [Path(x.stdout.strip()).name for x in results if x.returncode == 0]
    check('four concurrent synthetic writers exit cleanly', codes == [0, 0, 0, 0], str(codes))
    check('concurrent IDs are unique', len(set(x.split('-')[0] for x in issued)) == 4, str(issued))
    check('concurrent ID floor never regresses',
          int((concurrent_root / 'skill-observations/observation-log/archive/.id-floor').read_text()) >= max(int(x.split('-')[0]) for x in issued))

    # Snapshot only synthetic metadata, avoid public release of raw log bodies.
    RECORD['checkpoint_lines'] = len((root / 'skill-observations/checkpoints.log').read_text().splitlines())
    RECORD['observation_file_names'] = sorted(p.name for p in d.glob('*.md'))
    RECORD['archived_file_names'] = sorted(p.name for p in (d / 'archive').glob('*.md'))
    RECORD['status'] = 'PASS'
except Exception as exc:
    RECORD['status'] = 'FAIL'
    RECORD['error'] = f'{type(exc).__name__}: {str(exc)[:350]}'
finally:
    try:
        shutil.rmtree(SANDBOX)
        cleaned = not SANDBOX.exists()
    except OSError:
        cleaned = False
    if not cleaned:
        RECORD['status'] = 'FAIL'
        RECORD['error'] = 'Temporary workspace cleanup failed'
    print(json.dumps({'status': RECORD['status'], 'checks': len(RECORD['checks']),
                      'passed': sum(x['result']=='PASS' for x in RECORD['checks']),
                      'failed': sum(x['result']=='FAIL' for x in RECORD['checks']),
                      'error': RECORD.get('error'),
                      'sandbox_removed': cleaned}, ensure_ascii=False))
if RECORD['status'] != 'PASS':
    raise SystemExit(1)
