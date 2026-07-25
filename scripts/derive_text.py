#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""derive_text.py — reproduce each authoritative text.txt BYTE-EXACTLY from its stored original.

WHY THIS EXISTS. This corpus's reproducibility claim was weaker than the other four: extract.py
measures >=97% contiguous TOKEN OVERLAP between a fresh extraction and the stored text, not byte
equality. Measured 2026-07-22, the gap is not sloppiness — the stored texts are MORE faithful to the
official document than the raw extraction is. A human repaired real extraction defects:

    'extra- atmosphérique'  -> 'extra-atmosphérique'   (line-break hyphenation rejoined)
    '*Reaffirming*'         -> 'Reaffirming'           (markdown emphasis from the capture)
    'redevance '      -> 'redevance.'            (broken private-use glyph in the source PDF)
    ''                      -> 'Étienne Schneider'     (signatory absent from the PDF text layer)

Those repairs are correct and must be kept. But while they live only in the stored bytes they are
INVISIBLE: nothing records that a human changed anything, or why. This module makes the derivation
explicit and auditable, so byte equality and honesty are the same act:

    text.txt  ==  extract -> slice -> reflow -> mechanical rules -> recorded corrections

Every stage is deterministic and declared per record in corrections/<corpus_id>/<version_id>.json.
Nothing is hidden in a person's memory; every human edit carries a reason, a reviewer and a date.

    python3 scripts/derive_text.py            # verify every record with a corrections file
    python3 scripts/derive_text.py --selftest # offline checks of the pure transforms
"""
from __future__ import annotations
import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashing import normalize_text_bytes  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
AUTH = os.path.join(REPO, "authoritative")
CORR = os.path.join(REPO, "corrections")


# ---- stage 1: extraction ---------------------------------------------------------------------
def extract(orig_path: str, spec: dict) -> str:
    """Run the pinned extractor. 'passthrough' means the stored original IS text."""
    if spec.get("tool") == "passthrough":
        return open(orig_path, encoding="utf-8").read()
    args = spec.get("args", [])
    out = subprocess.run(["pdftotext"] + args + ["-enc", "UTF-8", orig_path, "-"],
                         capture_output=True)
    return out.stdout.decode("utf-8", "replace")


# ---- stage 2: slice --------------------------------------------------------------------------
def do_slice(text: str, sl) -> str:
    """Cut the instrument out of a larger document.

    UNOOSA pages reproduce the adopting GA resolution with the treaty as its ANNEX, and US Code
    pages carry a 'Source: U.S. Government Publishing Office' banner. Slicing is therefore normal
    and must be RECORDED — every extraction recipe in this repo currently says slice:null, which is
    factually wrong for those records.
    """
    if not sl:
        return text
    lines = text.split("\n")
    if "drop_leading_lines" in sl:
        lines = lines[int(sl["drop_leading_lines"]):]
    if "drop_trailing_lines" in sl:
        n = int(sl["drop_trailing_lines"])
        lines = lines[:-n] if n else lines
    text = "\n".join(lines)
    if sl.get("start_contains"):
        i = text.find(sl["start_contains"])
        if i >= 0:
            text = text[i:]
    if sl.get("end_contains"):
        j = text.find(sl["end_contains"])
        if j >= 0:
            text = text[:j + len(sl["end_contains"])]
    return text


# ---- stage 3: reflow -------------------------------------------------------------------------
def reflow(text: str, mode) -> str:
    """Undo the source's hard wrapping.

    A PDF extraction is wrapped at the page's column width; the stored texts join each paragraph
    onto one line (res-1962-XVIII stores 19 lines against 3980 extracted). Blank lines separate
    paragraphs, so joining within a block and keeping blank-line boundaries is deterministic.
    """
    if not mode or mode == "none":
        return text
    if mode != "paragraphs":
        raise ValueError(f"unknown reflow mode: {mode}")
    out, buf = [], []
    for line in text.split("\n"):
        if line.strip():
            buf.append(line.strip())
        else:
            if buf:
                out.append(" ".join(buf)); buf = []
            out.append("")
    if buf:
        out.append(" ".join(buf))
    return "\n".join(out)


# ---- stage 4: mechanical rules ---------------------------------------------------------------
def dehyphenate(t: str) -> str:
    """'extra- atmosphérique' -> 'extra-atmosphérique'. A hyphen followed by a space between two
    word characters is a line-break artifact, not real punctuation."""
    return re.sub(r"(\w)-\s+(\w)", r"\1-\2", t)


def strip_emphasis(t: str) -> str:
    """'*Reaffirming*' -> 'Reaffirming'. The HTML captures carried markdown emphasis."""
    return re.sub(r"\*([^*\n]+)\*", r"\1", t)


def collapse_spaces(t: str) -> str:
    """Collapse runs of spaces/tabs, but never touch newlines (line structure is meaningful)."""
    return re.sub(r"[ \t]{2,}", " ", t)


MECHANICAL = {"dehyphenate": dehyphenate, "strip_emphasis": strip_emphasis,
              "collapse_spaces": collapse_spaces}


def apply_mechanical(text: str, rules) -> str:
    for name in (rules or []):
        if name not in MECHANICAL:
            raise ValueError(f"unknown mechanical rule: {name}")
        text = MECHANICAL[name](text)
    return text


# ---- stage 5: recorded corrections -----------------------------------------------------------
def apply_corrections(text: str, corrections) -> str:
    """Apply each declared human repair, asserting the expected occurrence count.

    `count` is the guard: if the source document changes such that a correction no longer matches
    the expected number of times, this RAISES rather than silently producing different text. A
    correction that stops applying is a signal the original changed, not something to paper over.
    """
    for c in (corrections or []):
        op = c.get("op", "replace")
        if op == "replace":
            frm, to = c["from"], c["to"]
            n = text.count(frm)
            want = c.get("count", 1)
            if n != want:
                raise ValueError(f"correction expected {want} occurrence(s) of {frm!r}, found {n}"
                                 f" — the stored original may have changed; re-review before editing")
            text = text.replace(frm, to)
        elif op == "insert_after":
            anchor, ins = c["anchor"], c["text"]
            if text.count(anchor) != 1:
                raise ValueError(f"insert_after anchor {anchor!r} is not unique")
            text = text.replace(anchor, anchor + ins, 1)
        else:
            raise ValueError(f"unknown correction op: {op}")
    return text


# ---- pipeline --------------------------------------------------------------------------------
def derive(spec: dict, orig_path: str) -> bytes:
    t = extract(orig_path, spec["extractor"])
    t = do_slice(t, spec.get("slice"))
    t = reflow(t, spec.get("reflow"))
    t = apply_mechanical(t, spec.get("mechanical"))
    t = apply_corrections(t, spec.get("corrections"))
    return normalize_text_bytes(t)


def corr_path(cid: str, ver: str) -> str:
    return os.path.join(CORR, cid, ver + ".json")


def selftest() -> int:
    assert dehyphenate("extra- atmosphérique") == "extra-atmosphérique"
    assert dehyphenate("au- delà et (2007- 2008)") == "au-delà et (2007-2008)"
    # a real hyphen followed by punctuation/space-word boundary that ISN'T a break stays put
    assert dehyphenate("well-known") == "well-known"
    assert strip_emphasis("*Reaffirming* the treaty") == "Reaffirming the treaty"
    assert strip_emphasis("2 * 3 = 6") == "2 * 3 = 6", "a lone asterisk is not emphasis"
    assert collapse_spaces("a    b") == "a b"
    assert collapse_spaces("a\n\nb") == "a\n\nb", "newlines must survive"
    # a trailing newline in the input yields a trailing blank line; normalize_text_bytes settles
    # the final-newline convention at the end of the pipeline, so reflow must not second-guess it
    assert reflow("one\ntwo\n\nthree\n", "paragraphs") == "one two\n\nthree\n"
    assert reflow("one\ntwo\n\nthree", "paragraphs") == "one two\n\nthree"
    assert reflow("keep\nas is", None) == "keep\nas is"
    assert do_slice("a\nb\nc", {"drop_leading_lines": 1}) == "b\nc"
    assert do_slice("xxSTARTyy", {"start_contains": "START"}) == "STARTyy"
    # corrections: count guard must FAIL LOUDLY rather than silently produce different text
    assert apply_corrections("a b a", [{"from": "a", "to": "z", "count": 2}]) == "z b z"
    try:
        apply_corrections("a b a", [{"from": "a", "to": "z", "count": 1}])
        raise AssertionError("a wrong occurrence count MUST raise")
    except ValueError:
        pass
    print("derive_text selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    specs = sorted(glob.glob(os.path.join(CORR, "**", "*.json"), recursive=True))
    if not specs:
        print(f"No corrections files under {os.path.relpath(CORR, REPO)}/ yet.")
        print("Each record reaching byte equality declares one; see scripts/derive_text.py.")
        return 0
    ok = fail = 0
    for sp in specs:
        spec = json.load(open(sp, encoding="utf-8"))
        cid, ver = spec["corpus_id"], spec["version_id"]
        vd = os.path.join(AUTH, cid, ver)
        meta = yaml.safe_load(open(os.path.join(vd, "metadata.yaml"), encoding="utf-8"))
        orig = os.path.join(vd, meta["original_filename"])
        try:
            got = derive(spec, orig)
            h = "sha256:" + hashlib.sha256(got).hexdigest()
        except Exception as e:
            print(f"  ERROR      {cid}/{ver}: {type(e).__name__}: {e}")
            fail += 1
            continue
        if h == meta.get("text_sha256"):
            print(f"  BYTE-EXACT {cid}/{ver}")
            ok += 1
        else:
            print(f"  MISMATCH   {cid}/{ver}\n     recorded {meta.get('text_sha256')}\n     derived  {h}")
            fail += 1
    print(f"\n{ok}/{ok + fail} record(s) re-derive BYTE-EXACT from their stored original.")
    if fail:
        print("A mismatch means the declared pipeline no longer reproduces the stored text — "
              "investigate before changing either.")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
