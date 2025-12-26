# scripts: how to run upgrade_repo.sh

This repository includes a safe, dry-run upgrade and analysis script at `scripts/upgrade_repo.sh`.

Basic usage:

```
# dry-run (default) - does NOT create venv or install packages
bash scripts/upgrade_repo.sh

# install mode: create venv and install pinned requirements (network required)
bash scripts/upgrade_repo.sh --install
```

What it does (dry-run):
- ensures `.env` exists (copies from `.env.example` if missing)
- runs lint/type checks if tools are installed (ruff/black/mypy)
- validates key JSON manifests (`functions.json`, `schemas/functions.json`)
- runs a heuristic secrets scan and reports findings
- creates an archive snapshot in `/tmp` if `zip` is available

The `--install` flag will create a `.venv` and attempt to install `requirements-lock.txt` or `requirements.txt`.

Note: This script is intentionally conservative and avoids destructive actions. Review `SECURITY.md` before running anything that performs network scans or writes to external services.
