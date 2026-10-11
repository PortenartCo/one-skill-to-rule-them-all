# Codex integration candidate - NOT INSTALLED

This is a candidate for later review, NOT an `AGENTS.md` to be copied into a
live workspace and NOT an instruction to automatically invoke any Skill.

## Candidate opt-in instruction

> In an expressly authorized, isolated Task Observer evaluation session,
> read `portenart/README.md` and `portenart/POLICY.md` before doing anything.
> Use only pre-built synthetic, structured cases. Run
> `node --test portenart/tests/assess-observation.test.mjs`, then (optionally)
> feed `portenart/fixtures/synthetic-events.json` through the offline pilot
> classifier. Report decisions with source/test version and limitations.
> Never inspect actual user messages for this pilot, activate upstream
> session-start hooks, write observation logs, change live Skills, send
> outbound requests, or modify production.

## Before any real Codex adoption

- Approve an actual private, persistent workspace and data retention policy.
- Confirm whether an existing, governed observation mechanism already covers
  the intended job. Avoid a parallel source of truth.
- Decide how sessions are explicitly opted in. Do not inject an unconditional
  global `AGENTS.md` instruction or session-start hook at this stage.
- Independently test one fresh Codex session with no privileged connectors,
  using synthetic inputs; inspect its full trace for accidental writes.
- Keep the original upstream Task Observer source and attribution intact.

**Activation status: NO.**
