# Contributing

Help is wanted. This decode comes from one motorcycle and one rider, and a good part of the
bus is still unknown. You do not need to be an expert: a log from your bike with a note of what
you did is a real contribution.

- **Not sure where to start?** Open a discussion or an issue and ask.
- **Found something unsafe or damaging in the docs?** See [SECURITY.md](SECURITY.md).
- Everyone taking part is expected to follow the [code of conduct](CODE_OF_CONDUCT.md).

Three kinds of contribution help most, in this order.

## 1. "It works on my bike" (or it does not)

Everything here comes from one 2022 base-model Tracer 9. A one-minute capture from any other
bike of the family tells us which frames are shared. Any trim, year and market counts,
including another base Tracer 9:

1. Connect a logger at 500 kbit/s ([docs/connecting.md](docs/connecting.md)).
2. Ignition on, wait ten seconds, start the engine, let it idle for a minute, blip the
   throttle once, press the rear brake once, switch the ignition off.
3. Open a "Confirm on my bike" issue and attach the log (any common format: `candump -l`,
   SavvyCAN CSV, PCAN `.trc`).

Please include model, year, market and anything fitted that the base bike lacks (quickshifter,
cruise control, semi-active suspension, heated grips, radar).

## 2. Answers to open questions

[docs/open-questions.md](docs/open-questions.md) lists what we do not know and what kind of
capture would settle each item. A capture with a note of what you did and when is enough; you
do not have to do the analysis.

## 3. Corrections and new signals

Open an issue or a pull request. For a pull request:

1. Edit `data/signals.yaml`. It is the only source; the DBC and the pages under
   `docs/messages/` are generated.
2. Run the generators and the tests:

   ```bash
   python3 -m venv .venv && . .venv/bin/activate
   pip install -r requirements-dev.txt
   python3 tools/gen_docs.py && python3 tools/gen_dbc.py && python3 tools/gen_decoder.py
   pytest
   ```

3. Say in the pull request how you know: which capture, which reference, how many events.

### What status to give

- **confirmed** needs an independent reference (dash, GPS, another sensor, a deliberate action)
  and a second recording that reproduces it. Say what the reference was in `confirmed_by` and
  give the numbers in `evidence`. A field that only ever equals another field is a copy of it,
  and a field that never changes is `unknown`.
- Anything else is a **hypothesis**. That is a perfectly good status.
- If you disprove something, mark it **ruled_out** with the reason. Do not delete it.
- A decode published for another bike is welcome as a pointer in the issue, not as evidence.

### Conventions

- Bytes are numbered from 0. Bit 7 is the most significant bit of a byte.
- Multi-byte values are big-endian unless the entry says otherwise.
- `value = raw × scale + offset`.
- Signal names are lower_snake_case and say what the thing is, not where it is, once that is
  known (`throttle_grip`, not `b2b3`).

## Captures

- Remove anything that identifies you or your bike: no GPS tracks, no VIN (it appears in UDS
  answers to `22 F1 90`), no absolute timestamps if you would rather not share when you rode.
- Say whether your logger acknowledged frames (normal mode) or only listened.
- Note the events: "t = 12 s: rear brake", "t = 30 s: mode 1 → 2". A capture with notes is
  worth ten without.

## What happens to your issue or pull request

- A capture or report gets a reply and a label (`bike-report`, `signal`, `open-question`,
  `docs`, `safety`).
- A new signal goes into `data/signals.yaml` with the status its evidence supports, usually
  `hypothesis` first. It moves to `confirmed` when a reference and a second ride back it.
- If your capture is used as evidence, you are credited in the changelog unless you ask not
  to be.
- Disagreement is fine. If two captures conflict, both are recorded and the entry says so.

## What will not be merged

This is a read-only project. See [DISCLAIMER.md](DISCLAIMER.md). No security access, no
writing or routine control, no flashing, no frame injection, no odometer, immobiliser, ABS or
emissions changes. Nothing copied from service manuals or dealer tools.

## Licence of contributions

By contributing you agree that data and documentation are published under CC BY 4.0 and code
under the MIT licence, as in the rest of the repository.
