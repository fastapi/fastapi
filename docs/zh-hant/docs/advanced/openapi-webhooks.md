# OpenAPI Webhook { #openapi-webhooks }

有些情況下，你會想告訴你的 API 使用者，你的應用程式可能會攜帶一些資料去呼叫他們的應用程式（發送請求），通常是為了通知某種類型的事件。

這表示，與其由使用者向你的 API 發送請求，改為你的 API（或你的應用）可能會向他們的系統（他們的 API、他們的應用）發送請求。

這通常稱為 webhook。

## Webhook 步驟 { #webhooks-steps }

流程通常是：你在程式碼中定義要發送的訊息，也就是請求的主體（request body）。

你也會以某種方式定義應用在哪些時刻會發送那些請求或事件。

而你的使用者則會以某種方式（例如在某個 Web 控制台）設定你的應用應該將這些請求送往的 URL。

關於如何註冊 webhook 的 URL，以及實際發送那些請求的程式碼等所有邏輯，都由你決定。你可以在自己的程式碼中用你想要的方式撰寫。

## 使用 FastAPI 與 OpenAPI 記錄 webhook { #documenting-webhooks-with-fastapi-and-openapi }

在 FastAPI 中，透過 OpenAPI，你可以定義這些 webhook 的名稱、你的應用將發送的 HTTP 操作類型（例如 `POST`、`PUT` 等），以及你的應用要發送的請求主體。

這能讓你的使用者更容易實作他們的 API 以接收你的 webhook 請求，甚至可能自動產生部分他們自己的 API 程式碼。

/// info

Webhook 功能自 OpenAPI 3.1.0 起提供，FastAPI `0.99.0` 以上版本支援。

///

## 含有 webhook 的應用 { #an-app-with-webhooks }

建立 FastAPI 應用時，會有一個 `webhooks` 屬性可用來定義 webhook，方式與定義路徑操作相同，例如使用 `@app.webhooks.post()`。

{* ../../docs_src/openapi_webhooks/tutorial001_py310.py hl[9:12,15:20] *}

你定義的 webhook 會出現在 OpenAPI 結構描述與自動產生的文件 UI 中。

/// info

`app.webhooks` 其實就是一個 `APIRouter`，與你在將應用拆分為多個檔案時所使用的型別相同。

///

注意，使用 webhook 時你其實不是在宣告路徑（例如 `/items/`），你傳入的文字只是該 webhook 的識別名稱（事件名稱）。例如在 `@app.webhooks.post("new-subscription")` 中，webhook 名稱是 `new-subscription`。

這是因為預期由你的使用者以其他方式（例如 Web 控制台）來設定實際要接收 webhook 請求的 URL 路徑。

### 查看文件 { #check-the-docs }

現在你可以啟動應用，然後前往 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你會在文件中看到一般的路徑操作，另外還有一些 webhook：

<img src="/img/tutorial/openapi-webhooks/image01.png">
