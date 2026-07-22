# Feature Specification: Background Job Scheduler

**Feature ID:** `002-job-scheduler`

> This is a small, self-contained teaching spec written for the
> `sdd-terminology-audit` worked example. Several terminology problems are
> planted deliberately, along with two traps that a good audit should
> *not* flag. The audit outputs live in
> `examples/sample-reports/job-scheduler/`.

## User Story 1 — Recurring background work

As an operator, I want to register recurring background work with a cron
expression so that maintenance runs happen without manual triggering.

### Acceptance Scenarios

- **AS1:** **Given** a valid cron expression, **When** the operator
  submits a task, **Then** the task appears in the job queue with status
  `queued`.
- **AS2:** **Given** a job in status `running`, **When** the operator
  cancels it, **Then** the run finishes its current step and the job
  moves to status `cancelled`.
- **AS3:** **Given** a job whose run exceeds its lease, **When** the
  lease expires, **Then** the runner kills the process and records the
  run as `expired`.

## Requirements

- **FR-001:** The system MUST allow an operator to create a job with a
  name and a cron expression.
- **FR-002:** The system MUST validate the cron before accepting the job.
- **FR-003:** The dashboard MUST display the schedule for each job.
- **FR-004:** Completed run results MUST be cached with a configurable
  time-to-live.
- **FR-005:** Each run MUST hold a lease with a time-to-live; the runner
  MUST NOT extend a lease more than twice.
- **FR-006:** The cleanup worker MUST purge all entries whose TTL has
  expired.
- **FR-007:** Cancelling a job MUST NOT kill an in-flight process; kill
  is reserved for lease expiry.

## Edge Cases

- What happens when the schedule produces no runs within the next year?
  The dashboard MUST show an empty schedule rather than an error.
- A job queue outage MUST NOT lose queued tasks.

## Success Criteria

- Operators can register a job and see its next ten runs on the
  dashboard.
- No cached result is ever served past its TTL.
