# Task Observer pilot — Codex independent review report

Complete using observed evidence only. `UNVERIFIED` and `NOT_RUN` are valid.
Do not copy private logs, credentials, or personally identifying information.

| Gate | Result | Evidence |
| --- | --- | --- |
| `NEW_CODEX_SESSION` | UNVERIFIED / VERIFIED | Task identifier when exposed; absence alone does not block synthetic tests in a verified published runtime |
| `SOURCE_BRANCH` | UNVERIFIED / VERIFIED | Repo, branch, HEAD SHA, reference baseline |
| `ISOLATION_ENFORCED` | UNVERIFIED / PASS / FAIL | Correct fork, only accessible repository, published runtime, enforced restricted egress and no secrets/capabilities; document filesystem write permissions separately | 
| `WORKSPACE_WRITABLE` | YES / NO / UNVERIFIED | Filesystem immutability is not a prerequisite for temporary synthetic test writes; do not call the workspace read-only when writable | 
| `TEMP_TEST_WRITES` | NOT_RUN / PASS / FAIL | Test temp dir outside checkout, cleanup status and absence of unexpected repo modifications |
| `SOURCE_DIFF_LIMITED` | UNVERIFIED / PASS / FAIL | File list relative to baseline |
| `SYNTHETIC_TESTS` | NOT_RUN / PASS / FAIL | Node version, exit code, actual pass/fail counts |
| `SYNTHETIC_DECISIONS` | NOT_RUN / PASS / FAIL | Only fixture IDs and schema decisions |
| `NO_REPO_CHANGES` | UNVERIFIED / PASS / FAIL | Git status + untracked files + three blob hashes before/after; do not infer absolute immutability |
| `NO_EXTERNAL_ACTIONS` | UNVERIFIED / PASS / FAIL | Runtime permissions and trace coverage |
| `TRUE_TASK_OBSERVER_SKILL_INVOKED` | NO / UNVERIFIED / YES | This pilot does not install upstream Skill |
| `PERSISTENT_OBSERVATION_ENGINE_TESTED` | NO / UNVERIFIED / YES | This pilot contains no engine |
| `CODEX_INTEGRATION_READY` | NO / CONDITIONAL / YES | Blockers and separate approval required |

## Findings

Only concrete observations. Distinguish confirmed defects from hypotheses.

## Recommended smallest next action

Specify a separate opt-in trial in a private isolated workspace, or explain
why the task must remain blocked.

## Final verdict

Choose exactly one:

- `INDEPENDENT_CODE_REVIEW_PASS`
- `INDEPENDENT_CODE_REVIEW_INCOMPLETE` (tests run, but part of independent evidence remains unverified)
- `INDEPENDENT_CODE_REVIEW_FAIL`
- `REVIEW_NOT_RUN` (preflight failed and tests were not run)

Never claim an installed, running or production-ready observer without
independent live activation evidence.
