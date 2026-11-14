# shutdown

The capture starts with the engine idling at about 1400 rpm and the bike stationary; the last frame with rpm above 0 is at 13.65 s.
The other IDs stop in steps between 14.38 s (IMU frames first) and 14.585 s (0x260 and 0x268 last); 0x401 changes from 0x00 to 0x80 at 14.494 s, while the last of them are still running.
Afterwards 0x401 = 0x80 is the only frame on the bus, every 100 ms, until the end of the capture 31.5 s later; the capture ends with it still sending.
Look at: 0x401 B0 bit 7, the last frame of 0x209 and 0x205, and the 100 ms spacing of 0x401.
Odd: the bike is stationary all along and gear position reads 0 (neutral) in 0x209 B4 bits 2..0 for the whole capture.
