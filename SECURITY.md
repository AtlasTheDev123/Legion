# Security & Safe-Run Guidelines

This repository contains modules and stubs that are potentially dangerous if run outside an isolated and authorized environment. Follow these rules:

- Never run network scans, malware analysis, or any code that interacts with external networks on a production or public network. Use an air-gapped lab or dedicated isolated environment.
- Do not store real secrets or API tokens in the repository. Use environment variables, OS keyrings, or a secrets manager.
- Sensitive modules must require explicit confirmation and an environment variable `ALLOW_DESTRUCTIVE_ACTIONS=true` to run. Search for `ALLOW_DESTRUCTIVE_ACTIONS` in the codebase.
- For sandboxed code execution, ensure containers use strict seccomp, no network access, and resource limits (CPUs, memory, disk). Prefer hardware virtualization for malware analysis.
- To report a security issue, open a private issue and tag @ENZOxNINJA; avoid posting sensitive details publicly.

If you are unsure whether to run a module, ask a security reviewer or run in an isolated disposable VM.
