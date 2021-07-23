# Lifespan Event Dependencencies

FastAPI also supports dependencies in startup and shutdown events (also known as app lifespan).

For example, you might want to load [Pydantic Settings](../../advanced/settings.md#pydantic-settings){.internal-link target=_blank} on startup:

```Python hl_lines="13"
{!../../../docs_src/dependencies/tutorial013.py!}
```

!!! warning
    Your startup and shutdown cannot directly or indirectly via dependencies depend on any request or reponse parameters.
    For example, you cannot have `def startup(request: Request): ...`.
    If you do, FastAPI will raise a `fastapi.exceptions.DependencyResolutionError`.

## Setting the cache scope of startup dependencies

Typically, if you are doing something like loading settings in your startup, you don't want to load those settings again if you need them in an endpoint.
You can acheive this using [Dependencies Cache Scopes](dependencies-cache-scopes.md){.internal-link target=_blank}:

```Python hl_lines="13"
{!../../../docs_src/dependencies/tutorial014.py!}
```

## Setting the lifetime of a startup dependency

If you have a startup dependency that uses `yield` to execute teardown, you probably want to keep that dependency alive for the lifetime of your app and only execute the teardown when the app shuts down.
You can acheive this using [Dependency Lifetimes](dependencies-lifetimes.md){.internal-link target=_blank}.

To see this in action, see the [Async SQL Databases](../../advanced/async-sql-databases.md){.internal-link target=_blank} tutorial.
