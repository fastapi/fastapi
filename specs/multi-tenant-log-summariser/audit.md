# Audit — multi-tenant-log-summariser
Isolation tier: B (fresh session, no repo context)

## Audit prompt used
I'm pasting a feature spec. You have NOT seen this feature before. Find three requirements this spec silently omits. Be specific — point at the section that lacks the detail, name what's missing, and explain how an implementation that ignores the gap would surface in production.

## Findings
1. Concurrency section: missing idempotency behavior under concurrent duplicate requests.
2. AC2 / Async execution: missing job state transition requirements.
3. Tenant isolation requirement: idempotency key lookups/uniqueness not explicitly tenant-scoped.

## Resolution log
1. INCORPORATE — Added "Idempotency under concurrency" requirement to the Concurrency section (atomic create-or-return for same (tenant_id, Idempotency-Key)).
2. INCORPORATE — Added "Async job lifecycle rules" to Errors (monotonic state machine + stuck-job timeout to failed).
3. INCORPORATE — Made idempotency explicitly tenant-scoped in Integrations (and noted in Boundaries).
