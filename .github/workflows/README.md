# Automated Monitoring (GitHub Actions)

**Status:** placeholder — configured in Phase F (maintenance architecture).

Planned, using free GitHub Actions where possible:

- **Source watcher** — periodically checks in-scope sources for new or changed documents (by content hash) and opens an issue queuing anything new/altered for review. Automation watches; the maintainer judges.
- **Integrity check** — on every change, re-runs `scripts/validate.py`: schema validation, hash verification, and the two-layer wall check (`scripts/check_layers.py`).
- **Annual review reminder** — opens a review issue aligned to the COPUOS Legal Subcommittee session (triggerable earlier).

Any credentials or repository secrets these need will be requested from the maintainer as a `⚠️ MANUAL STEP`.
