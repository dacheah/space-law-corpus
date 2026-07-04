#!/usr/bin/env python3
"""
diff_passes.py -- compare two independent concept-tagging passes and emit the
adjudication queue (dual-pass review method; see CHANGELOG 2026-07-04).

Reads  reviews/concept-passes/pass-A.json / pass-B.json
Writes reviews/concept-review-queue.md and .json, prints agreement stats.

Unit labels are normalised ("Principle 7" == "Paragraph 7"; "Art. 2" == "Article 2")
so passes that used different unit-naming conventions still align. A pass entry
whose label contains "(whole instrument)" or "(whole text)" is document-level: it
cannot be unit-aligned and is queued as a granularity decision.
"""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASSES = os.path.join(ROOT, "reviews", "concept-passes")

def norm(label):
    s = label.strip().lower()
    if "whole" in s: return "@doc"
    s = re.sub(r"^(article|art\.?|principle|paragraph|guideline|§)\s*", "", s)
    tok = s.split()[0] if s.split() else s
    tok = tok.rstrip(".").replace("er", "") if re.match(r"\d+er$", tok) else tok.rstrip(".")
    return re.sub(r"[^a-z0-9.\-]", "", tok)

def load(p):
    d = json.load(open(os.path.join(PASSES, p), encoding="utf-8"))
    return d["_provenance"], {cid: {norm(u): (u, set(cs)) for u, cs in units.items()}
                              for cid, units in d["tags"].items()}

provA, A = load("pass-A.json")
provB, B = load("pass-B.json")
queue, agree, total = [], 0, 0
for cid in sorted(set(A) | set(B)):
    a, b = A.get(cid, {}), B.get(cid, {})
    if "@doc" in a and "@doc" not in b:
        queue.append({"corpus_id": cid, "unit": "(granularity)", "kind": "granularity",
                      "pass_a": sorted(a["@doc"][1]), "pass_b": "per-unit tags (see pass-B.json)",
                      "note": "Pass A tagged the whole instrument; pass B tagged per unit."})
        for k, (lbl, cs) in sorted(b.items()):
            total += 1
        continue
    for k in sorted(set(a) | set(b)):
        la, ca = a.get(k, (None, set()))
        lb, cb = b.get(k, (None, set()))
        total += 1
        if ca == cb:
            agree += 1
        else:
            queue.append({"corpus_id": cid, "unit": lb or la, "kind": "tags",
                          "pass_a": sorted(ca) if la else "(untagged by A)",
                          "pass_b": sorted(cb) if lb else "(untagged by B)",
                          "only_a": sorted(ca - cb), "only_b": sorted(cb - ca)})
print(f"units compared: {total}  agreements: {agree}  disagreements: {len(queue)}  "
      f"agreement rate: {agree/max(total,1):.1%}")
json.dump({"provenance": {"pass_a": provA, "pass_b": provB},
           "units_compared": total, "agreements": agree, "queue": queue},
          open(os.path.join(ROOT, "reviews", "concept-review-queue.json"), "w"), indent=1)
with open(os.path.join(ROOT, "reviews", "concept-review-queue.md"), "w", encoding="utf-8") as f:
    f.write("# Concept-tag adjudication queue (dual-pass)\n\n")
    f.write(f"Units compared: {total} — agreement {agree} ({agree/max(total,1):.1%}). ")
    f.write("Each row below is a disagreement between two independent model passes; a human "
            "ruling resolves it (record rulings in reviews/concept-decisions-<date>.yaml).\n\n")
    f.write("| # | Instrument | Unit | Pass A | Pass B |\n|---|---|---|---|---|\n")
    for i, q in enumerate(queue, 1):
        f.write(f"| {i} | {q['corpus_id']} | {q['unit']} | {q['pass_a']} | {q['pass_b']} |\n")
print("queue written -> reviews/concept-review-queue.md")
