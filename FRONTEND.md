# FRONTEND.md — Frontend Constraints & Best Practices

This document governs all frontend work. Read this before writing any UI component, hook, or route.
All rules here are enforced mechanically via linters and CI or enforced by convention.

---

## 1. Component Boundaries

- **Presentational components**: Render only. Receive all data and callbacks via props. No direct API calls, no side effects.
- **Container components / page-level**: Responsible for data fetching, state orchestration, and wiring presentational components. One per route.
- **Hooks**: Encapsulate reusable stateful logic. A hook that makes a network call must own its loading and error state.

> **Rule**: No component file should exceed 300 lines. If it does, split into smaller components.

---

## 2. State Management

- Local UI state (open/closed, hover, form values): `useState` / framework equivalent. Keep it local.
- Shared application state (auth session, feature flags): Context / global store. Only one canonical source per concept.
- Server-side data: Use a data-fetching library (e.g., React Query / SWR). **Never** copy server responses directly into a global store without schema validation.

**Immutability rule**: All state updates must use immutable spread operations. Never mutate state in place.

---

## 3. Network Data Validation

All data received from the network **must** be validated at the boundary before touching the type system:

```typescript
// ✅ CORRECT — validate at boundary
const result = MyResponseSchema.parse(await fetch(...).then(r => r.json()))

// ❌ WRONG — raw cast
const result = await fetch(...).then(r => r.json()) as MyResponse
```

Use Zod (TypeScript), Pydantic (Python), or the project's chosen schema library. This is non-negotiable.

---

## 4. Error Handling in the UI

- Every async operation must have an explicit error state rendered to the user.
- Never swallow errors silently (`catch(e) => {}` is forbidden).
- Use a global error boundary as a last resort, but always prefer local error handling near the source.
- All error messages shown to users must be human-readable — never expose raw stack traces or error codes.

---

## 5. Performance Constraints

- **No waterfall data fetching**: Parallel-fetch all data required for a route before rendering.
- **Lazy load** any component or module not needed on the initial paint.
- **No layout shifts**: Images and media must have explicit dimensions or aspect ratios.
- Target: Initial page load under 1s on a fast connection. Core Web Vitals are a CI signal.

---

## 6. Accessibility (a11y)

- All interactive elements must be keyboard-accessible.
- All images must have `alt` attributes.
- Use semantic HTML elements (`<button>`, `<nav>`, `<main>`, `<header>`) — not `<div onClick>`.
- Sufficient color contrast ratio (WCAG AA minimum).

---

## 7. Design System Reference

The primary design token reference for the AI agent lives at:
`docs/references/design-system-reference-llms.txt`

Do not invent colors, spacing values, or typography outside of the defined tokens.
The design system is the source of truth for visual consistency.

---

## 8. What NOT to Build (Frontend Scope Constraints)

- Do not hand-roll animation libraries — use CSS transitions or the project's designated animation utility.
- Do not build a custom component that already exists in the design system.
- Do not implement client-side routing logic unless using the project's designated router.
- Do not write inline styles beyond truly one-off cases — use the design system tokens.
