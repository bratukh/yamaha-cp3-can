import re
import subprocess
import sys
from pathlib import Path

import cantools
import pytest

import cp3can
import cp3data as d

ROOT = Path(__file__).resolve().parent.parent
DB = d.load()


def examples():
    for can_id, msg in DB["messages"].items():
        for sig in msg.get("signals", []):
            if sig.get("example"):
                yield can_id, sig, d.parse_frame(sig["example"]["frame"])


def tol(sig):
    return max(abs(sig.get("scale", 1)) * 0.51, 0.051)


def test_validate():
    assert d.validate(DB) == []


@pytest.mark.parametrize("can_id,sig,data", list(examples()),
                         ids=lambda v: v["name"] if isinstance(v, dict) else None)
def test_example_decodes(can_id, sig, data):
    got = cp3can.decode(can_id, data)[sig["name"]]
    assert abs(got - sig["example"]["value"]) <= tol(sig)


def test_decode_edge_cases():
    assert cp3can.decode(0x7FF, b"\0" * 8) == {}
    assert cp3can.decode(0x205, b"") == {}
    short = cp3can.decode(0x205, bytes.fromhex("2B212B78"))
    assert "wheel_speed_front" in short and "wheel_speed_rear" in short
    assert len(short) < len(cp3can.decode(0x205, bytes(8)))


def test_lean_angle():
    assert cp3can.lean_angle_deg(0, 100) == 0
    assert cp3can.lean_angle_deg(5, 90) > 0 > cp3can.lean_angle_deg(-5, 90)


def test_state():
    st = cp3can.State()
    st.update(0x205, bytes.fromhex("2B212B7800040000"))
    st.update(0x254, bytes.fromhex("74A8740276 30D8D8".replace(" ", "")))
    assert "wheel_slip" in st.values and "lean_angle" in st.values


def test_dbc_matches_decoder():
    dbc = cantools.database.load_file(ROOT / "dbc" / "yamaha_cp3_2021-2024.dbc",
                                      strict=True)
    checked = 0
    for can_id, sig, data in examples():
        if not sig.get("dbc", True) or sig["status"] not in ("confirmed", "hypothesis"):
            continue
        message = dbc.get_message_by_frame_id(can_id)
        want = cp3can.decode(can_id, data)
        got = message.decode(data, decode_choices=False, scaling=True)
        name = sig["name"].upper()
        assert name in got, name
        assert abs(float(got[name]) - want[sig["name"]]) < 1e-9, name
        checked += 1
    assert checked > 10


@pytest.mark.parametrize("script", ["gen_dbc.py", "gen_docs.py", "gen_decoder.py"])
def test_generators_fresh(script):
    r = subprocess.run([sys.executable, str(ROOT / "tools" / script), "--check"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def tree_files():
    for p in ROOT.rglob("*"):
        parts = set(p.relative_to(ROOT).parts)
        if p.is_file() and not parts & {".git", ".venv", "__pycache__", ".pytest_cache"}:
            yield p


FORBIDDEN = ["/" + "Users/", "/" + "home/", "@" + "gmail", "@" + "yahoo", "@" + "outlook"]
THIS = Path(__file__).resolve()


def test_hygiene():
    cyr = re.compile("[" + chr(0x400) + "-" + chr(0x4FF) + "]")
    bad = []
    for p in tree_files():
        if p.name == ".DS_Store":
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if cyr.search(text):
            bad.append(f"{p.relative_to(ROOT)}: Cyrillic")
        if p != THIS:
            bad += [f"{p.relative_to(ROOT)}: {s!r}" for s in FORBIDDEN if s in text]
    assert not bad, bad


def test_captures():
    for log in ROOT.glob("captures/*/capture.log"):
        for n, line in enumerate(log.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            m = re.match(r"\(([\d.]+)\)\s+\S+\s+([0-9A-Fa-f]+)#([0-9A-Fa-f]*)$", line.strip())
            assert m and len(m.group(3)) % 2 == 0, f"{log}:{n}: cannot parse"
            msg = DB["messages"].get(int(m.group(2), 16))
            if msg:
                assert len(m.group(3)) // 2 == msg["dlc"], f"{log}:{n}: wrong DLC"
