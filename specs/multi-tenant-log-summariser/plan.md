```md

\# Plan — multi-tenant-log-summariser



\## Component 1: HTTP API layer (create/retrieve)

Responsibilities:

\- Expose POST /tenants/{tenant\_id}/summaries and GET /tenants/{tenant\_id}/summaries/{summary\_id}.

\- Validate inputs and enforce per-tenant rate limiting.

\- Produce consistent error response shape.

\- Decide sync vs async path based on line count boundaries.



Interface (seam) to Component 2:

\- Calls `SummaryService.create\_summary(tenant\_id, log\_lines, idempotency\_key) -> CreateResult` where CreateResult includes {summary\_id, mode: "sync"|"async", job\_status, summary\_text?}.



Interface (seam) to Component 3:

\- Calls `SummaryService.get\_summary(tenant\_id, summary\_id) -> SummaryRecord` where SummaryRecord includes {job\_status, summary\_text?, error?}.



\## Component 2: SummaryService (business rules + orchestration)

Responsibilities:

\- Enforce idempotency semantics (tenant-scoped).

\- Enforce sync/async thresholds.

\- For sync: invoke summariser and persist result.

\- For async: enqueue work item and persist queued state.

\- Enforce job lifecycle rules (monotonic transitions, timeout policy).



Interface (seam) to Component 4:

\- Uses `SummaryStore` for persistence:

&#x20; - `put\_idempotency(tenant\_id, key, payload\_hash) -> {created|existing|conflict}`

&#x20; - `create\_summary\_row(...) -> summary\_id`

&#x20; - `update\_job\_status(summary\_id, from\_state?, to\_state, error?)`

&#x20; - `get\_summary(tenant\_id, summary\_id)`



Interface (seam) to Component 5:

\- Enqueue: `QueueClient.enqueue(SummaryJob{tenant\_id, summary\_id}) -> ok|queue\_unavailable`



\## Component 3: Worker (async execution path)

Responsibilities:

\- Dequeue SummaryJob.

\- Transition queued→running→(succeeded|failed) with monotonic rules.

\- Call summariser and persist output/error.

\- Apply retry policy (max 3 attempts, backoff starting 500ms).

\- Apply stuck-job policy: jobs > 10 minutes in queued/running → failed(job\_timeout). (May be implemented as a watchdog or by worker lease/timeout logic.)



Interface (seam) to Component 4:

\- Reads/writes `SummaryStore` job state and result fields.

\- Contract: job state updates must be conditional/atomic to preserve monotonic transitions.



Interface (seam) to Component 6:

\- Calls `Summariser.summarise(log\_lines) -> summary\_text` or raises summariser\_unavailable.



\## Component 4: Persistence (SummaryStore)

Responsibilities:

\- Store summary rows partitioned by tenant\_id.

\- Store idempotency table keyed by (tenant\_id, idempotency\_key) with payload hash.

\- Support atomic create-or-return behaviour under concurrent duplicate requests.

\- Support conditional updates to job status to prevent regression.



Interface contracts (seams):

\- Idempotency decision is atomic: two concurrent creates with same key return the same summary\_id (no duplicates).

\- Tenant isolation: all lookups/writes require tenant\_id.



\## Component 5: Rate limiting

Responsibilities:

\- Soft per-tenant rate limit: 60 create requests / 60 seconds.

\- Provide Retry-After seconds on 429.

\- Ensure concurrency correctness: near-simultaneous requests don’t allow unlimited bursts once limit reached.



Interface (seam) to API:

\- `RateLimiter.check\_and\_increment(tenant\_id, now) -> allowed|rate\_limited{retry\_after\_seconds}`



\## Component 6: Summarisation integration

Responsibilities:

\- Provide summarise(log\_lines) abstraction.

\- Map integration failure to summariser\_unavailable (503 for sync; failed job for async).



Interface (seam):

\- Error mapping contract: integration failure must become a stable error code, not a raw exception.



\## Cross-cutting: Error model + boundaries + NFRs

\- Error response shape is stable JSON: {"error": {"code","message","details"}}.

\- Boundary rules are authoritative (line counts, sizes, payload limit).

\- NFR budgets define required p95 latency targets and payload caps.

```

