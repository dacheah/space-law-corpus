# 02 — Versioning Scheme

**Status:** APPROVED — locked 2026-07-02.
**Date:** 2026-07-02

This document fixes how the corpus records versions and identifies documents. The rule underneath everything: **nothing is ever overwritten or deleted; every change is a new dated version.** Git is the substrate precisely because its history is immutable and dated.

---

## 1. Three concepts, kept distinct

Legal texts change over time, and we retrieve them at points in time. Conflating these causes silent corruption, so we separate three ideas:

- **Instrument** — a distinct legal thing (the Outer Space Treaty; France's Space Operations Act). Identified by a `corpus_id`.
- **Version** — a distinct *textual state* of that instrument (as originally adopted; as consolidated after the 2015 amendments). Identified by a `version_id`.
- **Capture** — a single *retrieval event* (we downloaded a file from a URL on a date and hashed it). Recorded in `capture_history`.

One instrument has one or more versions. One version is backed by one or more captures. This lets us answer both "what did the law say in 2008?" (version) and "when and from where did we get our copy, and has the source changed since?" (capture).

## 2. Identifier scheme (`corpus_id`)

Stable, human-readable, lowercase, slash-delimited namespaces. Once assigned, a `corpus_id` never changes — external references depend on it.

```
International treaties:   un/treaty/<slug>-<year>
UN GA resolutions:        un/ga/res-<number>-<session>       (roman session as filed)
Soft law (UN/COPUOS):     un/softlaw/<slug>-<year>
Soft law (other bodies):  <body>/softlaw/<slug>-<year>
National legislation:     nat/<ISO3166-alpha3>/<slug>-<year>
Arbitration rules:        pca/rules/<slug>-<year>
```

Examples:

| Instrument | `corpus_id` |
|---|---|
| Outer Space Treaty (1967) | `un/treaty/ost-1967` |
| Rescue Agreement (1968) | `un/treaty/rescue-1968` |
| Liability Convention (1972) | `un/treaty/liability-1972` |
| Registration Convention (1975) | `un/treaty/registration-1975` |
| Moon Agreement (1979) | `un/treaty/moon-1979` |
| Declaration of Legal Principles (Res 1962 XVIII) | `un/ga/res-1962-XVIII` |
| IADC Space Debris Mitigation Guidelines | `iadc/softlaw/debris-mitigation-2002` |
| PCA Optional Rules for Outer Space Disputes | `pca/rules/outer-space-2011` |
| US Commercial Space Launch Act (1984) | `nat/usa/commercial-space-launch-act-1984` |

The `<year>` is the year of original adoption/enactment, so the ID stays stable even as later versions are added.

## 3. Version identifier (`version_id`)

A version represents a textual state. The `version_id` is the date that state took legal effect where known, otherwise a labelled marker:

- Original text: the adoption/enactment date, `YYYY-MM-DD` (e.g., `1967-01-27`).
- A consolidated/amended text: `YYYY-consolidated` or the effective date of the consolidation (e.g., `2015-08-06`).
- Where the source gives no reliable effective date: `asretrieved-YYYY-MM-DD` (our retrieval date), with the uncertainty recorded in `provenance_note`. This is an honest fallback, never a guess dressed as a fact.

On disk: `authoritative/<corpus_id>/<version_id>/`. Example:
`authoritative/un/treaty/ost-1967/1967-01-27/`

## 4. What creates a new version vs. a new capture

This is the operational heart of "never overwrite."

- **New capture, same version (no new folder):** we re-download the same textual state and the `text_sha256` matches the existing version. We append an entry to `capture_history` (proving we re-verified) and commit. The text files are untouched.
- **Source changed but represents the *same* legal text (e.g., publisher re-typeset the PDF):** `original_sha256` differs but the text is substantively identical. We append to `capture_history`, add a `provenance_note` explaining the benign difference, and — per the JUDGEMENT CALL in doc 03 — keep the original stored version as the record. We do **not** overwrite the stored `text.txt`.
- **The legal text itself changed (amendment, consolidation, new resolution):** this is a **new version**. We create a new `<version_id>/` folder with its own files and metadata, set `supersedes` on the new version and `superseded_by` on the old one. The old version's text files are **never** modified.

The single permitted edit to an existing authoritative record is adding a `superseded_by` pointer to its metadata — a forward reference, not a change to the text or its provenance. Even this is a Git commit, so the addition is itself dated and attributable.

## 5. Git as the immutable dated record

Git stores the complete history of every file. Each commit is timestamped, attributed, and content-addressed (identified by its own hash), so the history cannot be silently rewritten without detection. Concretely:

- Every ingestion, correction note, or new version is a **commit** with a descriptive message.
- We **tag** meaningful states (e.g., `snapshot-2026-annual-review`) so a specific dated state of the whole corpus can be cited and retrieved.
- We adopt a convention that the authoritative layer is **append-only**: files under `authoritative/` are added or (for `superseded_by`) minimally annotated, never rewritten or force-pushed. This is a policy, backed later (Phase F) by a CI check that flags any modification to existing authoritative text files.
- Commit-message convention (fixed now):
  - `ingest(<corpus_id>): <version_id> — <source_publisher>`
  - `version(<corpus_id>): add <version_id>, supersedes <old_version_id>`
  - `capture(<corpus_id>): re-verify <version_id>, no text change`
  - `derive(<corpus_id>): <derived_type> for <version_id>`
  - `queue: add candidate <name> — pending JUDGEMENT CALL`

## 6. Withdrawals, corrections, and errors

- **A source retracts or a treaty is denounced:** we do not delete anything. We add a new version or a status annotation recording the withdrawal, with provenance. History shows what we held and when.
- **We ingested something wrongly (bad extraction, wrong file):** we do not silently replace it. We add a correcting version/capture with a `provenance_note` explaining the error, so the mistake and its correction are both visible. For the *derived* layer, regeneration is fine (see doc 06) — but the authoritative record's history stays intact.

## 7. Snapshots and citeability

Because a reader may need to cite "the corpus as it stood on a date," we (a) rely on Git commit hashes as immutable pointers, and (b) create an annual tag at each COPUOS-legal-subcommittee review (Phase F). A citation to the corpus therefore always resolves to an exact, reproducible state.
