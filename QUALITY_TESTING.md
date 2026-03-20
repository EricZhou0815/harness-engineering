# QUALITY_TESTING.md — Testing Harness Philosophy

We write tests to mechanically encode our boundaries and prove business resilience.
Coverage percentages are a side effect of good tests, not a goal.

The rule: **a bug that reached production must never reach production again without
a test that would have caught it.**

---

## The Harness Philosophy

Before implementing complex feature logic, lay down the mechanical harness that will
immediately catch breakages. This consists of:

1. **Linters & Formatters**: Semantic code stability before any logic runs. (ESLint, Ruff, Prettier, etc.)
2. **Type Safety**: Full compilation or strict-type check passing. (TypeScript `strict`, `mypy`, etc.)
3. **Import Linter**: Architectural layer rules enforced mechanically. (see `scripts/lint/`)
4. **Semantic Tests**: Focused tests validating the exact constraints from `PRODUCT_SENSE.md`.
5. **Structural / Architecture Tests**: CI gates that codify dependency direction rules.

---

## Testing Tiers

### Tier 1 — Unit Tests (Isolated)

For pure business logic: calculations, state-machine transitions, string normalizations,
validation rules, domain object behavior.

**Rules:**
- Zero disk, network, or database I/O. No exceptions.
- Input → Output assertions only. No side effects.
- Must be fast: the full unit suite must run in under 10 seconds.
- Coverage target: **100% of business logic in the `service/` layer**.

**File convention**: `[module].test.ts` / `test_[module].py` co-located with the source.

---

### Tier 2 — Integration Tests

For proving the full flow from the API boundary through to persistence.

**Rules:**
- Must run against a local containerized DB or in-memory equivalent (Testcontainers, SQLite in-memory).
- Validate exact serialization shapes — HTTP 400s must return the correct RFC error schema, not just "a 400".
- Start from a clean state. Tests must not depend on execution order.
- Must be tagged/grouped separately so they can be excluded from fast feedback loops.

**File convention**: `[feature].integration.test.ts` / `test_[feature]_integration.py` in a `tests/integration/` directory.

---

### Tier 3 — Structural / Architecture Tests

Mechanically verify that architectural invariants from `ARCHITECTURE.md` hold.
These tests are not about feature behaviour — they are about the shape of the codebase.

Examples:
- Import graph test: `UI` must not import from `Repo` or `infra/`
- File size test: no source file exceeds 400 lines
- Naming convention test: all schema types end in `Schema`, all DTOs end in `Dto`

**Location**: `scripts/lint/` (see the import linter for the canonical example).

---

## The Red-Green Discipline

When `PLANS.md` instructs you to build a feature:

1. **Write the test file first.** Structure the `describe` / `it` blocks before any implementation.
2. **Outline the Act/Assert** for each scenario using the acceptance criteria from `docs/product-specs/`.
3. **Watch it fail (Red).** Run the tests. Confirm they fail for the right reason — not because of a syntax error.
4. **Write the minimum code to make it pass (Green).** Nothing more.
5. **Refactor if needed.** Clean up duplication without changing test outcomes.

This is not optional. If tests are written after the implementation they are verifying,
they are not tests — they are documentation.

---

## What Good Coverage Actually Means

| Layer       | What to test                                      | What NOT to test              |
|-------------|---------------------------------------------------|-------------------------------|
| `types/`    | Schema parsing (valid + invalid inputs)           | The schema library itself     |
| `config/`   | Config loading and env var defaults               | Env var parsing libraries     |
| `repo/`     | Query shapes, response mapping, error handling    | The ORM / DB driver           |
| `service/`  | All business rules, branching logic, edge cases   | Infrastructure setup code     |
| `runtime/`  | Job trigger logic, retry behaviour                | Clock/scheduler internals     |
| `ui/`       | User interactions, state transitions, error states| Framework rendering internals |
