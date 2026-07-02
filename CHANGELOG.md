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

Sourcing notes recorded in each record's `provenance_note`: most from UNOOSA HTML pages; the **Rescue Agreement** from the Australian Treaty Series (AustLII) because UNOOSA's page was unfetchable and the only other complete copy contained transcription errors (JC-7, resolved by Dan: keep hunting for a clean official capture — tracked); the **five principles** sliced from UNOOSA's consolidated official compilation ST/SPACE/61/Rev.3 because the individual principle pages were unfetchable.

### E. Derived layer
`scripts/build_derived.py` produced, for all ten instruments: structure extraction (`structure.json` — units, dates, detected citations) and neutral concept tags (`concepts.json`). Deterministic (`rule_based`) first passes, `review_status: unreviewed`, quarantined in `derived/`, each traceable to its authoritative text hash with staleness detection. Minor backward-compatible refinement to the derived-metadata format recorded in `docs/design/06`.

### F. Maintenance architecture
Three GitHub Actions workflows: `validate.yml` (integrity gate on every change), `watch-sources.yml` (monthly source monitor → review issue), `annual-review.yml` (yearly COPUOS-aligned checklist). Monitored-source list in `monitoring/sources.json`; watcher in `scripts/watch_sources.py`.

### G. Transferability
Full maintainer's guide (`docs/MAINTAINERS.md`) and this changelog. Finding a permanent institutional home is noted as a future milestone, not a present dependency.

### Fidelity verification (2026-07-02)
All ten texts cross-checked word-for-word against UNOOSA's official compilation ST/SPACE/61/Rev.3 (an independent source for the treaties; source of record for the principles) — see `docs/verification-2026-07.md`. Eight were confirmed faithful. Two carried real defects, corrected per JC-8 as documented, dated corrections (prior text preserved in Git): Liability ("mattters"→"matters", "aircraft flight"→"aircraft in flight"), Moon ("depository"→"depositary"), Rescue ("to the following"→"on the following", "of the Article"→"of this Article", "authorised"→"authorized"). All ten upgraded to `text_fidelity: extracted_verified` with a `verification` record; derived layer regenerated. Schema gained optional `verification` and `corrections` fields. The **Rescue Agreement** was then re-sourced from ST/SPACE/61 (replacing the Australian Treaty Series interim base), which also corrected non-authentic ordering of the depositary Governments and authentic languages; `source_is_official` is now true and the prior state is preserved in Git.

### Open follow-ons (tracked, not blocking)
- Verify the ten texts against certified references; upgrade `text_fidelity` from `extracted_unverified`.
- Re-capture the Rescue Agreement from a UN/depositary source to replace the Australian Treaty Series copy.
- Ingest national legislation and key soft law (COPUOS/IADC/PCA under the JC-5 check).
- Human review of the first-pass concept tags.
