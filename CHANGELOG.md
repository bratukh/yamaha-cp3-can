# Changelog

Versions follow semantic versioning for the data: a major version changes an ID, an address or
a scale of a confirmed signal; a minor version adds signals or promotes a status; a patch fixes
text. The DBC `VERSION` equals the repository tag.

## Unreleased

From a 2026-11 ride with dash video: the rider switched the menu settings with the dash
filmed, did a brake test at a standstill, and rode with a phone on the handlebar.

- 0x226 decoded as the rider-settings frame: B3 is the TCS mode the dash shows, B0 bits 3..2
  the TCS level in effect (they differ in M), B0 bits 1..0 and B5 bits 3..2 the SCS and LIF
  levels (which is which is open), B1 bit 0 and B5 bit 5 the quickshifter DOWN and UP enables,
  B5 bits 1..0 the brake control mode (BC1 / BC2, confirmed; was `setting_2bit`). Message
  renamed `mode_tcs` → `rider_settings`. The old readings "B0 low nibble = TCS level written
  twice" and "B5 = 0x20 + level × 4 + setting" are kept as ruled out.
- 0x209 `tcs_level` is the TCS level in effect, a copy of 0x226 B0 bits 3..2, not of the mode.
- 0x215: the copies in B4, B5 and B6 are the TCS mode, one assist level, both quickshifter
  enables and the TCS level in effect (`tcs_mode`, `assist_level_b`, `qs_down_enabled`,
  `qs_up_enabled`, `tcs_level`); "B5 = 0x28 + level" ruled out.
- 0x260 is the front brake circuit only; 0x268 B4 bit 2 and 0x22A B1 bit 3 are the brake light
  switch, set by either brake (`rear_brake_pedal` → `brake_switch`; 0x22A confirmed).
  0x268 B4 bits 4..3 renamed `bc_mode`.
- 0x23E: air temperature is 0.625 × raw − 30 (was raw − 55, a hypothesis), confirmed against
  the dash on the move; signal renamed `air_temp` → `ambient_temp`. Coolant checked against 11
  more dash readings.
- 0x254 pitch rate confirmed against a phone gyroscope; all three gyro axes about 100 counts
  per °/s. 0x258 B6:B7 described as a second pitch-rate channel. Lean reconstruction repeated
  on a second day (0.94–0.97 × the phone angle).
- 0x205 B5 bits 3..1: an acceleration level 0–7 with reversed bit order (hypothesis,
  replaces `accel_state_bits`). Dash trip meter = 1.0388 × the integrated front-wheel distance.
- 0x250 x axis: 993–999 counts per g against a phone; riding zero about 7027 against 7056 at
  rest.
- Smaller notes on 0x209 start bit and B5 quickshift patterns, 0x23A, 0x268 B1, ABS flag
  duration, 0x25C, 0x401, the always-zero frames; open questions updated.

## 0.1.0 — 2026-11-14

First public version.

- 18 broadcast frames of the 2022 Tracer 9: 9 with confirmed signals, 4 partly understood,
  5 not decoded.
- Lean angle reconstruction from yaw rate and wheel speed, with its measured error.
- OBD-II: supported-PID masks and 18 confirmed PIDs. UDS: two control units and their
  identification data.
- Generated DBC, a dependency-free Python decoder, sample captures.
