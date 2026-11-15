# The bus at a glance

500 kbit/s, 11-bit identifiers, 18 broadcast IDs, 1071 frames per second. All rates
below were measured on full-rate captures and are exact to the precision shown: the 100 Hz
frames arrive every 10 ms.

| ID | DLC | Rate | Content | Status |
|---|---|---|---|---|
| [0x205](messages/0x205.md) | 8 | 100 Hz | Front and rear wheel speed | confirmed |
| [0x209](messages/0x209.md) | 6 | 100 Hz | Engine speed, gear, riding mode, TCS level in effect | confirmed |
| [0x215](messages/0x215.md) | 8 | 100 Hz | Throttle grip and throttle valve, copies of rider settings | confirmed |
| [0x226](messages/0x226.md) | 7 | 100 Hz | Rider settings: mode, TCS mode and level, SCS/LIF, quickshifter, BC | confirmed |
| [0x22A](messages/0x22A.md) | 2 | 10 Hz | Brake light switch (either brake) | confirmed |
| [0x22B](messages/0x22B.md) | 2 | 10 Hz | Always zero | unknown |
| [0x22E](messages/0x22E.md) | 2 | 10 Hz | Always zero | unknown |
| [0x23A](messages/0x23A.md) | 3 | 10 Hz | A wake-up phase flag | hypothesis |
| [0x23E](messages/0x23E.md) | 4 | 1 Hz | Coolant and air temperature, a load counter | confirmed |
| [0x245](messages/0x245.md) | 1 | 10 Hz | Always zero | unknown |
| [0x250](messages/0x250.md) | 8 | 100 Hz | Accelerometer | confirmed |
| [0x254](messages/0x254.md) | 8 | 100 Hz | Gyroscope | confirmed |
| [0x258](messages/0x258.md) | 8 | 100 Hz | IMU, packed fields, a second pitch rate | hypothesis |
| [0x25C](messages/0x25C.md) | 4 | 100 Hz | IMU, not decoded | unknown |
| [0x260](messages/0x260.md) | 8 | 100 Hz | Front brake pressure (front circuit only) | confirmed |
| [0x268](messages/0x268.md) | 6 | 100 Hz | Speed, ABS flags, brake light switch, BC mode | confirmed |
| [0x401](messages/0x401.md) | 1 | 10 Hz | After-run flag at shutdown | hypothesis |
| [0x590](messages/0x590.md) | 4 | 10 Hz | Always zero | unknown |

Ten IDs at 100 Hz, seven at 10 Hz and one at 1 Hz add up to 1071 frames per second, which is
what the full-rate captures show.

## Who sends what

We have not opened the harness, so the senders below are a guess from content. Start-up and
shutdown timing does not fully support it: 0x205 starts and stops together with 0x209 and
0x215 and not with 0x260 and 0x268, and 0x226 starts with 0x22E and 0x590, about 0.18 s after
0x209.

- **Engine ECU:** 0x209, 0x215, 0x226, 0x23E and probably 0x23A.
- **ABS unit:** 0x205, 0x260, 0x268.
- **IMU:** 0x250, 0x254, 0x258, 0x25C.
- **Unassigned:** 0x22A, 0x22B, 0x22E, 0x245, 0x401, 0x590.

The instrument cluster does not appear as a sender we can identify, and it did not answer on
any standard diagnostic address. The four always-zero frames stayed zero in every byte through a
whole day of riding. They may belong to equipment this base model does not have (heated grips,
heated seat, semi-active suspension on the GT models) or to states we never triggered.

## One setting, several copies

The engine ECU repeats the rider's settings in several frames, which makes a useful consistency
check for a decoder. The TCS mode (what the dash shows) and the TCS level in effect are
different fields: in the TCS 1 and TCS 2 modes they are equal, in M the level is whatever the
rider set inside M. Early captures could not tell them apart, because the rider's M setup had
every level at 3.

| Setting | Copies |
|---|---|
| Riding mode | 0x209 B4 bits 7..6, 0x215 B7 bits 7..6, 0x226 B0 bits 7..6 |
| TCS mode | 0x226 B3, 0x215 B4 bits 1..0 |
| TCS level in effect | 0x226 B0 bits 3..2, 0x209 B3 bits 4..1, 0x215 B6 bits 2..1 |
| SCS or LIF level (which is open) | 0x226 B0 bits 1..0 |
| The other of SCS and LIF | 0x226 B5 bits 3..2, 0x215 B5 bits 1..0 |
| Quickshifter UP on | 0x226 B5 bit 5, 0x215 B5 bit 5 |
| Quickshifter DOWN on | 0x226 B1 bit 0, 0x215 B5 bit 3 |
| Brake control mode (BC1 / BC2) | 0x226 B5 bits 1..0, 0x268 B4 bits 4..3 |
| Brake light switch | 0x268 B4 bit 2, 0x22A B1 bit 3 |

## Power-up

The first frames after the bus wakes are not ordinary data. A decoder should skip about one
second, or at least know these:

| Frame | Start-up behaviour |
|---|---|
| 0x209 | B4 reads 0x48/0x49 for ~0.2 s, then 0x08/0x09 for ~0.35 s |
| 0x226 | The very first frame is `05 01 00 01 00 25 28` whatever the settings; real values follow within 10 ms |
| 0x23A | B0 = 0x04 for a while (0.1 s to 54 s), then 0x00 |
| 0x250 | First frame is the reset value `1B 58 1B 58 1F 40 80 00`; B6 = 0x60 for 0.4 s |
| 0x254 | First frame is `75 30 75 30 75 30 60 60` (all axes at 30000) |
| 0x268 | B1 = 0x01 until the bike first exceeds about 6 km/h |

## Shutdown

When the ignition is switched off the IDs stop within about 0.2 s of one another: the IMU
frames first, then the 10 Hz frames and 0x226, then 0x205, 0x209 and 0x215, and last 0x260 and
0x268. 0x401 switches from 0x00 to 0x80 while the last of them are still running and then keeps
going alone at 10 Hz. Our longest capture ends 31 s later with 0x401 still sending, so we do
not know how long it lasts. See the `shutdown` capture.

## Engine running or not

No single flag that says "engine running" has been confirmed. Use `engine_rpm` from 0x209.
Two frames that look like engine-state flags in short captures (0x23A and 0x401) turned out to
be wake-up and shutdown phases.

## Diagnostic traffic

Diagnostic frames (0x7DF, 0x7E0–0x7EF) appear only when a tester asks. See [obd2.md](obd2.md)
and [uds.md](uds.md).
