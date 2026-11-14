# corner-right

A sustained right-hand corner at 44-50 km/h that starts at about 8 s; speed over the whole capture is 40-82 km/h.
Yaw rate (0x254 B4:B5, positive = left) goes negative and reaches -22 deg/s (raw 27760) at 12.6 s, about 46 km/h.
Look at: 0x254 B4:B5, 0x205 B0:B1. Reconstructed lean is about 25 to 30 degrees at the peak (docs/lean-reconstruction.md).
The rider downshifts 3 -> 2 at about 6 s, shortly before the corner (0x209 B4 reads 7 briefly).
Odd: the yaw word is noisy from frame to frame; the events use a 0.4 s average.
