# Dependency Cache Scopes

In FastAPI, if one of your dependencies is declared multiple times for the same *path operation*, for example, multiple dependencies have a common sub-dependency, **FastAPI** will know to call that sub-dependency only once per request.

And it will save the returned value in a <abbr title="A utility/system to store computed/generated values, to re-use them instead of computing them again.">"cache"</abbr> and pass it to all the "dependants" that need it in that specific request, instead of calling the dependency multiple times for the same request.

But you may not want this behavior. FastAPI let's you control this via _cache scopes_. You can set the _cache scope_ using the `use_cache` parameter to `Depends()`. For example, to disable the cache for a dependency:

```Python hl_lines="1"
def needy_dependency(fresh_value: str = Depends(get_value, use_cache=False)):
    return {"fresh_value": fresh_value}
```

You may also find situations where you only want your dependencies to be created _once_.
For example, if you are loading a config from enviroment variables using [Pydantic's settings management](../../advanced/settings.md){.internal-link target=_blank}, you probably only want that to happen once, and be cached therafter.
For this situation, set `use_cache="app"` to cache the dependencies value for the lifetime of your application:

```Python hl_lines="4"
def load_config():
    return Config()

def dependent(cfg: Config = Depends(load_config, use_cache="app")):
    return cfg.some_value
```

!!! note "Technical Details"
    FastAPI caches your dependencies based on the callable's identity.
    If your dependency is a class or function, the cache will be based on `id(ClassName)` or `id(function_name)`.
    However if your dependency is an _instance_ of a class implementing `__call__`, only that particular _instance_ will be cached.

## DependencyCacheScopes

To be more explicit, you can also use the `fastapi.dependencies.cache.DependencyCacheScopes` enumeration to set values:

```Python
from fastapi.dependencies.cache import DependencyCacheScopes

def dependent(cfg: Config = Depends(load_config, use_cache=DependencyCacheScopes.app)):
    return cfg.some_value
```

!!! note "Technical Details"
    FastAPI uses `fastapi.dependencies.cache.DependencyCacheScopes` internally.
    When you pass in `use_cache={True,False,"app"}` it gets converted to a value from `DependencyCacheScopes`.
    The scalar values of `{True,False,"app"}` are supported so that you don't have to import `fastapi.dependencies.cache.DependencyCacheScopes` all over the place, but if you are using dependency scopes extensively it may be clearer to use `DependencyCacheScopes` directly.

## Dependencies in multiple scopes

If a dependency is cached in the `"app"` scope, it will be used for any dependencies declared with the default scope (`use_cache=True`, scoped to a single request).

If you need to use a dependency both in the `"app"` scope and seperately at the individual request scope, you have two options.

### Disable cache for the shared dependency

You can mark the dependencies at the request scope with `Depends(..., use_cache=False)`, but note that they will not be cached at all in the request scope:

```Python hl_lines="6"
def random_num() -> float:
    return random.random()

async def dependent(
    app_value: float = Depends(random_num, use_cache="app"),
    request_value_1: float = Depends(random_num, use_cache=False),
    request_value_2: float = Depends(random_num, use_cache=False),
):
    assert request_value_1 != request_value_2
```

However, now there will be no caching done at the request level.
In this example, `app_value` will always have the same value while `request_value_1` and `request_value_2` will each have a new unique value every call.

### Specialize the dependency

If you want to have caching at _both_ the `"app"` scope _and_ the `"request"` scope, you can specialize your dependency itself.
If your dependency is a class, you can sublcass it:

```Python
class Dependency:
    ...


class DependencyApp(Dependency):
    ...

class DependencyRequest(Dependency):
    ...
```

Or if it's a function, you can wrap it:

```Python
def random_num_app()
    return random_num()

def random_num_request():
    return random_num()

async def dependent(
    app_value: float = Depends(random_num_app, use_cache="app"),
    request_value_1: float = Depends(random_num_request),
    request_value_2: float = Depends(random_num_request),
):
    assert request_value_1 == request_value_2
```

Now `app_value` will still be the same every call while `request_value_1` and `request_value_2` will be different every call.
But `request_value_1` and `request_value_2` will share the same value, and `random_num_request` will only be called once per request.

## Recap

In total, **FastAPI** supports **3** _cache scopes_:

- `True`: this is the default. The dependency's value is cached for that individual request.
- `False`: this completely disables the cache that dependency.
- `"app"`: the dependency's value is cached for the lifetime of the app.

These cache scopes are set via the `use_cache` parameter to `Depends()`.

You can also use the values of `fastapi.dependencies.cache.DependencyCacheScopes` directly to be more explicit:

- `DependencyCacheScopes.request`: equivalent to `True`.
- `DependencyCacheScopes.nocache`: equivalent to `False`.
- `DependencyCacheScopes.app`: equivalent to `"app"`.

!!! note "Info"
    You may be asking yourself what happens if you ask **FastAPI** to cache your dependency's value for the lifetime of your app when using [Dependencies with yield](dependencies-with-yield.md){.internal-link target=_blank}
    The handling of teardown for dependencies with yield can be controlled indpendently of the caching of the dependency's yielded value.
    Read onto [Dependency lifetimes (the next section)](dependencies-with-yield.md){.internal-link target=_blank} to find out more!
