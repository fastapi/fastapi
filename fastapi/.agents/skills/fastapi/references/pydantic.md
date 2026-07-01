# Pydantic

## Do not use Ellipsis

Do not use `...` as a default value for required parameters or model fields. It's not needed and not recommended.

Do this, without Ellipsis (`...`):

```python
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(gt=0)


@app.post("/items/")
async def create_item(item: Item, project_id: Annotated[int, Query()]):
    return item
```

Instead of:

```python
# DO NOT DO THIS
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str = ...
    description: str | None = None
    price: float = Field(..., gt=0)


@app.post("/items/")
async def create_item(item: Item, project_id: Annotated[int, Query(...)]):
    return item
```

## Do not use Pydantic RootModels

Do not use Pydantic `RootModel`; instead use regular type annotations with `Annotated` and Pydantic validation utilities.

For example, for a list with validations:

```python
from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import Field

app = FastAPI()


@app.post("/items/")
async def create_items(items: Annotated[list[int], Field(min_length=1), Body()]):
    return items
```

Instead of:

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

FastAPI supports these type annotations and will create a Pydantic `TypeAdapter` for them, so types work normally without custom wrapper models.
