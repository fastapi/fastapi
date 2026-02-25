# 扩展 OpenAPI { #extending-openapi }

在某些情况下，你可能需要修改生成的 OpenAPI 架构（schema）。

本节将介绍如何实现。

## 常规流程 { #the-normal-process }

常规（默认）流程如下。

`FastAPI` 应用（实例）有一个 `.openapi()` 方法，预期返回 OpenAPI 架构。

在创建应用对象时，会注册一个用于 `/openapi.json`（或你在 `openapi_url` 中设置的路径）的路径操作。

它只会返回一个 JSON 响应，内容是应用 `.openapi()` 方法的结果。

默认情况下，`.openapi()` 方法会检查属性 `.openapi_schema` 是否已有内容，若有则直接返回。

如果没有，则使用 `fastapi.openapi.utils.get_openapi` 工具函数生成。

该 `get_openapi()` 函数接收以下参数：

- `title`：OpenAPI 标题，显示在文档中。
- `version`：你的 API 版本，例如 `2.5.0`。
- `openapi_version`：使用的 OpenAPI 规范版本。默认是最新的 `3.1.0`。
- `summary`：API 的简短摘要。
- `description`：API 的描述，可包含 Markdown，并会展示在文档中。
- `routes`：路由列表，即已注册的每个路径操作。来自 `app.routes`。

/// info | 信息

参数 `summary` 仅在 OpenAPI 3.1.0 及更高版本中可用，FastAPI 0.99.0 及以上版本支持。

///

## 覆盖默认值 { #overriding-the-defaults }

基于以上信息，你可以用同一个工具函数生成 OpenAPI 架构，并按需覆盖其中的各个部分。

例如，让我们添加 <a href="https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo" class="external-link" target="_blank">ReDoc 的 OpenAPI 扩展以包含自定义 Logo</a>。

### 常规 **FastAPI** { #normal-fastapi }

首先，像平常一样编写你的 **FastAPI** 应用：

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[1,4,7:9] *}

### 生成 OpenAPI 架构 { #generate-the-openapi-schema }

然后，在一个 `custom_openapi()` 函数中使用同一个工具函数生成 OpenAPI 架构：

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[2,15:21] *}

### 修改 OpenAPI 架构 { #modify-the-openapi-schema }

现在你可以添加 ReDoc 扩展，在 OpenAPI 架构的 `info` “对象”中加入自定义 `x-logo`：

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[22:24] *}

### 缓存 OpenAPI 架构 { #cache-the-openapi-schema }

你可以把 `.openapi_schema` 属性当作“缓存”，用来存储已生成的架构。

这样一来，用户每次打开 API 文档时，应用就不必重新生成架构。

它只会生成一次，后续请求都会使用同一份缓存的架构。

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[13:14,25:26] *}

### 覆盖方法 { #override-the-method }

现在你可以用你的新函数替换 `.openapi()` 方法。

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[29] *}

### 验证 { #check-it }

当你访问 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> 时，你会看到已使用你的自定义 Logo（本例中为 **FastAPI** 的 Logo）：

<img src="/img/tutorial/extending-openapi/image01.png">
