---
name: terminology-audit
description: Audit technical/engineering docs for inconsistent terminology, then produce (1) a termbase/glossary of preferred terms with metadata, (2) an ASCII stem-and-leaf diagram of which terms dominate and which conflict, and (3) a written audit report of inconsistencies and recommendations. Use whenever the user asks to audit, standardize, clean up, or reconcile terminology, naming, or word choice across docs, wikis, API references, READMEs, specs, or user-facing strings — even phrased as "we use too many words for the same thing," "make our terms consistent," "build a glossary," "show me a stem and leaf diagram," or "check our naming conventions." Also trigger for vocabulary/lexicon review, "how do we talk about X," naming conflicts across standards/specs, style-guide term sections, variant/synonym cleanup, or prepping term lists for TMS/CAT localization pipelines.
---

# Terminology Audit

Audits a set of technical/engineering documents, finds places where multiple
terms are used for the same underlying concept (or the same term is used
inconsistently), and produces three deliverables:

1. **Termbase** — a structured glossary of preferred terms with metadata
   (definition, part of speech, usage context, forbidden variants).
2. **Stem-and-leaf diagram** — an ASCII/Markdown diagram showing, for each
   concept, which real-world terms ("leaves") are in use, how often, in
   which source, and whether that usage is clean or conflicting.
3. **Audit report** — a written summary of what's inconsistent, why it
   matters, and what to do about it, organized so an engineering/docs team
   can act on it.

This is fundamentally a judgment task, not a pure text-processing task.
Do the extraction and classification yourself by reading the source
documents closely — don't look for a script to do this part. The only
bundled script (`scripts/build_diagram.py`) exists purely to render the
diagram's ASCII layout once you've done the thinking; it does not do any
of the extraction or judgment.

## When there's no existing termbase to check against

Per this skill's default mode: build the termbase fresh from the provided
source documents on each run, rather than assuming a pre-existing one. If
the user does provide an existing termbase or style guide, check new usage
against that instead of inventing preferred terms from scratch.

## Workflow

### Step 1 — Inventory the source material

List every file the user provided (or ask which files/directories are in
scope if ambiguous — e.g. "just this API reference, or the whole docs
site?"). For technical/engineering docs, common sources are: README files,
API references, architecture docs, runbooks, CLI help text, config schemas,
error messages, and code comments/docstrings if the user wants UI/log strings
included too.

### Step 2 — Read and extract terms yourself (per source, not just globally)

Read through each source document directly — don't rely on a frequency
script for this. As you read, keep a running per-source tally for terms
that carry definitional weight:

- headings, bold text, first-use-in-a-section
- phrases like "X means…", "X is defined as…", or any term in a normative
  statement
- acronyms/initialisms and their expansions
- proper nouns and product/component names
- any term that recurs 3+ times in a single document

Record, for each candidate term: the term itself, which source(s) it
appeared in, a rough per-source occurrence count, and a one-line context
snippet (what was the sentence doing when it used this term?).

Watch for the false-positive traps that make naive extraction noisy:
markdown syntax that looks like an acronym (e.g. `[!NOTE]`, `[!TIP]`),
sentence-initial capitals that aren't proper nouns ("The API..."), and
raw CLI/table output that isn't prose (column headers like `STATUS
HEALTH`, literal command output). Don't count these as terminology.

Also actively look for near-miss synonym pairs that share no surface
characters — these are easy to miss by skimming for repeated substrings:
"sign up" / "register" / "create an account" all mean the same concept
despite sharing nothing textually. Catching these is exactly the value
you add over a mechanical frequency count.

### Step 3 — Concept-oriented analysis (the core skill)

For each distinct **concept** (not each word) — what the author was
reaching for, stripped of the specific word choice — work out:

1. **All the terms used for it**, per source, from Step 2 (include
   differing capitalization, pluralization, expanded vs. abbreviated
   forms, and differing part-of-speech usage — e.g. "authenticate" the
   verb vs. "Authentication" the noun heading).
2. **Whether variation is actually a problem.** One term might be a legal/
   trademarked product name, one a generic technical term for a class of
   things, or the variation may be intentional (a UI label vs. an internal
   engineering term for the same underlying object are sometimes *correctly*
   different — flag this distinction rather than flattening it).
3. **The preferred term**, using these default heuristics for
   technical/engineering content, in priority order:
   - An existing trademark, product name, or externally-published API/field
     name always wins (don't propose renaming things that are contractually
     or technically fixed, like a JSON field name in a public API).
   - Prefer the term used in the most authoritative source (spec > API
     reference > guide > blog-style doc), especially where inconsistent
     capitalization exists.
   - Prefer full/expanded forms as canonical, with acronyms noted as
     accepted shorthand after first use, unless the acronym is what
     practitioners actually search for and use in the domain.
   - Prefer the more precise/technically correct term over an informal
     synonym for engineering docs (contrast with UX copy, where the
     friendliest term usually wins — flag this if the user's material is
     borderline UX-facing).
   - When usage is a genuine toss-up, don't force a decision — mark it as
     `needs stakeholder input` and classify it `ambiguous` rather than
     guessing.
4. **A classification for every term+source pair** ("card"), using this
   four-way scheme:

   | Symbol | Meaning | Rule |
   |--------|---------|------|
   | `●` unambiguous | Clearly scoped — one meaning, matches the concept precisely, and is (or should become) the preferred term |
   | `○` correct-in-context | Technically correct but narrower or more specific than the concept |
   | `△` ambiguous | The reader has to guess which meaning applies; used inconsistently within or across sources |
   | `✕` conflict | The same word appears in another source, or another part of the same source, with an incompatible meaning |

   A term earns `✕` specifically when reusing the *same word* for two
   *different* concepts (real conflict), not merely when two words compete
   for the same concept (that's `△` on the losing variant, or `○` if it's
   just a narrower valid usage).

Out of everything classified `✕`, identify the one conflict that would
cause the worst operational or compliance failure if a reader picked the
wrong meaning — this becomes the diagram's callout. Also note which single
source uses terms most precisely and consistently overall — this becomes
"best existing practice."

### Step 4 — Build the termbase

Produce a CSV at `termbase.csv` (write it directly — a header row plus one
row per concept) with these columns:

| Column | Meaning |
|---|---|
| `term_id` | short stable slug, e.g. `access-token` |
| `preferred_term` | the canonical label |
| `part_of_speech` | noun / verb / adjective / proper noun |
| `definition` | 1–2 sentence definition in plain language |
| `usage_context` | where/how it's used, e.g. "API responses, error messages" |
| `forbidden_variants` | semicolon-separated list of terms NOT to use for this concept |
| `status` | `approved` / `needs stakeholder input` / `provisional` |
| `source_locations` | file(s)/section(s) where this concept appears |

This format is deliberately close to what Translation Management Systems
(TMS) and CAT tools expect for term imports, so the user can feed it
downstream with minimal reformatting if they're localizing content.

Quote any field containing a comma so the CSV stays well-formed (standard
CSV quoting: wrap the field in double quotes).

### Step 5 — Build the stem-and-leaf diagram

Group the concepts from Step 3 into 2–3 sections by layer or intent (e.g.
"Technical Model", "Operational", "Ambiguous / Unresolved" — name sections
to fit the actual material, this is just a starting pattern). Then build
the JSON input the renderer expects:

```json
{
  "topic": "Short topic name for the title",
  "sections": [
    {
      "name": "SECTION NAME",
      "stems": [
        {
          "stem": "concept name, 3-5 words",
          "description": "what the author was reaching for",
          "cards": [
            {"symbol": "unambiguous", "term": "access token", "source": "auth-guide.md", "count": 12}
          ]
        }
      ]
    }
  ],
  "conflict_callout": "One sentence naming the worst ✕ conflict and why it matters operationally.",
  "best_practice": "Which source uses terms most precisely, and why."
}
```

`symbol` accepts the long-form names: `unambiguous`, `correct_in_context`,
`ambiguous`, `conflict`. `count` should be your per-source count from Step 2
where available (omit `count` for terms observed only in pasted/inline text
with no reliable repetition data — the renderer will drop the bar for that
card rather than fabricate a number).

Keep each `description` to a handful of short words — the renderer wraps
on spaces only, so a single long unbroken word can get truncated mid-word
in the narrow stem column. Short, plain phrases render best.

Render it:

```bash
python3 scripts/build_diagram.py /tmp/diagram_input.json terminology-diagram.md
```

**Always use this script for the diagram — do not hand-write the ASCII
table yourself.** Fixed-width box-drawing columns and proportional
frequency bars are exactly the kind of formatting that's easy to get
subtly wrong by eye (columns drift half a character off row to row, bar
lengths stop being proportional) and hard for a reader to notice is wrong
without measuring it. The script guarantees exact, consistent alignment
every time; free-hand ASCII art does not.

**Edge cases:**
- **No conflicts found** — still build the diagram; note in `conflict_callout`
  that usage is consistent and name the most reliable source instead.
- **Tiny corpus (< 3 sources)** — still run it, but say in the topic/intro
  that conflicts may emerge as more sources are added.
- **Term appears in only one source** — include it only if it carries
  definitional weight (heading, bold, "X means…") or is a plausible future
  conflict; omit purely incidental one-off mentions.
- **No focus concept given** — don't try to diagram everything. Pick the
  3–5 concept families with the most internal variation from your Step 2
  reading — those surface the most useful drift.

### Step 6 — Write the audit report

Produce `terminology-audit-report.md` with these sections:

1. **Summary** — one paragraph: how many documents scanned, how many
   distinct inconsistencies found, overall severity read (e.g. "mostly
   cosmetic" vs "conflicting terms could confuse API consumers").
2. **Inconsistencies found** — a table: Concept | Variants observed |
   Recommended preferred term | Locations | Notes. Group by concept, not by
   individual word. This can lean on the same Step 3 analysis as the
   diagram — don't re-derive it from scratch.
3. **Items needing stakeholder input** — cases from Step 3 marked
   `needs stakeholder input`, with the competing options and why it's not a
   clear call (e.g. legal trademark vs. common usage, product naming vs.
   engineering naming).
4. **Recommendations** — concrete next steps: which docs to update first,
   whether a style-guide term section should be added, whether a review
   cadence should be established to prevent drift going forward.

Keep the report skimmable — tables over prose paragraphs wherever the
content is naturally tabular. This is a working document for a docs/eng
team, not a formal deliverable, so avoid padding it with generic
boilerplate about "the importance of consistent terminology."

### Step 7 — Deliver

Save all three files (`termbase.csv`, `terminology-diagram.md`,
`terminology-audit-report.md`) to the outputs directory and present them
together. If the user only asked for a subset (e.g. just the diagram, or
just the termbase), still run Steps 1–3 in full since the analysis is
shared, but only render/deliver the piece(s) they asked for.

## Notes on scale

For a handful of files, read them directly and do Steps 2–3 by hand as
described above — that's the default path for this skill. For a very
large corpus (dozens of files or a full docs site) where reading
everything in full isn't feasible in one pass, say so explicitly in the
report's Summary and the diagram's intro (e.g. "prioritized the most
prominent recurring terms across N files; a full manual pass would catch
additional low-frequency variants"), and prioritize the files most likely
to define core concepts (READMEs, glossaries, core-concepts docs) first.