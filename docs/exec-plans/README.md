# Execution Plans

This directory contains execution plans for complex, multi-step work.

## Structure

```
exec-plans/
├── active/          ← Plans currently in progress
├── completed/       ← Completed plans, kept for historical reference
└── tech-debt-tracker.md  ← Known technical debt, tracked continuously
```

---

## Plan Format

Each execution plan should contain:

```markdown
# Plan: [Short descriptive title]
Created: YYYY-MM-DD
Status: active | completed | blocked

## Objective
One paragraph describing the goal and success criteria.

## Milestones
- [ ] Step 1: ...
- [ ] Step 2: ...

## Decision Log
*(Agent: append discoveries and trade-offs here as you work)*

## Blockers
*(If blocked, describe what is needed and by whom)*
```

---

## Usage

- **Small tasks** (< 1 day of agent work): Use `PLANS.md` at the root. No separate plan file needed.
- **Complex tasks** (multi-day, cross-domain): Create a dedicated plan file in `active/`.
- When a plan is complete, move it to `completed/` and update `tech-debt-tracker.md` if any debt was knowingly incurred.

---

## Agent Instruction

Before starting work on a complex task, check `active/` for an existing plan. If one exists,
read it fully — including the Decision Log — before proposing an approach. Plans are the
institutional memory of work in progress.
