# SECURITY.md — Security Requirements & Invariants

Security constraints that must be applied uniformly. These are not optional.
Do not defer security to "later phases." If a feature cannot be built securely within the current
plan, escalate to a human rather than shipping an insecure version.

---

## 1. Authentication & Authorization

- **Never hand-roll authentication logic or crypto functions.** Use the project's designated identity provider (OAuth2, OIDC, or an internal auth service).
- All protected routes/endpoints must verify auth tokens before executing any business logic.
- Authorization checks must happen at the **Service layer**, not the presentation layer.
  - The UI hiding a button is not a security control. The API must reject unauthorized calls regardless of the UI state.
- Use role-based or attribute-based access control as defined in the product spec. Never hardcode user IDs or roles.

---

## 2. Input Validation & Injection Prevention

- All external input (HTTP request bodies, query params, headers, file uploads) **must** be validated at the boundary using a schema library before passing further into the system.
- Never construct SQL queries via string concatenation. Use parameterized queries or the project's ORM exclusively.
- Never construct shell commands from user input.
- Sanitize all user-provided content before rendering in the UI (`innerHTML` is forbidden; use text binding).

---

## 3. Secrets Management

- **No secrets in source code.** This includes API keys, tokens, passwords, connection strings, and private certificates.
- All secrets are loaded from environment variables or a secrets manager at runtime.
- `.env` files containing real secrets must never be committed. The repository must include a `.env.example` with placeholder values only.
- If an agent accidentally commits a secret, treat it as **immediately compromised** and rotate it — do not just delete the commit.

---

## 4. Dependency Security

- Do not introduce new dependencies without checking for known CVEs (run `npm audit`, `pip-audit`, `cargo audit`, etc.).
- Pin dependency versions in lock files (`package-lock.json`, `uv.lock`, `Cargo.lock`).
- Flag any dependency that has not been updated in >2 years for review before adoption.

---

## 5. Transport Security

- All external communication must use TLS. No plaintext HTTP for anything production-bound.
- Set strict CORS policies — never use `*` in production for authenticated APIs.
- Use `Content-Security-Policy`, `X-Frame-Options`, and `Strict-Transport-Security` headers on all web-facing services.

---

## 6. Data Handling

- Personally Identifiable Information (PII) must be identified and documented in `docs/design-docs/` before the feature ships.
- PII must never be logged in plaintext. Use masking or omission.
- Data at rest containing PII must be encrypted.
- Define and document data retention policies in `docs/product-specs/`.

---

## 7. What the Agent Must Never Do

- Never disable security checks to make a test pass.
- Never return internal stack traces or error details to API consumers.
- Never expose admin or internal endpoints without authentication.
- Never store passwords in plaintext — always use a proper password hashing algorithm (e.g., bcrypt, argon2).
