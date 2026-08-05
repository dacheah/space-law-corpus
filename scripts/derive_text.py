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

    text.txt  ==  extract -> slice -> drop_lines -> pre -> reflow -> mechanical -> corrections

Every stage is deterministic and declared per record in corrections/<corpus_id>/<version_id>.json.
Nothing is hidden in a person's memory; every human edit carries a reason, a reviewer and a date.

    extract      the pinned extractor (pdftotext with recorded args, or passthrough)
    slice        cut ONE contiguous instrument out of a larger document
    drop_lines   delete interleaved page furniture slicing cannot reach (page numbers, footnotes)
    pre          line surgery that must happen BEFORE paragraphs are joined (form feeds, soft
                 hyphens, words broken across lines, restoring breaks before numbered items)
    reflow       undo the source's hard wrapping
    mechanical   named, general text rules (markdown artefacts, spacing)
    corrections  declared human repairs, each with a reason, reviewer, date and a count guard

The order is load-bearing. `pre` runs before `reflow` because joining paragraphs first would make a
word broken across lines indistinguishable from two words; `corrections` runs last so a repair is
written against the text a reader would actually see.

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


# ---- stage 2b: drop page furniture ------------------------------------------------------------
def drop_lines(text: str, rules) -> tuple:
    """Delete whole lines matching declared patterns. Returns (text, counts).

    WHY SLICING IS NOT ENOUGH. The UNOOSA compendia (ST/SPACE/61/Rev.3) print several instruments
    in one volume, and the page furniture is INTERLEAVED with the text — a page number on its own
    line, a form feed, a footnote line such as '7Adopted by the General Assembly in its resolution
    1962 (XVIII) of 13 December 1963.' sitting between two preambular paragraphs. `slice` cuts one
    contiguous range and cannot remove something from the middle.

    Every pattern carries a `_reason` in the recipe, and the count of lines each one removed is
    reported back, so a pattern that silently starts matching real text is visible rather than
    invisible. Patterns are anchored by the recipe author, not guessed here.
    """
    if not rules:
        return text, {}
    compiled = [(r["pattern"], re.compile(r["pattern"])) for r in rules]
    counts = {p: 0 for p, _ in compiled}
    out = []
    for line in text.split("\n"):
        for pat, rx in compiled:
            if rx.search(line):
                counts[pat] += 1
                break
        else:
            out.append(line)
    return "\n".join(out), counts


# ---- stage 2c: pre-reflow line surgery --------------------------------------------------------
def join_hyphenated_breaks(t: str) -> str:
    """'propa-\\nganda' -> 'propaganda'.

    Distinct from `dehyphenate`, and the difference matters. A typeset PDF breaks a word across
    lines with a hyphen that is NOT part of the word, so the hyphen must go. `dehyphenate` handles
    the opposite case — a real hyphen in a compound ('non- governmental') that a line break merely
    separated — and keeps it. Applying the wrong one turns 'propaganda' into 'propa-ganda'.
    """
    return re.sub(r"(\w)-\n(\w)", r"\1\2", t)


def strip_soft_hyphens(t: str) -> str:
    """Remove U+00AD SOFT HYPHEN together with any whitespace it introduced.

    The soft hyphen is an invisible typesetting hint marking where a word MAY break. It survives PDF
    extraction where the rendered hyphen does not, and -layout output often carries the break's
    whitespace with it: 'Earth S\\xad atellites' and 'inter\\xad national'. Removing only the U+00AD
    leaves 'S atellites' — a word split by a space, which is worse than the original defect because
    it looks like real text. So the character and the whitespace that followed it go together.
    """
    return re.sub("­[ \t]*\n?[ \t]*", "", t)


def strip_form_feeds(t: str) -> str:
    """Remove U+000C FORM FEED characters without deleting their line.

    pdftotext marks a page break with a form feed PREPENDED to the first line of the next page, so
    '\\x0cA.\\tDeclaration of Legal Principles' is both a page boundary AND the instrument's title.
    A drop_lines rule matching the form feed would delete the title with it — which is exactly the
    mistake this rule exists to prevent. Page NUMBERS sit on their own lines and are handled by
    drop_lines; the form feed itself is a character, so it is removed as one.
    """
    return t.replace("\x0c", "")


def split_numbered_paragraphs(t: str) -> str:
    """Insert a paragraph break before a line that begins a numbered principle ('1. ', '2. ' …).

    Typeset UN volumes set an enumerated list as one continuous block with no blank line between
    items, while the stored texts treat each numbered principle as its own paragraph. Without this,
    reflow collapses all nine principles of resolution 1962 (XVIII) onto a single line.

    Deliberately NARROW: it fires only on a line whose first non-space characters are digits then a
    full stop then a space, and only when the previous line is not already blank. A wrapped line
    that happens to start with a year or a quantity does not match, because those are not followed
    by '. '. It is opt-in per record, so a document where numbering runs inline is unaffected.
    """
    out = []
    for line in t.split("\n"):
        if re.match(r"^\s*\d+\.\s", line) and out and out[-1].strip():
            out.append("")
        out.append(line)
    return "\n".join(out)


PRE = {"join_hyphenated_breaks": join_hyphenated_breaks, "strip_soft_hyphens": strip_soft_hyphens,
       "strip_form_feeds": strip_form_feeds,
       "split_numbered_paragraphs": split_numbered_paragraphs}


def apply_pre(text: str, rules) -> str:
    for name in (rules or []):
        if name not in PRE:
            raise ValueError(f"unknown pre rule: {name}")
        text = PRE[name](text)
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
    if mode not in ("paragraphs", "paragraphs_tight"):
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

    if mode == "paragraphs_tight":
        # Collapse runs of blank lines to one.
        #
        # WHY THIS IS A SEPARATE MODE. The UNOOSA HTML captures pad between paragraphs with a line
        # containing a single NO-BREAK SPACE (U+00A0). Python treats U+00A0 as whitespace, so
        # `line.strip()` already reads it as blank — which is why the sequence "", "\xa0", "" emits
        # THREE blank lines where the stored text has one. The padding is the page's layout, not the
        # instrument's structure.
        #
        # It is opt-in rather than folded into "paragraphs" because collapsing blank lines is a real
        # change to a document's shape, and the record already verified under "paragraphs"
        # (registration-1975) must keep deriving from the mode it was verified under.
        tight, blank = [], False
        for line in out:
            if line == "":
                if not blank:
                    tight.append(line)
                blank = True
            else:
                tight.append(line); blank = False
        out = tight
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


def strip_heading_markers(t: str) -> str:
    """'### Article I' -> 'Article I'.

    The UNOOSA treaty pages were captured as HTML and rendered to markdown, so the article headings
    arrived as ATX headings. The '#' characters are the CAPTURE's markup, not the instrument's text —
    the treaty says "Article I", not "### Article I". Anchored to line start so a '#' inside a
    sentence (e.g. a document symbol) is untouched.
    """
    return re.sub(r"(?m)^#{1,6}[ \t]+", "", t)


def strip_links(t: str) -> str:
    """'[Treaty on Principles](https://…)' -> 'Treaty on Principles'.

    The captures render cross-references as markdown links. The link TARGET is UNOOSA's navigation,
    not the instrument's words; the link TEXT is the instrument's words and is kept verbatim. Only
    inline links are matched — a bare '[1]' footnote marker carries no target and is left alone,
    because deciding whether a footnote marker belongs in the text is a judgement, not a mechanical
    rule, and belongs in `corrections` where it needs a reason.
    """
    return re.sub(r"\[([^\]\n]*)\]\((?:[^()\n]|\([^()\n]*\))*\)", r"\1", t)


MECHANICAL = {"dehyphenate": dehyphenate, "strip_emphasis": strip_emphasis,
              "collapse_spaces": collapse_spaces,
              "strip_heading_markers": strip_heading_markers,
              "strip_links": strip_links}


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
def derive(spec: dict, orig_path: str, report=None) -> bytes:
    t = extract(orig_path, spec["extractor"])
    t = do_slice(t, spec.get("slice"))
    t, counts = drop_lines(t, spec.get("drop_lines"))
    if report is not None:
        report["dropped"] = counts
    t = apply_pre(t, spec.get("pre"))
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
    assert strip_heading_markers("### Article I\ntext") == "Article I\ntext"
    assert strip_heading_markers("#### Article II") == "Article II"
    assert strip_heading_markers("A/RES/51/122 #3") == "A/RES/51/122 #3", \
        "a '#' inside a line is not a heading marker"
    assert strip_heading_markers("#no-space") == "#no-space", "ATX headings require a space"
    assert strip_links("see [the Treaty](https://un.org/x) now") == "see the Treaty now"
    assert strip_links("[a](b) and [c](d)") == "a and c"
    assert strip_links("footnote [1] stays") == "footnote [1] stays", \
        "a bare marker has no target and is not a link"
    assert strip_links("[t](https://x.org/a_(b))") == "t", "one nested paren pair is handled"
    # nbsp padding: U+00A0 is whitespace to str.strip(), so a padded gap yields THREE blank lines
    assert reflow("a\n\n\xa0\n\nb", "paragraphs") == "a\n\n\n\nb"
    assert reflow("a\n\n\xa0\n\nb", "paragraphs_tight") == "a\n\nb"
    assert reflow("one\ntwo\n\nthree", "paragraphs_tight") == "one two\n\nthree"
    assert collapse_spaces("a    b") == "a b"
    assert collapse_spaces("a\n\nb") == "a\n\nb", "newlines must survive"
    # a trailing newline in the input yields a trailing blank line; normalize_text_bytes settles
    # the final-newline convention at the end of the pipeline, so reflow must not second-guess it
    assert reflow("one\ntwo\n\nthree\n", "paragraphs") == "one two\n\nthree\n"
    assert reflow("one\ntwo\n\nthree", "paragraphs") == "one two\n\nthree"
    assert reflow("keep\nas is", None) == "keep\nas is"
    assert do_slice("a\nb\nc", {"drop_leading_lines": 1}) == "b\nc"
    # drop_lines: removes whole lines and REPORTS how many, so a pattern that starts eating real
    # text shows up as a changed count rather than as silently missing words
    txt, counts = drop_lines("keep\n   42\nalso\n\x0cpage\n", [{"pattern": r"^\s*\d{1,3}\s*$"},
                                                              {"pattern": "\x0c"}])
    assert txt == "keep\nalso\n", txt
    assert counts == {r"^\s*\d{1,3}\s*$": 1, "\x0c": 1}, counts
    assert drop_lines("a\nb", None)[0] == "a\nb"
    # the two hyphen rules are opposites and must not be confused
    assert join_hyphenated_breaks("propa-\nganda") == "propaganda"
    assert join_hyphenated_breaks("non-\ngovernmental") == "nongovernmental"
    assert dehyphenate("non- governmental") == "non-governmental", \
        "a hyphen kept across a SPACE is a real compound; across a NEWLINE it is typesetting"
    assert strip_soft_hyphens("afore­mentioned") == "aforementioned"
    assert strip_soft_hyphens("Earth S­ atellites") == "Earth Satellites", \
        "removing only the U+00AD would leave 'S atellites' — a word split by a space"
    assert strip_soft_hyphens("inter­\nnational") == "international"
    assert apply_pre("a-\nb", ["join_hyphenated_breaks"]) == "ab"
    try:
        apply_pre("x", ["no_such_rule"])
    except ValueError:
        pass
    else:
        raise AssertionError("an unknown pre rule must raise, not pass silently")
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
