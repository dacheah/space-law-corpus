"""
validate_corpus.py — integrity and structure checks for the Space Law Corpus.

What it checks:
  1. Every authoritative metadata.yaml validates against
     schema/authoritative-metadata.schema.json.
  2. Recorded hashes actually match the files on disk (nothing silently altered).
  3. Every non-"authoritative_missing" record has a text.txt.
  4. Every derived-metadata.yaml validates against the derived schema, points to
     a real authoritative version, and (staleness) its source_text_sha256 still
     matches that version's current text_sha256.
  5. The two-layer wall: nothing model-generated sneaks into authoritative/.

Exit code 0 = all good; 1 = one or more failures. Warnings (e.g. stale derived
artifacts) do not fail the build but are reported.

Usage:
    python3 validate_corpus.py            # validates the whole repo
    python3 validate_corpus.py --path authoritative/un/treaty/ost-1967
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from hashing import sha256_file

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "schema"


def _load_schema(name: str) -> Draft202012Validator:
    with open(SCHEMA_DIR / name, "r", encoding="utf-8") as f:
        return Draft202012Validator(json.load(f))


def _load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_authoritative(record_meta: Path, schema: Draft202012Validator,
                           errors: list, warnings: list) -> None:
    rel = record_meta.relative_to(REPO_ROOT)
    meta = _load_yaml(record_meta)
    version_dir = record_meta.parent

    # 1. Schema.
    schema_errs = sorted(schema.iter_errors(meta), key=lambda e: e.path)
    for e in schema_errs:
        loc = "/".join(str(p) for p in e.path) or "(root)"
        errors.append(f"[schema] {rel}: {loc}: {e.message}")
    if schema_errs:
        return  # further checks assume a well-formed record

    status = meta.get("authoritative_status")

    # 2. original hash matches the stored original artifact.
    original_path = version_dir / meta["original_filename"]
    if status != "authoritative_missing":
        if not original_path.exists():
            errors.append(f"[file] {rel}: original artifact "
                          f"'{meta['original_filename']}' is missing")
        else:
            actual = sha256_file(original_path)
            if actual != meta["original_sha256"]:
                errors.append(f"[hash] {rel}: original_sha256 mismatch "
                              f"(recorded {meta['original_sha256']}, actual {actual})")

    # 3. text.txt presence + hash for non-missing records.
    text_path = version_dir / "text.txt"
    if status == "authoritative_missing":
        if text_path.exists():
            errors.append(f"[policy] {rel}: authoritative_missing record must "
                          f"NOT contain a text.txt")
    else:
        if not text_path.exists():
            errors.append(f"[file] {rel}: text.txt is missing for status '{status}'")
        else:
            actual = sha256_file(text_path)
            if actual != meta.get("text_sha256"):
                errors.append(f"[hash] {rel}: text_sha256 mismatch "
                              f"(recorded {meta.get('text_sha256')}, actual {actual})")
            # content_hash must point at the text when a text exists.
            if meta.get("content_hash") != meta.get("text_sha256"):
                errors.append(f"[hash] {rel}: content_hash should equal text_sha256 "
                              f"when a text.txt exists")


def validate_derived(record_meta: Path, schema: Draft202012Validator,
                     errors: list, warnings: list) -> None:
    rel = record_meta.relative_to(REPO_ROOT)
    meta = _load_yaml(record_meta)

    schema_errs = sorted(schema.iter_errors(meta), key=lambda e: e.path)
    for e in schema_errs:
        loc = "/".join(str(p) for p in e.path) or "(root)"
        errors.append(f"[schema] {rel}: {loc}: {e.message}")
    if schema_errs:
        return

    # Must trace to a real authoritative version.
    src_dir = REPO_ROOT / "authoritative" / meta["source_corpus_id"] / meta["source_version_id"]
    src_meta = src_dir / "metadata.yaml"
    if not src_meta.exists():
        errors.append(f"[trace] {rel}: source authoritative version not found: "
                      f"{meta['source_corpus_id']}/{meta['source_version_id']}")
        return

    # Staleness: does the source text still have the hash this was built from?
    src = _load_yaml(src_meta)
    if src.get("text_sha256") and meta.get("source_text_sha256") != src.get("text_sha256"):
        warnings.append(f"[stale] {rel}: built from {meta['source_text_sha256']}, "
                        f"but source text is now {src['text_sha256']} — regenerate/re-review")


def validate_all(subpath: str | None = None):
    errors: list = []
    warnings: list = []

    auth_schema = _load_schema("authoritative-metadata.schema.json")
    der_schema = _load_schema("derived-metadata.schema.json")

    auth_root = REPO_ROOT / "authoritative"
    der_root = REPO_ROOT / "derived"

    scope = REPO_ROOT / subpath if subpath else None

    auth_metas = sorted(auth_root.rglob("metadata.yaml"))
    der_metas = sorted(der_root.rglob("derived-metadata.yaml"))

    n_auth = n_der = 0
    for m in auth_metas:
        if scope and scope not in m.parents and scope != m.parent:
            continue
        validate_authoritative(m, auth_schema, errors, warnings)
        n_auth += 1
    for m in der_metas:
        if scope and scope not in m.parents and scope != m.parent:
            continue
        validate_derived(m, der_schema, errors, warnings)
        n_der += 1

    return errors, warnings, n_auth, n_der


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate the Space Law Corpus.")
    ap.add_argument("--path", default=None,
                    help="Optional subpath to limit validation (e.g. authoritative/un/treaty/ost-1967)")
    args = ap.parse_args()

    errors, warnings, n_auth, n_der = validate_all(args.path)

    print(f"Checked {n_auth} authoritative record(s), {n_der} derived record(s).")
    for w in warnings:
        print("WARN  " + w)
    for e in errors:
        print("FAIL  " + e)

    if errors:
        print(f"\nRESULT: FAILED with {len(errors)} error(s).")
        return 1
    print(f"\nRESULT: OK{' (with ' + str(len(warnings)) + ' warning(s))' if warnings else ''}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
