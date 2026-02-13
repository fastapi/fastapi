# 自托管自定义文档 UI 静态资源 { #custom-docs-ui-static-assets-self-hosting }

API 文档使用 Swagger UI 和 ReDoc，它们各自需要一些 JavaScript 和 CSS 文件。

默认情况下，这些文件从一个 <abbr title="Content Delivery Network - 内容分发网络: 一种服务，通常由多台服务器组成，用于提供静态文件，如 JavaScript 和 CSS。它常用于从更接近客户端的服务器提供这些文件，从而提升性能。">CDN</abbr> 提供。

不过你可以自定义：可以指定特定的 CDN，或自行提供这些文件。

## 为 JavaScript 和 CSS 自定义 CDN { #custom-cdn-for-javascript-and-css }

假设你想使用不同的 <abbr title="Content Delivery Network - 内容分发网络">CDN</abbr>，例如使用 `https://unpkg.com/`。

如果你所在的国家/地区屏蔽了某些 URL，这会很有用。

### 关闭自动文档 { #disable-the-automatic-docs }

第一步是关闭自动文档，因为默认它们会使用默认的 CDN。

要关闭它们，在创建 `FastAPI` 应用时将其 URL 设为 `None`：

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[8] *}

### 包含自定义文档 { #include-the-custom-docs }

现在你可以为自定义文档创建*路径操作*。

你可以复用 FastAPI 的内部函数来创建文档的 HTML 页面，并传入所需参数：

- `openapi_url`：文档 HTML 页面获取你的 API 的 OpenAPI 模式的 URL。这里可以使用 `app.openapi_url` 属性。
- `title`：你的 API 标题。
- `oauth2_redirect_url`：这里可以使用 `app.swagger_ui_oauth2_redirect_url` 来使用默认值。
- `swagger_js_url`：你的 Swagger UI 文档 HTML 获取**JavaScript** 文件的 URL。这里是自定义的 CDN URL。
- `swagger_css_url`：你的 Swagger UI 文档 HTML 获取**CSS** 文件的 URL。这里是自定义的 CDN URL。

ReDoc 也类似...

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[2:6,11:19,22:24,27:33] *}

/// tip | 提示

`swagger_ui_redirect` 的*路径操作*是在你使用 OAuth2 时的一个辅助。

如果你把 API 与某个 OAuth2 提供方集成，你就可以完成认证并带着获取到的凭据回到 API 文档里。然后使用真实的 OAuth2 认证与之交互。

Swagger UI 会在幕后为你处理这些，但它需要这个“重定向”辅助路径。

///

### 创建一个路径操作进行测试 { #create-a-path-operation-to-test-it }

现在，为了测试一切是否正常，创建一个*路径操作*：

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[36:38] *}

### 测试 { #test-it }

现在，你应该可以访问 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>，并刷新页面，页面会从新的 CDN 加载这些资源。

## 为文档自托管 JavaScript 和 CSS { #self-hosting-javascript-and-css-for-docs }

如果你需要在离线、无法访问互联网或仅在局域网内时，应用仍能工作，那么自托管 JavaScript 和 CSS 会很有用。

这里你将看到如何在同一个 FastAPI 应用中自行提供这些文件，并配置文档使用它们。

### 项目文件结构 { #project-file-structure }

假设你的项目文件结构如下：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

现在创建一个目录来存放这些静态文件。

你的新文件结构可能如下：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### 下载文件 { #download-the-files }

下载文档需要的静态文件，并将它们放到 `static/` 目录中。

你通常可以右键点击每个链接，选择类似“将链接另存为...”的选项。

Swagger UI 使用以下文件：

- <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js" class="external-link" target="_blank">`swagger-ui-bundle.js`</a>
- <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" class="external-link" target="_blank">`swagger-ui.css`</a>

而 ReDoc 使用以下文件：

- <a href="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js" class="external-link" target="_blank">`redoc.standalone.js`</a>

之后，你的文件结构可能如下：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static
    ├── redoc.standalone.js
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
```

### 提供静态文件 { #serve-the-static-files }

- 导入 `StaticFiles`。
- 在特定路径上“挂载”一个 `StaticFiles()` 实例。

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[7,11] *}

### 测试静态文件 { #test-the-static-files }

启动你的应用，并访问 <a href="http://127.0.0.1:8000/static/redoc.standalone.js" class="external-link" target="_blank">http://127.0.0.1:8000/static/redoc.standalone.js</a>。

你应该会看到一个非常长的 **ReDoc** 的 JavaScript 文件。

它可能以如下内容开头：

```JavaScript
/*! For license information please see redoc.standalone.js.LICENSE.txt */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t(require("null")):
...
```

这就确认了你的应用能够提供静态文件，并且你把文档所需的静态文件放在了正确的位置。

现在我们可以配置应用，让文档使用这些静态文件。

### 为静态文件关闭自动文档 { #disable-the-automatic-docs-for-static-files }

和使用自定义 CDN 一样，第一步是关闭自动文档，因为默认情况下它们会使用 CDN。

要关闭它们，在创建 `FastAPI` 应用时将其 URL 设为 `None`：

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[9] *}

### 为静态文件包含自定义文档 { #include-the-custom-docs-for-static-files }

同样地，现在你可以为自定义文档创建*路径操作*。

你可以再次复用 FastAPI 的内部函数来创建文档的 HTML 页面，并传入所需参数：

- `openapi_url`：文档 HTML 页面获取你的 API 的 OpenAPI 模式的 URL。这里可以使用 `app.openapi_url` 属性。
- `title`：你的 API 标题。
- `oauth2_redirect_url`：这里可以使用 `app.swagger_ui_oauth2_redirect_url` 来使用默认值。
- `swagger_js_url`：你的 Swagger UI 文档 HTML 获取**JavaScript** 文件的 URL。**这是现在由你的应用自己提供的那个**。
- `swagger_css_url`：你的 Swagger UI 文档 HTML 获取**CSS** 文件的 URL。**这是现在由你的应用自己提供的那个**。

ReDoc 也类似...

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[2:6,14:22,25:27,30:36] *}

/// tip | 提示

`swagger_ui_redirect` 的*路径操作*是在你使用 OAuth2 时的一个辅助。

如果你把 API 与某个 OAuth2 提供方集成，你就可以完成认证并带着获取到的凭据回到 API 文档里。然后使用真实的 OAuth2 认证与之交互。

Swagger UI 会在幕后为你处理这些，但它需要这个“重定向”辅助路径。

///

### 创建一个路径操作测试静态文件 { #create-a-path-operation-to-test-static-files }

现在，为了测试一切是否正常，创建一个*路径操作*：

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[39:41] *}

### 测试静态文件 UI { #test-static-files-ui }

现在，你可以断开 WiFi，访问 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>，并刷新页面。

即使没有互联网，你也能看到 API 的文档并与之交互。
