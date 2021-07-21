# App lifespan scoped dependencies

FastAPI supports dependencies that get created once, when the app starts, and are cached thereafter.
This can be used, for example, to load your config from environment variables or initialize database connections.

Let's say we have a `Database` object which uses a `.connect` context manager to establish a connection.
Our goal is to create the connection _once_, and keep it alive for the lifespan of the app.

```Python hl_lines="7-14"
{!../../../docs_src/dependencies/tutorial013.py!}
```

We want to populate the hostname using our application's configuration,
which we define using Pydantic's `BaseSettings` Model (see [Settings and Environment Variables](../../advanced/settings.md){.internal-link}):

```Python hl_lines="18-19"
{!../../../docs_src/dependencies/tutorial013.py!}
```

In order to get `Database` wired up with the config and connected, we create a couple of dependencies:

```Python hl_lines="22-30"
{!../../../docs_src/dependencies/tutorial013.py!}
```

And then we can define our app and endpoint.
Notice that we mark the `DBConnection` dependency with `lifespan="app"`.

```Python hl_lines="33-38"
{!../../../docs_src/dependencies/tutorial013.py!}
```

!!! tip
    There are only 2 valid options for the `lifespan` parameter:
    - ``"request"`: the default, you don't need to set this explicitly
    - `"app"`: tied to the app's startup/shutdown lifecycle


Now the first time your app gets a request, the connection will be created on the fly, based on your apps config,
and will be persisted for the lifespan of the app.

!!! tip
    Shutdown events can be handled by using dependencies with `yield` (see [Dependencies with yield](dependencies-with-yield.md){.internal-link}).

!!! tip
    You only need to mark the root of your startup dependency tree with the `"app"` lifespan,
    any sub-dependencies will automatically be cached.
