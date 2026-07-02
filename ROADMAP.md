# Roadmap

**Status:** active, revisable. Last set 2026-07-02.
**How to use this:** this is a strategy document, not a promise. Revisit it at each annual review (COPUOS Legal Subcommittee season) or whenever something material happens, and record changes as dated updates — the same discipline the corpus applies to everything else (see `docs/design/02-versioning-scheme.md`).

## Governing strategy (one line)

**Depth and integrity before breadth; every expansion is a deliberate decision, never drift; use visibility to reduce the single-maintainer risk.** More texts under a weak structure is just more files. A smaller corpus with an excellent concept layer and airtight provenance is the thing worth transferring to an institution.

## Where we are

Phase 1 (foundational build, A–G) is complete: ten UN-level instruments (five treaties + five principle instruments), all authentic English text, full provenance, `extracted_verified` against an official UN source; a derived layer (structure + concept tags); automated validation, monitoring, and an annual-review ritual; and documentation good enough to hand over. See `CHANGELOG.md` and `docs/verification-2026-07.md`.

The two facts that drive what's next: the concept layer is still a crude keyword pass, and the project has a single maintainer. Those, not content volume, are where the leverage is.

---

## The steps (in order)

### Step 1 — Complete the UN-produced instruments (soft law)
**Goal.** Draw a defensible completeness line: "every instrument the UN itself has produced."
**Do.** Ingest the COPUOS soft-law guidelines — the Space Debris Mitigation Guidelines and the Guidelines for the Long-Term Sustainability of Outer Space Activities — from UNOOSA, with full provenance (they are clean UN documents).
**Done when.** Both are in the authoritative layer, verified, with derived artifacts, and the corpus validates.
**Effort/risk.** Low / low. **Note.** IADC and PCA are *not* in this step — they require the licensing judgement (JC-5) and are handled at Step 5-adjacent, likely as link-and-cite rather than stored full text.

### Step 2 — Upgrade the concept layer (the differentiator)
**Goal.** Turn the crude keyword tagging into the thing that makes this *the structured record*, not a folder of texts.
**Do.** Replace the first-pass keyword tags with a reviewed, model-assisted tagging pass (cheaper models for the mechanical work, quarantined in the derived layer); anchor tags to specific articles/principles; build a **cross-instrument concept view** (e.g., every provision touching "non-appropriation" across all instruments). Human-review upgrades `review_status` from `unreviewed` to `human_reviewed`.
**Done when.** Each instrument has reviewed concept tags at article/principle granularity, and a generated concept index spans the whole corpus.
**Effort/risk.** Medium / low (stays entirely in the derived layer; the authoritative record is untouched). **Note.** This is the highest-value step for turning what exists into something uniquely useful.

### Step 3 — Add a browsable view
**Goal.** Make the corpus readable by a lawyer or diplomat, not just a developer — and create the on-ramp to going public.
**Do.** A generator script that builds a simple static index/site *from* the repo (authoritative texts + derived structure/concepts + provenance shown per document). No hand-maintained content; the repo stays the single source of truth; the view is read-only and regenerable.
**Done when.** Running one script produces a browsable site reflecting the current corpus, provenance visible.
**Effort/risk.** Medium / low.

### Step 4 — Go public (deliberate governance milestone)
**Goal.** Reduce the biggest long-term risk (single maintainer) by inviting scrutiny, collaborators, and an eventual institutional home.
**Pre-flight checklist (all must pass — this is a `⚖️ JUDGEMENT CALL`).**
- Authoritative core verified ✓ and docs current ✓.
- Licensing/attribution review: confirm every stored text has a rights basis (per `docs/design/04-licensing-policy.md`); no third-party copyrighted full text stored without a basis.
- Third-party-text audit (notably anything not from a clearly public source).
- Confirm nothing private/sensitive is in the history.
**Do.** Flip the repository to public; add a short public-facing note inviting issues/contributions and a co-maintainer.
**Done when.** Repo is public with the checklist recorded as a dated decision.
**Effort/risk.** Low effort / medium consequence — hence the checklist. **Note.** This is the move most likely to recruit help; do it once the core is something you're proud to stand behind (you are close).

### Step 5 — National legislation: pilot, then scale deliberately
**Goal.** Extend into the corpus's genuinely distinctive territory — a clean, provenance-tracked national-law collection — without creating an unmaintainable mess.
**Do (pilot first).** Prove the national-law pipeline and the authentic-vs-unofficial-translation gap-handling (`⚖️ JC-4`) on **2–3 well-documented jurisdictions** (e.g., United States, France, Luxembourg). Source authentic-language originals from official national gazettes; where only an unofficial translation exists, record an `authoritative_missing` gap and keep the translation in the derived layer. Build any national-law-specific tooling once, on the pilot.
**Then scale.** Add jurisdictions one at a time, at a cadence you can sustain, each a deliberate inclusion.
**Done when (pilot).** The pilot jurisdictions are ingested, verified, and gaps flagged; the pipeline and gap-handling are proven.
**Effort/risk.** High / medium-high. **The trap to avoid:** do **not** treat national law as "ingest everything." It is unbounded, unevenly sourced, translation-heavy, and update-heavy — the fastest route to a backlog you can't maintain alone. Curated and deliberate, always.

---

## Ongoing / cross-cutting (not steps — always on)

- **Monitoring:** the monthly watcher runs; triage each `needs-review` issue (genuine change → ingest; cosmetic → close).
- **Annual review:** the COPUOS-aligned ritual; revisit *this roadmap* at that point.
- **Residual follow-on:** independent (non-compilation) corroboration of the five principles.
- **Bus-factor:** actively seek a co-maintainer or institutional home once public (Step 4 enables this).

## The standing decision rule

Breadth is added by decision, never by drift. Depth and integrity come before volume. Anything borderline goes to `queue/candidates.md`, not the corpus. Revisit and re-date this roadmap at each annual review.
