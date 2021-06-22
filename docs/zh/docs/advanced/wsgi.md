# 包含Flask，Django等WSGI应用

如 [Sub Applications - Mounts](./sub-applications.md){.internal-link target=_blank}, [Behind a Proxy](./behind-a-proxy.md){.internal-link target=_blank} 章节所示，你同样也可以挂载其它WSGI应用程序。

你可以通过使用 `WSGIMiddleware` 包装其它WSGI 应用程序(如Flask, Django等)来实现。

## 使用 `WSGIMiddleware`

首先你需要导入 `WSGIMiddleware`。

然后用其包装 WSGI应用(例如Flask)。

最后将其挂载在一个请求路径下。

```Python hl_lines="2-3  22"
{!../../../docs_src/wsgi/tutorial001.py!}
```

## 验证

现在，每个`/v1/` 路径下的请求都将由 Flask 应用程序处理，其余的将由 **FastAPI** 处理。

使用 Uvicorn 运行程序后，如果你访问 <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a> 你会看到来自 Flask 的如下响应：

```txt
Hello, World from Flask!
```

如果你访问 <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a> 你会看到来自 FastAPI 的如下响应：

```JSON
{
    "message": "Hello World"
}
```
