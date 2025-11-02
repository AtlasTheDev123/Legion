# Usage README — where to find sanitized vs experimental material

This repository contains a mix of actionable developer guidance and exploratory/vision notes. To avoid accidental implementation of speculative ideas, follow these rules:

- Canonical, actionable guidance: see `docs/PROTOCOL_SANITIZED.md` — this file contains the safety-first, implementable protocol and recommended practices.
- Experimental / Conceptual material: files that contain speculative tools, fictional CLI commands, or research ideas are collected under `docs/experimental/` (or, if not already moved, flagged with `EXPERIMENTAL` headers). These are for reading and discussion only; do not attempt to run commands shown there without verification.

Quick links

- `docs/PROTOCOL_SANITIZED.md` — sanitized protocol (actionable)
- `docs/WSL_SETUP.md` — WSL setup and bootstrap script usage
- `docs/prompt_safeguard.md` — suggested policy-compliant prompt template and contract
- `docs/adr/` — architecture decision records (add ADRs here before major changes)
- `docs/experimental/` — (if present) exploratory/vision documents

Contributing

1. If you add a new experimental idea, add it under `docs/experimental/` and include an `EXPERIMENTAL` header.
2. If you propose a change to infra, DB, or auth mechanisms, create an ADR in `docs/adr/` first.
3. For code changes, follow the repository's normal contribution process (PRs, CI checks, code review).

Contact

If a document's intent is unclear (actionable vs experimental), open an issue and tag @maintainers for clarification.
