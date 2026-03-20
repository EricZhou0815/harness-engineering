# QUALITY_SCORE.md — Quality Scorecard & Testing Harness

This file serves two purposes:
1. **Quality Scorecard**: Grades each product domain and architectural layer, tracking gaps over time.
2. **Testing Harness Philosophy**: Defines the required testing approach and what "done" means.

A doc-gardening agent updates quality grades on a regular cadence. Grades reflect actual observed quality, not aspirational targets.

---

## Domain Quality Scorecard

| Domain / Layer          | Test Coverage | Type Safety | Lint Passing | Doc Freshness | Grade  | Notes                                  |
|-------------------------|---------------|-------------|--------------|---------------|--------|----------------------------------------|
| *(no domains yet)*      | —             | —           | —            | —             | —      | Populate as domains are created        |

**Grade scale**: 🟢 Good · 🟡 Needs Attention · 🔴 Critical Gap · ⚪ Not Applicable

---

## Testing Harness Philosophy

We write tests to mechanically encode our boundaries and prove business resilience, never just to hit arbitrary coverage percentages.

## The Harness Philosophy
Before you implement complex feature logic, you must lay down the mechanical "harness" that will immediately catch breakages. This consists of:
1. **Linters & Formatters (Pre-commit)**: Ensures semantic code stability (e.g., ESLint, Prettier, Ruff, Roslyn, formatting defaults).
2. **Type Safety Validation**: Passing full compilation or strict-type checks (e.g., TypeScript `strict`, Python `mypy`, C# Nullability).
3. **Semantic Tests**: Highly focused explicit tests validating complex product constraints described in `PRODUCT_SENSE.md`. 
4. **Structural / Architecture Tests**: CI gates that prevent domain layers from importing front-end or HTTP networking logic.

## Semantic Testing Tiers

### 1. Isolated Unit Tests
Used exclusively for pure business logic (calculations, string normalizations, state-machine transitions).
- **Rule**: Absolutely zero disk, network, or database I/O allowed here. 
- **Rule**: Input → Output assertions only. 

### 2. Integration / System Tests
Used to prove the full flow from the API Controller down through the persistence layer.
- **Rule**: Must test against a local containerized DB or explicitly volatile In-Memory provider equivalent (e.g. SQLite In-Memory, Testcontainers).
- **Rule**: Validate the output matches exact structured serialization (e.g., HTTP 400s return proper RFC validation schemas).

### 3. Structural Mechanics
"When documentation falls short, promote the rule into mechanical code."
Use structural linters or graph-testing tools to ensure components remain cleanly bounded long term. (e.g. `Imports into the Domain package strictly cannot contain references to Web or Platform APIs.`)

## Instructions for Execution
When `PLANS.md` instructs you to build a feature:
1. Generate the test file first.
2. Outline the explicit `Act/Assert` scenario using pure logic mapping `PRODUCT_SENSE.md`.
3. Watch the test completely fail (Red).
4. Build the exact minimum layer of code necessary to produce a success hook (Green).
