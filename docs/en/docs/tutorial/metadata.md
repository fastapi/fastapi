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

## Tag description

You can also add a description for different tags used to group your path operations.

First define your tag descriptions as a list of tags. Tags are represented as dictonaries with three key/value pairs:
* **name**: The tag value
* **description**: A description of the tag in OpenAPI and the automatic API docs UIs.
* **externalDocs**: 
  * **description**: Link text
  * **url**: The URL to the external documentation

```Python hl_lines="3 4 5 6 7 8 9 10 11 12 13"
{!../../../docs_src/metadata/tutorial004.py!}
```

Then add your tag description to your app using the parameter `openapi_tag`:


```Python hl_lines="15"
{!../../../docs_src/metadata/tutorial004.py!}
```

Use the `tags` parameter with your path operations to assign them to different tags. 
Read more about tags in [Path Operation Configuration](../path-operation-configuration/#tags).

```Python hl_lines="18 23"
{!../../../docs_src/metadata/tutorial004.py!}
```

With this configuration, the automatic API docs would look like:

<img src="/img/tutorial/metadata/image02.png">

## OpenAPI URL

By default, the OpenAPI schema is served at `/openapi.json`.

But you can configure it with the parameter `openapi_url`.

For example, to set it to be served at `/api/v1/openapi.json`:

```Python hl_lines="3"
{!../../../docs_src/metadata/tutorial002.py!}
```

If you want to disable the OpenAPI schema completely you can set `openapi_url=None`.

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
