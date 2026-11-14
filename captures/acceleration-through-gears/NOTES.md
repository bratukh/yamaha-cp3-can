# acceleration-through-gears

A pull from 16 km/h in 1st gear up to 151 km/h in 6th, on a straight road.
Look at: 0x209 B4 bits 2..0 (gear_requested; it reads 7 for a moment during each shift except 1-2), 0x209 B0:B1 (rpm), 0x205 B0:B1 (front wheel speed = raw / 101 km/h), 0x215 B2:B3 (throttle grip).
rpm drops at each upshift and the gear changes 1-2 at 2.6 s, 2-3 at 6.8 s, 3-4 at 8.5 s, 4-5 at 10.4 s and 5-6 at 26.5 s (see events.csv).
Dividing rpm by rear wheel speed gives one almost constant number per gear (about 106, 80, 67, 57, 49 and 43), which is how the gear signal was confirmed.
Odd: 5th gear lasts 16 s; the grip word peaks at 373 raw (54 % of full travel), so this is not a wide-open pull.
