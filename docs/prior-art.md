# Comparison with other public decodes

Before publishing we looked for other public work on Yamaha CAN buses and checked our results
against it. This page lists what we found, where it agrees with our data and where it does
not.

Searched in July and November 2026, in English, on GitHub and the main owner forums. Closed
communities and most non-English forums are not covered.

## Sources

| Source | Motorcycle | What it has |
|---|---|---|
| [DeziderMesko/motocan](https://github.com/DeziderMesko/motocan) | YZF-R9 (same engine as the Tracer 9) | Signal-level decode with a DBC and captures |
| r1-forum.com, thread "CAN Bus Protocol" | YZF-R1, 2015 on | Bus description, some frame IDs |
| fz07.org and the RaceChrono forum, thread "PIDs for Yamaha" | MT-07, Ténéré 700 | Some IDs and formulas |

We found no public signal-level decode of the 2021–2024 Tracer 9 (any trim), MT-09, XSR900 or
Niken GT. If you know of one, please open an issue.

The forum threads sit behind bot protection, so their details below come from manual reading
and search excerpts.

## Where the results agree

**YZF-R9, engine frame.** The R9 sends it on ID 0x27C, the Tracer 9 on 0x209. The fields are
in the same places:

| Field | R9, 0x27C | Tracer 9, 0x209 (ours) |
|---|---|---|
| Engine speed | B0:B1 × 100/256 | B0:B1 × 25/64, the same factor |
| TCS setting | (B3 >> 1) & 0x0F | B3 bits 4..1 |
| Start bit | B3 & 0x01, about 0.5 s at engine start | B3 bit 0, 0.7–0.9 s at engine start |
| Gear | B4 & 0x07, 7 = between gears | B4 bits 2..0, 7 = between gears |
| Riding mode | B4 >> 6 | B4 bits 7..6 |

**YZF-R9, coolant temperature.** 0.625 × raw − 30 in both, on different IDs (theirs 0x512, ours
0x23E). Theirs was fitted to dash readings, ours to OBD-II.

**YZF-R1.** It names 0x260 and 0x268 as ABS frames, with brake pressure in 0x260. Same IDs and
same roles as ours.

**MT-07 / Ténéré 700.** 0x268 B4 reads 0x04 while braking, which is our rear brake pedal bit.
Gear is coded in three bits with 7 for "between gears", as in ours, though in a different
frame.

## Where they differ

| | Other source | Tracer 9 (ours) |
|---|---|---|
| Engine frame ID | R9: 0x27C | 0x209 |
| Number of broadcast IDs | R9: 23 | 18 |
| Frames per second | R9: about 506 | 1071 |
| Byte next to coolant | R9: intake air, 0.625 × raw − 30 | `air_temp`, raw − 55, a hypothesis. Not resolved; see [0x23E](messages/0x23E.md). |
| Diagnostic connector | R9: frames flow only while something acknowledges | Not tested in listen-only mode |
| Engine speed and throttle IDs | MT-07 / Ténéré 700: 0x20A and 0x216 | 0x209 and 0x215 |
| IMU frames | R9: not in the decode as far as we read | 0x250, 0x254 |

## What the comparison changed in our data

One thing. The R9 table has the TCS setting in B3 of the engine frame. We had the TCS level
from frame 0x226 and had not examined those bits of 0x209. We checked them on our logs: they
equal 0x226 B3 in more than 420 000 paired frames. That field is in the database as
[0x209 `tcs_level`](messages/0x209.md).

Nothing else was changed. No scale, address or status in this repository comes from another
source; each rests on the recordings described in [methodology.md](methodology.md).

## Not found anywhere else

As far as we could find, these have not been published before for any Yamaha with this engine:

- the accelerometer and gyroscope frames (0x250, 0x254) with scales and signs;
- per-wheel speeds (0x205) with a GPS-checked scale;
- a lean angle reconstructed from yaw rate and speed, with a measured error;
- the OBD-II and UDS identification data of the Tracer 9.
