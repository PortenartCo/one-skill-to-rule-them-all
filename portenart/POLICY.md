# Pilot safety and ownership policy

## Status

Design and test artefact only. No runtime privilege, integration, new writer,
operational task, webhook, background observer, CI automation, or Skill update.

## Data minimization

The public GitHub fork may contain only generic documentation, source code,
and entirely synthetic test cases. Production logs, addresses, names, client
records, emails, user prompts, internal case references, secret values and
unredacted observations are forbidden. Do not treat public repository branches
as private staging locations.

The offline classifier validates six fields only:

| Field | Accepted values |
| --- | --- |
| `case_id` | `SYN-` and exactly three digits |
| `signal` | `explicit_correction`, `repeated_failure`, `confirmed_pattern`, `unverified_idea` |
| `evidence` | `verified`, `reported`, `missing` |
| `occurrences` | Integer 1 to 100 |
| `owner` | `execution_health`, `operational_learning`, `architecture`, `unknown` |
| `data_class` | `synthetic`, `non_synthetic` |

`verified` means **declared verified by the supplied synthetic fixture**. The
script does not independently authenticate any evidence. Never use this script
as a proof gate for a real decision. Extra fields are rejected; the CLI prints
a fixed error without replaying input.

## Decisions

- `PROPOSE_REVIEW`: candidate for an authorized reviewer; NOT applied.
- `NEEDS_EVIDENCE`: cited evidence has not been declared verified.
- `NEEDS_MORE_CASES`: repetition is insufficient for a repeated-failure claim.
- `NEEDS_OWNER`: ownership remains to be assigned by governance.
- `NOT_ACTIONABLE`: a mere idea does not become an operational rule.
- `BLOCKED_NON_SYNTHETIC`: this public pilot must not process real records.

Every output carries `effects: NONE`. No approval flow, modification flow,
worker retry, queue, state database, or agent activation is part of this code.

## Governance of observations

1. Capture the signal only through a separately authorized, private boundary.
2. Retain source provenance and distinguish observations, claims and proofs.
3. Send runtime quality findings to the existing diagnostic owner.
4. Send observed work practice improvements to the existing learning owner.
5. Send cross-skill responsibility changes to the architecture owner.
6. Do not promote a pattern to policy without authority, counter-examples,
   human review, and a regression test.
7. Make any future Skill change in a distinct reviewed delivery package. Never
   overwrite an installed Skill simply because this pilot generated a proposal.

## Explicit non-goals

Do not add global prompts, always-on hooks, automatic PR creation, automatic
Skill rewrites, retention jobs, or a second permanent observation store. The
upstream Task Observer activation instructions are NOT enabled by this pilot.
