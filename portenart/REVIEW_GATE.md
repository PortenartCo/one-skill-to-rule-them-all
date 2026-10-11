# Review gate - isolated observer pilot

## Current evidence (offline preparation and Codex reports)

| Control | Result | Evidence / limits |
| --- | --- | --- |
| Isolated GitHub branch | VERIFIED | Published and compared against fork `main`; all additions remain under `portenart/` |
| Upstream Task Observer unchanged | DESIGNED | Only `portenart/` additions; verify with GitHub compare after push |
| Synthetic classifier | PASS | Deterministic allowlisted schema and advisory output |
| Offline tests | PASS | 10/10 on Node.js 22.16.0; zero failing tests |
| No CLI file creation in test | PASS | Child process run in empty temporary directory; listing unchanged |
| Raw text rejection | PASS | Unexpected fields and non-synthetic class blocked |
| Network / production / live account access | NOT TESTED | Not exercised and not authorized; no such implementation in pilot |
| Codex fresh-session invocation | REVIEW_NOT_RUN | Bounded metadata-only discovery subsequently found no target checkout and did find another accessible repository; Cloud selection must be corrected before any test |
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

## Later attempt: non-Git workspace root (reported, not independently replayed)

A further user-provided Codex report ran `git rev-parse` and `git status`
from `/workspace` and obtained `fatal: not a git repository`. It did NOT
inspect first-level or second-level checkout directories. Therefore it
establishes only `WORKSPACE_ROOT_IS_GIT=NO`; `TARGET_CHECKOUT_PRESENT`,
`SOURCE_BRANCH` and `ISOLATION_ENFORCED` remain UNVERIFIED by that attempt.
No tests were run. Do not present this as a confirmed environment misrouting,
nor as independent code failure.

The subsequent bounded discovery has now been reported by the user.
It found no target checkout and found a different accessible repository.
Do not retry in that task. A properly selected and PUBLISHED Cloud
environment, with only the target GitHub fork included, followed by a
NEW Cloud task is a required external configuration gate. Do not publish
private session identifiers or the names or contents of other repositories.

## Latest Cloud report: bounded checkout discovery (user-reported)

The reviewer checked Git metadata at bounded depth under `/workspace`.
The target fork was not among the discovered usable Git checkouts; an
unrelated Git checkout was present. The reported verdict was
`REVIEW_NOT_RUN`, with `SOURCE_BRANCH=UNVERIFIED`,
`ISOLATION_ENFORCED=FAIL`, and both synthetic test stages `NOT_RUN`.
These are reported observations, not independently authenticated
Cloud telemetry.

**No further prompt-only retry in the same environment.** First change
the Cloud environment's **Repositories** selection in the Codex UI
and publish it; start a fresh task from that published environment.
If the target repository is missing from the selector, verify that the
Codex-connected GitHub account and GitHub App installation are explicitly
authorized for this repository. ChatGPT's separate GitHub connector
working is not proof that Codex Cloud has the same repository access.
Reference: https://developers.openai.com/codex/environments/cloud-environments

## Gate for next phase

A reviewer must verify: (a) the public/private data boundary; (b) absence of a
second learning or diagnostic authority; (c) actual platform behavior in a
new isolated session; (d) a private evidence and retention model if real
signals are ever permitted; and (e) an independent diff / non-regression
check. No test in this document proves an always-running observer.

**Decision: REVIEW_NOT_RUN after bounded Cloud preflight; ENVIRONMENT_SELECTION_HUMAN_REQUIRED; READY_FOR_CODE_REVIEW only after correct exclusive checkout; NOT READY_FOR_ACTIVATION.**
