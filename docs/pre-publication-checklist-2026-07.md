# Pre-Publication Checklist — 2026-07-03

The deliberate governance review run before making the repository public (Roadmap Step 4). Recorded as a dated decision (per `docs/design/02-versioning-scheme.md`). Going public is a `⚖️ JUDGEMENT CALL`; this is the evidence for it.

## Automated audit results

| Check | Result |
|---|---|
| **Licensing basis — every stored text** | ✅ All 12 instruments are official UN documents (`license: UN-materials-terms`, `source_is_official: true`, `authoritative_status: authentic_text`), freely reproducible with attribution. |
| **Third-party copyrighted base texts** | ✅ None. Every stored base is an official source (the interim Australian Treaty Series base for the Rescue Agreement was re-sourced to the UN compilation). IADC/PCA full texts are deliberately *not* stored (deferred under JC-5). |
| **Secrets / keys / tokens** | ✅ None found. Workflows use the built-in `GITHUB_TOKEN`; no hard-coded secrets. |
| **Personal data / PII** | ✅ Only public contacts appear in files (`actions@github.com` bot email; UN `permissions@un.org`). No personal emails. See the open item below re: the operator first name. |
| **Required public files** | ✅ `LICENSE` (CC BY 4.0), `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `ROADMAP.md`, `docs/MAINTAINERS.md` all present. |
| **Integrity gate** | ✅ `validate_corpus.py` passes (12 authoritative + 12 derived records). |

## Resolved

- **Operator name in provenance — resolved.** To keep the record neutral, the `retrieved_by`/`verified_by` fields were genericised to `maintainer + Claude` across the 12 records (metadata-only; authoritative text and hashes untouched; prior state preserved in Git). Note that **Git commit history still carries the committer name/email** from the GitHub account used — standard for any public repo, and not scrubbed.

## Not blocking, but worth knowing

- Derived **concept tags are `unreviewed`** (a model pass); the site and index label them unofficial. Fine to publish as-is; human review upgrades them over time.
- **Two instruments are `extracted_unverified`** (the two soft-law guidelines — the debris one stores the byte-exact UN PDF; LTS from the UN booklet). Clearly flagged; verification is a tracked follow-on.

## Decision

Publication is a maintainer decision. On approval: flip the repository to **public**, optionally enable **GitHub Pages** (a `pages.yml` workflow is included to publish `site/`), set a repository description and topics, and open the invitation for a co-maintainer (see `CONTRIBUTING.md`).
