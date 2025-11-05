# Templates { #templates }

You can use any template engine you want with **FastAPI**.

A common choice is Jinja2, the same one used by Flask and other tools.

There are utilities to configure it easily that you can use directly in your **FastAPI** application (provided by Starlette).

## Install dependencies { #install-dependencies }

Make sure you create a [virtual environment](../virtual-environments.md){.internal-link target=_blank}, activate it, and install `jinja2`:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## Using `Jinja2Templates` { #using-jinja2templates }

* Import `Jinja2Templates`.
* Create a `templates` object that you can reuse later.
* Declare a `Request` parameter in the *path operation* that will return a template.
* Use the `templates` you created to render and return a `TemplateResponse`, pass the name of the template, the request object, and a "context" dictionary with key-value pairs to be used inside of the Jinja2 template.

{* ../../docs_src/templates/tutorial001.py hl[4,11,15:18] *}

/// note

Before FastAPI 0.108.0, Starlette 0.29.0, the `name` was the first parameter.

Also, before that, in previous versions, the `request` object was passed as part of the key-value pairs in the context for Jinja2.

///

/// tip

By declaring `response_class=HTMLResponse` the docs UI will be able to know that the response will be HTML.

///

/// note | Technical Details

You could also use `from starlette.templating import Jinja2Templates`.

**FastAPI** provides the same `starlette.templating` as `fastapi.templating` just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with `Request` and `StaticFiles`.

///

## Writing templates { #writing-templates }

Then you can write a template at `templates/item.html` with, for example:

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### Template Context Values { #template-context-values }

In the HTML that contains:

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...it will show the `id` taken from the "context" `dict` you passed:

```Python
{"id": id}
```

For example, with an ID of `42`, this would render:

```html
Item ID: 42
```

### Template `url_for` Arguments { #template-url-for-arguments }

You can also use `url_for()` inside of the template, it takes as arguments the same arguments that would be used by your *path operation function*.

So, the section with:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...will generate a link to the same URL that would be handled by the *path operation function* `read_item(id=id)`.

For example, with an ID of `42`, this would render:

```html
<a href="/items/42">
```

## Templates and static files { #templates-and-static-files }

You can also use `url_for()` inside of the template, and use it, for example, with the `StaticFiles` you mounted with the `name="static"`.

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

In this example, it would link to a CSS file at `static/styles.css` with:

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

And because you are using `StaticFiles`, that CSS file would be served automatically by your **FastAPI** application at the URL `/static/styles.css`.

## More details { #more-details }

For more details, including how to test templates, check <a href="https://www.starlette.dev/templates/" class="external-link" target="_blank">Starlette's docs on templates</a>.
