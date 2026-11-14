# rear-abs-on-downshift

Engine braking from 92 km/h with the throttle closed and no front brake (pressure 0-6 raw around the event). The gear drops 3 -> 2 at 3.2 s and 2 -> 1 at 6.6 s at 61 km/h.
At 6.608 s the rear wheel word (0x205 B2:B3) drops 9.9 km/h below the front word and 10 ms later 0x268 B4 bit 0 (rear ABS) turns on; it stays on for 0.5 s.
Look at: 0x205 B0:B1 against B2:B3, 0x268 B4 bit 0, 0x209 B4 bits 2..0 (gear), 0x209 B0:B1 (rpm jumps from 4880 to 6090 across the shift).
The wheel-speed dip lasts two frames (-9.9 and -8.5 km/h at 10 ms spacing), then the rear word is within 3 km/h of the front again.
Odd: the rear ABS flag also comes on when the rear wheel slows sharply with no brake applied, which is why this event is a good test for it.
