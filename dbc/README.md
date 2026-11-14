# DBC file

`yamaha_cp3_2021-2024.dbc` is generated from [`data/signals.yaml`](../data/signals.yaml) by
`tools/gen_dbc.py`. Do not edit it by hand.

It loads in SavvyCAN, cantools, Kvaser Database Editor, PCAN-Explorer, BusMaster and anything
else that reads DBC.

What it contains:

- Every signal with status `confirmed` or `hypothesis`. Unknown bits are left unallocated.
- The status of each message and signal as a `Status` attribute, and at the start of each
  signal comment as `[status/confidence]`. **Check it before you rely on a signal.**
- Cycle times as `GenMsgCycleTime`.
- Value tables for gear, riding mode and traction-control level.

What it cannot contain:

- **Lean angle.** It is computed from two frames; see
  [docs/lean-reconstruction.md](../docs/lean-reconstruction.md).
- **Wheel slip**, the difference of two signals.
- **Static lean angle**, which reuses the bits of `ACCEL_Y`.
- The evidence behind each signal. That is on the pages under
  [docs/messages/](../docs/messages/).

All signals are big-endian (Motorola byte order, `@0` in DBC terms). The name covers the
2021–2024 generation; the content was read from a 2022 Tracer 9 only.
