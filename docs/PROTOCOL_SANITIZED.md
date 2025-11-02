# PROTOCOL (SANITIZED)

Status: DRAFT
Author: Automated assistant (suggested edits)
Date: 2025-11-02

Purpose
-------
This document is a sanitized, actionable consolidation of several internal design and prompt-engineering documents. It extracts practical, implementable guidance while clearly labeling and isolating speculative, experimental, or fictional content.

Goals
-----
- Provide a single, safety-conscious reference for developers and contributors.
- Preserve visionary/experimental ideas but mark them clearly so they are not executed accidentally.
- Replace language that suggests bypassing safety, privacy, or policy guardrails.

Principles
----------
- Safety-first: remove or reword instructions that imply bypassing platform or legal safeguards.
- Explicit labeling: any experimental or fictional tool/command must be marked with the header "EXPERIMENTAL / CONCEPTUAL" and not presented as runnable.
- Realism: replace absolute or unattainable targets ("100% coverage", "unlimited") with measurable ranges and actionable steps.
- Auditability: require an Architecture Decision Record (ADR) for major changes (new databases, biometric auth, etc.).

Sanitized summary (actionable)
-------------------------------
The following sections are practical guidance that can be acted on now by the project team.

1. Development environment
   - Use a virtual environment for Python projects (`.venv`) or node virtual environments as appropriate.
   - Document exact setup steps in `README.md` and `docs/dev-setup.md`.
   - Keep dependency manifests (`requirements.txt`, `package.json`, etc.) up-to-date and pinned where possible.

2. Recommended stack (example)
   - Frontend: Next.js (stable release) with React + Tailwind CSS. Use TanStack Query for server state, Jotai/Zustand for local state.
   - Backend: Node.js (LTS) + TypeScript. Use Express or Fastify for REST endpoints; Apollo Server for GraphQL where required.
   - Database: PostgreSQL for transactional data; Redis for caching; a vector DB (e.g., Milvus or Pinecone) only after an ADR and cost analysis.

3. CI/CD & testing
   - Use GitHub Actions (or equivalent) for CI with stages for lint, unit tests, integration tests, and security scanning.
   - Write unit tests (Jest for JS/TS) and at least one integration test per public API surface (Supertest/Cypress for E2E).
   - Track coverage per package/module. Set realistic target ranges (example: aim for 70–90% coverage depending on module criticality).

4. Security & privacy
   - Use OWASP Top 10 as a baseline. Run automated SAST/DAST tools and dependency scanners (Dependabot, Snyk) in CI.
   - Before implementing any biometric or sensitive-data feature, require a legal/privacy review and a security ADR.
   - Do not include any instructions that attempt to disable platform safety checks or bypass policies.

5. Documentation & governance
   - Split content into `docs/` subfolders: `design/`, `operational/`, `experimental/`, `adr/`.
   - Maintain an ADR for any major technical decision. Use the template in `docs/adr/0001-template.md` (see repository suggestions).

Experimental / Conceptual (clearly labeled)
-------------------------------------------
The original documents contained a number of visionary and speculative ideas (quantum computing, "reality manipulation", fictional CLI tools). These are preserved below under a clearly labeled section to capture creative thinking while preventing accidental implementation.

EXPERIMENTAL / CONCEPTUAL — Examples
 - "quantum-dev init", "quantum-deploy": Conceptual placeholders for future infra automation. Do not attempt to run.
 - Claims like "1M token context" or "unlimited token limit": mark as aspirational; record as R&D objectives if you plan on pursuing large-context LLM architectures.
 - "Brainwave/DNA authentication": requires legal/regulatory review; treat as research notes only.

How to treat speculative proposals
---------------------------------
1. Tag files with `EXPERIMENTAL` in filename or header and move them to `docs/experimental/`.
2. Require an ADR plus risk assessment and budget estimate before any experimental idea moves to implementation.
3. If code or scripts appear to implement experimental features, add a comment header clearly indicating "DO NOT RUN — EXPERIMENTAL / FICTIONAL".

Prompt templates and safety
--------------------------
If the repository includes system prompts intended to interact with LLMs, follow these rules:
- Provide a "safe" variant that enforces policy constraints, failure modes, and refusal behavior.
- Avoid any wording that asks the model to ignore policy or safety restrictions. Replace "unrestricted" with "privileged (policy-enforced)" where necessary.
- Include an explicit contract describing inputs, outputs, allowed data exfiltration, and logging requirements.

Example of a short safe contract (for any LLM system prompt):
- Input: user_message (string), metadata (source, timestamp)
- Output: JSON object with keys {status, content, warnings}
- Error modes: if the model is asked for disallowed content, return status="refused" with a brief explanation

Operational recommendations (next steps)
----------------------------------------
1. Create `docs/experimental/` and move all speculative docs there with an `EXPERIMENTAL` header.
2. Add `docs/PROTOCOL_SANITIZED.md` (this file) as the canonical, safety-first implementation guide.
3. Add an ADR template at `docs/adr/0001-template.md` and require ADRs for major decisions.
4. Add a short `docs/USAGE_README.md` that points contributors to the sanitized doc and the experimental area.

Security & compliance notes
---------------------------
- Biometric data: do not store or process without explicit consent, secure storage, and a privacy/data-protection assessment.
- Cryptography claims: use vetted, standard libraries (e.g., libsodium, WebCrypto). Do not rely on unverified or fictional algorithms described as "quantum-safe" without external review.

Appendix: quick action checklist
-------------------------------
- [ ] Move speculative files to `docs/experimental/` and add headers.
- [ ] Create ADR template and require ADRs for new infra/services.
- [ ] Add a short README summarizing where to find safe vs experimental material.
- [ ] Create a "safe prompt" variant and place it in `docs/prompt_safeguard.md`.

Contact
-------
If you want, I can implement the following now:
- Create `docs/USAGE_README.md` (summary & links)
- Add `docs/adr/0001-template.md`
- Create `docs/prompt_safeguard.md`

Pick one or say "create all" and I will add the selected files to the repository.
