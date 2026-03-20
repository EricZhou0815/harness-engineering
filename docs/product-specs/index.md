# Product Specs Index

This directory contains detailed product specifications. Each spec describes what a
specific feature or user journey is intended to do — including edge cases, acceptance
criteria, and explicit out-of-scope items.

> **Agent instruction**: Before implementing any user-facing feature, find the relevant
> spec here. If no spec exists, create a stub and escalate to a human to fill it in before
> proceeding. Do not invent scope.

---

## Index

| Document                                                | Status     | Summary                                              |
|---------------------------------------------------------|------------|------------------------------------------------------|
| [new-user-onboarding.md](./new-user-onboarding.md)     | 🚧 Draft   | First-run experience for new users                   |
| *(Add new specs here as they are created)*              |            |                                                      |

---

## Spec Format

Each spec should contain the following sections:

```markdown
# Spec: [Feature Name]
Status: draft | ready | shipped
Last Updated: YYYY-MM-DD

## User Story
As a [user type], I want [goal] so that [outcome].

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Edge Cases
- What happens if [X]?
- How do we handle [Y]?

## Out of Scope (this phase)
- Explicit non-goals

## Open Questions
- [ ] Question that needs a human decision before implementation
```
