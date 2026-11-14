#!/usr/bin/env python3
"""Decode Yamaha CP3 (Tracer 9 2021-2024) CAN frames. Python 3.9+, standard library only.

    from cp3can import decode, State
    decode(0x205, bytes.fromhex("2B212B7800040000"))   # {'wheel_speed_front': 109.3, ...}

Command line, on a Linux `candump -l` log:
    python3 cp3can.py capture.log [--csv out.csv] [--signals a,b,c] [--rate HZ]

The signal table (cp3_table.py) is generated from data/signals.yaml.
"""
import argparse
import csv
import math
import re
import sys

try:
    from cp3_table import MESSAGES
except ImportError:  # imported as a package
    from .cp3_table import MESSAGES


def _raw(sig, data):
    """Raw integer of one signal, or None if the frame is too short for it."""
    first = sig["byte"]
    if sig["bit"] is not None:
        if first >= len(data):
            return None
        return (data[first] >> sig["bit"]) & ((1 << sig["nbits"]) - 1)
    end = first + sig["nbits"] // 8
    if end > len(data):
        return None
    return int.from_bytes(data[first:end], sig["endian"], signed=sig["signed"])


def decode(can_id, data):
    """Physical value of every signal in a frame, by name. Unknown ids give {}.

    Signals that do not fit in a short frame are skipped. Signals with a value
    table return the raw code (look it up in cp3_table.MESSAGES).
    """
    msg = MESSAGES.get(can_id)
    if msg is None:
        return {}
    out = {}
    for sig in msg["signals"]:
        raw = _raw(sig, data)
        if raw is not None:
            out[sig["name"]] = raw * sig["scale"] + sig["offset"]
    return out


def lean_angle_deg(yaw_rate_deg_s, speed_kmh):
    """Lean angle in degrees, positive to the left, from yaw rate and speed.

    The bus carries no lean angle: atan(yaw * v / 45873) with yaw in raw counts
    (yaw_rate * 100 counts) and v in m/s. The 45873 constant folds together
    gravity and the yaw scale. Valid for steady corners; see the docs.
    """
    return math.degrees(math.atan(yaw_rate_deg_s * 100 * (speed_kmh / 3.6) / 45873))


# Signal names that occur in more than one message get the id appended.
_COUNT = {}
for _msg in MESSAGES.values():
    for _sig in _msg["signals"]:
        _COUNT[_sig["name"]] = _COUNT.get(_sig["name"], 0) + 1


class State:
    """Latest value of every signal, plus lean_angle and wheel_slip.

    Feed frames with update(can_id, data). Read self.values (a dict).
    A name used by several messages is stored as "<name>_<id>", e.g. "tcs_level_209".
    """

    def __init__(self):
        self.values = {}

    @staticmethod
    def known_names():
        """Every key update() can produce."""
        names = {"wheel_slip", "lean_angle"}
        for can_id, msg in MESSAGES.items():
            for sig in msg["signals"]:
                name = sig["name"]
                names.add(name if _COUNT[name] == 1 else "%s_%03x" % (name, can_id))
        return names

    def update(self, can_id, data):
        for name, value in decode(can_id, data).items():
            key = name if _COUNT[name] == 1 else "%s_%03x" % (name, can_id)
            self.values[key] = value
        v = self.values
        if "wheel_speed_front" in v and "wheel_speed_rear" in v:
            v["wheel_slip"] = v["wheel_speed_rear"] - v["wheel_speed_front"]
        if "yaw_rate" in v and "wheel_speed_front" in v:
            v["lean_angle"] = lean_angle_deg(v["yaw_rate"], v["wheel_speed_front"])
        return self.values


_LINE = re.compile(r"\(([\d.]+)\)\s+\S+\s+([0-9A-Fa-f]+)#([0-9A-Fa-f]*)\s*$")


def read_candump(lines):
    """Yield (time_s, can_id, data) from candump -l lines; others are skipped."""
    for line in lines:
        m = _LINE.match(line.strip())
        if m and len(m.group(3)) % 2 == 0:
            yield float(m.group(1)), int(m.group(2), 16), bytes.fromhex(m.group(3))


def resample(frames, rate_hz, names=None):
    """Return (columns, rows): the state sampled on a regular grid (hold last value)."""
    state, rows, columns = State(), [], []
    step = 1.0 / rate_hz
    t0 = next_t = None
    snapshots = []
    for t, can_id, data in frames:
        if t0 is None:
            t0 = next_t = t
        while next_t <= t:
            snapshots.append((next_t - t0, dict(state.values)))
            next_t += step
        state.update(can_id, data)
        for key in state.values:
            if key not in columns:
                columns.append(key)
    if names:
        columns = list(names)
    for t, values in snapshots:
        cells = [values.get(c, "") for c in columns]
        rows.append([round(t, 6)] + [round(v, 4) if isinstance(v, float) else v for v in cells])
    return columns, rows


def main(argv=None):
    ap = argparse.ArgumentParser(description="Decode a candump -l log.")
    ap.add_argument("log")
    ap.add_argument("--csv", help="write CSV here instead of stdout")
    ap.add_argument("--signals", help="comma-separated signal names (default: all seen)")
    ap.add_argument("--rate", type=float, default=10.0, help="output rate in Hz (default 10)")
    args = ap.parse_args(argv)
    names = args.signals.split(",") if args.signals else None
    with open(args.log, encoding="utf-8", errors="replace") as fh:
        columns, rows = resample(read_candump(fh), args.rate, names)
    if names:
        seen = State.known_names()
        for name in names:
            if name not in seen:
                close = sorted(k for k in seen if k.startswith(name + "_") or name in k)
                print(f"warning: no signal named {name!r}"
                      + (f"; did you mean {', '.join(close)}?" if close else ""), file=sys.stderr)
    out = open(args.csv, "w", newline="") if args.csv else sys.stdout
    try:
        writer = csv.writer(out)
        writer.writerow(["time_s"] + columns)
        writer.writerows(rows)
    finally:
        if args.csv:
            out.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
