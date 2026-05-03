# File uploads { #file-uploads }

Multipart uploads: `File()` inside `Annotated`, plus `Depends(schema)` when `schema` includes fields such as `UploadFile`. OpenAPI then describes file parts the same way as in the regular [Request Files](../../tutorial/request-files.md) tutorial.

The sample uses `POST`, which is what browsers and most clients use for uploads. `PUT`, `PATCH`, or `DELETE` with multipart follow the same rules if the client actually sends multipart data. See [Which HTTP methods?](index.md#which-http-methods).

## Models { #models }

{* ../../docs_src/body_depends_model_merge_file/tutorial001_an_py310.py ln[10:19] hl[10:19] *}

## The path operation { #the-path-operation }

{* ../../docs_src/body_depends_model_merge_file/tutorial001_an_py310.py ln[22:41] hl[22:41] *}

Full helper and registrations for `/files/attachments/commented/` and `/files/attachments/named/`:

{* ../../docs_src/body_depends_model_merge_file/tutorial001_an_py310.py ln[44:57] hl[44:57] *}

The handler returns a small JSON payload: upload metadata plus `data` from `model_dump(exclude={"file"})` so non-file fields (`comment`, `name`, …) stay JSON-serializable.

Install [`python-multipart`](https://github.com/Kludex/python-multipart) for multipart support in your own project.

See [overview](index.md) for context.
