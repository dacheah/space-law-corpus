# 01 — Provenance Schema

**Status:** APPROVED — locked 2026-07-02.
**Date:** 2026-07-02

This document fixes the exact metadata every authoritative document must carry. Provenance is the foundation of the corpus and cannot be retrofitted, so this schema is deliberately strict: no document enters the authoritative layer without every **required** field populated.

Metadata is stored as a `metadata.yaml` file sitting beside each document version. YAML is chosen because it is plain text (survives decades, diffs cleanly in Git, readable by a human with no tools) and is trivially machine-parseable. A matching machine-checkable definition lives at `schema/authoritative-metadata.schema.json`, so a validation script can reject any record missing a required field before it is ever committed.

---

## 1. The seven non-negotiable fields (from the governing principle)

Every authoritative document **must** carry all seven. These are the fields the founding principle names explicitly:

| Field | Meaning | Example |
|-------|---------|---------|
| `source_url` | The exact URL the document was retrieved from | `https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties/outerspacetreaty.html` |
| `retrieval_date` | Date (UTC, ISO 8601) the file was captured | `2026-07-02` |
| `official_citation` | The recognised official/legal citation | `610 UNTS 205; UN Res 2222 (XXI)` |
| `jurisdiction` | The enacting jurisdiction | `international/UN` or ISO 3166-1 alpha-3 (`USA`, `FRA`, `JPN`) |
| `language` | Language of *this stored text* (ISO 639-1/639-3) | `en` |
| `authoritative_status` | The authoritativeness flag (see doc 03) | `authentic_text` |
| `content_hash` | Cryptographic hash of the content (see §4) | `sha256:9f2c…` |

## 2. The full field set

The seven above are necessary but not sufficient to make provenance verifiable and durable. The complete required schema:

### Identity
- `corpus_id` *(required)* — stable internal identifier for the instrument (scheme in doc 02). *e.g.* `un/treaty/ost-1967`
- `version_id` *(required)* — identifier for this textual version (doc 02). *e.g.* `1967-01-27` (adoption) or `2015-consolidated`
- `title` *(required)* — official title of the instrument, verbatim
- `short_title` *(optional)* — common name. *e.g.* `Outer Space Treaty`

### Legal identity
- `jurisdiction` *(required)* — as above
- `document_type` *(required)* — one of: `treaty`, `ga_resolution`, `national_legislation`, `soft_law_guideline`, `arbitration_rules`
- `official_citation` *(required)*
- `authentic_languages` *(required)* — list of all languages in which the instrument is authentic. *e.g.* `[en, ru, zh, fr, es]`
- `adoption_date` *(required if known, else `null` + note)*
- `entry_into_force_date` *(optional)*
- `effective_date` *(optional)* — for national legislation, the in-force date of this version

### Source & retrieval (the provenance trail)
- `source_url` *(required)*
- `source_publisher` *(required)* — who published the copy we retrieved. *e.g.* `UNOOSA`, `ASTRO`, `Legifrance`, `US GPO`
- `source_is_official` *(required, boolean)* — is `source_publisher` the official issuer or an official depositary? (vs. a mirror/aggregator)
- `retrieval_date` *(required)*
- `retrieved_by` *(required)* — tool + operator. *e.g.* `corpus-ingest v0.1 / manual: the maintainer`
- `original_format` *(required)* — `pdf`, `html`, `docx`, `txt`
- `original_filename` *(required)* — the stored artifact name. *e.g.* `original.pdf`

### Integrity (hashes — see §4)
- `content_hash` *(required)* — hash of the primary stored content (the `text.txt` rendering if present, else the original artifact). Prefixed with algorithm. *e.g.* `sha256:…`
- `original_sha256` *(required)* — hash of the byte-for-byte original artifact
- `text_sha256` *(required if a `text.txt` exists)* — hash of the stored text rendering
- `text_fidelity` *(required if a `text.txt` exists)* — one of: `verbatim_transcription`, `extracted_verified`, `extracted_unverified`, `ocr_unverified`

### Status & language of stored text
- `language` *(required)* — language of the stored `text.txt`
- `authoritative_status` *(required)* — enum defined in doc 03: `authentic_text`, `official_consolidation`, `certified_copy`, `authoritative_missing` (placeholder record where we could not obtain the authentic text)

### Rights
- `license` *(required)* — terms governing the *source text* (doc 04). *e.g.* `UN-materials-terms`, `public-domain-gov`, `see-provenance-note`
- `rights_note` *(optional)* — any redistribution caveats

### History & relationships
- `capture_history` *(required, append-only list)* — every retrieval event: `{date, source_url, original_sha256, note}`. Never edited, only appended.
- `supersedes` *(optional)* — `corpus_id/version_id` this version replaces
- `superseded_by` *(optional)* — filled in when a later version arrives (this is the one permitted metadata *addition* to an old record; the text is never touched — see doc 02)
- `related_documents` *(optional)* — cross-references (amends, implements, protocol-to)

### Free-text provenance
- `provenance_note` *(required)* — plain-language account of how this was obtained and anything a future maintainer must know (e.g., "UNOOSA page lists this as the depositary text; cross-checked against UNTS registration no. 8843").

---

## 3. Worked example (`metadata.yaml` for the Outer Space Treaty, English authentic text)

```yaml
corpus_id: un/treaty/ost-1967
version_id: "1967-01-27"
title: "Treaty on Principles Governing the Activities of States in the Exploration and Use of Outer Space, including the Moon and Other Celestial Bodies"
short_title: "Outer Space Treaty"

jurisdiction: international/UN
document_type: treaty
official_citation: "610 UNTS 205; UNGA Res 2222 (XXI); TIAS 6347"
authentic_languages: [en, ru, zh, fr, es]
adoption_date: "1966-12-19"
entry_into_force_date: "1967-10-10"

source_url: "https://treaties.un.org/doc/Publication/UNTS/Volume%20610/volume-610-I-8843-English.pdf"
source_publisher: "United Nations Treaty Series (UNTS)"
source_is_official: true
retrieval_date: "2026-07-02"
retrieved_by: "corpus-ingest v0.1 / manual: the maintainer"
original_format: pdf
original_filename: original.pdf

content_hash: "sha256:PLACEHOLDER_computed_at_ingest"
original_sha256: "sha256:PLACEHOLDER_computed_at_ingest"
text_sha256: "sha256:PLACEHOLDER_computed_at_ingest"
text_fidelity: extracted_verified

language: en
authoritative_status: authentic_text

license: "UN-materials-terms"
rights_note: "UN document; reproduced with attribution per UN terms of use."

capture_history:
  - date: "2026-07-02"
    source_url: "https://treaties.un.org/doc/Publication/UNTS/Volume%20610/volume-610-I-8843-English.pdf"
    original_sha256: "sha256:PLACEHOLDER_computed_at_ingest"
    note: "Initial capture from UNTS."

supersedes: null
superseded_by: null
related_documents: []

provenance_note: >
  English authentic text as registered in the UN Treaty Series, vol. 610,
  registration no. 8843. The OST is authentic in five languages; each is
  stored as a co-equal authoritative version under this corpus_id.
```

## 4. How content hashes are computed (exact, reproducible)

A hash is a short fingerprint of a file's exact bytes; if a single character changes, the hash changes completely. This is how we prove, years later, that a stored text has not been silently altered.

Rules, fixed now so any maintainer reproduces the same value:

1. **Algorithm:** SHA-256. Every hash value is written with its algorithm prefix (`sha256:`) so we can migrate to a stronger algorithm in future without ambiguity.
2. **`original_sha256`** is computed over the **raw bytes** of the original artifact exactly as retrieved — no normalisation, no re-encoding. This is the anchor of integrity.
3. **`text_sha256`** is computed over the **raw bytes of `text.txt` as stored** (UTF-8, LF line endings, no BOM). We fix the encoding so the hash is stable across machines.
4. **`content_hash`** is a convenience pointer equal to `text_sha256` when a text rendering exists, otherwise `original_sha256`. It exists so tooling has one canonical field to check.
5. Hashes are computed by the ingestion script at capture time and are **never** hand-edited. A validation script recomputes them from the files on disk and fails if they disagree with `metadata.yaml`.

> **⚖️ JUDGEMENT CALL JC-1** — see doc 03. Whether `text.txt` (a same-language rendering) is itself part of the authoritative record affects whether `text_sha256`/`content_hash` point at authoritative bytes. My recommendation (keep faithful same-language renderings authoritative, with the `text_fidelity` flag doing the honest disclosure) is reflected above.

## 5. Placeholder records for missing authentic texts

Provenance integrity means we **record the gap** rather than hide it. Where the authentic text cannot be obtained (only an unofficial translation exists, or the source is offline), we still create an authoritative record with `authoritative_status: authoritative_missing`, populated `source_url`/`retrieval_date`/`provenance_note` explaining the gap, and **no** `text.txt`. The unofficial translation, if any, lives only in the derived layer and points back to this placeholder. This makes gaps first-class, queryable facts. (See doc 03 §4 and doc 05.)
