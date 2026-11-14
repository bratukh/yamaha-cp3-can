## What changes

<!-- One or two sentences. Which CAN ID, signal or page. -->

## How you know

<!-- Which capture, which reference (dash, GPS, another sensor, a deliberate action), how many
events, which bike (model, year, market). "Hypothesis, no reference yet" is a fine answer. -->

## Checklist

- [ ] Signal changes are in `data/signals.yaml`, not in the generated files
- [ ] `python3 tools/gen_docs.py && python3 tools/gen_dbc.py && python3 tools/gen_decoder.py` run, and the results are in this pull request
- [ ] `pytest` passes
- [ ] The status follows the rule in CONTRIBUTING.md (`confirmed` needs an independent reference and a second ride)
- [ ] Captures contain no GPS data and no VIN
- [ ] Nothing here writes to the motorcycle (see DISCLAIMER.md)
