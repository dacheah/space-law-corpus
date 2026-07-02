# Derived Layer — machine/human-generated, unofficial

**Everything in this folder is derived and unofficial.** Structure extraction, concept tags, summaries, and machine-draft translations. None of it is the authoritative legal text. Every artifact traces back to a specific authoritative version.

## Rules for this folder

1. **Never authoritative.** Nothing here may be presented as the legal text. Each artifact carries a standing disclaimer.
2. **One-way dependency.** Derived files reference authoritative files (`source_corpus_id` / `source_version_id` / `source_text_sha256`). Authoritative files never depend on anything here.
3. **Traceable and staleness-aware.** Each artifact records the hash of the exact authoritative text it was built from, so it can be flagged stale if that text is later corrected or superseded.
4. **Regeneration allowed.** Unlike the authoritative layer, derived artifacts may be regenerated with better models; Git retains their history.
5. **Model work is quarantined here** and labelled with generator, method, and review status (`unreviewed` / `machine_only` / `human_reviewed`).

## Layout (mirrors the authoritative tree)

```
derived/<corpus_id>/<version_id>/
    structure.json         articles, sections, dates, parties, citations
    concepts.json          neutral concept tags
    translations/<lang>.md unofficial machine-draft translations
    summary.md             plain-language summary (unofficial)
    derived-metadata.yaml  provenance of the derivation
```

Validate `derived-metadata.yaml` against `../schema/derived-metadata.schema.json`.

Nothing has been generated yet — the derived layer is built in Phase E, after the authoritative pipeline is proven.
