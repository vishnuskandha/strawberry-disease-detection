# Contributing to Strawberry Disease Detection

Thanks for your interest in contributing! This project detects strawberry diseases from images using YOLOv8.

## Getting started

1. Fork the repository and clone your fork.
2. Create a feature branch from `main`:

   ```bash
   git checkout -b feature/your-change
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Development workflow

- Keep changes focused and atomic; one logical change per pull request.
- Follow PEP 8 style for Python and keep the existing code conventions.
- Run a syntax check before committing:

  ```bash
  python -m compileall -q .
  ```

- Do not commit model weights, training runs, or dataset files. `.gitignore` already excludes `*.pt`, `runs/`, `yolo/`, `__pycache__/`, and the raw dataset splits.
- If you change the training or inference scripts, test them on a small subset (low `epochs`, a single image) before opening the PR.

## Committing

- Use clear, imperative commit messages (for example: `Add ONNX export script`).
- Keep the working tree free of derived artifacts before committing.

## Pull requests

- Open your PR against `main` with a description of the change and, where relevant, what you verified.
- CI runs a syntax check and installs `requirements.txt`; make sure it passes.
- Reference any related issue in the PR description.

## Reporting bugs and requesting features

Use the issue templates in `.github/ISSUE_TEMPLATE/` for bug reports and feature requests. For security issues, follow [SECURITY.md](SECURITY.md) instead.
