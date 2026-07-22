# SDD Terminology Audit Report — Background Job Scheduler

## 1. Ambiguity Alerts

```
✕ "task" vs "job" — two words for one thing (AMB-SYN)
  job-scheduler-spec.md › AS1 — "submits a task, Then the task appears in the job queue"
  AS1 and Edge Cases say "task"; FR-001–FR-007, AS2, and AS3 say "job" — both name the schedulable unit.
  Decide: confirm "job" (the term every FR uses) and replace "task" in AS1 and Edge Cases, or define "task" as a distinct concept.

△ "TTL" — shorthand with two possible referents (AMB-SCENT)
  job-scheduler-spec.md › FR-006 — "purge all entries whose TTL has expired"
  The spec defines two time-to-lives — the result cache TTL (FR-004) and the lease TTL (FR-005) — and FR-006 names neither.
  Decide: which entries does the cleanup worker purge — expired cached results, expired leases, or both? Name the TTL explicitly.

△ "schedule" — one word, two meanings (AMB-POLY)
  job-scheduler-spec.md › FR-003 — "display the schedule for each job"
  Sometimes the recurrence rule (the job's cron expression, FR-001), sometimes the list of upcoming runs ("next ten runs"; "empty schedule").
  Decide: does the dashboard show the cron expression, the upcoming-run list, or both as separately named fields?
```

The findings touch three different kinds of names — an entity ("job",
facet: object), a stored value ("TTL", facet: value), and a dashboard
field ("schedule", facet: field) — no single cluster.

## 2. Summary

- Files audited: 1 (`examples/sample-sdd-dataset/job-scheduler-spec.md`)
- Authority sources inspected: none beyond the audited specification (no implementation, schema, or documented product vocabulary was in scope)
- `✕` findings (`AMB-SYN`, two words for one thing): 1
- `△` findings (`AMB-POLY` / `AMB-SCENT`, one word or shorthand with two meanings): 2
- Unresolved terminology decisions: 2

## 3. Evidence Table

| Exact text | Anchor | Source location | Candidate concept |
| --- | --- | --- | --- |
| "the operator submits a task, **Then** the task appears in the job queue" | AS1 | job-scheduler-spec.md | Schedulable unit |
| "create a job with a name and a cron expression" | FR-001 | job-scheduler-spec.md | Schedulable unit |
| "A job queue outage MUST NOT lose queued tasks." | Edge Cases | job-scheduler-spec.md | Schedulable unit |
| "The dashboard MUST display the schedule for each job." | FR-003 | job-scheduler-spec.md | Schedule (rule vs. run list) |
| "when the schedule produces no runs … show an empty schedule" | Edge Cases | job-scheduler-spec.md | Schedule (rule vs. run list) |
| "see its next ten runs on the dashboard" | Success Criteria | job-scheduler-spec.md | Schedule (rule vs. run list) |
| "cached with a configurable time-to-live" | FR-004 | job-scheduler-spec.md | Result cache TTL |
| "a lease with a time-to-live" | FR-005 | job-scheduler-spec.md | Lease TTL |
| "purge all entries whose TTL has expired" | FR-006 | job-scheduler-spec.md | TTL referent in FR-006 |
| "Cancelling a job MUST NOT kill an in-flight process; kill is reserved for lease expiry." | FR-007 | job-scheduler-spec.md | Cancel vs. kill (distinct concepts) |

## 4. Terminology Findings

| Sentence to clarify | Concept | Rule | Facet | Variants or meanings | Judgment | Supported wording |
| --- | --- | --- | --- | --- | --- | --- |
| "When the operator submits a task, Then the task appears in the job queue" (AS1) | Schedulable unit | `AMB-SYN` | object | "task" (AS1, Edge Cases) vs. "job" (FR-001–FR-007, AS2, AS3) | `✕` | job |
| "The cleanup worker MUST purge all entries whose TTL has expired." (FR-006) | TTL referent | `AMB-SCENT` | value | result cache time-to-live (FR-004) vs. lease time-to-live (FR-005) | `△` | Unresolved |
| "The dashboard MUST display the schedule for each job." (FR-003) | Schedule | `AMB-POLY` | field | recurrence rule (cron expression) vs. list of upcoming runs | `△` | Unresolved |

## 5. Why Each Finding Matters

### `job` vs. `task`

| Field | Content |
| --- | --- |
| `Sentence to clarify` | "When the operator submits a task, Then the task appears in the job queue with status `queued`." (AS1) |
| `Interpretation A` | "task" is the same entity FR-001 calls a "job"; one concept, two names. |
| `Interpretation B` | "task" is a distinct submitted unit that becomes, or is held by, a "job"; two concepts. |
| `What could differ` | Generated entity/model names, queue record types, and endpoint names — an agent could emit separate `Task` and `Job` types, or a `TaskQueue` beside a `JobQueue`. |
| `Why context does not settle it` | AS1 sits under a story whose requirements only ever create a "job"; nothing states that a submitted "task" is that job. The queue is named "job queue" yet holds "queued tasks" (Edge Cases). |
| `Evidence` | AS1, Edge Cases ("queued tasks") vs. FR-001–FR-007 ("job" throughout), AS2/AS3 ("job"). |
| `Terminology decision` | "job" — all seven normative requirements use it consistently; "task" appears only twice in supporting scenario text (authority rule 4, consistent usage). |

### TTL referent in FR-006

| Field | Content |
| --- | --- |
| `Sentence to clarify` | "The cleanup worker MUST purge all entries whose TTL has expired." (FR-006) |
| `Interpretation A` | Purge cached run results older than the result cache time-to-live (FR-004). |
| `Interpretation B` | Purge leases older than the lease time-to-live (FR-005). |
| `What could differ` | What data the cleanup worker deletes — cached results, leases, or both — and therefore which store the worker touches. |
| `Why context does not settle it` | "entries" is unqualified, and the two requirements immediately above FR-006 each define a different time-to-live. |
| `Evidence` | FR-004 ("cached with a configurable time-to-live") vs. FR-005 ("a lease with a time-to-live"). |
| `Terminology decision` | Unresolved — the spec supports both referents and names neither in FR-006. |

### `schedule` in FR-003

| Field | Content |
| --- | --- |
| `Sentence to clarify` | "The dashboard MUST display the schedule for each job." (FR-003) |
| `Interpretation A` | Display the recurrence rule — the cron expression each job carries (FR-001). |
| `Interpretation B` | Display the list of upcoming runs — Success Criteria requires "next ten runs on the dashboard", and Edge Cases calls a run list with no entries "an empty schedule" (a cron string cannot be empty). |
| `What could differ` | What the dashboard field renders and the shape of the value behind it — a cron string vs. an array of run timestamps. |
| `Why context does not settle it` | FR-003 carries no qualifier, and the spec itself uses "schedule" both as the generator ("the schedule produces no runs") and as the generated list ("an empty schedule") in the same edge case. |
| `Evidence` | FR-001 (cron expression) vs. Success Criteria ("next ten runs") and Edge Cases ("empty schedule"). |
| `Terminology decision` | Unresolved — usage inside the audited spec is split between the two meanings. |

## 6. Settled Classification Table

Symbols: `●` supported and unambiguous · `○` benign variation · `△` one word or shorthand with two meanings (`AMB-POLY`/`AMB-SCENT`) · `✕` two words for one thing (`AMB-SYN`). Spec position: `behavioral` = normative or executable text · `contextual` = supporting prose.

| Concept | Wording found | Judgment | Spec position | Wording to use |
| --- | --- | --- | --- | --- |
| Schedulable unit | "job" (FR-001–FR-007, AS2, AS3); "task" (AS1, Edge Cases) | `✕` | behavioral | job |
| Queue holding schedulable units | "job queue" (AS1, Edge Cases) | `●` | behavioral | job queue |
| Single execution of a job | "run" (AS2, AS3, FR-004, FR-005, Success Criteria) | `●` | behavioral | run |
| TTL referent in FR-006 | "entries whose TTL has expired" | `△` | behavioral | Unresolved |
| Schedule shown on dashboard | "the schedule" (FR-003, Edge Cases) | `△` | behavioral | Unresolved |

The `●` rows are included because they bound the findings: the queue's own name consistently uses "job" (part of the evidence for preferring it), and "run" is the concept the upcoming-run reading of "schedule" is built from.

## 7. Items Needing Stakeholder Input

1. **Which entries does FR-006's cleanup worker purge?**
   Sentence: "The cleanup worker MUST purge all entries whose TTL has expired."
   Competing meanings: expired cached results (FR-004's time-to-live) vs. expired leases (FR-005's time-to-live).
   Why authority does not settle it: both time-to-lives are defined in the audited spec and FR-006 names neither.
   Decision required: state which store the cleanup worker purges and name the TTL explicitly (e.g., "result cache TTL", "lease TTL").

2. **What does the dashboard "schedule" show?**
   Sentence: "The dashboard MUST display the schedule for each job."
   Competing meanings: the cron expression vs. the list of upcoming runs.
   Why authority does not settle it: the spec uses "schedule" in both senses, including both within one edge case.
   Decision required: state whether the dashboard shows the cron expression, the upcoming-run list, or both as separately named fields.

## 8. Scope Limitation

This audit covers vocabulary ambiguity only. It does not evaluate logical
consistency, requirement completeness, technical feasibility, or
implementation correctness.
