# 扩展 OpenAPI

!!! warning "警告"

    本章介绍的功能较难，您可以跳过阅读。

    如果您刚开始学习**用户指南**，最好跳过本章。

    如果您确定要修改 OpenAPI 概图，请继续阅读。

某些情况下，我们需要修改 OpenAPI 概图。

本章介绍如何修改 OpenAPI 概图。

## 常规流程

常规（默认）流程如下。

`FastAPI` 应用（实例）提供了返回 OpenAPI 概图的 `.openapi()` 方法。

作为应用对象创建的组成部分，要注册 `/openapi.json` （或其它为 `openapi_url` 设置的任意内容）*路径操作*。

它只返回包含应用的 `.openapi()` 方法操作结果的 JSON 响应。

但默认情况下，`.openapi()` 只是检查 `.openapi_schema` 属性是否包含内容，并返回其中的内容。

如果 `.openapi_schema` 属性没有内容，该方法就使用 `fastapi.openapi.utils.get_openapi` 工具函数生成内容。

`get_openapi()` 函数接收如下参数：

* `title`：文档中显示的 OpenAPI 标题
* `version`：API 的版本号，例如 `2.5.0`
* `openapi_version`： OpenAPI 规范的版本号，默认为最新版： `3.0.2`
* `description`：API 的描述说明
* `routes`：路由列表，每个路由都是注册的*路径操作*。这些路由是从 `app.routes` 中提取的。

## 覆盖默认值

`get_openapi()` 工具函数还可以用于生成 OpenAPI 概图，并利用上述信息参数覆盖指定的内容。

例如，使用 <a href="https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo" class="external-link" target="_blank">ReDoc 的 OpenAPI 扩展添加自定义 Logo</a>。

### 常规 **FastAPI**

首先，编写常规 **FastAPI** 应用：

```Python hl_lines="1  4  7-9"
{!../../../docs_src/extending_openapi/tutorial001.py!}
```

### 生成 OpenAPI 概图

然后，在 `custom_openapi()` 函数里使用 `get_openapi()` 工具函数生成 OpenAPI 概图：

```Python hl_lines="2  15-20"
{!../../../docs_src/extending_openapi/tutorial001.py!}
```

### 修改 OpenAPI 概图

添加 ReDoc 扩展信息，为 OpenAPI 概图里的  `info` **对象**添加自定义 `x-logo`：

```Python hl_lines="21-23"
{!../../../docs_src/extending_openapi/tutorial001.py!}
```

### 缓存 OpenAPI 概图

把 `.openapi_schema` 属性当作**缓存**，存储生成的概图。

通过这种方式，**FastAPI** 应用不必在用户每次打开 API 文档时反复生成概图。

只需生成一次，下次请求时就可以使用缓存的概图。

```Python hl_lines="13-14  24-25"
{!../../../docs_src/extending_openapi/tutorial001.py!}
```

### 覆盖方法

用新函数替换 `.openapi()` 方法。

```Python hl_lines="28"
{!../../../docs_src/extending_openapi/tutorial001.py!}
```

### 查看文档

打开 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc，查看</a>自定义 Logo（本例中是 **FastAPI** 的 Logo）：

<img src="/img/tutorial/extending-openapi/image01.png">

## 文档 JavaScript 与 CSS 自托管

FastAPI 支持 **Swagger UI** 和 **ReDoc** 两种 API 文档，这两种文档都需要调用 JavaScript 与 CSS 文件。

这些文件默认由 <abbr title="Content Delivery Network（内容分发网络）: 由多台服务器为 JavaScript 和 CSS 等静态文件支持的服务。一般来说，从靠近客户端的服务器提供静态文件服务可以提高性能。">CDN</abbr> 提供支持服务。

但也可以自定义设置指定的 CDN 或自行提供文件服务。

这种做法很常用，例如，在没有联网或本地局域网时也能让应用在离线状态下正常运行。

本文介绍如何为 FastAPI 应用提供文件自托管服务，并设置文档使用这些文件。

### 项目文件架构

假设项目文件架构如下：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

接下来，创建存储静态文件的文件夹。

新的文件架构如下：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### 下载文件

下载文档所需的静态文件，把文件放到 `static/` 文件夹里。

右键点击链接，选择**另存为...**。

**Swagger UI** 使用如下文件：

* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js" class="external-link" target="_blank">`swagger-ui-bundle.js`</a>
* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css" class="external-link" target="_blank">`swagger-ui.css`</a>

**ReDoc** 使用如下文件：

* <a href="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js" class="external-link" target="_blank">`redoc.standalone.js`</a>

保存好后，文件架构所示如下：

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

### 安装 `aiofiles`

现在，安装 `aiofiles`：


<div class="termy">

```console
$ pip install aiofiles

---> 100%
```

</div>

### 静态文件服务

* 导入 `StaticFiles`
* 在指定路径下**挂载** `StaticFiles()` 实例

```Python hl_lines="7  11"
{!../../../docs_src/extending_openapi/tutorial002.py!}
```

### 测试静态文件

启动应用，打开 <a href="http://127.0.0.1:8000/static/redoc.standalone.js" class="external-link" target="_blank">http://127.0.0.1:8000/static/redoc.standalone.js。</a>

就能看到 **ReDoc** 的 JavaScript 文件。

该文件开头如下：

```JavaScript
/*!
 * ReDoc - OpenAPI/Swagger-generated API Reference Documentation
 * -------------------------------------------------------------
 *   Version: "2.0.0-rc.18"
 *   Repo: https://github.com/Redocly/redoc
 */
!function(e,t){"object"==typeof exports&&"object"==typeof m

...
```

能打开这个文件就表示 FastAPI 应用能提供静态文件服务，并且文档要调用的静态文件放到了正确的位置。

接下来，使用静态文件配置文档。

### 禁用 API 文档

第一步是禁用 API 文档，就是使用 CDN 的默认文档。

创建 `FastAPI` 应用时把文档的 URL 设置为 `None` 即可禁用默认文档：

```Python hl_lines="9"
{!../../../docs_src/extending_openapi/tutorial002.py!}
```

### 添加自定义文档

现在，创建自定义文档的*路径操作*。

导入 FastAPI 内部函数为文档创建 HTML 页面，并把所需参数传递给这些函数：

* `openapi_url`： API 文档获取 OpenAPI 概图的 HTML 页面，此处可使用 `app.openapi_url`
* `title`：API 的标题
* `oauth2_redirect_url`：此处使用 `app.swagger_ui_oauth2_redirect_url` 作为默认值
* `swagger_js_url`：Swagger UI 文档所需 **JavaScript** 文件的 URL，即为应用提供服务的文件
* `swagger_css_url`：Swagger UI 文档所需 **CSS** 文件的 URL，即为应用提供服务的文件

添加 ReDoc 文档的方式与此类似……

```Python hl_lines="2-6  14-22  25-27  30-36"
{!../../../docs_src/extending_openapi/tutorial002.py!}
```

!!! tip "提示"

    `swagger_ui_redirect` 的*路径操作*是 OAuth2 的辅助函数。

    集成 API 与 OAuth2 第三方应用时，您能进行身份验证，使用请求凭证返回 API 文档，并使用真正的 OAuth2 身份验证与 API 文档进行交互操作。

    Swagger UI 在后台进行处理，但它需要这个**重定向**辅助函数。

### 创建测试*路径操作*

现在，测试各项功能是否能顺利运行。创建*路径操作*：

```Python hl_lines="39-41"
{!../../../docs_src/extending_openapi/tutorial002.py!}
```

### 测试文档

断开 WiFi 连接，打开 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs，刷新页面。</a>

现在，就算没有联网也能查看并操作 API 文档。
