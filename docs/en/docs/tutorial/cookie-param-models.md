# Cookie Parameter Models { #cookie-parameter-models }

If you have a group of **cookies** that are related, you can create a **Pydantic model** to declare them. 🍪

This would allow you to **re-use the model** in **multiple places** and also to declare validations and metadata for all the parameters at once. 😎

/// note

This is supported since FastAPI version `0.115.0`. 🤓

///

/// tip

This same technique applies to `Query`, `Cookie`, and `Header`. 😎

///

## Cookies with a Pydantic Model { #cookies-with-a-pydantic-model }

Declare the **cookie** parameters that you need in a **Pydantic model**, and then declare the parameter as `Cookie`:

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI** will **extract** the data for **each field** from the **cookies** received in the request and give you the Pydantic model you defined.

## Check the Docs { #check-the-docs }

You can see the defined cookies in the docs UI at `/docs`:

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// note

Have in mind that, as **browsers handle cookies** in special ways and behind the scenes, they **don't** easily allow **JavaScript** to touch them.

If you go to the **API docs UI** at `/docs` you will be able to see the **documentation** for cookies for your *path operations*.

But even if you **fill the data** and click "Execute", because the docs UI works with **JavaScript**, the cookies won't be sent, and you will see an **error** message as if you didn't write any values.

///

## Forbid Extra Cookies { #forbid-extra-cookies }

In some special use cases (probably not very common), you might want to **restrict** the cookies that you want to receive.

Your API now has the power to control its own <dfn title="This is a joke, just in case. It has nothing to do with cookie consents, but it's funny that even the API can now reject the poor cookies. Have a cookie. 🍪">cookie consent</dfn>. 🤪🍪

You can use Pydantic's model configuration to `forbid` any `extra` fields:

{* ../../docs_src/cookie_param_models/tutorial002_an_py310.py hl[10] *}

If a client tries to send some **extra cookies**, they will receive an **error** response.

Poor cookie banners with all their effort to get your consent for the <dfn title="This is another joke. Don't pay attention to me. Have some coffee for your cookie. ☕">API to reject it</dfn>. 🍪

For example, if the client tries to send a `santa_tracker` cookie with a value of `good-list-please`, the client will receive an **error** response telling them that the `santa_tracker` <dfn title="Santa disapproves the lack of cookies. 🎅 Okay, no more cookie jokes.">cookie is not allowed</dfn>:

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

## Combine Parameter Models { #combine-parameter-models }

You can combine multiple cookie parameter models with individual cookie parameters and dependencies. Each model is extracted and validated independently, as explained for [query parameter models](query-param-models.md#combine-parameter-models).

Each model's `extra` configuration applies to all cookie parameters, including those declared in other models or dependencies. With `extra="forbid"`, any cookie outside that model is rejected. With `extra="allow"`, those cookies are included as model extras.

## Optional Cookie Parameter Models { #optional-cookie-parameter-models }

Declare a cookie parameter model with `| None` and a default of `None` to make the group optional.

{* ../../docs_src/cookie_param_models/tutorial003_an_py310.py hl[15] *}

If neither `theme` nor `locale` is sent, `preferences` is `None`. If either is sent, FastAPI validates the model and requires both fields.

The same rules for defaults, extra fields, and OpenAPI apply as for [optional query parameter models](query-param-models.md#optional-query-parameter-models).

## Summary { #summary }

You can use **Pydantic models** to declare <dfn title="Have a last cookie before you go. 🍪">**cookies**</dfn> in **FastAPI**. 😎
