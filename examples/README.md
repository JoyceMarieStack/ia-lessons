# Sample dataset

Real content, straight from official NASA pages (public domain, so no copyright issue).

```
nasa-planets/
├── solar-system-overview.md
├── mars.md
└── dwarf-planets.md
```

## Why this is a genuinely good test corpus, not just a fun one

- **A real, famous terminology conflict is baked in.** `dwarf-planets.md` documents the actual 2006 IAU reclassification: Pluto was a "planet," now it's a "dwarf planet" — and the doc itself says so plainly ("Pluto was long considered our solar system's ninth planet," "Ceres... also was once classified as a planet"). This is a genuine, sourced case of a term's meaning changing over time — a good test of whether a skill can tell "inconsistent usage" apart from "the definition legitimately changed, and both old/new terms are correct depending on context" (the same discipline it showed with rollback/revert on the Argo CD run).
- **A near-synonym pair to test:** "moon" vs. "satellite" — both appear (`mars.md`: "the largest satellite relative to the planet it orbits"), a fair test of whether the skill treats these as interchangeable rather than flagging false drift.
- **A nickname/epithet pattern:** "Mars" vs. "the Red Planet" — used constantly and interchangeably across `mars.md`. Tests whether the skill correctly identifies this as an accepted stylistic variant (like a trade name) rather than "inconsistency."
- **Small enough to read in full** — no need to lean on frequency-prioritization shortcuts, so it's a clean test of Steps 2–3 done properly.

---

## Notes: controlled vocabulary management, walked through the Argo CD example

What the Argo CD run produced is a real, worked example of a discipline called **controlled vocabulary management** — a core part of information architecture. Concept by concept:

### 1. Concept vs. term — the foundational IA distinction

The single most important idea underneath the termbase and report: *a concept and the word used to describe it are not the same thing.*

Look at a single termbase row: `term_id` names the concept (what it IS); `preferred_term` and `forbidden_variants` are the competing labels pointing at it —

```
term_id: applicationset                              ← the concept (what it IS)
preferred_term: ApplicationSet                        ← the canonical label
forbidden_variants: AppSet; App Set; app-set; Appset  ← other terms, same concept
```

This maps directly onto ISO 25964, the standard for thesauri:

- **Preferred term** — the one label designated as canonical (`ApplicationSet`).
- **Entry terms / non-preferred terms** — the others, which should route back to the preferred term rather than compete with it (`AppSet`, `Appset`).

This is exactly what `termbase.csv`'s `preferred_term` / `forbidden_variants` columns encode — not a CSV quirk, but the standard shape of a thesaurus entry or authority record, the same structure a library catalog uses to make sure "automobile," "car," and "motor vehicle" all point a searcher to the same shelf.

### 2. Synonymy vs. polysemy — two different problems that look similar

- **Synonymy** = different words, same concept. Fixable by picking a preferred term. → `destination cluster` vs. `target cluster` (both mean the same field).
- **Polysemy / homograph collision** = the same word, different concepts. Not fixable by picking a preferred term — you have to disambiguate by context or rename one usage. → `Appset-Any-Namespace.md`'s casing colliding with the real `ApplicationSet` CRD name.

The report's "Notes" column carries this distinction in prose rather than a symbol — flagging a row as a genuine synonym pair to standardize (`destination cluster`/`target cluster`) reads and is fixed completely differently than flagging a row as a true collision (`Appset-Any-Namespace.md`, called out explicitly as "the one true naming collision" in the report). Not a wording nuance: these two problems need entirely different fixes, and conflating them in the write-up would send a team down the wrong one.

### 3. False synonyms — the trap good IA work catches

The best move in the report was actually a *non-fix*: `rollback (16)` vs. `revert (12)` — genuinely different concepts that happen to sound similar, correctly kept distinct.

This is the inverse of the mistake beginners make: seeing two similar-sounding words and assuming they're a "vocabulary inconsistency" to merge. A naive frequency-based tool would flag rollback/revert as a variant pair (they're near-synonyms in casual English). Recognizing that Argo CD uses them for two different features (application-history rollback vs. Git/PR revert) is domain modeling — understanding what the words refer to, not just how they're spelled. Same with `OutOfSync` vs. `out-of-sync` vs. `out of sync` — not inconsistency at all, just English grammar (attributive vs. predicate adjective forms), correctly left alone.

### 4. Faceted classification — grouping concepts by type, not alphabet

Read down the Argo CD report's "Inconsistencies found" table and the concepts fall into natural clusters even with no explicit section headers: object/CRD names (`ApplicationSet`, `AppProject`), states and operations (`OutOfSync`, `out of sync`, `rollback` vs. `revert`), and unexpanded abbreviations (`SSO`, `CMP`). That's a lightweight version of faceted classification — organizing not by alphabetical term but by *type of thing*. Same underlying move as a card-sorting exercise in website IA: not "what do we call this," but "what kind of thing is this, and does that grouping reveal a pattern?" Here it reveals that most of the real, actionable problems cluster in "abbreviations" — a genuinely useful diagnostic that falls out of reading the table by type instead of top to bottom.

### 5. Findability and information scent

Several high-traffic top-level pages (`index.md`, `getting_started.md`) use "SSO" with no expansion anywhere on the page — a first-time reader has to infer the meaning.

This is the IA concept of *information scent*: whether a piece of content gives a reader (or a search engine, or an AI) enough signal to know what it means without external context. An unexpanded acronym on an entry-point page is a scent failure — someone arriving cold has nothing to follow.

### 6. Governance — the part most people skip

Recommendation #4 in the report — "add a Terminology section to the style guide" — is the least flashy line but arguably the most important IA concept of all: **controlled vocabularies decay without stewardship.** A termbase is a snapshot; the moment a new contributor writes a doc next week, drift starts again unless there's a living reference and a process (this is why library science has "authority control" as an ongoing job, not a one-time project). The audit produced the artifact; it didn't solve the organizational problem — it handed over the tool to solve it.

**The throughline:** good information architecture isn't about eliminating every variant word — it's about correctly classifying which variants are (a) harmless register differences, (b) real synonym drift worth fixing, or (c) actual concept collisions — and building a structure (termbase + governance) that keeps new content from re-introducing the problem.

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
