# yamaha-cp3-can

The CAN bus of the Yamaha Tracer 9 (2021–2024 generation, CP3 890 cc engine), decoded by
listening at the diagnostic connector: 18 broadcast frames, the OBD-II PIDs the engine ECU
answers, and the read-only UDS identifiers of the engine and ABS units.

Use it to build your own dash, data logger, lap timer feed or ride analysis.

> **Read-only.** Nothing here writes to the motorcycle, and the project does not accept
> anything that does. Wiring into a vehicle bus is at your own risk. Read
> [DISCLAIMER.md](DISCLAIMER.md) first.

## What was tested

| Model | Code | Year | Market | Engine ECU software | Status |
|---|---|---|---|---|---|
| Tracer 9 (base) | RN70 | 2022 | EU, Euro 5 | 12165003 | everything in this repository |

![The test motorcycle: a red 2022 Yamaha Tracer 9](docs/img/test-bike.jpg)

That is one motorcycle, the one in the photo. Its electronics are factory standard; it has an
aftermarket exhaust, a top case and bags (details in [docs/methodology.md](docs/methodology.md)). 

Every other bike of this generation is unchecked, and every one of them is welcome: another
Tracer 9 of any trim (base, GT, GT+), year or market, the MT-09 and MT-09 SP, the XSR900 and
the Niken GT. They share the engine and electronics platform and probably share most of these
frames, but nobody has checked. A second base Tracer 9 is as useful as a GT: it tells us
whether what is here holds beyond one bike. A one-minute capture settles it: see
[CONTRIBUTING.md](CONTRIBUTING.md).

## What you get

| Quantity | Frame | Rate | Status |
|---|---|---|---|
| Engine speed | [0x209](docs/messages/0x209.md) | 100 Hz | confirmed |
| Gear (sensor and shift mechanism) | [0x209](docs/messages/0x209.md) | 100 Hz | confirmed |
| Riding mode, traction-control mode and level | [0x209](docs/messages/0x209.md), [0x226](docs/messages/0x226.md) | 100 Hz | confirmed |
| Quickshifter on/off, brake-control mode (BC1/BC2) | [0x226](docs/messages/0x226.md) | 100 Hz | confirmed |
| Front and rear wheel speed, wheel slip | [0x205](docs/messages/0x205.md) | 100 Hz | confirmed |
| Throttle grip and throttle valve | [0x215](docs/messages/0x215.md) | 100 Hz | grip confirmed, valve hypothesis |
| Front brake pressure (front circuit only) | [0x260](docs/messages/0x260.md) | 100 Hz | confirmed (raw units) |
| ABS front / rear intervention, brake light switch | [0x268](docs/messages/0x268.md) | 100 Hz | confirmed |
| Acceleration, 3 axes | [0x250](docs/messages/0x250.md) | 100 Hz | confirmed |
| Roll, pitch and yaw rate | [0x254](docs/messages/0x254.md) | 100 Hz | confirmed |
| **Lean angle** (reconstructed) | [0x254](docs/messages/0x254.md) + 0x205 | 100 Hz | confirmed, with limits |
| Coolant and air temperature | [0x23E](docs/messages/0x23E.md) | 1 Hz | confirmed |
| Battery voltage, intake pressure, fuel trims and more | [OBD-II](docs/obd2.md) | on request | confirmed |

The full table is in [docs/signals.md](docs/signals.md). What we do not know is in
[docs/open-questions.md](docs/open-questions.md): the odometer, oil temperature, cruise
control state and several whole frames are still open.

The bike does not broadcast a lean angle. [docs/lean-reconstruction.md](docs/lean-reconstruction.md)
shows how to get one from yaw rate and wheel speed, and how far to trust it.

## Status

Every signal carries a status and, where it applies, a confidence.

| Status | Meaning |
|---|---|
| confirmed | Agrees with an independent reference (dash, GPS, phone sensors, an OBD-II reading or a deliberate rider action), and the agreement was reproduced on a second recording. A field that always equals a confirmed one is confirmed as a copy of it. |
| hypothesis | A pattern in the data that fits, without an independent reference yet. |
| unknown | The bits are on the bus; we do not know what they mean. That includes fields that never changed. |
| ruled out | An earlier reading that the data disproved. Kept so nobody repeats it. |

Confidence is high, medium or low. Medium usually means one ride, one reference, or a scale
known to a few percent only. Each confirmed signal names what it was checked against
("Confirmed by") on its message page and in [docs/signals.md](docs/signals.md); the methods
are in [docs/methodology.md](docs/methodology.md).

## Quick start

Hardware and wiring: [docs/connecting.md](docs/connecting.md). The bus runs at 500 kbit/s with
11-bit IDs.

With a Linux SocketCAN adapter and [cantools](https://github.com/cantools/cantools):

```bash
candump can0 | python3 -m cantools decode dbc/yamaha_cp3_2021-2024.dbc
```

With the small decoder in this repository (Python standard library only), on one of the
sample captures:

```bash
python3 decoder/cp3can.py captures/acceleration-through-gears/capture.log --signals engine_rpm,gear_actual,wheel_speed_front
```

In your own code the essentials fit in a few lines:

```c
// 0x209, 6 bytes
rpm  = ((d[0] << 8) | d[1]) * 25 / 64;
gear = d[4] & 0x07;                      // 0 = neutral, 7 = between gears

// 0x205, 8 bytes
front_kmh = ((d[0] << 8) | d[1]) / 101.0;
rear_kmh  = ((d[2] << 8) | d[3]) / 101.0;

// 0x254, 8 bytes
yaw_deg_s = (((d[4] << 8) | d[5]) - 30000) / 100.0;   // positive = left turn
```

## Repository map

| Path | What |
|---|---|
| [data/signals.yaml](data/signals.yaml) | The signal database. Everything else is generated from it or cites it. |
| [dbc/](dbc/) | Generated DBC file for SavvyCAN, cantools, Kvaser, PCAN and the like. |
| [docs/messages/](docs/messages/) | One generated page per CAN ID: layout, formula, evidence, example frame. |
| [docs/connecting.md](docs/connecting.md) | Connector, wiring, what the logger must do. |
| [docs/bus.md](docs/bus.md) | Which frames exist, how often, what happens at power-up and shutdown. |
| [docs/imu.md](docs/imu.md), [docs/lean-reconstruction.md](docs/lean-reconstruction.md) | The inertial unit and the lean angle. |
| [docs/obd2.md](docs/obd2.md), [docs/uds.md](docs/uds.md) | Request/response diagnostics, read-only. |
| [docs/methodology.md](docs/methodology.md) | How signals were found and what counts as confirmed. |
| [docs/prior-art.md](docs/prior-art.md) | Our results compared with other public Yamaha decodes. |
| [captures/](captures/) | Short sample logs in `candump` format with event lists. |
| [decoder/](decoder/) | A dependency-free Python decoder. |

## Contributing

Help is wanted: this is one bike's worth of data, and a good part of the bus is still unknown.

- **Own any bike of this family?** A Tracer 9 of any trim, an MT-09, an XSR900 or a Niken GT,
  any year from 2021, any market. A one-minute capture tells us which frames your bike shares.
- **Curious?** [docs/open-questions.md](docs/open-questions.md) lists what would settle each
  unknown, often a two-minute test with the bike parked.
- **Found a mistake?** Open an issue. Several entries here were wrong before they were right.

How to capture, what to send and how statuses are decided: [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

Data and documentation (`data/`, `dbc/`, `docs/`, `captures/`) are under
[CC BY 4.0](LICENSE-DATA). Code (`decoder/`, `tools/`, `tests/`) is under the [MIT licence](LICENSE).

Yamaha, Tracer and MT-09 are trademarks of Yamaha Motor Co., Ltd. This project is not
affiliated with or endorsed by Yamaha.
