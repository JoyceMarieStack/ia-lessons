#!/usr/bin/env python3
"""Programmatic grading for vocabulary-contract iteration runs.

Checks each eval's mechanical assertions against the produced files and writes
grading.json (fields: text/passed/evidence) into each run directory.
"""
import json
import os
import re
import subprocess
import sys

BASE = "/home/user/ia-lessons/vocabulary-contract-workspace"
IT = os.path.join(BASE, sys.argv[1] if len(sys.argv) > 1 else "iteration-1")


def read(evaldir, name):
    p = os.path.join(IT, evaldir, "with_skill", "outputs", name)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return f.read()


def grade(evaldir, expectations):
    out = {"expectations": [{"text": t, "passed": bool(p), "evidence": e}
                            for t, p, e in expectations]}
    out["passed"] = all(x["passed"] for x in out["expectations"])
    d = os.path.join(IT, evaldir, "with_skill")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "grading.json"), "w") as f:
        json.dump(out, f, indent=2)
    n = sum(1 for x in out["expectations"] if x["passed"])
    print(f"{evaldir}: {n}/{len(out['expectations'])} passed")
    for x in out["expectations"]:
        if not x["passed"]:
            print(f"  FAIL: {x['text']} — {x['evidence']}")


def count_findings_sections(text):
    """Count distinct findings in a findings report: prefer explicit
    'Finding N' / numbered-list detection, fall back to counting quoted
    variant occurrences."""
    m = re.findall(r"(?im)^#+\s*finding\b|^\s*\d+\.\s", text)
    return len(m)


# --- eval 0: render ---------------------------------------------------------
frag = read("render-agents-fragment", "agents-fragment.md") or ""
pre = read("render-agents-fragment", "spec-preamble.md") or ""
both = frag + "\n" + pre
terms8 = ["extend mode", "project-local schema", "config.yaml",
          "schema registry", "merge policy", "validation pass",
          "spec preamble", "draft proposal"]
missing = [t for t in terms8 if t.lower() not in frag.lower()]
declared = ["extendMode", "extend-mode", "--extend-mode", "EXTEND_MODE",
            "projectLocalSchema", "SchemaRegistry", "mergePolicy"]
missing_forms = [d for d in declared if d not in frag]
invented = [s for s in ["validationPass", "specPreamble", "validation_pass",
                        "spec_preamble", "validation-pass", "spec-preamble"]
            if s in both]
# table = a markdown table row used for term entries
table_rows = re.findall(r"(?m)^\s*\|.*\|\s*$", frag)
cites = re.findall(r"(?i)source:.*row\s*\d+", frag)
never = re.search(r"(?is)never write.{0,40}extension\s+mode", frag)
pending = re.search(r"(?i)(pending|not yet binding|candidate)", frag)
grade("render-agents-fragment", [
    ("All 8 termbase terms appear in the fragment",
     frag and not missing, f"missing: {missing}" if missing else "all present"),
    ("Entries are imperative prose, not a markdown table",
     frag and not table_rows, f"{len(table_rows)} table rows found" if table_rows else "no table rows"),
    ("Declared transforms present (extendMode, extend-mode, --extend-mode, EXTEND_MODE, projectLocalSchema, SchemaRegistry, mergePolicy)",
     frag and not missing_forms, f"missing: {missing_forms}" if missing_forms else "all present"),
    ("No invented transforms for validation pass / spec preamble",
     frag and not invented, f"invented forms found: {invented}" if invented else "none found"),
    ("Banned variants stated as prohibitions",
     bool(never), never.group(0)[:80] if never else "no 'Never write ... extension mode' sentence"),
    ("draft proposal (candidate) marked pending/non-binding",
     bool(pending) and "draft proposal" in frag.lower(),
     (pending.group(0) if pending else "no pending marker")),
    ("Every entry carries a source row citation",
     len(cites) >= 7, f"{len(cites)} citations found"),
])

# --- eval 1: enforce (3 findings) ------------------------------------------
rep = read("enforce-three-findings", "findings.md") or ""
ext_flagged = len(re.findall(r"(?i)extension mode", rep))
lines_ok = all(re.search(rf"(?i)line\s*{n}\b|:{n}\b", rep) for n in (5, 12, 14))
lso = re.search(r"(?i)local schema override", rep)
cfg_flagged = re.search(r"(?i)config\.ya?ml.*(flag|violat|replace|instead)", rep)
pd_flagged = re.search(r"(?i)proposal draft.*(flag|violat|replace|instead)", rep)
three = re.search(r"(?i)\b(3|three)\b.*(finding|violation|issue)", rep) or \
        count_findings_sections(rep) == 3
quotes = ext_flagged >= 2 and bool(lso)
grade("enforce-three-findings", [
    ("Report contains exactly 3 findings",
     bool(three), "explicit count of 3 or 3 finding sections detected" if three else f"finding sections counted: {count_findings_sections(rep)}"),
    ("Both 'extension mode' occurrences flagged -> extend mode, lines 5 and 14",
     ext_flagged >= 2 and "extend mode" in rep.lower(), f"'extension mode' mentioned {ext_flagged}x"),
    ("'local schema override' flagged -> project-local schema, line 12",
     bool(lso) and "project-local schema" in rep.lower(), "present" if lso else "not mentioned"),
    ("Line numbers 5, 12, 14 all referenced",
     lines_ok, "all present" if lines_ok else "some line refs missing"),
    ("config.yaml NOT flagged as a violation",
     not cfg_flagged, cfg_flagged.group(0)[:80] if cfg_flagged else "not flagged"),
    ("'proposal draft' NOT flagged (candidate status)",
     not pd_flagged, pd_flagged.group(0)[:80] if pd_flagged else "not flagged"),
    ("Findings quote the offending lines",
     quotes, "variant text quoted" if quotes else "offending text not quoted"),
])

# --- eval 2: edge case ------------------------------------------------------
rep = read("enforce-surface-edge-case", "findings.md") or ""
kebab_flag = re.search(r"(?i)extend-mode", rep) and re.search(r"(?i)(surface|prose|kebab|file form|wrong form)", rep)
code_ok = not re.search(r"(?im)^.*extendMode.*(violat|flag(?!ged as correct)|must change|incorrect).*$", rep) or \
          re.search(r"(?i)extendMode.*(correct|not flagged|passes|fine|ok)", rep)
flag_ok = not re.search(r"(?i)--extend-mode.*(violat|incorrect|wrong)", rep)
one = re.search(r"(?i)\b(1|one)\b.*(finding|violation|issue)", rep) or count_findings_sections(rep) == 1
line5 = re.search(r"(?i)line\s*5\b|:5\b", rep)
grade("enforce-surface-edge-case", [
    ("prose 'extend-mode' flagged as wrong surface form",
     bool(kebab_flag), "flagged with surface/prose framing" if kebab_flag else "not flagged as surface issue"),
    ("extendMode in code block NOT flagged as violation",
     bool(code_ok), "code usage treated as correct"),
    ("`--extend-mode` inline code NOT flagged",
     bool(flag_ok), "not flagged" if flag_ok else "flagged"),
    ("Exactly 1 finding, with line 5 reference",
     bool(one) and bool(line5), f"one={bool(one)}, line5={bool(line5)}"),
])

# --- eval 3: roundtrip ------------------------------------------------------
rep = read("roundtrip-candidates", "candidates.md") or ""
sp = re.search(r"(?i)schema pinning", rep)
cnt = re.search(r"(?i)(schema pinning.{0,120}?\b([4-9]|\d{2})\b)|(\b([4-9]|\d{2})\b.{0,120}schema pinning)", rep, re.S)
locs = len(re.findall(r"(?i)(pinning\.py|docs\.md|cli\.md)[^\n]*?(:|line\s*)\d+", rep))
oneoffs = [w for w in ("rollback window", "audit trail")
           if re.search(rf"(?i)^.*{w}.*$", rep, re.M) and
              re.search(rf"(?i)propose[^\n]*{w}|{w}[^\n]*candidate\b(?![^\n]*not)", rep)]
nowrote = re.search(r"(?i)(not(hing)?\s+(been\s+)?(written|added|modif)|termbase (was|is) (unchanged|not modified)|no changes .*termbase)", rep)
md5_ok = subprocess.run(["md5sum", "-c", os.path.join(BASE, "termbase.md5")],
                        capture_output=True, cwd="/home/user/ia-lessons").returncode == 0
grade("roundtrip-candidates", [
    ("'schema pinning' proposed as candidate",
     bool(sp), "present" if sp else "absent"),
    ("Occurrence count >=4 and >=2 file:line locations given",
     bool(cnt) and locs >= 2, f"count-near-phrase={bool(cnt)}, locations={locs}"),
    ("One-off nouns not proposed as candidates",
     not oneoffs, f"proposed one-offs: {oneoffs}" if oneoffs else "none proposed"),
    ("Explicitly states nothing written to termbase",
     bool(nowrote), nowrote.group(0)[:80] if nowrote else "no such statement"),
    ("termbase.csv byte-identical after run",
     md5_ok, "md5 matches" if md5_ok else "md5 CHANGED"),
])

# --- eval 4: clean pass -----------------------------------------------------
rep = read("clean-pass", "findings.md") or ""
zero = re.search(r"(?i)(no (terminology )?(violation|finding|issue)|zero (finding|violation)|0 (finding|violation)|clean)", rep)
scope = re.search(r"(?i)(clean/spec\.md|spec\.md)", rep) and re.search(r"(?i)(approved term|7 |seven )", rep)
grade("clean-pass", [
    ("Explicit zero-findings statement",
     bool(zero), zero.group(0)[:60] if zero else "no explicit clean statement"),
    ("Says what was checked (file and approved terms)",
     bool(scope), "scope stated" if scope else "scope not stated"),
    ("findings.md non-empty",
     len(rep.strip()) > 50, f"{len(rep)} chars"),
])
print("done")
