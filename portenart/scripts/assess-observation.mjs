/**
 * Offline classification of PUBLIC SYNTHETIC observation signals.
 * No network, filesystem writes, persistence, agent activation or skill edits.
 * This is a compatibility pilot, not the upstream Task Observer runtime.
 * Copyright 2026 PortenartCo. Pilot adapter; upstream is CC BY 4.0.
 */
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

const FIELDS = new Set(['case_id', 'signal', 'evidence', 'occurrences', 'owner', 'data_class']);
const SIGNALS = new Set(['explicit_correction', 'repeated_failure', 'confirmed_pattern', 'unverified_idea']);
const EVIDENCE = new Set(['verified', 'reported', 'missing']);
const OWNERS = Object.freeze({
  execution_health: 'diagnostic',
  operational_learning: 'learning',
  architecture: 'governance',
  unknown: 'unassigned',
});
const CLASSES = new Set(['synthetic', 'non_synthetic']);

function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value) &&
    (Object.getPrototypeOf(value) === Object.prototype || Object.getPrototypeOf(value) === null);
}

export function assessObservation(item) {
  if (!isPlainObject(item)) throw new Error('INVALID_INPUT');
  if (Object.keys(item).some((field) => !FIELDS.has(field))) throw new Error('UNKNOWN_FIELD');
  if (typeof item.case_id !== 'string' || !/^SYN-[0-9]{3}$/.test(item.case_id)) throw new Error('INVALID_CASE_ID');
  if (!SIGNALS.has(item.signal)) throw new Error('INVALID_SIGNAL');
  if (!EVIDENCE.has(item.evidence)) throw new Error('INVALID_EVIDENCE');
  if (!Number.isInteger(item.occurrences) || item.occurrences < 1 || item.occurrences > 100) throw new Error('INVALID_OCCURRENCES');
  if (!Object.hasOwn(OWNERS, item.owner)) throw new Error('INVALID_OWNER');
  if (!CLASSES.has(item.data_class)) throw new Error('INVALID_DATA_CLASS');

  // No user-supplied free text, identifiers or business content ever reach output.
  const result = { case_id: item.case_id, decision: 'NOT_ACTIONABLE', review_route: OWNERS[item.owner], effects: 'NONE' };
  if (item.data_class !== 'synthetic') {
    // Even the synthetic-looking case ID is withheld for non-synthetic inputs.
    return { case_id: null, decision: 'BLOCKED_NON_SYNTHETIC', review_route: 'privacy', effects: 'NONE' };
  }
  if (item.signal === 'unverified_idea') return result;
  if (item.evidence !== 'verified') return { ...result, decision: 'NEEDS_EVIDENCE' };
  if (item.signal === 'repeated_failure' && item.occurrences < 2) return { ...result, decision: 'NEEDS_MORE_CASES' };
  if (item.owner === 'unknown') return { ...result, decision: 'NEEDS_OWNER' };
  return { ...result, decision: 'PROPOSE_REVIEW' };
}

export function assessBatch(items) {
  if (!Array.isArray(items) || items.length < 1 || items.length > 50) throw new Error('INVALID_BATCH');
  return { mode: 'OFFLINE_SYNTHETIC_READ_ONLY', decisions: items.map(assessObservation) };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    const text = readFileSync(0, 'utf8'); // file descriptor 0 = stdin, no filesystem access
    const input = JSON.parse(text);
    process.stdout.write(`${JSON.stringify(assessBatch(input))}\n`);
  } catch {
    // Do not echo input or error details, including potentially sensitive content.
    process.stderr.write('INVALID_INPUT\n');
    process.exitCode = 2;
  }
}
