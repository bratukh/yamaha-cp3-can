# Changelog

Versions follow semantic versioning for the data: a major version changes an ID, an address or
a scale of a confirmed signal; a minor version adds signals or promotes a status; a patch fixes
text. The DBC `VERSION` equals the repository tag.

## 0.1.0 — unreleased

First public version.

- 18 broadcast frames of the 2022 Tracer 9: 9 with confirmed signals, 4 partly understood,
  5 not decoded.
- Lean angle reconstruction from yaw rate and wheel speed, with its measured error.
- OBD-II: supported-PID masks and 18 confirmed PIDs. UDS: two control units and their
  identification data.
- Generated DBC, a dependency-free Python decoder, sample captures.
