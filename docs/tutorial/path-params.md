You can declare path "parameters" or "variables" with the same syntax used by Python format strings:

```Python hl_lines="6 7"
{!./tutorial/src/path_params/tutorial001.py!}
```

The value of the path parameter `item_id` will be passed to your function as the argument `item_id`.

So, if you run this example and go to <a href="http://127.0.0.1:8000/items/foo" target="_blank">http://127.0.0.1:8000/items/foo</a>, you will see a response of:

```JSON
{"item_id":"foo"}
```

## Path parameters with types

You can declare the type of a path parameter in the function, using standard Python type annotations:

```Python hl_lines="7"
{!./tutorial/src/path_params/tutorial002.py!}
```

In this case, `item_id` is declared to be an `int`.

!!! check
    This will give you editor support inside of your function, with error checks, completion, etc.

## Data "parsing"

If you run this example and open your browser at <a href="http://127.0.0.1:8000/items/3" target="_blank">http://127.0.0.1:8000/items/3</a>, you will see a response of:

```JSON
{"item_id":3}
```

!!! check
    Notice that the value your function received (and returned) is `3`, as a Python `int`, not a string `"3"`.
    
    So, with that type declaration, **FastAPI** gives you automatic request <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>.

## Data validation

But if you go to the browser at <a href="http://127.0.0.1:8000/items/foo" target="_blank">http://127.0.0.1:8000/items/foo</a>, you will see a nice HTTP error of:

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

because the path parameter `item_id` had a value of `"foo"`, which is not an `int`.

The same error would appear if you provided a `float` instead of an int, as in: <a href="http://127.0.0.1:8000/items/4.2" target="_blank">http://127.0.0.1:8000/items/4.2</a>


!!! check
    So, with the same Python type declaration, **FastAPI** gives you data validation.

    Notice that the error also clearly states exactly the point where the validation didn't pass. 
    
    This is incredibly helpful while developing and debugging code that interacts with your API.

## Documentation

And when you open your browser at <a href="http://127.0.0.1:8000/docs" target="_blank">http://127.0.0.1:8000/docs</a>, you will see an automatic, interactive, API documentation like:

<img src="/img/tutorial/path-params/image01.png">

!!! check
    Again, just with that same Python type declaration, **FastAPI** gives you automatic, interactive documentation (integrating Swagger UI).

    Notice that the path parameter is declared to be an integer.

## Standards-based benefits, alternative documentation

And because the generated schema is from the <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md" target="_blank">OpenAPI</a> standard, there are many compatible tools.

Because of this, **FastAPI** itself provides an alternative API documentation (using ReDoc):

<img src="/img/tutorial/path-params/image02.png">

The same way, there are many compatible tools. Including code generation tools for many languages.

## Pydantic

All the data validation is performed under the hood by <a href="https://pydantic-docs.helpmanual.io/" target="_blank">Pydantic</a>, so you get all the benefits from it. And you know you are in good hands.

You can use the same type declarations with `str`, `float`, `bool` and many other complex data types.

These are explored in the next chapters of the tutorial.

## Recap

With **FastAPI**, by using short, intuitive and standard Python type declarations, you get:

* Editor support: error checks, autocompletion, etc.
* Data "<abbr title="converting the string that comes from an HTTP request into Python data">parsing</abbr>"
* Data validation
* API annotation and automatic documentation

And you only have to declare them once.

That's probably the main visible advantage of **FastAPI** compared to alternative frameworks (apart from the raw performance).