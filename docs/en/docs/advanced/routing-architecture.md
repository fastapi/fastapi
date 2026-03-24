# Routing Architecture

FastAPI keeps public routing imports stable at `fastapi.routing`, but the
implementation is split into focused internal modules for maintainability.

## Public facade

- `fastapi.routing`
  - compatibility facade and stable imports
  - re-exports core symbols such as `APIRouter`, `APIRoute`, and helper hooks

## Internal modules

- `fastapi.routing_router`
  - `APIRouter` implementation
- `fastapi.routing_routes`
  - `APIRoute` and `APIWebSocketRoute`
- `fastapi.routing_handlers`
  - request/websocket handler factories and handler config objects
- `fastapi.routing_utils`
  - low-level shared utilities (response serialization, lifespan helpers, wrappers)

## Stability contract

- Application code should import from `fastapi.routing` (or top-level `fastapi`).
- Internal modules are implementation details and may evolve.
- Compatibility tests validate that key re-exports remain stable.
