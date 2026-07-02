# Automated Monitoring (GitHub Actions)

Three workflows, all using the built-in `GITHUB_TOKEN` (no external secrets):

- **`validate.yml`** — runs `scripts/validate_corpus.py` on every push / pull request.
  Fails the check on any hash mismatch, schema break, broken derived-trace, or
  two-layer-wall violation. This is the integrity gate.
- **`watch-sources.yml`** — monthly (1st, 06:00 UTC) and on demand. Runs
  `scripts/watch_sources.py` to diff the monitored sources in `monitoring/sources.json`
  against their stored baseline; on a change it opens a `needs-review` issue with a
  report and advances the baseline. **Automation only watches and queues — nothing is
  ingested automatically; the maintainer judges.**
- **`annual-review.yml`** — yearly (1 April, ~COPUOS Legal Subcommittee season) and on
  demand. Opens the annual review checklist issue.

## One-time settings (see the maintainer's guide)

For a private repo the maintainer must enable Actions and set **Settings → Actions →
General → Workflow permissions → Read and write** so the watcher can open issues and
commit the updated baseline.

## Notes / limitations

- The watcher hashes page *text* (tags stripped). Index/news pages have a volatile
  "Latest" area, so some flags may be cosmetic — the reviewer triages. This is a simple,
  honest v1; it can be refined to section-scoped hashing later.
- Scheduled workflows run from the default branch only.
