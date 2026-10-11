# Task Observer pilot — Codex independent review report

Complete using observed evidence only. `UNVERIFIED` and `NOT_RUN` are valid.
Do not copy private logs, credentials, or personally identifying information.

| Gate | Result | Evidence |
| --- | --- | --- |
| `NEW_CODEX_SESSION` | UNVERIFIED / VERIFIED | Fresh task identifier or exact lack of it |
| `SOURCE_BRANCH` | UNVERIFIED / VERIFIED | Repo, branch, HEAD SHA, reference baseline |
| `ISOLATION_ENFORCED` | UNVERIFIED / PASS / FAIL | Actual sandbox controls, not just requested flags |
| `SOURCE_DIFF_LIMITED` | UNVERIFIED / PASS / FAIL | File list relative to baseline |
| `SYNTHETIC_TESTS` | NOT_RUN / PASS / FAIL | Node version, exit code, actual pass/fail counts |
| `SYNTHETIC_DECISIONS` | NOT_RUN / PASS / FAIL | Only fixture IDs and schema decisions |
| `NO_REPO_CHANGES` | UNVERIFIED / PASS / FAIL | Git status before/after; note blind spots |
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
- `INDEPENDENT_CODE_REVIEW_FAIL`
- `REVIEW_NOT_RUN`

Never claim an installed, running or production-ready observer without
independent live activation evidence.
