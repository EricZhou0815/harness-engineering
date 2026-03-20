# DESIGN.md — Architecture & Component Boundaries

This document dictates the architectural patterns and communication boundaries for the system. Code that violates these structures will fail CI.

## 1. Modularity & Separation of Concerns
Whether building a React frontend or a Python backend, logically decouple your code into distinct boundary lines. No file should contain both network access and complex business arithmetic.

- **Presentation Layer (Controllers/Routes/UI Views)**: Only map parameters, handle HTTP/Input parsing, and display mapped states. **Zero business logic.**
- **Domain Layer (Services/Hooks/Business Logic)**: The pure engine context. Executes rules independently of whether the call came from REST, CLI, or an internal job.
- **Data/Infrastructure (Repositories/DB Clients/External Fetchers)**: Translates domain instructions into low-level I/O queries.

## 2. DTO Isolation at Boundaries
Never expose raw database models (`Entities`) to public APIs, or raw API payloads directly into UI state without sanitization.
- **Backends**: Map queried data to isolated `Response` DTO/Records before serializing perfectly structured JSON fields.
- **Frontends**: Use boundary schemas to validate incoming network data before updating the React/Vue global states.

## 3. Standardized Error Contracts
All boundary errors must utilize standardized JSON payload shapes (e.g., RFC 7807 Problem Details).
Never return a bare string, unexpected HTML, or an unformatted internal stack trace.
A unified error formatter middleware/interceptor must catch anomalies centrally.

## 4. Solid Design Mechanisms
- **Single Responsibility**: Every component, function, or class has only one single reason to change. 
- **Dependency Inversion**: High-level modules should never depend on low-level concretions. Use Dependency Injection (DI) to pass generic `IStorageLayer` parameters, never concrete instances. It ensures mockable, testable units.

## 5. What NOT To Build
- Do not build custom wrappers around industry-standard SDKs until absolutely necessary. 
- Do not implement arbitrary caching logic at the business layer—delegate caching purely to Edge layers or specific proxy caches.
- Do not hand-roll authentication logic or crypto functions. Use standardized identity providers or libraries.
