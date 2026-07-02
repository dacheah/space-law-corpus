# Scripts

**Status:** placeholder — tooling is built in Phase D onward.

Planned tools (all in open, portable languages — Python by default):

- `ingest.py` — fetch a source, store `original.<ext>`, compute hashes, write `metadata.yaml`, place into the authoritative layer.
- `hash.py` — compute/verify SHA-256 content hashes.
- `validate.py` — validate every `metadata.yaml` / `derived-metadata.yaml` against the JSON Schemas in `../schema/`, and check that on-disk file hashes match recorded hashes.
- `extract_structure.py`, `tag_concepts.py`, `draft_translation.py` — derived-layer passes (Phase E), using cheaper/free models, output quarantined in `../derived/`.
- `check_layers.py` — enforce the two-layer wall (no model content in authoritative/; every derived artifact traces to an authoritative version; flag stale derived artifacts).

Nothing is implemented yet.
