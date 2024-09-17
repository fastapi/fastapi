# Cookie Parameter Models

If you have a group of **cookies** that are related, you can create a **Pydantic model** to declare them. 🍪

This would allow you to **re-use the model** in **multiple places** and also to declare validations and metadata for all the parameters at once. 😎

/// note

This is supported since FastAPI version `0.115.0`. 🤓

///

/// tip

This same technique applies to `Query`, `Cookie`, and `Header`. 😎

///

## Cookies with a Pydantic Model

Declare the **cookie** parameters that you need in a **Pydantic model**, and then declare the parameter as `Cookie`:

//// tab | Python 3.10+

```Python hl_lines="9-12  16"
{!> ../../../docs_src/cookie_param_models/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9-12  16"
{!> ../../../docs_src/cookie_param_models/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10-13  17"
{!> ../../../docs_src/cookie_param_models/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="7-10  14"
{!> ../../../docs_src/cookie_param_models/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="9-12  16"
{!> ../../../docs_src/cookie_param_models/tutorial001.py!}
```

////

**FastAPI** will **extract** the data for **each field** from the **cookies** received in the request and give you the Pydantic model you defined.

## Check the Docs

You can see the defined cookies in the docs UI at `/docs`:

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// info

Have in mind that, as **browsers handle cookies** in special ways and behind the scenes, they **don't** easily allow **JavaScript** to touch them.

If you go to the **API docs UI** at `/docs` you will be able to see the **documentation** for cookies for your *path operations*.

But even if you **fill the data** and click "Execute", because the docs UI works with **JavaScript**, the cookies won't be sent, and you will see an **error** message as if you didn't write any values.

///

## Forbid Extra Cookies

In some special use cases (probably not very common), you might want to **restrict** the cookies that you want to receive.

Your API now has the power to control its own <abbr title="This is a joke, just in case. It has nothing to do with cookie consents, but it's funny that even the API can now reject the poor cookies. Have a cookie. 🍪">cookie consent</abbr>. 🤪🍪

You can use Pydantic's model configuration to `forbid` any `extra` fields:

//// tab | Python 3.9+

```Python hl_lines="10"
{!> ../../../docs_src/cookie_param_models/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11"
{!> ../../../docs_src/cookie_param_models/tutorial002_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="10"
{!> ../../../docs_src/cookie_param_models/tutorial002.py!}
```

////

If a client tries to send some **extra cookies**, they will receive an **error** response.

Poor cookie banners with all their effort to get your consent for the <abbr title="This is another joke. Don't pay attention to me. Have some coffee for your cookie. ☕">API to reject it</abbr>. 🍪

For example, if the client tries to send a `santa_tracker` cookie with a value of `good-list-please`, the client will receive an **error** response telling them that the `santa_tracker` <abbr title="Santa disapproves the lack of cookies. 🎅 Okay, no more cookie jokes.">cookie is not allowed</abbr>:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
```

## Summary

You can use **Pydantic models** to declare <abbr title="Have a last cookie before you go. 🍪">**cookies**</abbr> in **FastAPI**. 😎
