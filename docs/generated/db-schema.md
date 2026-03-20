# DB Schema — Generated Reference

> **This file is agent-generated.** Do not manually edit.
> It is regenerated automatically when the database schema changes.
> It serves as a readable, in-repo reference for the agent to inspect data shapes
> without querying the live database.

---

## Tables

*(This section is populated automatically by the schema generation script.
Run `[your schema generation command]` to regenerate.)*

---

## Conventions

- All tables use `id` as the primary key (UUID v4 or serial — as per project config)
- `created_at` and `updated_at` timestamps are present on every table
- Soft-deletion is **not** used by default (hard deletes only, unless a spec requires audit trails)
- Foreign keys are always explicitly constrained at the DB level — never just in application code
- No nullable columns without an explicit default or a documented reason

---

## Relationships

*(Described here once the schema is populated)*

---

## Index Strategy

*(Described here once the schema is populated — list which columns are indexed and why)*
