# Space Law Corpus

A neutral, authoritative, structured, machine-readable record of international and national space law, built to last for decades.

**Status:** Phase 1 foundational build — the UN-level core is complete (10 instruments, authoritative + derived layers, self-validating). Private during construction; intended to become public infrastructure at a deliberate later milestone. See [`CHANGELOG.md`](CHANGELOG.md).

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

Authoritative layer (10 instruments, English authentic text, full provenance + SHA-256 hashes):

- The **five UN space treaties** — Outer Space Treaty (1967), Rescue Agreement (1968), Liability Convention (1972), Registration Convention (1975), Moon Agreement (1979).
- The **five UN General Assembly space-law principle instruments** — Declaration of Legal Principles (1963), Direct Broadcasting (1982), Remote Sensing (1986), Nuclear Power Sources (1992), Benefits Declaration (1996).

Derived layer (for each of the above): structure extraction and neutral concept tags, deterministic first passes marked `unreviewed`.

Not yet ingested (deliberately, and tracked): national legislation, key soft law (COPUOS/IADC/PCA), and a fidelity-verification pass to upgrade texts from `extracted_unverified`. See [`docs/source-coverage.md`](docs/source-coverage.md).

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
.github/workflows CI validation + automated source monitoring + annual review
```

## How to use it

- Need the law itself? Open `authoritative/<corpus-id>/<version>/text.txt` and check its `metadata.yaml` for provenance.
- Want to navigate by concept or structure? Open the matching `derived/...` files — everything there is unofficial and traceable back to a specific authoritative version.
- Taking over maintenance? Read [`docs/MAINTAINERS.md`](docs/MAINTAINERS.md); a competent stranger can run and extend the corpus from it alone.

## Start here

Read the design lock in [`docs/design/`](docs/design/00-design-lock-index.md). Those six documents govern everything in this repository.

## Licensing (summary)

Our own contributions — the derived layer, schema, scripts, and documentation — are licensed **CC BY 4.0** (see [`LICENSE`](LICENSE)). **Source texts are not relicensed**; each remains under its own terms, recorded in that document's metadata. See [`docs/design/04-licensing-policy.md`](docs/design/04-licensing-policy.md).

## Provenance of this corpus

Design locked 2026-07-02. Maintained at an annual cadence aligned to the COPUOS Legal Subcommittee session, with automated monitoring between reviews. See [`docs/MAINTAINERS.md`](docs/MAINTAINERS.md).
