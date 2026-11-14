<!-- GENERATED from data/signals.yaml by tools/gen_docs.py. Do not edit by hand. -->

# All signals

One row per signal. The last column says what a confirmed signal was checked against; where it reads 'Copy of' or 'nothing outside the bus', it is known only by agreement with another field. Follow the ID link for the description, the numbers and an example frame. Status meanings are in the [README](../README.md#status).

## Broadcast frames

| ID | Hz | Signal | Where | Value | Unit | Status | Confirmed by |
|---|---|---|---|---|---|---|---|
| [0x205](messages/0x205.md) | 100 | `wheel_speed_front` | B0:B1 | raw × 0.00990099 | km/h | confirmed (high) | Phone GPS speed on one ride; the dash speedometer on video on two others |
| [0x205](messages/0x205.md) | 100 | `wheel_speed_rear` | B2:B3 | raw × 0.00990099 | km/h | confirmed (medium) | The front wheel word; the wheel-speed dip at rear ABS events |
| [0x205](messages/0x205.md) | 100 | `accel_state_bits` | B5 bits 3..0 | raw |  | hypothesis (low) |  |
| [0x205](messages/0x205.md) | 100 | `b6b7_always_zero` | B6:B7 | raw |  | unknown |  |
| [0x205](messages/0x205.md) | | `wheel_slip` (derived) | | `wheel_speed_rear - wheel_speed_front` | km/h | confirmed (high) | Rear ABS events; wheelspin on sand |
| [0x209](messages/0x209.md) | 100 | `engine_rpm` | B0:B1 | raw × 0.390625 | rpm | confirmed (high) | OBD-II PID 0x0C on the same bus; the exhaust-note frequency on the camera sound track |
| [0x209](messages/0x209.md) | 100 | `b2_unknown` | B2 | raw |  | unknown |  |
| [0x209](messages/0x209.md) | 100 | `gear_actual` | B3 bits 7..5 | enum | gear | confirmed (high) | Published gearbox ratios, through engine speed divided by wheel speed |
| [0x209](messages/0x209.md) | 100 | `tcs_level` | B3 bits 4..1 | enum |  | confirmed (high) | The dash on video with spoken markers, through 0x226 B3 |
| [0x209](messages/0x209.md) | 100 | `start_flag` | B3 bit 0 | raw |  | hypothesis (medium) |  |
| [0x209](messages/0x209.md) | 100 | `gear_requested` | B4 bits 2..0 | enum | gear | confirmed (high) | Gear changes on rides; the dash gear indicator with the engine stopped |
| [0x209](messages/0x209.md) | 100 | `b4_bit3_unknown` | B4 bit 3 | raw |  | unknown |  |
| [0x209](messages/0x209.md) | 100 | `ride_mode` | B4 bits 7..6 | enum |  | confirmed (medium) | The dash on video with spoken markers |
| [0x209](messages/0x209.md) | 100 | `shift_window_bits` | B5 bits 3..2 | enum |  | hypothesis (medium) |  |
| [0x215](messages/0x215.md) | 100 | `throttle_valve` | B0:B1 | raw | raw | hypothesis (medium) |  |
| [0x215](messages/0x215.md) | 100 | `throttle_grip` | B2:B3 | raw | raw | confirmed (medium) | The mechanical stops of the grip. No independent position reference |
| [0x215](messages/0x215.md) | 100 | `tcs_level_b4` | B4 bits 1..0 | raw |  | confirmed (medium) | Copy of 0x226 `tcs_level`; nothing outside the bus |
| [0x215](messages/0x215.md) | 100 | `grip_closed` | B4 bit 5 | raw |  | confirmed (medium) | Follows `throttle_grip`; nothing outside the bus |
| [0x215](messages/0x215.md) | 100 | `b4_bits67_unknown` | B4 bits 7..6 | raw |  | unknown |  |
| [0x215](messages/0x215.md) | 100 | `tcs_level_b5` | B5 bits 1..0 | raw |  | confirmed (medium) | Copy of 0x226 `tcs_level`; nothing outside the bus |
| [0x215](messages/0x215.md) | 100 | `tcs_level_b6` | B6 bits 2..1 | raw |  | confirmed (medium) | Copy of 0x226 `tcs_level`; nothing outside the bus |
| [0x215](messages/0x215.md) | 100 | `ride_mode` | B7 bits 7..6 | enum |  | confirmed (medium) | Copy of 0x209 `ride_mode`; nothing outside the bus |
| [0x226](messages/0x226.md) | 100 | `ride_mode` | B0 bits 7..6 | enum |  | confirmed (medium) | The dash on video with spoken markers |
| [0x226](messages/0x226.md) | 100 | `tcs_pattern` | B0 bits 3..0 | enum |  | confirmed (high) | Copy of `tcs_level` in the same frame; nothing outside the bus |
| [0x226](messages/0x226.md) | 100 | `tcs_level` | B3 | enum |  | confirmed (high) | The dash on video with spoken markers |
| [0x226](messages/0x226.md) | 100 | `tcs_level_b5` | B5 bits 3..2 | raw |  | confirmed (high) | Copy of `tcs_level` in the same frame; nothing outside the bus |
| [0x226](messages/0x226.md) | 100 | `setting_2bit` | B5 bits 1..0 | raw |  | hypothesis (medium) |  |
| [0x22A](messages/0x22A.md) | 10 | `brake_switch` | B1 bit 3 | raw |  | hypothesis (medium) |  |
| [0x22A](messages/0x22A.md) | 10 | `b1_motion_flag` | B1 bits 7..4 | raw |  | ruled out |  |
| [0x22B](messages/0x22B.md) | 10 | — | | | | unknown | |
| [0x22E](messages/0x22E.md) | 10 | — | | | | unknown | |
| [0x23A](messages/0x23A.md) | 10 | `wake_phase` | B0 | enum |  | hypothesis (low) |  |
| [0x23E](messages/0x23E.md) | 1 | `coolant_temp` | B0 | raw × 0.625 − 30 | degC | confirmed (high) | OBD-II PID 0x05 (same ECU); one dash reading on video |
| [0x23E](messages/0x23E.md) | 1 | `air_temp` | B1 | raw − 55 | degC | hypothesis (low) |  |
| [0x23E](messages/0x23E.md) | 1 | `load_counter` | B2:B3 | raw | raw | hypothesis (low) |  |
| [0x245](messages/0x245.md) | 10 | — | | | | unknown | |
| [0x250](messages/0x250.md) | 100 | `accel_x` | B0:B1 | raw × 0.001008 − 7.056 | g | confirmed (medium) | The derivative of wheel speed; GPS speed change |
| [0x250](messages/0x250.md) | 100 | `accel_y` | B2:B3 | raw × 0.001008 − 7.056 | g | confirmed (medium) | An iPhone level (Measure app) fixed above the dash, filmed, bike parked |
| [0x250](messages/0x250.md) | 100 | `accel_z` | B4:B5 | raw × 0.001008 − 7.056 | g | confirmed (medium) | Gravity: the magnitude of the three axes at rest |
| [0x250](messages/0x250.md) | 100 | `lean_static` | B2:B3 | raw × -0.057412 + 402.59 | deg | confirmed (high) | An iPhone level (Measure app) fixed above the dash, filmed, bike parked |
| [0x250](messages/0x250.md) | 100 | `power_up_flags` | B6 | enum |  | hypothesis (medium) |  |
| [0x254](messages/0x254.md) | 100 | `roll_rate` | B0:B1 | raw × 0.01 − 300 | deg/s | confirmed (medium) | The accelerometer angle over two side-stand lifts; an iPhone gyro fixed above the dash |
| [0x254](messages/0x254.md) | 100 | `pitch_rate` | B2:B3 | raw × 0.01 − 300 | deg/s | hypothesis (medium) |  |
| [0x254](messages/0x254.md) | 100 | `yaw_rate` | B4:B5 | raw × 0.01 − 300 | deg/s | confirmed (medium) | Phone GPS heading over whole turns |
| [0x254](messages/0x254.md) | 100 | `b6_unknown` | B6 | raw |  | unknown |  |
| [0x254](messages/0x254.md) | | `lean_angle` (derived) | | `atan((yaw_raw - 30000) * v / 45873), v = wheel_speed_front in m/s` | deg | confirmed (medium) | An iPhone's attitude (Sensor Logger app), fixed above the dash, one ride |
| [0x258](messages/0x258.md) | 100 | `b0b3_unknown` | B0:B3 | raw |  | unknown |  |
| [0x258](messages/0x258.md) | 100 | `b4b5_always_zero` | B4:B5 | raw |  | unknown |  |
| [0x258](messages/0x258.md) | 100 | `pitch_rate_level` | B6:B7 | raw × 0.01 − 300 | deg/s | hypothesis (medium) |  |
| [0x25C](messages/0x25C.md) | 100 | — | | | | unknown | |
| [0x260](messages/0x260.md) | 100 | `brake_pressure_front` | B0:B1 | raw | raw | confirmed (high) | The rider's announced lever use; coincidence with front ABS and front-wheel deceleration. No pressure gauge |
| [0x268](messages/0x268.md) | 100 | `not_moved_since_start` | B1 bit 0 | raw |  | hypothesis (medium) |  |
| [0x268](messages/0x268.md) | 100 | `vehicle_speed` | B2:B3 | raw × 0.056497 | km/h | confirmed (medium) | Copy of 0x205 `wheel_speed_front` at a different scale; nothing outside the bus |
| [0x268](messages/0x268.md) | 100 | `abs_rear_active` | B4 bit 0 | raw |  | confirmed (high) | The rear wheel-speed dip at each event; rear-brake stops announced by the rider |
| [0x268](messages/0x268.md) | 100 | `abs_front_active` | B4 bit 1 | raw |  | confirmed (medium) | The rider's call and audible pulsing during deliberate hard stops; brake pressure; front wheel deceleration |
| [0x268](messages/0x268.md) | 100 | `rear_brake_pedal` | B4 bit 2 | raw |  | confirmed (medium) | The rider's announced pedal presses |
| [0x268](messages/0x268.md) | 100 | `setting_2bit` | B4 bits 4..3 | raw |  | hypothesis (medium) |  |
| [0x401](messages/0x401.md) | 10 | `after_run` | B0 bit 7 | raw |  | hypothesis (medium) |  |
| [0x590](messages/0x590.md) | 10 | — | | | | unknown | |

## OBD-II mode 01

Details in [obd2.md](obd2.md).

| PID | Name | Unit | Status | Example response data → value |
|---|---|---|---|---|
| 0x04 | Calculated engine load | % | confirmed (medium) | `43` → 26.3 |
| 0x05 | Coolant temperature | degC | confirmed (high) | `5D` → 53 |
| 0x06 | Short-term fuel trim | % | confirmed (medium) | `7F 00` → -0.8 |
| 0x07 | Long-term fuel trim | % | confirmed (medium) | `7F 00` → -0.8 |
| 0x0B | Intake manifold pressure | kPa | confirmed (medium) | `44` → 68 |
| 0x0C | Engine speed | rpm | confirmed (high) | `17 0D` → 1475.25 |
| 0x0D | Vehicle speed | km/h | confirmed (medium) | `0E` → 14 |
| 0x0E | Timing advance | deg | confirmed (medium) | `8A` → 5 |
| 0x0F | Intake air temperature | degC | confirmed (medium) | `36` → 14 |
| 0x11 | Throttle position | % | confirmed (medium) | `25` → 14.5 |
| 0x14 | Oxygen sensor 1 voltage | V | confirmed (medium) | `3E 80` → 0.31 |
| 0x1C | OBD standard |  | hypothesis (low) | `25` → 37 |
| 0x33 | Barometric pressure | kPa | confirmed (medium) | `63` → 99 |
| 0x42 | Control module voltage | V | confirmed (medium) | `37 3C` → 14.14 |
| 0x45 | Relative throttle position | % | confirmed (medium) | `05` → 2.0 |
| 0x47 | Absolute throttle position B | % | confirmed (medium) | `22` → 13.3 |
| 0x49 | Accelerator position D | % | confirmed (medium) | `20` → 12.5 |
| 0x4A | Accelerator position E | % | confirmed (medium) | `20` → 12.5 |
| 0x4D | Run time with MIL on | min | confirmed (medium) | `00 00` → 0 |
| 0x5A | Relative accelerator position | % | hypothesis (low) |  |
| 0x65 | Auxiliary input / output |  | unknown |  |
| 0x2F | Fuel level | % | ruled out |  |
| 0xA6 | Odometer | km | ruled out |  |

## UDS data identifiers (read-only)

Details in [uds.md](uds.md).

| ECU | DID | Name | Status | Note |
|---|---|---|---|---|
| 0x7E0 | 0xF190 | VIN | confirmed (high) | 17 ASCII characters, multi-frame. |
| 0x7E0 | 0xF18A | System supplier | confirmed (high) | 44 45 4E 00 = DEN. |
| 0x7E0 | 0xF18C | ECU serial number | confirmed (high) | FF FF FF FF (not provided). |
| 0x7E0 | 0xF192 | Hardware number | confirmed (high) | FF FF FF FF (not provided). |
| 0x7E0 | 0xF194 | Software number | confirmed (high) | 12 16 50 03, BCD for 12165003; matches OBD mode 09 CalID. |
| 0x7E0 | 0xF195 | Software version | confirmed (high) | 03. |
| 0x7E0 | 0xF197 | System name | confirmed (high) | 42 35 55 31 = B5U1. |
| 0x7E0 | 0xF1A0 | Manufacturer-specific | unknown | 0C 01 00 05; the ABS unit answers 0C 01 00 02. |
| 0x7E0 | 0xF1A1 | Ignition-on time | confirmed (high) | 32-bit count of seconds with the ignition on. Rose by 85 in the 84.3 s between two reads. |
| 0x7E0 | 0xF1A2 | Slow counter | hypothesis (low) | 16-bit. Constant within a session and a few counts higher on later days; possibly ignition cycles. |
| 0x7E0 | 0xF1EF | Unknown | unknown | 00 00. |
| 0x7E0 | 0xF198 | Unknown | unknown | NRC 0x22 conditionsNotCorrect in both sessions. |
| 0x7E0 | 0xF199 | Unknown | unknown | NRC 0x22 conditionsNotCorrect in both sessions. |
| 0x7E3 | 0xF18A | System supplier | confirmed (high) | 42 4F 53 43 = BOSC. |
| 0x7E3 | 0xF18C | ECU serial number | confirmed (high) | 00 00 00 00. |
| 0x7E3 | 0xF192 | Hardware number | confirmed (high) | 00 00 00 00. |
| 0x7E3 | 0xF194 | Software number | confirmed (high) | 12 16 51 80. |
| 0x7E3 | 0xF195 | Software version | confirmed (high) | 00. |
| 0x7E3 | 0xF197 | System name | confirmed (high) | 42 35 55 31 = B5U1, the same string as the engine ECU. |
| 0x7E3 | 0xF1A0 | Manufacturer-specific | unknown | 0C 01 00 02. |
