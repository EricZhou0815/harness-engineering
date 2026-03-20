# Agent Context Map

Welcome. This repository utilizes "Harness Engineering" philosophy to explicitly map the boundaries and priorities of autonomous AI coding agents.

Context is a scarce resource. Do not try to read every file at once. 
Use this file as your table of contents to navigate the repository's rules system before executing the user's tasks.

## Core Directives
1. **Follow the boundaries, not the implementation:** We define strict architectural rules (`DESIGN.md`) and product scope (`PRODUCT_SENSE.md`). Within those boundaries, you have absolute autonomy to construct the best implementation possible.
2. **Build the Harness First:** Before writing any feature or API code, always consult `QUALITY.md` and `GOLDEN_PRINCIPLES.md`. Build and wire the CI feedback loops (Tests, Linters, Type-Checkers) *first*.
3. **Do not hallucinate scope:** If a feature isn't explicitly in the plan, don't build it. Do not guess API shapes; use typed SDKs, generated OpenAPI specs, and structured contracts.

## Knowledge Base Map

Instead of a single monolithic instruction file, the repository's knowledge base lives in a structured `docs/` directory and root markdown files treated as the system of record.
This file serves primarily as a map, with pointers to deeper sources of truth elsewhere.

### Root Context Files
* `ARCHITECTURE.md`: Top-level map of domains and package layering.
* `DESIGN.md`: The architectural boundaries. Defines modularity, separation of concerns, and system communication structures.
* `FRONTEND.md`: Frontend constraints, boundaries, and best practices.
* `PLANS.md`: Your current execution map. Ephemeral lightweight plans for small changes.
* `PRODUCT_SENSE.md`: The "Why" and the Edge Cases. Underlying business goals and explicit functionality.
* `QUALITY_SCORE.md`: Quality document grading each product domain and architectural layer, tracking gaps over time.
* `RELIABILITY.md`: Platform-specific reliability requirements with custom lints and constraints.
* `SECURITY.md`: Security requirements and invariants.
* `GOLDEN_PRINCIPLES.md`: Mechanical rules and "taste invariants" to prevent AI framework-drift and technical debt.

### Deeper Documentation (`docs/`)
* `docs/design-docs/`: Catalogued and indexed design decisions, including a set of core beliefs (`core-beliefs.md`) that define agent-first operating principles.
* `docs/exec-plans/`: Complex work is captured in execution plans with progress and decision logs here. Includes `active/`, `completed/`, and `tech-debt-tracker.md`.
* `docs/generated/`: Agent-generated artifacts like `db-schema.md`.
* `docs/product-specs/`: Detailed product specifications like `new-user-onboarding.md`.
* `docs/references/`: Reference materials and AI contexts for specific tools (e.g., `design-system-reference-llms.txt`).

## Universal Agent Operating Principles
Regardless of the language or framework (e.g., Node.js, Python, .NET, React, Vue), you must adhere to these behavioral rules:

1. **Think Before You Code**: Do not immediately execute write operations. First, comprehensively study the problem, systematically map the files to modify, build your tests, and anticipate edge cases.
2. **Minimize the Blast Radius**: Write the absolute minimal code required to satisfy the execution plan. Unsolicited or aesthetic refactoring of stable files is strictly forbidden unless authorized.
3. **Fail Fast and Ask**: If a functional requirement in `PRODUCT_SENSE.md` is contradictory, or a critical data shape is undocumented, do not guess. Suspend execution and ask the human for clarification.
4. **The Compiler/Linter is the Source of Truth**: Treat compilation errors, linter rules, and the test runner as your primary feedback loops. If something fails, read the semantic output carefully, document the error in your reasoning, and apply the surgical fix.
5. **No "YOLO" Data Probing**: Never assume un-typed data objects. Rely exclusively on strongly-typed DTOs, interfaces, and boundary validations (e.g., Zod, FluentValidation, Pydantic).
