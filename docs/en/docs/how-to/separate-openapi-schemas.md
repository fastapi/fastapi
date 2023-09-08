# Separate OpenAPI Schemas for Input and Output or Not

When using **Pydantic v2**, the generated OpenAPI is a bit more exact and **correct** than before. 😎

In fact, in some cases, it will even have **two JSON Schemas** in OpenAPI for the same Pydantic model, for input and output, depending on if they have **default values**.

Let's see how that works and how to change it if you need to do that.

## Pydantic Models for Input and Output

Let's say you have a Pydantic model with default values, like this one:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001_py310.py[ln:1-7]!}

    # Code below omitted 👇
    ```

    <details>
    <summary>👀 Full file preview</summary>

    ```Python
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001_py310.py!}
    ```

    </details>

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001_py39.py[ln:1-9]!}

    # Code below omitted 👇
    ```

    <details>
    <summary>👀 Full file preview</summary>

    ```Python
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001_py39.py!}
    ```

    </details>

=== "Python 3.7+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001.py[ln:1-9]!}

    # Code below omitted 👇
    ```

    <details>
    <summary>👀 Full file preview</summary>

    ```Python
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001.py!}
    ```

    </details>

### Model for Input

If you use this model as an input like here:

=== "Python 3.10+"

    ```Python hl_lines="14"
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001_py310.py[ln:1-15]!}

    # Code below omitted 👇
    ```

    <details>
    <summary>👀 Full file preview</summary>

    ```Python
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001_py310.py!}
    ```

    </details>

=== "Python 3.9+"

    ```Python hl_lines="16"
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001_py39.py[ln:1-17]!}

    # Code below omitted 👇
    ```

    <details>
    <summary>👀 Full file preview</summary>

    ```Python
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001_py39.py!}
    ```

    </details>

=== "Python 3.7+"

    ```Python hl_lines="16"
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001.py[ln:1-17]!}

    # Code below omitted 👇
    ```

    <details>
    <summary>👀 Full file preview</summary>

    ```Python
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001.py!}
    ```

    </details>

...then the `description` field will **not be required**. Because it has a default value of `None`.

### Input Model in Docs

You can confirm that in the docs, the `description` field doesn't have a **red asterisk**, it's not marked as required:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image01.png">
</div>

### Model for Output

But if you use the same model as an output, like here:

=== "Python 3.10+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="21"
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001_py39.py!}
    ```

=== "Python 3.7+"

    ```Python hl_lines="21"
    {!> ../../../docs_src/separate_openapi_schemas/tutorial001.py!}
    ```

...then because `description` has a default value, if you **don't return anything** for that field, it will still have that **default value**.

### Model for Output Response Data

If you interact with the docs and check the response, even though the code didn't add anything in one of the `description` fields, the JSON response contains the default value (`null`):

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image02.png">
</div>

This means that it will **always have a value**, it's just that sometimes the value could be `None` (or `null` in JSON).

That means that, clients using your API don't have to check if the value exists or not, they can **assume the field will always be there**, but just that in some cases it will have the default value of `None`.

The way to describe this in OpenAPI, is to mark that field as **required**, because it will always be there.

Because of that, the JSON Schema for a model can be different depending on if it's used for **input or output**:

* for **input** the `description` will **not be required**
* for **output** it will be **required** (and possibly `None`, or in JSON terms, `null`)

### Model for Output in Docs

You can check the output model in the docs too, **both** `name` and `description` are marked as **required** with a **red asterisk**:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image03.png">
</div>

### Model for Input and Output in Docs

And if you check all the available Schemas (JSON Schemas) in OpenAPI, you will see that there are two, one `Item-Input` and one `Item-Output`.

For `Item-Input`, `description` is **not required**, it doesn't have a red asterisk.

But for `Item-Output`, `description` is **required**, it has a red asterisk.

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image04.png">
</div>

With this feature from **Pydantic v2**, your API documentation is more **precise**, and if you have autogenerated clients and SDKs, they will be more precise too, with a better **developer experience** and consistency. 🎉

## Do not Separate Schemas

Now, there are some cases where you might want to have the **same schema for input and output**.

Probably the main use case for this is if you already have some autogenerated client code/SDKs and you don't want to update all the autogenerated client code/SDKs yet, you probably will want to do it at some point, but maybe not right now.

In that case, you can disable this feature in **FastAPI**, with the parameter `separate_input_output_schemas=False`.

!!! info
    Support for `separate_input_output_schemas` was added in FastAPI `0.102.0`. 🤓

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/separate_openapi_schemas/tutorial002_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="12"
    {!> ../../../docs_src/separate_openapi_schemas/tutorial002_py39.py!}
    ```

=== "Python 3.7+"

    ```Python hl_lines="12"
    {!> ../../../docs_src/separate_openapi_schemas/tutorial002.py!}
    ```

### Same Schema for Input and Output Models in Docs

And now there will be one single schema for input and output for the model, only `Item`, and it will have `description` as **not required**:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image05.png">
</div>

This is the same behavior as in Pydantic v1. 🤓
