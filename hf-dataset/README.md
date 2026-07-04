---
pretty_name: Space Law Corpus
license: other
license_name: mixed-provenance
license_link: https://github.com/dacheah/space-law-corpus/blob/main/docs/design/04-licensing-policy.md
language:
- en
- fr
tags:
- legal
- law
- space-law
- provenance
- legal-nlp
- rag
- public-international-law
task_categories:
- text-retrieval
- text-classification
size_categories:
- n<1K
annotations_creators:
- machine-generated
configs:
- config_name: documents
  data_files: data/documents.jsonl
- config_name: provisions
  data_files: data/provisions.jsonl
---

# Space Law Corpus

A neutral, **provenance-first**, machine-readable record of international and national space law. Every record carries its official source, retrieval date, citation, language, an authoritative-status flag, and a SHA-256 content hash; texts are verified against official sources.

- **Source of truth / build history:** https://github.com/dacheah/space-law-corpus
- **Human-browsable site:** https://dacheah.github.io/space-law-corpus/
- **15** instruments (15 verified against official sources) · **214** provisions · **204** neutral concept tags

## Why this dataset is different

Most legal datasets are scraped text with no sourcing. Here **every row is traceable**: the authoritative text is stored in its authentic language with a content hash and a fidelity flag, and anything generated (concept tags, structure) is kept in a separate, clearly-labelled layer. That makes it low-risk input for retrieval-augmented generation and citation-grounded legal NLP.

## Configs

**`documents`** — one row per instrument version: the full authoritative `text` plus provenance (`source_url`, `official_citation`, `authoritative_status`, `text_fidelity`, `content_hash`, `license`, `rights_note`, `provenance_note`, dates, jurisdiction, language).

**`provisions`** — one row per structural unit (article / section / principle / guideline): the unit `text`, its neutral `concepts` (a model pass, unreviewed), and a link back to the source instrument's text hash and URL. Ideal as pre-chunked, concept-labelled context for RAG.

```python
from datasets import load_dataset
docs = load_dataset("dacheah/space-law-corpus", "documents")
prov = load_dataset("dacheah/space-law-corpus", "provisions")
```

## Contents

| Instrument | Jurisdiction | Adopted | Fidelity |
|---|---|---|---|
| French Space Operations Act (2008, consolidated) | FRA | 2008-06-03 | `extracted_verified` |
| Luxembourg Space Resources Law (2017) | LUX | 2017-07-20 | `extracted_verified` |
| US Space Resource Act (51 U.S.C. ch. 513) | USA | 2015-11-25 | `extracted_verified` |
| Declaration of Legal Principles | international/UN | 1963-12-13 | `extracted_verified` |
| Direct Broadcasting Principles | international/UN | 1982-12-10 | `extracted_verified` |
| Remote Sensing Principles | international/UN | 1986-12-03 | `extracted_verified` |
| Nuclear Power Sources Principles | international/UN | 1992-12-14 | `extracted_verified` |
| Benefits Declaration | international/UN | 1996-12-13 | `extracted_verified` |
| COPUOS Space Debris Mitigation Guidelines | international/UN | 2007-06-15 | `extracted_verified` |
| LTS Guidelines | international/UN | 2019-06-21 | `extracted_verified` |
| Liability Convention | international/UN | 1971-11-29 | `extracted_verified` |
| Moon Agreement | international/UN | 1979-12-05 | `extracted_verified` |
| Outer Space Treaty | international/UN | 1966-12-19 | `extracted_verified` |
| Registration Convention | international/UN | 1974-11-12 | `extracted_verified` |
| Rescue Agreement | international/UN | 1967-12-19 | `extracted_verified` |

## Licensing

**Mixed, and recorded per record.** The compilation, structure, and concept tags (the derived layer) are **CC BY 4.0**. **Source texts are not relicensed** — each keeps its own terms (e.g. UN-materials terms; public-domain government works), recorded in every row's `license` / `rights_note`. See the [licensing policy](https://github.com/dacheah/space-law-corpus/blob/main/docs/design/04-licensing-policy.md).

## Disclaimer

This is a **reference record, not legal advice**. The authoritative text of each instrument is the original in its authentic language; **translations and concept tags are unofficial and derived** (the concept tags are an unreviewed model pass — expect occasional over/under-tagging). Always confirm against the cited official source for anything legally operative.

## Citation

```
Space Law Corpus (Daniel Cheah). https://github.com/dacheah/space-law-corpus
```

_Dataset generated from the repository by `scripts/export_hf_dataset.py` on 2026-07-03 — do not edit by hand._
