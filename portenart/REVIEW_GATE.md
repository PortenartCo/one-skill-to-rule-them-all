# Review gate - isolated observer pilot

## Current evidence (offline preparation and Codex reports)

| Control | Result | Evidence / limits |
| --- | --- | --- |
| Isolated GitHub branch | VERIFIED | Published and compared against fork `main`; all additions remain under `portenart/` |
| Upstream Task Observer unchanged | DESIGNED | Only `portenart/` additions; verify with GitHub compare after push |
| Synthetic classifier | PASS | Deterministic allowlisted schema and advisory output |
| Offline tests | PASS | 10/10 on Node.js 22.16.0; zero failing tests |
| Authentic upstream helper scripts | PASS_SYNTHETIC | Three byte-identical upstream scripts; 36/36 sandbox checks (start scan, write, skill lookup, archive, ID floor, concurrency). [Report](evaluations/UPSTREAM_NATIVE_HELPERS_PILOT_20261012.md) and [replay script](tests/upstream-native-smoke.py) |
| No CLI file creation in test | PASS | Child process run in empty temporary directory; listing unchanged |
| Raw text rejection | PASS | Unexpected fields and non-synthetic class blocked |
| Network / production / live account access | NOT TESTED | Not exercised and not authorized; no such implementation in pilot |
| Codex independent synthetic execution | REVIEW_NOT_RUN | The latest user-provided Cloud report confirms source blobs/diff but does not prove the effective network restrictions, runtime credential boundary or exclusive tool permissions; no tests run in Cloud |
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

## Latest runtime verification — published Cloud revision (user-reported)

A more recent Codex report verifies the correct fork, detached HEAD at
`07a7d926ad986548b8d5dac1db9fc9687c0060ef`, and the three expected
pilot blob hashes. It reports a published Cloud runtime (revision 3),
restricted outbound network policy ENFORCED, one repository declared,
and no secrets, outbound identities, runtime variables or privileged
capabilities. Git status was clean both before and after preflight.

Synthetic tests were NOT_RUN because the earlier mission demanded
filesystem-wide immutability. Inspection of the actual test source
shows it creates and removes a temporary directory in the OS temp
location, not in the Git checkout. This strictness is unnecessary for
a synthetic-only review. The mandate is now **corrected**: perform the
three allowlisted local Node commands with a clean checkout and an
enforced restricted network, permit transient OS temp writes, and
recheck Git status/untracked files/blob hashes after tests. Neither
file-system immutability nor an exposed fresh-task ID is a mandatory
gate for this bounded synthetic evaluation. Report unverified
system-wide guarantees as limits, not as proven properties.

**Do not claim an installed/operational Task Observer.** Independent
code review and all actual integration/activation gates remain separate.
The report is user-supplied, not independently authenticated Cloud
telemetry. Do not publish session IDs, proprietary logs or other
repositories' identities in this public fork.

## Separate local reproduction — completed

A separate local execution, **not a Codex Cloud review**, reproduced the
three exact pilot Git blob hashes and ran the complete synthetic Node.js
test suite under a minimal explicitly set process environment.

- Node.js v22.16.0: **10/10 PASS, 0 FAIL**, exit 0.
- Synthetic CLI: **2 PROPOSE_REVIEW, 1 NOT_ACTIONABLE**,
  all `effects: NONE`, exit 0.
- Pilot script/test/fixture Git blob hashes: unchanged before and after.
- GitHub PR file comparison: all paths remain under `portenart/`.
- No real customer data, Skill installations, hooks, writes to the public
  repo or external integrations were involved in this local execution.

This is evidence of standalone synthetic classifier correctness ONLY.
It is not evidence of operational Task Observer observation collection,
CodeX session-start activation, or real-data integration.

## Most recent Codex Cloud attempt — unresolved environment attestation

The latest user-supplied Cloud report verifies the intended repository,
pilot blobs and bounded source diff but stops before tests: effective
network restriction status is not demonstrably enforced, and the runtime
credential/tool boundary is not certifiable from the available evidence.
The mere presence of a credential variable **name** is not evidence of a
usable secret, and available agent-side connectors are not proof they were
invoked. Conversely, their existence cannot be treated as a verified
isolation boundary.

Mark `CLOUD_SYNTHETIC_TESTS=NOT_RUN`; do not upgrade to
`CLOUD_REVIEW_PASS`. Stop repeating the same Cloud preflight until its
isolation controls can be verified through platform configuration and
runtime evidence. Avoid copying any user-specific environment identifiers
or credentials into this public repository.

## Prochain protocole d'invocation par agent

Le seul jalon restant avant de pouvoir juger un usage reel de Task Observer est un test d'agent **explicitement opt-in**, avec deux sessions sur des corrections totalement fictives, aucune Skill installee et un stockage prive approuve. Le [protocole de prochaine phase](evaluations/OPT_IN_AGENT_SESSION_PILOT.md) est prepare, mais **non execute**. Il ne certifie ni hook global ni detection autonome.

## Gate for next phase

A reviewer must verify: (a) the public/private data boundary; (b) absence of a
second learning or diagnostic authority; (c) actual platform behavior in a
new isolated session; (d) a private evidence and retention model if real
signals are ever permitted; and (e) an independent diff / non-regression
check. No test in this document proves an always-running observer.

**Decision: LOCAL_SYNTHETIC_TESTS=PASS; ORIGINAL_UPSTREAM_HELPERS_SYNTHETIC=PASS; CODEX_CLOUD_REVIEW=REVIEW_NOT_RUN; AGENT_SESSION_ACTIVATION=NOT_TESTED; INTEGRATION_NO_GO; ACTIVATION_NO_GO.**
