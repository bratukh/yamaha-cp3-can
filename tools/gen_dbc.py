#!/usr/bin/env python3
"""Generate dbc/yamaha_cp3_2021-2024.dbc from data/signals.yaml.

Usage:
    python3 tools/gen_dbc.py            # write the file
    python3 tools/gen_dbc.py --check    # exit 1 if the file on disk is stale

Only signals with status 'confirmed' or 'hypothesis' are exported. Signals
flagged 'dbc: false' in the data file (aliases that reuse the bits of another
signal, such as a static lean angle computed from an accelerometer word) are
left out, because a DBC cannot hold overlapping signals. Derived quantities
that need more than one frame (lean angle from yaw rate and speed) are not
expressible in DBC at all; see docs/lean-reconstruction.md.
"""
from __future__ import annotations

import sys

import cp3data as d

OUT = d.ROOT / "dbc" / "yamaha_cp3_2021-2024.dbc"
EXPORT = ("confirmed", "hypothesis")


def _num(x: float) -> str:
    return f"{x:.10g}"


_ASCII = {"×": "x", "−": "-", "–": "-", "—": "-", "°": " deg", "≈": "~", "±": "+/-",
          "é": "e", "…": "...", "’": "'", "“": "'", "”": "'"}


def _quote(text: str) -> str:
    """One line, no double quotes, plain ASCII (DBC tools disagree on encodings)."""
    text = " ".join(str(text).split()).replace('"', "'")
    for src, dst in _ASCII.items():
        text = text.replace(src, dst)
    return text.encode("ascii", "replace").decode("ascii")


def _unit(sig: dict) -> str:
    unit = sig.get("unit", "")
    return "" if unit in ("raw", "gear") else _quote(unit)


def build(db: dict) -> str:
    meta = db["meta"]
    out: list[str] = []
    out.append(f'VERSION "{meta["version"]}"')
    out.append("")
    out.append("NS_ :")
    out.append("")
    out.append("BS_:")
    out.append("")
    out.append("BU_: BIKE LOGGER")
    out.append("")

    comments: list[str] = []
    values: list[str] = []
    status_attr: list[str] = []
    cycle_attr: list[str] = []

    for can_id in sorted(db["messages"]):
        msg = db["messages"][can_id]
        out.append(f'BO_ {can_id} {msg["name"].upper()}: {msg["dlc"]} BIKE')
        comments.append(f'CM_ BO_ {can_id} "{_quote(msg["summary"])}";')
        status_attr.append(f'BA_ "Status" BO_ {can_id} "{msg["status"]}";')
        if msg.get("rate_hz"):
            cycle = round(1000 / msg["rate_hz"])
            cycle_attr.append(f'BA_ "GenMsgCycleTime" BO_ {can_id} {cycle};')
        for sig in msg.get("signals", []):
            if sig["status"] not in EXPORT or not sig.get("dbc", True) \
                    or sig["name"].startswith("reserved"):
                continue
            addr = sig["addr"]
            name = sig["name"].upper()
            order = 1 if d.is_little(addr) else 0
            sign = "-" if addr.get("signed") else "+"
            length = d.bit_length(addr)
            scale = sig.get("scale", 1)
            offset = sig.get("offset", 0)
            raw_max = max(sig["values"]) if sig.get("values") else (1 << length) - 1
            lo = sig.get("min", min(offset, raw_max * scale + offset))
            hi = sig.get("max", max(offset, raw_max * scale + offset))
            out.append(
                f' SG_ {name} : {d.dbc_start_bit(addr)}|{length}@{order}{sign} '
                f'({_num(scale)},{_num(offset)}) [{_num(lo)}|{_num(hi)}] '
                f'"{_unit(sig)}" LOGGER')
            note = f'[{sig["status"]}/{sig.get("confidence", "-")}] {sig["description"]}'
            comments.append(f'CM_ SG_ {can_id} {name} "{_quote(note)}";')
            status_attr.append(f'BA_ "Status" SG_ {can_id} {name} "{sig["status"]}";')
            if sig.get("values"):
                pairs = " ".join(f'{k} "{_quote(v)}"'
                                 for k, v in sorted(sig["values"].items(), reverse=True))
                values.append(f"VAL_ {can_id} {name} {pairs} ;")
        out.append("")

    out.append(f'CM_ "{_quote(meta["dbc_comment"])}";')
    out.extend(comments)
    out.append("")
    out.append('BA_DEF_ BO_ "GenMsgCycleTime" INT 0 65535;')
    out.append('BA_DEF_ BO_ "Status" STRING ;')
    out.append('BA_DEF_ SG_ "Status" STRING ;')
    out.append('BA_DEF_DEF_ "GenMsgCycleTime" 0;')
    out.append('BA_DEF_DEF_ "Status" "unknown";')
    out.extend(cycle_attr)
    out.extend(status_attr)
    out.append("")
    out.extend(values)
    out.append("")
    return "\n".join(out)


def main() -> int:
    db = d.load()
    errors = d.validate(db)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    text = build(db)
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print(f"{OUT.relative_to(d.ROOT)} is stale: run tools/gen_dbc.py", file=sys.stderr)
            return 1
        return 0
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(d.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
