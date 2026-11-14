# Parameter Models

Use `Annotated[Model, Query()]`, `Header()`, `Cookie()`, or `Form()` to group related inputs. Multiple models can coexist with individual parameters and dependencies. Do not add dependency wrappers just to unpack fields into models.

Each model validates independently. Request fields stay flat, without keys named after the function parameters.

## Multiple and optional models

```python
from datetime import date
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class Pagination(BaseModel):
    limit: int = Field(10, ge=1)
    offset: int = Field(0, ge=0)


class DateRange(BaseModel):
    start: date
    end: date


@app.get("/items/")
def read_items(
    pagination: Annotated[Pagination, Query()],
    date_range: Annotated[DateRange | None, Query()] = None,
    search: str | None = None,
):
    return {"pagination": pagination, "date_range": date_range, "search": search}
```

* Use `Model | None` with `= None` to make a group optional. `| None` alone still makes it required.
* With the default `extra="ignore"`, omitting both `start` and `end` leaves `date_range` as `None`, even when `limit` or `search` is sent.
* Sending either field triggers validation and requires both. Keep required model fields required when making the group optional.
* Apply the same pattern with `Header()`, `Cookie()`, and `Form()`.

## Extra fields and shared names

Each model's `extra` setting applies to all submitted fields in the same location, including sibling parameters and dependencies. For forms, this includes files.

* `extra="ignore"` is the default and lets independent groups coexist.
* `extra="forbid"` rejects sibling fields outside that model.
* `extra="allow"` includes sibling fields as extras. These make an optional model present, triggering validation of required fields. Ordinary headers such as `Host` also count for header models.

Shared names or aliases are validated independently by every model that declares them. Keep their types and constraints compatible. Use distinct names or aliases for independent inputs.

## Forms and unions

Forms require `python-multipart`. Combine form models with other form models, individual `Form` parameters, and `File` parameters. Use `multipart/form-data` when uploading files.

Forms also support optional unions such as `contact: Annotated[Person | Company | None, Form(discriminator="kind")] = None`. Give each model a distinct `Literal` value for `kind`. Unions can coexist with other unions, models, form fields, and files.

An empty submitted form value counts as supplying a field and triggers validation. Omitted boolean fields use defaults or produce missing-field errors. Use `False` defaults for HTML checkboxes.

See the [query model documentation](https://fastapi.tiangolo.com/tutorial/query-param-models/) and [form model documentation](https://fastapi.tiangolo.com/tutorial/request-form-models/) for more examples.
