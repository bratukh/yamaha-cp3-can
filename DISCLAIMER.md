# Disclaimer

## This is a read-only project

Everything here was learned by listening to the bus and by sending standard
read-only diagnostic requests. The repository contains no way to change
anything on the motorcycle, and will not accept one.

Requests that are in scope:

- OBD-II modes 01, 02, 03, 06, 07, 09 and 0A.
- UDS `0x22` ReadDataByIdentifier and `0x19` ReadDTCInformation.
- UDS `0x10` DiagnosticSessionControl, default (`0x01`) and extended (`0x03`).
- UDS `0x3E` TesterPresent.

Out of scope, and not welcome in issues or pull requests:

- SecurityAccess (`0x27`), seed/key material, or ways around it.
- Writing data (`0x2E`), I/O control (`0x2F`), routines (`0x31`), ECU reset
  (`0x11`), clearing fault codes (`0x14`), communication control (`0x28`).
- Programming sessions and flashing (`0x10 0x02`, `0x34`–`0x37`, `0x3D`).
- Injecting or spoofing broadcast frames.
- Changing odometer, immobiliser, ABS, traction control or emissions behaviour.

## Your motorcycle, your risk

A CAN node that is wired or configured wrongly can disturb the bus. The bus
carries ABS, traction control and engine messages. Check your wiring before you
turn the key, do not debug while riding, and stop if the dash shows a warning
you did not have before.

The information is provided as is, with no warranty of any kind. It comes from
one motorcycle (see the tested-vehicles table in the README). Other model
years, markets and trim levels may differ. Signals marked `hypothesis` or
`unknown` are exactly that. The authors accept no liability for damage, injury,
loss of warranty or legal consequences that follow from using it.

Keep your motorcycle road-legal. Do not use this information to defeat
type-approved safety or emissions systems.

## Trademarks and manufacturer material

Yamaha, Tracer, MT-09, XSR900, Niken and YZF-R9 are trademarks of Yamaha Motor
Co., Ltd. This project is not affiliated with, endorsed by or supported by
Yamaha Motor Co., Ltd. or any of its suppliers. The names are used only to say
which motorcycles the data applies to.

Nothing here is copied from service manuals, dealer tools or other
manufacturer documents. If you believe something in this repository infringes
your rights, open an issue and it will be looked at promptly.
