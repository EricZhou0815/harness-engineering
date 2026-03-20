# Harness Engineering: Agent-First Development

This repository contains the blueprints for **agentic software engineering**. It is heavily inspired by OpenAI's internal practices for building software entirely with AI agents. 

The goal of this harness is to provide the **predictable structure, rigid boundaries, and continuous feedback loops** that agents need to operate autonomously without their code collapsing into chaos over time.

Instead of writing code, your job as the human engineer is to design the boundaries and review the output. The agents do the execution.

---

## 🚀 How to Use This Harness in a Project

You can apply this harness to any new or existing project to make it "agent-ready".

### 1. Copy the Harness
Copy the contents of this repository into the root directory of your project. The `docs/` folder and the root markdown files will become the central nervous system for your AI agents.

### 2. Configure the Architecture Linter
If you are applying this to an existing codebase with custom folder names (e.g., `workers/` instead of `runtime/`), copy `.harness.json.example` to `.harness.json` and adjust the mappings so the import linter understands your structure.

### 3. Fill Out `PRODUCT_SENSE.md` (CRITICAL)
Agents do not know your business. If you ask an agent to build a feature without context, it will hallucinate scope.
Open `PRODUCT_SENSE.md` and replace all `[REQUIRED]` placeholders with your actual user journeys, product goals, and edge cases. **Do not let an agent write code until this is filled out.**

### 4. Direct the Agent
Point your coding agent (e.g., Cline, Cursor, Aider) at your project.
Start by saying: *"Read `AGENTS.md` and familiarise yourself with the repository rules before executing my next task."*

---

## 🧠 The Architecture of the Harness

This harness uses **Progressive Disclosure** so agents don't get overwhelmed with context.

1. **`AGENTS.md`** is the entry point. It's a map. It tells the agent what other files exist.
2. **`PRODUCT_SENSE.md`** defines the "why" and explicitly forbids out-of-scope work.
3. **`ARCHITECTURE.md`** defines the "where". It strictly types out the layered domain architecture (`Types → Config → Repo → Service → Runtime → UI`).
4. **`GOLDEN_PRINCIPLES.md`** covers mechanical invariants (e.g., "don't reinvent shared utilities", "always use boundaries").
5. **`AGENT_LOOP.md`** is the procedural protocol. It dictates exactly what the agent must do locally (lint, tests, self-review) before claiming a task is done.

### The Enforcement Mechanism

Words in markdown files are suggestions. Code is an invariant.
This harness includes `scripts/lint/check_imports.py`. It mechanically enforces the dependency rules defined in `ARCHITECTURE.md`. 

If an agent makes a mistake—like making the `UI` layer directly import a database `Repo`—the linter fails locally, forcing the agent to fix its own architectural drift before opening a PR.

---

## 🧑‍💻 The Human's Job

When you shift to agent-first development, your role changes from **Author** to **Reviewer and Architect**.

Your day-to-day responsibilities:
1. **Writing Specs:** creating clear, bounded task descriptions in `docs/product-specs/`.
2. **Updating Context:** maintaining `PRODUCT_SENSE.md` when business rules change.
3. **Approving Designs:** reviewing new architectural patterns proposed by agents in `docs/design-docs/`.
4. **Enforcing the Loop:** rejecting agent pull requests if the agent skipped the `AGENT_LOOP.md` self-validation cycle.

By mechanically locking down the architecture, testing, and dependency rules, you free the agents to do what they do best: writing high-throughput code at extreme velocity.
