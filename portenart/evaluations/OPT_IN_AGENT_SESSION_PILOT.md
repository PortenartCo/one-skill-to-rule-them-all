# NEXT GATE — opt-in Task Observer agent-session experiment

**STATUS: SPECIFICATION ONLY. NOT INSTALLED, NOT EXECUTED.**

The reproducible native-helper sandbox pilot passed (see
[UPSTREAM_NATIVE_HELPERS_PILOT_20261012.md](UPSTREAM_NATIVE_HELPERS_PILOT_20261012.md)).
That proves shell helper behavior, **not** the model's ability to notice an
improvement and invoke the Skill in an agent session.

## Preflight completed — two distinct OS processes, NOT two agents

A new fully reproducible synthetic handoff check is provided in
[the two-process preflight](../tests/two-process-agent-preflight.py).

- It directly verifies the three original upstream helper Git blob hashes.
- A standalone subprocess creates one fictional observation using the
  original shell helpers; a NEW subprocess receives only the shared
  temporary workspace path, scans its frontmatter, loads the target
  fictional Skill and reads the existing observation.
- The record SHA-256 remains unchanged, there are zero duplicates, and
  the private test directory is removed at completion.
- **Five consecutive runs PASS**, with no journal exported or kept.
- **Three negative-path gates PASS**: a tampered helper is rejected;
  an invalid phase is rejected; an out-of-sandbox path is rejected.
- The published runner is byte-identical to the tested file (Git blob
  `9580f77ff5dba17847e99aa2a8bde5045cb51877`).
- These are **processes, not agent sessions**. No real language-model
  invocation, automatic discovery, or persistence across genuine Cloud
  tasks is certified.

To reproduce in a Linux checkout of this fork, use Python 3.9+ and Bash:

```sh
python3 portenart/tests/two-process-agent-preflight.py
```

Separate optional agent prompts are now ready:
[Session A](OPT_IN_AGENT_SESSION_A_PROMPT.md) and
[Session B](OPT_IN_AGENT_SESSION_B_PROMPT.md). Do not run them in a
credentialed or connector-enabled work environment.

## Owner and boundaries

- No changes to Portenart's installed Skills, agent assignments, global
  prompts, AGENTS.md, hooks, production or SharePoint/Supabase records.
- An explicitly selected, temporary agent task is the only allowed trigger.
  No global startup rule and no automatic background observation.
- No external services or connected Portenart tools. No GitHub, email,
  SharePoint, Supabase, Railway, Outlook, webhooks or production access.
- Use a separate **private** synthetic-only workspace and a sandboxed
  runtime with no secrets/credential variables or privileged connectors.
  Do not use the existing Cloud task whose effective environment restrictions
  and credential boundary could not be attested.
- The Skill under evaluation is the **unmodified upstream** Task Observer
  v3.6.0, with proper CC BY 4.0 attribution. Its source instructions
  are treated as the candidate behavior under test, not authority to
  override system or organizational restrictions.
- The journal is not a new source of truth. Every hypothetical proposal
  stays an advisory output; domain owners remain the existing diagnostic,
  learning and supervision Skills.

## Session A — user correction is a synthetic observation

The test agent receives only this wholly fictional activity:

> Draft a checklist for the imaginary "Blue Meteor" paper-airplane club:
> registration, approval, communication. The synthetic user corrects the
> draft: "Approval and sending are not the same step. Label them separately.
> Do not state that the message was sent when only a draft exists."

Expected observations, subject to model judgment:
1. Record **one** candidate observation using the original helper
   `scripts/new-observation.sh` in the private pinned workspace, with a
   valid numbered YAML frontmatter and `status: open`.
2. Distinguish **reported correction** from proven generalized best
   practice; do not promote a rule automatically.
3. Route the candidate to the existing appropriate learning/governance
   owner without writing to that owner's real persistent store.
4. Produce an explicit report of whether the agent invoked the original
   Skill instructions **before** planning and whether any step was missed.
5. Never publish the fictional journal to this public GitHub fork.

## Session B — separate invocation and reload

Start a **new** authorized agent session with access to the **same private
synthetic workspace** but no previous session transcript. If a shared
workspace is not possible, report `PERSISTENCE_NOT_TESTED`; do not
substitute a GitHub commit or uncontrolled export.

Expected:
1. Re-probe the pinned workspace and run the original
   `scripts/session-start-scan.sh`.
2. Run `scripts/skill-load.sh` against the fictional target Skill and
   confirm the open observation is found by its numbered id.
3. Read the fictional observation only, summarize the proposed improvement,
   and leave `status: open`. No Skill edit or installation.
4. Check checkpoint provenance and absence of duplicate files.
5. Inspect trace coverage. A prompt that asks the agent to use Task
   Observer proves **opt-in manual behavior**, not automatic global
   invocation.

## Evidence and verdict

Capture: runtime identity/permissions, source commit and helper blob hashes,
startup time/step trace, fake observation filename/id, before/after directory
snapshot, second-session reload, and exact Skill-change count (must be zero).

- `NATIVE_HELPERS_SYNTHETIC_PASS`: already demonstrated offline.
- `OPT_IN_AGENT_SESSIONS_PASS`: requires both session traces and observed
  model behavior, not a script-only rehearsal.
- `AUTOMATIC_SESSION_START`: remains **NOT_TESTED** without a separately
  approved mechanism and new-session evidence.
- `PERSISTENT_PRIVATE_STORAGE`: remains **NO_GO** pending an approved owner,
  retention specification, permissions, and reconstructibility contract.
- `PORTENART_INTEGRATION` and `PRODUCTION`: **NO_GO**.

Stop and report `AGENT_TRIAL_NOT_RUN` rather than broaden permissions,
introduce credentials, modify live Skills or reuse an untrusted environment.
