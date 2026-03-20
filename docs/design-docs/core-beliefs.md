# Core Beliefs — Agent-First Operating Principles

These are the foundational beliefs that shape every decision in this repository.
They represent the accumulated lessons of building software where agents execute
and humans steer.

> Last Verified: 2026-03-20

---

## 1. Repository Knowledge is the System of Record

Anything an agent cannot access from the repository effectively **does not exist**.
Knowledge that lives in chat threads, documents outside this repo, or people's heads
is invisible to the agent — in the same way it would be unknown to a new hire joining
three months later.

**Implication**: Every architectural decision, alignment discussion, or important constraint
that happens outside this repository must be encoded into it. If it isn't discoverable here,
it doesn't influence agent behavior.

---

## 2. Give Agents a Map, Not a Manual

A giant instruction file crowds out useful context. When everything is "important," nothing is.

We use a short `AGENTS.md` (~100 lines) as a table of contents. Deeper truths live in structured
subdirectories and are fetched only when relevant. Agents are taught *where to look* next,
not overwhelmed upfront.

**Implication**: The `AGENTS.md` must remain concise. If you're tempted to add more than a few
lines there, create a new doc in `docs/design-docs/` and add a pointer instead.

---

## 3. Enforce Boundaries, Allow Autonomy

The layered domain architecture (`ARCHITECTURE.md`) is non-negotiable.
Within those layers, agents have significant freedom in how solutions are expressed.

We care deeply about the *shape* of the solution. We do not micromanage *which loop
construct* is used or *how* a function is decomposed internally.

**Implication**: Write linters for structural rules, not style nitpicks.

---

## 4. When Documentation Falls Short, Promote to Code

If an important rule is documented but routinely violated, the rule belongs in a linter,
a structural test, or a CI gate — not in a stronger-worded document.

Documentation enforces nothing. Code enforces everything.

**Implication**: The lifecycle of a rule is:
1. Write it down (docs)
2. Observe violations
3. Encode it mechanically (linter / test / CI)

---

## 5. Prefer Boring, Inspectable Technology

Dependencies that the agent can fully model from its training are more
reliable than bleeding-edge or opaque libraries. Agents reason better about
technology with stable APIs, composable behavior, and well-understood semantics.

**Implication**: Evaluate every new dependency by asking:
- Can the agent read and understand its source?
- Is its behavior fully specifiable in-repo?
- Would a small in-house implementation be more legible than the library?

In some cases, it is cheaper to reimplement a narrow subset of functionality
than to work around opaque upstream behavior.

---

## 6. Humans Steer. Agents Execute.

Human engineers are not primarily code writers in an agent-first system.
The primary job is:
- Translate user feedback into acceptance criteria
- Design environments, abstractions, and feedback loops
- Validate outcomes
- Encode taste and judgment into tooling — not just words

When the agent struggles, the question is always: *"What capability is missing,
and how do we make it both legible and enforceable?"*

---

## 7. Corrections are Cheap. Waiting is Expensive.

In a high-throughput agent system, the cost calculus is different from a
low-throughput human team. Blocking progress indefinitely to achieve perfection
is often worse than merging and correcting in the next pass.

**Implication**: Prefer short-lived PRs, fast feedback loops, and follow-up fix
agents over prolonged blocking reviews. Technical debt is paid continuously via
the recurring cleanup process, not in painful bursts.
