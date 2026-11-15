# Lean angle from yaw rate and speed

The Tracer 9 has a six-axis inertial unit and uses it for cornering ABS and traction control,
but we found no plain lean angle value in any of the 18 broadcast frames, after comparing
every byte and 16-bit word with a reference on two rides.

The angle can still be had from two signals that are on the bus: yaw rate and wheel speed.

## The formula

```
yaw  = (0x254 B4:B5) - 30000          raw counts, positive in a left turn
v    = (0x205 B0:B1) / 101.0 / 3.6    front wheel speed in m/s
lean = atan(yaw * v / 45873)          radians, positive to the left
```

In C:

```c
float lean_deg(uint16_t yaw_raw, uint16_t front_wheel_raw)
{
    float yaw = (float)yaw_raw - 30000.0f;
    float v   = front_wheel_raw / 101.0f / 3.6f;
    return atanf(yaw * v / 45873.0f) * 57.29578f;
}
```

## Why it works

A motorcycle in a steady corner leans until gravity and the centripetal force balance:

```
tan(lean) = v * ω / g
```

where `ω` is the rate at which the heading changes and `v` the speed. The yaw gyro gives `ω`
and the wheel gives `v`.

The accelerometer cannot do this job. In a balanced corner the resultant force points straight
down through the bike, so the lateral axis reads close to zero however far the bike leans. On
this bike the lateral word moves 17.4 counts per degree when the parked bike is tilted and
only a few counts per degree in a corner (our estimates run from 2 to 4).

## Why the constant is 45873 and not 56200

The gyro scale is about 100 counts per degree per second (see [imu.md](imu.md)), so the
textbook formula would use `g × 100 × 57.3 = 56 200`. The constant that matches measured lean is
about 18 % smaller.

Possible reasons, none of them measured separately:

- The gyro is fixed to the bike. A leaned sensor sees only `ω × cos(lean)` on its yaw axis and
  the rest on its pitch axis.
- A real tyre has width. The contact patch moves to the side as the bike leans, so the bike
  must lean further than the point-mass formula says.
- The rider and the bike do not lean by the same amount.

The first effect depends on the angle itself (for a sensor fixed to the frame the exact
relation is `sin(lean) = v × ω_sensor / g`), so a single constant inside `atan` can only
approximate it over the range it was fitted on.

The constant is therefore empirical. It belongs to the wheel-speed scale it was fitted with:
if you change one, change the other (`constant × speed scale` stays the same).

## How it was checked

Reference: a phone fixed to the bike above the dash, behind the windscreen ([photo](imu.md#what-all-of-this-rests-on)), recording its attitude at 50 Hz and GPS at 1 Hz,
on one ride of about an hour. Log and phone were aligned in time by cross-correlating speed.

Steady corners (lean above 8°, roll rate under 3°/s, speed above 30 km/h, 197 s in total):

| | |
|---|---|
| Slope, reconstructed against phone | 0.99 |
| Residual standard deviation | 2.8° |
| Correlation | 0.98 |
| Constant refitted on this ride | 47 000 to 51 000 depending on the estimator |

The table uses 45873, the constant in the formula above. It was fitted earlier against the
filmed phone level in slow corners (13–24 km/h) and rescaled when the wheel-speed scale was
corrected. Fitting the constant directly on this ride gives 47 000 by least squares on the
angle and 47 700–51 100 from a block bootstrap, 2–11 % above the value we use, even though the
slope with 45873 is 0.99. The two statements weight the data differently and we have not
reconciled them. Since the formula also reads low at the speeds of the original fit, part of
the early agreement may be luck. Treat the constant as uncertain by about 10 %.

By lean angle the ratio is 1.03 at 8–15°, 1.02 at 15–22° and 0.95 at 22–30°. By speed it is
0.96 at 30–60 km/h, 1.02 at 60–90 and 1.01 at 90–120.

A second check needs no phone. In a steady corner the bike's own pitch gyro reads
`−yaw × tan(lean)`, so `atan(−pitch / yaw)` is another estimate of the lean. It reads 4 %
(`corner-left` capture) to 7 % (`corner-right`) higher than the formula above, which points the
same way as the refit. This check assumes the pitch and yaw gyros have the same scale, and that
equality is itself inferred from this geometry, so it is a consistency check and not an
independent measurement.

The sign was checked against the GPS course: a left turn raises the raw yaw word in 15 of 15
turns.

## Where it is wrong

| Situation | What happens |
|---|---|
| Below 30 km/h | Reads about 13 % low. Steering angle matters at walking pace. |
| Quick left-right transitions | Peaks overshoot by about 9 % (median). The formula assumes a balanced corner. |
| Straight line | Reads a few degrees of noise: up to 4° at the 95th percentile where the phone shows under 2°. |
| Standstill | Always 0. A parked, tilted bike has no yaw rate. Use the static formula in [0x250](messages/0x250.md). |
| Above 30° of steady lean | Not validated. The reference ride has almost no data there; the one hard moment read 29° against the phone's 36°. |
| Above 120 km/h | 17 seconds of data. Not validated. |

A filter helps on the road. We use a first-order low-pass with a time constant of 0.3 s. Our
records do not say for certain whether the comparison above used filtered or unfiltered
values; in steady corners the difference is small.

## What to make of it

For a dash, an overlay or ride statistics it is good enough: the residual standard deviation
in ordinary cornering is 2.8°, so about one reading in three is more than 3° off. A repeat on
a cold day, with the phone on the handlebar and only data above 40 km/h (up to 18° of lean,
two recordings), gave 0.97 and 0.94 × the phone angle, r 0.96: the same answer within about
5 % on a different day, mount and tyre temperature, so the constant was left as it is.
It is not a measurement instrument. The reference is a phone whose attitude is itself a sensor
fusion. It was fixed to the bike's body, not to the handlebar, so steering did not move it; the
main validation is one ride, one rider, one set of
tyres.

A better estimate should be possible by integrating the roll rate and correcting it with this
formula, which is what the bike's own controller presumably does. The frames
[0x258](messages/0x258.md) and [0x25C](messages/0x25C.md) are not decoded yet and may contain
exactly that. See [open-questions.md](open-questions.md).
