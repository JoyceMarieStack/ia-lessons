---
name: terminology-audit
description: >
  Scan a corpus of documents for lexicon drift — where different words are used
  for the same concept, or the same word carries incompatible meanings across
  sources. Produces a stem & leaf diagram in ASCII/Markdown showing which terms
  dominate, which conflict, and where the most damaging ambiguity lives.

  Use this skill whenever the user asks for a terminology audit, vocabulary
  analysis, lexicon review, or wants to understand how their docs use a specific
  term. Also trigger when the user asks for a stem and leaf diagram, mentions
  inconsistent terminology across docs, wants to know "how do we talk about X",
  or wants to surface naming conflicts in a set of standards, specs, or
  architecture documents.
---

# Terminology Audit

## What this skill produces

A Markdown file containing a stem & leaf diagram. Each **stem** is an underlying
concept — what the author was reaching for. Each **leaf** is a real term from a
real source, colour-coded by how precisely it matches the stem. A frequency bar
shows which terms dominate the corpus.

The output goes in the user's selected folder as `terminology-audit-<topic>.md`.

---

## Inputs

- **Corpus**: a folder path, a set of files, or text pasted inline. If the user
  has a folder selected in Cowork, scan that. If they paste text, treat each
  paste as one source.
- **Focus** (optional): a concept or question like "how do we talk about
  ownership?" or "deployment terminology". If not given, auto-detect the 3–5
  most fragmented concept clusters in the corpus.
- **Output path** (optional): defaults to the user's selected folder.

---

## Process

Work through this in two strict phases. Mixing them produces sloppy counts.

### Phase 1 — Extract (no judgment yet)

Scan the corpus. For each file or source:

1. Find terms that carry definitional weight: headings, bold text, first use in
   a section, phrases like "X means…", "X is defined as…", or any term that
   appears in a normative statement.
2. Also collect high-frequency terms (appearing 3+ times in a single document).
3. Count occurrences **per source** (file or document), not globally. The source
   name on each card comes from the filename or document title.
4. Record: term | source | count | a one-line context snippet (what was the
   sentence doing when it used this term?).

Do not classify yet. Build a flat list.

### Phase 2 — Cluster, classify, and render

**Cluster into stems.** Group the term list into 3–6 concept families. A stem is
the underlying idea, not the word. Ask: if you stripped the words away and
described what the author *meant*, which terms are describing the same thing?
Name each stem as a short noun phrase (3–5 words). Group stems into 2–3 sections
by layer or intent — for example: "Technical Model", "Operational", "Ambiguous /
Unresolved".

**Classify each term + source** using this four-way scheme:

| Symbol | Meaning | Rule |
|--------|---------|------|
| `●` | unambiguous | Clearly scoped — one meaning, matches the stem precisely |
| `○` | correct-in-context | Technically correct but narrower or more specific than the stem |
| `△` | ambiguous | The reader has to guess which meaning applies; used inconsistently |
| `✕` | conflict | The same word appears in another source with an incompatible meaning |

Append ` △` to the term name for `△` and `✕` cards.

**Find the worst conflict.** Of all `✕` cards: which one, if misread, causes the
worst operational or compliance failure? This goes in the callout. Also note the
source that uses the term most precisely — name it as "best existing practice".

---

## Output format

Produce a Markdown file using exactly this structure. Preserve the box-drawing
characters and column alignment.

```
# Stem & Leaf — [Topic]
Each card = one source using that term.
● unambiguous  ○ correct-in-context  △ ambiguous  ✕ conflict

══════════════════════════════════════════════════════════════════════
SECTION NAME
══════════════════════════════════════════════════════════════════════

stem name            │ ● term name         source-name · 12×  ████████
(what they were      │ ○ other term        other-source · 4×  ███░░░░░
reaching for)        │ △ ambig term △      source · 2×        ██░░░░░░
                     │ ✕ conflict term △   source · 8×        █████░░░

──────────────────────────────────────────────────────────────────────

stem name 2          │ ● term              source · 6×        █████░░░
(description)        │

══════════════════════════════════════════════════════════════════════
LEGEND
══════════════════════════════════════════════════════════════════════
● Clearly scoped — unambiguous, correct for context
○ Technically correct but narrower than the stem
△ Ambiguous or inconsistent use
✕ Conflict — same word, incompatible meaning across sources

══════════════════════════════════════════════════════════════════════
⚠  THE CONFLICT THAT MATTERS MOST
══════════════════════════════════════════════════════════════════════
[Name the worst ✕ conflict in one sentence, then explain why it matters
operationally — what goes wrong when someone reads the wrong meaning.]

THE BEST EXISTING PRACTICE
[Name the source that uses the term most precisely and why it works.]
```

### Frequency bar rules

- 8 blocks wide: `█` filled, `░` empty.
- Scale to the highest count in **this diagram** (that card gets `████████`).
- Minimum 1 filled block for any card with count ≥ 1.
- If no count is available (e.g. inline pasted text with no repetition data),
  omit the bar entirely for that card.
- The `N×` label sits immediately after the bar, separated by two spaces.

### Column alignment

- Stem column: right-pad stem name + description to 20 chars, then ` │ `
- Symbol + term: left-align, pad to 24 chars
- Source: left-align, pad to 32 chars  
- Bar + label: 8 chars + `  N×`
- Aim for ~95 chars total line width; wrap long descriptions onto a continuation
  line indented to match the cards column.

---

## Edge cases

**No conflicts found.** If everything is unambiguous, say so in the callout and
note which source has the most consistent usage.

**Tiny corpus (< 3 sources).** Still run the audit. Note in the subtitle that the
diagram reflects a small sample and conflicts may emerge as more sources are added.

**Term appears in only one source.** Include it if it carries definitional weight
or is a candidate for conflict with another term. Omit purely incidental mentions.

**Focus not given.** Scan the top 50 most-frequent non-trivial terms (ignore
stop words, code keywords, and boilerplate). Pick the 3–5 families with the most
internal variation — those have the most useful drift to surface.