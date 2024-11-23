# Lifespan Scoped Dependencies

So far we've used dependencies which are "endpoint scoped". Meaning, they are
called again and again for every incoming request to the endpoint. However,
this is not ideal for all kinds of dependencies.

Sometimes dependencies have a large setup/teardown time, or there is a need
for their value to be shared throughout the lifespan of the application. An
example of this would be a connection to a database. Databases are typically
less efficient when working with lots of connections and would prefer that
clients would create a single connection for their operations.

For such cases, you might want to use "lifespan scoped" dependencies.

## Intro

Lifespan scoped dependencies work similarly to the dependencies we've worked
with so far (which are endpoint scoped). However, they are called once and only
once in the application's lifespan (instead of being called again and again for
every request). The returned value will be shared across all requests that need
it.


## Create a lifespan scoped dependency

You may declare a dependency as a lifespan scoped dependency by passing
`dependency_scope="lifespan"` to the `Depends` function:

{* ../../docs_src/dependencies/tutorial013a_an_py39.py hl[16] *}

/// tip

In the example above we saved the annotation to a separate variable, and then
reused it in our endpoints. This is not a requirement, we could also declare
the exact same annotation in both endpoints. However, it is recommended that you
do save the annotation to a variable so you won't accidentally forget to pass
`dependency_scope="lifespan"` to some of the endpoints (Causing the endpoint
to create a new database connection for every request).

///

In this example, the `get_database_connection` dependency will be executed once,
during the application's startup. **FastAPI** will internally save the resulting
connection object, and whenever the `read_users` and `read_items` endpoints are
called, they will be using the previously saved connection. Once the application
shuts down, **FastAPI** will make sure to gracefully close the connection object.

## The `use_cache` argument

The `use_cache` argument works similarly to the way it worked with endpoint
scoped dependencies. Meaning as **FastAPI** gathers lifespan scoped dependencies, it
will cache dependencies it already encountered before. However, you can disable
this behavior by passing `use_cache=False` to `Depends`:

{* ../../docs_src/dependencies/tutorial013b_an_py39.py hl[16] *}

In this example, the `read_users` and `read_groups` endpoints are using
`use_cache=False` whereas the `read_items` and `read_item` are using
`use_cache=True`. That means that we'll have a total of 3 connections created
for the duration of the application's lifespan. One connection will be shared
across all requests for the `read_items` and `read_item` endpoints. A second
connection will be shared across all requests for the `read_users` endpoint. The
third and final connection will be shared across all requests for the
`read_groups` endpoint.


## Lifespan Scoped Sub-Dependencies
Just like with endpoint scoped dependencies, lifespan scoped dependencies may
use other lifespan scoped sub-dependencies themselves:

{* ../../docs_src/dependencies/tutorial013c_an_py39.py hl[16] *}

Endpoint scoped dependencies may use lifespan scoped sub dependencies as well:

{* ../../docs_src/dependencies/tutorial013d_an_py39.py hl[16] *}

/// note

You can pass `dependency_scope="endpoint"` if you wish to explicitly specify
that a dependency is endpoint scoped. It will work the same as not specifying
a dependency scope at all.

///

As you can see, regardless of the scope, dependencies can use lifespan scoped
sub-dependencies.

## Dependency Scope Conflicts
By definition, lifespan scoped dependencies are being setup in the application's
startup process, before any request is ever being made to any endpoint.
Therefore, it is not possible for a lifespan scoped dependency to use any
parameters that require the scope of an endpoint.

That includes but not limited to:
    * Parts of the request (like `Body`, `Query` and `Path`)
    * The request/response objects themselves (like `Request`, `Response` and `WebSocket`)
    * Endpoint scoped sub-dependencies.

Defining a dependency with such parameters will raise an `InvalidDependencyScope` error.
