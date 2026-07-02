# Fidelity Verification Report — 2026-07-02

**Method.** Each stored authoritative `text.txt` was cross-checked, word-for-word (case, punctuation, hyphenation, and whitespace normalised away), against UNOOSA's official consolidated publication *International Space Law: United Nations Instruments* (**ST/SPACE/61/Rev.3**, 2025). For the **treaties** this is a genuinely independent source — they were originally ingested from UNOOSA's individual HTML pages (or, for Rescue, the Australian Treaty Series). For the **principles** it is the source of record (they were ingested from this compilation), so the check confirms extraction fidelity but is not independent corroboration.

**Caveat on the reference.** The compilation is a PDF; its text extraction carries spacing artifacts (e.g., "inter national", "non governmental", "prac ticable", "time limits"). Where our text differs from the reference only by such artifacts, **our text is the correct one** and the difference is disregarded.

---

## Results

| Instrument | Result | Notes |
|---|---|---|
| `un/treaty/ost-1967` | ✅ Faithful | Differences are compilation-side PDF spacing artifacts only. |
| `un/treaty/registration-1975` | ✅ Faithful | Only date-adjacent reference artifacts; text matches. |
| `un/treaty/moon-1979` | ✅ Faithful (minor) | Matches; a few spacing variants (e.g., "in so far"/"insofar"). |
| `un/treaty/liability-1972` | ⚠️ **Defects found** | See below — inherited from the UNOOSA HTML source. |
| `un/treaty/rescue-1968` | ⚠️ **Defects found** | See below — the Australian Treaty Series copy is not the authentic UN text. |
| `un/ga/res-1962-XVIII` (Legal Principles) | ✅ Matches source | 100% match vs ST/SPACE/61 (its source; independent check pending). |
| `un/ga/res-37-92` (Direct Broadcasting) | ✅ Matches source | 100% match. |
| `un/ga/res-41-65` (Remote Sensing) | ✅ Matches source | 100% match. |
| `un/ga/res-47-68` (Nuclear Power Sources) | ✅ Matches source | 100% match. |
| `un/ga/res-51-122` (Benefits Declaration) | ✅ Matches source | 100% match. |

## Confirmed defects

**`un/treaty/liability-1972`** (source: UNOOSA HTML page)
- Article XIX(4): "all other administrative **mattters**" → authentic: "matters" (typo, three t's).
- Article II region: "or to aircraft **flight**" → authentic: "aircraft **in** flight" (dropped word).

**`un/treaty/rescue-1968`** (source: Australian Treaty Series via AustLII)
- Preamble: "HAVE AGREED **to** the following" → authentic: "**on** the following".
- Article 5(4): "paragraphs 2 and 3 of **the** Article" → authentic: "of **this** Article".
- Article 10 / final clause: "duly **authorised**" → authentic: "authorized" (British vs. authentic orthography).
- (Possible depositary-order variant in Article 7(2) — to confirm against a UN source.)

These confirm the interim-sourcing caveats recorded at ingestion (Rescue's `provenance_note` and JC-7).

## What this means

- Eight of ten instruments are verified faithful (the five principles against their source of record; OST, Registration, Moon against an independent UN source).
- Two instruments (**Liability**, **Rescue**) carry small but real text defects that must be corrected from an authoritative source — the ST/SPACE/61 compilation carries the correct wording for every defect above.

## Open decisions (for the maintainer)

1. **How to correct Liability and Rescue** — see `⚖️ JC-8` in the session. Correcting an authentic text is never a silent edit; it is a documented, dated correction.
2. **How far to upgrade `text_fidelity`** for the eight faithful instruments, and by what mechanism (metadata-only update; text and hashes untouched; the verification recorded).
3. **Independent corroboration of the principles** (a non-compilation source) remains a tracked follow-on.

---

## Resolution (2026-07-02)

Per JC-8 (spot-correct), the confirmed defects were corrected against the compilation as documented, dated corrections (recorded in each record's `corrections` field; the prior text is preserved in Git history):

- **Liability** — "mattters" → "matters"; "aircraft flight" → "aircraft in flight".
- **Moon** — "depository" → "depositary".
- **Rescue** — "to the following" → "on the following"; "of the Article" → "of this Article"; "authorised" → "authorized".

All ten instruments were then set to `text_fidelity: extracted_verified`, with a `verification` object added to each record (the text and its hashes remain the source of truth; Git preserves every prior state). The derived layer was regenerated so no artifact is stale, and the corpus validates clean.

**Residual follow-on:** independent (non-compilation) corroboration of the five principles.

## Rescue re-source (2026-07-02)

The Rescue Agreement base text was subsequently **re-sourced from UNOOSA's official compilation ST/SPACE/61/Rev.3**, replacing the interim Australian Treaty Series text. Beyond the three spot-corrections, the Australian reproduction was found to carry non-authentic **ordering** of the depositary Governments (it listed the United Kingdom first; the authentic UN text lists the Union of Soviet Socialist Republics first) and of the authentic languages, plus British orthography (`co-operation`, `inter-governmental`). The record now carries the authentic UN text (`source_is_official: true`), with the re-source documented in its `corrections`/`provenance_note` and the prior state preserved in Git history.
