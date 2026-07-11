# Scripts

Portable Python tooling for the corpus. Dependencies are minimal and mainstream
(`PyYAML`, `jsonschema`) — see `requirements.txt`. Install once with:

```
pip install -r requirements.txt
```

## Implemented (Phase D)

- **`hashing.py`** — SHA-256 helpers and the canonical text-byte normalisation
  (UTF-8, LF, no BOM) that makes `text_sha256` reproducible on any machine.
- **`ingest.py`** — deterministic, offline packager. Given a captured original
  (and optional cleaned authentic text) plus a manifest of metadata fields, it
  writes an authoritative version folder (`original.*`, `text.txt`,
  `metadata.yaml`), computes hashes, and validates the result. It **refuses to
  overwrite** an existing version (append-only). Capture (fetching bytes from a
  source) is deliberately a separate step, so the retrieval boundary is explicit.
  Run: `python3 ingest.py --manifest path/to/manifest.json`
- **`validate_corpus.py`** — the integrity/structure checker: schema validation,
  hash verification (detects any silent alteration), text-presence rules, the
  two-layer wall, and derived-artifact staleness. Run: `python3 validate_corpus.py`
  (add `--path <subdir>` to scope it). Exit code 0 = OK, 1 = failures.

## Planned (later phases)

- `extract_structure.py`, `tag_concepts.py`, `draft_translation.py` — derived-layer
  passes (Phase E), using cheaper/free models, output quarantined in `../derived/`.
- `watch_sources.py` — source monitoring for the Phase F GitHub Actions.

## Proven so far

The pipeline has been exercised end-to-end: a throwaway self-test (ingest +
append-only guard + tamper detection), then the first real document — the Outer
Space Treaty English authentic text at
`authoritative/un/treaty/ost-1967/1967-01-27/`.

- **`extract.py`** — reproducibility engine. Re-extracts each `original.<ext>` with a version-pinned extractor and proves `text.txt` is a ≥97% contiguous token slice of the official original (recipes in `extraction/`). Run `python3 scripts/extract.py` to verify all; `--calibrate` to (re)author recipes. Needs `pdftotext` (poppler).
