# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | Yes       |

## Reporting a vulnerability

If you discover a security issue in this repository, please do **not** open a public issue. Report it privately by emailing the maintainer (see the author in [CITATION.cff](CITATION.cff) or GitHub profile), or by opening a draft GitHub Security Advisory via the repository's **Security** tab.

Please include:

- A description of the vulnerability and its impact
- Steps to reproduce, including any relevant files or commands
- The version(s) affected

You should receive a response within a few business days. After triage, the issue is fixed on a private branch and released, and the report is credited (unless you prefer to remain anonymous).

## Security notes for this project

- Model weights (`*.pt`, `*.onnx`, `*.engine`, `*.tflite`) are untrusted binaries; only load weights you trained yourself or that come from a trusted source.
- This project downloads `yolov8n.pt` from Ultralytics at first training run. Keep the `ultralytics` package up to date.
- Do not run untrusted images or converted datasets through inference without scanning them first.
