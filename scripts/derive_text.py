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


def join_breaks_keep_hyphen(t: str) -> str:
    """'extra-\\natmosphérique' -> 'extra-atmosphérique'. Joins the lines, KEEPS the hyphen.

    The third member of the hyphen family, and the reason all three are separate opt-in rules rather
    than one clever heuristic:

        join_hyphenated_breaks   'propa-\\nganda'          -> 'propaganda'         hyphen dropped
        join_breaks_keep_hyphen  'extra-\\natmosphérique'  -> 'extra-atmosphérique' hyphen kept
        dehyphenate              'non- governmental'      -> 'non-governmental'   space removed

    The first two are IDENTICAL in shape — 'X-\\nY' — and differ only in whether the hyphen belongs
    to the word. Nothing in the bytes can tell them apart: 'propaganda' is one word broken by the
    typesetter, 'extra-atmosphérique' is a genuine French compound that happened to break at its own
    hyphen. Only someone reading the language knows. So the choice is declared per record, and
    picking wrongly is visible immediately as a failed byte comparison rather than as quiet damage.
    """
    return re.sub(r"(\w-)\n(\w)", r"\1\2", t)


def strip_soft_hyphens(t: str) -> str:
    """Remove U+00AD SOFT HYPHEN together with any whitespace it introduced.

    The soft hyphen is an invisible typesetting hint marking where a word MAY break. It survives PDF
    extraction where the rendered hyphen does not, and -layout output often carries the break's
    whitespace with it: 'Earth S\\xad atellites' and 'inter\\xad national'. Removing only the U+00AD
    leaves 'S atellites' — a word split by a space, which is worse than the original defect because
    it looks like real text. So the character and the whitespace that followed it go together.
    """
    # The optional leading group requires TWO OR MORE spaces. That distinction is load-bearing:
    # -layout pads a justified line with runs of spaces ('Nations P     \xad rogramme' — padding, must
    # go), but a single space before the soft hyphen is a real space between two words
    # ('United Nations \xad Conference'). Absorbing the single space fuses them into
    # 'NationsConference', which reads as a typo in the corpus rather than as our bug.
    return re.sub("(?:[ \t]{2,})?­[ \t]*\n?[ \t]*", "", t)


def strip_leading_spaces(t: str) -> str:
    """Remove leading whitespace from every line.

    -layout reproduces the printed left margin as literal spaces. Where the stored text keeps the
    document's own line wrapping (rather than reflowing it), that margin is the only difference and
    stripping it is the whole transformation. Trailing whitespace is left alone: normalize_text_bytes
    settles that at the end of the pipeline.
    """
    return "\n".join(ln.lstrip(" \t") for ln in t.split("\n"))


def strip_form_feeds(t: str) -> str:
    """Remove U+000C FORM FEED characters without deleting their line.

    pdftotext marks a page break with a form feed PREPENDED to the first line of the next page, so
    '\\x0cA.\\tDeclaration of Legal Principles' is both a page boundary AND the instrument's title.
    A drop_lines rule matching the form feed would delete the title with it — which is exactly the
    mistake this rule exists to prevent. Page NUMBERS sit on their own lines and are handled by
    drop_lines; the form feed itself is a character, so it is removed as one.
    """
    return t.replace("\x0c", "")


def strip_typesetting_controls(t: str) -> str:
    """Remove U+0007 BEL and normalise U+2002/2003 EN/EM SPACE to an ordinary space.

    The UNOOSA compendia carry both as layout instructions the extractor faithfully preserves:
    'A.\\t\\x07Declaration of Legal Principles' and 'Annex.\\u2003\\x07Principles Governing…'. Neither is
    a character of the instrument. BEL is deleted outright; the wide spaces become one ordinary
    space, because they ARE doing the work of a space between words and deleting them would fuse
    'Annex.' onto the title.
    """
    return re.sub("[  ]", " ", t.replace("\x07", ""))


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


def split_lettered_items(t: str) -> str:
    """Insert a paragraph break before a lettered sub-item ('(a) ', '(b) ' …).

    Companion to split_numbered_paragraphs, for instruments that enumerate with letters rather than
    numbers — resolution 41/65 defines its terms as '(a) The term "remote sensing" means…'. The
    volume runs them together; the stored text gives each its own paragraph.

    Requires the parenthesis to open the line, so a mid-sentence '(a)' inside a cross-reference does
    not match.
    """
    out = []
    for line in t.split("\n"):
        if re.match(r"^\s*\([a-z]\)\s", line) and out and out[-1].strip():
            out.append("")
        out.append(line)
    return "\n".join(out)


def split_short_markers(t: str) -> str:
    """Give a line that is ONLY a subsection marker ('A', 'B', 'I') its own paragraph.

    Resolution 1721 (XVI) is really two resolutions, 1721 A and 1721 B, and the volume marks the
    division with a single centred capital on its own line. With no blank line around it, reflow
    swallows the marker into the surrounding text — 'of outer space A The General Assembly,' — which
    reads as a typo and loses the division between two distinct resolutions.

    Narrow by construction: the ENTIRE line must be one to three capitals or roman numerals. It
    cannot fire on a sentence, and it cannot fire on 'A. Declaration…' because of the full stop.
    """
    out = []
    for line in t.split("\n"):
        solo = re.match(r"^\s*([A-Z]{1,3})\s*$", line)
        if solo and out and out[-1].strip():
            out.append("")
        out.append(line)
        if solo:
            out.append("")
    return "\n".join(out)


def split_principle_headings(t: str) -> str:
    """Put a paragraph break after a line that is ONLY a principle heading ('Principle I').

    Some instruments in the volume set the heading on its own line with the text running straight on
    beneath it, and the stored text keeps the heading as a standalone paragraph. Fires only when the
    whole line is the heading — resolution 47/68 writes 'Principle 1. Applicability of international
    law' with substantive text on the SAME line and must not be split, which is why this is opt-in
    per record rather than always on.
    """
    out = []
    for line in t.split("\n"):
        out.append(line)
        if re.match(r"^\s*Principle\s+[IVXLCDM0-9]+\.?\s*$", line):
            out.append("")
    return "\n".join(out)


PRE = {"join_hyphenated_breaks": join_hyphenated_breaks,
       "join_breaks_keep_hyphen": join_breaks_keep_hyphen, "strip_soft_hyphens": strip_soft_hyphens,
       "strip_form_feeds": strip_form_feeds,
       "strip_typesetting_controls": strip_typesetting_controls,
       "strip_leading_spaces": strip_leading_spaces,
       "split_numbered_paragraphs": split_numbered_paragraphs,
       "split_lettered_items": split_lettered_items,
       "split_short_markers": split_short_markers,
       "split_principle_headings": split_principle_headings}


def split_before(text: str, prefixes) -> str:
    """Insert a paragraph break before any line starting with one of the declared literal prefixes.

    THE ESCAPE HATCH, AND WHY IT IS NARROW. The other split rules key off a structural signal the
    typesetter left behind — a number, a letter, a heading on its own line. Occasionally there is no
    signal at all: resolution 47/68 runs 'Such design and use shall also ensure…' straight on from
    the previous sentence with no blank line, no indent and no marker, yet the stored text sets it as
    its own paragraph. No general rule can see that, and inventing one that fires on sentence shape
    would corrupt other records.

    So the break is declared literally, per record, with a reason — visible in the recipe rather than
    hidden in a regex that happens to work. Each prefix must match EXACTLY ONE line, and this raises
    otherwise: a prefix that stops matching means the source changed, and a prefix that matches twice
    means it is not the anchor its author thought it was.
    """
    if not prefixes:
        return text
    lines = text.split("\n")
    for p in prefixes:
        hits = [i for i, ln in enumerate(lines) if ln.lstrip().startswith(p)]
        if len(hits) != 1:
            raise ValueError(
                f"split_before prefix {p!r} matched {len(hits)} lines, expected exactly 1 — "
                f"re-review before editing; the stored original may have changed"
            )
    out = []
    for line in lines:
        if any(line.lstrip().startswith(p) for p in prefixes) and out and out[-1].strip():
            out.append("")
        out.append(line)
    return "\n".join(out)


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
    if mode == "tight":
        # Collapse runs of blank lines WITHOUT joining anything. For sources whose stored text keeps
        # the document's own line wrapping — the Légifrance consolidated PDF is set as a single
        # column and its wrapping IS the text's shape — so joining would destroy it, but removing
        # page furniture still leaves blank runs behind.
        out, blank = [], False
        for line in text.split("\n"):
            if line.strip() == "":
                if not blank:
                    out.append("")
                blank = True
            else:
                out.append(line); blank = False
        return "\n".join(out)
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


# ---- stage 4b: declared regex substitutions ---------------------------------------------------
def apply_substitutions(text: str, subs):
    """Declared regex substitutions, each with an expected match count.

    WHEN TO USE THIS RATHER THAN `corrections`. A correction repairs ONE place and names it
    literally, which is right for a human judgement about a specific defect. Some publisher
    apparatus is repetitive instead: Légifrance appends '(Article 1)', '(Articles 2 à 5)' to every
    heading and stamps 'VERSION EN VIGUEUR DEPUIS LE 03/08/2023' throughout. Recording 150 literal
    corrections would bury the handful of real judgements among them.

    THE GUARD IS WHAT KEEPS THIS FROM BECOMING REGEX SOUP. Every substitution declares how many
    matches it expects, and a mismatch RAISES. A pattern that silently starts matching more (or
    less) of the document is the exact failure this module exists to prevent, and a regex is far
    easier to get subtly wrong than a literal string.
    """
    for s in (subs or []):
        rx = re.compile(s["pattern"], re.M)
        n = len(rx.findall(text))
        want = s.get("count")
        if want is not None and n != want:
            raise ValueError(
                f"substitution {s['pattern']!r} expected {want} match(es), found {n} — the stored "
                f"original may have changed; re-review before editing"
            )
        text = rx.sub(s.get("replacement", ""), text)
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
    t = split_before(t, spec.get("split_before"))
    t = reflow(t, spec.get("reflow"))
    t = apply_mechanical(t, spec.get("mechanical"))
    t = apply_substitutions(t, spec.get("substitutions"))
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
    assert reflow("a\n\n\n\nb", "tight") == "a\n\nb"
    assert reflow("one\ntwo\n\nthree", "tight") == "one\ntwo\n\nthree", \
        "'tight' collapses blank runs but must NOT join wrapped lines"
    assert strip_leading_spaces("   a\n  b") == "a\nb"
    assert apply_substitutions("A (Article 1)\nB (Articles 2 à 5)",
                               [{"pattern": r" \(Articles? [^)]*\)$", "replacement": "", "count": 2}]) == "A\nB"
    try:
        apply_substitutions("x", [{"pattern": "zzz", "replacement": "", "count": 1}])
    except ValueError:
        pass
    else:
        raise AssertionError("a substitution whose count is wrong must raise, not pass silently")
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
    assert join_breaks_keep_hyphen("extra-\natmosphérique") == "extra-atmosphérique"
    assert join_breaks_keep_hyphen("propa-\nganda") == "propa-ganda", \
        "same shape as join_hyphenated_breaks — only a reader of the language can choose between them"
    assert dehyphenate("non- governmental") == "non-governmental", \
        "a hyphen kept across a SPACE is a real compound; across a NEWLINE it is typesetting"
    assert strip_soft_hyphens("afore­mentioned") == "aforementioned"
    assert strip_soft_hyphens("Earth S­ atellites") == "Earth Satellites", \
        "removing only the U+00AD would leave 'S atellites' — a word split by a space"
    assert strip_soft_hyphens("inter­\nnational") == "international"
    assert strip_soft_hyphens("Nations P     ­ rogramme") == "Nations Programme", \
        "-layout pads BEFORE the soft hyphen too; leaving that padding yields 'P rogramme'"
    assert strip_soft_hyphens("United Nations ­ Conference") == "United Nations Conference", \
        "a SINGLE space before the soft hyphen is a real word space and must survive"
    assert apply_pre("a-\nb", ["join_hyphenated_breaks"]) == "ab"
    assert strip_typesetting_controls("A.\t\x07Declaration") == "A.\tDeclaration"
    assert strip_typesetting_controls("Annex.\u2003\x07Principles") == "Annex. Principles", \
        "the EM SPACE is doing a space's work and must not simply vanish"
    assert split_lettered_items("intro\n(a) first\n(b) second") == "intro\n\n(a) first\n\n(b) second"
    assert split_lettered_items("see (a) inline") == "see (a) inline", \
        "a mid-sentence marker must not open a paragraph"
    assert split_principle_headings("Principle I\ntext") == "Principle I\n\ntext"
    assert split_short_markers("of outer space\n   A\nThe General Assembly,") \
        == "of outer space\n\n   A\n\nThe General Assembly,"
    assert split_short_markers("A. Declaration of Legal") == "A. Declaration of Legal", \
        "a section label with a full stop is not a bare marker"
    assert split_short_markers("A sentence starting with A") == "A sentence starting with A"
    assert split_before("a\nSuch design and use x", ["Such design"]) == "a\n\nSuch design and use x"
    assert split_before("a\nb", None) == "a\nb"
    for bad in (["nope"], ["a"]):
        try:
            split_before("a\nSuch design\na", bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"split_before must raise when a prefix matches != 1 line: {bad}")
    assert split_principle_headings("Principle 1. Applicability of law and more") \
        == "Principle 1. Applicability of law and more", \
        "a heading with substantive text on the same line must not be split"
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
    # ---- derivable:false declarations must be well formed AND falsifiable -------------------
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        open(os.path.join(td, "original.txt"), "w", newline="\n").write("hello\n")
        open(os.path.join(td, "text.txt"), "w", newline="\n").write("hello\n")
        o = os.path.join(td, "original.txt")
        real = "sha256:" + hashlib.sha256(b"hello\n").hexdigest()

        # a bad basis is rejected
        st, _ = check_not_derivable({"not_derivable_basis": "because-i-said-so",
                                     "not_derivable_reason": "x"}, {"text_sha256": real}, o)
        assert st == "error", "an undeclared basis must not pass"
        # an empty reason is rejected
        st, _ = check_not_derivable({"not_derivable_basis": "would_be_a_transcript",
                                     "not_derivable_reason": "  "}, {"text_sha256": real}, o)
        assert st == "error", "a 'cannot' with no reason is indistinguishable from 'did not try'"
        # a well-formed declaration with no attempted pipeline is accepted
        st, d = check_not_derivable({"not_derivable_basis": "different_source_artefact",
                                     "not_derivable_reason": "text predates this artefact"},
                                    {"text_sha256": real}, o)
        assert st == "declared", d
        # THE KEY ONE: if the recorded best effort actually reproduces the text, the claim is stale
        st, d = check_not_derivable(
            {"not_derivable_basis": "would_be_a_transcript", "not_derivable_reason": "r",
             "attempted": {"extractor": {"tool": "passthrough"}}},
            {"text_sha256": real}, o)
        assert st == "error" and "stale" in d, \
            "a not-derivable claim whose own pipeline succeeds must be reported, not believed"

    print("derive_text selftest: OK")
    return 0


NOT_DERIVABLE_BASES = {
    "different_source_artefact":
        "The stored text was produced from something other than the stored original — typically an "
        "earlier capture that a byte-exact artefact later replaced as the integrity anchor. No "
        "pipeline over the stored original can reproduce it, however it is written.",
    "would_be_a_transcript":
        "Reproducible in principle, but only by declaring so many literal anchors that the recipe "
        "would restate the stored output instead of describing a transformation of the source. Such "
        "a recipe proves nothing about the original, so it is refused rather than written.",
}


def check_not_derivable(spec: dict, meta: dict, orig: str):
    """Validate a `derivable: false` declaration and try to FALSIFY it.

    A record that cannot be re-derived is a legitimate outcome, and saying so plainly is better than
    an absent recipe (which is indistinguishable from work not yet done) or a forced one. But an
    unfalsifiable claim is not worth much either, so:

      * the reason must be non-empty and its `basis` must be one of the declared kinds;
      * if the recipe still carries a best-effort `attempted` pipeline, it is RUN. If that pipeline
        turns out to reproduce the stored text byte-for-byte, the declaration is WRONG and this
        reports an error — a stale "cannot be done" is exactly the kind of comfortable claim that
        outlives its evidence.

    Returns (status, detail) where status is 'declared' or 'error'.
    """
    reason = (spec.get("not_derivable_reason") or "").strip()
    basis = spec.get("not_derivable_basis")
    if basis not in NOT_DERIVABLE_BASES:
        return "error", (f"not_derivable_basis {basis!r} is not one of "
                         f"{sorted(NOT_DERIVABLE_BASES)}")
    if not reason:
        return "error", ("derivable is false but not_derivable_reason is empty — an undocumented "
                         "'cannot' is indistinguishable from 'did not try'")
    attempted = spec.get("attempted")
    if not attempted:
        return "declared", f"{basis}; no best-effort pipeline recorded"
    try:
        got = derive(attempted, orig)
    except Exception as e:                                            # noqa: BLE001
        return "declared", f"{basis}; best-effort pipeline raises ({type(e).__name__})"
    if "sha256:" + hashlib.sha256(got).hexdigest() == meta.get("text_sha256"):
        return "error", ("declared NOT derivable, but the recorded best-effort pipeline reproduces "
                         "the stored text byte-for-byte — the declaration is stale, delete it and "
                         "promote the pipeline")
    import difflib
    ratio = difflib.SequenceMatcher(
        None, got.decode("utf-8", "replace").split("\n"),
        open(os.path.join(os.path.dirname(orig), "text.txt"), encoding="utf-8").read().split("\n")
    ).ratio()
    return "declared", f"{basis}; best effort reaches {ratio:.4f}, not 1.0"


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
    ok = fail = declared = 0
    for sp in specs:
        spec = json.load(open(sp, encoding="utf-8"))
        cid, ver = spec["corpus_id"], spec["version_id"]
        vd = os.path.join(AUTH, cid, ver)
        meta = yaml.safe_load(open(os.path.join(vd, "metadata.yaml"), encoding="utf-8"))
        orig = os.path.join(vd, meta["original_filename"])
        if spec.get("derivable") is False:
            status, detail = check_not_derivable(spec, meta, orig)
            if status == "declared":
                print(f"  NOT DERIVABLE (declared) {cid}/{ver}\n     {detail}")
                declared += 1
            else:
                print(f"  ERROR      {cid}/{ver}: {detail}")
                fail += 1
            continue
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
    if declared:
        print(f"{declared} further record(s) are DECLARED NOT DERIVABLE, each with a recorded "
              f"reason. Those texts remain hash-pinned by text_sha256 — tamper-evident, but not "
              f"reproducible from the stored original. The distinction is the point: a corpus that "
              f"says which of its texts can be rebuilt, and which can only be checked, is making a "
              f"claim it can defend.")
    if fail:
        print("A mismatch means the declared pipeline no longer reproduces the stored text — "
              "investigate before changing either.")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
