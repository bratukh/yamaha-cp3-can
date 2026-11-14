<!-- GENERATED from data/signals.yaml by tools/gen_docs.py. Do not edit by hand. -->

# Open questions

What we do not know yet. A capture that settles any of these is the most useful contribution you can make; see [CONTRIBUTING](../CONTRIBUTING.md).

## Where is the odometer?

Not found. None of the 18 broadcast IDs carries a distance counter, and neither the engine ECU nor the ABS unit returns the dash mileage on any identifier we swept. The instrument cluster most likely keeps it, and the cluster did not answer on any standard address.

**What would settle it:** Not known. Passive ideas first: log while the dash menu shows the odometer and trip meters, and compare the idle bus with the cluster unplugged. We do not recommend sending requests to the unidentified units; anything sent must stay inside the read-only list in DISCLAIMER.md, with the bike parked and the engine off.

## Is there an oil temperature?

Not on the broadcast frames. OBD-II PID 0x5C is not declared in the supported-PID masks and was never requested.

**What would settle it:** One PID 0x5C request on a warm engine.

## Does a listen-only node see traffic?

Every capture here was made with a node that acknowledges frames. Some diagnostic connectors carry traffic only while something acknowledges it. We have not tried listen-only mode on the Tracer 9.

**What would settle it:** Connect a transceiver in listen-only (silent) mode with the ignition on and count frames.

## What is `setting_2bit`?

A two-bit setting sent by both the engine ECU (0x226) and the ABS unit (0x268). Brake control mode is the candidate.

**What would settle it:** Switch BC1/BC2 with the bike parked while logging, then do the same for every other menu setting.

## What do the 0x209 B5 bits mean?

They fit quickshifter up and down availability, see `shift_window_bits`.

**What would settle it:** Video of the dash quickshifter arrows together with a full-rate log.

## Traction control intervention and TCS OFF

Wheel slip is visible in 0x205, but no flag that says "traction control is cutting power now" has been found. Level 0 is probably TCS OFF but has not been confirmed with a deliberate switch during a capture.

**What would settle it:** Select TCS OFF at standstill while logging; provoke TCS on a loose surface with video of the dash light.

## Cruise control

The throttle valve stays open with the grip closed during what must be cruise control, but no cruise state or set-speed field has been identified. 0x215 B4 bits 7..6 are a candidate.

**What would settle it:** Switch cruise on, set, change the set speed and cancel while logging.

## Gyro roll and pitch scale, IMU frames 0x258 and 0x25C

Roll and pitch scales are known to 5-7 % only. 0x258 B0:B3 and all of 0x25C are not decoded; they may hold the IMU's own attitude estimate.

**What would settle it:** A ride with a rigidly mounted reference IMU, including braking and slow lean sweeps.

## Other models

Everything here comes from one 2022 base-model Tracer 9. Other Tracer 9s of any trim, year or market, the MT-09, the XSR900 and the Niken GT of the same generation probably share most of it. A second base Tracer 9 would show whether the data holds beyond one bike; the GT models have extra systems (semi-active suspension, radar on the GT+) that should add frames.

**What would settle it:** A 60-second idle capture from any of those bikes, with the model, year and market.

## Signals that are not confirmed

| ID | Signal | Where | Status | What is known |
|---|---|---|---|---|
| [0x205](messages/0x205.md) | `accel_state_bits` | B5 bits 3..0 | hypothesis (low) | Four flag bits in the low nibble of B5 (B4 is always 0). |
| [0x205](messages/0x205.md) | `b6b7_always_zero` | B6:B7 | unknown | Always 0x0000 in every full-rate capture and long-ride log. |
| [0x209](messages/0x209.md) | `b2_unknown` | B2 | unknown | Changes with road speed (correlation 0.99 with rear wheel speed over one ride). |
| [0x209](messages/0x209.md) | `start_flag` | B3 bit 0 | hypothesis (medium) | Set while the engine is cranking: in 13 of 13 engine starts it comes on with the first cranking frame and clears 0.7-0.9 s later when the engine idles. |
| [0x209](messages/0x209.md) | `b4_bit3_unknown` | B4 bit 3 | unknown | Set for about half a second at every bus wake-up, and for the whole time `tcs_level` reads 0 on the one ride where that happened. |
| [0x209](messages/0x209.md) | `shift_window_bits` | B5 bits 3..2 | hypothesis (medium) | B5 takes the values 0x00, 0x04 and 0x08. |
| [0x215](messages/0x215.md) | `throttle_valve` | B0:B1 | hypothesis (medium) | Throttle valve opening: about 14 at idle, 697-698 at the stop. |
| [0x215](messages/0x215.md) | `b4_bits67_unknown` | B4 bits 7..6 | unknown | Takes all four values during a ride, independent of the riding mode. |
| [0x226](messages/0x226.md) | `setting_2bit` | B5 bits 1..0 | hypothesis (medium) | A two-bit rider setting that the ABS unit repeats in 0x268 B4 bits 4..3: the two are equal in every paired frame. |
| [0x22A](messages/0x22A.md) | `brake_switch` | B1 bit 3 | hypothesis (medium) | B1 = 0x08 while the rear brake pedal switch (0x268 B4 bit 2) is on: 2209 of 2217 such frames on one ride, 99.2 % on another. |
| [0x22A](messages/0x22A.md) | `b1_motion_flag` | B1 bits 7..4 | ruled out | An early reading of B1 = 0x50 as "moving" did not hold: B1 stays 0x00 at a sustained 100 km/h. |
| [0x23A](messages/0x23A.md) | `wake_phase` | B0 | hypothesis (low) | 0x04 from wake-up for anything between 0.1 s and 54 s, back to 0x00 before the engine is started, and 0x00 from then on whether the engine runs or not (including a 66 s stall). |
| [0x23E](messages/0x23E.md) | `air_temp` | B1 | hypothesis (low) | An air temperature. |
| [0x23E](messages/0x23E.md) | `load_counter` | B2:B3 | hypothesis (low) | 0 with the engine off; rises on a cold start and under hard acceleration (peak 878 on one ride). |
| [0x250](messages/0x250.md) | `power_up_flags` | B6 | hypothesis (medium) | 0x80 in the first frame, 0x60 for the next 0.4 s, then 0x20 for the rest of the session whether the bike moves or not. |
| [0x254](messages/0x254.md) | `pitch_rate` | B2:B3 | hypothesis (medium) | Pitch rate, (raw − 30000) / 100. |
| [0x254](messages/0x254.md) | `b6_unknown` | B6 | unknown | B6 and B7 are always equal. |
| [0x258](messages/0x258.md) | `b0b3_unknown` | B0:B3 | unknown | Packed fields. |
| [0x258](messages/0x258.md) | `b4b5_always_zero` | B4:B5 | unknown | Always 0x0000 (311 000 frames of three full-rate captures). |
| [0x258](messages/0x258.md) | `pitch_rate_level` | B6:B7 | hypothesis (medium) | Zero at 30000-30004. |
| [0x268](messages/0x268.md) | `not_moved_since_start` | B1 bit 0 | hypothesis (medium) | 1 from power-on until the speed first passes about 6 km/h, then 0 through every later stop of the ride, and 1 again only in the last 0.2 s before the bus goes quiet. |
| [0x268](messages/0x268.md) | `setting_2bit` | B4 bits 4..3 | hypothesis (medium) | Copy of 0x226 `setting_2bit` (equal in every paired frame). |
| [0x401](messages/0x401.md) | `after_run` | B0 bit 7 | hypothesis (medium) | 0 for the whole ride, engine running or not. |
