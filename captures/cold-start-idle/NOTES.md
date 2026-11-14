# cold-start-idle

The bus wakes at t=0 with the engine off. 0x23A B0 reads 0x04 for the first two seconds and then 0x00.
0x209 B4 shows the wake pattern 0x48, 0x08, 0x00 in the first 0.6 s; ignore 0x209 until it has settled.
The first 0x226 frame is a power-on placeholder (05 01 00 01 00 25 28); real values follow within a few milliseconds.
The engine is cranked at about 15.9 s: 0x209 B3 bit 0 (start flag) is set for about 0.8 s, rpm leaves 0 at 16.2 s and passes 1000 about 0.3 s later.
Look at: 0x209 B0:B1 (rpm = raw x 0.390625), 0x209 B3 bit 0, 0x23E B0 (coolant = raw x 0.625 - 30), 0x23A B0.
Coolant reads 23.75 degC at the start and 28.1 degC at the end; 0x23E is sent once per second, so it moves in 0.625 degC steps.
Gear position (0x209 B4 bits 2..0) reads 0, neutral, after the wake pattern; wheel speeds are 0 throughout.
Odd: 0x23A B0 is back to 0x00 about 14 s before the engine is cranked, so it does not tell a running engine from a stopped one.
