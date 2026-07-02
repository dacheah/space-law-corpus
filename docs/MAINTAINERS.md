# Maintainer's Guide

This guide is written so that **a competent stranger could take over the Space Law Corpus from this document alone.** You do not need to have been involved in the original build. You do need care: this is a legal-record project, and its value rests entirely on the integrity of its provenance.

Read the six design documents in [`docs/design/`](design/00-design-lock-index.md) once before making changes. They are the constitution; this guide is the operating manual.

---

## 1. The one principle

**Provenance and version integrity override convenience, always.**

Every authoritative document carries, from its first commit: source URL, retrieval date, official citation, enacting jurisdiction, language, an authoritative-status flag, and a content hash. Every change is a new dated version — never an overwrite. If any choice ever conflicts with this principle, the principle wins. When in doubt, do the slower, more traceable thing.

## 2. The two layers (the wall)

- **`authoritative/`** — primary source texts only, in their authentic enacting language, with full provenance. The legal record. **No model-generated content, ever. Append-only.**
- **`derived/`** — everything machine- or human-generated: structure extraction, concept tags, summaries, translations. Unofficial, labelled, traceable to a specific authoritative version. May be regenerated.

Where a file lives tells you what it is. The wall is enforced by folder location, by the schemas (`schema/`), and by the validator. Never put an interpretation, translation, or summary under `authoritative/`.

## 3. Environment setup

You need [Git](https://git-scm.com/) (or the [GitHub Desktop](https://desktop.github.com/) app — friendlier, no command line) and Python 3.11+.

```
pip install -r scripts/requirements.txt   # PyYAML, jsonschema
python3 scripts/validate_corpus.py         # should print RESULT: OK
```

If the validator prints OK, your environment works and the corpus is intact.

## 4. Identifiers and layout

Stable, lowercase, slash-delimited `corpus_id` (never changes once assigned — external references depend on it):

```
un/treaty/<slug>-<year>       e.g. un/treaty/ost-1967
un/ga/res-<number>-<session>  e.g. un/ga/res-1962-XVIII  (or res-37-92)
un/softlaw/<slug>-<year>
<body>/softlaw/<slug>-<year>  e.g. iadc/softlaw/debris-mitigation-2002
nat/<ISO3166-alpha3>/<slug>-<year>
pca/rules/<slug>-<year>
```

On disk, each instrument version is a folder:

```
authoritative/<corpus_id>/<version_id>/
    original.<ext>    byte-for-byte / as-retrieved artifact (integrity anchor)
    text.txt          authentic-language text (UTF-8, LF)
    metadata.yaml      full provenance (schema: schema/authoritative-metadata.schema.json)
derived/<corpus_id>/<version_id>/
    structure.json  concepts.json  derived-metadata.yaml
```

`version_id` is the date the textual state took effect (adoption/consolidation), `YYYY-MM-DD`, or a labelled fallback if the source gives no reliable date (record the uncertainty in `provenance_note`).

## 5. How to ingest a new authoritative document

Capture and ingest are deliberately **separate** steps.

**Step A — Capture.** Obtain the source. Prefer the official issuer or an official depositary. Save exactly what you retrieved as a local file (the "capture"). Note the exact URL and today's date.

**Step B — Prepare the text.** Produce a clean `text.txt` of the **authentic-language** text only (no editorial apparatus, no translation). If you cannot get an authentic text — only an unofficial translation — do **not** ingest it as authoritative; see §8 (gaps).

**Step C — Write an ingest manifest** (JSON) with the metadata fields (see any existing `metadata.yaml` for a worked example, and `docs/design/01-provenance-schema.md` for field definitions). Point it at your capture file and your `text.txt`:

```json
{
  "corpus_id": "nat/xxx/...-YYYY",
  "version_id": "YYYY-MM-DD",
  "title": "...", "jurisdiction": "XXX", "document_type": "national_legislation",
  "official_citation": "...", "authentic_languages": ["xx"],
  "source_url": "https://...", "source_publisher": "...", "source_is_official": true,
  "retrieval_date": "YYYY-MM-DD", "retrieved_by": "you",
  "original_format": "pdf", "language": "xx",
  "authoritative_status": "authentic_text", "license": "...",
  "text_fidelity": "extracted_unverified",
  "provenance_note": "how obtained, caveats, verification status",
  "original_source_path": "/path/to/capture", "text_source_path": "/path/to/text.txt"
}
```

**Step D — Run the packager.** It stores the files, computes hashes, writes `metadata.yaml`, and validates:

```
python3 scripts/ingest.py --manifest your-manifest.json
```

It **refuses to overwrite** an existing version (append-only). If validation fails, fix the manifest — do not hand-edit hashes.

**Step E — Commit.** `ingest(<corpus_id>): <version_id> — <source_publisher>`.

### Flags you must set honestly
- `authoritative_status`: `authentic_text` (authentic-language/depositary), `official_consolidation`, `certified_copy`, or `authoritative_missing` (a flagged gap, no `text.txt`).
- `source_is_official`: is the publisher the issuer/depositary, or a reproduction/aggregator? A clean government treaty-series copy that isn't the depositary is `false`.
- `text_fidelity`: `verbatim_transcription` > `extracted_verified` > `extracted_unverified` > `ocr_unverified`. Never claim more than you checked.

## 6. Versioning (never overwrite)

- **Same text, re-retrieved:** append to `capture_history`; do not touch the text files.
- **The legal text changed (amendment/consolidation/new resolution):** create a **new** `version_id` folder; set `supersedes`/`superseded_by`. The old version is never modified.
- **You made an ingestion error:** add a correcting version/capture with a `provenance_note` explaining it. The mistake and its correction both stay visible. (Derived artifacts, by contrast, may simply be regenerated.)
- The authoritative layer is **append-only**. Never force-push or rewrite history.

## 7. The derived layer

Rebuild derived artifacts (structure + concept tags) for all documents:

```
python3 scripts/build_derived.py
python3 scripts/validate_corpus.py
```

These are deterministic (`rule_based`) first passes, `review_status: unreviewed`. They are honest mechanical drafts — expect false positives/negatives in concept tags. When you human-review one, set its `review_status` to `human_reviewed` and record `reviewed_by`. Every derived artifact stores the hash of the authoritative text it was built from; if that text changes, the validator warns that the artifact is **stale** and must be regenerated. Never let derived content leak into `authoritative/`.

## 8. Gaps are recorded, not hidden

If you cannot obtain an authentic text: create an `authoritative_status: authoritative_missing` record (populated `source_url`/`retrieval_date`/`provenance_note`, **no** `text.txt`). Put any unofficial translation only in the derived layer, pointing back to the placeholder. Surface the gap in `docs/source-coverage.md` and at the annual review. A visible gap is an asset; a hidden one is a liability.

## 9. Monitoring and the annual review

Three GitHub Actions workflows (`.github/workflows/`, documented in `.github/workflows/README.md`):

- **`validate.yml`** runs the validator on every push/PR. If it goes red, the corpus's integrity is in question — investigate before merging.
- **`watch-sources.yml`** (monthly + manual) diffs the sources in `monitoring/sources.json` and opens a `needs-review` issue on change. Triage it: is this a genuinely new/amended instrument (ingest it), or a cosmetic page change (close the issue)? Automation watches; **you** judge.
- **`annual-review.yml`** (yearly, ~COPUOS Legal Subcommittee season, + manual) opens the deep-review checklist. Trigger it early from the Actions tab if something material happens.

One-time settings for a private repo: **Settings → Actions → General → Workflow permissions → Read and write**.

## 10. Licensing (per source type)

Our own contributions (derived layer, schema, scripts, docs) are **CC BY 4.0** (`LICENSE`). Source texts are **not** relicensed — each keeps its own terms, recorded per document in `metadata.yaml` and summarised in `docs/design/04-licensing-policy.md`. Do not store full text you lack a rights basis for (notably third-party copyrighted translations, and check IADC/PCA terms): link and cite, and generate our own unofficial machine-draft instead. When rights are unclear or high-stakes, treat it as a judgement call, not a default.

## 11. Scope

In scope: the five UN treaties, UN GA space-law principles/resolutions, national space legislation (UNOOSA/ASTRO/official gazettes), key soft law (COPUOS/IADC/PCA). Out of scope until a deliberate, recorded decision: ITU telecoms regulation, export-control law, general international law, aviation law. Borderline items go to `queue/candidates.md`, **not** into the corpus, until decided. Record any scope change as a dated decision note.

## 12. Succession

Everything here is in open, portable, well-documented formats (plain text, YAML, JSON, Python, Git) specifically so the corpus can move to a permanent institutional home when the time comes. **Finding that home is a future milestone, not a present dependency** — the corpus is fully functional and maintainable as it stands. To hand it over: transfer the Git repository (history and all), this guide, and the design documents. Nothing else is required.

---

*If you change how the corpus works, update this guide and the design documents in the same commit. The next stranger is relying on it.*
