#!/usr/bin/env python3
"""Re-derive source baselines after a change to the monitor's comparable text.

WHY THIS EXISTS. Any change to `to_text()`'s normalisation — unescaping HTML entities (watch_sources
v3.10), adjusting whitespace — changes the hash of every HTML source, so the first sweep after it
reports the WHOLE corpus CHANGED. Announcing a "one-time reset" in the report is not good enough: the
flood buries whatever genuine change was pending, and it teaches the reader to skim the reports. This
tool re-derives the baselines in the same change instead.

THE RULE, AND WHY IT CANNOT SWALLOW A REAL SIGNAL. For each source the LIVE page is hashed under BOTH
normalisations — the old rules recovered from git (the old CODE ITSELF, never a re-typing of it) and the
new rules — and both are compared with the stored baseline:

    old == stored   the page has not moved since its baseline, so only the normalisation differs.
                    Re-baselining to the new hash is LOSSLESS.
    old != stored   the page genuinely differs from its baseline: a REAL pending signal. Left
                    untouched and reported, because adopting a new baseline here is exactly the
                    silent swallow this tool exists to prevent.

BINARY DOCUMENTS are hashed as bytes and are untouched by a text-normalisation change, so their
baselines are left exactly as they are.

RECORD-MODE SOURCES (`schema`, `json_extract`) need nothing: their alert decision runs on the RECORD
hash, and records are extracted from the DOM where entities are already resolved. Their page hash
simply refreshes on the next sweep. Do NOT compute a page hash for them — for those sources
`last_sha256` is the RECORD hash, and comparing a page hash against it reports "moved" on a source that
never moved.

A BUG THIS TOOL SHIPPED WITH, AND THE RULE IT TEACHES (2026-09-14). Its first version decided whether a
source was a binary document by reading the source's `capture_type` (`"pdf"`). That field describes how
the crawl layer captures the DOCUMENTS A PAGE LINKS — it is not a statement about the watched page. The
nine ISA page sources are `capture_type: "pdf"` while being HTML pages, so the tool skipped all nine as
"binary - unaffected", never re-derived their baselines, and the first v3.10 sweep flagged every one.
It now delegates to the monitor's OWN predicate (`is_binary_doc`, which sniffs content), because that is
what the monitor actually uses. A tool that touches a monitor's state must never invent its own reading
of a shared field.

COROLLARY, and the reason this was caught at all: "0 genuine pending changes" is a claim about the
page-text world only, and it must be VERIFIED WITH A REAL SWEEP before it is believed. On space-law and
BBNJ this run matched the actual sweeps exactly (0 changed; 6 unchanged plus the 1 genuine change already
identified). On deep-seabed it did not, and only dispatching CI exposed that.

Usage:
    python3 rebaseline_entities.py <repo-dir> --from-ref <ref>            # analysis only (default)
    python3 rebaseline_entities.py <repo-dir> --from-ref <ref> --apply    # write the baselines

`--from-ref` must name a commit whose scripts/watch_sources.py predates the normalisation change; the
tool refuses a ref whose to_text() already unescapes, so it cannot silently "re-derive" against the new
rules twice.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import urllib.request

BINARY_EXT = (".pdf", ".docx", ".doc", ".xlsx", ".zip")
OLD_MODULE = "old_watch_sources"


def load_module(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise SystemExit(f"could not load a module from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def recover_old_monitor(repo: pathlib.Path, ref: str, tmpdir: pathlib.Path):
    """Write the pre-change watch_sources.py from git to a temp file and import it."""
    try:
        src = subprocess.run(["git", "-C", str(repo), "show", f"{ref}:scripts/watch_sources.py"],
                             capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"could not read scripts/watch_sources.py at {ref}: {e.stderr.strip()[:200]}")
    path = tmpdir / f"{OLD_MODULE}.py"
    path.write_text(src, encoding="utf-8")
    return load_module(path, OLD_MODULE)


def fetch(url: str, timeout: int = 40):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 corpus-rebaseline"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


_NEWMOD = None  # the post-change monitor, set in main(); is_binary delegates to its predicate


def is_binary(raw: bytes, url: str) -> bool:
    """Whether the monitor would hash this source as a BYTES document.

    DELEGATES TO THE MONITOR'S OWN PREDICATE. Never use a source's `capture_type` here: it describes
    how the crawl layer captures the documents a page LINKS, not the watched page itself, and reading
    it as "this source is a binary document" caused this tool to skip nine HTML ISA sources as
    "unaffected" (see the docstring).
    """
    if _NEWMOD is not None and hasattr(_NEWMOD, "is_binary_doc"):
        return bool(_NEWMOD.is_binary_doc(raw, ""))
    return raw[:5] == b"%PDF-" or url.lower().split("?")[0].endswith(BINARY_EXT)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Re-derive source baselines after a change to the monitor's comparable text.")
    ap.add_argument("repo", help="path to the corpus repo")
    ap.add_argument("--from-ref", required=True,
                    help="git ref holding the PRE-change scripts/watch_sources.py")
    ap.add_argument("--apply", action="store_true", help="write the re-derived baselines")
    args = ap.parse_args()
    repo = pathlib.Path(args.repo).resolve()

    with tempfile.TemporaryDirectory() as td:
        tmpdir = pathlib.Path(td)
        old = recover_old_monitor(repo, args.from_ref, tmpdir)

        sys.path.insert(0, str(repo / "scripts"))
        newmod = load_module(repo / "scripts" / "watch_sources.py", "new_watch_sources")
        global _NEWMOD
        _NEWMOD = newmod

        # Guard: the old ref must genuinely predate the normalisation change, or the comparison is
        # meaningless (both sides identical -> everything trivially "lossless").
        probe = "<p>a&nbsp;b</p>"
        if old.content_hash(probe) == newmod.content_hash(probe):
            raise SystemExit(
                f"ABORT: {args.from_ref}'s to_text() normalises like the current one, so there is no "
                f"normalisation change to re-derive against. Point --from-ref at a pre-change commit.")

        sp = repo / "monitoring" / "sources.json"
        data = json.loads(sp.read_text(encoding="utf-8"))
        sources = data["sources"] if isinstance(data, dict) and "sources" in data else data

        safe, noop, real, skipped, failed = [], [], [], [], []
        for s in sources:
            name, url = s["name"], s.get("url", "")
            if not url.lower().startswith("http"):
                skipped.append((name, "not an http source"))
                continue
            raw, err = fetch(url)
            if err or raw is None:
                failed.append((name, err or "empty response"))
                continue
            if is_binary(raw, url):
                skipped.append((name, "binary document - hashed as bytes, unaffected"))
                continue

            html = raw.decode("utf-8", "replace")
            ig = s.get("ignore_patterns")
            old_h = old.content_hash(html, ig)
            new_h = newmod.content_hash(html, ig)

            if s.get("schema") or s.get("json_extract"):
                skipped.append((name, "record mode: records unaffected; page hash refreshes on next sweep"))
                continue

            stored = s.get("last_sha256")
            if not stored:
                skipped.append((name, "no stored baseline yet (baselines on the next run)"))
                continue

            same = old.norm_digest(old_h) == old.norm_digest(stored)
            matters = old.norm_digest(new_h) != old.norm_digest(old_h)
            if old.norm_digest(new_h) == old.norm_digest(stored):
                # Already carries a new-normalisation baseline: this source was migrated on an
                # earlier run. Without this check a re-run reports it as "needs triage", because the
                # old-rules hash no longer matches a baseline that is already in the new form.
                noop.append((name, "already re-derived under the new normalisation"))
            elif not same:
                real.append(name)
            elif matters:
                safe.append(name)
                if args.apply:
                    s["last_sha256"] = new_h
            else:
                noop.append((name, "normalisation changes nothing here"))

        print("=" * 96)
        print(f"{repo.name}   [{'APPLIED' if args.apply else 'analysis only'}]   from {args.from_ref}")
        print(f"  lossless re-baseline    : {len(safe)}")
        print(f"  GENUINE pending change  : {len(real)}")
        print(f"  unaffected / no-op      : {len(noop) + len(skipped)}")
        print(f"  fetch failures          : {len(failed)}")
        for label, items in (("lossless", safe), ("NOT re-baselined - needs triage", real)):
            if items:
                print(f"\n  {label}:")
                for n in items:
                    print(f"     {n[:70]}")
        if failed:
            print("\n  fetch failures (the picture is incomplete for these):")
            for n, e in failed:
                print(f"     {n[:60]}  {e}")

        if args.apply:
            if failed:
                print("\n  NOT WRITTEN: resolve the fetch failures first.")
                return 1
            sp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"\n  wrote {sp}")
            print("  VERIFY WITH A REAL SWEEP - see the coverage gap in this file's docstring.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
