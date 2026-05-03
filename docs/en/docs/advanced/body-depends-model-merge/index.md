# Composing Annotated metadata for runtime validation schemas { #composing-annotated-metadata-for-runtime-validation-schemas }

Several FastAPI helpers can live together inside one [`typing.Annotated`](../../python-types.md#type-hints-with-metadata-annotations) annotation: a normal Python type for your editor and for static analysis, plus markers such as `Body()`, `Form()`, `File()`, or `Query()` so FastAPI knows **where** to read the request, and `Depends(SomeModel)` so validation and OpenAPI know **which** Pydantic model to use.

Sometimes the provided model is not fixed in source. You might build routes from a factory: the caller provides a model to generate a new view that validates against the provided class and exposes the right API. You also want the annotation to stay meaningful for type checkers.

## Factories and dynamic models { #factories-and-dynamic-models }

The straightforward closure passes the runtime schema type straight into the parameter annotation. FastAPI can use that to build request parsing and OpenAPI, because it inspects the annotation when the application loads:

```python
def new_create_view(schema: type[ItemBase]):
    def create_view(
        item_in: schema,
    ):
        print("creating a new item based on", item_in)
        return ...

    return create_view
```

For mypy, Pyright, and other static tools, this pattern won't work: the type for type checking should be static, and here the annotation is defined in runtime. Checkers expect annotations to describe types in a way they can resolve without executing any code, so you lose precise checking on `item_in` and the type checker will complain about using a variable as an annotation.

Instead, you can use something wide as a static annotation, for example a shared base class. And the desired validation schema should be provided separately:

```python
def new_create_view(schema: type[ItemBase]):
    def create_view(
        item_in: Annotated[
            ItemBase,
            Body(),
            Depends(schema),
        ],
    ):
        print("creating a new item based on", item_in)
        return ...

    return create_view
```

The first argument to `Annotated` is the type you treat as `item_in` in typeshed-aware tooling: editors and checkers see `ItemBase`. Everything after it is metadata: `Body()` tells FastAPI the payload is a JSON body; `Depends(schema)` tells it which model class to use for validation and for generating OpenAPI for this route.

A natural shape looks like this:

```python
def register(
    router: APIRouter,
    path_suffix: str,
    schema: type[ItemBase],
) -> None:

    path = f"/create/{path_suffix}"

    @router.post(path)
    def create(
        item_in: Annotated[
            ItemBase,  # type annotation for the `item_in`
            Body(),  # hint for FastAPI to expect Body
            Depends(schema),  # required schema for body validation
        ]
    ):
        print("processing item", item_in)
        return ...
```

Older FastAPI kept only one of those `Annotated` markers. `Body()` could disappear, `Depends(schema)` was treated like an ordinary dependency, and the model fields were read from the query string instead of the JSON body.

## Another approach: a small dependency per route { #another-approach-a-small-dependency-per-route }

There's also another solution for older FastAPI versions, if you want to have proper annotation in the view and to specify the data location: create a new dependency function whose only parameter is the body, annotated with the desired model and `Body()`.

The new way to do this is described in the [JSON request body example](body.md), here's the old way to do it:

```python
from fastapi import APIRouter, Body, Depends, FastAPI
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str


class Gadget(ItemBase):
    description: str


class Part(ItemBase):
    sku: str


def register_post_route(
    router: APIRouter,
    path: str,
    schema: type[ItemBase],
) -> None:

    def parse_item(
        item: schema = Body(),
    ) -> ItemBase:
        return item

    @router.post(path)
    def create_item(
        item: ItemBase = Depends(parse_item),
    ):
        print("processing item", item)
        return ...


app = FastAPI()
items_router = APIRouter()
register_post_route(items_router, "/objects/gadgets/", Gadget)
register_post_route(items_router, "/objects/parts/", Part)
app.include_router(items_router, prefix="/items")
```

Each call to `register_post_route` closes over a different `schema`, so `parse_item` is not shared between routes. The tradeoff is boilerplate: an extra nested function and `Depends(...)` on the path-operation parameter, and also you will need to add ignore comments for mypy to skip the line with the `item: schema` annotation.

## Merge inside `Annotated` { #merge-inside-annotated }

FastAPI can combine `Body()`, `Form()`, `File()`, or `Query()` with `Depends(SomeModel)` when `SomeModel` is a subclass of Pydantic `BaseModel`. They collapse into one parameter: validation and OpenAPI use the model from `Depends`, while the first type argument to `Annotated` is what you use for static typing.

The order of `Body`, `Form`, `File`, `Query`, and `Depends` inside `Annotated` does not matter.

**You cannot mix** `Query()` with `Body()`, `Form()`, or `File()` in the same `Annotated` list.

## Which HTTP methods? { #which-http-methods }

The merge only fixes **where one parameter** is read. That is separate from the HTTP verb: `POST`, `PUT`, `PATCH`, `DELETE`, and the rest work the same for that parameter.

### Query string and a merged body in the same path operation { #query-string-and-a-merged-body-in-the-same-path-operation }

You cannot put `Query()` and `Body()` in the same `Annotated` list (see [limitations](#limitations)). You can add another parameter: e.g. bind data from the query string to one param, and bind payload from body to another parameter.

#### Models { #models }

Here we declare query models and record body models:

{* ../../docs_src/body_depends_model_merge_query_plus_body/tutorial001_an_py310.py ln[10:31] hl[10:31] *}

#### Path operation: merged query model + merged JSON body { #path-operation-merged-query-model-merged-json-body }

{* ../../docs_src/body_depends_model_merge_query_plus_body/tutorial001_an_py310.py ln[34:52] hl[34:52] *}

The `client_info` parameter uses merge for the query string:

- static `ClientInfoBase` as type annotation
- a `Query()` marker so FastAPI binds this parameter to query argument - bare `Query()` can be omitted, but it's ok to be placed to verbosely state that the query string should be processed here. Also, you will need to put `Query()` to provide extra OpenAPI options
- `Depends(client_schema)` for the provided model

The `record` parameter does the same for the JSON body with `Body()` and `Depends(record_schema)`.

The first argument to each `Annotated[...]` (`ClientInfoBase`, `RecordBase`) is what language servers and type checkers use for static analysis.


#### Handler body { #handler-body }

Inside the handler, your IDE can suggest attributes such as `client_info.client_id` and `record.title`, also anything from parent class is available too, for example the `.model_dump()` method. And tools like mypy or Pyright check those attributes against the provided types. At runtime, FastAPI still validates data with the provided classes.

{* ../../docs_src/body_depends_model_merge_query_plus_body/tutorial001_an_py310.py ln[53:57] hl[53:57] *}

#### Register routes { #register-routes }

Factories mount two POST routes under `/clients`, passing both record and client schemas:

{* ../../docs_src/body_depends_model_merge_query_plus_body/tutorial001_an_py310.py ln[62:81] hl[62:81] *}

The same layout applies if the body parameter uses `Form()` or `File()` with `Depends(schema)` instead of `Body()` - always as its own parameter alongside the merged query parameter, not mixed into one `Annotated`.

## When this matters { #when-this-matters }

It matters most when the validation model is chosen while registering routes (see the example above): your helper takes `schema: type[ItemBase]`, you want one implementation and several paths, and each path should expose the right OpenAPI schema. `Depends(schema)` alone means `Query`, but when you need to say where the data comes from, you need to provide `Body` / `Form` / `File` / `Query` as a hint for FastAPI.


## Examples { #examples }

* [JSON request body](body.md): `application/json`; the sample uses `POST` (same idea for `PUT`, `PATCH`, `DELETE` with a JSON body).
* [Form data](form.md): `application/x-www-form-urlencoded`.
* [File uploads](file.md): typical file upload flow.
* [Query parameters](query.md): `GET` with a query model chosen at registration time.

## Limitations { #limitations }

The shortcut applies only when:

* There is exactly one “shape” marker among `Body()`, `Form()`, `File()`, and `Query()`.
* There is exactly one `Depends`.
* You do not add other parameter markers such as `Path` or `Header` into the same `Annotated` bucket.

If the declaration does not match these rules, FastAPI may raise an exception.
