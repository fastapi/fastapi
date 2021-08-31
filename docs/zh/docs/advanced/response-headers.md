# 响应头

## 使用 `Response` 参数

与声明 Cookie 响应一样，*路径操作函数*中还可以声明 `Response` 类型的参数。

现在，在*临时*响应对象中设置响应头。

```Python hl_lines="1  7-8"
{!../../../docs_src/response_headers/tutorial002.py!}
```

接着，就可以像返回字典、数据库模型一样返回任意所需的对象。

仍可以使用声明的 `response_model` 筛选和转换返回的对象。

**FastAPI** 使用*临时*响应获取响应头（及 Cookie 与状态码），并把这些对象放入包含了 `response_model` 筛选过的返回值的最终响应。

依赖项中也可以声明 `Response` 参数，并设置响应头（和 Cookie）。

## 直接返回 `Response`

直接返回 `Response` 时，也可以添加响应头。

以[直接返回响应](response-directly.md){.internal-link target=_blank}所述的方式创建响应，并以附加参数的形式传递响应头：

```Python hl_lines="10-12"
{!../../../docs_src/response_headers/tutorial001.py!}
```

!!! note "技术细节"

    您也可以使用 `from starlette.responses import Response` 或 `from starlette.responses import JSONResponse`。
    
    **FastAPI** 的 `fastapi.responses` 与 `starlette.responses` 一样，只是为开发者提供的快捷方式，但其中绝大部分可用的响应都直接继承自 Starlette。
    
    `Response` 常用于设置响应头与 Cookie，因此，**FastAPI** 也在 `fastapi.Response` 中提供了支持。

## 自定义响应头

注意，自定义专用响应头可以添加<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">前缀 'X-'</a>。

但如果需要浏览器中的客户端查看自定义响应头，则要在 CORS 配置中（详见 [CORS（跨域资源共享）](../tutorial/cors.md){.internal-link target=_blank})使用 <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette 官档 - CORS</a> 中的 `expose_headers` 参数。

