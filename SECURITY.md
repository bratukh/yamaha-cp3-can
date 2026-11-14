# Safety and security

This repository documents how to read a motorcycle's CAN bus. It contains no software that
runs on the motorcycle's own control units.

## Reporting a safety problem

Please open an issue marked **safety** straight away if you find that something documented
here:

- is wrong in a way that could damage a bike or mislead a rider (a swapped pin, a wrong
  voltage, a signal that a display should not trust), or
- disturbs the bus when done as described (warning lights, fault codes, limp mode).

Say what you did, on which bike, and what happened. Safety reports are handled before
anything else.

## What we will not publish

If you have found a way to write to a control unit, bypass security access, change the
odometer or defeat ABS, traction control, the immobiliser or emissions systems, do not post it
here. It is outside the scope of this project (see [DISCLAIMER.md](DISCLAIMER.md)) and such
issues will be closed and removed. Consider reporting it to the manufacturer.
