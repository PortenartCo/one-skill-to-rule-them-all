#!/usr/bin/env python3
"""Synthetic preflight for a future two-agent-session Task Observer trial.

Runs the GENUINE upstream shell helpers in two independent subprocesses,
with a shared TEMPORARY fixture workspace and a minimal child environment.
This does NOT invoke a model, install a Skill, or certify two agent sessions.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / 'scripts'
EXPECTED = {
    'new-observation.sh': '9ce7d716c9faef8f7b1c8ad65065e01006dd7224',
    'session-start-scan.sh': '090aa2dfb8fd870ca39958ea0f383c94466d02b2',
    'skill-load.sh': '5339b9b5dc3f7d37797f8e739336b395382b47d6',
}
MARKER = 'BODY_FAKE_AGENT_HANDED_OFF_NOT_IN_SCAN'


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def run_helper(name: str, *arguments: str) -> str:
    result = subprocess.run(
        ['/usr/bin/bash', str(SCRIPTS / name), *map(str, arguments)],
        cwd=REPO, env={k: os.environ[k] for k in ('PATH', 'HOME', 'LANG', 'TZ', 'TMPDIR')},
        capture_output=True, text=True, timeout=25, check=False,
    )
    if result.returncode:
        raise RuntimeError(f'{name} exit={result.returncode}, stderr={result.stderr[:200]}')
    return result.stdout


def snapshot(root: Path) -> list[str]:
    d = root / 'skill-observations' / 'observation-log'
    return sorted(p.name for p in d.glob('[0-9]*.md'))


def phase_a(root: Path) -> dict:
    d = root / 'skill-observations'
    (d / 'observation-log' / 'archive').mkdir(parents=True)
    (d / 'last-review-date.txt').write_text('never\n')
    (d / 'cross-cutting-principles.md').write_text(
        '# Cross-Cutting Principles\n\n## Active Principles\n', encoding='utf-8'
    )
    initial = run_helper('session-start-scan.sh', root)
    assert 'files: 0  parsed: 0' in initial, 'initial scan not empty'
    created = Path(run_helper('new-observation.sh', 'imaginary-approval-versus-send', root).strip())
    assert created.parent == d / 'observation-log'
    match = re.fullmatch(r'(\d{4})-imaginary-approval-versus-send\.md', created.name)
    assert match, 'invalid generated observation ID'
    obs_id = int(match.group(1))
    assert obs_id == 1, 'expected first independent fixture record'
    created.write_text('\n'.join([
        '---',
        f'id: {obs_id}',
        'title: "Approval is not message delivery (synthetic)"',
        'status: open',
        'type: open-source',
        'skill: [fictional-workflow]',
        'proposes_skill: []',
        'target_file: []',
        'siblings_checked: "none: wholly fictional workflow"',
        'area: "synthetic paper-airplane checklist"',
        f'date: {date.today().isoformat()}',
        'session_context: "Imaginary Blue Meteor paper-airplane club only"',
        'parked_until:', 'resolved:', 'resolution:', 'reference:',
        'commands_verified: none', '---', '',
        '**Issue:** A fictional draft marked a message sent without sending it.',
        '**Suggested improvement:** Label approval, drafting, and actual sending separately.',
        '**Principle:** A proposed action is not evidence that it was executed.',
        '', MARKER, '',
    ]), encoding='utf-8')
    return {
        'phase': 'A', 'pid': os.getpid(), 'observation': created.name,
        'observation_sha256': hashlib.sha256(created.read_bytes()).hexdigest(),
        'files': snapshot(root), 'status': 'PASS',
    }


def phase_b(root: Path) -> dict:
    d = root / 'skill-observations' / 'observation-log'
    before = snapshot(root)
    assert len(before) == 1, 'no single persisted observation found'
    scan = run_helper('session-start-scan.sh', root)
    assert 'files: 1  parsed: 1' in scan, 'did not reload a valid persisted header'
    assert MARKER not in scan, 'frontmatter scanner leaked observation body'
    loaded = run_helper('skill-load.sh', root, 'fictional-workflow')
    assert 'fictional-workflow: 1 open observations' in loaded
    assert before[0] in loaded
    obs = d / before[0]
    text = obs.read_text(encoding='utf-8')
    assert 'status: open' in text
    assert 'draft marked a message sent' in text
    assert snapshot(root) == before, 'reload created an unexpected duplicate'
    checkpoints = (root / 'skill-observations' / 'checkpoints.log').read_text()
    assert checkpoints.count('session-start scan:') == 2
    assert checkpoints.count('loaded fictional-workflow') == 1
    return {
        'phase': 'B', 'pid': os.getpid(), 'observation': obs.name,
        'observation_sha256': hashlib.sha256(obs.read_bytes()).hexdigest(),
        'files': snapshot(root), 'status': 'PASS',
    }


def main() -> None:
    if len(sys.argv) == 4 and sys.argv[1] == '--phase':
        phase, root = sys.argv[2], Path(sys.argv[3])
        if phase not in {'A', 'B'}:
            raise SystemExit('invalid phase')
        if not root.is_absolute() or not root.resolve().is_relative_to(Path('/tmp').resolve()):
            raise SystemExit('refusing non-temporary workspace')
        result = phase_a(root) if phase == 'A' else phase_b(root)
        print(json.dumps(result, sort_keys=True))
        return

    if len(sys.argv) != 1:
        raise SystemExit('usage: python3 portenart/tests/two-process-agent-preflight.py')
    for filename, expected in EXPECTED.items():
        if git_blob(SCRIPTS / filename) != expected:
            raise SystemExit(f'FAIL: upstream helper blob mismatch: {filename}')
    parent = Path(tempfile.mkdtemp(prefix='task-observer-isolated-', dir='/tmp'))
    root = parent / 'fictional workspace with spaces'
    root.mkdir()
    (parent / 'empty-home').mkdir()
    env = {
        'PATH': '/usr/bin:/bin', 'HOME': str(parent / 'empty-home'),
        'LANG': 'C', 'TZ': 'UTC', 'TMPDIR': str(parent),
    }
    try:
        stages = []
        for phase in ('A', 'B'):
            process = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), '--phase', phase, str(root)],
                cwd=REPO, env=env, text=True, capture_output=True,
                timeout=50, check=False,
            )
            if process.returncode:
                raise RuntimeError(f'phase {phase} exit {process.returncode}: {process.stderr[:260]}')
            stages.append(json.loads(process.stdout))
        a, b = stages
        assert a['phase'] == 'A' and b['phase'] == 'B'
        assert a['pid'] != b['pid'], 'fresh process boundary could not be certified'
        assert a['observation'] == b['observation']
        assert a['observation_sha256'] == b['observation_sha256']
        assert a['files'] == b['files']
        assert len(a['files']) == 1
        print(json.dumps({
            'status': 'PASS',
            'evidence': 'TWO_SEPARATE_PROCESSES_ONLY',
            'upstream_script_blobs': 'MATCH',
            'shared_synthetic_observation': a['observation'],
            'observation_unchanged': True,
            'duplicate_count': 0,
            'child_environment_allowlisted': sorted(env),
            'agent_session_invocation': 'NOT_TESTED',
            'skill_activation': 'NOT_TESTED',
            'durable_storage': 'NOT_TESTED',
        }, sort_keys=True))
    finally:
        shutil.rmtree(parent)


if __name__ == '__main__':
    main()
