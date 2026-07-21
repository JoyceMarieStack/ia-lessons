---
name: markdown-vocabulary-governance
description: >
  Analyze terminology, tagging, and taxonomy consistency across a
  Markdown documentation corpus and produce two distinct governance
  artifacts: Vocabulary Governance (canonical terms with a four-way
  ambiguity classification, synonyms, preferred spellings, naming
  conventions, deprecation rules — termbase-shaped output suitable for
  TMS/localization use) and Taxonomy Design (classification facets,
  allowed values, hierarchies, metadata schema, facet governance). Use
  when the user wants to identify duplicate terminology, synonym drift,
  inconsistent tags/categories, taxonomy inconsistencies, or naming
  conflicts, or asks to build a controlled vocabulary, glossary,
  termbase, or improve tagging/classification for a knowledge base.
  Scoped to `.md` files only. Skill 3 in the
  markdown-docs-corpus-discovery, markdown-content-model-discovery,
  markdown-vocabulary-governance sequence.
---

# Markdown Vocabulary Governance

Surfaces terminology inconsistency AND taxonomy/tagging drift across a
**Markdown-only** corpus, then proposes a controlled vocabulary. This is
skill 3 of an IA analysis family (after corpus discovery and content
model discovery). If the corpus is mostly non-Markdown formats, this
skill won't have much frontmatter/prose to mine — say so rather than
force it.

Like the rest of this family, this runs with general-purpose tools —
`bash` (`grep`, `find`, `sort`, `uniq`, `sed`) and direct file reading —
rather than a bundled script. The bash commands below surface
*candidates*; deciding whether a candidate is a real inconsistency or a
false positive (a term that's correctly used two different ways, a tag
variant that's actually a different concept) is a judgment call that
requires reading the source, not just counting matches.

This skill absorbs the deep term-conflict analysis that used to live in a
separate `terminology-audit` skill — a four-way ambiguity classification
and termbase-style output, folded into the Vocabulary Governance section
below rather than split across two skills that were mining the same
sentences for the same purpose.

## Step 1 — Locate the corpus

Same as the other skills in this family: filesystem path, or
`/mnt/user-data/uploads` in claude.ai.

## Step 2 — Mine candidate terminology

```bash
# Acronyms (candidate abbreviations to define/expand)
grep -rohE '\b[A-Z]{2,6}\b' <root> --include='*.md' | sort | uniq -c | sort -rn | head -50

# Capitalized multi-word phrases (candidate proper nouns / component names)
grep -rohE '\b[A-Z][a-z0-9]+( [A-Z][a-z0-9]+){1,3}\b' <root> --include='*.md' \
  | sort | uniq -c | sort -rn | head -50
```

These will include noise — sentence-initial capitals, common words that
happen to be all-caps in some context. That's expected; the point is a
candidate list to investigate, not a final answer.

To spot spelling/formatting variants of the same term, normalize and
re-group the capitalized-phrase output:

```bash
grep -rohE '\b[A-Z][a-z0-9]+( [A-Z][a-z0-9]+){1,3}\b' <root> --include='*.md' \
  | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn > /tmp/normalized_phrases.txt
```

Compare this against the un-normalized version — entries whose count
jumps when normalized are candidate variant clusters (e.g. "API Gateway"
and "Api gateway" collapsing together). Read the actual files to confirm
before treating any cluster as a real inconsistency.

## Step 3 — Mine candidate taxonomy/facet data

```bash
# Frontmatter tag/category/label/domain values and their frequency
grep -rhE '^(tags|categories|labels|domain|topic):' <root> --include='*.md' \
  | sed -E 's/^[a-zA-Z_]+:\s*//' | tr -d '[],"' | tr ',' '\n' \
  | sed 's/^ *//;s/ *$//' | sort | uniq -c | sort -rn

# Which facet field names are actually in use — inconsistency here (tags
# vs. categories for the same purpose) is itself a governance finding
grep -rohE '^(tags|categories|labels|domain|topic):' <root> --include='*.md' \
  | sort | uniq -c | sort -rn

# Implicit taxonomy from folder structure, for comparison against tags
find <root> -type f -name '*.md' -not -path '*/.git/*' \
  | sed "s|<root>/||" | awk -F/ 'NF>1{print $1"/"$2}' | sort | uniq -c | sort -rn
```

As with terminology, normalize the tag-value list (lowercase, strip
punctuation) and compare counts to spot near-duplicate tags — then
verify by reading a couple of files using each variant.

## Step 4 — Analyze (judgment step)

For each area, read enough of the actual source docs to make real calls,
not just the extracted lists:

**Terminology drift**: for each variant cluster from Step 2, decide
real inconsistency vs. false positive. Pick a preferred form using these
heuristics, in priority order:

- An existing trademark, product name, or externally-published API/field
  name always wins — don't propose renaming something that's
  contractually or technically fixed (e.g. a public API's JSON field
  name)
- Prefer the term used in the most authoritative source (spec > API
  reference > guide > blog-style doc), especially where inconsistent
  capitalization exists
- Prefer full/expanded forms as canonical, with acronyms noted as
  accepted shorthand after first use, unless the acronym is what
  practitioners actually search for and use in the domain
- Prefer the more precise/technically correct term over an informal
  synonym for engineering docs
- When usage is a genuine toss-up, don't force a decision — mark it
  `needs stakeholder input` rather than guessing

Classify each term using this four-way scheme (this is what turns "these
words look similar" into an actual governance call):

| Symbol | Meaning | Rule |
|--------|---------|------|
| `●` unambiguous | Clearly scoped — one meaning, matches the concept precisely, is (or should become) the preferred term |
| `○` correct-in-context | Technically correct but narrower/more specific than the concept |
| `△` ambiguous | Reader has to guess which meaning applies; used inconsistently |
| `✕` conflict | The same word is used for two genuinely different concepts |

`✕` is reserved for real conflict — the same word meaning two different
things — not merely two words competing for the same concept (that's
`△` on the losing variant, or `○` if it's just a narrower valid usage).
Classify at the term level, not per individual source/file, unless a
specific conflict is genuinely source-specific — in which case name the
sources, don't just say "conflicting."

**Taxonomy/facet drift**: for each near-duplicate tag cluster from
Step 3, decide the canonical value. Separately check whether the facet
*field names themselves* are used consistently — some docs using `tags`
and others `categories` for the same purpose is a governance problem
worth flagging on its own.

**Explicit vs. implicit taxonomy mismatch**: compare the folder-based
grouping against the tag values. If they disagree about how content is
organized (e.g. folder says `security/`, tag says `domain: networking`),
note specific examples — not just that they differ in general.

## Step 5 — Build two separate governance artifacts

Vocabulary governs language; taxonomy governs classification. They're
related — a drifting facet value is often also a terminology variant —
but they answer different IA questions and get built (and eventually
owned/maintained) separately. Don't merge them into one table.

**5a. Vocabulary Governance artifact** — covers terminology used in
prose, built from Step 2's findings:

- **Canonical terms** — the preferred form for each concept identified
  in Step 4's terminology analysis, with its classification symbol
  (`●`/`○`/`△`/`✕`) and status (`approved` / `needs stakeholder input` /
  `provisional`). This is deliberately termbase-shaped — if the user
  wants a full standalone termbase CSV (e.g. for a TMS/localization
  pipeline), this table's rows already have what's needed; just export
  them to `termbase.csv` with a one-line definition added per term
  rather than redoing the analysis
- **Synonyms** — every variant observed for each canonical term
- **Preferred spellings** — casing/hyphenation/pluralization resolved
  per term (e.g. "API Gateway" not "Api gateway" or "API-Gateway")
- **Naming conventions** — any pattern you can generalize from what's
  actually observed (e.g. "component names are Title Case two-word
  phrases," "acronyms are expanded on first use in guides but not in
  reference docs") — only state conventions the corpus actually
  demonstrates, don't prescribe ones it doesn't
- **Deprecation rules** — which variants should stop being used, and
  what (if anything) should replace them going forward

**5b. Taxonomy Design artifact** — covers classification/metadata,
built from Step 3's findings:

- **Classification facets** — the facet fields in actual use (or, if
  none exist coherently, a small recommended set grounded in what the
  corpus's content actually supports). Put any "here's what we
  recommend" content directly in this subsection — don't split it into
  a separate recommendations block elsewhere in the report.
- **Allowed values** — the canonical value set per facet, resolved from
  Step 4's drift-cluster analysis
- **Hierarchies** — any parent/child structure within a facet (e.g.
  `domain: security > network-security`), and how it compares to the
  implicit folder-based taxonomy from Step 3
- **Metadata schema** — how each facet maps to a frontmatter field:
  field name, whether it's single- or multi-value, required vs. optional
  (cross-check against `markdown-content-model-discovery`'s findings if
  that skill has run)
- **Facet governance** — who should own additions/changes to allowed
  values, and a lightweight process for reviewing new facet values
  before they're used (e.g. new tags get flagged in review rather than
  silently proliferating)

## Step 6 — Write the report

Produce `vocabulary-governance-report.md` with these sections, **in this
order, top to bottom**. The Summary is section 1 and belongs at the very
top of the file — don't default to the habit of writing it as a
wrap-up/conclusion at the end. Write it first, before the other
sections, and place it first in the document.

**This is a first pass, not a finished audit — write it like one.**
Same register as `markdown-docs-corpus-discovery`: an informed fast
read someone can act on, not a fully-hedged verdict. Two concrete
constraints:

- **Length budget**: roughly 400–600 words of prose total across the
  whole report (subsection tables don't count against this — and most
  subsections below should mostly *be* tables). If a draft is running
  long, move content into a table or cut it rather than keep writing.
- **Confidence level**: "looks inconsistent between X and Y" rather
  than "the corpus suffers from significant terminology drift." You
  mined candidates and verified a sample — the tone should read as an
  informed first look, not a completed audit.

1. **Summary** — corpus size scanned, headline inconsistency count for
   each of vocabulary and taxonomy, one to two sentences of first-pass
   severity read — not a paragraph

2. **Vocabulary Governance** — language-level findings, as its own
   top-level section with subsections matching 5a directly. Each of
   these should be a table, not prose:
   - Canonical terms — table: `Term | Classification | Status | Notes`
     (classification is the `●`/`○`/`△`/`✕` symbol from Step 4; status
     is approved/needs stakeholder input/provisional)
   - Synonyms — can combine with Canonical terms into one table if that
     avoids repeating the same term list twice
   - Preferred spellings — table: `Preferred | Rejected forms`
   - Naming conventions — short bullet list, one line each
   - Deprecation rules — table: `Deprecated | Replacement | Notes`

3. **Taxonomy Design** — classification-level findings, as its own
   top-level section with subsections matching 5b directly. Same
   table-first approach:
   - Classification facets — table: `Facet | In use? | Notes`
   - Allowed values — table: `Facet | Canonical value | Rejected variants`
   - Hierarchies — short bullet list or a small nested list, not prose
     paragraphs
   - Metadata schema — table: `Facet | Frontmatter field | Cardinality
     | Required?`
   - Facet governance — a few bullet lines, not a paragraph

4. **Cross-cutting observations** — anywhere vocabulary and taxonomy
   findings reinforce or explain each other (e.g. a term that drifts in
   prose is also the facet value that drifts in frontmatter) — keep this
   section short and pointed (2–4 bullet points), it's a bridge between
   the two main sections, not a place to re-list findings already
   covered above

Default to tables over prose anywhere the content is naturally rows and
columns — which, in this skill, is nearly everything (terms, variants,
facets, values, mappings). Prose should be reserved for the handful of
things a table genuinely can't carry, like why a mismatch matters.
Working document, not a formal deliverable. Keep the two top-level
sections genuinely independent — a reader should be able to hand
"Vocabulary Governance" to whoever owns writing/style conventions and
"Taxonomy Design" to whoever owns the metadata schema, without either
needing the other section.

**Don't add sections beyond these four.** In particular, don't append a
separate "recommended facets" or "field-name governance" block after
Cross-cutting observations — that content belongs inside Taxonomy
Design's Classification facets and Facet governance subsections
respectively, not restated again afterward. If you find yourself about
to write a closing recommendations block, put that content into the
relevant subsection above instead of adding a new one at the end.

## Step 7 — Deliver

Before saving, double-check the file: the Summary section must be the
first thing in the document after the title, not appended at the end.
Check the prose length against the ~400–600 word budget from Step 6 —
if it's substantially over, move content into tables or cut it rather
than treat this corpus as a special case. Then save the report to the
outputs directory and present it. If both this skill and
`markdown-content-model-discovery` have run in the conversation, note
where their findings reinforce each other.