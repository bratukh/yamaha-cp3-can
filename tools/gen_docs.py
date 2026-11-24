#!/usr/bin/env python3
"""Generate docs/signals.md, docs/messages/0xNNN.md, docs/open-questions.md and the
"All signals at a glance" block of README.md from data/signals.yaml.

Usage:
    python3 tools/gen_docs.py            # write the files
    python3 tools/gen_docs.py --check    # exit 1 if any file on disk is stale
"""
from __future__ import annotations

import sys

import cp3data as d

DOCS = d.ROOT / "docs"
MARK = {"confirmed": "confirmed", "hypothesis": "hypothesis",
        "unknown": "unknown", "ruled_out": "ruled out"}
HEADER = ("<!-- GENERATED from data/signals.yaml by tools/gen_docs.py. "
          "Do not edit by hand. -->\n")


def _status(item: dict) -> str:
    text = MARK[item["status"]]
    if item.get("confidence") and item["status"] in ("confirmed", "hypothesis"):
        text += f" ({item['confidence']})"
    return text


def _formula(sig: dict) -> str:
    if sig.get("values"):
        return "enum"
    scale, offset = sig.get("scale"), sig.get("offset", 0)
    if scale is None and not offset:
        return "raw"
    text = "raw" if scale in (None, 1) else f"raw × {scale:.10g}"
    if offset:
        text += f" {'+' if offset > 0 else '−'} {abs(offset):.10g}"
    return text


def _cell(text) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def _layout(msg: dict) -> str:
    """One row per byte, naming the signals that live in it."""
    rows = ["| Byte | Content |", "|---|---|"]
    for byte in range(msg["dlc"]):
        names = [s["name"] for s in msg.get("signals", [])
                 if s.get("dbc", True)
                 and d.bit_span(s["addr"])[0] // 8 <= byte
                 <= (sum(d.bit_span(s["addr"])) - 1) // 8]
        rows.append(f"| B{byte} | {', '.join(f'`{n}`' for n in names) or '—'} |")
    return "\n".join(rows)


def message_page(can_id: int, msg: dict) -> str:
    tag = d.can_id_text(can_id)
    out = [HEADER, f"# {tag} — `{msg['name']}`", ""]
    rate = f"{msg['rate_hz']} Hz" if msg.get("rate_hz") else "rate not measured"
    out.append(f"DLC {msg['dlc']} · {rate} · status: **{_status(msg)}**")
    out += ["", msg["summary"].strip(), ""]
    out += ["## Layout", "", "Bytes are numbered from 0. Multi-byte values are big-endian "
            "unless a row says otherwise. Bit 7 is the most significant bit of a byte.",
            "", _layout(msg), ""]
    signals = msg.get("signals", [])
    if signals:
        out += ["## Signals", "",
                "| Signal | Where | Type | Value | Unit | Status |", "|---|---|---|---|---|---|"]
        for s in signals:
            out.append(f"| `{s['name']}` | {d.addr_text(s['addr'])} | {d.type_text(s['addr'])} "
                       f"| {_formula(s)} | {s.get('unit', '')} | {_status(s)} |")
        out.append("")
        for s in signals:
            out += [f"### `{s['name']}`", "", s["description"].strip(), ""]
            if s.get("values"):
                out += ["| Raw | Meaning |", "|---|---|"]
                out += [f"| {k} | {_cell(v)} |" for k, v in sorted(s["values"].items())]
                out.append("")
            if s.get("confirmed_by"):
                out += [f"**Confirmed by:** {s['confirmed_by'].strip()}.", ""]
            if s.get("evidence"):
                out += [f"**How we know:** {s['evidence'].strip()}", ""]
            if s.get("caveats"):
                out += [f"**Caveats:** {s['caveats'].strip()}", ""]
            if s.get("example"):
                ex = s["example"]
                out += [f"**Example:** `{tag}  {ex['frame']}` → {ex['value']} "
                        f"{s.get('unit', '')}".rstrip(), ""]
    for der in msg.get("derived", []):
        out += [f"### Derived: `{der['name']}`", "", f"`{der['formula']}` "
                f"({der.get('unit', '')}) — {_status(der)}", "", der["description"].strip(), ""]
        if der.get("confirmed_by"):
            out += [f"**Confirmed by:** {der['confirmed_by'].strip()}.", ""]
        if der.get("evidence"):
            out += [f"**How we know:** {der['evidence'].strip()}", ""]
    for note in msg.get("notes", []):
        out += [f"> {note.strip()}", ""]
    return "\n".join(out).rstrip() + "\n"


def signals_page(db: dict) -> str:
    out = [HEADER, "# All signals", "",
           "One row per signal. The last column says what a confirmed signal was checked "
           "against; where it reads 'Copy of' or 'nothing outside the bus', it is known only "
           "by agreement with another field. Follow the ID link for the description, the numbers "
           "and an example frame. Status meanings are in the [README](../README.md#status).", "",
           "## Broadcast frames", "",
           "| ID | Hz | Signal | Where | Value | Unit | Status | Confirmed by |",
           "|---|---|---|---|---|---|---|---|"]
    for can_id in sorted(db["messages"]):
        msg = db["messages"][can_id]
        tag = d.can_id_text(can_id)
        link = f"[{tag}](messages/{tag}.md)"
        signals = msg.get("signals", [])
        if not signals:
            out.append(f"| {link} | {msg.get('rate_hz', '')} | — | | | | {_status(msg)} | |")
        for s in signals:
            out.append(f"| {link} | {msg.get('rate_hz', '')} | `{s['name']}` | "
                       f"{d.addr_text(s['addr'])} | {_formula(s)} | {s.get('unit', '')} "
                       f"| {_status(s)} | {_cell(s.get('confirmed_by', ''))} |")
        for der in msg.get("derived", []):
            out.append(f"| {link} | | `{der['name']}` (derived) | | `{_cell(der['formula'])}` "
                       f"| {der.get('unit', '')} | {_status(der)} "
                       f"| {_cell(der.get('confirmed_by', ''))} |")
    obd = db.get("obd2", {})
    if obd.get("pids"):
        out += ["", "## OBD-II mode 01", "", "Details in [obd2.md](obd2.md).", "",
                "| PID | Name | Unit | Status | Example response data → value |",
                "|---|---|---|---|---|"]
        for p in obd["pids"]:
            ex = p.get("example")
            ex_text = f"`{ex['data']}` → {ex['value']}" if ex else ""
            out.append(f"| 0x{p['pid']:02X} | {p['name']} | {p.get('unit', '')} "
                       f"| {_status(p)} | {ex_text} |")
    uds = db.get("uds", {})
    if uds.get("dids"):
        out += ["", "## UDS data identifiers (read-only)", "", "Details in [uds.md](uds.md).", "",
                "| ECU | DID | Name | Status | Note |", "|---|---|---|---|---|"]
        for x in uds["dids"]:
            out.append(f"| 0x{x['ecu']:03X} | 0x{x['did']:04X} | {x['name']} | {_status(x)} "
                       f"| {_cell(x.get('note', ''))} |")
    return "\n".join(out).rstrip() + "\n"


def open_questions_page(db: dict) -> str:
    out = [HEADER, "# Open questions", "",
           "What we do not know yet. A capture that settles any of these is the most "
           "useful contribution you can make; see [CONTRIBUTING](../CONTRIBUTING.md).", ""]
    for q in db.get("open_questions", []):
        out += [f"## {q['title']}", "", q["text"].strip(), ""]
        if q.get("how_to_close"):
            out += [f"**What would settle it:** {q['how_to_close'].strip()}", ""]
    out += ["## Signals that are not confirmed", "",
            "| ID | Signal | Where | Status | What is known |", "|---|---|---|---|---|"]
    for can_id in sorted(db["messages"]):
        msg = db["messages"][can_id]
        tag = d.can_id_text(can_id)
        for s in msg.get("signals", []):
            if s["status"] == "confirmed":
                continue
            first = s["description"].strip().split(". ")[0].rstrip(".") + "."
            out.append(f"| [{tag}](messages/{tag}.md) | `{s['name']}` | {d.addr_text(s['addr'])} "
                       f"| {_status(s)} | {_cell(first)} |")
    return "\n".join(out).rstrip() + "\n"


README_BEGIN = "<!-- BEGIN GENERATED: signals at a glance (tools/gen_docs.py) -->"
README_END = "<!-- END GENERATED: signals at a glance -->"


def _values_text(sig: dict, limit: int = 90) -> str:
    """Compact enum map for the README: '0 = neutral, 1 = 1st, ...'."""
    parts = [f"{k} = {v}" for k, v in sig["values"].items()]
    text = ", ".join(parts)
    return text if len(text) <= limit else text[:limit].rsplit(", ", 1)[0] + ", …"


def readme_block(db: dict) -> str:
    """Every confirmed or hypothesis signal in one table, so the README alone is enough."""
    out = [README_BEGIN, "<details>",
           "<summary>Bytes and formulas for every confirmed and hypothesis signal</summary>", "",
           "| ID | Hz | Where | Signal | Value | Unit | Status |",
           "|---|---|---|---|---|---|---|"]
    for can_id in sorted(db["messages"]):
        msg = db["messages"][can_id]
        tag = d.can_id_text(can_id)
        link = f"[{tag}](docs/messages/{tag}.md)"
        for s in msg.get("signals", []):
            if s["status"] not in ("confirmed", "hypothesis"):
                continue
            value = _values_text(s) if s.get("values") else _formula(s)
            out.append(f"| {link} | {msg.get('rate_hz', '')} | {d.addr_text(s['addr'])} "
                       f"| `{s['name']}` | {_cell(value)} | {s.get('unit', '')} | {_status(s)} |")
        for der in msg.get("derived", []):
            if der["status"] not in ("confirmed", "hypothesis"):
                continue
            out.append(f"| {link} | | derived | `{der['name']}` | `{_cell(der['formula'])}` "
                       f"| {der.get('unit', '')} | {_status(der)} |")
    out += ["", "</details>", README_END]
    return "\n".join(out)


def readme_text(db: dict) -> str:
    text = (d.ROOT / "README.md").read_text(encoding="utf-8")
    head, rest = text.split(README_BEGIN, 1)
    _, tail = rest.split(README_END, 1)
    return head + readme_block(db) + tail


def build(db: dict) -> dict:
    files = {DOCS / "signals.md": signals_page(db),
             DOCS / "open-questions.md": open_questions_page(db),
             d.ROOT / "README.md": readme_text(db)}
    for can_id, msg in db["messages"].items():
        files[DOCS / "messages" / f"{d.can_id_text(can_id)}.md"] = message_page(can_id, msg)
    return files


def main() -> int:
    db = d.load()
    errors = d.validate(db)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    files = build(db)
    if "--check" in sys.argv:
        stale = [p for p, text in files.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != text]
        extra = [p for p in (DOCS / "messages").glob("0x*.md") if p not in files]
        for p in stale + extra:
            print(f"{p.relative_to(d.ROOT)} is stale: run tools/gen_docs.py", file=sys.stderr)
        return 1 if stale or extra else 0
    (DOCS / "messages").mkdir(parents=True, exist_ok=True)
    for path, text in files.items():
        path.write_text(text, encoding="utf-8")
    print(f"wrote {len(files)} files (docs/ and the README block)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
