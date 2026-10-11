# Codex Cloud environment setup — isolated evaluation only

**Status:** instructions, not proof that an environment has been created.

## Reason this is required

The first independent attempt ended with `REVIEW_NOT_RUN`: the reported
Cloud workspace mounted a different repository, and no local checkout of
this pilot was available. Codex stopped before running tests.
This is **an environment-selection failure**, not evidence that the pilot
classifier itself is defective.

The detailed task/environment identifier and other workspace's internal name
are intentionally excluded from this PUBLIC GitHub repository.

## Required UI setup (performed by the user)

Open Codex Cloud on the web or desktop. Following the [official Codex Cloud
environment documentation](https://learn.chatgpt.com/docs/environments/cloud-environments):

1. Select **Work in > Cloud**, then **Select environment > Create environment**
   (or **Settings > Codex Cloud > Environments > Create environment**).
2. Select exactly **`PortenartCo/one-skill-to-rule-them-all`** as the GitHub
   repository. No other repositories, local devices, Microsoft services,
   database integrations, or privileged connectors should be included.
   If the fork is missing, stop; confirm GitHub connection and access to this
   particular repository rather than falling back to a different one.
3. Prepare a private environment (suggested name:
   `task-observer-synthetic-review`). No secrets, outbound identities,
   additional environment variables, session-start hooks, task observers,
   or automatic Skill activation are required. Only Node.js is needed for
   the synthetic tests. Do not enable broader network access to make a
   failing setup pass.
4. Examine the setup report before choosing **Publish**. The prepared
   repository must be the fork above and only that fork.
5. Select **Start a new task** from the published environment. Select the
   branch `codex/portenart-readonly-pilot-20261011` before submission,
   where the interface exposes branch selection. Never reuse the failed
   task or the unrelated Cloud environment.
6. In the new task, request the mission
   `portenart/evaluations/CODEX_CLOUD_REVIEW_MISSION.md`, keeping all
   read-only and synthetic-only restrictions.

Environment creation is a separate, explicit user action. These files do
not create or publish an environment.

## Required Codex preflight — stop before tests on mismatch

**Do not assume the shell starts inside a Git repository.** A prompt
starting at `/workspace` can be in a container root while the actual
checkout, if provisioned, is a child directory. An error from
`git rev-parse` in `/workspace` alone proves only that this directory
is not a Git worktree; it does NOT prove the target checkout is absent.

First, execute this bounded **metadata-only** discovery (POSIX shell):

```sh
pwd
if git rev-parse --show-toplevel >/dev/null 2>&1; then
  git rev-parse --show-toplevel
else
  find /workspace -mindepth 1 -maxdepth 4 -name .git -print 2>/dev/null
fi
```

The `find` command may reveal only the paths of `.git` entries, not
the contents of any other repository. Do not expand this scan into user
home directories or other mounts. A `.git` path may be a worktree file
rather than a directory; either may designate a checkout. If `find`
is unavailable, list immediate directory names under `/workspace` and
check `<candidate>/.git` without reading source files.

For a **single** candidate, use its parent directory as
`<repo-path>` in the commands below. Do not automatically `cd`
into unrelated checkouts:

```sh
git -C "<repo-path>" rev-parse --show-toplevel
git -C "<repo-path>" rev-parse --abbrev-ref HEAD
git -C "<repo-path>" rev-parse HEAD
git -C "<repo-path>" status --porcelain
```

Check the candidate's remote origin against the exact fork, but never
print an unsanitized remote URL; it may contain credentials. If there
are multiple candidate repositories, confirm that no unrelated repo
is accessible before any tests. Record only sanitized identities in the
final report.

- If `/workspace` itself is not Git, do NOT stop until this bounded
  discovery has been attempted.
- If the scan finds NO target candidate: stop with
  `REVIEW_NOT_RUN`, `TARGET_CHECKOUT=UNVERIFIED` or
  `TARGET_CHECKOUT=ABSENT_WITHIN_CHECKED_SCOPE`, as evidence allows.
- If a wrong-origin repository is the only candidate: stop with
  `REVIEW_NOT_RUN`, `TARGET_CHECKOUT=FAIL`.
- If any other repository is mounted and accessible: stop with
  `REVIEW_NOT_RUN`, `ISOLATION_ENFORCED=FAIL`.
- Do not clone, fetch isolated files, broaden access, adjust permissions
  or execute tests to overcome any mismatch.
- A Codex task may use a temporary local branch such as `work` or a
  detached HEAD. That label alone does NOT prove the wrong source was loaded.
  Verify the sanitized GitHub origin is this exact fork and that the pilot
  source corresponds to the PR, either through Git commit ancestry or these
  unchanged expected Git blob SHA-1 values (run `git hash-object <path>`
  without `-w`, so nothing is written):
  - `portenart/scripts/assess-observation.mjs`:
    `4e207240c2bfa1113048d038844a896d1b4cc3ef`
  - `portenart/tests/assess-observation.test.mjs`:
    `d73b20def990e7d5adfbf9048a7f7849fc943c5e`
  - `portenart/fixtures/synthetic-events.json`:
    `806cc3a3273745b680bd201094dca190fa2a5860`
  These identify the synthetic pilot snapshot, NOT future file revisions.
  If origin is wrong, any blob differs, or provenance cannot be established:
  STOP and report `SOURCE_BRANCH=UNVERIFIED`. Never repair the checkout
  during this read-only task.
- If source contents or tests can only be accessed by fetching standalone
  files rather than through the checked-out target repository: STOP.
- If `git` checks or isolation probes are blocked: report `UNVERIFIED`;
  do not compensate by cloning elsewhere, changing permissions, or
  broadening access.
- For this **synthetic-only** review, a published runtime with restricted
  egress ENFORCED, just the intended accessible repo, no secrets/outbound
  identities or privileged capabilities, the correct source hashes, and a
  clean Git checkout is sufficient to begin the allowlisted Node tests.
  A writable OS workspace is **not** a reason to stop: the tests create
  and remove a temporary directory outside the repository.
  A missing visible task identifier is a reporting limitation, not a
  reason to reject an otherwise verified published Cloud runtime.
  Do NOT claim the OS filesystem is immutable or that complete action
  traces exist if those guarantees cannot be demonstrated.

Before and after tests, check the working tree and untracked files;
reconfirm the three pilot hashes. Temporary writes under the OS temp
directory are allowed; persistent checkout changes and all external
writes are prohibited. An unexpected modification is a FAIL; preserve
evidence and do not silently revert it.

If the source diff to the baseline is unavailable due to shallow Git
history, record `SOURCE_DIFF_LIMITED=UNVERIFIED` and classify the result
as `INDEPENDENT_CODE_REVIEW_INCOMPLETE` if tests otherwise pass, rather
than blocking safe synthetic test execution.

Successful synthetic tests do **not** prove the upstream Task Observer
Skill activates in Codex. Installation, observation capture, persistent
storage, private business data, or Skill mutation require separate
approval.

## Minimal new-task prompt

```text
Use only the selected GitHub repository
PortenartCo/one-skill-to-rule-them-all, branch
codex/portenart-readonly-pilot-20261011, in a NEW isolated Codex Cloud
task. First verify the live checkout, branch identity, and exclusive
workspace using the bounded metadata-only discovery in
portenart/evaluations/CODEX_CLOUD_ENVIRONMENT_SETUP.md. The directory
/workspace itself need not be a Git repository: inspect only .git entries
within /workspace at depth <=4 before deciding there is no checkout.
STOP with REVIEW_NOT_RUN if the target repo is absent after that check,
the origin is wrong, or another repository is accessible.
Only after a passing preflight, execute
portenart/evaluations/CODEX_CLOUD_REVIEW_MISSION.md as written and
report using portenart/evaluations/REPORT_TEMPLATE.md. Synthetic-only:
the repository and external systems remain unchanged. Temporary OS
test-directory creation and removal are allowed. No commits, pushes,
PRs, external writes, Skill installation, hooks, merge or deployment.
```
