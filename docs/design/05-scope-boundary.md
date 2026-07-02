# 05 — Scope Boundary

**Status:** APPROVED — locked 2026-07-02. JC-2 approved: the five principle instruments are in scope, plus a curated foundational-resolution shortlist (exact citations to be verified in Phase C).
**Date:** 2026-07-02

This document fixes what the corpus covers in Phase 1, what it deliberately excludes, and how borderline items are handled. The discipline: **start narrow, expand only by a deliberate, recorded decision.** Breadth is added on purpose, never by drift.

The corpus is organised by **neutral legal concepts** (registration, liability, jurisdiction, non-appropriation, resource rights, abandonment/salvage). Abandonment and salvage are one concept-lens among several, never the organising purpose. Scope is defined by *sources and instruments*, not by any doctrine.

---

## 1. In scope for Phase 1

### (a) The five UN space treaties
- Outer Space Treaty (1967) — `un/treaty/ost-1967`
- Rescue Agreement (1968) — `un/treaty/rescue-1968`
- Liability Convention (1972) — `un/treaty/liability-1972`
- Registration Convention (1975) — `un/treaty/registration-1975`
- Moon Agreement (1979) — `un/treaty/moon-1979`

### (b) UN General Assembly space-law principles and resolutions

The recognised **core set of five principle instruments** (proposed for inclusion):

1. Declaration of Legal Principles Governing the Activities of States in the Exploration and Use of Outer Space — Res 1962 (XVIII), 1963
2. Principles Governing the Use by States of Artificial Earth Satellites for International Direct Television Broadcasting — Res 37/92, 1982
3. Principles Relating to Remote Sensing of the Earth from Outer Space — Res 41/65, 1986
4. Principles Relevant to the Use of Nuclear Power Sources in Outer Space — Res 47/68, 1992
5. Declaration on International Cooperation in the Exploration and Use of Outer Space for the Benefit and in the Interest of All States — Res 51/122, 1996

Plus a proposed shortlist of **foundational/operative resolutions**: Res 1721 (XVI) (1961), Res 1472 (XIV) (1959, establishing COPUOS), and the resolutions recommending national registration and space-object registration practice (e.g., Res 59/115, Res 62/101). 

> **⚖️ JUDGEMENT CALL JC-2 — Exact resolution list.**
>
> There are dozens of GA resolutions touching space over six decades. I propose we lock the five principle instruments above as definitely in scope, and treat the broader resolution stream as a *curated shortlist* (the foundational and operative ones) rather than an exhaustive sweep — with additions made deliberately at annual review. Please (a) confirm the five principle instruments, and (b) tell me whether you want the foundational-resolution shortlist as proposed, a broader sweep, or just the five principle instruments for now. I will verify the exact resolution numbers/citations against UN sources in Phase C before ingesting.

### (c) National space legislation from spacefaring jurisdictions
Sourced primarily from **UNOOSA's National Space Law Collection** and the **ASTRO database**. Phase C will map exact coverage. Priority spacefaring jurisdictions to seed with (illustrative, refined in Phase C): United States, Russian Federation, China, France, Germany, United Kingdom, Japan, India, Luxembourg, United Arab Emirates, Australia, Canada, plus others present in the UNOOSA collection.

### (d) Key soft law
- COPUOS guidelines (e.g., Space Debris Mitigation Guidelines; Guidelines for the Long-Term Sustainability of Outer Space Activities)
- IADC Space Debris Mitigation Guidelines (subject to the licensing check in doc 04, JC-5)
- PCA Optional Rules for Arbitration of Disputes Relating to Outer Space Activities (subject to the licensing check in doc 04, JC-5)

## 2. Explicitly out of scope (until a deliberate future decision)

- **ITU telecommunications regulation** (spectrum/orbital-slot allocation, Radio Regulations)
- **Export-control law** (e.g., ITAR/EAR and equivalents)
- **General international law** (except where a specific instrument is directly space-law, e.g., we do not ingest the VCLT or general UN Charter materials)
- **Aviation law** (Chicago Convention and air-law instruments)

These are excluded not because they are irrelevant but because scope must be added deliberately. Each is a candidate for a future, recorded expansion decision — not Phase 1.

## 3. Borderline items → the queue (never silently included)

When a document sits near the boundary (e.g., a dual-use instrument that is part space-law and part telecoms; a national law that is mostly export-control with a space chapter; a bilateral agreement; a national *policy* that is not *law*), the rule is:

1. Do **not** ingest it into the authoritative layer.
2. Add an entry to `queue/candidates.md` with: proposed `corpus_id`, title, `source_url`, why it is borderline, and which concept(s) it touches.
3. Surface it to you as a `⚖️ JUDGEMENT CALL` at the next review (or sooner if you ask).

The queue is the pressure valve that lets us stay narrow without losing track of things worth reconsidering. Nothing enters the corpus by drift; things enter by decision.

## 4. How scope expands later

A scope change is itself a recorded event: a dated decision note added under `docs/design/` (an ADR — "architecture decision record"), referenced in the changelog, and reflected in this document via a new version (per doc 02). This keeps the "start narrow, expand deliberately" discipline auditable for decades.

## 5. What scope is *not*

Scope is not a statement about which doctrines matter. The corpus stores the sources neutrally; the concept-tagging in the derived layer (doc 06) lets any user view the same authoritative texts through registration, liability, jurisdiction, non-appropriation, resource-rights, or abandonment/salvage lenses. The corpus retains full value regardless of how any specific doctrine develops.
