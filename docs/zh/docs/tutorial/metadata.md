# 元数据和文档 URL { #metadata-and-docs-urls }

你可以在 **FastAPI** 应用程序中自定义多个元数据配置。

## API 的元数据 { #metadata-for-api }

你可以设置以下字段，它们会用于 OpenAPI 规范以及自动 API 文档 UI：

| 参数 | 类型 | 描述 |
|------------|------|-------------|
| `title` | `str` | API 的标题。 |
| `summary` | `str` | API 的简短摘要。 <small>自 OpenAPI 3.1.0、FastAPI 0.99.0 起可用。</small> |
| `description` | `str` | API 的简短描述。可以使用 Markdown。 |
| `version` | `string` | API 的版本。这是你自己的应用程序的版本，而不是 OpenAPI 的版本。例如 `2.5.0`。 |
| `terms_of_service` | `str` | API 服务条款的 URL。如果提供，则必须是 URL。 |
| `contact` | `dict` | 公开的 API 的联系信息。它可以包含多个字段。 <details><summary><code>contact</code> 字段</summary><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>联系人/组织的识别名称。</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>指向联系信息的 URL。必须采用 URL 格式。</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>联系人/组织的电子邮件地址。必须采用电子邮件地址格式。</td></tr></tbody></table></details> |
| `license_info` | `dict` | 公开的 API 的许可证信息。它可以包含多个字段。 <details><summary><code>license_info</code> 字段</summary><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>必填</strong>（如果设置了 <code>license_info</code>）。用于 API 的许可证名称。</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>API 的 <a href="https://spdx.org/licenses/" class="external-link" target="_blank">SPDX</a> 许可证表达式。<code>identifier</code> 字段与 <code>url</code> 字段互斥。 <small>自 OpenAPI 3.1.0、FastAPI 0.99.0 起可用。</small></td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>用于 API 的许可证的 URL。必须采用 URL 格式。</td></tr></tbody></table></details> |

你可以按如下方式设置它们：

{* ../../docs_src/metadata/tutorial001_py39.py hl[3:16, 19:32] *}

/// tip

你可以在 `description` 字段中编写 Markdown，它会在输出中被渲染。

///

通过这样设置，自动 API 文档看起来会像：

<img src="/img/tutorial/metadata/image01.png">

## License identifier { #license-identifier }

自 OpenAPI 3.1.0 和 FastAPI 0.99.0 起，你也可以在 `license_info` 中使用 `identifier` 来替代 `url`。

例如：

{* ../../docs_src/metadata/tutorial001_1_py39.py hl[31] *}

## 标签的元数据 { #metadata-for-tags }

你也可以为用于通过参数 `openapi_tags` 对你的路径操作进行分组的不同标签添加额外的元数据。

它接受一个列表，其中每个标签对应一个字典。

每个字典可以包含：

* `name`（**必填**）：一个 `str`，与在你的 *路径操作* 和 `APIRouter` 中 `tags` 参数使用的标签名相同。
* `description`：一个 `str`，用于标签的简短描述。它可以包含 Markdown，并会显示在文档 UI 中。
* `externalDocs`：一个 `dict`，描述外部文档，包含：
    * `description`：一个 `str`，用于外部文档的简短描述。
    * `url`（**必填**）：一个 `str`，用于外部文档的 URL。

### 为标签创建元数据 { #create-metadata-for-tags }

让我们在带有 `users` 和 `items` 标签的示例中试一下。

为你的标签创建元数据并把它传递给 `openapi_tags` 参数：

{* ../../docs_src/metadata/tutorial004_py39.py hl[3:16,18] *}

注意你可以在描述中使用 Markdown，例如 "login" 会显示为粗体（**login**），而 "fancy" 会显示为斜体（_fancy_）。

/// tip

你不必为你使用的所有标签都添加元数据。

///

### 使用你的标签 { #use-your-tags }

将 `tags` 参数与*路径操作*（以及 `APIRouter`）一起使用，将它们分配给不同的标签：

{* ../../docs_src/metadata/tutorial004_py39.py hl[21,26] *}

/// info

阅读更多关于标签的信息：[路径操作配置](path-operation-configuration.md#tags){.internal-link target=_blank}。

///

### 查看文档 { #check-the-docs }

现在，如果你查看文档，它们会显示所有附加的元数据：

<img src="/img/tutorial/metadata/image02.png">

### 标签顺序 { #order-of-tags }

每个标签元数据字典的顺序也定义了在文档 UI 中显示的顺序。

例如，尽管按字母顺序 `users` 应该排在 `items` 之后，但它会显示在前面，因为我们将它的元数据作为列表内的第一个字典添加。

## OpenAPI URL { #openapi-url }

默认情况下，OpenAPI schema 服务于 `/openapi.json`。

但是你可以通过参数 `openapi_url` 对其进行配置。

例如，将其设置为服务于 `/api/v1/openapi.json`：

{* ../../docs_src/metadata/tutorial002_py39.py hl[3] *}

如果你想完全禁用 OpenAPI schema，可以将其设置为 `openapi_url=None`，这样也会禁用使用它的文档用户界面。

## 文档 URLs { #docs-urls }

你可以配置内置的两个文档用户界面，包括：

* **Swagger UI**：服务于 `/docs`。
    * 可以使用参数 `docs_url` 设置它的 URL。
    * 可以通过设置 `docs_url=None` 禁用它。
* **ReDoc**：服务于 `/redoc`。
    * 可以使用参数 `redoc_url` 设置它的 URL。
    * 可以通过设置 `redoc_url=None` 禁用它。

例如，设置 Swagger UI 服务于 `/documentation` 并禁用 ReDoc：

{* ../../docs_src/metadata/tutorial003_py39.py hl[3] *}
