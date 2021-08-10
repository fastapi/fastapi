# Dependency Injection Implementation Overhaul

## Context and Problem Statement

FastAPI has a simple yet powerful Dependency Injection (DI) system.
Fundamentally, this system lets users declare any _callable_ as a dependency to their path operation, and then FastAPI builds the dependency and passes it's value to the dependant.
Values are cached for the lifetime of a request, and setup/teardown are supported by linking context-manager dependencies to an AsyncExitStack.
Internally, FastAPI also uses this DI system to wire up `Request`, `Response`, `Headers`, etc. as well as query, body and path parameters.

Some of standout features of this DI system are:

1. Simplicity: it's easy to get started, and there's not a lot of concepts (containers, singletons, etc.)
2. Integration into the framework (e.g. the binding of teardown to the request's execution).

Yet because of this simplicity and design, the DI system lacks some features present in other DI systems such as:

- Scoping: to be able to tie dependencies to the app lifetime or an endpoint instead of the request response cycle.
- DI in lifespan (startup/shutdown) methods: this is mainly due to tight coupling of the internal implementation w/ the request/response cycle.
- Parallelization of dependency collection: if the endpoint depends on foo and bar, and neither has further dependencies, foo and bar can be executed in parallel.

Some of the issues that tie into this are:

- [#2057](https://github.com/tiangolo/fastapi/issues/2057): Dependency Overrides in startup event gives TypeError
- [#617](https://github.com/tiangolo/fastapi/issues/617): Further develop startup and shutdown events
- [#617](https://github.com/tiangolo/fastapi/issues/617): Further develop startup and shutdown events
- [#2697](https://github.com/tiangolo/fastapi/pull/2697): yield dependencies exit code before response
- [#2372](https://github.com/tiangolo/fastapi/issues/2372): Dependency injection without resorting to global state
- [#504](https://github.com/tiangolo/fastapi/issues/504): Dependency Injection - Singleton?
- [#425](https://github.com/tiangolo/fastapi/issues/425): Startup event dependencies
- [#1873](https://github.com/tiangolo/fastapi/issues/1873): Use FastAPI Dependency Injection separately from the API routes
- [#3620](https://github.com/tiangolo/fastapi/issues/3620): Automatically run session.commit() in session dependency BEFORE returning request
- [#3317](https://github.com/tiangolo/fastapi/issues/3317): Add support to lazy initialize OAuth2 classes

## Proposal

This proposal seeks to expand FastAPIs DI system to support these use cases.
There are two main principals under which this expansion was designed:

1. API compatibility with the current DI system.
2. Where possible, use well-known DI concepts.

To this end, the following high-level modifications are being proposed:

1. Introduce a formal `Container`.
2. Introduce scopes beyond the current defaults of `request` (`use_cache=True`) and no-scope/prototype (`use_cache=False`). These scopes would provide a more formal context for caching and lifetime control.
3. Try to decouple the steps of wiring, building of an execution graph and execution of this graph. This allows parallelization of graph execution as well as introspection (e.g. to find Security scopes) without executing the graph.

These changes should allow several of the features to be implemented naturally:

1. The container controls binds (like `Request`), which removes the need to have `request_param_name` and such in Dependant objects. This also means the container can wire and execute arbitrary non-request/response functions, like `Starlette(lifetime=...)`.
2. There can be an `"app"` scope for startup & shutdown dependencies or for singleton-like dependencies.
3. Dependencies like `Security` models can be found in the dependency graph without executing anything.

### Example usage

```python
from typing import Generator

from anydep.container import Container
from anydep.models import Dependant
from anydep.params import Depends

async def dep() -> Generator[int, None, None]:
    yield 1

async def endpoint(v1: int = Depends(dep)) -> int:
    return v1

async def main():
    container = Container()
    async with container.enter_global_scope("app"):  # shared across tasks
        async with container.enter_local_scope("request"):  # localized via contextvars
            await container.execute(Dependant(endpoint))
```

Internally, FastAPI would enter these scopes.
The DI system would abstract away the boilerplate of crating caches, entering / exiting AsyncContextStacks, etc.

FastAPI can also override methods of `Dependant`, e.g. to support custom processing of Pydantic models.

Dependency overrides can easily be implemented as context-managed binds.

### Implementation

For a mostly functional sample implementation, see https://github.com/adriangb/anydep

A good place to start is the `comparisons` folder.

In `comparisons/simple` there are comparisons between FastAPI, anydep and python-dependency-injector (a mature full fledged DI system).
The anydep implementation attempts to bridge the gap between FastAPI and python-dependency-injector.
If you run the files, you'll see that anydep and python-dependency-injector are 2x as fast as FastAPI because they parallelize execution.

In `comparisons/anydep_nested.py` and `comparisons/fastapi_nested.py` are comparisons of execution of deeply nested/branched dependency graphs. Interestingly, FastAPI seems to choke pretty quickly as the graph grows, while anydep seems to have much less trouble.

#### Backwards compatibility

This implementation should be API compatible (in terms of using `Depends` and such), but it would break or obsolete a lot of the functions in `fastapi/dependencies/utils.py`.
