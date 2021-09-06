# 响应 - Cookie

## 使用 `Response` 参数

*路径操作函数* 中可以声明 `Response` 类型的参数。

然后你可以在这个*临时*的响应对象中设置 cookie。

```Python hl_lines="1  8-9"
{!../../../docs_src/response_cookies/tutorial002.py!}
```

接着，就可以像返回字典、数据库模型一样返回任意所需的对象。

仍可以声明的 `response_model` 筛选和转换返回的对象。

**FastAPI** 使用*临时*响应获取 cookie（及响应头与状态码），并把这些对象放入包含了 `response_model` 筛选过的返回值的响应。

依赖项中也可以声明 `Response` 参数，并设置 cookie（和响应头）。

## 直接返回 `Response`

在代码中直接返回 `Response` 时，可以创建 cookie。

此时要以[直接返回响应](response-directly.md){.internal-link target=_blank}一章中所述的方式创建响应。

然后，在响应内设置 Cookie，并返回响应：

```Python hl_lines="10-12"
{!../../../docs_src/response_cookies/tutorial001.py!}
```

!!! tip "提示"

    注意，如果不使用 `Response` 参数而是直接返回一个响应对象，FastAPI 会将该响应不加处理直接返回给客户端。
    
    因此，必须确保数据类型是正确的。例如，使用 `JSONResponse` 返回响应时，数据类型要兼容 JSON。
    
    而且不能发送经 `response_model` 筛选过的数据。

### 更多说明

!!! note "技术细节"

    您也可以使用 `from starlette.responses import Response` 或 `from starlette.responses import JSONResponse`。
    
    **FastAPI** 的 `fastapi.responses` 与 `starlette.responses` 一样，只是为开发者提供的快捷方式，但其中绝大部分可用的响应都直接继承自 Starlette。
    
    `Response` 常用于设置响应头或 Cookie，因此，**FastAPI** 在 `fastapi.Response` 中提供了支持。

所有可用参数及选项，详见 <a href="https://www.starlette.io/responses/#set-cookie" class="external-link" target="_blank">Starlette 官档</a>。

