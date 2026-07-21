---
name: markdown-docs-corpus-discovery
description: >
  Perform initial reconnaissance of a Markdown documentation corpus (a
  git repo or folder of .md/.mdx files). Produces a corpus inventory,
  repository structure map, and recommendations for deeper analysis.
  Use when the user wants to understand "what documentation do we
  have," audit or inventory a Markdown docs repository, get a
  first-pass map of a docs-as-code corpus before deeper work, or asks
  "what's in our docs," "how mature is our documentation," "audit our
  docs repo," or "give me a corpus overview." Scoped to Markdown only —
  a poor fit if the corpus is primarily Confluence exports, Word docs,
  PDFs, or HTML. Does not classify documents into types or infer a
  schema — that's markdown-content-model-discovery's job. First step in
  an IA analysis suite (with markdown-content-model-discovery and
  markdown-vocabulary-governance) — trigger this first for any
  IA/documentation-quality work on a Markdown corpus not yet run in the
  conversation.
---

# Markdown Docs Corpus Discovery

First-pass reconnaissance of a **Markdown-only** documentation corpus.
Answers: what exists, how is it organized, what's missing, and how
mature is it — before any deeper Information Architecture work (content
modeling, vocabulary governance, etc.) begins.

**This skill does not classify document types or infer a schema.** That
overlaps with `markdown-content-model-discovery`, which does it properly
(frequency-based required/optional field analysis, confirmed section
patterns). If you find yourself bucketing files into "Guide / ADR /
Policy / Reference" here, stop — that's the next skill's job, not this
one's. This skill stays at the level of directories, file counts, and
freshness/provenance signals, not document semantics.

**Scope: `.md` and `.mdx` files only.** This skill does not inventory,
parse, or count other formats (PDF, Word, HTML, Confluence exports,
etc.). If the user's corpus turns out to be mostly non-Markdown, say so
plainly and stop rather than producing a report built on a small,
unrepresentative slice — that's a "wrong tool for this corpus" finding,
not something to work around by loosening scope mid-run.

This skill runs entirely with general-purpose tools — `bash` commands
(`find`, `grep`, `git`, `wc`) and direct file reading — rather than a
bundled analysis script. Documentation corpora vary too much in
convention for a one-size-fits-all parser to be fully trustworthy, and
reading real files instead of trusting a regex is what catches the
exceptions that matter (a "frontmatter" block that's actually a
horizontal rule, a folder name that doesn't mean what it looks like,
etc.). Work through the steps below using judgment at each one, not
just command output.

Works best on small-to-medium corpora (dozens to a few hundred `.md`/
`.mdx` files) since it's built around sampling files by hand. On a very
large corpus (thousands+), be upfront in the report that the sample is
necessarily partial.

This is skill 1 of an IA analysis family. Its findings are useful input
for `markdown-content-model-discovery` and `markdown-vocabulary-governance`
if the user runs those next — mention that once this report is done,
rather than assuming the user wants them automatically.

## Step 1 — Locate the corpus

- **Filesystem access (Claude Code / Cowork):** ask for or infer the
  root directory. If the user references "the docs repo" or similar and
  you have file tools, look for likely candidates (a `docs/` folder, a
  repo the user has open) before asking.
- **claude.ai (uploads only):** use `/mnt/user-data/uploads`. If the
  corpus is a single zip/export, unzip it to a working directory first.
- If genuinely ambiguous, ask once rather than guessing at a large scan.

## Step 2 — Check that Markdown is actually the right scope

Before doing anything else, confirm this skill fits the corpus:

```bash
find <root> -type f -name '*.md' -o -name '*.mdx' | wc -l
find <root> -type f -not -path '*/.git/*' | wc -l
```

If the `.md`/`.mdx` count is a small fraction of total files, tell the
user directly: this skill only covers Markdown, and most of the corpus
is something else it won't analyze. Ask whether to proceed on the
Markdown subset anyway or stop here.

## Step 3 — Get the shape of the Markdown corpus

```bash
# Directory structure and how much Markdown lives in each top-level folder
find <root> -maxdepth 1 -mindepth 1 -type d
find <root> -type f \( -name '*.md' -o -name '*.mdx' \) -not -path '*/.git/*' \
  | awk -F/ '{print $1}' | sort | uniq -c | sort -rn

# Total count
find <root> -type f \( -name '*.md' -o -name '*.mdx' \) -not -path '*/.git/*' | wc -l
```

Adjust the `awk` field count if `<root>` isn't the current directory —
the goal is "which top-level folder does each Markdown file live under."

## Step 4 — Check for git signals

```bash
test -d <root>/.git && git -C <root> log -1 --format='%ci'
test -d <root>/.git && git -C <root> shortlog -sn --all | wc -l
```

If it's not a git repo, note the corpus's actual provenance (plain
export, hand-authored folder, etc.) instead of guessing.

## Step 5 — Sample and read real files

Counts from Step 3 tell you *how much* Markdown exists; they don't tell
you *what it's like*. Pick a representative sample — a handful of files
from each major top-level folder, more if the corpus is small enough to
read most of it, fewer (but still spread across folders) if it's large.
For each sampled file, actually open it with `view` and note:

- Does it have YAML frontmatter (block between `---` lines)?
- Roughly how long is it, how recently was it touched, does it read as
  authoritative/maintained or stale/abandoned?
- Any outbound Markdown links — internal cross-references, external
  URLs — and do they look intact?
- Anything that suggests the folder structure doesn't mean what it looks
  like (e.g. a "guides" folder that's actually mostly meeting notes)

You're reading to sanity-check the structural picture from Steps 3–4,
not to build a typology — resist the pull to start categorizing what
you're reading into document types. That synthesis belongs to
`markdown-content-model-discovery`.

Speed up specific checks with targeted commands instead of opening every
file by hand:

```bash
# How many files have frontmatter at all
grep -lc '^---$' <root>/**/*.md 2>/dev/null | wc -l
```

Treat this as a way to check a hypothesis formed from actually reading
files, not a substitute for reading them.

## Step 6 — Assess structure and maturity

Using the directory breakdown and git signals, characterize:

- **Repository structure**: flat vs. hierarchical, whether top-level
  folders map to a sensible organization or look ad hoc
- **Freshness**: last commit date, and what the sampled files suggested
  about how current the bulk of content is
- **Stewardship signals**: contributor count as a rough proxy for how
  many people maintain this vs. how many people it likely serves
- **Gaps**: folders or areas that seem thin relative to what the corpus
  otherwise covers, or referenced-but-missing content noticed while
  sampling — described in plain terms, not as missing "types"

Maturity is qualitative — describe it in plain terms (e.g. "early-stage:
consistent structure in one team's folder, ad hoc elsewhere") rather
than inventing a numeric score.

## Step 7 — Write the report

Produce `corpus-discovery-report.md` with these sections, **in this
order, top to bottom**. The Summary is section 1 and belongs at the very
top of the file — don't default to the habit of writing it as a
wrap-up/conclusion at the end. Write it first, before the other
sections, and place it first in the document.

**This is a first pass, not an audit — write it like one.** The report
should read as "here's a fast orientation, go deeper if you need to,"
not as a finished, fully-hedged verdict someone spent a day producing.
Two concrete constraints to keep it in that register:

- **Length budget**: aim for roughly 400–600 words of prose total
  across the whole report (tables don't count against this). If a draft
  is running long, that's a signal to move content into a table or cut
  it, not to keep writing — a first pass that takes as long to read as
  the corpus itself takes to skim has failed at its job.
- **Confidence level**: use first-impression language ("looks
  actively maintained," "reads as stable rather than stale") rather
  than settled-fact language ("is a mature, actively maintained
  documentation set"). You sampled a fraction of the corpus — the
  report's tone should reflect that it's an informed first look, not a
  completed audit.

1. **Summary** — Markdown file count, what fraction of the total corpus
   that represents (from Step 2), one to two sentences of first-pass
   impression — not a paragraph
2. **Content distribution** — table of directory breakdown from Step 3
   (file counts per top-level folder). Not a document-type breakdown —
   that's out of scope here.
3. **Repository structure** — how the corpus is organized, called out
   against what a sensible structure would look like for this content.
   If there's a nav config or index that governs the real reading
   order, note it in a sentence or two — don't narrate its full
   contents.
4. **Observations** — a short table where possible: `Observation |
   Example file(s) | What it suggests`. Reserve prose for the one or
   two observations that genuinely need more than a row to explain.
5. **Gaps** — bullet list, one line each. Not paragraphs.
6. **Out of scope** — one or two sentences: what exists outside scope
   and roughly how much
7. **Recommendations for deeper analysis** — which of the other IA
   skills would be most valuable next, and why, in a sentence or two
   each. Document typing and metadata schema questions always route to
   `markdown-content-model-discovery`, not answered here; terminology/
   taxonomy questions route to `markdown-vocabulary-governance`. When
   justifying the content-model-discovery recommendation, point to
   *evidence* of variety — file length spread, inconsistent or absent
   frontmatter, differing heading structures between files — not to
   named or grouped document types (no "task walkthroughs, reference
   specs, FAQ-style pages" style lists). Naming and grouping types is
   exactly the classification this skill hands off; if you catch
   yourself listing type labels here, even briefly, replace them with
   the underlying structural evidence instead.

Default to tables over prose anywhere the content is naturally rows and
columns (files, dates, counts, examples) — prose should be reserved for
the handful of observations that need connecting logic a table can't
carry. Cite concrete file paths as examples wherever you make a claim
about the corpus, but a short citation, not a guided tour of every
sampled file.

## Step 8 — Deliver

Before saving, double-check the file: the Summary section must be the
first thing in the document after the title, not appended at the end.
Check the prose length against the ~400–600 word budget from Step 7 —
if it's substantially over, that's a sign content needs to move into
tables or get cut, not that this corpus was a special case that
justified more. Also confirm the report doesn't contain a document-type
breakdown or schema anywhere — including inside the Recommendations
section's justification prose, where named/grouped type lists tend to
sneak back in even after Step 6 is removed. If you find one, rewrite it
as structural evidence (length variance, frontmatter presence, heading
differences) instead. Then save the report to the outputs directory
(or, in Claude Code/Cowork, wherever the user's other IA artifacts
live) and present it.