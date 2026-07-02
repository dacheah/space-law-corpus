# Space Law Corpus

A neutral, authoritative, structured, machine-readable record of international and national space law, built to last for decades.

**Status:** Phase 1 — foundational build. Private during construction; intended to become public infrastructure at a deliberate later milestone.

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

## Repository map

```
docs/design/      the locked design documents (start here)
docs/             source-coverage report, maintainer's guide
authoritative/    LAYER 1 — the legal record (see authoritative/README.md)
derived/          LAYER 2 — derived, unofficial products (see derived/README.md)
schema/           machine-checkable JSON Schemas for the metadata
queue/            borderline items awaiting a scope decision
scripts/          ingestion, hashing, validation tooling
.github/workflows automated source monitoring (Phase F)
```

## Start here

Read the design lock in [`docs/design/`](docs/design/00-design-lock-index.md). Those six documents govern everything in this repository.

## Licensing (summary)

Our own contributions — the derived layer, schema, scripts, and documentation — are licensed **CC BY 4.0** (see [`LICENSE`](LICENSE)). **Source texts are not relicensed**; each remains under its own terms, recorded in that document's metadata. See [`docs/design/04-licensing-policy.md`](docs/design/04-licensing-policy.md).

## Provenance of this corpus

Design locked 2026-07-02. Maintained at an annual cadence aligned to the COPUOS Legal Subcommittee session, with automated monitoring between reviews. See [`docs/MAINTAINERS.md`](docs/MAINTAINERS.md).
