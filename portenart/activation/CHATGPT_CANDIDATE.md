# ChatGPT integration candidate - NOT INSTALLED

GitHub forking and adding files on a branch do not install a ChatGPT Skill.
The upstream bundle is Claude-oriented (environment variables, paths, hook
conventions and frontmatter). A ChatGPT version requires a separate review of
capability, packaging metadata and file persistence limitations.

For a future isolated ChatGPT pilot:

1. Keep task-observer semantics as suggestions only, not automatic rule edits.
2. Use short, compatible Skill metadata and a complete self-contained bundle;
   preserve the upstream attribution and the original source unchanged.
3. Prefer a manual, sanitized handoff for environments without a persistent
   authorized workspace. Do not invent background observation capabilities.
4. Verify invocation in a fresh conversation, then verify that no private
   content escaped to a public store or to unapproved destinations.
5. Require a separate human authorization before installation, agent binding,
   automation, persistence or any actual modifications to existing Skills.

**ChatGPT installation: NO. Agent bindings: unchanged.**
