---
name: vocabulary-contract
description: Turn a termbase.csv controlled vocabulary into an enforceable naming contract for spec-driven development. Use this whenever the user mentions a termbase, glossary, canonical terms, naming consistency, vocabulary drift, term linting, AGENTS.md vocabulary sections, or wants specs/proposals/generated code checked against approved terminology — even if they don't say 'vocabulary contract'. Also use when the user asks to render a glossary into agent context or to find new candidate terms after an implementation.
---

# Vocabulary Contract

Turn a `termbase.csv` (a small controlled vocabulary of canonical terms, usually
produced by a terminology audit) into an enforceable naming contract for
spec-driven development workflows (proposal → spec → tasks → implementation).
This skill needs only the CSV — it does not depend on whatever tool produced it.

Three modes. Pick the one that matches the user's request:

| Mode | The user wants to... | Typical phrasings |
|------|----------------------|-------------------|
| **Render** | Generate consumption views of the termbase | "render the glossary", "add a vocabulary section to AGENTS.md / CLAUDE.md", "make a spec preamble from the termbase" |
| **Enforce** | Check a draft document against the termbase | "check this spec", "lint the proposal for terminology", "did we use the approved terms?" |
| **Round-trip** | Find new terms an implementation introduced | "what new terms did this change add?", "scan the diff for vocabulary drift", "candidate terms for the next termbase revision" |

If the request is ambiguous, infer from the artifact offered: a termbase alone →
render; a termbase plus a draft spec/proposal/tasks file → enforce; a termbase
plus a diff, new code, or implementation docs → round-trip. When genuinely
unclear, ask. `references/openspec-workflow.md` explains where each mode sits in
the proposal → spec → tasks → implementation cycle if you need to orient the
user.

## Ground rules (all modes)

- **Advisory, never blocking.** Output findings and suggested rewrites; never
  fail, reject, or auto-edit the checked document unless the user asks you to
  apply fixes.
- **Traceability.** Every finding cites file and line; every rendered entry
  cites its source termbase row. This lets a human verify any claim in seconds.
- **The termbase is read-only.** Never add, remove, or edit termbase rows.
  Round-trip mode *proposes* candidates; a human approves them into the
  termbase.
- **Only `approved` terms are enforced.** Rows with status `candidate`,
  `provisional`, etc. are context, not contract (a missing status column means
  everything is approved).

## The termbase input

Expected columns — only `term` is required, tolerate everything else missing:

| Column | Meaning |
|--------|---------|
| `term` | canonical prose form, e.g. `extend mode`, `config.yaml` |
| `variants` | semicolon-separated banned variants |
| `code_identifier`, `file_form`, `cli_flag`, `env_var` | the term's form in each surface |
| `definition` | one-line definition |
| `status` | `approved` / `candidate`; only approved rows are enforced |

Always start any mode by running:

```bash
python scripts/check_terms.py --termbase <termbase.csv> --mode load
```

The script maps common alternative headers automatically (`preferred_term` →
`term`, `forbidden_variants` → `variants`, ...) and reports the
`column_mapping` it applied plus any `unmapped_columns`. If the user's CSV used
non-standard headers, state the mapping in your output so they can confirm it —
a silently misread column corrupts every downstream finding. If no term column
can be found at all, show the user the headers you saw and ask which column
holds the canonical term.

## Mode 1: Render

Goal: consumption views of the termbase for agents and spec authors.

1. Run `--mode load` and read the normalized terms.
2. Write an **AGENTS.md / CLAUDE.md fragment** following
   `assets/agents-md-template.md`. Agents follow imperative prose far better
   than tables, so write prose, not a table. Per approved term:
   - Canonical usage sentence, folding in the definition when present:
     *"Always write 'extend mode' when referring to ..."*
   - Banned variants as prohibitions: *"Never write 'extension mode' or
     'inherit mode'."* Omit the sentence when there are no variants.
   - One naming-transform line covering **only the surfaces present in the
     row** (code identifier, file name, CLI flag, env var). Never invent a
     transform the termbase doesn't declare — an invented `extendMode` that the
     codebase actually spells `extend_mode` would manufacture violations.
   - A source citation (termbase row number and term_id) as an HTML comment.
3. Include non-approved terms only in a short trailing "Pending terms" note, so
   readers know they exist but are not binding.
4. If asked (or if the user is about to draft a spec), also emit the **compact
   spec preamble**: the template's second section — one line per term — meant
   for pasting at the top of a spec or proposal.

## Mode 2: Enforce

Goal: flag term-usage drift in a draft spec, proposal, or tasks file — with
suggestions, quoting the offending lines.

1. Run:
   ```bash
   python scripts/check_terms.py --termbase <termbase.csv> --mode check <files-or-dirs>
   ```
   The script does the mechanical work deterministically: case-insensitive,
   word-boundary-aware matching of banned variants in both prose and code
   shapes (`extension mode` *and* `extensionMode`, `extension-mode`, ...), plus
   `surface_mismatch` findings when a canonical term's code/file/flag/env form
   appears in running prose (e.g. `extend-mode` outside backticks). Matches
   inside code fences and inline backticks are marked `context: "code"`;
   canonical surface forms in code context are correct and not reported.
2. Interpret the JSON — this is where your judgement comes in:
   - Drop false positives (e.g. a "variant" that is actually part of a proper
     noun, a quoted example of what *not* to do, or a heading naming the old
     term deliberately).
   - For `surface_mismatch` findings, decide whether the right fix is the prose
     form or wrapping the token in backticks (if the sentence genuinely refers
     to the identifier).
3. Write the report: one finding per line-occurrence with **file, line, the
   quoted offending line, the variant found, the canonical term, and a
   suggested rewrite of the sentence**. Group by term. End with a one-line
   count summary and which terms were skipped as non-approved.
4. **Zero findings must be said out loud** — "Checked N files against M
   approved terms: no violations found." Silence reads as a skipped check, not
   a clean one.

## Mode 3: Round-trip

Goal: after an implementation, surface recurring domain terms that are NOT in
the termbase as candidates for the next revision.

1. Run:
   ```bash
   python scripts/check_terms.py --termbase <termbase.csv> --mode candidates <files-or-dirs>
   ```
   The script only shortlists *frequent unknown word sequences* (from prose
   n-grams and split camelCase/snake_case identifiers, default min-count 3). It
   has no idea what a domain term is — that judgement is yours.
2. Filter the shortlist: keep phrases that name a concept in this system's
   domain (an entity, mode, policy, artifact); discard generic engineering
   vocabulary ("unit test", "error message"), phrase fragments, and incidental
   collocations. When in doubt about a borderline phrase, include it flagged as
   low-confidence rather than dropping it silently.
3. Propose each surviving candidate with: phrase, occurrence count, surfaces
   seen (prose / identifier spellings), 2–3 example locations (file:line with
   the quoted line), and a suggested definition inferred from usage.
4. State explicitly that **nothing was written to the termbase** and that these
   are proposals for human review. Suggest the user add approved ones with
   status `candidate` first if their process stages adoption. If it is empty
   say that too — "no recurring unknown terms found" is a result.
5. Also worth reporting when you see it: a shortlisted phrase that looks like a
   *near-synonym of an existing term* (e.g. `schema pinning` vs an existing
   `schema locking`) — call that out as possible drift rather than a fresh
   candidate.

## Bundled files

- `scripts/check_terms.py` — deterministic scanner; all modes start here.
  Run `--help` for flags (`--min-count`, `--max-examples`).
- `references/openspec-workflow.md` — read when you need to explain where each
  mode fits in a proposal → spec → tasks → implementation workflow, or which
  mode applies at the user's current stage.
- `assets/agents-md-template.md` — the output template for render mode; read it
  before writing the fragment.
