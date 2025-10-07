# 包含 WSGI - Flask，Django，其它

您可以挂载多个 WSGI 应用，正如您在 [Sub Applications - Mounts](sub-applications.md){.internal-link target=_blank}, [Behind a Proxy](behind-a-proxy.md){.internal-link target=_blank} 中所看到的那样。

为此, 您可以使用 `WSGIMiddleware` 来包装你的 WSGI 应用，如：Flask，Django，等等。

## 使用 `WSGIMiddleware`

您需要导入 `WSGIMiddleware`。

然后使用该中间件包装 WSGI 应用（例如 Flask）。

之后将其挂载到某一个路径下。

{* ../../docs_src/wsgi/tutorial001.py hl[2:3,22] *}

## 检查

现在，所有定义在 `/v1/` 路径下的请求将会被 Flask 应用处理。

其余的请求则会被 **FastAPI** 处理。

如果您使用 Uvicorn 运行应用实例并且访问 <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a>，您将会看到由 Flask 返回的响应：

```txt
Hello, World from Flask!
```

并且如果您访问 <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a>，您将会看到由 FastAPI 返回的响应：

```JSON
{
    "message": "Hello World"
}
```
