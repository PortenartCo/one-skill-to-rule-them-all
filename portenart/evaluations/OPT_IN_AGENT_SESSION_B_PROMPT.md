# Task Observer — manual opt-in agent Session B

**STATUS: candidate prompt, NOT executed.** Run only in a NEW agent
task/session, not a continuation of Session A.

The operator supplies the SAME authorized private synthetic workspace
root used by A, but **no Session A transcript, observation file name,
expectation or content**. Provide the unchanged original Task Observer
source at commit 07a7d926ad986548b8d5dac1db9fc9687c0060ef.

The same isolation restrictions apply: no real records, secrets, usable
privileged connectors, outbound tools, global Skill installation or
automatic hooks. Do not export the journal to GitHub.

If the designated private workspace cannot be mounted, stop with
PERSISTENCE_NOT_TESTED. Do not synthesize missing history or create an
empty substitute.

## Session B task

1. Record an actual independent task/session identifier if the runtime
   provides one. If unavailable, mark NEW_AGENT_SESSION=UNVERIFIED.
   Different subprocess IDs do not prove separate agent sessions.
2. Read the genuine upstream SKILL.md and scan instructions only as
   candidate behavior; do not activate hooks or global rules.
3. Probe the provided private workspace; run the original
   scripts/session-start-scan.sh against its root and note exact exit
   status and header count.
4. Run original scripts/skill-load.sh for fictional-workflow. Locate
   any open numbered observation **from the journal itself**, not from
   Session A output.
5. Read only that synthetic observation, summarize its proposed
   principle as a hypothetical improvement needing review, and
   leave status: open. No Skill edits, email, or business actions.
6. Verify that the observation's SHA-256 was not changed by this
   session; check checkpoint entries, duplicate IDs, source and
   installed Skill changes; none is allowed.
7. Return only sanitized evidence: session provenance (or its precise
   limit), source hash/commit, helper exit codes, open record count
   and IDs, record SHA-256, and unchanged-status confirmation.

Maximum verdict for this task: SESSION_B_RELOAD_PASS. The complete
OPT_IN_AGENT_SESSIONS_PASS requires external evidence that A and B
were truly separate agent tasks on a shared authorized private
workspace, not two scripts called within one task.

A passing opt-in pilot is NOT proof of global automatic startup and
does not authorize Portenart integration or production activation.
