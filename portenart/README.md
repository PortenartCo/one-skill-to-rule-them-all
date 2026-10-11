# Task Observer - Portenart compatibility pilot

**State: PREPARATION ONLY. Not installed or activated.**

This directory is an isolated, public-safe compatibility experiment for the
[Task Observer project](https://github.com/rebelytics/one-skill-to-rule-them-all)
by Eoghan Henn and contributors (upstream license: CC BY 4.0).

## Purpose

Assess whether observations about repeated agent failures and explicit human
corrections can be transformed into **review candidates**, while preserving
existing responsibilities for operational learning, runtime diagnostics, and
architectural governance. The pilot must not create a second workflow engine,
operational database, or autonomous skill editor.

## Exact scope

- The root upstream `SKILL.md`, `scripts/`, and `references/` are NOT modified.
- The optional CLI at `portenart/scripts/assess-observation.mjs` is a tiny,
  deterministic, **synthetic-input-only** classifier. It does not implement
  Task Observer's full session monitoring or persistent observation log.
- It accepts only an allowlisted JSON schema. Raw emails, transcripts, names,
  addresses, user messages, business data, and arbitrary text are rejected.
- It reads from standard input and writes JSON to standard output only.
  There are no network calls or persistent writes.
- Results are advisory and remain in `PROPOSE_REVIEW` or a blocking state.
  No result constitutes an approved rule or permission to modify a Skill.
- No `AGENTS.md`, activation hooks, schedulers, workflows, CI, or installed
  skills are changed by this pilot.

## Test (offline, synthetic fixtures)

From this repository's root:

```sh
node --test portenart/tests/assess-observation.test.mjs
node portenart/scripts/assess-observation.mjs < portenart/fixtures/synthetic-events.json
```

The initial local test used Node.js 22.16.0: **10 passed, 0 failed**.
This is NOT a Codex/ChatGPT invocation test or evidence of real-session
observation, persistence, production monitoring, or live compatibility.

## Responsibilities and security boundary

- **Diagnostic owner**: investigate recurring runtime or quality failures.
- **Operational learning owner**: validate actual work-practice corrections.
- **Architecture governance owner**: arbitrate impacts and authorize the
  smallest justified change.
- **Human reviewer**: approve each proposed improvement and any eventual
  installation/activation. Approving a proposal is not executing it.
- **Canonical internal sources**: the existing private architecture and
  execution-governance documents, not this public GitHub fork.

This fork is PUBLIC. Never commit source conversations, technical credentials,
customer examples, person-level data, property records, internal audit exports, or
private observation logs. An approved persistence design must use an existing
authorized private store, never this public repository.

## Next gate

The independent fresh-session Codex review is specified in
[evaluations/CODEX_CLOUD_REVIEW_MISSION.md](evaluations/CODEX_CLOUD_REVIEW_MISSION.md)
with its [report contract](evaluations/REPORT_TEMPLATE.md). Publishing a
mission does **not** start a Codex task, activate a Skill, or prove that the
upstream Task Observer runs in Codex.

See [REVIEW_GATE.md](REVIEW_GATE.md). Review the staged code, select one bounded
platform (Codex or ChatGPT) for an opt-in integration trial, validate actual
invocation and review mechanics in an isolated environment, and approve any
runtime integration separately. Do NOT merge or install merely because the
offline tests pass.
