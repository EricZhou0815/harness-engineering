# GOLDEN_PRINCIPLES.md — Mechanical Invariants

These are the non-negotiable operational invariants. Code that circumvents these principles—regardless of language—will introduce severe technical debt, memory leaks, or race conditions.

## 1. Concurrency & Transactions
Any method that performs multiple state modifications across shared resources must execute atomically.
- Do not implement application-level "read-modify-write" patterns for counters or toggles. (e.g., *never* query a record into RAM, `value++`, and save back). Two concurrent REST requests will corrupt the database.
- Exploit native transactional guarantees: Use raw atomic updates (`UPDATE tables SET view = view + 1`), explicitly lock database rows (`FOR UPDATE`), or enforce Native Unique Constraints when writing many-to-many relationship states.

## 2. Paginating Data
Memory is finite; databases are massive.
- **Never** retrieve an entire table collection into application RAM arrays before applying limits (`.Take()`, `LIMIT`, `.slice()`). Filtering, sorting, and pagination MUST be mechanically pushed down into the persistence/query layer.

## 3. Immutability
- UI States (e.g., React/Vue) must strictly utilize immutable object spread operations rather than in-place reference mutations.
- Network API configurations must be defined as tightly-immutable static structures. Avoid mutating payload classes after construction. 

## 4. Total Error Trapping
You must never silently consume a caught exception unless it explicitly maps to a safe fallback scenario mechanism.
- If data mapping fails, throw a boundary exception. 
- Log the actual caught error natively; don't just `.catch(e => console.log('failed'))`.
- Use specific exception trapping; never implement an empty `catch (Exception) {}` or generic `except Exception: pass`.

## 5. Idempotent Executions
Ensure operations can run repeatedly without fundamentally corrupting system states. If an external client re-submits identical POST/PUT packets due to network jitters, the destination system's final state should remain harmoniously consistent.
