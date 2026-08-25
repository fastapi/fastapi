Multi-tenant log summariser service

Behaviour

We are introducing a multi-tenant HTTP service that accepts raw log lines for a tenant, produces a concise summary, and stores the summary for later retrieval. Tenants are isolated: one tenant cannot read or influence another tenant’s data or rate limits. The service supports synchronous summarisation for small inputs and asynchronous job processing for larger inputs.





Acceptance criteria

AC1 — Create summary (sync)





Given a valid tenant\_id and an authenticated request



When the client submits ≤ 200 log lines to POST /tenants/{tenant\_id}/summaries



Then the service returns 201 with a summary\_id and the generated summary text



AC2 — Create summary (async)





Given a valid tenant\_id and an authenticated request



When the client submits > 200 and ≤ 5,000 log lines to POST /tenants/{tenant\_id}/summaries



Then the service returns 202 with a summary\_id and job\_status="queued"



AC3 — Retrieve summary





Given an existing summary\_id for tenant\_id



When the client calls GET /tenants/{tenant\_id}/summaries/{summary\_id}



Then the service returns 200 with the stored summary and job\_status in {queued,running,succeeded,failed}



AC4 — Soft per-tenant rate limit





Given a tenant that has exceeded 60 create-summary requests in the last 60 seconds



When the tenant submits another POST /tenants/{tenant\_id}/summaries request



Then the service returns 429 with a Retry-After value in seconds



Concurrency

The service must behave correctly under concurrent requests for the same tenant and different tenants. Two simultaneous POST requests for the same tenant are allowed and must produce distinct summary\_id values and independent job lifecycles. Rate limiting is enforced per tenant across concurrent requests; if multiple requests arrive near-simultaneously, at most one may pass once the limit is reached, and the rest must receive 429. Retrieval (GET) must be safe during job execution and return the latest known job\_status without partial/invalid JSON responses.





Idempotency under concurrency: If two or more POST requests arrive concurrently with the same (tenant\_id, Idempotency-Key), the service MUST behave atomically: exactly one summary\_id is created, and all concurrent requests MUST return the same summary\_id and the same eventual job lifecycle. Implementations MUST ensure the “check idempotency key → create summary/job” operation is a single atomic decision (e.g., unique constraint + transactional insert). Concurrent duplicates MUST NOT create duplicate jobs or return different summary\_id values.





Errors

All error responses are JSON with fields: { "error": { "code": string, "message": string, "details": object|null } }.





400 invalid\_input: malformed JSON body; missing required fields; log\_lines not an array of strings; any log line > 8KB; empty log\_lines array.



401 unauthenticated: missing/invalid auth credentials.



403 forbidden: authenticated but not authorized for the tenant\_id.



404 not\_found: tenant\_id or summary\_id does not exist (do not leak which).



409 conflict: client attempts to reuse an idempotency key (see Integrations/Assumptions) with a different payload hash.



413 payload\_too\_large: request exceeds payload limits (see NFR budget).



422 unsupported\_content: content-type is not application/json.



429 rate\_limited: per-tenant soft rate limit exceeded.



500 internal: unexpected server error (no stack traces returned).

For async jobs, failures must be represented as job\_status="failed" and include an error.code/message in the GET response for that summary\_id.



Async job lifecycle rules:





Allowed states: queued, running, succeeded, failed.



Transitions MUST be monotonic and one-way: queued → running → succeeded|failed.



States MUST NOT regress (e.g., running → queued) and MUST NOT oscillate.



queued MAY be skipped only if the job is picked up immediately (e.g., create returns 202 but worker transitions to running before first GET).



A job is considered stuck if it remains in queued or running for > 10 minutes; stuck jobs MUST transition to failed with error.code="job\_timeout".



Boundaries

Idempotency is tenant-scoped: the same Idempotency-Key value used by two different tenants is treated as independent.



log\_lines length:



0 lines → 400 invalid\_input



1–200 lines → sync path (201)



201–5,000 lines → async path (202)



> 5,000 lines → 413 payload\_too\_large



log line size:



any line > 8KB → 400 invalid\_input



total payload:



body > 1MB → 413 payload\_too\_large



character encoding: accept UTF-8; reject invalid UTF-8 with 400 invalid\_input.



duplicate submits:



with same idempotency key and same payload hash → return the same summary\_id (201/202) without reprocessing



with same idempotency key but different payload hash → 409 conflict



retrieval during processing:



GET must return job\_status queued/running and summary may be null until succeeded/failed.



Integrations

AuthN/AuthZ: assumes an external identity layer provides an authenticated principal and a mapping to allowed tenant\_ids. If auth provider is unavailable, requests fail closed with 503 auth\_unavailable.



Storage: summaries and job state are persisted in the service datastore (assume Postgres). Tenant\_id is a mandatory partition key on all reads/writes.



Async execution: async jobs are processed by a worker using an internal queue mechanism (assume a durable queue). If the queue is unavailable, POST requests that would be async must return 503 queue\_unavailable.



Summarisation engine: the summariser may call an external model/API. If the model/API is unavailable:



sync requests return 503 summariser\_unavailable



async jobs move to failed with error.code="summariser\_unavailable"



Idempotency: the service supports an Idempotency-Key header on POST. Idempotency storage and uniqueness MUST be scoped by tenant\_id: deduplication is keyed on (tenant\_id, idempotency\_key). Keys from different tenants MUST NOT collide, influence dedup decisions, or leak identifiers across tenants.





NFR budget

Latency: p95 ≤ 300ms for sync POST (≤200 lines) excluding summariser external call time; p95 ≤ 100ms for GET summary.



Payload size: request body ≤ 1MB; each log line ≤ 8KB; max 5,000 lines.



Error behavior: 0 retries by default on POST at the API boundary; clients may retry safely only with Idempotency-Key. For async jobs, worker retries max 3 attempts with exponential backoff starting at 500ms.



Cost/complexity constraint: no new paid SaaS dependencies; must run with existing CI/CD and one datastore + one queue.

