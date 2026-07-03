# Source Coverage Report

**Status:** Phase C — first pass, 2026-07-02. Portal-level source map. Exhaustive per-document enumeration (exact URLs, hashes, party counts) happens at ingestion (Phase D), where each figure is captured with provenance.

This report answers, for each in-scope source: what it exposes, in what formats, in what languages, under what terms — and, honestly, **where authoritative texts are missing or only unofficial translations exist.** Where a live UNOOSA page could not be retrieved by the automated fetcher (their server timed out repeatedly during this pass), findings are grounded in current search results and are flagged for direct verification at ingestion.

---

## 1. Summary judgement (read this first)

- **The five UN treaties are the clean, canonical starting point.** Authentic-language texts are public, stable, and freely reproducible with attribution. This is why Phase D begins here to prove the pipeline.
- **UN GA principles and resolutions are equally clean** — official UN documents, multiple languages.
- **National legislation is the hard part.** Coverage is genuinely uneven: 40+ jurisdictions, but a mix of authentic-language originals and *unofficial* translations, variable formats, and irregular updates. This is where our "gaps are flagged, not papered over" rule earns its keep.
- **Soft law is mixed on rights.** COPUOS guidelines are UN documents (clean). IADC guidelines and PCA rules are published by non-UN bodies that may assert their own copyright — so these are the first real tests of JC-5 (link/cite vs. reproduce) and must be checked before storing full text.

---

## 2. Source-by-source map

### 2.1 The five UN treaties — UNOOSA + UN Treaty Series + UN AVL

| Attribute | Finding |
|---|---|
| **Primary portal** | UNOOSA Space Law "Treaties and Principles": `https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties.html` (each treaty also has its own HTML page, e.g. `.../treaties/outerspacetreaty.html`). |
| **Status data** | UNOOSA "Status of international agreements relating to activities in outer space": `https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties/status/index.html` (updated annually). Cross-source: UNODA treaties database `https://treaties.unoda.org/t/outer_space`. |
| **Consolidated official text** | UN publication *International Space Law: United Nations Instruments*, ST/SPACE/61/Rev.3 (2025) — treaties + principles in one document: `https://www.unoosa.org/res/oosadoc/data/documents/2025/stspace/stspace61rev_3_0_html/st_space_61rev03E.pdf` (English; other UN-language editions exist). |
| **Most authoritative source of record** | The **UN Treaty Series (UNTS)** registration (e.g., OST = 610 UNTS 205, reg. no. 8843) and the **UN Audiovisual Library of International Law** (`legal.un.org/avl`). Prefer these for the depositary text. |
| **Formats** | HTML (per-treaty pages) and PDF (UNTS scans, ST/SPACE compilation). |
| **Authentic languages** | Chinese, English, French, Russian, Spanish — **equally authentic** per each treaty's final clause. Arabic exists as a later UN translation (6th official language) but is **not** an authentic text of these treaties -> derived layer if used. |
| **Approximate participation (as of 2025, verify at ingestion)** | OST ~116 parties; Rescue Agreement ~100; Liability Convention ~100; Registration Convention ~75; Moon Agreement ~18. Treat as indicative only until captured from the status page with a retrieval date. |
| **Terms** | Treaty texts are legal instruments, freely reproducible with attribution. See section 3 on the distinction between the treaty text and UN *publication* copyright. |
| **Gaps** | None material for English authentic text. Obtaining all five authentic-language versions (esp. Chinese/Russian originals as clean text vs. scanned PDF) will require per-language verification — tracked as an open item, gaps visible until filled (JC-3). |

### 2.2 UN General Assembly principles & resolutions

| Attribute | Finding |
|---|---|
| **Portal** | UNOOSA "Treaties and Principles" and the UNOOSA documents/resolutions database (`https://www.unoosa.org/oosa/en/ourwork/spacelaw/docs.html` and the resolutions search). Also the official UN Digital Library for A/RES/ documents. |
| **In-scope core** | The five principle instruments (Legal Principles 1963; DBS 1982; Remote Sensing 1986; Nuclear Power Sources 1992; Benefits Declaration 1996) — confirmed in scope (JC-2). Foundational/operative resolutions to be finalised as a curated shortlist. |
| **Formats / languages** | HTML + PDF; six UN languages. Resolutions are official records — clean provenance. |
| **Gaps** | None material; exact resolution numbers/citations to be verified against the UN Digital Library at ingestion. |

### 2.3 National space legislation — UNOOSA National Space Law Database + ASTRO

| Attribute | Finding |
|---|---|
| **Portals** | (a) UNOOSA National Space Law Database: `https://www.unoosa.org/oosa/en/ourwork/spacelaw/nationalspacelaw/index.html` (+ a "Schematic Overview" page); (b) **ASTRO** (Accessing Space Treaty Resources Online): `https://astro.unoosa.org/` — launched 2022, funded by Luxembourg, covering national space laws, policies and regulations of COPUOS member states. |
| **Coverage** | 40+ jurisdictions. Known contributors span the major spacefaring states and many others (e.g., US, Russia, and a large Asia-Pacific group — Australia, India, Indonesia, Japan, Malaysia, Philippines, Republic of Korea, Thailand, Viet Nam — plus many more). Exact current list to be enumerated at ingestion. |
| **Critical caveat (from UNOOSA itself)** | ASTRO texts are **"reproduced in the form and in the language(s) in which they were received from States, and were not formally edited and/or translated by the United Nations."** So a given entry may be an authentic-language original **or** a state-supplied unofficial translation — this must be checked per document, not assumed. |
| **Update cadence** | Irregular, with variable coverage (confirmed as a known limitation). Monitoring (Phase F) must therefore watch for silent additions/changes. |
| **Formats / languages** | Mixed: PDF and HTML; original languages and/or English. Quality varies. |
| **Gaps (the honest part)** | Expect three recurring situations: (1) authentic-language original present -> authoritative layer; (2) only an unofficial/state-supplied translation present -> authoritative slot = `authoritative_missing`, translation -> derived layer (JC-4); (3) UNOOSA/ASTRO lists a law but links out to a national gazette we must fetch separately. Prefer the **official national gazette / government source** as the authoritative source of record; use UNOOSA/ASTRO as the finding aid and cross-check. |

### 2.4 Soft law

| Instrument | Source | Format / rights | Handling |
|---|---|---|---|
| **COPUOS Space Debris Mitigation Guidelines** (endorsed by GA Res 62/217, 2007) | UNOOSA | UN document; PDF/HTML; freely reproducible w/ attribution | Authoritative-clean; store + attribute. |
| **COPUOS Guidelines for the Long-Term Sustainability of Outer Space Activities** (2019) | UNOOSA | UN document | Authoritative-clean; store + attribute. |
| **IADC Space Debris Mitigation Guidelines** (IADC-02-01, Rev. 3 2021; a Rev. 4 is also referenced) | UNOOSA mirror `https://www.unoosa.org/documents/pdf/spacelaw/sd/IADC_space_debris_mitigation_guidelines.pdf` and IADC `https://www.iadc-home.org/` | PDF; **IADC is a non-UN inter-agency body** and may assert its own terms | **JC-5 test.** Verify IADC's stated terms before storing full text; default to link + citation + our own summary if redistribution isn't clearly permitted. Note version ambiguity (Rev.3 vs Rev.4) — capture the exact revision. |
| **PCA Optional Rules for Arbitration of Disputes Relating to Outer Space Activities** (adopted 6 Dec 2011; based on UNCITRAL 2010 rules) | Permanent Court of Arbitration `https://pca-cpa.org/` | PDF; **PCA asserts copyright on its publications** | **JC-5 test.** Likely link + citation rather than wholesale reproduction; confirm PCA terms. |

### 2.5 Not a legal-text source (noted for completeness)

The **UN Register of Objects Launched into Outer Space** (registration data submitted under the Registration Convention) is a *data* resource, not a source of legal texts, and is **out of scope** for the corpus. Mentioned only so a future maintainer doesn't mistake it for a legislation source.

---

## 3. Licensing / terms findings (feeds JC-5 and JC-6)

- **Treaty and resolution *texts* vs. UN *publications*.** The treaty texts themselves are legal instruments and are freely reproducible with attribution; there is broad, settled practice of reproducing them. Separately, the UN asserts copyright over its **publications, compilations, and databases** (e.g., the typeset ST/SPACE/61 volume, the ASTRO database as a database). UN policy permits reproducing **excerpts** of publications "provided that acknowledgment of the United Nations as source and a proper copyright statement is given," and routes broader/commercial/translation reuse to `permissions@un.org`.
  - **Practical line for us:** store the **treaty/resolution text** with attribution (authoritative layer); attribute UNOOSA/UNTS as publisher; do not represent our copy as the UN's official publication; cite (don't wholesale-copy) UN *compilations* as compilations.
- **National legislation:** rights vary by country — many statutes are public-domain government works; some states assert Crown/state copyright with reuse terms. Record each country's position in `rights_note` at ingestion (per doc 04).
- **IADC / PCA:** non-UN publishers with their own asserted rights -> **JC-5 applies**; verify terms before storing full text.
- **JC-6 (store originals in-repo):** for the UN treaties, GA resolutions, and COPUOS guidelines (public / freely reproducible), storing byte-for-byte originals in-repo is appropriate. For IADC/PCA and copyright-asserting national sources, default to hash + URL + provenance unless terms clearly permit storage.

**Reminder:** this is an operating policy, not legal advice. Anything ambiguous or high-stakes returns to the maintainer as a `⚖️ JUDGEMENT CALL`.

---

## 4. Borderline items for the queue

None newly identified in this portal-level pass. Expect candidates to surface during national-legislation ingestion (e.g., laws that are mostly telecoms/export-control with a space chapter; national space *policies* that are not *law*). These go to `queue/candidates.md`, not the corpus.

---

## 5. Recommended Phase D ingestion order

1. **Outer Space Treaty (1967), English authentic text** — from UNTS / UN AVL, cross-checked against UNOOSA. Proves the full pipeline end-to-end (fetch -> store original -> hash -> metadata -> validate).
2. The remaining four treaties (English authentic text), same method.
3. Add other **authentic-language** versions of each treaty (JC-3), gaps visible until complete.
4. The five GA principle instruments.
5. COPUOS guidelines (clean soft law).
6. **Then** national legislation, jurisdiction by jurisdiction, applying the authentic-vs-translation gap rule (JC-4) rigorously.
7. IADC / PCA only after their terms are checked (JC-5).

---

*Sources consulted for this pass are recorded in the Phase C research log (chat) and will be re-captured with retrieval dates and hashes at ingestion. UNOOSA live pages to be re-verified directly at ingestion, as the automated fetcher timed out against their server during this pass.*
