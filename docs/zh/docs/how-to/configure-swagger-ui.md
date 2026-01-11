# 配置 Swagger UI { #configure-swagger-ui }

你可以配置一些额外的 <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">Swagger UI 参数</a>。

如果需要配置它们，可以在创建 `FastAPI()` 应用对象时或调用 `get_swagger_ui_html()` 函数时传递 `swagger_ui_parameters` 参数。

`swagger_ui_parameters` 接受一个字典，其中的配置会直接传递给 Swagger UI。

FastAPI 会将这些配置转换为 **JSON**，使其与 JavaScript 兼容，因为这是 Swagger UI 需要的。

## 禁用语法高亮 { #disable-syntax-highlighting }

比如，你可以禁用 Swagger UI 中的语法高亮。

当没有改变设置时，语法高亮默认启用：

<img src="/img/tutorial/extending-openapi/image02.png">

但是你可以通过设置 `syntaxHighlight` 为 `False` 来禁用：

{* ../../docs_src/configure_swagger_ui/tutorial001_py39.py hl[3] *}

...在此之后，Swagger UI 将不再显示语法高亮：

<img src="/img/tutorial/extending-openapi/image03.png">

## 更改主题 { #change-the-theme }

同样地，你也可以通过键 `"syntaxHighlight.theme"` 来设置语法高亮主题（注意中间有一个点）：

{* ../../docs_src/configure_swagger_ui/tutorial002_py39.py hl[3] *}

这个配置会更改语法高亮的颜色主题：

<img src="/img/tutorial/extending-openapi/image04.png">

## 更改默认 Swagger UI 参数 { #change-default-swagger-ui-parameters }

FastAPI 包含了一些适用于大多数用例的默认配置参数。

其包括这些默认配置：

{* ../../fastapi/openapi/docs.py ln[9:24] hl[18:24] *}

你可以通过在参数 `swagger_ui_parameters` 中设置不同的值来覆盖其中任意一项。

比如，如果要禁用 `deepLinking`，你可以把这些设置传递给 `swagger_ui_parameters`：

{* ../../docs_src/configure_swagger_ui/tutorial003_py39.py hl[3] *}

## 其他 Swagger UI 参数 { #other-swagger-ui-parameters }

要查看你可以使用的所有其他可能配置，请阅读官方的 <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">Swagger UI 参数文档</a>。

## 仅 JavaScript 的设置 { #javascript-only-settings }

Swagger UI 也允许将其他配置设为 **仅 JavaScript** 对象（例如，JavaScript 函数）。

FastAPI 也包含这些仅 JavaScript 的 `presets` 设置：

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

这些是 **JavaScript** 对象，而不是字符串，所以你不能直接从 Python 代码中传递它们。

如果你需要像那样使用仅 JavaScript 的配置，你可以使用上述方法之一。覆盖所有 Swagger UI *path operation* 并手动编写任何你需要的 JavaScript。
