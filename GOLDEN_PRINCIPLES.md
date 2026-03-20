# GOLDEN_PRINCIPLES.md — Mechanical Invariants

## Quick Reference (always read)

These are the non-negotiable rules. Violations are caught by CI and the cleanup agent.

| # | Rule | Enforcement |
|---|------|-------------|
| A1 | **Reuse before rewrite** — check `utils/` and `shared-types/` before implementing any helper | Code review |
| A2 | **No divergent reimplementation** — if it "almost fits", extend it or escalate, never fork | Code review |
| A3 | **Bounded concurrency** — use `mapWithConcurrency(items, fn, { concurrency: N })`, never raw `Promise.all` | Linter |
| A4 | **No YOLO typing** — validate all external data at boundary with schema library, never `as SomeType` | Type check |
| A5 | **Match existing patterns** — new patterns require a design doc + human approval | Code review |
| B1 | **Atomic writes** — never read-modify-write across concurrent requests; use DB-level atomics | Test |
| B2 | **Paginate at query layer** — never load a full table into memory then slice | Code review |
| B3 | **Explicit timeouts** — every outbound I/O call must have a timeout; retries use exponential backoff with jitter | Code review |
| B4 | **Idempotent mutations** — retried or replayed operations must not corrupt state | Test |
| E1 | **No silent catches** — always log the real error and re-throw or handle explicitly | Linter |
| E2 | **Typed catches** — never catch bare `Exception`/`Error` outside a top-level boundary | Linter |
| E3 | **Structured logs at every boundary** — JSON with `trace_id`, `user_id`, `duration_ms` | Code review |
| I1 | **Immutable UI state** — spread, never mutate in place | Code review |
| S1 | **File size** — source files ≤ 400 lines, test files ≤ 600 lines | `scripts/lint/check_imports.py` SIZE-01 |

---

## Detailed Reference (read only when the scenario applies)

<details>
<summary>A — Agent Entropy Invariants (expand when adding utilities, shared patterns, or concurrency)</summary>

### A1. Reuse Before You Rewrite

Before implementing any utility, helper, or abstraction, check `utils/` and `shared-types/` first.
If it exists, use it exactly as-is. If it's close but missing a narrow capability, extend it — do not fork it.

**Forbidden**: implementing a local `sleep()`, `retry()`, `chunk()`, `groupBy()`, or `mapWithConcurrency()` inline in a feature file when one already exists in `utils/`.

**Why**: Agents pattern-match locally. Without this rule, you get 8 subtly different `retry` implementations across the codebase within a week.

### A2. No Divergent Reimplementation

Do not reimplement an existing pattern with variation. If the existing one doesn't fit:
1. Extend it (preferred)
2. Open a PR to generalise it
3. Escalate to a human

"The existing one doesn't quite fit" is not justification for a new one-off.

### A3. Bounded Concurrency

All concurrent batch operations must use the project's `mapWithConcurrency` utility (or equivalent). The utility must be instrumented with OpenTelemetry.

```typescript
// ❌ FORBIDDEN — unbounded, no OTel
await Promise.all(items.map(item => process(item)))

// ✅ REQUIRED — bounded, instrumented
await mapWithConcurrency(items, process, { concurrency: 5 })
```

### A4. No YOLO Data Probing

```typescript
// ❌ FORBIDDEN
const user = response.data as User

// ✅ REQUIRED
const user = UserSchema.parse(response.data)
```

### A5. Match Existing Patterns

Find an analogous existing feature. Follow its exact pattern — folder structure, naming, test conventions, error handling. New patterns require a design doc in `docs/design-docs/` and human approval.

</details>

<details>
<summary>B — Backend Invariants (expand when writing DB operations, queues, or external I/O)</summary>

### B1. Concurrency & Transactions

Never implement application-level read-modify-write:
```sql
-- ❌ FORBIDDEN (two concurrent requests will corrupt this)
SELECT count FROM table WHERE id = ?   -- then value++ in app code -- then UPDATE

-- ✅ REQUIRED — atomic
UPDATE table SET count = count + 1 WHERE id = ?
```

A transaction must span all writes that must succeed or fail together. Never commit partial state.

### B2. Pagination at the Query Layer

Filtering, sorting, and pagination must be pushed into the DB query (`WHERE`, `LIMIT`, `OFFSET` / cursor). Never retrieve an entire collection into memory then slice it in application code.

### B3. Timeouts & Retries

- Every outbound network call, DB query, and queue operation must have an explicit timeout
- Retry policy: exponential backoff with jitter, max 3 retries by default
- Only retry **idempotent** operations — never retry a non-idempotent POST without an idempotency key

### B4. Idempotent Operations

Use idempotency keys for payment and mutation endpoints. Use upsert semantics on DB writes where appropriate. Deduplicate replayed events at the consumer.

</details>

<details>
<summary>E — Error Handling (expand when writing try/catch, logging, or error propagation)</summary>

### E1. No Silent Catches

```typescript
// ❌ FORBIDDEN
try { ... } catch (e) {}
try { ... } catch (e) { console.log('failed') }

// ✅ REQUIRED
try { ... } catch (e) {
  logger.error({ err: e, msg: 'operation.failed', context: ... })
  throw new DomainError('descriptive message', { cause: e })
}
```

### E2. Typed Catches

Use specific error types. Only catch `Exception`/`Error` at top-level boundary handlers (global middleware, queue consumer root).

### E3. Structured Logging

```json
{ "level": "info", "msg": "user.created", "user_id": "u_123", "duration_ms": 12, "trace_id": "..." }
```

Plain string messages are insufficient. See `RELIABILITY.md` for the full required shape.

</details>

<details>
<summary>I — Immutability (expand when writing UI state or config objects)</summary>

### I1. UI State

All state updates in UI frameworks must use immutable spread. Never mutate state references in place.

### I2. Config Structures

Network API configs, feature flag maps, and static config objects must be defined as immutable constants. Never mutate them after construction.

</details>

<details>
<summary>S — File Size Limits</summary>

| File type       | Max lines | Action if exceeded         |
|-----------------|-----------|----------------------------|
| Any source file | 400       | Split into smaller modules |
| Any test file   | 600       | Split by test scenario     |
| Any markdown    | 300       | Split with an index doc    |

Enforced by `scripts/lint/check_imports.py` rule SIZE-01. Agents lose coherence on large files.

</details>
