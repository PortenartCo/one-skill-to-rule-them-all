# Task Observer — manual opt-in agent Session A

**STATUS: candidate prompt, NOT executed.** This is a one-task test,
NOT a Skill installation, a startup hook, or a global AGENTS.md rule.

## Before starting

Use a NEW private agent task whose operator has verified:
- only a read-only copy of the public Task Observer source is present,
  at commit 07a7d926ad986548b8d5dac1db9fc9687c0060ef;
- no Portenart records, secrets, usable privileged connectors, or external
  system access are available; scripts have outbound networking blocked;
- the agent is supplied with an explicitly authorized **private** empty
  workspace root, outside all Git checkouts, that will remain mounted for
  an independent Session B. Do not assume a Codex Cloud task reuses its
  previous workspace. The trial may use temporary fake files there only.

If unavailable: stop with AGENT_TRIAL_NOT_RUN. Do not weaken restrictions.

## Session A task

1. Read the genuine upstream root SKILL.md and the relevant references
   for logging and session-start. Their activation guidance is a test
   candidate, NOT permission to add hooks or global instructions.
2. Answer this **fully fictional** prompt:

   "For the imaginary Blue Meteor paper-airplane club, draft a checklist
   covering registration, approval and telling members."

   Treat the following as fictional user correction:

   "Approval and sending are different steps. Label them separately.
   Do not say a message was sent when only a draft exists."

3. Revise the fictional checklist. Qualify the correction as an
   observation candidate, not an established global rule or authorization
   to contact anybody.
4. Within the *provided private workspace only*, run the genuine
   scripts/session-start-scan.sh and scripts/new-observation.sh. Write
   exactly one synthetic numbered observation using upstream YAML
   frontmatter, status: open, nonempty siblings_checked, and target
   skill: [fictional-workflow]. Do not create a real-business log.
5. Verify a single synthetic record exists, its numbered ID matches
   the frontmatter, checkpoint provenance is present, and no existing
   Skill or tracked source file was modified.
6. Report sanitized evidence only: whether the Skill was read before
   planning, command exit codes, record ID, SHA-256 of the synthetic
   record, observed file count, and the preapproved PRIVATE workspace
   path for a later Session B. Do not upload a journal to GitHub.

No commits, pushes, merges, connectors, mail, rules, hook installation,
Skill updates or persistent observation outside the short-lived pilot.

Maximum verdict: SESSION_A_MANUAL_OPT_IN_PASS, not automatic invocation.
