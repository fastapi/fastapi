# 元数据和文档 URL

你可以在 **FastAPI** 应用中自定义几个元数据配置。

## 标题、描述和版本

你可以设定：

* **Title**：在 OpenAPI 和自动 API 文档用户界面中作为 API 的标题/名称使用。
* **Description**：在 OpenAPI 和自动 API 文档用户界面中用作 API 的描述。
* **Version**：API 版本，例如 `v2` 或者 `2.5.0`。
    * 如果你之前的应用程序版本也使用 OpenAPI 会很有用。

使用 `title`、`description` 和 `version` 来设置它们：

```Python hl_lines="4-6"
{!../../../docs_src/metadata/tutorial001.py!}
```

通过这样设置，自动 API 文档看起来会像：

<img src="/img/tutorial/metadata/image01.png">

## 标签元数据

你也可以使用参数 `openapi_tags`，为用于分组路径操作的不同标签添加额外的元数据。

它接受一个列表，这个列表包含每个标签对应的一个字典。

每个字典可以包含：

* `name`（**必要**）：一个 `str`，它与*路径操作*和 `APIRouter` 中使用的 `tags` 参数有相同的标签名。
* `description`：一个用于简短描述标签的 `str`。它支持 Markdown 并且会在文档用户界面中显示。
* `externalDocs`：一个描述外部文档的 `dict`：
    * `description`：用于简短描述外部文档的 `str`。
    * `url`（**必要**）：外部文档的 URL `str`。

### 创建标签元数据

让我们在带有标签的示例中为 `users` 和 `items` 试一下。

创建标签元数据并把它传递给 `openapi_tags` 参数：

```Python hl_lines="3-16  18"
{!../../../docs_src/metadata/tutorial004.py!}
```

注意你可以在描述内使用 Markdown，例如「login」会显示为粗体（**login**）以及「fancy」会显示为斜体（_fancy_）。

!!! 提示
    不必为你使用的所有标签都添加元数据。

### 使用你的标签

将 `tags` 参数和*路径操作*（以及 `APIRouter`）一起使用，将其分配给不同的标签：

```Python hl_lines="21  26"
{!../../../docs_src/metadata/tutorial004.py!}
```

!!! 信息
    阅读更多关于标签的信息[路径操作配置](../path-operation-configuration/#tags){.internal-link target=_blank}。

### 查看文档

如果你现在查看文档，它们会显示所有附加的元数据：

<img src="/img/tutorial/metadata/image02.png">

### 标签顺序

每个标签元数据字典的顺序也定义了在文档用户界面显示的顺序。

例如按照字母顺序，即使 `users` 排在 `items` 之后，它也会显示在前面，因为我们将它的元数据添加为列表内的第一个字典。

## OpenAPI URL

默认情况下，OpenAPI 模式服务于 `/openapi.json`。

但是你可以通过参数 `openapi_url` 对其进行配置。

例如，将其设置为服务于 `/api/v1/openapi.json`：

```Python hl_lines="3"
{!../../../docs_src/metadata/tutorial002.py!}
```

如果你想完全禁用 OpenAPI 模式，可以将其设置为 `openapi_url=None`，这样也会禁用使用它的文档用户界面。

## 文档 URLs

你可以配置两个文档用户界面，包括：

* **Swagger UI**：服务于 `/docs`。
    * 可以使用参数 `docs_url` 设置它的 URL。
    * 可以通过设置 `docs_url=None` 禁用它。
* ReDoc：服务于 `/redoc`。
    * 可以使用参数 `redoc_url` 设置它的 URL。
    * 可以通过设置 `redoc_url=None` 禁用它。

例如，设置 Swagger UI 服务于 `/documentation` 并禁用 ReDoc：

```Python hl_lines="3"
{!../../../docs_src/metadata/tutorial003.py!}
```
