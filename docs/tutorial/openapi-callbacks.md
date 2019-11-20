There are cases where the API that is being developed will require the clients to implement callback handlers, that will in turn be invoked
by the application. 

Since this is a cuommon usecase, the OpenAPI spec defines how these callbacks should be documented: <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#callbackObject">OpenAPI callback object spec</a>,
and there are also some more detailed examples available <a href="https://swagger.io/docs/specification/callbacks/">Swagger callback example</a>.

## Use case

Often, clients of a `FastAPI` application, will need to register callback handlers that will be notified when certain events occur.

An example of this shown below is having the clients implement a simple `health` endpoint that the application invokes at given times to check if the registered clients are still are still available.

```Python
{!./src/openapi_callbacks/tutorial001.py!}
```

