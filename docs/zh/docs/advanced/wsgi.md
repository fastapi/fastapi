# 包含 WSGI - Flask，Django，其它 { #including-wsgi-flask-django-others }

您可以挂载 WSGI 应用，正如您在 [子应用 - 挂载](sub-applications.md){.internal-link target=_blank}、[在代理之后](behind-a-proxy.md){.internal-link target=_blank} 中所看到的那样。

为此, 您可以使用 `WSGIMiddleware` 来包装你的 WSGI 应用，如：Flask，Django，等等。

## 使用 `WSGIMiddleware` { #using-wsgimiddleware }

/// info | 信息

需要安装 `a2wsgi`，例如使用 `pip install a2wsgi`。

///

您需要从 `a2wsgi` 导入 `WSGIMiddleware`。

然后使用该中间件包装 WSGI 应用（例如 Flask）。

之后将其挂载到某一个路径下。

{* ../../docs_src/wsgi/tutorial001_py310.py hl[1,3,23] *}

/// note | 注意

之前推荐使用 `fastapi.middleware.wsgi` 中的 `WSGIMiddleware`，但它现在已被弃用。

建议改用 `a2wsgi` 包，使用方式保持不变。

只要确保已安装 `a2wsgi` 包，并且从 `a2wsgi` 正确导入 `WSGIMiddleware` 即可。

///

## 检查 { #check-it }

现在，所有定义在 `/v1/` 路径下的请求将会被 Flask 应用处理。

其余的请求则会被 **FastAPI** 处理。

如果你运行它并访问 <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a>，你将会看到由 Flask 返回的响应：

```txt
Hello, World from Flask!
```

如果你访问 <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a>，你将会看到由 FastAPI 返回的响应：

```JSON
{
    "message": "Hello World"
}
```
