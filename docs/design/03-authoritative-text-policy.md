# 03 — Authoritative-Text Policy

**Status:** APPROVED — locked 2026-07-02. JC-1, JC-3, JC-4 approved as recommended.
**Date:** 2026-07-02

This document fixes what counts as authoritative text, how we flag authoritativeness, and — critically — how we handle gaps and unofficial translations without ever papering over them.

---

## 1. The core rule

**The authentic enacting-language text is the authoritative record.** Translations are unofficial, attributed, and live only in the derived layer. Where the authentic text cannot be obtained, the gap is flagged as a first-class fact — never filled with a translation dressed up as the original.

"Authentic" is a legal term of art: it is the language version(s) that the instrument itself declares to be equally definitive. For the five UN treaties, the treaty text names its own authentic languages (typically Chinese, English, French, Russian, Spanish). Each of those is authoritative and co-equal — none is a translation of another.

## 2. The `authoritative_status` flag

Every authoritative record carries exactly one status:

| Value | Meaning |
|-------|---------|
| `authentic_text` | The text is an authentic-language version as declared by the instrument (or the official depositary text). The strongest status. |
| `official_consolidation` | An official body's consolidated/amended text (e.g., a government's official consolidated statute). Authoritative but derivative-of-authentic in the ordinary legal sense; still primary, still official. |
| `certified_copy` | An official certified reproduction (e.g., depositary certified true copy) where the pure authentic original is not separately published. |
| `authoritative_missing` | A **placeholder** record: we could not obtain an authentic/official text. No `text.txt` is stored. The gap, its cause, and any derived-only translation are recorded. |

The status is a factual claim about the *source and its authority*, and must be justified in `provenance_note`. When in doubt between two statuses, choose the weaker (more cautious) one and explain.

## 3. Faithful renderings vs. translations vs. interpretation

Three different operations, treated very differently:

1. **Faithful same-language rendering** — converting the authentic text from one carrier to another *without changing the words* (e.g., extracting the text of an official PDF into UTF-8 plain text). This is transcription, not translation. Fidelity is disclosed via `text_fidelity` (`verbatim_transcription`, `extracted_verified`, `extracted_unverified`, `ocr_unverified`).
2. **Translation** — rendering the text into a *different* language. Always unofficial (unless it is itself an authentic language version, in which case it is not a translation — it is another authentic text). **Translations never enter the authoritative layer.** They live in `derived/.../translations/` with attribution and a disclaimer.
3. **Interpretation** — summary, structure extraction, concept tagging. Always derived (doc 06).

> **⚖️ JUDGEMENT CALL JC-1 — Does a faithful same-language rendering belong in the authoritative layer?**
>
> Two coherent positions:
> - **(A) Strict:** only the original artifact (`original.pdf`) is authoritative; *every* text rendering, even a verbatim transcription, is derived. Cleanest possible wall, but the machine-usable text everyone actually reads becomes "derived," which is counter-intuitive for a treaty whose official text simply *is* plain text.
> - **(B) Faithful-reproduction (my recommendation):** the original artifact **and** a faithful same-language rendering are both authoritative, with `text_fidelity` making the honesty explicit. Anything that changes the language or the meaning (translation, summary) is derived. This matches how serious legal databases operate and keeps the useful text in the authoritative record while quarantining all interpretation.
>
> I recommend **(B)**. Please confirm, or choose (A).

> **⚖️ JUDGEMENT CALL JC-3 — Co-equal authentic languages.**
>
> The five UN treaties are authentic in multiple languages. I propose we treat *each* authentic-language version as a co-equal authoritative record under the same `corpus_id` (distinguished by `language`), and store as many authentic versions as we can obtain — not privilege English. For Phase 1's proving run I will start with the English authentic text (cleanest to obtain and verify) and add the other authentic languages as a tracked follow-on, with the gaps visible until then. Please confirm this approach.

## 4. Gaps are flagged, never papered over

When we cannot obtain the authentic text, we do three things:

1. Create an authoritative record with `authoritative_status: authoritative_missing`, full `source_url`/`retrieval_date`/`provenance_note`, and **no** `text.txt`.
2. If an unofficial translation or an unofficial copy exists, store it **only** in the derived layer, clearly labelled, pointing back (`source_corpus_id`/`source_version_id`) to the placeholder.
3. Surface the gap in the Phase C source-coverage report and in the queue for the annual review, so missing authentic texts are actively tracked, not forgotten.

> **⚖️ JUDGEMENT CALL JC-4 — National legislation available only as an unofficial translation.**
>
> UNOOSA's National Space Law Collection and the ASTRO database frequently provide only an *unofficial English translation* of a national law (ASTRO texts are reproduced as received from states, unedited and often untranslated). My proposed handling: the authentic-language original is the authoritative target; where only an unofficial translation is available, the authoritative slot is `authoritative_missing` and the translation sits in the derived layer with attribution. We do **not** promote an unofficial translation into the authoritative record just because the original is hard to get. Please confirm.

## 5. Verification and the fidelity ladder

For each stored `text.txt` we record how much we trust the rendering:

- `verbatim_transcription` — typed/copied character-for-character from an authentic text and proof-read. Highest.
- `extracted_verified` — machine-extracted from the official artifact, then checked by a human against the original. High.
- `extracted_unverified` — machine-extracted, not yet human-checked. Usable, but flagged; queued for verification.
- `ocr_unverified` — produced by OCR from a scanned image; error-prone; flagged prominently.

The fidelity flag is part of provenance: it tells a future user exactly how much to trust the machine-readable text relative to the original artifact, which we always keep. Nothing is presented as more reliable than it is.

## 6. What this policy forbids

- Presenting any translation as the authoritative text.
- Auto-translating into the authoritative layer (ever).
- Filling a gap with a substitute and moving on silently.
- Editing an authentic text to "clean it up" — corrections are new versions with notes (doc 02), and cleanups belong to derived structure extraction, not the authoritative text.


---

### Dated addendum — 2026-07-04: JC-3 layout decision (co-equal authentic languages)

**⚖️ JUDGEMENT CALL (approved by maintainer, 2026-07-04).** JC-3 fixed that each authentic-language
version is a co-equal authoritative record under the same `corpus_id`, distinguished by `language`,
but did not fix the on-disk layout. Decision: a co-equal authentic-language record lives in a
**language-suffixed version directory** — `authoritative/<corpus_id>/<version_id>-<lang>/` with
`version_id` `"<date>-<lang>"` (e.g. `un/treaty/ost-1967/1967-01-27-fr/`), `language: <lang>`, and the
un-suffixed directory remaining the English record ingested first. Rationale: keeps one `corpus_id`
(so the concept index and cross-references stay unified), needs no schema or validator change, and the
suffix makes the language visible in every path and derived trace. First instance: the French
authentic text of the Outer Space Treaty, from the UNOOSA ST/SPACE/61/Rev.3 French edition.
