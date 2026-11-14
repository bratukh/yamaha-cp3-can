# Connecting to the bus

## The connector

The bus is reached at the 6-pin diagnostic connector under the seat. It is the connector type
that Euro 5 motorcycles use for diagnostics (ISO 19689); the mating part is commonly sold as a
"Euro 5 6-pin diagnostic" plug or as a 6-pin to OBD-II adapter cable.

The connector carries six wires. We reach them through an off-the-shelf adapter cable (a
Yamaha 6-pin plug with bare wires at the other end), so we know them by function and by the
colour of the wire on that cable:

| Function | Wire colour on our adapter cable | Our experience | Pin, from published pinouts for this connector type |
|---|---|---|---|
| CAN high | Green | **Verified**: the logger has run on it for months | 2 |
| CAN low | Yellow | **Verified**, same | 5 |
| Ground | Black | **Verified** | 3 |
| Battery +12 V | Red | **Verified, and permanent**: it stays live with the ignition off | 4 |
| Not used | Brown | Probably K-line; not tested | 6 |
| Not used | Orange | Function unknown | 1 |

The functions and colours are first-hand. Two cautions:

- **The colours are those of our adapter cable.** They are the usual ones for these cables
  (green and yellow for CAN, red and black for power), but another maker may use different
  colours, and the colours inside the bike's own harness are not known to us.
- **The pin numbers are not ours.** We have not traced which pin of the plug each wire goes
  to. The numbers in the last column come from published descriptions of the ISO 19689
  connector. Our own early notes had ground on pin 1 and +12 V on pin 6, which contradicts
  that layout, and we never settled it. Which of the two unused wires is on pin 6 and which
  on pin 1 is also an assumption. Rely on the functions, not on the numbers.

Before you connect anything, check with a multimeter: find the wire with continuity to the
battery negative terminal, then the one that shows battery voltage against it. The two CAN
wires sit near 2.5 V each with the ignition on. If you trace the pin numbers on your bike,
please [tell us](../CONTRIBUTING.md) and this table gets fixed.

## Bus parameters

| | |
|---|---|
| Bit rate | 500 kbit/s |
| Identifiers | 11-bit (standard) |
| Traffic | 18 IDs, 1071 frames per second with the ignition on |
| Termination | Not measured. Our transceiver board is stock; see the note below. |

## What the logger does

Our captures were made with an ESP32-S3 (TWAI controller) and an SN65HVD230 3.3 V transceiver
board, powered from the connector's +12 V wire through a small step-down converter, with the
controller in **normal mode**. In normal mode a
node acknowledges every frame it receives. It transmitted nothing else except the OBD-II and
UDS requests listed in [obd2.md](obd2.md) and [uds.md](uds.md), and those only in dedicated
sessions.

**Listen-only mode is untested.** We do not know whether a silent node sees traffic on this
connector. Some diagnostic connectors carry frames only while something acknowledges them. On
the Tracer 9 the connector shows frames from several units
(engine, ABS, IMU), which suggests they acknowledge one another and a silent node would work,
but that is a guess. If you try it, the result is worth an issue either way.

If you can, start in listen-only mode: it is the safer way to meet an unknown bus, and if
frames arrive you never need to leave it for a logger or a dash.

## Do not

- Do not add a 120 Ω terminator unless you have measured that the bus needs one. Many small
  transceiver boards, the common SN65HVD230 breakout among them, ship with a 120 Ω resistor
  already fitted across CAN high and CAN low. Ours is such a board, used exactly as delivered,
  so our captures were most likely made with that resistor in place, and the bus ran for
  months without errors. That shows the bus tolerates it at this connector. It does not show
  that it is right: a bus is normally terminated by its own units, and an extra terminator
  loads it. We have not measured the bus resistance. If you want to be careful, measure
  between CAN high and CAN low with the ignition off (about 60 Ω means the bus is already
  terminated at both ends) and remove the resistor from your board.
- Do not transmit broadcast IDs. The ABS, traction control and engine units listen to this bus.
- Do not send diagnostic requests while riding.
- Do not leave a device connected to the +12 V wire when the bike is parked for days. That
  wire is live with the ignition off, and a motorcycle battery is small. Unplug the logger or
  switch its supply.

## Power-up and shutdown behaviour

Frames start when the ignition is switched on. The first half second of several frames holds start-up values, described
in [bus.md](bus.md). After the ignition is switched off, every ID stops within about 0.2 s except 0x401, which
keeps going alone for at least half a minute.
