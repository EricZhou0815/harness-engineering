# ARCHITECTURE.md — Domain Map & Package Layering

This is the top-level map of the system's architecture. Read this before designing any feature.
It tells you *where* things live and *how* layers are allowed to communicate.

For the deeper "why" behind each domain, see `docs/design-docs/`.

---

## 1. Layered Domain Architecture

Every business domain is divided into a fixed set of layers. Dependencies may only flow **forward**
through the stack — never backward. This is mechanically enforced via custom linters and CI jobs.

```
Types → Config → Repo → Service → Runtime → UI
```

| Layer       | Purpose                                                                 | May Import From                    |
|-------------|-------------------------------------------------------------------------|------------------------------------|
| **Types**   | Shared DTOs, value objects, enums, and schema definitions               | Nothing (leaf node)                |
| **Config**  | Environment variables, feature flags, static configuration              | Types                              |
| **Repo**    | Data access: DB queries, external API calls, cache adapters             | Types, Config                      |
| **Service** | Business logic: orchestration, validation, domain rules                 | Types, Config, Repo                |
| **Runtime** | Entry points for background work: job runners, queue consumers, cron handlers, webhook processors. Thin — delegates all logic to Service. | Types, Config, Repo, Service |
| **UI**      | Frontend views, components, hooks, route handlers                       | Types, Config, Service (via DI)    |

**Cross-cutting concerns** (auth, telemetry, feature flags, connectors) enter through a single
explicit interface: **Providers**. A `Utils` module may be imported by any layer.

Anything that violates this dependency graph is disallowed and caught by CI.

---

## 2. Business Domains

List the primary product domains here as they are defined. Each domain has its own isolated
implementation of the layer stack above.

```
domains/
├── [domain-name]/
│   ├── types/
│   ├── config/
│   ├── repo/
│   ├── service/
│   ├── runtime/
│   └── ui/
```

> **Agent instruction**: When adding a new domain, only create a `runtime/` layer if the domain
> has a concrete background job, queue consumer, or scheduled task. Do not create it speculatively.
> All other layers (`types/`, `config/`, `repo/`, `service/`, `ui/`) should be created upfront.

---

## 3. Shared Infrastructure

| Package         | Responsibility                                                        |
|-----------------|-----------------------------------------------------------------------|
| `utils/`        | Pure utility functions with 100% test coverage. No side effects.      |
| `providers/`    | Auth, telemetry (OTel), feature flags, connectors — single interface  |
| `shared-types/` | Cross-domain DTOs and type contracts                                  |
| `infra/`        | DB clients, queue adapters, cache clients — never imported by UI      |

---

## 3a. The Runtime Layer — What It Is and What It Isn't

**Runtime is the background-job equivalent of a route handler.** It is an *entry point*, not a logic layer.

A route handler receives an HTTP request → validates input → calls Service → returns a response.
A runtime handler receives a trigger (time, event, or queue message) → validates input → calls Service → acknowledges or errors.

**What belongs in `runtime/`:**

| Example | Description |
|---------|-------------|
| Cron job handler | `SendWeeklyDigestJob` — runs on a schedule, calls `NotificationService.sendDigest()` |
| Queue consumer | `OrderEventConsumer` — receives an SQS/Kafka message, calls `OrderService.processEvent()` |
| Webhook processor | `StripeWebhookHandler` — validates Stripe signature, calls `BillingService.handleWebhook()` |
| Scheduled cleanup | `ExpiredSessionPurgeJob` — runs nightly, calls `SessionService.purgeExpired()` |

**What does NOT belong in `runtime/`:**

- Business logic — that lives in `service/`
- Database queries — that lives in `repo/`
- Retry logic for business operations — that lives in `service/` (Runtime only handles infrastructure-level retries, e.g. acknowledging a failed queue message)

**The rule**: if you find yourself writing more than ~30 lines of logic in a Runtime file, that logic belongs in Service. Runtime files should read like a list of calls to Service methods.

**When to create `runtime/` for a domain**: only when there is a concrete job or consumer to implement. Do not create it speculatively.

## 4. Business Domains — Concrete Example

Each domain has its own isolated layer stack. Below is a **concrete reference** using `billing`.
When scaffolding any new domain, follow this exact structure and naming pattern — do not invent variations.

```
domains/
└── billing/
    ├── types/
    │   ├── index.ts                       ← re-exports everything from this layer
    │   ├── invoice.types.ts               ← InvoiceDto, InvoiceStatus enum
    │   └── subscription.types.ts          ← SubscriptionDto, PlanTier enum
    │
    ├── config/
    │   ├── index.ts
    │   └── billing.config.ts              ← stripe keys, plan limits, trial period constants
    │
    ├── repo/
    │   ├── index.ts
    │   ├── invoice.repo.ts                ← createInvoice(), getById(), listByUser()
    │   └── subscription.repo.ts           ← upsertSubscription(), getActiveByUser()
    │
    ├── service/
    │   ├── index.ts
    │   ├── invoice.service.ts             ← createInvoice(), voidInvoice(), retryFailed()
    │   └── subscription.service.ts        ← activate(), cancel(), upgrade(), checkEntitlement()
    │
    ├── runtime/                           ← only exists because billing has real background jobs
    │   ├── index.ts
    │   ├── retry-failed-invoices.job.ts   ← runs nightly, calls invoice.service
    │   └── subscription-expiry.job.ts     ← runs hourly, calls subscription.service
    │
    └── ui/
        ├── index.ts
        ├── BillingPage.tsx                ← route-level page, composes presentational components
        ├── InvoiceList.tsx                ← presentational, receives invoices as props
        ├── PlanSelector.tsx               ← presentational, emits onSelect callback
        └── hooks/
            ├── useSubscription.ts         ← calls subscription.service, owns loading/error state
            └── useInvoices.ts             ← calls invoice.service, paginated
```

**Naming conventions to follow exactly:**

| Layer     | File naming pattern       | Example                          |
|-----------|--------------------------|----------------------------------|
| `types`   | `<entity>.types.ts`      | `invoice.types.ts`               |
| `config`  | `<domain>.config.ts`     | `billing.config.ts`              |
| `repo`    | `<entity>.repo.ts`       | `invoice.repo.ts`                |
| `service` | `<entity>.service.ts`    | `subscription.service.ts`        |
| `runtime` | `<description>.job.ts`   | `retry-failed-invoices.job.ts`   |
| `ui`      | `<Component>.tsx`        | `BillingPage.tsx`                |
| `ui/hooks`| `use<Entity>.ts`         | `useInvoices.ts`                 |
| any layer | `index.ts`               | re-exports only, no logic        |

> **Agent instruction:** Create all layers except `runtime/` upfront when adding a new domain,
> even if files are initially empty stubs (`export {}`). Only create `runtime/` when
> a concrete job is being implemented.

---

## 5. Communication Contracts

- **Intra-service calls**: Direct function/method calls within a domain layer stack
- **Inter-domain calls**: Only via `Service` interfaces — never reaching into another domain's `Repo`
- **External I/O**: Always encapsulated in the `Repo` layer with typed response schemas
- **Events/Queues**: Published from `Service`, consumed in `Runtime`

See `DESIGN.md` for DTO isolation rules at each boundary.



## 5. Dependency Rules — Mechanical Enforcement

The following rules are enforced by `scripts/lint/check_imports.py` and will fail CI if violated.
Run locally with: `python scripts/lint/check_imports.py --root ./src`

| Rule     | Check                                                                             |
|----------|-----------------------------------------------------------------------------------|
| ARCH-01  | Layer dependency direction: no layer imports from a later layer in the stack      |
| ARCH-02  | `UI` must never import from `repo`, `infra/`, or any external DB client           |
| ARCH-03  | `Service` must never import from `ui`                                             |
| ARCH-04  | `Runtime` must never import from `ui`                                             |
| SIZE-01  | No source file exceeds 400 lines (configurable via `--max-lines`)                 |

Error messages from the linter are written to be actionable: they name the violated rule,
the offending import, and the remediation path. Read them carefully before attempting a fix.

See `docs/design-docs/core-beliefs.md` for the philosophical rationale behind these constraints.

