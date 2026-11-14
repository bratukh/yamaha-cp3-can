# Sample captures

Short windows of raw CAN traffic from one Yamaha Tracer 9 (2022, RN70, EU), 500 kbit/s, 11-bit IDs.
Each capture is a few tens of seconds long and shows one thing a reader can verify against the signal
database in `data/signals.yaml`.

## Files in each directory

| File | Content |
|---|---|
| `capture.log` | Linux `candump -l` format, one frame per line: `(0000012.345678) can0 205#2B212B7800040000`. Time is seconds **relative to the first frame of the capture** (first frame = 0.000000), ID is 3 uppercase hex digits, data is uppercase hex without spaces. Every broadcast frame of every ID in the window is kept, in original order. The logger has 1 ms timestamp resolution, so the microsecond digits end in 000. |
| `events.csv` | `t_s,event`: things that can be checked in the data, with times relative to the capture start. Each row was derived from the decoded frames of that capture. |
| `meta.yaml` | Bike, capture month, logger, duration, frame count, frames per ID, `full_rate`, one-line description. |
| `NOTES.md` | What happens, which signals to look at, anything odd. |

The logger sat on the diagnostic connector in normal mode, so it acknowledged frames on the bus. A
`full_rate: true` capture contains every frame the bus carried (1071 frames/s over 18 IDs, 100 Hz for
the fast IDs). A capture with `full_rate: false` is decimated and says so in its notes.

## Index

| Capture | Month | Duration | Frames | Full rate | What it shows |
|---|---|---|---|---|---|
| [`cold-start-idle`](cold-start-idle/) | 2026-07 | 47 s | 50237 | yes | Cold bus wake-up, engine start and the first 30 s of idle; coolant starts at 23.75 degC and rises. |
| [`mode-and-tcs-switching`](mode-and-tcs-switching/) | 2026-05 | 24 s | 747 | no (decimated) | Standstill, engine off: the rider steps through the four riding modes twice and then the traction-control levels, engine starts at the end. Decimated log. |
| [`acceleration-through-gears`](acceleration-through-gears/) | 2026-07 | 29 s | 31061 | yes | A pull from 16 to 151 km/h with upshifts 1-2, 2-3, 3-4, 4-5 and 5-6. |
| [`corner-left`](corner-left/) | 2026-07 | 20 s | 21420 | yes | A sustained left-hand corner in 2nd gear at 47-73 km/h, yaw rate up to +13 deg/s. |
| [`corner-right`](corner-right/) | 2026-07 | 20 s | 21425 | yes | A sustained right-hand corner at 40-82 km/h, yaw rate down to -22 deg/s. |
| [`hard-braking-front-abs`](hard-braking-front-abs/) | 2026-07 | 20 s | 21422 | yes | Two hard front-brake stops in first gear (from 43 and 32 km/h) with the front ABS flag set, pressure up to 839 raw. |
| [`rear-abs-on-downshift`](rear-abs-on-downshift/) | 2026-07 | 20 s | 21420 | yes | Throttle closed, no brake applied: a 2nd-to-1st downshift at 61 km/h makes the rear wheel slow sharply (up to 16 % below the front for two frames) and sets the rear ABS flag. |
| [`shutdown`](shutdown/) | 2026-07 | 46 s | 15798 | yes | Engine idles, is switched off, the bus goes quiet and 0x401 = 0x80 is the only frame left for about 31 s. |

Reading a file: feed it to `canplayer -I capture.log`, open it with `cantools`/`python-can` (`CanutilsLogReader`),
or split each line yourself (`(time) can0 ID#DATA`).
Decode with the formulas in `data/signals.yaml` (`tools/cp3data.py` has `load`, `raw_value`, `physical`).

## Privacy

- Times are relative to the start of each capture. Only the month of recording is given. There is no clock time,
  no GPS or position data, no VIN, no vehicle or person identifier.
- Broadcast frames only. Every frame with an ID of 0x700 or above (diagnostic requests and responses) was
  removed from the source before cutting, so these files contain no OBD-II or UDS traffic.
- Windows were cut from longer recordings; nothing outside the window is included.
