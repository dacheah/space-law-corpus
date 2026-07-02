# 04 — Licensing Policy (per source type)

**Status:** APPROVED — locked 2026-07-02. JC-5, JC-6 approved as recommended (subject to per-source terms verification in Phase C).
**Date:** 2026-07-02

This document fixes the rights position for every kind of material in the corpus. The principle: **attribute properly, respect each source's terms, license only what is genuinely ours, and never redistribute third-party copyrighted material wholesale.** When rights are unclear, we link and cite rather than copy.

*This is an operating policy, not legal advice. Where a specific source's terms are ambiguous or high-stakes, that is a `⚖️ JUDGEMENT CALL` for you.*

---

## 1. Two different things get two different licences

- **Source texts** (treaties, resolutions, national laws, guidelines) — governed by *their own* terms. We never relicense them. We record the applicable terms per document in the `license` metadata field.
- **Our contributions** (structure extraction, concept tags, summaries, machine-draft translations, documentation, the schema, the scripts) — licensed by us under **CC-BY 4.0** (your decision). Attribution to the corpus is required; reuse is otherwise free.

The `LICENSE` file at the repository root covers **only our contributions**. A prominent `NOTICE`/README paragraph will state plainly that source texts remain under their own terms and are included with attribution.

## 2. Policy by source type

| Source type | Typical rights position | Our handling |
|---|---|---|
| **Five UN treaties** | UN documents; the treaty texts themselves are public and freely reproducible with attribution under UN terms of use. | Store full text + original artifact in the authoritative layer. Attribute to the UN / UNTS. `license: UN-materials-terms`. |
| **UN GA resolutions & principles** | UN documents; official records, freely reproducible with attribution. | Store full text. Attribute (resolution number, session, date). `license: UN-materials-terms`. |
| **UNOOSA-published material** (incl. its National Space Law Collection pages) | UN terms of use: reproduction generally permitted with attribution; some third-party content on their pages may carry other rights. | Attribute UNOOSA as `source_publisher`. Check per item for embedded third-party rights. `license: UN-materials-terms` unless flagged. |
| **National legislation — official government source** | Government works; copyright status varies by country. Many states place statutes in the public domain or permit reproduction; some assert Crown/state copyright with reuse terms. | Prefer the official government source. Record the country's specific position in `rights_note`. `license: public-domain-gov` or the specific government licence (e.g., a national open-government licence). |
| **ASTRO database texts** | Reproduced as received from states, unedited/untranslated; underlying rights are the state's. | Treat as the state's material; attribute ASTRO as the `source_publisher` and the state as issuer. Same per-country analysis as above. |
| **Soft law — COPUOS guidelines** | UN documents; reproducible with attribution. | Store + attribute. `license: UN-materials-terms`. |
| **Soft law — IADC debris-mitigation guidelines** | IADC is an inter-agency body; the guidelines are published but IADC asserts its own position. | ⚖️ Check IADC's stated terms before storing full text (see JC-5). Default to link + citation + summary if redistribution is not clearly permitted. |
| **PCA optional arbitration rules** | Published by the Permanent Court of Arbitration; PCA asserts copyright on some publications. | ⚖️ Check PCA terms; likely link + citation rather than wholesale reproduction (see JC-5). |
| **Third-party unofficial translations** (scholarly, commercial, or courtesy government translations of a foreign statute) | Copyright of the translator/publisher. | **Do not redistribute wholesale.** Link and cite. If we need a translation, we generate our own machine-draft in the derived layer (clearly unofficial) rather than copying someone else's. |

## 3. The no-wholesale-redistribution rule

> **⚖️ JUDGEMENT CALL JC-5 — Third-party copyrighted material.**
>
> Proposed firm line, for your confirmation: where a text (a) is not a public-domain government work, (b) is not clearly reproducible under the publisher's terms, or (c) is a third party's copyrighted translation, we **do not store the full text**. Instead we store a full provenance record (title, citation, `source_url`, retrieval date, hash of what we saw) plus, at most, short quotation for identification, and we link to the source. Our own machine-draft translation (derived layer, unofficial) is how we provide a readable rendering without copying anyone's protected translation.
>
> This applies notably to: IADC guidelines, PCA rules, and any scholarly/commercial translations. Please confirm this line, and tell me if you want me to treat any specific source more permissively based on terms you've checked.

## 4. Storing originals vs. linking

> **⚖️ JUDGEMENT CALL JC-6 — Do we store original artifacts in-repo?**
>
> Storing the original PDF/HTML byte-for-byte is best for durability, self-containment, and integrity (we can re-verify the hash forever, even if the source goes offline). But it (a) grows the Git repository and (b) can implicate copyright for non-public-domain items.
>
> Proposed policy: **store originals in-repo for public-domain / freely-reproducible materials** (the UN treaties, GA resolutions, COPUOS guidelines, and public-domain national statutes). For copyright-sensitive or very large items, **store the hash + URL + provenance only** and, where permitted, a local archival copy kept out of the public distribution. If the repo later needs large binaries, we adopt Git LFS (large-file storage) — a standard, portable extension. Please confirm.

## 5. Attribution mechanics

- Every authoritative record's `metadata.yaml` names the issuer and `source_publisher` and carries the `official_citation` — attribution travels with the document, permanently.
- The repository README and a `SOURCES.md` will list every source publisher and its terms in plain language.
- Derived files carry a standard disclaimer (doc 06): *"Derived, unofficial content generated by the Space Law Corpus. Not the authoritative legal text. See the linked authoritative source."*

## 6. What we will not do

- Relicense any source text as our own.
- Present CC-BY as covering the source texts (it covers only our contributions).
- Redistribute a third party's copyrighted translation to save the effort of generating our own.
- Store a copyright-sensitive full text without a rights basis, on the theory that "it's on the internet anyway."
