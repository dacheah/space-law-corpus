# Handling national legislation

National space legislation is the hardest part of the corpus, and the part where the two-layer wall and the provenance principle earn their keep. UN treaties and GA principles are clean and canonical — one issuer, authentic languages fixed in the final clause, freely reproducible. National law is none of those things: dozens of jurisdictions, authentic texts in many languages, some behind official gazettes that block automated fetching, licensing that varies country by country, and finding-aids that quietly mix originals with unofficial translations. This guide is the operating manual for that terrain. It sits under the maintainer's guide (`docs/MAINTAINERS.md` §5) and the design documents (`docs/design/`), and does not override them.

## The pilot, and why it is deliberate

National ingestion is a **considered, instrument-by-instrument pilot, not a sweep**. Breadth is worthless if any single record's provenance is doubtful. The first three instruments were chosen to exercise the hard cases rather than the easy ones:

- **`nat/usa/space-resources-2015`** — 51 U.S.C. ch. 513 (the Space Resource Exploration and Use Act). English authentic; a US Government work in the public domain; taken from the official GPO edition of the US Code. The easy shape: authentic English, official source, clean licence.
- **`nat/lux/ressources-espace-2017`** — the Luxembourg Law of 20 July 2017 on the exploration and use of space resources. **French authentic** (not English); sourced from Legilux via Claude in Chrome because the automated fetcher could not reach the site; and reproduced **with the official page's own spacing defects intact** rather than silently corrected. This record is the template for the hard national case.
- **`nat/fra/...`** (France, Loi n° 2008-518) — French authentic; behind a bot-protected official portal (Légifrance); large consolidated text. The template for "the official source is real but awkward to retrieve."

Each new jurisdiction should be added the same way: one instrument, fully provenanced, before the next.

## 1. Identifiers

National instruments use `nat/<ISO 3166-1 alpha-3>/<slug>-<year>`, lowercase, assigned once and never changed (external references depend on it). Examples: `nat/usa/space-resources-2015`, `nat/lux/ressources-espace-2017`, `nat/fra/loi-operations-spatiales-2008`. The `<year>` is the year of the instrument, not of retrieval. `document_type` is `national_legislation`; `jurisdiction` is the same alpha-3 code. Where a country has several relevant instruments, give each its own slug rather than crowding them into one.

## 2. Sourcing — prefer the official national gazette

The **official source of record is the national government's own publication**: the gazette or official legal portal of the enacting state (Légifrance for France, Legilux for Luxembourg, the GPO US Code for the United States). UNOOSA's National Space Law Database and **ASTRO** are excellent *finding aids* — use them to discover what exists and to cross-check — but treat them as pointers, not as the source of record. UNOOSA states plainly that ASTRO texts are "reproduced in the form and in the language(s) in which they were received from States, and were not formally edited and/or translated by the United Nations." So an ASTRO entry may be an authentic original **or** a state-supplied unofficial translation. Always resolve to the official national publication and record *that* as `source_url` / `source_publisher`, with `source_is_official: true`.

### When the fetcher can't reach the source

Official legal portals frequently block the automated web fetcher (bot-protection, JavaScript-only rendering). The fallback ladder, in order of preference:

1. **Claude in Chrome** — a real browser reaches pages the fetcher cannot. This is how the Luxembourg text was retrieved from Legilux. Extract the authentic text; record the retrieval in `provenance_note`.
2. **Maintainer-supplied official file** — have the maintainer download the official PDF/text directly from the gazette and drop it in the folder. Store it **byte-for-byte** as `original.<ext>`; its `original_sha256` then fingerprints the authentic file, which is a provenance *upgrade* over any text rendering. This is the right choice for large or awkward texts (e.g. a long consolidated statute) where reconstructing the text through a browser risks transcription error in an authoritative legal document. It is the same pattern used for the COPUOS debris guidelines.

Never bypass or solve a CAPTCHA or bot-detection challenge to obtain a text. If a portal actively blocks automated access, use route 2 (a human downloads the file) instead.

## 3. Authentic language is authoritative; translations are derived (JC-4)

This is the rule that national law tests hardest, because most national space law is not in English.

- The **authentic-language text** — the language(s) in which the instrument was enacted — is the only thing that goes in `authoritative/`. Luxembourg's authoritative text is **French**. France's is **French**. Do not put an English rendering in the authoritative layer, however good.
- A **translation is always derived and unofficial**, regardless of who produced it — including an official state-supplied translation, and including our own machine drafts. It lives in `derived/<corpus_id>/<version>/translations/<lang>.md`, carries a `translation` record in `derived-metadata.yaml` (`derived_type: translation`, `generation_method`, `generator`, `review_status`, `source_text_sha256` bound to the authoritative text, `license`, and a plain disclaimer), and is regenerated by `build_derived.py`, which detects `translations/*.md` automatically. It is never presented as authoritative.
- **Where only a translation exists** (the authentic text cannot be obtained): create an `authoritative_status: authoritative_missing` placeholder with no `text.txt`, and attach the translation in the derived layer pointing back to the placeholder. A visible gap is an asset; a substituted unofficial text presented as authoritative is a liability.

A worked example ships with the corpus: `derived/nat/lux/ressources-espace-2017/2017-07-20/translations/en.md` is a machine-draft English translation of the Luxembourg law — clearly labelled unofficial, bound by hash to the French authoritative text, `review_status: unreviewed`. It demonstrates the JC-4 handling end to end.

## 4. Reproduce the official source faithfully — including its defects

The authoritative text must match its official source **exactly**, defects and all. Official gazettes sometimes contain typographic or spacing errors; the corpus reproduces them verbatim and **flags** them, rather than silently "fixing" them (a silent fix is an unrecorded edit to a legal record). The Luxembourg record does this: the Legilux HTML runs several words together (Art. 7(2) "L'exploitantàagréerdoitdisposer…", Art. 12 "es articles", Art. 16 "pleineent"). Those are reproduced as-is, with `text_fidelity: extracted_unverified` and a `provenance_note` describing each defect and its source. If and when the text is checked character-by-character against the official gazette PDF, upgrade `text_fidelity` to `extracted_verified` and add a `verification` record — never quietly rewrite the text. Corrections, if genuinely warranted, are new dated versions (append-only), not overwrites.

Set `text_fidelity` honestly: `verbatim_transcription` > `extracted_verified` > `extracted_unverified` > `ocr_unverified`. Never claim more than you actually checked.

## 5. Licensing — per jurisdiction, recorded per document

National statutes carry different rights in different countries; record each one in the record's `license` / `rights_note`, and default to caution:

- **United States** — federal statutes are US Government works in the **public domain** (`license: public-domain-gov`); store freely.
- **France / Luxembourg** — official legal texts published by the state are freely reproducible with attribution to the gazette; many EU states treat official texts as outside copyright or under permissive reuse. Record the gazette as publisher and the reuse basis in the metadata.
- **Crown-copyright and similar** — some states (e.g. UK-tradition jurisdictions) assert copyright over official texts with specific reuse terms. Record the terms; store full text only where they clearly permit it, otherwise link + cite + our own derived summary.
- **State-supplied translations** — often third-party copyrighted; do not store as our text. Link and cite, and generate our own unofficial machine-draft in the derived layer instead.

When rights are unclear or high-stakes, treat it as a `⚖️ JUDGEMENT CALL` for the maintainer, not a default.

## 6. Checklist for a new national instrument

1. Assign `nat/<alpha-3>/<slug>-<year>`; confirm it is genuinely in scope (space *law*, not telecoms/export-control with a space clause — borderline goes to `queue/candidates.md`).
2. Locate the official national gazette version; use UNOOSA/ASTRO only to find and cross-check it.
3. Capture the authentic-language text (fetcher → Chrome → maintainer-supplied byte-exact file, in that order of fallback). Store the byte-for-byte `original.<ext>`.
4. Ingest via `scripts/ingest.py` with `document_type: national_legislation`, honest `authentic_languages`, `source_is_official`, `text_fidelity`, and a `provenance_note` recording exactly how it was obtained and any reproduced defects.
5. If only a translation exists, ingest an `authoritative_missing` placeholder and attach the translation in `derived/`.
6. Add any needed concept tags in `scripts/concept_tags.py`, then `python3 scripts/build_derived.py && python3 scripts/validate_corpus.py`.
7. Regenerate the site (`python3 scripts/build_site.py`), update `CHANGELOG.md`, commit, push.

*This guide is part of the operating manual. If you change how national law is handled, update this file and the design documents in the same commit.*
