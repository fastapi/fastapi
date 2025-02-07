# 配置 Swagger UI

你可以配置一些额外的 <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">Swagger UI 参数</a>.

如果需要配置它们，可以在创建 `FastAPI()` 应用对象时或调用 `get_swagger_ui_html()` 函数时传递 `swagger_ui_parameters` 参数。

`swagger_ui_parameters` 接受一个直接传递给 Swagger UI的字典，包含配置参数键值对。

FastAPI会将这些配置转换为 **JSON**，使其与 JavaScript 兼容，因为这是 Swagger UI 需要的。

## 不使用语法高亮

比如，你可以禁用 Swagger UI 中的语法高亮。

当没有改变设置时，语法高亮默认启用：

<img src="/img/tutorial/extending-openapi/image02.png">

但是你可以通过设置 `syntaxHighlight` 为 `False` 来禁用 Swagger UI 中的语法高亮：

{* ../../docs_src/configure_swagger_ui/tutorial001.py hl[3] *}

...在此之后，Swagger UI 将不会高亮代码:

<img src="/img/tutorial/extending-openapi/image03.png">

## 改变主题

同样地，你也可以通过设置键 `"syntaxHighlight.theme"` 来设置语法高亮主题（注意中间有一个点）：

{* ../../docs_src/configure_swagger_ui/tutorial002.py hl[3] *}

这个配置会改变语法高亮主题：

<img src="/img/tutorial/extending-openapi/image04.png">

## 改变默认 Swagger UI 参数

FastAPI 包含了一些默认配置参数，适用于大多数用例。

其包括这些默认配置参数：

{* ../../fastapi/openapi/docs.py ln[7:23] *}

你可以通过在 `swagger_ui_parameters` 中设置不同的值来覆盖它们。

比如，如果要禁用 `deepLinking`，你可以像这样传递设置到 `swagger_ui_parameters` 中：

{* ../../docs_src/configure_swagger_ui/tutorial003.py hl[3] *}

## 其他 Swagger UI 参数

查看其他 Swagger UI 参数，请阅读 <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">docs for Swagger UI parameters</a>。

## JavaScript-only 配置

Swagger UI 同样允许使用 **JavaScript-only** 配置对象（例如，JavaScript 函数）。

FastAPI 包含这些 JavaScript-only 的 `presets` 设置：

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

这些是 **JavaScript** 对象，而不是字符串，所以你不能直接从 Python 代码中传递它们。

如果你需要像这样使用 JavaScript-only 配置，你可以使用上述方法之一。覆盖所有 Swagger UI *path operation* 并手动编写任何你需要的 JavaScript。
