import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { mkdtempSync, readdirSync, rmSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { assessObservation, assessBatch } from '../scripts/assess-observation.mjs';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const cli = join(root, 'scripts', 'assess-observation.mjs');
const input = JSON.parse(readFileSync(join(root, 'fixtures', 'synthetic-events.json'), 'utf8'));

const sample = (changes = {}) => ({
  case_id: 'SYN-101', signal: 'explicit_correction', evidence: 'verified',
  occurrences: 1, owner: 'operational_learning', data_class: 'synthetic', ...changes,
});

test('verified user correction yields proposal, never application', () => {
  assert.deepEqual(assessObservation(sample()), {
    case_id: 'SYN-101', decision: 'PROPOSE_REVIEW', review_route: 'learning', effects: 'NONE',
  });
});

test('repeated failure needs at least two independent occurrences', () => {
  assert.equal(assessObservation(sample({ signal: 'repeated_failure', occurrences: 1 })).decision, 'NEEDS_MORE_CASES');
  assert.equal(assessObservation(sample({ signal: 'repeated_failure', occurrences: 2, owner: 'execution_health' })).review_route, 'diagnostic');
});

test('unverified ideas never become procedures', () => {
  assert.equal(assessObservation(sample({ signal: 'unverified_idea' })).decision, 'NOT_ACTIONABLE');
});

test('reported or missing evidence cannot pass', () => {
  for (const evidence of ['reported', 'missing']) {
    assert.equal(assessObservation(sample({ evidence })).decision, 'NEEDS_EVIDENCE');
  }
});

test('unknown ownership must be resolved', () => {
  assert.equal(assessObservation(sample({ owner: 'unknown' })).decision, 'NEEDS_OWNER');
});

test('non synthetic event blocks and withholds identifier', () => {
  const result = assessObservation(sample({ data_class: 'non_synthetic' }));
  assert.deepEqual(result, { case_id: null, decision: 'BLOCKED_NON_SYNTHETIC', review_route: 'privacy', effects: 'NONE' });
});

test('unknown text and extra fields rejected instead of being echoed', () => {
  assert.throws(() => assessObservation(sample({ transcript: 'private example' })), /UNKNOWN_FIELD/);
  assert.throws(() => assessObservation(sample({ case_id: 'REAL_IDENTIFIER' })), /INVALID_CASE_ID/);
});

test('invalid schema and oversized batches rejected', () => {
  assert.throws(() => assessBatch([sample(), ...Array(50).fill(sample())]), /INVALID_BATCH/);
  assert.throws(() => assessBatch([]), /INVALID_BATCH/);
  assert.throws(() => assessObservation(sample({ occurrences: 0 })), /INVALID_OCCURRENCES/);
});

test('CLI emits only schema-bound decisions without creating any file', () => {
  const dir = mkdtempSync(join(tmpdir(), 'observer-pilot-'));
  try {
    const before = readdirSync(dir);
    const result = spawnSync(process.execPath, [cli], { cwd: dir, input: JSON.stringify(input), encoding: 'utf8' });
    assert.equal(result.status, 0, result.stderr);
    assert.deepEqual(readdirSync(dir), before);
    assert.equal(result.stderr, '');
    const output = JSON.parse(result.stdout);
    assert.equal(output.mode, 'OFFLINE_SYNTHETIC_READ_ONLY');
    assert.deepEqual(output.decisions.map((x) => x.decision), ['PROPOSE_REVIEW', 'PROPOSE_REVIEW', 'NOT_ACTIONABLE']);
    assert.ok(output.decisions.every((x) => x.effects === 'NONE'));
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('CLI rejects free-text input without copying content to stderr', () => {
  const result = spawnSync(process.execPath, [cli], { input: JSON.stringify([sample({ notes: 'private example' })]), encoding: 'utf8' });
  assert.equal(result.status, 2);
  assert.equal(result.stdout, '');
  assert.equal(result.stderr, 'INVALID_INPUT\n');
});
