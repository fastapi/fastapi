# 集成 WSGI - Flask、Django 等 { #including-wsgi-flask-django-others }

你可以像在 [子应用 - 挂载](sub-applications.md)、[在代理后](behind-a-proxy.md) 里那样挂载 WSGI 应用。

为此，用 `WSGIMiddleware` 包一层你的 WSGI 应用，比如 Flask、Django 等。

## 使用 `WSGIMiddleware` { #using-wsgimiddleware }

/// note | 注意

需要先安装 `a2wsgi`，比如运行 `pip install a2wsgi`。

///

从 `a2wsgi` 导入 `WSGIMiddleware`。

然后用这个中间件包住 WSGI 应用（比如 Flask）。

再把它挂载到某个路径下。

{* ../../docs_src/wsgi/tutorial001_py310.py hl[1,3,23] *}

/// note | 注意

以前推荐用 `fastapi.middleware.wsgi` 里的 `WSGIMiddleware`，现在已弃用。

建议改用 `a2wsgi` 包。用法不变。

只要确保安装了 `a2wsgi`，并从 `a2wsgi` 正确导入 `WSGIMiddleware`。

///

## 试一下 { #check-it }

现在，路径 `/v1/` 下的请求都会由 Flask 应用处理。

其他路径走 **FastAPI**。

运行后，打开 [http://localhost:8000/v1/](http://localhost:8000/v1/)，能看到来自 Flask 的响应：

```txt
Hello, World from Flask!
```

打开 [http://localhost:8000/v2](http://localhost:8000/v2)，能看到来自 FastAPI 的响应：

```JSON
{
    "message": "Hello World"
}
```
