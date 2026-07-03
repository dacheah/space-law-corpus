# Contributing

Thank you for considering a contribution. This is a neutral legal-infrastructure resource — the authoritative structured record of space law — built to last. Contributions are welcome, but they must uphold the one principle the whole project rests on.

## The one principle

**Provenance and version integrity override convenience, always.** Every authoritative document carries, from its first commit: source URL, retrieval date, official citation, enacting jurisdiction, language, an authoritative-status flag, and a content hash. Every change is a new dated version — never an overwrite. If a change would compromise this, it will not be accepted.

## Non-negotiable rules

1. **The two-layer wall.** `authoritative/` holds primary source texts in their authentic enacting language, with full provenance. `derived/` holds machine- or human-generated structure, concept tags, summaries and translations — unofficial, traceable, never presented as authoritative. Never put derived or model-generated content under `authoritative/`.
2. **Authentic-language text only** in the authoritative layer. Translations are derived and unofficial.
3. **Prefer official sources** — the issuer or an official depositary. If the automated fetcher can't reach a source, use Claude in Chrome or supply the official file directly and store it byte-for-byte (see `docs/MAINTAINERS.md`).
4. **Gaps are flagged, not filled.** Where an authentic text can't be obtained, record an `authoritative_missing` placeholder — never substitute an unofficial text and present it as authoritative.
5. **Append-only.** Never overwrite or rewrite an authoritative text's history. Corrections and amendments are new dated versions (Git preserves every prior state).
6. **Scope discipline.** In scope: the UN treaties, UN GA space-law principles/resolutions, national space legislation, and key soft law. Borderline items go to `queue/candidates.md` for a deliberate decision — not straight into the corpus. See `docs/design/05-scope-boundary.md`.

## How to contribute

- **Report an error or propose an instrument:** open an issue. For a suspected text error, cite the authoritative source and the exact wording.
- **Ingest an instrument:** follow `docs/MAINTAINERS.md` (capture → `scripts/ingest.py` manifest → validate). Run `python3 scripts/validate_corpus.py` before opening a pull request — the CI check must pass (it enforces schema, hashes, the two-layer wall, and derived-artifact staleness).
- **Improve the derived layer:** the concept tags are a model pass marked `review_status: unreviewed`. Reviewed corrections are very welcome; a human review upgrades a tag to `review_status: human_reviewed`.
- **Read first:** the six design documents in `docs/design/` govern everything here.

## Licensing of contributions

Our own contributions — the derived layer, schema, scripts, site, and documentation — are licensed **CC BY 4.0** (`LICENSE`). By contributing, you agree your contributions are offered under CC BY 4.0. **Source texts are not relicensed**; each keeps its own terms, recorded per document. Do not contribute third-party copyrighted full text without a clear rights basis.

## Seeking a co-maintainer / institutional home

This corpus is designed to be transferable to a permanent institutional home, and to be maintained by more than one person. If you or your institution would like to help maintain it, or host it long-term, please open an issue — that conversation is explicitly welcome.

## Conduct

Be respectful and constructive. This is a shared, long-term public good; treat contributors and the record with care.
