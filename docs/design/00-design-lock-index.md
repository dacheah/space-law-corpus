# Space Law Corpus — Phase A Design Lock (Index)

**Status:** APPROVED — locked 2026-07-02. All six judgement calls (JC-1 … JC-6) approved by the maintainer on 2026-07-02. These six documents now govern the build; changes to them follow the versioning scheme in doc 02 (a dated decision record, never a silent overwrite).
**Date:** 2026-07-02
**Purpose:** These six documents are the foundational, locked-in design decisions for the Space Law Corpus. Once approved, they become the constitutional documents of the repository (they will live at `docs/design/` from the first commit in Phase B). Everything built afterward must conform to them.

---

## The governing principle (applies to every document here)

**Provenance and version integrity override convenience, always.** Every document in the corpus carries, from its first commit: source URL, retrieval date, official citation, enacting jurisdiction, language, an authoritative-status flag, and a content hash. Every change is a new dated version — never an overwrite. If any design choice ever conflicts with this principle, the principle wins.

## The two layers (the hard wall)

- **Authoritative layer** — primary source texts only, in their authentic enacting language, with full provenance. This is the legal record.
- **Derived layer** — everything machine- or human-generated: translations, summaries, concept tags, structure extraction. Always labelled as derived, always traceable to its authoritative source, never presented as authoritative.

These never mix. The separation is enforced physically (separate top-level folders) and in the metadata schema.

---

## The six locked documents

| # | Document | What it fixes |
|---|----------|---------------|
| 01 | [Provenance schema](01-provenance-schema.md) | The exact metadata fields every document must carry, and how content hashes are computed. |
| 02 | [Versioning scheme](02-versioning-scheme.md) | How versions are created, dated, and never overwritten; how Git history is the immutable record; the identifier scheme. |
| 03 | [Authoritative-text policy](03-authoritative-text-policy.md) | Authentic-language text is authoritative; translations are unofficial and derived; gaps are flagged, not hidden. |
| 04 | [Licensing policy](04-licensing-policy.md) | Terms per source type; our own contributions under CC-BY 4.0; no wholesale redistribution of third-party copyrighted translations. |
| 05 | [Scope boundary](05-scope-boundary.md) | What is in scope for Phase 1, what is deliberately excluded, and how borderline items are queued. |
| 06 | [Two-layer separation](06-two-layer-separation.md) | The concrete file structure and schema that enforce the authoritative/derived wall. |

---

## Repository structure (preview — built in Phase B)

```
space-law-corpus/
├── README.md                     ← plain-language overview (Phase G)
├── LICENSE                       ← CC-BY 4.0, governs OUR contributions only
├── docs/
│   ├── design/                   ← these six locked documents
│   ├── MAINTAINERS.md            ← maintainer's guide (Phase G)
│   └── source-coverage.md        ← honest source map (Phase C)
├── authoritative/                ← LAYER 1: primary source texts + provenance
│   └── <corpus-id>/<version-date>/
│         ├── original.<ext>      ← byte-for-byte as retrieved
│         ├── text.txt            ← authentic-language faithful rendering
│         └── metadata.yaml       ← full provenance record
├── derived/                      ← LAYER 2: machine/human generated, labelled
│   └── <corpus-id>/<version-date>/
│         ├── structure.json      ← articles, dates, parties, citations
│         ├── concepts.json       ← neutral concept tags
│         ├── translations/<lang>.md
│         └── derived-metadata.yaml
├── queue/                        ← borderline items awaiting a JUDGEMENT CALL
├── schema/                       ← machine-checkable JSON Schemas for the above
├── scripts/                      ← ingestion / hashing / validation (Phase D+)
└── .github/workflows/            ← automated monitoring (Phase F)
```

The physical split between `authoritative/` and `derived/` **is** the two-layer wall. A file's location tells you, unambiguously, whether it is the legal record or a derived product.

---

## JUDGEMENT CALLs — RESOLVED (approved by the maintainer, 2026-07-02)

All six were approved as recommended. Detail lives in the relevant documents; JC-5 and JC-6 remain subject to per-source terms verification in Phase C, which sets policy here but may surface individual exceptions for a fresh decision.

- **⚖️ JC-1 (doc 03):** Should a faithful *same-language* text rendering (e.g., extracted plain text of a treaty) live in the authoritative layer alongside the original artifact, or should *only* the original artifact be authoritative and every text rendering be treated as derived? *My recommendation: keep faithful same-language renderings in the authoritative layer with an explicit fidelity flag.*
- **⚖️ JC-2 (doc 05):** Exactly which UN General Assembly resolutions/principles are in scope. *My recommendation: the recognised core set of space-law principles plus the foundational resolutions; listed in doc 05 for your yes/no.*
- **⚖️ JC-3 (doc 03):** The five UN treaties are authentic in multiple languages (e.g., English, Russian, Chinese, French, Spanish). All authentic-language versions are authoritative — none is a "translation." Confirm we treat all authentic languages as co-equal authoritative texts.
- **⚖️ JC-4 (doc 03 & 05):** For national legislation where only an *unofficial* English translation is publicly available (common in UNOOSA's collection), the authoritative slot is left explicitly empty/flagged and the translation goes to the derived layer. Confirm this handling.
- **⚖️ JC-5 (doc 04):** How to treat third-party copyrighted *unofficial* translations (scholars', commercial, or a foreign ministry's courtesy translation): link and cite rather than redistribute. Confirm the no-wholesale-redistribution line.
- **⚖️ JC-6 (doc 04 & 06):** Whether to store original source artifacts (PDFs/HTML) inside the Git repository (best for durability and self-containment) versus storing only the hash + URL for copyright- or size-sensitive items. *My recommendation: store originals for public-domain UN materials; decide case-by-case for others.*

---

## What I am NOT deciding for you

Anything requiring legal judgement is flagged `⚖️ JUDGEMENT CALL` and left to you. Anything requiring your credentials, a login, or a billing choice is flagged `⚠️ MANUAL STEP` and I will wait for your explicit "done." This design-lock phase contains no such manual steps — it is all drafting for your review.
