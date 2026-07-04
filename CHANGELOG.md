# Changelog

A human-readable record of how the corpus was built and how it changes. Git holds the exact, dated, immutable history; this file is the readable summary. Dates are UTC.

## Phase 1 — Foundational build (2026-07-02)

### A. Design lock
Six design documents approved and locked (`docs/design/`): provenance schema, versioning scheme, authoritative-text policy, licensing policy, scope boundary, two-layer separation. Six judgement calls (JC-1…JC-6) decided. Governing principle fixed: provenance and version integrity override convenience.

### B. Repository & environment
Private GitHub repository created (`dacheah/space-law-corpus`); two-layer folder structure, machine-checkable JSON Schemas, CC BY 4.0 licence (our contributions only), and README established.

### C. Source investigation
Honest source-coverage report (`docs/source-coverage.md`): UNOOSA, ASTRO, national and soft-law sources mapped for formats, languages, terms, and gaps. Key finding: UN treaties/principles are clean and canonical; national legislation coverage is uneven (authentic originals vs. unofficial translations); IADC/PCA soft law needs a licensing check (JC-5).

### D. Authoritative layer — UN treaties and principles
Deterministic ingestion pipeline built (`scripts/ingest.py`, `hashing.py`, `validate_corpus.py`): capture → store original → SHA-256 hashes → provenance `metadata.yaml` → schema + hash validation; append-only, with tamper detection proven.

Ingested (English authentic text, full provenance, `text_fidelity: extracted_unverified`):

- Five UN treaties: Outer Space Treaty (`un/treaty/ost-1967`), Rescue Agreement (`un/treaty/rescue-1968`), Liability Convention (`un/treaty/liability-1972`), Registration Convention (`un/treaty/registration-1975`), Moon Agreement (`un/treaty/moon-1979`).
- Five UN GA principle instruments: Legal Principles (`un/ga/res-1962-XVIII`), Direct Broadcasting (`un/ga/res-37-92`), Remote Sensing (`un/ga/res-41-65`), Nuclear Power Sources (`un/ga/res-47-68`), Benefits Declaration (`un/ga/res-51-122`).

Sourcing notes recorded in each record's `provenance_note`: most from UNOOSA HTML pages; the **Rescue Agreement** from the Australian Treaty Series (AustLII) because UNOOSA's page was unfetchable and the only other complete copy contained transcription errors (JC-7, resolved by the maintainer: keep hunting for a clean official capture — tracked); the **five principles** sliced from UNOOSA's consolidated official compilation ST/SPACE/61/Rev.3 because the individual principle pages were unfetchable.

### E. Derived layer
`scripts/build_derived.py` produced, for all ten instruments: structure extraction (`structure.json` — units, dates, detected citations) and neutral concept tags (`concepts.json`). Deterministic (`rule_based`) first passes, `review_status: unreviewed`, quarantined in `derived/`, each traceable to its authoritative text hash with staleness detection. Minor backward-compatible refinement to the derived-metadata format recorded in `docs/design/06`.

### F. Maintenance architecture
Three GitHub Actions workflows: `validate.yml` (integrity gate on every change), `watch-sources.yml` (monthly source monitor → review issue), `annual-review.yml` (yearly COPUOS-aligned checklist). Monitored-source list in `monitoring/sources.json`; watcher in `scripts/watch_sources.py`.

### G. Transferability
Full maintainer's guide (`docs/MAINTAINERS.md`) and this changelog. Finding a permanent institutional home is noted as a future milestone, not a present dependency.

### Fidelity verification (2026-07-02)
All ten texts cross-checked word-for-word against UNOOSA's official compilation ST/SPACE/61/Rev.3 (an independent source for the treaties; source of record for the principles) — see `docs/verification-2026-07.md`. Eight were confirmed faithful. Two carried real defects, corrected per JC-8 as documented, dated corrections (prior text preserved in Git): Liability ("mattters"→"matters", "aircraft flight"→"aircraft in flight"), Moon ("depository"→"depositary"), Rescue ("to the following"→"on the following", "of the Article"→"of this Article", "authorised"→"authorized"). All ten upgraded to `text_fidelity: extracted_verified` with a `verification` record; derived layer regenerated. Schema gained optional `verification` and `corrections` fields. The **Rescue Agreement** was then re-sourced from ST/SPACE/61 (replacing the Australian Treaty Series interim base), which also corrected non-authentic ordering of the depositary Governments and authentic languages; `source_is_official` is now true and the prior state is preserved in Git.

### Roadmap Step 1 — soft law (2026-07-03)
Ingested the COPUOS **Guidelines for the Long-term Sustainability of Outer Space Activities** (preamble/context + 21 guidelines A.1–D.2), from UNOOSA's official publication of A/74/20 annex II — `un/softlaw/lts-guidelines-2019`. The COPUOS **Space Debris Mitigation Guidelines** could not be sourced from a UN full text this pass (six UNOOSA/UN routes returned blank to the fetcher or a description sheet only; the authentic text is in ST/SPACE/61 but past that PDF's extraction cut-off) — initially tracked as a follow-on rather than adopting a non-UN copy. **Resolved the same day:** the operator supplied the official UN PDF (ST/SPACE/49), which is stored byte-for-byte as `original.pdf`, and the guidelines were ingested — `un/softlaw/copuos-debris-mitigation-2007` — completing Step 1's soft-law pair. The corpus now holds 12 authoritative instruments.

### Roadmap Step 2 — concept layer (2026-07-03)
Upgraded the derived concept layer from the initial keyword pass to a **model-generated tagging** (`generation_method: model`, `review_status: unreviewed`) across all 12 instruments — 14 neutral concepts (`docs/concept-vocabulary.md`), 113 tagged provisions at article/guideline/principle granularity. Added the **cross-instrument concept index** (`derived/concept-index.json` and `derived/concept-index.md`): every provision addressing each concept, across the corpus. Tags are model output awaiting human review. Structure extraction now also recognises "Guideline" units.

### Roadmap Step 3 — browsable view (2026-07-03)
Added `scripts/build_site.py`, which generates a static, self-contained, dependency-free browsable site into `site/` from the repository (the repo stays the single source of truth; the site is read-only and regenerable). A page per instrument shows the **authoritative text alongside its full provenance** (source, official-vs-reproduction flag, retrieval date, citation, fidelity, content hash, verification, corrections); a concept page renders the cross-instrument index; derived concept tags are clearly labelled unofficial. This is the on-ramp to going public (Step 4).

### Roadmap Step 4 — go-public preparation (2026-07-03)
Ran the pre-publication audit (`docs/pre-publication-checklist-2026-07.md`): licensing basis, third-party-text, secrets/PII, and the integrity gate all clear. Added `CONTRIBUTING.md` (contribution rules honouring the provenance/two-layer principles, plus a co-maintainer invitation) and a Pages deploy workflow (`.github/workflows/pag
### Anchor upgrades + French-language pilot (2026-07-04)
**Byte-exact anchors for the five GA principle instruments.** The maintainer supplied the official
ST/SPACE/61/Rev.3 PDF (the same source document the 2026-07-02 captures were text-extracted from);
it is now stored byte-for-byte as `original.pdf` in all five `un/ga/*` records (prior text captures
preserved in Git), with appended `capture_history`, a superseding `verification`, and six dated
corrections of web-fetch extraction artifacts ("afore mentioned", "inter national" ×2,
"con sequences", "non- governmental", "non- commercial").
**Treaties deliberately NOT re-anchored to Rev.3.** Token-level cross-check showed Rev.3 modernises
the authentic-era orthography ('co-operation'→'cooperation'), reorders testimonium listings, and
drops 'the' in Rescue Art. 2 — so it serves as a second official *verification* rendering (new
`verification` records on all five treaties, five dated corrections of genuine capture defects:
OST 'Space",which', Moon 'man uvres'/'man- made'/'non- governmental' ×2, Liability doubled
'Articles'), while the byte-exact anchor upgrade is queued for the UNTS depositary volumes
(`queue/candidates.md`).
**First co-equal authentic-language record (JC-3 follow-through).** The French authentic text of the
Outer Space Treaty — `un/treaty/ost-1967/1967-01-27-fr` — ingested from the maintainer-supplied
byte-exact ST/SPACE/61/Rev.3 French edition; layout decision (language-suffixed version directory)
recorded as a dated addendum in design doc 03. Cleaning verified token-for-token (0.9987) against an
independent extraction. The corpus now holds 16 authoritative records (15 instruments; OST in two
authentic languages). Derived layer regenerated; validation green. French concept tags mirror the
English model pass and remain `unreviewed`.
fiers, official-gazette sourcing and the fetcher→Chrome→maintainer-supplied fallback ladder, authentic-vs-translation handling (JC-4), faithful reproduction of official defects with honest fidelity flags, and per-jurisdiction licensing — with the three pilot instruments as worked examples. **(c) France (Loi n° 2008-518)** — the French Space Operations Act was ingested as `nat/fra/loi-operations-spatiales-2008` from the official Légifrance **consolidated in-force version** (Titres I–VIII, Articles 1–30 plus the inserted sub-articles 7-1, 11-1, 11-2, 13-1, 20-1, 25-1). The maintainer supplied the official Légifrance PDF (the automated fetcher is blocked by Légifrance bot-protection); it is stored byte-for-byte as `original.pdf` and the cleaned French legislative text as `text.txt`. `authoritative_status` is honestly `official_consolidation` (not the as-enacted 2008 text), `version_id 2023-08-03` being the date of the latest consolidated state (LOI n° 2023-703). Légifrance's amendment-tracking apparatus and navigation labels were stripped while the official NOTA notes and the operative code-amendment lines (Arts 21, 22, 28) were kept; a known pdftotext line-wrap artifact class is flagged (`extracted_unverified`, with the byte-exact PDF as the authoritative anchor). 29 provisions concept-tagged (model pass). **This completes the national-legislation pilot — three contrasting instruments (US, Luxembourg, France) across two authentic languages, three sourcing paths, and three authoritative-status shapes. The corpus now holds 15 authoritative instruments.**

### Fidelity verification — soft law + national pilot (2026-07-03)
Verified four `extracted_unverified` texts against their official sources and upgraded them to `extracted_verified` (dated corrections; prior text preserved in Git; see each record's `verification` and `corrections` fields). **COPUOS Space Debris Mitigation Guidelines** — checked against the stored byte-exact UN PDF (`original.pdf`, ST/SPACE/49); one dropped UN document symbol restored (`A/AC.105/ C.1/L..` → `A/AC.105/C.1/L.260.`). **France (Loi 2008-518)** — independently re-extracted from the stored byte-exact Légifrance PDF and compared token-for-token: **0 substantive divergences**; seven line-wrap hyphen-joins restored (`extra-atmosphérique` ×4, `au-delà`, `2007-2008` ×2). **LTS Guidelines (2019)** — content verified word-for-word against the official UNOOSA publication (0 word/number divergences after normalising hyphenation/spacing); five hyphen-drop slips restored (`long-term` ×4, `real-time`). Then the last two were completed the same day. **Luxembourg** — the maintainer supplied the official Legilux Journal officiel PDF (Mémorial A n° 674); token-for-token comparison confirmed text.txt matches it, and crucially the three previously-flagged spacing defects (`exploitantàagréer`, `es articles`, `pleineent`) are **confirmed present in the official source** — genuine source defects faithfully reproduced, not our errors. Its integrity anchor was upgraded from the initial HTML text capture to the byte-exact official PDF (`original.pdf`; prior capture preserved in Git). **US Space Resource Act** — verified word-for-word against the official GPO US Code (govinfo.gov); the statutory body (§§51301–51303 with credits and editorial notes) matches verbatim. **The corpus is now 15 of 15 `extracted_verified` — every text-bearing authoritative record has been checked against an official source.** Finally, the **LTS** integrity anchor was upgraded from its text capture to the byte-exact official UNOOSA publication PDF (`original.pdf`); re-verifying against the full PDF extraction caught one further internal-space defect (`intergovern mental` → `intergovernmental`), now corrected. Four records (debris, France, Luxembourg, LTS) are anchored to byte-exact official PDFs; the remaining eleven (UN treaties, GA principles, US statute) are verified against official sources but anchored to text captures.

### Open follow-ons (tracked, not blocking)
- Independent (non-compilation) corroboration of the five GA principles.
- Human review of the model concept tags (upgrade `review_status` to `human_reviewed`).
- (Optional) Give the eleven text-anchored records (UN treaties, GA principles, US statute) byte-exact PDF anchors too — the four national/soft-law records (debris, France, Luxembourg, LTS) already have them; the rest are verified against official sources but anchored to text captures.
- Scale national legislation beyond the pilot (further jurisdictions), per `docs/national-law-guide.md` — a deliberate, instrument-by-instrument decision, not a sweep.
- Optionally add the **as-enacted 2008** France text as an earlier dated version (the ingested version is the consolidated in-force text).
- IADC and PCA soft law, pending the JC-5 licensing check.