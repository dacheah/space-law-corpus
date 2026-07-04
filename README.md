# Space Law Corpus

A neutral, authoritative, structured, machine-readable record of international and national space law, built to last for decades.

**Status:** Public — a neutral legal-infrastructure resource. The UN-level core is complete: 12 instruments (5 treaties, 5 GA principle instruments, 2 COPUOS soft-law guidelines), authoritative + derived layers, verified, self-validating and self-monitoring. Contributions and a co-maintainer are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). Build history in [`CHANGELOG.md`](CHANGELOG.md).

---

## What this is

The authoritative structured record of space law, organised by neutral legal concepts (registration, liability, jurisdiction, non-appropriation, resource rights, abandonment/salvage, and others). It is a legal-infrastructure resource, **not advocacy** for any doctrine. It is designed to retain full value regardless of how any specific doctrine develops.

## What it is not

It is not a commentary, not a legal-advice service, and not organised around any single doctrine. No concept lens is the "point" of the corpus.

## The one principle everything serves

**Provenance and version integrity override convenience, always.** Every document carries, from its first commit: source URL, retrieval date, official citation, enacting jurisdiction, language, an authoritative-status flag, and a content hash. Every change is a new dated version — never an overwrite. Git provides the immutable, dated history.

## Two layers, kept strictly apart

- **`authoritative/`** — primary source texts only, in their authentic enacting language, with full provenance. This is the legal record.
- **`derived/`** — everything machine- or human-generated: translations, summaries, concept tags, structure extraction. Always labelled as derived, always traceable to its authoritative source, never presented as authoritative.

Where a file lives tells you what it is. The two never mix.

## Current contents

Authoritative layer (23 records: 15 instruments with full provenance + SHA-256 hashes. The Outer Space Treaty is held in **all five authentic languages** (en/ru/fr/es/zh) and all five UN treaties carry their French authentic text — co-equal authoritative records per design doc 03. The five GA principle instruments, both soft-law guidelines, and all eight language records carry byte-exact official-PDF anchors). The 12 UN-level instruments carry English authentic text verified against an official UN source; a deliberate 3-instrument national pilot adds authentic-language national statutes:

- The **five UN space treaties** — Outer Space Treaty (1967), Rescue Agreement (1968), Liability Convention (1972), Registration Convention (1975), Moon Agreement (1979).
- The **five UN General Assembly space-law principle instruments** — Declaration of Legal Principles (1963), Direct Broadcasting (1982), Remote Sensing (1986), Nuclear Power Sources (1992), Benefits Declaration (1996).
- **Two COPUOS soft-law guidelines** — Space Debris Mitigation Guidelines (2007) and the Guidelines for the Long-term Sustainability of Outer Space Activities (2019).
- **National-legislation pilot (3 instruments)** — the US Space Resource Act (51 U.S.C. ch. 513; English), the Luxembourg space-resources law (2017; French), and the French Space Operations Act (Loi n° 2008-518; French, official consolidated version). Deliberate and instrument-by-instrument — see [`docs/national-law-guide.md`](docs/national-law-guide.md).

Derived layer (for each of the above): structure extraction and neutral concept tags — **dual-pass reviewed**: two independent model passes, every divergence adjudicated by the maintainer, per-unit consensus/adjudication status recorded (`reviews/`) — plus a cross-instrument concept index. A generated browsable site lives in [`site/`](site/index.html).

Not yet ingested (deliberately, and tracked): national legislation beyond the current three-instrument pilot, and the IADC/PCA instruments pending the JC-5 licensing check. See [`docs/source-coverage.md`](docs/source-coverage.md) and [`ROADMAP.md`](ROADMAP.md).

## Repository map

```
docs/design/      the locked design documents (start here)
docs/             source-coverage report, maintainer's guide
authoritative/    LAYER 1 — the legal record (see authoritative/README.md)
derived/          LAYER 2 — derived, unofficial products (see derived/README.md)
schema/           machine-checkable JSON Schemas for the metadata
queue/            borderline items awaiting a scope decision
scripts/          ingestion, hashing, validation, derived-build, source-watch tooling
monitoring/       watched-source list + latest monitor report
site/             generated browsable view — open site/index.html (built by scripts/build_site.py)
.github/workflows CI validation + automated source monitoring + annual review
```

## How to use it

- Need the law itself? Open `authoritative/<corpus-id>/<version>/text.txt` and check its `metadata.yaml` for provenance.
- Want to navigate by concept or structure? Open the matching `derived/...` files — everything there is unofficial and traceable back to a specific authoritative version.
- Taking over maintenance? Read [`docs/MAINTAINERS.md`](docs/MAINTAINERS.md); a competent stranger can run and extend the corpus from it alone.

## Start here

Read the design lock in [`docs/design/`](docs/design/00-design-lock-index.md). Those six documents govern everything in this repository. For where the project is heading, see [`ROADMAP.md`](ROADMAP.md).

## How to cite

Citation metadata lives in [`CITATION.cff`](CITATION.cff) (GitHub renders a "Cite this repository"
button from it). The dataset is also published on Hugging Face as
[`dacheah/space-law-corpus`](https://huggingface.co/datasets/dacheah/space-law-corpus) — one JSONL row
per authoritative instrument version (full text + provenance) and one per concept-tagged provision.
Archived releases receive a DOI via Zenodo
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21185483.svg)](https://doi.org/10.5281/zenodo.21185483)
— concept DOI **10.5281/zenodo.21185483** (always the latest release); the current release
(v2026.07.2, human-reviewed concept layer) is **10.5281/zenodo.21189076**. Cite the version DOI
for reproducibility and check the `content_hash` of any text you rely on.

## Licensing (summary)

Our own contributions — the derived layer, schema, scripts, and documentation — are licensed **CC BY 4.0** (see [`LICENSE`](LICENSE)). **Source texts are not relicensed**; each remains under its own terms, recorded in that document's metadata. See [`docs/design/04-licensing-policy.md`](docs/design/04-licensing-policy.md).

## Provenance of this corpus

Design locked 2026-07-02. Maintained at an annual cadence aligned to the COPUOS Legal Subcommittee session, with automated monitoring between reviews. See [`docs/MAINTAINERS.md`](docs/MAINTAINERS.md).
