# PRODUCT_SENSE.md — Product Context & Logic Flow

This document outlines the *intent* of the system. An autonomous agent must read this file to deeply understand *why* we are building this product, what the user actually wants, and where corners can safely be cut.

## Mission Statement
[Insert your high-level product goal here, e.g., "A fast, resilient e-commerce checkout loop optimized exclusively for mobile web, built to accept payments within 3 steps maximum."]

## Core Values (Ranked)
1. **Reliability > Features**: Core flows must never randomly fail. Better to have fewer features than broken ones.
2. **Speed Metrics > Aesthetics**: Fast feedback loops, instant layout rendering, sub-100ms API responses.
3. **Idempotency**: All destructive endpoints or transaction-submission buttons must defensively prevent multiple identical clicks.

## Critical Business Logic Context
- **Edge cases mapped**: How do we handle network timeouts? [Define here e.g., "Queue offline state locally via ServiceWorker and replay"]
- **State mapping**: When a core action occurs, what upstream/downstream metrics change with it? [Define here e.g., "Adjusting inventory always publishes a domain event immediately"]
- **Silent deduplication**: Should invalid user inputs immediately throw errors, or inherently normalize? [Define here e.g., "Normalize all user IDs silently, don't throw 400s for trailing spaces"].

## Explicit Scope Constraints (MVP Bounds)
To avoid over-engineering, you are strictly forbidden from building the following during this execution phase:
- *No complex admin dashboards or analytic tracking.*
- *No soft-deletion mechanisms; destructive operations are hard-deletes.*
- *No real-time WebSocket syncing unless explicitly ordered in `PLANS.md`.*
- *No multi-tenancy auth wrappers.*
