# 元数据和文档 URL

你可以在 FastAPI 应用程序中自定义多个元数据配置。

## API 元数据

你可以在设置 OpenAPI 规范和自动 API 文档 UI 中使用的以下字段：

| 参数 | 类型 | 描述 |
|------------|------|-------------|
| `title` | `str` | API 的标题。 |
| `summary` | `str` | API 的简短摘要。 <small>自 OpenAPI 3.1.0、FastAPI 0.99.0 起可用。.</small> |
| `description` | `str` | API 的简短描述。可以使用Markdown。 |
| `version` | `string` | API 的版本。这是您自己的应用程序的版本，而不是 OpenAPI 的版本。例如 `2.5.0` 。 |
| `terms_of_service` | `str` | API 服务条款的 URL。如果提供，则必须是 URL。 |
| `contact` | `dict` | 公开的 API 的联系信息。它可以包含多个字段。<details><summary><code>contact</code> 字段</summary><table><thead><tr><th>参数</th><th>Type</th><th>描述</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>联系人/组织的识别名称。</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>指向联系信息的 URL。必须采用 URL 格式。</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>联系人/组织的电子邮件地址。必须采用电子邮件地址的格式。</td></tr></tbody></table></details> |
| `license_info` | `dict` | 公开的 API 的许可证信息。它可以包含多个字段。<details><summary><code>license_info</code> 字段</summary><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>必须的</strong> (如果设置了<code>license_info</code>). 用于 API 的许可证名称。</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>一个API的<a href="https://spdx.org/licenses/" class="external-link" target="_blank">SPDX</a>许可证表达。 The <code>identifier</code> field is mutually exclusive of the <code>url</code> field. <small>自 OpenAPI 3.1.0、FastAPI 0.99.0 起可用。</small></td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>用于 API 的许可证的 URL。必须采用 URL 格式。</td></tr></tbody></table></details> |

你可以按如下方式设置它们：

{* ../../docs_src/metadata/tutorial001.py hl[4:6] *}

/// tip

您可以在 `description` 字段中编写 Markdown，它将在输出中呈现。

///

通过这样设置，自动 API 文档看起来会像：

<img src="/img/tutorial/metadata/image01.png">

## 标签元数据

### 创建标签元数据

让我们在带有标签的示例中为 `users` 和 `items` 试一下。

创建标签元数据并把它传递给 `openapi_tags` 参数：

{* ../../docs_src/metadata/tutorial004.py hl[3:16,18] *}

注意你可以在描述内使用 Markdown，例如「login」会显示为粗体（**login**）以及「fancy」会显示为斜体（_fancy_）。

/// tip | 提示

不必为你使用的所有标签都添加元数据。

///

### 使用你的标签

将 `tags` 参数和*路径操作*（以及 `APIRouter`）一起使用，将其分配给不同的标签：

{* ../../docs_src/metadata/tutorial004.py hl[21,26] *}

/// info | 信息

阅读更多关于标签的信息[路径操作配置](path-operation-configuration.md#tags){.internal-link target=_blank}。

///

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

{* ../../docs_src/metadata/tutorial002.py hl[3] *}

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

{* ../../docs_src/metadata/tutorial003.py hl[3] *}
