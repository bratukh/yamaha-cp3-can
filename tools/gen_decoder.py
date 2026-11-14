#!/usr/bin/env python3
"""Generate decoder/cp3_table.py from data/signals.yaml.

Usage:
    python3 tools/gen_decoder.py            # write the file
    python3 tools/gen_decoder.py --check    # exit 1 if the file on disk is stale

The table holds every message and every signal of the data file (including
unknown ones and aliases), as plain Python literals, so that decoder/cp3can.py
needs nothing but the standard library.
"""
from __future__ import annotations

import sys

import cp3data as d

OUT = d.ROOT / "decoder" / "cp3_table.py"

HEADER = '''\
# GENERATED from data/signals.yaml by tools/gen_decoder.py. Do not edit by hand.
#
# MESSAGES maps a CAN id to {"name", "dlc", "signals"}. Each signal is a dict:
#   name, byte, bit (None for whole bytes, else the least significant bit),
#   nbits, endian ("big" or "little"), signed, scale, offset, unit, values
#   (raw -> label, or None), status, alias (True if it reuses the bits of
#   another signal).
# physical value = raw * scale + offset.
'''


def _signal(sig: dict) -> dict:
    addr = sig["addr"]
    return {
        "name": sig["name"],
        "byte": addr["byte"],
        "bit": addr.get("bit"),
        "nbits": d.bit_length(addr),
        "endian": "little" if d.is_little(addr) else "big",
        "signed": bool(addr.get("signed")),
        "scale": sig.get("scale", 1),
        "offset": sig.get("offset", 0),
        "unit": sig.get("unit", ""),
        "values": dict(sig["values"]) if sig.get("values") else None,
        "status": sig["status"],
        "alias": not sig.get("dbc", True),
    }


def build(db: dict) -> str:
    out = [HEADER, "MESSAGES = {\n"]
    for can_id in sorted(db["messages"]):
        msg = db["messages"][can_id]
        out.append(f"    0x{can_id:03X}: {{\n")
        out.append(f"        \"name\": {msg['name']!r},\n")
        out.append(f"        \"dlc\": {msg['dlc']},\n")
        out.append("        \"signals\": [\n")
        for sig in msg.get("signals", []):
            out.append(f"            {_signal(sig)!r},\n")
        out.append("        ],\n")
        out.append("    },\n")
    out.append("}\n")
    return "".join(out)


def main() -> int:
    db = d.load()
    errors = d.validate(db)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    text = build(db)
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print(f"{OUT.relative_to(d.ROOT)} is stale: run tools/gen_decoder.py",
                  file=sys.stderr)
            return 1
        return 0
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(d.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
