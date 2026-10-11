# Review gate - isolated observer pilot

## Current evidence (initial local preparation and first Codex report)

| Control | Result | Evidence / limits |
| --- | --- | --- |
| Isolated GitHub branch | VERIFIED | Published and compared against fork `main`; all additions remain under `portenart/` |
| Upstream Task Observer unchanged | DESIGNED | Only `portenart/` additions; verify with GitHub compare after push |
| Synthetic classifier | PASS | Deterministic allowlisted schema and advisory output |
| Offline tests | PASS | 10/10 on Node.js 22.16.0; zero failing tests |
| No CLI file creation in test | PASS | Child process run in empty temporary directory; listing unchanged |
| Raw text rejection | PASS | Unexpected fields and non-synthetic class blocked |
| Network / production / live account access | NOT TESTED | Not exercised and not authorized; no such implementation in pilot |
| Codex fresh-session invocation | REVIEW_NOT_RUN | First Codex Cloud attempt reported wrong/non-exclusive checkout; no test executed, no target-repo status verified |
| ChatGPT Skill invocation | NOT VERIFIED | No Skill package or installation performed |
| Human approval and canonical architecture gate | PENDING | Review and separate approval required for any actual integration |
| Merge / deploy / hooks / schedulers / installed Skills | NO CHANGE | Explicit exclusions |

## First Cloud attempt — reported outcome

A user-supplied independent Codex report concluded `REVIEW_NOT_RUN`.
It stated that another repository was mounted, the pilot repo was not
checked out, and synthetic tests were `NOT_RUN`. This report has not
been independently replayed or authenticated. It does **not** change
the offline synthetic test results or certify that a live observer ran.
The detailed Cloud environment identifier and the unrelated internal
repository name are intentionally not copied into this public fork.

Next prerequisite: create a new Codex Cloud environment with **only**
the correct fork selected, publish it, start a fresh task on the
specified branch, and run the early identity/isolation preflight in
[evaluations/CODEX_CLOUD_ENVIRONMENT_SETUP.md](evaluations/CODEX_CLOUD_ENVIRONMENT_SETUP.md).

## Gate for next phase

A reviewer must verify: (a) the public/private data boundary; (b) absence of a
second learning or diagnostic authority; (c) actual platform behavior in a
new isolated session; (d) a private evidence and retention model if real
signals are ever permitted; and (e) an independent diff / non-regression
check. No test in this document proves an always-running observer.

**Decision: REVIEW_NOT_RUN on first Codex Cloud attempt; READY_FOR_CODE_REVIEW once the correct exclusive environment exists; NOT READY_FOR_ACTIVATION.**
