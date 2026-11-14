"""Shared loader and helpers for data/signals.yaml.

The YAML file is the single source of truth of this repository. The DBC file
and the pages under docs/messages/ are generated from it.
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "signals.yaml"

STATUSES = ("confirmed", "hypothesis", "unknown", "ruled_out")
CONFIDENCES = ("high", "medium", "low")


def load(path: Path = DATA) -> dict:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def bit_span(addr: dict) -> tuple[int, int]:
    """Return (first_bit, bit_length) of a signal, counted MSB-first.

    Bit 0 here is the most significant bit of byte 0, bit 8 the most
    significant bit of byte 1. This is only used for overlap checks and
    for drawing layouts; it is not the DBC start bit.
    """
    byte = addr["byte"]
    if "bit" in addr:
        length = addr.get("bit_len", 1)
        msb = addr["bit"] + length - 1          # bit number inside the byte, 7 = MSB
        return byte * 8 + (7 - msb), length
    return byte * 8, addr.get("len", 1) * 8


def bit_length(addr: dict) -> int:
    return bit_span(addr)[1]


def is_little(addr: dict) -> bool:
    return addr.get("endian", "big") == "little"


def dbc_start_bit(addr: dict) -> int:
    """DBC start bit. Big-endian signals start at their MSB, little-endian at their LSB."""
    byte = addr["byte"]
    if "bit" in addr:
        length = addr.get("bit_len", 1)
        return byte * 8 + addr["bit"] + length - 1   # MSB, big-endian within one byte
    if is_little(addr):
        return byte * 8
    return byte * 8 + 7


def addr_text(addr: dict) -> str:
    """Human-readable address: 'B0:B1', 'B3 bits 7..5', 'B4 bit 0'."""
    byte = addr["byte"]
    if "bit" in addr:
        length = addr.get("bit_len", 1)
        if length == 1:
            return f"B{byte} bit {addr['bit']}"
        return f"B{byte} bits {addr['bit'] + length - 1}..{addr['bit']}"
    n = addr.get("len", 1)
    if n == 1:
        return f"B{byte}"
    return f"B{byte}:B{byte + n - 1}"


def type_text(addr: dict) -> str:
    if "bit" in addr:
        n = addr.get("bit_len", 1)
        return "flag" if n == 1 else f"{n}-bit field"
    n = addr.get("len", 1) * 8
    sign = "int" if addr.get("signed") else "uint"
    if n == 8:
        return f"{sign}8"
    return f"{sign}{n} {'LE' if is_little(addr) else 'BE'}"


def raw_value(addr: dict, data: bytes) -> int:
    """Extract the raw integer of a signal from frame data."""
    byte = addr["byte"]
    if "bit" in addr:
        length = addr.get("bit_len", 1)
        return (data[byte] >> addr["bit"]) & ((1 << length) - 1)
    n = addr.get("len", 1)
    chunk = data[byte:byte + n]
    return int.from_bytes(chunk, "little" if is_little(addr) else "big",
                          signed=bool(addr.get("signed")))


def physical(sig: dict, data: bytes) -> float | int:
    raw = raw_value(sig["addr"], data)
    if "scale" not in sig and "offset" not in sig:
        return raw
    return raw * sig.get("scale", 1) + sig.get("offset", 0)


def parse_frame(text: str) -> bytes:
    return bytes(int(b, 16) for b in text.split())


def can_id_text(can_id: int) -> str:
    return f"0x{can_id:03X}"


def validate(db: dict) -> list[str]:
    """Return a list of problems found in the data file (empty = fine)."""
    errors: list[str] = []
    for can_id, msg in db["messages"].items():
        tag = can_id_text(can_id)
        if not isinstance(can_id, int) or not 0 <= can_id <= 0x7FF:
            errors.append(f"{tag}: not an 11-bit CAN id")
        for key in ("name", "dlc", "status", "summary"):
            if key not in msg:
                errors.append(f"{tag}: missing '{key}'")
        if msg.get("status") not in STATUSES:
            errors.append(f"{tag}: bad status {msg.get('status')!r}")
        taken: dict[int, str] = {}
        names: set[str] = set()
        for sig in msg.get("signals", []):
            name = sig.get("name", "?")
            where = f"{tag}.{name}"
            if name in names:
                errors.append(f"{where}: duplicate signal name")
            names.add(name)
            if sig.get("status") not in STATUSES:
                errors.append(f"{where}: bad status {sig.get('status')!r}")
            if sig.get("status") in ("confirmed", "hypothesis") and \
                    sig.get("confidence") not in CONFIDENCES:
                errors.append(f"{where}: needs confidence high/medium/low")
            if "description" not in sig:
                errors.append(f"{where}: missing description")
            if sig.get("status") == "confirmed":
                for key in ("confirmed_by", "evidence"):
                    if not sig.get(key):
                        errors.append(f"{where}: confirmed signals must state '{key}'")
            first, length = bit_span(sig["addr"])
            if first + length > msg.get("dlc", 8) * 8:
                errors.append(f"{where}: runs past DLC")
            if sig.get("dbc", True):
                for bit in range(first, first + length):
                    if bit in taken:
                        errors.append(f"{where}: overlaps {taken[bit]} "
                                      f"(set 'dbc: false' on the alias)")
                        break
                    taken[bit] = name
            example = sig.get("example")
            if example:
                data = parse_frame(example["frame"])
                if len(data) != msg.get("dlc"):
                    errors.append(f"{where}: example frame length != DLC")
                else:
                    got = physical(sig, data)
                    want = example["value"]
                    # half a raw count, or the rounding of a value written with one decimal
                    tol = max(abs(sig.get("scale", 1)) * 0.51, 0.051)
                    if abs(got - want) > tol:
                        errors.append(f"{where}: example decodes to {got:g}, file says {want}")
    return errors
