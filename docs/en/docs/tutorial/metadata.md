# Metadata and Docs URLs

You can customize several metadata configurations in your **FastAPI** application.

## Title, description, and version

You can set the:

* **Title**: used as your API's title/name, in OpenAPI and the automatic API docs UIs.
* **Description**: the description of your API, in OpenAPI and the automatic API docs UIs.
* **Version**: the version of your API, e.g. `v2` or `2.5.0`.
    * Useful for example if you had a previous version of the application, also using OpenAPI.

To set them, use the parameters `title`, `description`, and `version`:

```Python hl_lines="4 5 6"
{!../../../docs_src/metadata/tutorial001.py!}
```

With this configuration, the automatic API docs would look like:

<img src="/img/tutorial/metadata/image01.png">

## Tag descriptions

You can also add additional metadata for the different tags used to group your path operations with the parameter `openapi_tags`.

It takes a list containing one dictionary for each tag.

Each dictionary can contain:

* `name` (**required**): a `str` with the same tag name you use in the `tags` parameter in your *path operations* and `APIRouter`s.
* `description`: a `str` with a short description for the tag. It can have Markdown and will be shown in the docs UI.
* `externalDocs`: a `dict` describing external documentation with:
    * `description`: a `str` with a short description for the external docs.
    * `url` (**required**): a `str` with the URL for the external documentation.

### Create metadata for tags

Let's try that in an example with tags for `users` and `items`.

Create metadata for your tags and pass it to the `openapi_tags` parameter:

```Python hl_lines="3 4 5 6 7 8 9 10 11 12 13 14 15 16  18"
{!../../../docs_src/metadata/tutorial004.py!}
```

Notice that you can use Markdown inside of the descriptions, for example "login" will be shown in bold (**login**) and "fancy" will be shown in italics (_fancy_).

!!! tip
    You don't have to add metadata for all the tags that you use.

### Use your tags

Use the `tags` parameter with your *path operations* (and `APIRouter`s) to assign them to different tags:

```Python hl_lines="21  26"
{!../../../docs_src/metadata/tutorial004.py!}
```

!!! info
    Read more about tags in [Path Operation Configuration](../path-operation-configuration/#tags){.internal-link target=_blank}.

### Check the docs

Now, if you check the docs, they will show all the additional metadata:

<img src="/img/tutorial/metadata/image02.png">

### Order of tags

The order of each tag metadata dictionary also defines the order shown in the docs UI.

For example, even though `users` would go after `items` in alphabetical order, it is shown before them, because we added their metadata as the first dictionary in the list.

## OpenAPI URL

By default, the OpenAPI schema is served at `/openapi.json`.

But you can configure it with the parameter `openapi_url`.

For example, to set it to be served at `/api/v1/openapi.json`:

```Python hl_lines="3"
{!../../../docs_src/metadata/tutorial002.py!}
```

If you want to disable the OpenAPI schema completely you can set `openapi_url=None`, that will also disable the documentation user interfaces that use it.

## Docs URLs

You can configure the two documentation user interfaces included:

* **Swagger UI**: served at `/docs`.
    * You can set its URL with the parameter `docs_url`.
    * You can disable it by setting `docs_url=None`.
* ReDoc: served at `/redoc`.
    * You can set its URL with the parameter `redoc_url`.
    * You can disable it by setting `redoc_url=None`.

For example, to set Swagger UI to be served at `/documentation` and disable ReDoc:

```Python hl_lines="3"
{!../../../docs_src/metadata/tutorial003.py!}
```
