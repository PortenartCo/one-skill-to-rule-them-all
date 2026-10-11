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

Run only read-only workspace identity checks first:

```sh
pwd
git rev-parse --show-toplevel
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git status --porcelain
```

Check the configured repository identity against the exact fork. Do not
print raw remote URL values if they contain userinfo or tokens; report only
the sanitized owner/repository and GitHub host. Inspect just the immediate
workspace mount names, **never source files** from other repositories.

- If the target repository is not actually checked out: STOP.
- If the workspace contains another repository: STOP, report isolation FAIL.
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
- Running Node synthetic tests is permitted only after the preflight is
  satisfied and the prescribed tool restrictions are verifiable.

The correct first-run outcome is a factual report. Successful synthetic
tests do **not** prove the upstream Task Observer Skill activates in
Codex. Installation, observation capture, persistent storage, private
business data, or Skill mutation require separate approval.

## Minimal new-task prompt

```text
Use only the selected GitHub repository
PortenartCo/one-skill-to-rule-them-all, branch
codex/portenart-readonly-pilot-20261011, in a NEW isolated Codex Cloud
task. First verify the live checkout, branch identity, and exclusive
workspace using the preflight in
portenart/evaluations/CODEX_CLOUD_ENVIRONMENT_SETUP.md. STOP immediately
with REVIEW_NOT_RUN if the repo is absent, wrong or non-exclusive.
Only after a passing preflight, execute
portenart/evaluations/CODEX_CLOUD_REVIEW_MISSION.md as written and
report using portenart/evaluations/REPORT_TEMPLATE.md. Read-only,
synthetic inputs only. No commits, pushes, PRs, external writes,
Skill installation, hooks, merge or deployment.
```
