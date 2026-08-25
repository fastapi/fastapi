# Seven-lens review — T1
Isolation tier: B (fresh review session; memory/cross-chat off). Implementation transcript not loaded.

## Verdict
HOLD — pending lens passes (verdict must follow from findings).

## Inputs
- Diff: branch session-T1 (sandbox/log_summariser + sessions/T1)
- Spec: specs/multi-tenant-log-summariser/spec.md (AC3 + Errors section relevant)
- Independent tests: sandbox/log_summariser/tests/test_get_summary_independent.py (PASS: 8 passed)
- Test pass record: pytest output captured below

## Lens 1 — Behaviour preservation
(TBD)

## Lens 2 — Hidden assumptions
(TBD)

## Lens 3 — Spec/ADR drift
(TBD)

## Lens 4 — Independent tests check
(TBD)

## Lens 5 — Edge cases
(TBD)

## Lens 6 — Security / tool-call surface
(TBD)

## Lens 7 — Over-engineering
(TBD)

## Test pass record
(TBD)

## Diff
(TBD)

## Adversarial pass
Model/session: GitHub Copilot (fresh session). Isolation tier: B (separate Copilot profile; memory/cross-chat off).

### Pre-mortem finding (picked from causes 2–5)
- Finding: Import-time singleton mutable state (STORE) can be mutated by unrelated code paths, causing cross-request nondeterminism and hard-to-debug corruption.
- Trigger: Any future endpoint/background job/startup hook imports the module and writes unexpected shapes/values into STORE.
- Blast radius: All requests served by that process for any tenant whose data is in that instance (symptoms appear nondeterministic across requests).
- Risk location: sandbox/log_summariser/app/main.py (module-level STORE: dict[str, dict[str, SummaryRecord]] = {}).
- Mitigation: Make STORE an injected dependency (per-request or app.state) or wrap access behind a small Store interface that validates shapes on write/read.
- Resolution decision: ACCEPT WITH DOCUMENTED RISK (sandbox-only; not production persistence). Add/retain explicit README warning: process-local, mutable, not concurrency-safe.

### Edge-case-hunter finding (strongest)
- Finding: GET can return job_status values outside the allowed set, violating AC3.
- Input shape: SummaryRecord(job_status="cancelled", ...) stored under STORE[tenant_id][summary_id].
- Observable failure: GET returns 200 with job_status="cancelled" instead of restricting to {queued,running,succeeded,failed}.
- Risk location: sandbox/log_summariser/app/main.py — class SummaryRecord(BaseModel): job_status: str and eturn record in get_summary.
- Mitigation: Constrain job_status to an Enum/Literal union and/or validate before returning.
- Resolution decision: FIX NOW — change SummaryRecord.job_status type to Literal['queued','running','succeeded','failed'] (or Enum) and add an independent test that seeds an invalid value and expects 500→(or a defined error) OR spec update if pass-through is intended.

### Verdict update
- Prior verdict: REQUEST CHANGES.
- Updated verdict: REQUEST CHANGES (unchanged). Driven by FIX NOW edge-case (invalid job_status violates AC3) and the need to either enforce allowed values or clarify spec.

