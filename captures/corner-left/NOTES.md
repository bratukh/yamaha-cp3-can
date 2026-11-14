# corner-left

A sustained left-hand corner on a road in 2nd gear, wheel speed 47-73 km/h.
Yaw rate (0x254 B4:B5, zero at 30000, 100 counts per deg/s, positive = left) sits around +10 deg/s for about 7 s and peaks at +13 deg/s.
Look at: 0x254 B4:B5, 0x205 B0:B1 (speed). The lean angle is not on the bus; reconstructing it with atan((yaw_raw - 30000) x v / 45873), v in m/s, gives roughly 20 degrees here (docs/lean-reconstruction.md).
0x254 B0:B1 (roll rate) and B2:B3 (pitch rate) are in the same frame.
Odd: this is the cleanest left corner in the source that stays between 40 and 100 km/h; a sharper left turn exists below 40 km/h and is not used.
