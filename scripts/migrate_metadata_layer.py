#!/usr/bin/env python3
"""Metadata-layer migration (pilot: Space Law Corpus).

Adds three authoritative fields to every record and normalises jurisdiction:
  * binding_force            (required)  from document_type
  * issuing_authority        (required)  UNGA / COPUOS / national legislature
  * administering_authority  (optional)  national administering body, else null
  * jurisdiction 'international/UN' -> 'international'  (the '/UN' issuer now
    lives in issuing_authority; tier is DERIVED from jurisdiction downstream)

Metadata-only: never touches text or content/original/text hashes. Idempotent.
"""
from __future__ import annotations
import glob, json, os, re
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = os.path.join(ROOT, "schema", "authoritative-metadata.schema.json")

BINDING = {"treaty": "binding", "national_legislation": "binding",
           "ga_resolution": "non_binding", "soft_law_guideline": "non_binding",
           "arbitration_rules": "non_binding"}
ISSUER_BY_TYPE = {"treaty": "United Nations General Assembly",
                  "ga_resolution": "United Nations General Assembly",
                  "soft_law_guideline": "United Nations Committee on the Peaceful Uses of Outer Space (COPUOS)"}
ISSUER_BY_JUR = {"FRA": "Parliament of France",
                 "LUX": "Chamber of Deputies of Luxembourg",
                 "USA": "United States Congress"}
ADMIN_BY_JUR = {"FRA": "Minister responsible for space activities (France)",
                "LUX": "Ministry of the Economy (Luxembourg)"}


def patch_schema():
    txt = open(SCHEMA, encoding="utf-8").read()
    if "binding_force" in txt:
        print("schema: already patched"); return
    txt = txt.replace('    "provenance_note"\n  ],',
                      '    "provenance_note",\n    "binding_force",\n    "issuing_authority"\n  ],', 1)
    anchor = ('    "document_type": {\n      "type": "string",\n      "enum": [\n'
              '        "treaty",\n        "ga_resolution",\n        "national_legislation",\n'
              '        "soft_law_guideline",\n        "arbitration_rules"\n      ]\n    },\n')
    if anchor not in txt:
        raise SystemExit("schema anchor (document_type) not found; aborting")
    add = (anchor +
      '    "binding_force": {\n      "type": "string",\n      "enum": [\n        "binding",\n        "non_binding"\n      ],\n'
      '      "description": "Legal force of the instrument on its own accord: binding (imposes legal obligations enforceable in some legal order) or non_binding (recommendatory soft law, no obligation until adopted by a binding instrument). Orthogonal to authoritative_status. Instrument tier is DERIVED from jurisdiction downstream."\n    },\n'
      '    "issuing_authority": {\n      "type": "string",\n'
      '      "description": "Body that made/adopted the instrument (e.g. United Nations General Assembly, United States Congress). Distinct from source_publisher (where the text was obtained)."\n    },\n'
      '    "administering_authority": {\n      "type": [\n        "string",\n        "null"\n      ],\n'
      '      "description": "Body that administers/enforces the instrument where different from the issuer; null if not applicable."\n    },\n')
    txt = txt.replace(anchor, add, 1)
    json.loads(txt)  # must remain valid JSON
    open(SCHEMA, "w", encoding="utf-8").write(txt)
    print("schema: patched")


def yq(v):
    return '"' + v.replace('\\', '\\\\').replace('"', '\\"') + '"'


def backfill():
    changed = skipped = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "authoritative", "**", "metadata.yaml"), recursive=True)):
        raw = open(f, encoding="utf-8").read()
        d = yaml.safe_load(raw)
        if "binding_force" in d and "issuing_authority" in d:
            skipped += 1; continue
        dt, ju = d.get("document_type"), d.get("jurisdiction")
        bf = BINDING.get(dt)
        if dt == "national_legislation":
            issuer, admin = ISSUER_BY_JUR.get(ju), ADMIN_BY_JUR.get(ju)
        else:
            issuer, admin = ISSUER_BY_TYPE.get(dt), None
        if not bf or not issuer:
            raise SystemExit(f"no mapping for {dt}/{ju} in {f}")
        new = re.sub(r'(?m)^(jurisdiction:[ \t]*)([\'"]?)international/UN\2[ \t]*$', r'\1international', raw)
        if not new.endswith("\n"):
            new += "\n"
        new += f"binding_force: {bf}\n"
        new += f"issuing_authority: {yq(issuer)}\n"
        new += f"administering_authority: {yq(admin) if admin else 'null'}\n"
        d2 = yaml.safe_load(new)  # must re-parse
        assert d2["binding_force"] == bf and d2["issuing_authority"] == issuer
        assert d2["jurisdiction"] in ("international", "FRA", "LUX", "USA"), d2["jurisdiction"]
        open(f, "w", encoding="utf-8").write(new)
        changed += 1
        print(f"  {d.get('corpus_id'):40} {dt:20} {ju:16}-> {d2['jurisdiction']:13} | {bf:11} | {issuer}")
    print(f"backfill: {changed} changed, {skipped} already done")


if __name__ == "__main__":
    patch_schema()
    backfill()
