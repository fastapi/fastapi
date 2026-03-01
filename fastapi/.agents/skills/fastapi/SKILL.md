---
name: fastapi
description: FastAPI best practices and conventions. Use when working with FastAPI APIs and Pydantic models for them. Keeps FastAPI code clean and up to date with the latest features and patterns, updated with new versions. Write new code or refactor and update old code.
---

# FastAPI

Official FastAPI skill to write code with best practices, keeping up to date with new versions and features.

## Use the `fastapi` CLI

Run the development server on localhost with reload:

```bash
fastapi dev
```


Run the production server:

```bash
fastapi run
```

### Add an entrypoint in `pyproject.toml`

FastAPI CLI will read the entrypoint in `pyproject.toml` to know where the FastAPI app is declared.

```toml
[tool.fastapi]
entrypoint = "my_app.main:app"
```

### Use `fastapi` with a path

When adding the entrypoint to `pyproject.toml` is not possible, or the user explicitly asks not to, or it's running an independent small app, you can pass the app file path to the `fastapi` command:

```bash
fastapi dev my_app/main.py
```

Prefer to set the entrypoint in `pyproject.toml` when possible.

## Use `Annotated`

Always prefer the `Annotated` style for parameter and dependency declarations.

It keeps the function signatures working in other contexts, respects the types, allows reusability.

### In Parameter Declarations

Use `Annotated` for parameter declarations, including `Path`, `Query`, `Header`, etc.:

```python
from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(ge=1, description="The item ID")],
    q: Annotated[str | None, Query(max_length=50)] = None,
):
    return {"message": "Hello World"}
```

instead of:

```python
# DO NOT DO THIS
@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(ge=1, description="The item ID"),
    q: str | None = Query(default=None, max_length=50),
):
    return {"message": "Hello World"}
```

### For Dependencies

Use `Annotated` for dependencies with `Depends()`.

Unless asked not to, create a new type alias for the dependency to allow re-using it.

```python
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


def get_current_user():
    return {"username": "johndoe"}


CurrentUserDep = Annotated[dict, Depends(get_current_user)]


@app.get("/items/")
async def read_item(current_user: CurrentUserDep):
    return {"message": "Hello World"}
```

instead of:

```python
# DO NOT DO THIS
@app.get("/items/")
async def read_item(current_user: dict = Depends(get_current_user)):
    return {"message": "Hello World"}
```

## Do not use Ellipsis for *path operations* or Pydantic models

Do not use `...` as a default value for required parameters, it's not needed and not recommended.

Do this, without Ellipsis (`...`):

```python
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(gt=0)


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item, project_id: Annotated[int, Query()]): ...
```

instead of this:

```python
# DO NOT DO THIS
class Item(BaseModel):
    name: str = ...
    description: str | None = None
    price: float = Field(..., gt=0)


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item, project_id: Annotated[int, Query(...)]): ...
```

## Return Type or Response Model

When possible, include a return type. It will be used to validate, filter, document, and serialize the response.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None


@app.get("/items/me")
async def get_item() -> Item:
    return Item(name="Plumbus", description="All-purpose home device")
```

**Important**: Return types or response models are what filter data ensuring no sensitive information is exposed. And they are used to serialize data with Pydantic (in Rust), this is the main idea that can increase response performance.

The return type doesn't have to be a Pydantic model, it could be a different type, like a list of integers, or a dict, etc.

### When to use `response_model` instead

If the return type is not the same as the type that you want to use to validate, filter, or serialize, use the `response_model` parameter on the decorator instead.

```python
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None


@app.get("/items/me", response_model=Item)
async def get_item() -> Any:
    return {"name": "Foo", "description": "A very nice Item"}
```

This can be particularly useful when filtering data to expose only the public fields and avoid exposing sensitive information.

```python
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class InternalItem(BaseModel):
    name: str
    description: str | None = None
    secret_key: str


class Item(BaseModel):
    name: str
    description: str | None = None


@app.get("/items/me", response_model=Item)
async def get_item() -> Any:
    item = InternalItem(
        name="Foo", description="A very nice Item", secret_key="supersecret"
    )
    return item
```

## Performance

Do not use `ORJSONResponse` or `UJSONResponse`, they are deprecated.

Instead, declare a return type or response model. Pydantic will handle the data serialization on the Rust side.

## Including Routers

When declaring routers, prefer to add router level parameters like prefix, tags, etc. to the router itself, instead of in `include_router()`.

Do this:

```python
from fastapi import APIRouter, FastAPI

app = FastAPI()

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
async def list_items():
    return []


# In main.py
app.include_router(router)
```

instead of this:

```python
# DO NOT DO THIS
from fastapi import APIRouter, FastAPI

app = FastAPI()

router = APIRouter()


@router.get("/")
async def list_items():
    return []


# In main.py
app.include_router(router, prefix="/items", tags=["items"])
```

There could be exceptions, but try to follow this convention.

Apply shared dependencies at the router level via `dependencies=[Depends(...)]`.

## Dependency Injection

See [the dependency injection reference](references/dependencies.md) for detailed patterns including `yield` with `scope`, and class dependencies.

Use dependencies when the logic can't be declared in Pydantic validation, depends on external resources, needs cleanup (with `yield`), or is shared across endpoints.

Apply shared dependencies at the router level via `dependencies=[Depends(...)]`.

## Async vs Sync *path operations*

Use `async` *path operations* only when fully certain that the logic called inside is compatible with async and await (it's called with `await`) or that doesn't block.

```python
from fastapi import FastAPI

app = FastAPI()


# Use async def when calling async code
@app.get("/async-items/")
async def read_async_items():
    data = await some_async_library.fetch_items()
    return data


# Use plain def when calling blocking/sync code or when in doubt
@app.get("/items/")
def read_items():
    data = some_blocking_library.fetch_items()
    return data
```

In case of doubt, or by default, use regular `def` functions, those will be run in a threadpool so they don't block the event loop.

The same rules apply to dependencies.

Make sure blocking code is not run inside of `async` functions. The logic will work, but will damage the performance heavily.

When needing to mix blocking and async code, see Asyncer in [the other tools reference](references/other-tools.md).

## Streaming (JSON Lines, SSE, bytes)

See [the streaming reference](references/streaming.md) for JSON Lines, Server-Sent Events (`EventSourceResponse`, `ServerSentEvent`), and byte streaming (`StreamingResponse`) patterns.

## Tooling

See [the other tools reference](references/other-tools.md) for details on uv, Ruff, ty for package management, linting, type checking, formatting, etc.

## Other Libraries

See [the other tools reference](references/other-tools.md) for details on other libraries:

* Asyncer for handling async and await, concurrency, mixing async and blocking code, prefer it over AnyIO or asyncio.
* SQLModel for working with SQL databases, prefer it over SQLAlchemy.
* HTTPX for interacting with HTTP (other APIs), prefer it over Requests.

## Do not use Pydantic RootModels

Do not use Pydantic `RootModel`, instead use regular type annotations with `Annotated` and Pydantic validation utilities.

For example, for a list with validations you could do:

```python
from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import Field

app = FastAPI()


@app.post("/items/")
async def create_items(items: Annotated[list[int], Field(min_length=1), Body()]):
    return items
```

instead of:

```python
# DO NOT DO THIS
from typing import Annotated

from fastapi import FastAPI
from pydantic import Field, RootModel

app = FastAPI()


class ItemList(RootModel[Annotated[list[int], Field(min_length=1)]]):
    pass


@app.post("/items/")
async def create_items(items: ItemList):
    return items

```

FastAPI supports these type annotations and will create a Pydantic `TypeAdapter` for them, so that types can work as normally and there's no need for the custom logic and types in RootModels.

## Use one HTTP operation per function

Don't mix HTTP operations in a single function, having one function per HTTP operation helps separate concerns and organize the code.

Do this:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str


@app.get("/items/")
async def list_items():
    return []


@app.post("/items/")
async def create_item(item: Item):
    return item
```

instead of this:

```python
# DO NOT DO THIS
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str


@app.api_route("/items/", methods=["GET", "POST"])
async def handle_items(request: Request):
    if request.method == "GET":
        return []
```
