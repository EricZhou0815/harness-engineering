# Design Docs Index

This directory catalogues architectural decisions, design rationale, and the core operating
beliefs of the system. It is the institutional memory of the project — available to every agent.

> **Agent instruction**: Before proposing any design that deviates from existing patterns,
> check this index first. If a similar decision was made previously, read it. If not, create a
> new design doc after the fact to record the decision.

---

## Index

| Document                                    | Status    | Summary                                                  |
|---------------------------------------------|-----------|----------------------------------------------------------|
| [core-beliefs.md](./core-beliefs.md)        | ✅ Active  | The fundamental agent-first operating principles         |
| *(Add new design docs here as they are created)* |       |                                                          |

---

## How to Add a Design Doc

1. Create a new `.md` file in this directory with a descriptive name (e.g., `event-sourcing-for-audit-log.md`)
2. Add a row to the index table above
3. Include the following sections in the document:
   - **Context**: What problem is this solving?
   - **Decision**: What did we decide?
   - **Alternatives Considered**: What else did we evaluate?
   - **Consequences**: What trade-offs does this introduce?
   - **Verification Status**: Is this still the active approach?

---

## Verification Policy

A doc-gardening agent runs on a regular cadence to check for stale documentation.
Any design doc not updated within 90 days is flagged for review. If the decision
is still accurate, update the `Last Verified` date. If not, supersede it with a new doc.
