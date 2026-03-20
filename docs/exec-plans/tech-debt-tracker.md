# Technical Debt Tracker

This file tracks known technical debt. It is updated by agents after completing work that
knowingly incurs debt, and by the recurring cleanup (doc-gardening) process.

Each debt item is a high-interest loan: it is almost always better to pay it down
continuously in small increments than to let it compound and tackle it in painful bursts.

---

## Active Debt

| ID    | Domain   | Description                                           | Incurred    | Priority | Fix Plan                        |
|-------|----------|-------------------------------------------------------|-------------|----------|---------------------------------|
| *(none yet — add entries as they arise)*              |             |          |                                 |

---

## Resolved Debt

| ID    | Domain   | Description                                           | Resolved    | Resolution Summary              |
|-------|----------|-------------------------------------------------------|-------------|---------------------------------|
| *(none yet)* |    |                                                       |             |                                 |

---

## Debt Entry Format

When adding a new debt item, include:

```markdown
| TD-001 | auth | JWT refresh tokens not yet revocable on logout | 2026-03-20 | High | Implement token blacklist in Redis — see exec-plans/active/td-001-jwt-revocation.md |
```

**Priority levels:**
- **Critical**: Causes data loss, security vulnerability, or blocks users
- **High**: Degrades reliability or significantly increases future maintenance cost
- **Medium**: Suboptimal but safe; should be addressed within the next quarter
- **Low**: Style or preference; address opportunistically

---

## Recurring Cleanup Instructions

On a regular cadence, a background cleanup agent should:
1. Scan for code patterns that deviate from `GOLDEN_PRINCIPLES.md`
2. Check for documentation that does not reflect real code behavior
3. Update quality grades in `QUALITY_SCORE.md`
4. Open targeted refactoring PRs for each discrete debt item found
5. Mark items as resolved in this tracker once PRs are merged
