# Form data { #form-data }

Form-encoded data needs `Form()` in the metadata and `Depends(YourModel)` when the provided model is only known in runtime.

This example uses `POST` with `application/x-www-form-urlencoded`. The merge behaves the same on other methods if the client sends a form body. See [Which HTTP methods?](index.md#which-http-methods).

## Models { #models }

{* ../../docs_src/body_depends_model_merge_form/tutorial001_an_py310.py ln[10:19] hl[10:19] *}

## The path operation { #the-path-operation }

{* ../../docs_src/body_depends_model_merge_form/tutorial001_an_py310.py ln[22:37] hl[22:37] *}

Full helper and router wiring (`/auth/session/password/` and `/auth/session/token/`):

{* ../../docs_src/body_depends_model_merge_form/tutorial001_an_py310.py ln[40:53] hl[40:53] *}

Install [`python-multipart`](https://github.com/Kludex/python-multipart) first. The [Form models](../../tutorial/request-form-models.md) tutorial has more background.

For `GET` filters in the query string with a runtime `schema`, use `Annotated[..., Query(), Depends(schema)]` — see [Query parameters](query.md).

See [overview](index.md) for context.
