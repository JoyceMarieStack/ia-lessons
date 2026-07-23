# Sample dataset

Real content, straight from official NASA pages (public domain, so no copyright issue).

```
nasa-planets/
├── solar-system-overview.md
├── mars.md
└── dwarf-planets.md
```

## Why this is a genuinely good test corpus, not just a fun one

- **A real, famous terminology conflict is baked in.** `dwarf-planets.md` documents the actual 2006 IAU reclassification: Pluto was a "planet," now it's a "dwarf planet" — and the doc itself says so plainly ("Pluto was long considered our solar system's ninth planet," "Ceres... also was once classified as a planet"). This is a genuine, sourced case of a term's meaning changing over time — a good test of whether a skill can tell "inconsistent usage" apart from "the definition legitimately changed, and both old/new terms are correct depending on context."
- **A near-synonym pair to test:** "moon" vs. "satellite" — both appear (`mars.md`: "the largest satellite relative to the planet it orbits"), a fair test of whether the skill treats these as interchangeable rather than flagging false drift.
- **A nickname/epithet pattern:** "Mars" vs. "the Red Planet" — used constantly and interchangeably across `mars.md`. Tests whether the skill correctly identifies this as an accepted stylistic variant (like a trade name) rather than "inconsistency."
- **Small enough to read in full** — no need to lean on frequency-prioritization shortcuts, so it's a clean test of Steps 2–3 done properly.

The concept-vs-term walkthrough that used to live here (Argo CD's
`ApplicationSet`/`AppSet` synonym conflict, the `rollback`/`revert` false-synonym
trap, etc.) moved with `markdown-ia` to the `markdown-ia-skills` repo, along
with the Argo CD worked reports it was explaining.

---

## Notes: using this in a spec-driven development (SDD) workflow

Before handing specs to a coding agent, run the terminology audit on the spec files (not the finished docs) and treat it as a pre-flight check, the same way you'd run a linter before a build:

1. **Run the audit on `specs/*.md`** instead of `docs/*.md`.
2. **Fix every true conflict before the agent ever sees the spec.** Non-negotiable — a true conflict means the same word means two different things across the spec set. An AI agent generating code from that spec doesn't know which meaning was intended in a given section; it'll guess, consistently confidently, and the mistake won't surface until the generated code does the wrong thing.
3. **Resolve every "needs stakeholder input" row before generation, not after.** The direct SDD parallel to human-in-the-loop governance — exactly the ambiguities a human needs to settle before the planning phase hands off to code generation, because once code exists, disagreement about intent gets baked into behavior instead of staying visible as a question.
4. **Feed the termbase into the agent's context directly** — this turns the audit from a report into an actual SDD artifact. `termbase.csv`'s `preferred_term` / `forbidden_variants` columns are a machine-readable ubiquitous-language table. Drop that into `AGENTS.md` or a Cursor/Claude Code rules file alongside the spec, so the agent isn't inferring the naming convention from inconsistent prose — it's given the resolved vocabulary as a constraint. That's the "structured input to reduce hallucinations" idea.

### Worked example: the job-scheduler spec

`sample-sdd-dataset/job-scheduler-spec.md` is a small teaching spec with
three ambiguities planted on purpose — one of each rule the
`sdd-terminology-audit` skill knows:

- **`AMB-SYN`** (synonym conflict): "task" vs. "job" for the same
  schedulable unit — the classic way a generated codebase grows two
  entities for one thing.
- **`AMB-POLY`** (homograph collision): "the schedule" meaning both the
  cron expression and the list of upcoming runs, sometimes in the same
  sentence's neighborhood.
- **`AMB-SCENT`** (scent failure): "purge all entries whose TTL has
  expired" when the spec defines two different time-to-lives.

It also plants two traps the audit should *refuse* to flag: a
false-synonym pair ("cancel" vs. "kill", which the spec explicitly
distinguishes — merging them would create ambiguity, not remove it) and
harmless shorthand ("cron" after the qualified first use "cron
expression"). The outputs — report with the Ambiguity Alerts block,
`termbase.csv`, and `ambiguity-alerts.csv` — are in
`sample-reports/job-scheduler/`.

### Worked example: the dark-mode change folder (multi-artifact)

`sample-sdd-dataset/openspec-dark-mode/` is a full OpenSpec layout — a
base spec plus a change folder (`proposal.md`, `design.md`, a delta
spec, `tasks.md`) — with one problem planted per artifact:

- the proposal **coins** "theme preference" for what the base spec calls
  "appearance setting" (drift at birth, inherited by every downstream
  artifact — the alert anchors at the proposal, not where the echo is
  noticed);
- the delta's MODIFIED header rewords the base requirement's title,
  which OpenSpec's exact-header matching silently turns into a duplicate
  at archive time;
- the design introduces `DisplayModeStore` with no stated bridge to the
  spec concept (while `ThemeToggle`, whose bridge *is* stated, correctly
  goes unflagged);
- a task references "the preference bridge," which nothing upstream
  establishes — the `AMB-GHOST` case.

Outputs are in `sample-reports/openspec-dark-mode/`.

### The honest limitation, worth stating plainly

A terminology audit catches vocabulary ambiguity — it will never catch a spec that's internally logically inconsistent while using perfectly consistent words (e.g., a precondition that contradicts a postcondition two sections later, both phrased with impeccably consistent terminology). That's a different failure mode than SDD's other named risks (spec drift over time, non-determinism, the code-vs-spec-as-source-of-truth debate), which sit outside what a terminology tool can see. Worth being upfront about that scope when pitching this to a team — it's one piece of spec quality, not spec review in full.
