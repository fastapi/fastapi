# Query parameters { #query-parameters }

The same runtime `schema` idea as JSON `Body()` applies to query parameters: keep a base model in the type position and pass `Depends(schema)` when `schema` is fixed only at registration time. `Query()` must stay in `Annotated` so FastAPI reads fields from the query string. A bare base model on `GET` would still default to a body parameter.

## Models { #models }

{* ../../docs_src/body_depends_model_merge_query/tutorial001_an_py310.py ln[10:20] hl[10:20] *}

## The path operation { #the-path-operation }

{* ../../docs_src/body_depends_model_merge_query/tutorial001_an_py310.py ln[23:38] hl[23:38] *}

You can still use `Annotated[SomeModel, Query()]` without `Depends` when your class never changes.
And if it does, you can do `Annotated[SomeModelBase, Depends(SomeModel)]` to keep proper annotation.
But if you need to explicitly state that the `Query` is required here, follow the example.

## List routes wired with `schema` { #list-routes-wired-with-schema }

One helper registers `/catalog/items/` (full filters), `/catalog/items-paginated/` (pagination fields), and `/catalog/basics/` (only the base fields):

{* ../../docs_src/body_depends_model_merge_query/tutorial001_an_py310.py ln[41:59] hl[41:59] *}

More on query handling: [Query params](../../tutorial/query-params.md), [Query parameter models](../../tutorial/query-param-models.md). [Overview](index.md) for this feature set.
