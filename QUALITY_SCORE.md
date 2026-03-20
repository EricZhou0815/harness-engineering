# QUALITY_SCORE.md — Domain Quality Scorecard

This file grades each product domain and architectural layer. It is the current-state
assessment of quality, updated by the recurring doc-gardening / cleanup agent.

**This is not aspirational.** Grades reflect real observed state. If a grade is wrong,
fix the underlying code and update the row — do not upgrade the grade speculatively.

For the testing harness *philosophy*, see `QUALITY_TESTING.md`.

---

## Domain Quality Scorecard

| Domain / Layer     | Test Coverage | Type Safety | Lint Passing | Imports Clean | Doc Freshness | Grade | Notes                           |
|--------------------|---------------|-------------|--------------|---------------|---------------|-------|---------------------------------|
| *(no domains yet)* | —             | —           | —            | —             | —             | —     | Populate as domains are created |

**Grade scale**: 🟢 Good · 🟡 Needs Attention · 🔴 Critical Gap · ⚪ Not Applicable

---

## Grade Definitions

| Grade | Meaning                                                                                      |
|-------|----------------------------------------------------------------------------------------------|
| 🟢    | All gates passing. No known debt in this dimension.                                          |
| 🟡    | Partial coverage or known gaps. A cleanup PR is open or planned.                             |
| 🔴    | Significant gaps. Blocks new features being added to this domain. Fix before proceeding.     |
| ⚪    | Not applicable to this layer (e.g., Doc Freshness for `types/`)                             |

---

## Scorecard Update Instructions

The cleanup agent updates this file on a regular cadence. When updating:

1. Run all CI checks and the import linter (`scripts/lint/check_imports.py`)
2. Check test coverage reports per domain
3. Check doc freshness in `docs/design-docs/index.md` (verification dates)
4. Update the grade for any domain that has changed
5. If a domain goes 🔴, open a targeted fix PR and link it in the Notes column

---

## Architecture Layer Health

Separate from domain grades, the following architectural invariants are tracked globally:

| Invariant                             | Status | Last Checked  | Notes                    |
|---------------------------------------|--------|---------------|--------------------------|
| Import direction rules                | ⚪ —   | Never         | Run `scripts/lint/`      |
| No file > 400 lines                   | ⚪ —   | Never         | Run `scripts/lint/`      |
| All service/ layers have tests        | ⚪ —   | Never         | —                        |
| All external I/O has schema validation| ⚪ —   | Never         | —                        |
| Structured logging in all boundaries  | ⚪ —   | Never         | —                        |
