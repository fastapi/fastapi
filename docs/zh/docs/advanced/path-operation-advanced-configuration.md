# 路径操作高级配置

## OpenAPI operationId

!!! warning
    你要不是 OpenAPI "专家"，估计也用不着这个。

你可以使用参数 `operation_id` 设置要在路径操作中使用的 OpenAPI `operationId`。

你必须确保每个路径操作是唯一的。

```Python hl_lines="6"
{!../../../docs_src/path_operation_advanced_configuration/tutorial001.py!}
```

### 用*路径操作函数*的函数名作为 operationId

如果想用 API 的函数名作为 `operationId`，你可以遍历所有 API 然后用其 `APIRoute.name` 覆盖每个 *路径操作* 的 `operation_id`。

你应该在添加了所有 *路径操作* 之后再这么做。

```Python hl_lines="2 12 13 14 15 16 17 18 19 20 21 24"
{!../../../docs_src/path_operation_advanced_configuration/tutorial002.py!}
```

!!! tip
    如果你是手动调用 `app.openapi()`，你得在调用前更新`openationId`。

!!! warning
	如果你这样做的话，你必须确保每个 *路径操作函数* 的名字是唯一的。

	即便这些函数在不同的模块里(Python文件)

## 从 OpenAPI 里排除

要从生成的 OpenAPI 架构（以及自动文档系统）中排除 *路径操作*，可以将参数 `include_in_schema` 设置为 False:

```Python hl_lines="6"
{!../../../docs_src/path_operation_advanced_configuration/tutorial003.py!}
```

## Docstring 的高级描述

你可以限制被用来做 OpenAPI *路径操作函数* 文档的 docstinrg 行。

加一个`\f`（转义的“换页符”字符）就可以让 FastAPI 截断用于 OpenAPI 的输出。

截断剩下的不会显示在文档中，但是其他工具可以继续用（例如Sphinx）。

```Python hl_lines="19 20 21 22 23 24 25 26 27 28 29"
{!../../../docs_src/path_operation_advanced_configuration/tutorial004.py!}
```


