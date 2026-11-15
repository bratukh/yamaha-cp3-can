# hard-braking-front-abs

Two hard stops in first gear: from 43 to about 14 km/h, and again from about 32 to 16 km/h.
Front brake pressure (0x260 B0:B1) peaks at 839 raw in the first stop; the front ABS flag (0x268 B4 bit 1) goes on at 771 raw and off 0.65 s later.
In the second stop the flag comes on at 394 raw while the pressure is still rising (peak 765 raw) and stays on for 1.1 s.
Look at: 0x260 B0:B1 (B4:B5 repeat it), 0x268 B4 bit 1, 0x205 B0:B1 (front wheel speed falls steeply), 0x209 B0:B1 (rpm).
Odd: the ABS flag does not come on at the moment of peak pressure but while the wheel is already slowing; compare it with the front wheel speed.
Note: the rear brake pedal bit (0x268 B4 bit 2) is also on during both stops, so these are not front-brake-only stops.
