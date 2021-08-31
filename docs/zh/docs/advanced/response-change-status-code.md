# 响应 - 修改状态码

[响应状态码](../tutorial/response-status-code.md){.internal-link target=_blank}一章中介绍过如何设置默认状态码。

但有时要返回与默认状态码不同的状态码。

## 用例

例如，默认情况下返回 HTTP 状态码 - **OK** `200`。

但数据不存在时，要创建数据，并返回 HTTP 状态码 - **CREATED** `201`。

并且，还要使用 `response_model` 筛选并转换数据。

这些用例也可以使用 `Response` 参数。

## 使用 `Response` 参数

与处理 Cookie 和请求头响应一样，在*路径操作函数* 中可以声明 `Response` 类型的参数。

然后，在*临时*响应对象中设置状态码。

```Python hl_lines="1  9  12"
{!../../../docs_src/response_change_status_code/tutorial001.py!}
```

接下来，就可以像返回字典、数据库模型一样返回所需的任何对象。

声明了 `response_model` 时，仍可以筛选和转换返回的对象。

**FastAPI** 使用*临时*响应获取状态码（及 Cookie 与响应头），并把这些对象放入包含了 `response_model` 筛选过的返回值的最终响应。

依赖项中也可以声明 `Response` 参数，并设置状态码，但要注意，只有最后设置的状态码才会生效。

