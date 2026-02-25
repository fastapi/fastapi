# 自訂 Request 與 APIRoute 類別 { #custom-request-and-apiroute-class }

在某些情況下，你可能想要覆寫 `Request` 與 `APIRoute` 類別所使用的邏輯。

特別是，這可能是替代中介軟體（middleware）中實作邏輯的一個好方法。

例如，如果你想在應用程式處理之前讀取或操作請求本文（request body）。

/// danger

這是進階功能。

如果你剛開始使用 **FastAPI**，可以先跳過本節。

///

## 使用情境 { #use-cases }

可能的使用情境包括：

* 將非 JSON 的請求本文轉換為 JSON（例如 <a href="https://msgpack.org/index.html" class="external-link" target="_blank">`msgpack`</a>）。
* 解壓縮以 gzip 壓縮的請求本文。
* 自動記錄所有請求本文。

## 處理自訂請求本文編碼 { #handling-custom-request-body-encodings }

讓我們看看如何使用自訂的 `Request` 子類別來解壓縮 gzip 請求。

並透過 `APIRoute` 子類別來使用該自訂的請求類別。

### 建立自訂的 `GzipRequest` 類別 { #create-a-custom-gziprequest-class }

/// tip

這是一個示範用的簡化範例；如果你需要 Gzip 支援，可以直接使用提供的 [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware){.internal-link target=_blank}。

///

首先，我們建立 `GzipRequest` 類別，它會覆寫 `Request.body()` 方法，當存在對應的標頭時解壓縮本文。

如果標頭中沒有 `gzip`，它就不會嘗試解壓縮本文。

如此一來，相同的路由類別即可同時處理經 gzip 壓縮與未壓縮的請求.

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[9:16] *}

### 建立自訂的 `GzipRoute` 類別 { #create-a-custom-gziproute-class }

接著，我們建立 `fastapi.routing.APIRoute` 的自訂子類別，讓它使用 `GzipRequest`。

這次，它會覆寫 `APIRoute.get_route_handler()` 方法。

這個方法會回傳一個函式，而該函式會接收請求並回傳回應。

在這裡，我們用它將原始的請求包裝成 `GzipRequest`。

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[19:27] *}

/// note | 技術細節

`Request` 具有 `request.scope` 屬性，它其實就是一個 Python 的 `dict`，包含與該請求相關的中繼資料。

`Request` 也有 `request.receive`，那是一個用來「接收」請求本文的函式。

`scope` 這個 `dict` 與 `receive` 函式都是 ASGI 規格的一部分。

而 `scope` 與 `receive` 這兩者，就是建立一個新的 `Request` 實例所需的資料。

想了解更多 `Request`，請參考 <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">Starlette 的 Request 文件</a>。

///

由 `GzipRequest.get_route_handler` 回傳的函式，唯一不同之處在於它會把 `Request` 轉換成 `GzipRequest`。

這麼做之後，`GzipRequest` 會在把資料交給 *路徑操作* 之前（若有需要）先負責解壓縮。

之後的處理邏輯完全相同。

但由於我們修改了 `GzipRequest.body`，在 **FastAPI** 需要讀取本文時，請求本文會自動解壓縮。

## 在例外處理器中存取請求本文 { #accessing-the-request-body-in-an-exception-handler }

/// tip

要解決相同問題，使用針對 `RequestValidationError` 的自訂處理器來讀取 `body` 通常更簡單（[處理錯誤](../tutorial/handling-errors.md#use-the-requestvalidationerror-body){.internal-link target=_blank}）。

但本範例仍然有效，並示範了如何與內部元件互動。

///

我們也可以用同樣的方法，在例外處理器中存取請求本文。

我們只需要在 `try`/`except` 區塊中處理請求即可：

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[14,16] *}

若發生例外，`Request` 實例依然在作用域內，因此在處理錯誤時我們仍可讀取並使用請求本文：

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[17:19] *}

## 在路由器中自訂 `APIRoute` 類別 { #custom-apiroute-class-in-a-router }

你也可以在 `APIRouter` 上設定 `route_class` 參數：

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[26] *}

在此範例中，`router` 底下的路徑操作會使用自訂的 `TimedRoute` 類別，並在回應中多加上一個 `X-Response-Time` 標頭，標示產生該回應所花費的時間：

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[13:20] *}
