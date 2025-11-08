# Lifespan Scoped Dependencies

## Intro

So far we've used dependencies which are evaluated once for every incoming request. However, 
this is not always ideal:

* Sometimes dependencies have a large setup/teardown time. Running it for every request will result in bad performance.
* Sometimes dependencies need to have their values shared throughout the lifespan
of the application between multiple requests.


An example of this would be a connection to a database. Databases are typically
less efficient when working with lots of connections and would prefer to have connections
re-used across different operations.

For such cases can be solved by using "lifespan scoped dependencies".


## What is a lifespan scoped dependency?
Lifespan scoped dependencies work similarly to the (endpoint scoped)
dependencies we've worked with so far except for the following differences: 

* Lifespan scoped dependencies will only be called once, during the application's startup process.
* Lifespan scoped dependencies will share their values amongst all requests the application receives.
* Lifespan scoped dependencies will only be cleaned during the application's shutdown process.


## Create a lifespan scoped dependency

You may declare a dependency as a lifespan scoped dependency by passing
`scope="lifespan"` to the `Depends` function:

{* ../../docs_src/dependencies/tutorial013a_an_py39.py *}

/// tip

In the example above we saved the annotation to a separate variable, and then
reused it in our endpoints. This is not a requirement, we could also declare
the exact same annotation in both endpoints. However, it is recommended that you
do save the annotation to a variable so you won't accidentally forget to pass
`scope="lifespan"` to some of the endpoints (Causing the endpoint
to create a new database connection for every request).
It will also be more intuitive to use the exact same annotation, reminding us that the 
we are using the exact same value across all endpoints. 

///

In this example, the `get_database_connection` dependency will be executed once,
during the application's startup. **FastAPI** will internally save the resulting
connection object, and whenever the `read_users` and `read_items` endpoints are
called, they will be using the previously saved connection. Once the application
shuts down, **FastAPI** will make sure to gracefully close the connection object.

## The `use_cache` argument

The `use_cache` argument works similarly to the way it worked with endpoint
scoped dependencies. Meaning, as **FastAPI** gathers lifespan scoped dependencies, it
will cache dependencies it already encountered before. However, you can disable
this behavior by passing `use_cache=False` to `Depends`. This will cause a new lifespan 
dependency to be created for every endpoint/dependency/router where it shows up:

{* ../../docs_src/dependencies/tutorial013b_an_py39.py *}

In this example, we used a lifespan scoped dependency in a total of 4 places:
 
* The `read_item` endpoint (with `use_cache=True`)
* The `read_items` endpoint (with `use_cache=True`)
* The `read_users` endpoint (with `use_cache=False`)
* The `read_groups` endpoint (with `use_cache=False`)

Since the `read_item` and `read_items` endpoints enabled the cache, they will use the same connection.
However, since the `read_user` and `read_groups` disabled the cache, each of them will receive a new, 
dedicated connection for the application lifespan.

In total, we will have 3 connections created for our application which will remain for its entire lifespan:
* One connection will be shared across all requests for the `read_items` and `read_item` endpoints.
* A second connection will be shared across all requests for the `read_users` endpoint.
* A third and final connection will be shared across all requests for the `read_groups` endpoint.


## Lifespan Scoped Sub-Dependencies
Just like with endpoint scoped dependencies, lifespan scoped dependencies may
use other lifespan scoped sub-dependencies themselves:

{* ../../docs_src/dependencies/tutorial013c_an_py39.py *}

Endpoint scoped dependencies may use lifespan scoped sub dependencies as well:

{* ../../docs_src/dependencies/tutorial013d_an_py39.py *}

Here, we defined an endpoint-scoped dependency called `get_user_record` which will fetch 
the information of the given user from the database. It uses a lifespan-scoped sub-dependency called 
`get_database_connection`, which allows us to re-use the same connection each time the dependency is called.

## Dependency Scope Conflicts
By definition, lifespan scoped dependencies are being setup in the application's
startup process, before any request is ever being made to an endpoint.
Therefore, it doesn't make sense for a lifespan scoped dependency to use any
parameters that only make sense in the context of an endpoint.

That includes but not limited to:

* Parts of the request (like `Body`, `Query` and `Path`)
* The request/response objects themselves (like `Request`, `Response` and `WebSocket`)
* Sub-dependencies with smaller scopes (Like `"request"` or `"function"`).

Defining a dependency with such parameters will raise a `DependencyScopeError`.
