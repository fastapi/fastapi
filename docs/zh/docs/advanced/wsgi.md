# 包含 WSGI - Flask、Django 等

在 **FastAPI** 中挂载 WSGI 应用，要参照[子应用 - 挂载](./sub-applications.md){.internal-link target=_blank}与[使用代理](./behind-a-proxy.md){.internal-link target=_blank}两章的内容。

挂载 WSGI 应用要使用 `WSGIMiddleware`，并用它打包 Flask、Django 等 WSGI 应用。

## 使用 `WSGIMiddleware`

导入 `WSGIMiddleware`。

使用中间件打包 Flask 等 WSGI 应用。

然后，在路径下挂载该应用。

```Python hl_lines="2-3  22"
{!../../../docs_src/wsgi/tutorial001.py!}
```

## 查看文档

现在，就能用 Flask 应用处理 `/v1/` 路径下的每个请求。

其余的事情则由 **FastAPI** 处理。

运行 Uvicorn 并打开 <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a>，查看来自 Flask 的响应：

```txt
Hello, World from Flask!
```

打开 <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a>，查看来自 FastAPI 的响应：

```JSON
{
    "message": "Hello World"
}
```
