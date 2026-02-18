# 包含 WSGI：Flask、Django 等 { #including-wsgi-flask-django-others }

你可以像在 [子應用程式 - 掛載](sub-applications.md){.internal-link target=_blank}、[在 Proxy 後方](behind-a-proxy.md){.internal-link target=_blank} 中所見那樣掛載 WSGI 應用。

為此，你可以使用 `WSGIMiddleware` 來包住你的 WSGI 應用，例如 Flask、Django 等。

## 使用 `WSGIMiddleware` { #using-wsgimiddleware }

/// info

這需要先安裝 `a2wsgi`，例如使用 `pip install a2wsgi`。

///

你需要從 `a2wsgi` 匯入 `WSGIMiddleware`。

然後用該 middleware 包住 WSGI（例如 Flask）應用。

接著把它掛載到某個路徑下。

{* ../../docs_src/wsgi/tutorial001_py310.py hl[1,3,23] *}

/// note

先前建議使用來自 `fastapi.middleware.wsgi` 的 `WSGIMiddleware`，但現在已棄用。

建議改用 `a2wsgi` 套件。用法保持相同。

只要確保已安裝 `a2wsgi`，並從 `a2wsgi` 正確匯入 `WSGIMiddleware` 即可。

///

## 試試看 { #check-it }

現在，位於路徑 `/v1/` 底下的所有請求都會由 Flask 應用處理。

其餘則由 **FastAPI** 處理。

如果你啟動它並前往 <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a>，你會看到來自 Flask 的回應：

```txt
Hello, World from Flask!
```

如果你前往 <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a>，你會看到來自 FastAPI 的回應：

```JSON
{
    "message": "Hello World"
}
```
