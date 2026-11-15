# mode-and-tcs-switching

Decimated capture: the source logger recorded only frames whose bytes changed, so there are no regular 100 Hz series here. Frame counts are small and gaps are normal.
The bike stands still with the engine off (front wheel speed 0 in every frame) until the engine is started at 20.6 s.
Riding mode steps D-MODE 4 -> 3 -> 2 -> 1, jumps back to 4 and steps down again to 1 (twice in total, about 1 s per step).
Then the traction-control level goes M -> 2 -> 1 -> M.
Look at: 0x226 B0 bits 7..6 (mode, raw 0 = D-MODE 1 ... 3 = D-MODE 4) and 0x226 B3 (TCS mode, 1 = TCS 1, 2 = TCS 2, 3 = TCS M).
The mode is copied in 0x209 B4 bits 7..6 and in 0x215; the copies follow 0x226 by about 10 ms.
0x209 B3 bits 4..1 and 0x226 B0 bits 3..2 carry the TCS level in effect, not the mode. Here they equal the mode, because the rider's M setup at the time had TCS level 3.
TCS OFF was never selected, so its code is not in this capture.
