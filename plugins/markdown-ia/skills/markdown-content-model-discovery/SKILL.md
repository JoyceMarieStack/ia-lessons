---
name: markdown-content-model-discovery
description: >
  Infer the implicit content model (document types, common sections,
  metadata fields) of a Markdown documentation corpus without needing a
  predefined schema. Produces recommended content types, a schema per
  type (required vs. optional metadata), and validation rules. Use
  whenever the user asks "what's our content model," "what metadata
  should our docs have," "what fields are missing," wants a schema
  proposed for existing Markdown docs, is standardizing frontmatter/
  metadata across a Markdown docs corpus, or asks to infer structure
  from unstructured Markdown documentation. Scoped to `.md`/`.mdx` files
  only. Pairs with markdown-docs-corpus-discovery (run first for a
  broader inventory if the user hasn't already) and feeds into
  markdown-vocabulary-governance for terminology work.
---

# Markdown Content Model Discovery

Infers the structure documentation *already has* — even informally — and
proposes a content model (types, sections, required/optional metadata)
grounded in actual usage rather than an abstract ideal. This is skill 2
of an IA analysis family; it works well after `markdown-docs-corpus-discovery`
but can run standalone.

Like the rest of this skill family, this runs with general-purpose
tools (`bash`: `find`, `grep`, `sed`; direct file reading with `view`)
rather than a bundled script. Frequency counts from `grep`/`sort`/`uniq`
tell you *how often* something appears; reading actual sampled files is
what tells you whether that pattern is real structure or coincidence —
do both, don't skip the reading in favor of the counts.

**Scope: `.md` and `.mdx` files only.** If the corpus is mostly other
formats (PDF, Word, HTML, Confluence exports), there's little frontmatter
or heading structure here for this skill to infer from — say so rather
than force a schema from a thin, unrepresentative sample.

## Step 1 — Locate the corpus

Same as the other skills in this family: filesystem path, or
`/mnt/user-data/uploads` in claude.ai. If `markdown-docs-corpus-discovery` already
ran in this conversation, reuse its document-type read as a starting
hypothesis — but still do Step 2 below, since it captures field/heading
frequency that a first-pass inventory doesn't.

## Step 2 — Find candidate type groupings

Check for explicit type metadata first:

```bash
# Which files declare a type explicitly, and what values are in use?
grep -rlE '^(type|doc_type|category|kind):' <root> --include='*.md' --include='*.mdx'
grep -rhE '^(type|doc_type|category|kind):' <root> --include='*.md' --include='*.mdx' \
  | sed -E "s/^[a-zA-Z_]+:\s*//" | tr -d '"' | tr -d "'" | sort | uniq -c | sort -rn
```

For files with no such field, fall back to top-level folder as the
grouping (same approach as `markdown-docs-corpus-discovery` Step 2):

```bash
find <root> -type f \( -name '*.md' -o -name '*.mdx' \) -not -path '*/.git/*' \
  | awk -F/ '{print $1}' | sort | uniq -c | sort -rn
```

Treat any grouping (explicit-type or folder) with roughly 3+ files as
worth analyzing; note smaller ones but don't build a schema from a
sample that thin.

## Step 3 — Profile each group

For each candidate group, get its file list and save it for reuse:

```bash
# explicit-type group
grep -rl '^type: adr' <root> --include='*.md' > /tmp/group_adr.txt
# or folder-based group
find <root>/guides -name '*.md' > /tmp/group_guides.txt
```

Then pull frontmatter field frequency directly:

```bash
while read -r f; do
  sed -n '/^---$/,/^---$/{/^---$/d;p}' "$f" | grep -oE '^[A-Za-z_]+:'
done < /tmp/group_adr.txt | sort | uniq -c | sort -rn
```

Divide each count by the group's total file count (`wc -l < /tmp/group_adr.txt`)
to get presence percentage per field.

And heading structure frequency:

```bash
while read -r f; do
  grep -E '^#{1,3} ' "$f"
done < /tmp/group_adr.txt | sed -E 's/^#+\s*//' | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn
```

Then **read a handful of actual files** from the group with `view` —
the greps above will miss fields expressed differently (a field named
`author` in one file and `owner` in another that mean the same thing,
a heading phrased as a question instead of a noun) that only reading
catches.

## Step 4 — Turn frequency into a schema (judgment step)

For each group with enough files:

- **Required metadata**: fields present in ~80%+ of files in that group
  — de facto mandatory even if never documented as such
- **Recommended/optional metadata**: fields present in a meaningful
  minority (roughly 20–80%) — candidates for standardizing, not
  already-required
- **Incidental**: fields under ~20% presence — don't propose these as
  schema fields
- **Common sections**: heading clusters above a similar threshold become
  the type's expected structure

If folder-fallback group names don't look like real content types (e.g.
`misc`, `2023`, a person's name), say so plainly — it means there's no
consistent type-tagging convention in use, not that you should invent a
taxonomy to fill the gap.

## Step 5 — Identify missing governance metadata

Check presence of governance-relevant fields across the whole corpus,
not just per group — these are usually the most actionable finding:

```bash
grep -rlE '^(owner|steward|status|review_date|last_reviewed|id):' <root> --include='*.md' | wc -l
find <root> -name '*.md' -not -path '*/.git/*' | wc -l
```

Compare the two counts, and break down by group where useful. Call out
which of owner, status, review cadence, and stable identifier are
largely absent per type — this feeds directly into governance and
retrieval-readiness work if the user does that later.

## Step 6 — Write the content model documentation

Produce `content-model-report.md` with these sections, **in this order,
top to bottom**. The Summary is section 1 and belongs at the very top of
the file — don't default to the habit of writing it as a wrap-up/
conclusion at the end. Write it first, before the other sections, and
place it first in the document.

**This is a first pass, not a finished audit — write it like one.**
Same register as `markdown-docs-corpus-discovery` and
`markdown-vocabulary-governance`: an informed fast read someone can act
on, not a fully-hedged verdict. Two concrete constraints:

- **Length budget**: roughly 400–600 words of prose total across the
  whole report (subsection tables don't count against this — most
  subsections below should mostly *be* tables). If a draft is running
  long, move content into a table or cut it rather than keep writing.
- **Confidence level**: "looks like a de facto required field" rather
  than "this is a mandatory field for all decision records." You
  profiled a sample of groups — the tone should read as an informed
  first look, not a finalized schema spec.

1. **Summary** — how many groups/types found, one to two sentences of
   overall consistency read — not a paragraph
2. **Content types** — one row per type in a single table: `Type |
   File count | Sample files | Common sections`. Reserve prose only for
   a type whose story genuinely needs more than a row (e.g. an unusual
   fallback grouping worth explaining)
3. **Recommended schema per type** — table: `Field | Required/Optional |
   Observed in (%) | Notes`
4. **Missing metadata** — table: `Field | Present in (%) | Types most
   affected`
5. **Validation rules** — short bullet list, one rule per line, not
   paragraphs. Concrete, checkable rules the data actually supports
   (e.g. "every decision record must have a `status` field with value
   in {proposed, accepted, deprecated, superseded}") — don't propose
   aspirational rules the corpus doesn't back up
6. **Unclassified content** — one to two sentences: how much content
   didn't fit any recognized type, and what that suggests

Default to tables over prose anywhere the content is naturally rows and
columns (types, fields, percentages, counts) — reserve prose for the
handful of things a table can't carry, like why a particular gap
matters. Cite actual file paths for any claim, same as
`markdown-docs-corpus-discovery`.

## Step 7 — Deliver

Before saving, double-check the file: the Summary section must be the
first thing in the document after the title, not appended at the end.
Check the prose length against the ~400–600 word budget from Step 6 —
if it's substantially over, move content into tables or cut it rather
than treat this corpus as a special case. Then save the report to the
outputs directory and present it. If `markdown-docs-corpus-discovery`
hasn't run in this conversation and the corpus looks large or messy,
mention it could add useful context, but don't insist — this skill's
output stands on its own.