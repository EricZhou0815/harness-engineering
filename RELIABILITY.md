# RELIABILITY.md — Reliability Requirements & Operational Invariants

Reliability is a first-class concern. These rules are enforced mechanically where possible.
When enforcement is not automated, they are reviewed in every PR.

---

## 1. Service Level Objectives (SLOs)

Define and track these targets per domain. Update the `QUALITY_SCORE.md` when a domain drifts.

| SLO                           | Target          | Enforcement Method          |
|-------------------------------|-----------------|-----------------------------|
| API p99 response time         | < 500ms         | Span-based tracing in CI    |
| Critical user journey spans   | < 2s end-to-end | OTel trace assertions       |
| Service startup time          | < 800ms         | Boot-time metric assertion  |
| Error rate (5xx)              | < 0.1%          | Log-based alerting rule     |
| Test suite pass rate          | 100%            | CI gate (hard block)        |

> **Agent instruction**: When implementing a new feature, instrument it with OpenTelemetry spans.
> Traces are the source of truth for runtime performance. "It seemed fast" is not acceptable evidence.

---

## 2. Observability Stack

The local observability stack is ephemeral per worktree and includes:

- **Logs**: Structured JSON logs, queryable via LogQL
- **Metrics**: Prometheus-compatible, queryable via PromQL
- **Traces**: OpenTelemetry, queryable via TraceQL

**Rule**: Every service boundary (HTTP handler, queue consumer, DB call) must emit a span.
**Rule**: Logs must be structured (JSON). No `console.log("something happened")`.

Example structured log shape:
```json
{ "level": "info", "msg": "user.created", "user_id": "u_123", "duration_ms": 12, "trace_id": "..." }
```

---

## 3. Startup & Readiness

- Services must expose a `/healthz` (liveness) and `/readyz` (readiness) endpoint.
- Service startup must complete and `readyz` must return `200` within **800ms**.
- Startup failures must be logged with a structured error before exiting.
- Database migrations must run and complete before the service marks itself ready.

---

## 4. Graceful Shutdown

- Services must handle `SIGTERM` and drain in-flight requests before exiting.
- Queue consumers must finish processing the current message before stopping.
- Maximum graceful shutdown window: **30 seconds**.

---

## 5. Retry & Timeout Contracts

- **All outbound network calls** must have an explicit timeout. No unlimited waits.
- Retry logic must use exponential backoff with jitter. Max 3 retries by default.
- Retries are only appropriate for **idempotent** operations. Never retry a non-idempotent POST without a deterministic idempotency key.

---

## 6. Failure Modes & Circuit Breaking

- Identify the top-3 dependencies for each service. Define their failure modes explicitly in `docs/design-docs/`.
- If a dependency is non-critical, implement a graceful degradation path (return cached data, disable the feature flag).
- If a dependency is critical (e.g., primary DB), fail fast and surface a clear error.

---

## 7. Platform-Specific Constraints

*(Add project-specific runtime constraints here as the project evolves)*

- [ ] Define max memory allocation per service
- [ ] Define CPU throttle thresholds
- [ ] Document cold-start behaviour for serverless functions (if applicable)
