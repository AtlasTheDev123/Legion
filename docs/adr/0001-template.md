# ADR 0001: [Title] — Example ADR template

Status: proposed
Date: 2025-11-02
Deciders: [Team or person name]
Reviewers: [Reviewer list]

Context
-------
Briefly describe the background and why a decision is required. Include constraints, alternatives considered, and relevant costs or timelines.

Decision
--------
State the decision that has been made. Be specific about which components will change and how.

Consequences
------------
Describe the implications of the decision, including migration steps, roll-back plan, monitoring, and any compliance considerations.

Alternatives considered
-----------------------
- Alternative A — short pros/cons
- Alternative B — short pros/cons

Implementation plan
-------------------
Step-by-step tasks, owners, and estimated effort.

Related documents
-----------------
- Link to design docs, cost estimates, security reviews, and tickets.

Example
-------
Title: Use vector DB for embeddings

Status: proposed

Context: We need a cost-effective vector DB for semantic search. Options are Milvus, Pinecone, or a managed service.

Decision: We will pilot Milvus for 3 months in a non-production environment. If performance and cost targets are met, we will open an ADR for production adoption.

Consequences: Requires extra infra and backups; security review required before production.
