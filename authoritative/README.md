# Authoritative Layer — the legal record

**This folder contains primary source texts only**, in their authentic enacting language, each with a complete provenance record. This is the corpus's legal record.

## Absolute rules for this folder

1. **No model-generated content, ever.** No machine translations, summaries, or interpretations. Those live in `../derived/`.
2. **Append-only.** Files here are added and versioned, never overwritten. Corrections are new versions (see `../docs/design/02-versioning-scheme.md`). The single permitted edit to an existing record is adding a `superseded_by` pointer to its `metadata.yaml`.
3. **Full provenance is mandatory.** Every version folder must contain a `metadata.yaml` validating against `../schema/authoritative-metadata.schema.json`, with all required fields populated.
4. **Authentic language only.** Only authentic/official-language texts belong here. Translations are derived (see `../docs/design/03-authoritative-text-policy.md`).
5. **Gaps are recorded, not hidden.** Where an authentic text cannot be obtained, a placeholder record with `authoritative_status: authoritative_missing` and no `text.txt` documents the gap.

## Layout

```
authoritative/<corpus_id>/<version_id>/
    original.<ext>     byte-for-byte as retrieved (the integrity anchor)
    text.txt           authentic-language faithful rendering (UTF-8, LF)
    metadata.yaml       full provenance record
```

Example: `authoritative/un/treaty/ost-1967/1967-01-27/`

Nothing has been ingested yet — ingestion is Phase D and begins with the five UN treaties to prove the pipeline.
