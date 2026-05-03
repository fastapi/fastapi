# JSON request body { #json-request-body }

Minimal end-to-end example: a helper `register_post_route` takes `schema: type[ItemBase]`. The path operation stays the same, while `Gadget` and `Part` change both the OpenAPI schema and the expected JSON body.

The same `Annotated[..., Body(), Depends(schema)]` pattern works for all methods whenever you send JSON body.

This file uses `POST` only to stay short. See [Which HTTP methods?](index.md#which-http-methods) on the overview page.

## Models { #models }

{* ../../docs_src/body_depends_model_merge_body/tutorial001_an_py310.py ln[10:19] hl[10:19] *}

## The path operation { #the-path-operation }

The parameter uses `ItemBase` for static typing, `Body()` so FastAPI treats the payload as JSON, and `Depends(schema)` so validation uses the class supplied when the route is registered. `register_post_route` wraps that in a factory; registrations mount `items_router` at prefix `/items`, so the paths are `/items/objects/gadgets/` and `/items/objects/parts/`:

{* ../../docs_src/body_depends_model_merge_body/tutorial001_an_py310.py ln[22:53] hl[22:53] *}

See [overview](index.md) for context and alternatives.
