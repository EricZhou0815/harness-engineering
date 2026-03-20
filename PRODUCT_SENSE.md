# PRODUCT_SENSE.md — Product Context & Scope

> ⚠️ **AGENT: DO NOT PROCEED if this file contains `[REQUIRED]` placeholders.**
>
> This file is the primary defence against hallucinated scope. If the product context
> below is not filled in, you have no ground truth and will build the wrong thing.
> Surface this to the human and **stop** until it is complete.

---

## Mission Statement

**[REQUIRED — Replace this line with 1–2 sentences describing the product's core purpose and who it is for.]**

Example: *"A compliance automation tool for agricultural businesses that converts regulation PDFs into
structured digital forms, enabling farmers to submit field data and generate audit-ready reports."*

---

## Core Values (Priority Ordered)

These are ranked. When trade-offs arise, the higher item wins.

1. **Reliability > Features**: Core flows must never randomly fail. A working subset beats a broken whole.
2. **Speed Metrics > Aesthetics**: Fast feedback loops, instant layout rendering, sub-100ms API responses where possible.
3. **Correct Data > Convenient Data**: Never guess, coerce, or silently normalise data that should be validated. Surface the error.

**[REQUIRED — Adjust these rankings if they don't match your actual product priorities.]**

---

## User Journeys (Critical Paths)

List the 3–5 user journeys that are the core value of the product. These are the flows
that must never break and that every agent should understand deeply.

**[REQUIRED — Fill these in. Example format:]**

1. **[Journey name]**: User does X → system does Y → user sees Z. Critical because: ...
2. **[Journey name]**: ...
3. **[Journey name]**: ...

---

## Critical Business Logic

Describe the non-obvious rules that govern how the product behaves. These are the things
that would surprise a developer who only read the UI.

**[REQUIRED — Fill in the rules that agents must know to avoid building broken features.]**

Examples of what to document here:
- How are conflicts resolved when two users edit the same record?
- What triggers a downstream notification or event?
- What must happen atomically, and what is eventually consistent?
- What data is immutable once created, and why?

---

## Edge Cases That Must Be Handled

**[REQUIRED — List the edge cases with explicit handling instructions.]**

| Situation                          | Required behaviour                                      |
|------------------------------------|---------------------------------------------------------|
| Network timeout during form submit | [e.g., queue locally via service worker, retry on reconnect] |
| Duplicate form submission          | [e.g., use idempotency key, silently deduplicate]        |
| User loses session mid-flow        | [e.g., preserve unsaved state in localStorage]           |
| *(add your project's edge cases)*  |                                                         |

---

## Explicit Scope Constraints (What NOT to Build)

To prevent over-engineering, the following are **explicitly forbidden** in the current phase.
An agent that builds any of these without a new approved spec is out of scope.

**[REQUIRED — Replace the examples below with your actual non-goals.]**

- ❌ No admin dashboards or analytics tracking
- ❌ No soft-deletion mechanisms — destructive operations are hard-deletes
- ❌ No real-time WebSocket syncing unless explicitly ordered in `PLANS.md`
- ❌ No multi-tenancy or per-organisation data isolation
- ❌ No mobile-native (iOS/Android) implementations — web only

---

## Approved Technology Decisions

List any technology choices that are locked in and must not be renegotiated:

**[REQUIRED — Fill in your project's stack.]**

| Concern              | Decision                         | Rationale                          |
|----------------------|----------------------------------|------------------------------------|
| Language             | [e.g., TypeScript / Python]      | [why]                              |
| Framework            | [e.g., Next.js / FastAPI]        | [why]                              |
| Database             | [e.g., PostgreSQL]               | [why]                              |
| Auth                 | [e.g., Clerk / Auth.js]          | [why]                              |
| Deployment           | [e.g., Railway / Vercel]         | [why]                              |

---

## Open Questions (Requiring Human Decision)

Document any unresolved questions that block agent progress. An agent that encounters
something in this list must **stop and wait** — not guess.

**[Fill in as questions arise during development.]**

- [ ] *No open questions yet.*
