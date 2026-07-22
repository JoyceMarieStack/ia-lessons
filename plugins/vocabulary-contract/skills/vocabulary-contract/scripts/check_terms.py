#!/usr/bin/env python3
"""Deterministic term scanner for the vocabulary-contract skill.

Modes:
  load        Parse and normalize a termbase.csv. Prints the normalized terms
              and the column mapping that was applied, so the model can render
              views and note any header adaptation.
  check       Scan files/directories for banned variants (prose AND code-form,
              e.g. "extension mode" and extensionMode) and for wrong-surface
              usages of canonical terms (e.g. the kebab file form appearing in
              running prose). Emits JSON findings with file/line/context.
  candidates  Shortlist recurring word sequences NOT in the termbase
              (round-trip mode). Purely mechanical frequency shortlisting —
              the model decides which entries are genuine domain terms.

Output is always JSON on stdout. Exit code is 0 even when findings exist:
enforcement is advisory, and the model writes the human-readable report.

Usage:
  python check_terms.py --termbase termbase.csv --mode load
  python check_terms.py --termbase termbase.csv --mode check spec.md docs/
  python check_terms.py --termbase termbase.csv --mode candidates src/ --min-count 3
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict

# ---------------------------------------------------------------------------
# Termbase loading (tolerant of alternate column names)
# ---------------------------------------------------------------------------

COLUMN_ALIASES = {
    "term": ["term", "preferred_term", "canonical_term", "canonical", "preferred"],
    "variants": ["variants", "forbidden_variants", "banned_variants", "avoid",
                 "deprecated_variants", "synonyms"],
    "code_identifier": ["code_identifier", "code_form", "identifier"],
    "file_form": ["file_form", "file_name", "filename_form", "filename"],
    "cli_flag": ["cli_flag", "flag_form", "cli_form"],
    "env_var": ["env_var", "environment_variable", "env_form"],
    "definition": ["definition", "meaning", "gloss"],
    "status": ["status"],
    "term_id": ["term_id", "id"],
}

# statuses treated as enforceable; anything else (candidate, provisional,
# needs stakeholder input, ...) is loaded but not enforced
APPROVED_STATUSES = {"", "approved"}

PROSE_EXTS = {".md", ".markdown", ".txt", ".rst", ".adoc"}
CODE_EXTS = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".java", ".rb", ".rs",
             ".c", ".h", ".cpp", ".hpp", ".cs", ".sh", ".bash", ".yaml", ".yml",
             ".json", ".toml", ".ini", ".sql", ".proto"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}


def map_columns(fieldnames):
    """Map actual CSV headers to canonical keys. Returns (mapping, unmapped)."""
    lower = {(f or "").strip().lower(): f for f in fieldnames}
    mapping, used = {}, set()
    for key, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in lower and lower[alias] not in used:
                mapping[key] = lower[alias]
                used.add(lower[alias])
                break
    unmapped = [f for f in fieldnames if f and f not in used]
    return mapping, unmapped


def parse_variants(raw):
    """Split a variants cell on ';' or '|'; drop empties, 'none...' notes,
    and trailing parenthetical annotations like 'timezone (bare, when ...)'."""
    out = []
    for part in re.split(r"[;|]", raw or ""):
        v = re.sub(r"\s*\([^)]*\)\s*$", "", part.strip()).strip()
        if not v or v.lower().startswith("none"):
            continue
        out.append(v)
    return out


def load_termbase(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        mapping, unmapped = map_columns(fieldnames)
        if "term" not in mapping:
            raise SystemExit(json.dumps({
                "error": "no term column found",
                "headers_seen": fieldnames,
                "accepted_aliases": COLUMN_ALIASES["term"],
            }))
        terms = []
        for i, row in enumerate(reader, start=2):  # row 1 is the header
            get = lambda key: (row.get(mapping[key], "") or "").strip() if key in mapping else ""
            term = get("term")
            if not term:
                continue
            status = get("status").lower()
            terms.append({
                "row": i,
                "term_id": get("term_id"),
                "term": term,
                "variants": parse_variants(get("variants")),
                "code_identifier": get("code_identifier"),
                "file_form": get("file_form"),
                "cli_flag": get("cli_flag"),
                "env_var": get("env_var"),
                "definition": get("definition"),
                "status": status,
                "enforced": status in APPROVED_STATUSES,
            })
    return {
        "path": path,
        "column_mapping": mapping,
        "unmapped_columns": unmapped,
        "terms": terms,
    }


# ---------------------------------------------------------------------------
# Phrase normalization and surface-form derivation
# ---------------------------------------------------------------------------

def phrase_words(s):
    """Lowercase word list from a prose phrase OR a code identifier."""
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", s.strip())  # split camel humps
    return [p.lower() for p in re.split(r"[\s_\-]+", s) if p]


def norm(s):
    return " ".join(phrase_words(s))


def derived_forms(phrase):
    """Code/file/flag/env surfaces derivable from a multi-word phrase.
    Single-word phrases (or literals like config.yaml) get no derived forms."""
    words = phrase_words(phrase)
    if len(words) < 2:
        return {}
    return {
        "camelCase": words[0] + "".join(w.capitalize() for w in words[1:]),
        "PascalCase": "".join(w.capitalize() for w in words),
        "snake_case": "_".join(words),
        "kebab-case": "-".join(words),
        "SCREAMING_SNAKE": "_".join(words).upper(),
    }


def form_pattern(form):
    """Regex for a surface form with sensible boundaries (kebab-aware)."""
    esc = re.escape(form)
    return re.compile(r"(?<![\w\-])" + esc + r"(?![\w\-])")


def prose_pattern(phrase):
    """Case-insensitive, word-boundary, whitespace-flexible prose match."""
    parts = [re.escape(w) for w in re.split(r"\s+", phrase.strip()) if w]
    return re.compile(r"\b" + r"\s+".join(parts) + r"\b", re.IGNORECASE)


# ---------------------------------------------------------------------------
# File collection and context (code vs prose) detection
# ---------------------------------------------------------------------------

def collect_files(paths, termbase_path):
    files = []
    tb_abs = os.path.abspath(termbase_path)
    for p in paths:
        if os.path.isfile(p):
            files.append(p)
        elif os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for name in sorted(names):
                    ext = os.path.splitext(name)[1].lower()
                    if ext in PROSE_EXTS or ext in CODE_EXTS:
                        files.append(os.path.join(root, name))
    return [f for f in files if os.path.abspath(f) != tb_abs]


FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def line_contexts(path):
    """Yield (lineno, text, in_fence, inline_spans) for each line."""
    ext = os.path.splitext(path)[1].lower()
    whole_file_code = ext in CODE_EXTS
    in_fence = False
    with open(path, encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, start=1):
            text = line.rstrip("\n")
            fence_line = bool(FENCE_RE.match(text)) and not whole_file_code
            if fence_line:
                in_fence = not in_fence
                continue  # the fence marker itself is not scannable content
            spans = [(m.start(), m.end()) for m in INLINE_CODE_RE.finditer(text)]
            yield lineno, text, whole_file_code or in_fence, spans


def context_at(pos, in_fence, inline_spans):
    if in_fence:
        return "code"
    for a, b in inline_spans:
        if a <= pos < b:
            return "code"
    return "prose"


# ---------------------------------------------------------------------------
# check mode
# ---------------------------------------------------------------------------

def build_matchers(terms):
    """For each enforced term build: canonical spans pattern, variant patterns,
    and canonical-surface-form patterns (for wrong-surface detection)."""
    matchers = []
    for t in terms:
        if not t["enforced"]:
            continue
        canon_norm = norm(t["term"])
        variant_pats = []  # (compiled, matched_text_label, form_name)
        for v in t["variants"]:
            if norm(v) == canon_norm:
                continue
            variant_pats.append((prose_pattern(v), v, "prose"))
            for form_name, form in derived_forms(v).items():
                variant_pats.append((form_pattern(form), form, form_name))
        surface_pats = []  # canonical term's non-prose surfaces
        declared = [d for d in (t["code_identifier"], t["file_form"],
                                t["env_var"], t["cli_flag"],
                                t["cli_flag"].lstrip("-") if t["cli_flag"] else "")
                    if d]
        seen = set()
        for form_name, form in (list(derived_forms(t["term"]).items())
                                + [("declared", d) for d in declared]):
            # the term's own prose spelling is not a wrong surface
            if form.lower() == t["term"].lower() or form in seen:
                continue
            seen.add(form)
            surface_pats.append((form_pattern(form), form, form_name))
        matchers.append({
            "term": t,
            "canonical_pat": prose_pattern(t["term"]),
            "variant_pats": variant_pats,
            "surface_pats": surface_pats,
        })
    return matchers


def code_suggestion(t):
    return t["code_identifier"] or derived_forms(t["term"]).get("camelCase", t["term"])


def run_check(tb, paths):
    matchers = build_matchers(tb["terms"])
    files = collect_files(paths, tb["path"])
    findings = []
    for path in files:
        for lineno, text, in_fence, inline_spans in line_contexts(path):
            # spans where any canonical prose term occurs — matches inside
            # these are correct usage, never variant hits (e.g. "local schema"
            # inside "project-local schema")
            canon_spans = []
            for m in matchers:
                for hit in m["canonical_pat"].finditer(text):
                    canon_spans.append((hit.start(), hit.end()))
            line_hits = []
            for m in matchers:
                t = m["term"]
                for pat, label, form_name in m["variant_pats"]:
                    for hit in pat.finditer(text):
                        if any(a <= hit.start() and hit.end() <= b
                               for a, b in canon_spans):
                            continue
                        ctx = context_at(hit.start(), in_fence, inline_spans)
                        line_hits.append({
                            "type": "banned_variant",
                            "file": path, "line": lineno,
                            "col": hit.start() + 1,
                            "span": (hit.start(), hit.end()),
                            "matched_text": text[hit.start():hit.end()],
                            "matched_form": form_name,
                            "context": ctx,
                            "term": t["term"], "term_id": t["term_id"],
                            "termbase_row": t["row"],
                            "suggestion": t["term"] if ctx == "prose"
                                          else code_suggestion(t),
                            "line_text": text.strip(),
                        })
                for pat, label, form_name in m["surface_pats"]:
                    for hit in pat.finditer(text):
                        ctx = context_at(hit.start(), in_fence, inline_spans)
                        if ctx == "code":
                            continue  # canonical surface form in code is correct
                        line_hits.append({
                            "type": "surface_mismatch",
                            "file": path, "line": lineno,
                            "col": hit.start() + 1,
                            "span": (hit.start(), hit.end()),
                            "matched_text": text[hit.start():hit.end()],
                            "matched_form": form_name,
                            "context": ctx,
                            "term": t["term"], "term_id": t["term_id"],
                            "termbase_row": t["row"],
                            "suggestion": t["term"],
                            "line_text": text.strip(),
                        })
            # keep longest match when hits overlap (e.g. "local schema" inside
            # "local schema override"); then drop helper span field
            line_hits.sort(key=lambda h: (h["span"][0] - h["span"][1],
                                          h["span"][0]))
            kept = []
            for h in line_hits:
                if any(k["span"][0] <= h["span"][0] and
                       h["span"][1] <= k["span"][1] for k in kept):
                    continue
                kept.append(h)
            for h in sorted(kept, key=lambda h: h["span"][0]):
                del h["span"]
                findings.append(h)
    by_term = defaultdict(int)
    for f in findings:
        by_term[f["term"]] += 1
    return {
        "mode": "check",
        "termbase": termbase_summary(tb),
        "files_scanned": files,
        "findings": findings,
        "summary": {"total_findings": len(findings), "by_term": dict(by_term)},
    }


# ---------------------------------------------------------------------------
# candidates mode (round-trip)
# ---------------------------------------------------------------------------

STOPWORDS = set("""
a an and are as at be been but by can could did do does for from had has have
how if in into is it its may might must not of on or our shall should so than
that the their then there these they this those to use used uses using was we
were what when where which while will with would you your all any each every
more most new no other same some such only over under after before between
""".split())

IDENT_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9_]*\b")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z']*")


def known_phrases(tb):
    """Every normalized phrase already in the termbase, any status."""
    known = set()
    for t in tb["terms"]:
        pool = [t["term"]] + t["variants"] + [t["code_identifier"],
                t["file_form"], t["cli_flag"], t["env_var"]]
        for p in pool:
            if p:
                known.add(norm(p))
                for form in derived_forms(p).values():
                    known.add(norm(form))
    return known


def run_candidates(tb, paths, min_count, max_examples):
    known = known_phrases(tb)
    files = collect_files(paths, tb["path"])
    counts = defaultdict(int)
    examples = defaultdict(list)
    forms_seen = defaultdict(set)

    def record(phrase, path, lineno, text, surface):
        counts[phrase] += 1
        forms_seen[phrase].add(surface)
        if len(examples[phrase]) < max_examples:
            examples[phrase].append({"file": path, "line": lineno,
                                     "line_text": text.strip()[:160]})

    for path in files:
        for lineno, text, in_fence, inline_spans in line_contexts(path):
            # multi-word identifiers (camelCase / snake_case) -> phrases
            for m in IDENT_RE.finditer(text):
                tok = m.group(0)
                words = phrase_words(tok)
                if len(words) < 2 or any(len(w) < 3 for w in words):
                    continue
                phrase = " ".join(words)
                if phrase in known or all(w in STOPWORDS for w in words):
                    continue
                record(phrase, path, lineno, text, tok)
            # prose n-grams (bigrams and trigrams)
            words = [w.lower() for w in WORD_RE.findall(text)]
            for n in (2, 3):
                for i in range(len(words) - n + 1):
                    gram = words[i:i + n]
                    if gram[0] in STOPWORDS or gram[-1] in STOPWORDS:
                        continue
                    if any(len(w) < 3 for w in gram):
                        continue
                    phrase = " ".join(gram)
                    if phrase in known:
                        continue
                    record(phrase, path, lineno, text, "prose")

    # drop a shorter phrase fully contained in a longer one with the same count
    shortlisted = {p: c for p, c in counts.items() if c >= min_count}
    for p in list(shortlisted):
        for q in shortlisted:
            if p != q and p in q and counts[p] <= counts[q]:
                shortlisted.pop(p)
                break
    ranked = sorted(shortlisted.items(), key=lambda kv: (-kv[1], kv[0]))[:40]
    return {
        "mode": "candidates",
        "termbase": termbase_summary(tb),
        "files_scanned": files,
        "min_count": min_count,
        "note": ("Mechanical frequency shortlist only. The model must judge "
                 "which entries are genuine domain terms and discard generic "
                 "phrases. Nothing has been written to the termbase."),
        "candidates": [{
            "phrase": p,
            "count": c,
            "surfaces_seen": sorted(forms_seen[p]),
            "examples": examples[p],
        } for p, c in ranked],
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def termbase_summary(tb):
    return {
        "path": tb["path"],
        "column_mapping": tb["column_mapping"],
        "unmapped_columns": tb["unmapped_columns"],
        "terms_total": len(tb["terms"]),
        "terms_enforced": sum(1 for t in tb["terms"] if t["enforced"]),
        "terms_not_enforced": [{"term": t["term"], "status": t["status"]}
                               for t in tb["terms"] if not t["enforced"]],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--termbase", required=True)
    ap.add_argument("--mode", choices=["load", "check", "candidates"],
                    default="check")
    ap.add_argument("paths", nargs="*", help="files or directories to scan")
    ap.add_argument("--min-count", type=int, default=3,
                    help="candidates mode: minimum occurrences to shortlist")
    ap.add_argument("--max-examples", type=int, default=5)
    args = ap.parse_args()

    tb = load_termbase(args.termbase)
    if args.mode == "load":
        out = {"mode": "load", "termbase": termbase_summary(tb),
               "terms": tb["terms"]}
    elif args.mode == "check":
        if not args.paths:
            ap.error("check mode requires at least one file or directory")
        out = run_check(tb, args.paths)
    else:
        if not args.paths:
            ap.error("candidates mode requires at least one file or directory")
        out = run_candidates(tb, args.paths, args.min_count, args.max_examples)
    json.dump(out, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
