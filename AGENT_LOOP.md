# AGENT_LOOP.md — Self-Validation Cycle

Run this loop on every task. Do not open a PR until it passes.
Policy and rationale for each rule lives in the doc it references — don't repeat it here.

---

## Before You Write Anything

- [ ] `PRODUCT_SENSE.md` — is the feature in scope? If `[REQUIRED]` placeholders exist, **stop and ask**.
- [ ] `ARCHITECTURE.md` — which domain and layers does this change touch?
- [ ] `docs/exec-plans/active/` — is there an existing plan? Read the full Decision Log.
- [ ] `docs/product-specs/` — is there a spec? If not and the feature is user-facing, **stop and ask**.

---

## While Implementing

Run after every meaningful unit of work — don't accumulate errors across milestones:

```bash
[format command]     # e.g. ruff format . / prettier --write .
[lint command]       # e.g. ruff check . / eslint .
[typecheck command]  # e.g. mypy . / tsc --noEmit
```

---

## Self-Review Checklist (run before CI)

**Architecture** — see `ARCHITECTURE.md`
- [ ] No layer imports in the wrong direction
- [ ] No cross-domain Repo imports (went through Service interface)
- [ ] All external data validated at boundary with a schema library

**Code** — see `GOLDEN_PRINCIPLES.md`
- [ ] No shared utility reimplemented inline (checked `utils/` first)
- [ ] No dead code, commented-out blocks, or debug log statements
- [ ] All async operations have explicit timeout and error handling

**Tests** — see `QUALITY_TESTING.md`
- [ ] Test file exists for every new unit of business logic
- [ ] Tests are Red → Green (failing test written before implementation)
- [ ] All new tests pass locally

**Docs**
- [ ] `PLANS.md` or active exec-plan milestones updated
- [ ] New pattern introduced? Add a design doc to `docs/design-docs/`
- [ ] Debt knowingly incurred? Add to `docs/exec-plans/tech-debt-tracker.md`

---

## Run CI Locally

```bash
python scripts/lint/check_imports.py --root ./src   # ARCH-01–04, SIZE-01
[test command]                                        # e.g. pytest / npm test
```

If anything fails: read the full error, fix the root cause (not the symptom), repeat from Self-Review.

---

## Open the PR

PR description must include:
1. **What changed** — domains/layers modified
2. **Why** — link to spec, plan, or user feedback
3. **How to verify** — steps a reviewer should take

---

## Escalate to Human If

- `PRODUCT_SENSE.md` has an unresolved ambiguity
- The fix requires changing an architectural constraint
- CI is failing in a way you can't explain after 2 full loop iterations
- The change would touch > 5 files outside the target domain without a plan

**Escalation format** (write in PR or `PLANS.md`):
```
🚨 HUMAN DECISION REQUIRED
Context:        [what you are implementing]
Blocker:        [the specific ambiguity or constraint conflict]
Options:        [2–3 concrete options with trade-offs]
Recommendation: [which you believe is correct and why]
```
