# Spec: New User Onboarding

Status: 🚧 Draft
Last Updated: 2026-03-20

> This spec needs to be completed by a human before an agent can implement the feature.
> Fill in the `[TBD]` sections and update the status to `ready`.

---

## User Story

As a new user, I want a clear first-run experience so that I understand the core value
of the product and can complete my first meaningful action within [TBD] minutes.

---

## Acceptance Criteria

- [ ] New users are shown an onboarding flow on first login
- [ ] The flow explains the core product value in ≤ 3 steps
- [ ] Users can skip the onboarding flow at any point
- [ ] Completing the flow marks the user's onboarding as complete (persisted)
- [ ] Returning users who completed onboarding are never shown it again
- [ ] [TBD — add more criteria here]

---

## Edge Cases

- What if the user closes the browser mid-onboarding? → Progress is preserved; they resume where they left off on next login
- What if the user's account was created by an admin invite? → [TBD]
- What if the onboarding completion API call fails? → [TBD]

---

## Out of Scope (this phase)

- Personalised onboarding paths based on user role
- Onboarding analytics / funnel tracking
- A/B testing of onboarding variants

---

## Open Questions

- [ ] What is the primary "aha moment" action we want new users to complete?
- [ ] Should onboarding be a modal overlay or a dedicated route?
- [ ] What triggers the onboarding check — client-side or server-side redirect?
