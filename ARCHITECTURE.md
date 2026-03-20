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
| **Runtime** | Background jobs, event processors, schedulers                           | Types, Config, Repo, Service       |
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

> **Agent instruction**: When adding a new domain, create all layers upfront even if some are
> initially empty. This keeps the structure predictable for future agent runs.

---

## 3. Shared Infrastructure

| Package         | Responsibility                                                        |
|-----------------|-----------------------------------------------------------------------|
| `utils/`        | Pure utility functions with 100% test coverage. No side effects.      |
| `providers/`    | Auth, telemetry (OTel), feature flags, connectors — single interface  |
| `shared-types/` | Cross-domain DTOs and type contracts                                  |
| `infra/`        | DB clients, queue adapters, cache clients — never imported by UI      |

---

## 4. Communication Contracts

- **Intra-service calls**: Direct function/method calls within a domain layer stack
- **Inter-domain calls**: Only via `Service` interfaces — never reaching into another domain's `Repo`
- **External I/O**: Always encapsulated in the `Repo` layer with typed response schemas
- **Events/Queues**: Published from `Service`, consumed in `Runtime`

See `DESIGN.md` for DTO isolation rules at each boundary.

---

## 5. Dependency Rules (Mechanical Enforcement)

The following rules are enforced by the linter and will fail CI if violated:

1. `UI` must never import from `Repo`, `infra/`, or any external DB client
2. `Service` must never import from `UI`
3. `Runtime` must never import from `UI`
4. All external data must be validated with a boundary schema (Zod, Pydantic, etc.) before entering the type system
5. No circular imports across domain boundaries

See `docs/design-docs/core-beliefs.md` for the philosophical rationale.
