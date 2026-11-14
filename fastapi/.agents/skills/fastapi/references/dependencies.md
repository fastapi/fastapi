# Dependency Injection

Use dependencies when:

* They can't be declared in Pydantic validation and require additional logic
* The logic depends on external resources or could block in any other way
* Other dependencies need their results (it's a sub-dependency)
* The logic can be shared by multiple endpoints to do things like error early, handle authentication, etc.
* They need to handle cleanup (e.g., DB sessions, file handles), using dependencies with `yield`
* Their logic needs input data from the request, like headers, query parameters, etc.

## Dependencies with `yield` and `scope`

When using dependencies with `yield`, they can have a `scope` that defines when the exit code is run.

Use the default scope `"request"` to run the exit code after the response is sent back.

```python
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()


DBDep = Annotated[DBSession, Depends(get_db)]


@app.get("/items/")
def read_items(db: DBDep):
    return db.query(Item).all()
```

Use the scope `"function"` when they should run the exit code after the response data is generated but before the response is sent back to the client.

```python
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


def get_username():
    try:
        yield "Rick"
    finally:
        print("Clean up before response is sent")


UserNameDep = Annotated[str, Depends(get_username, scope="function")]


@app.get("/users/me")
def get_user_me(username: UserNameDep):
    return username
```

## Limit dependency concurrency

Use `max_concurrency` when concurrent dependency calls could exhaust a shared resource, such as a database connection pool.

* Put the limit on the dependency that manages the resource. Its sub-dependencies run before its limit is applied.
* Choose a positive integer from the resource's configured capacity, allowing for other code that uses it. FastAPI doesn't detect the pool size. The default `None` adds no limit.
* Declare one `Annotated` alias and reuse it in the routes that should share the limit. A new `Depends()` object creates a separate limit, even for the same dependency function.

For the `get_db()` dependency above, if the pool has capacity available for five sessions:

```python
DBDep = Annotated[DBSession, Depends(get_db, max_concurrency=5)]
```

Extra calls wait without occupying worker threads. For a dependency with `yield`, FastAPI holds the slot until cleanup finishes, at the time determined by `scope`. Without `yield`, the slot is released when the dependency function finishes.

Each worker process applies its own limit. Account for this when several workers share an external resource.

Before limiting repeated or nested resource dependencies, check whether a request could hold a slot while waiting for another. See [dependencies that need more than one resource](https://fastapi.tiangolo.com/advanced/advanced-dependencies/#dependencies-that-need-more-than-one-resource) for these cases.

## Class Dependencies

Avoid creating class dependencies when possible.

If a class is needed, instead create a regular function dependency that returns a class instance.

Do this:

```python
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


@dataclass
class DatabasePaginator:
    offset: int = 0
    limit: int = 100
    q: str | None = None

    def get_page(self) -> dict:
        # Simulate a page of data
        return {
            "offset": self.offset,
            "limit": self.limit,
            "q": self.q,
            "items": [],
        }


def get_db_paginator(
    offset: int = 0, limit: int = 100, q: str | None = None
) -> DatabasePaginator:
    return DatabasePaginator(offset=offset, limit=limit, q=q)


PaginatorDep = Annotated[DatabasePaginator, Depends(get_db_paginator)]


@app.get("/items/")
async def read_items(paginator: PaginatorDep):
    return paginator.get_page()
```

instead of this:

```python
# DO NOT DO THIS
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


class DatabasePaginator:
    def __init__(self, offset: int = 0, limit: int = 100, q: str | None = None):
        self.offset = offset
        self.limit = limit
        self.q = q

    def get_page(self) -> dict:
        # Simulate a page of data
        return {
            "offset": self.offset,
            "limit": self.limit,
            "q": self.q,
            "items": [],
        }


@app.get("/items/")
async def read_items(paginator: Annotated[DatabasePaginator, Depends()]):
    return paginator.get_page()
```
