#!/usr/bin/env python3
"""
build_diagram.py

Renders a stem-and-leaf terminology diagram from structured JSON. Claude
does the judgment work (clustering terms into concept "stems" and
classifying each term+source "card" as unambiguous / correct-in-context /
ambiguous / conflict); this script does the mechanical work of frequency
bars and fixed-width column alignment, which is fiddly to get right by eye
and easy to get right in code.

Input JSON schema:
{
  "topic": "Deployment Terminology",
  "sections": [
    {
      "name": "TECHNICAL MODEL",
      "stems": [
        {
          "stem": "access token",
          "description": "short-lived API auth credential",
          "cards": [
            {"symbol": "unambiguous", "term": "access token", "source": "auth-guide.md", "count": 12},
            {"symbol": "conflict", "term": "auth token", "source": "api-ref.md", "count": 8}
          ]
        }
      ]
    }
  ],
  "conflict_callout": "One-sentence description of the worst ✕ conflict and why it matters operationally.",
  "best_practice": "Which source uses terms most precisely, and why."
}

symbol values (long form, mapped to glyphs below): "unambiguous" -> ●,
"correct_in_context" -> ○, "ambiguous" -> △, "conflict" -> ✕

Usage:
    python3 build_diagram.py input.json output.md
"""

import sys
import json

SYMBOLS = {
    "unambiguous": "\u25cf",          # ●
    "correct_in_context": "\u25cb",   # ○
    "ambiguous": "\u25b3",            # △
    "conflict": "\u2715",             # ✕
}

STEM_COL = 20
TERM_COL = 24
SOURCE_COL = 32
BAR_WIDTH = 8
RULE_WIDTH = 72


def resolve_symbol(s):
    if s in SYMBOLS:
        return SYMBOLS[s]
    if s in SYMBOLS.values():
        return s
    raise ValueError(f"Unknown symbol: {s!r} (use one of {list(SYMBOLS)})")


def bar(count, max_count):
    if count is None:
        return None
    if max_count <= 0:
        filled = 0
    else:
        filled = max(1, round((count / max_count) * BAR_WIDTH)) if count > 0 else 0
    filled = min(filled, BAR_WIDTH)
    return "\u2588" * filled + "\u2591" * (BAR_WIDTH - filled)


def pad(s, width):
    s = str(s)
    if len(s) > width:
        return s[: width - 1] + "\u2026" if width > 1 else s[:width]
    return s + " " * (width - len(s))


def wrap_desc(desc, width):
    """Greedy word-wrap a description into lines that fit `width` chars."""
    words = desc.split()
    lines, cur = [], ""
    for w in words:
        candidate = (cur + " " + w).strip()
        if len(candidate) > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = candidate
    if cur:
        lines.append(cur)
    return lines or [""]


def render(data):
    all_counts = [
        c.get("count") for section in data.get("sections", [])
        for stem in section.get("stems", [])
        for c in stem.get("cards", [])
        if c.get("count") is not None
    ]
    max_count = max(all_counts) if all_counts else 0

    topic = data.get("topic", "Terminology Audit")
    lines = []
    lines.append(f"# Stem & Leaf \u2014 {topic}")
    lines.append("Each card = one source using that term.")
    lines.append(
        f"{SYMBOLS['unambiguous']} unambiguous  {SYMBOLS['correct_in_context']} correct-in-context  "
        f"{SYMBOLS['ambiguous']} ambiguous  {SYMBOLS['conflict']} conflict"
    )
    lines.append("")

    rule = "\u2550" * RULE_WIDTH
    thin_rule = "\u2500" * RULE_WIDTH

    for section in data.get("sections", []):
        lines.append(rule)
        lines.append(section.get("name", "").upper())
        lines.append(rule)
        lines.append("")

        stems = section.get("stems", [])
        for si, stem in enumerate(stems):
            stem_label_lines = wrap_desc(
                f"{stem['stem']}", STEM_COL
            )
            desc_lines = wrap_desc(f"({stem.get('description', '')})", STEM_COL) if stem.get("description") else []
            left_lines = stem_label_lines + desc_lines

            cards = stem.get("cards", [])
            card_lines = []
            for card in cards:
                glyph = resolve_symbol(card["symbol"])
                flagged = card["symbol"] in ("ambiguous", "conflict", SYMBOLS["ambiguous"], SYMBOLS["conflict"])
                term_display = f"{card['term']} \u25b3" if flagged else card["term"]
                term_field = f"{glyph} {term_display}"
                source = card.get("source", "")
                count = card.get("count")
                b = bar(count, max_count)
                tail = f"{b}  {count}\u00d7" if b is not None else ""
                card_lines.append(
                    f"{pad(term_field, TERM_COL)}{pad(source, SOURCE_COL)}{tail}"
                )

            n_rows = max(len(left_lines), len(card_lines), 1)
            for i in range(n_rows):
                left = pad(left_lines[i], STEM_COL) if i < len(left_lines) else pad("", STEM_COL)
                right = card_lines[i] if i < len(card_lines) else ""
                lines.append(f"{left}\u2502 {right}".rstrip())
            lines.append("")

            if si < len(stems) - 1:
                lines.append(thin_rule)
                lines.append("")

        lines.append("")

    lines.append(rule)
    lines.append("LEGEND")
    lines.append(rule)
    lines.append(f"{SYMBOLS['unambiguous']} Clearly scoped \u2014 unambiguous, correct for context")
    lines.append(f"{SYMBOLS['correct_in_context']} Technically correct but narrower than the stem")
    lines.append(f"{SYMBOLS['ambiguous']} Ambiguous or inconsistent use")
    lines.append(f"{SYMBOLS['conflict']} Conflict \u2014 same word, incompatible meaning across sources")
    lines.append("")

    if data.get("conflict_callout"):
        lines.append(rule)
        lines.append("\u26a0  THE CONFLICT THAT MATTERS MOST")
        lines.append(rule)
        lines.append(data["conflict_callout"])
        lines.append("")

    if data.get("best_practice"):
        lines.append("THE BEST EXISTING PRACTICE")
        lines.append(data["best_practice"])
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 build_diagram.py input.json output.md", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Wrote diagram to {sys.argv[2]}")
