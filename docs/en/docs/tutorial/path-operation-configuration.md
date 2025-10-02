# Path Operation Configuration { #path-operation-configuration }

There are several parameters that you can pass to your *path operation decorator* to configure it.

/// warning

Notice that these parameters are passed directly to the *path operation decorator*, not to your *path operation function*.

///

## Response Status Code { #response-status-code }

You can define the (HTTP) `status_code` to be used in the response of your *path operation*.

You can pass directly the `int` code, like `404`.

But if you don't remember what each number code is for, you can use the shortcut constants in `status`:

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

That status code will be used in the response and will be added to the OpenAPI schema.

/// note | Technical Details

You could also use `from starlette import status`.

**FastAPI** provides the same `starlette.status` as `fastapi.status` just as a convenience for you, the developer. But it comes directly from Starlette.

///

## Tags { #tags }

You can add tags to your *path operation*, pass the parameter `tags` with a `list` of `str` (commonly just one `str`):

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

They will be added to the OpenAPI schema and used by the automatic documentation interfaces:

<img src="/img/tutorial/path-operation-configuration/image01.png">

### Tags with Enums { #tags-with-enums }

If you have a big application, you might end up accumulating **several tags**, and you would want to make sure you always use the **same tag** for related *path operations*.

In these cases, it could make sense to store the tags in an `Enum`.

**FastAPI** supports that the same way as with plain strings:

{* ../../docs_src/path_operation_configuration/tutorial002b.py hl[1,8:10,13,18] *}

## Summary and description { #summary-and-description }

You can add a `summary` and `description`:

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[18:19] *}

## Description from docstring { #description-from-docstring }

As descriptions tend to be long and cover multiple lines, you can declare the *path operation* description in the function <abbr title="a multi-line string as the first expression inside a function (not assigned to any variable) used for documentation">docstring</abbr> and **FastAPI** will read it from there.

You can write <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a> in the docstring, it will be interpreted and displayed correctly (taking into account docstring indentation).

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

It will be used in the interactive docs:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## Response description { #response-description }

You can specify the response description with the parameter `response_description`:

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[19] *}

/// info

Notice that `response_description` refers specifically to the response, the `description` refers to the *path operation* in general.

///

/// check

OpenAPI specifies that each *path operation* requires a response description.

So, if you don't provide one, **FastAPI** will automatically generate one of "Successful response".

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## Deprecate a *path operation* { #deprecate-a-path-operation }

If you need to mark a *path operation* as <abbr title="obsolete, recommended not to use it">deprecated</abbr>, but without removing it, pass the parameter `deprecated`:

{* ../../docs_src/path_operation_configuration/tutorial006.py hl[16] *}

It will be clearly marked as deprecated in the interactive docs:

<img src="/img/tutorial/path-operation-configuration/image04.png">

Check how deprecated and non-deprecated *path operations* look like:

<img src="/img/tutorial/path-operation-configuration/image05.png">

## Recap { #recap }

You can configure and add metadata for your *path operations* easily by passing parameters to the *path operation decorators*.
