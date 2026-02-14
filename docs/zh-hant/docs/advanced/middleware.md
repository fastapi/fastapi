# 進階中介軟體 { #advanced-middleware }

在主要教學中你已學過如何將[自訂中介軟體](../tutorial/middleware.md){.internal-link target=_blank}加入到你的應用程式。

你也讀過如何使用 `CORSMiddleware` 處理 [CORS](../tutorial/cors.md){.internal-link target=_blank}。

本節將示範如何使用其他中介軟體。

## 新增 ASGI 中介軟體 { #adding-asgi-middlewares }

由於 **FastAPI** 建立在 Starlette 上並實作了 <abbr title="Asynchronous Server Gateway Interface - 非同步伺服器閘道介面">ASGI</abbr> 規範，你可以使用任何 ASGI 中介軟體。

中介軟體不一定要為 FastAPI 或 Starlette 專門撰寫，只要遵循 ASGI 規範即可運作。

一般來說，ASGI 中介軟體是類別，預期第一個參數接收一個 ASGI 應用程式。

因此，在第三方 ASGI 中介軟體的文件中，通常會指示你這樣做：

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

但 FastAPI（實際上是 Starlette）提供了一種更簡單的方式，確保內部中介軟體能處理伺服器錯誤，且自訂例外處理器可正常運作。

為此，你可以使用 `app.add_middleware()`（如同 CORS 範例）。

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` 將中介軟體類別作為第一個引數，並接收要傳遞給該中介軟體的其他引數。

## 內建中介軟體 { #integrated-middlewares }

**FastAPI** 內建數個常見用途的中介軟體，以下將示範如何使用。

/// note | 技術細節

在接下來的範例中，你也可以使用 `from starlette.middleware.something import SomethingMiddleware`。

**FastAPI** 在 `fastapi.middleware` 中提供了一些中介軟體，純粹是為了方便你這位開發者。但大多數可用的中介軟體直接來自 Starlette。

///

## `HTTPSRedirectMiddleware` { #httpsredirectmiddleware }

強制所有傳入請求必須使用 `https` 或 `wss`。

任何指向 `http` 或 `ws` 的請求都會被重新導向至對應的安全協定。

{* ../../docs_src/advanced_middleware/tutorial001_py310.py hl[2,6] *}

## `TrustedHostMiddleware` { #trustedhostmiddleware }

強制所有傳入請求正確設定 `Host` 標頭，以防範 HTTP Host Header 攻擊。

{* ../../docs_src/advanced_middleware/tutorial002_py310.py hl[2,6:8] *}

支援以下參數：

- `allowed_hosts` - 允許作為主機名稱的網域名稱清單。支援萬用字元網域（例如 `*.example.com`）以比對子網域。若要允許任意主機名稱，可使用 `allowed_hosts=["*"]`，或乾脆不要加上此中介軟體。
- `www_redirect` - 若設為 True，對允許主機的不含 www 版本的請求會被重新導向至其 www 對應版本。預設為 `True`。

若傳入請求驗證失敗，將回傳 `400` 回應。

## `GZipMiddleware` { #gzipmiddleware }

處理在 `Accept-Encoding` 標頭中包含 `"gzip"` 的請求之 GZip 壓縮回應。

此中介軟體會處理一般與串流回應。

{* ../../docs_src/advanced_middleware/tutorial003_py310.py hl[2,6] *}

支援以下參數：

- `minimum_size` - 小於此位元組大小的回應不會進行 GZip。預設為 `500`。
- `compresslevel` - GZip 壓縮時使用的等級。為 1 到 9 的整數。預設為 `9`。值越小壓縮越快但檔案較大，值越大壓縮較慢但檔案較小。

## 其他中介軟體 { #other-middlewares }

還有許多其他 ASGI 中介軟體。

例如：

- <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">Uvicorn 的 `ProxyHeadersMiddleware`</a>
- <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">MessagePack</a>

想瞭解更多可用的中介軟體，請參考 <a href="https://www.starlette.dev/middleware/" class="external-link" target="_blank">Starlette 的中介軟體文件</a> 與 <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">ASGI 精選清單</a>。
