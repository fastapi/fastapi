# Tasks — multi-tenant-log-summariser

## First slice — one AC end-to-end, < 100 lines: T1

### T1 — Minimal GET retrieve path over in-memory store (end-to-end)
Input: AC3 + error response shape contract.
Output: GET /tenants/{tenant_id}/summaries/{summary_id} returns 200 with {job_status, summary_text?} for a seeded in-memory record; returns 404 with the standard error shape when missing.
Done: Test "test_get_summary_happy_path_and_404" passes proving 200/404 and response shape.

Seam contract: Defines the initial SummaryRecord response shape that later tasks must preserve.

### T2 — Define SummaryStore interface + in-memory implementation (tenant-scoped)
Input: Plan Component 4 seam requirements.
Output: SummaryStore interface + in-memory store supporting create/get + tenant-scoped keying.
Done: Unit test proves tenant isolation: same summary_id in different tenants is not cross-readable.

Seam contract: SummaryStore.get_summary(tenant_id, summary_id) and returned record fields are fixed at end of T2.

### T3 — Implement idempotency decision contract (atomic create-or-return) in store
Input: Boundaries (Idempotency-Key semantics) + SummaryStore from T2.
Output: put_idempotency(tenant_id, key, payload_hash) behavior with outcomes {created|existing|conflict}.
Done: Unit test simulates two "concurrent" creates (same tenant/key/hash) returning the same summary_id and no duplicates; conflict returns 409-equivalent outcome.

Seam contract: Idempotency outcomes and payload-hash conflict rule are fixed at end of T3.

### T4 — POST create (sync only) using Summariser stub + persistence
Input: SummaryStore+idempotency from T3; Summariser interface stub.
Output: POST /tenants/{tenant_id}/summaries accepts 1–200 lines, returns 201 with summary_id and summary_text; rejects empty log_lines with 400; rejects >1MB with 413.
Done: Test "test_create_summary_sync_happy_path_and_boundaries" passes (AC1 + boundary checks).

Seam contract: CreateResult for sync (fields returned by POST) is fixed at end of T4.

### T5 — Per-tenant soft rate limit at API boundary
Input: POST handler from T4.
Output: RateLimiter.check_and_increment(tenant_id, now) + in-memory impl; POST returns 429 with Retry-After when exceeded.
Done: Test "test_rate_limit_60_per_60s" makes 61 requests for one tenant and asserts 60 succeed then 429 with Retry-After.

Highest-risk task: T5 — shared mutable state + concurrency makes it easy to allow bursts or deny incorrectly.

Seam contract: RateLimiter decision contract (allowed vs rate_limited{retry_after_seconds}) is fixed at end of T5.

### T6 — Async create path (enqueue only) + queued status persisted
Input: Boundaries (201–5000 => async) + QueueClient seam + SummaryStore from T3.
Output: POST returns 202 with summary_id and job_status=queued; queue_unavailable returns 503 with error.code=queue_unavailable.
Done: Test "test_create_summary_async_enqueues_and_persists_queued" passes (AC2).

Seam contract: SummaryJob payload shape {tenant_id, summary_id} is fixed at end of T6.

### T7 — Worker processes SummaryJob and enforces monotonic lifecycle + retries
Input: SummaryJob from T6; lifecycle rules; Summariser integration seam.
Output: Worker transitions queued→running→succeeded|failed; retries up to 3 with backoff; failures produce stable error codes (summariser_unavailable, job_timeout).
Done: Test suite "test_worker_job_lifecycle_monotonic_and_retries" passes proving monotonic transitions + retry cap (max 3) + stable error codes.

Seam contract: Job status lifecycle (queued→running→terminal) and error.code mapping are fixed at end of T7.
