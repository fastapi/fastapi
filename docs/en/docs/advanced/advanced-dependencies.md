# Advanced Dependencies { #advanced-dependencies }

## Parallel dependency resolution (opt-in) { #parallel-dependency-resolution-opt-in }

FastAPI can resolve independent dependencies in parallel to reduce overall latency.

This is disabled by default. You can opt in per-application, and you can also control
it per dependency.

- Application-wide default (disabled by default):
  - Set `depends_default_parallelizable=True` in `FastAPI(...)` to allow parallel
    resolution by default.
- Per-dependency override:
  - Use `Depends(..., parallelizable=True | False)` (and the same for `Security(...)`).
  - If not provided, the application default is used.

When parallelization is enabled, dependencies at the same level of the dependency graph
that are not "context sensitive" will be resolved concurrently.

Context sensitive dependencies are always resolved sequentially:

- Dependencies implemented with `yield` (generator or async generator dependencies).
- Dependencies explicitly marked with `parallelizable=False`.

Dependency errors are still raised in the order of declaration, even if resolved in
parallel. Caching (`use_cache=True`, the default) still works per request: concurrent
callers share a single in-flight execution and the same result.

### Enable globally

{* ../../docs_src/dependencies/parallel_global_opt_in.py *}

### Enable/disable per dependency

{* ../../docs_src/dependencies/parallel_per_dep_enable.py *}

You can also opt out for a specific dependency when the app default is parallel:

{* ../../docs_src/dependencies/parallel_per_dep_disable.py *}

### Security dependencies

`Security(...)` supports the same `parallelizable` flag. Caching for security dependencies
respects OAuth2 scopes: dependencies with the same scopes share a cached value within
one request, different scopes result in separate executions.

{* ../../docs_src/dependencies/parallel_security.py *}

### Notes

- Sync (regular `def`) dependencies participate via a threadpool.
- Generator (`yield`) dependencies are always sequential.
- Errors from dependencies are raised respecting the declaration order.

## Parameterized dependencies { #parameterized-dependencies }

All the dependencies we have seen are a fixed function or class.

But there could be cases where you want to be able to set parameters on the dependency, without having to declare many different functions or classes.

Let's imagine that we want to have a dependency that checks if the query parameter `q` contains some fixed content.

But we want to be able to parameterize that fixed content.

## A "callable" instance { #a-callable-instance }

In Python there's a way to make an instance of a class a "callable".

Not the class itself (which is already a callable), but an instance of that class.

To do that, we declare a method `__call__`:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[12] *}

In this case, this `__call__` is what **FastAPI** will use to check for additional parameters and sub-dependencies, and this is what will be called to pass a value to the parameter in your *path operation function* later.

## Parameterize the instance { #parameterize-the-instance }

And now, we can use `__init__` to declare the parameters of the instance that we can use to "parameterize" the dependency:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[9] *}

In this case, **FastAPI** won't ever touch or care about `__init__`, we will use it directly in our code.

## Create an instance { #create-an-instance }

We could create an instance of this class with:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[18] *}

And that way we are able to "parameterize" our dependency, that now has `"bar"` inside of it, as the attribute `checker.fixed_content`.

## Use the instance as a dependency { #use-the-instance-as-a-dependency }

Then, we could use this `checker` in a `Depends(checker)`, instead of `Depends(FixedContentQueryChecker)`, because the dependency is the instance, `checker`, not the class itself.

And when solving the dependency, **FastAPI** will call this `checker` like:

```Python
checker(q="somequery")
```

...and pass whatever that returns as the value of the dependency in our *path operation function* as the parameter `fixed_content_included`:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[22] *}

/// tip

All this might seem contrived. And it might not be very clear how is it useful yet.

These examples are intentionally simple, but show how it all works.

In the chapters about security, there are utility functions that are implemented in this same way.

If you understood all this, you already know how those utility tools for security work underneath.

///
