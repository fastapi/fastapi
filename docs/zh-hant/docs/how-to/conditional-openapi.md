# 條件式 OpenAPI { #conditional-openapi }

如果需要，你可以用設定與環境變數，依據執行環境有條件地調整 OpenAPI，甚至完全停用它。

## 關於安全性、API 與文件 { #about-security-apis-and-docs }

在正式環境中隱藏文件 UI *不應該* 是用來保護 API 的方式。

這並不會為你的 API 增添任何額外的安全性，*路徑操作* 仍舊照常可用。

若你的程式碼有安全性缺陷，它依然會存在。

隱藏文件只會讓他人更難理解如何與你的 API 互動，也可能讓你在正式環境除錯更困難。這通常僅被視為一種 <a href="https://en.wikipedia.org/wiki/Security_through_obscurity" class="external-link" target="_blank">以隱匿求安全</a>。

如果你想保護 API，有許多更好的作法，例如：

- 確保針對請求本文與回應，具備定義良好的 Pydantic 模型。
- 透過依賴設定所需的權限與角色。
- 切勿儲存明文密碼，只儲存密碼雜湊。
- 實作並使用成熟且廣為人知的密碼學工具，例如 pwdlib 與 JWT 權杖等。
- 視需要以 OAuth2 scopes 新增更細緻的權限控管。
- ...等。

儘管如此，在某些特定情境下，你可能確實需要在某些環境（例如正式環境）停用 API 文件，或依據環境變數的設定來決定是否啟用。

## 透過設定與環境變數的條件式 OpenAPI { #conditional-openapi-from-settings-and-env-vars }

你可以用相同的 Pydantic 設定，來配置產生的 OpenAPI 與文件 UI。

例如：

{* ../../docs_src/conditional_openapi/tutorial001_py310.py hl[6,11] *}

這裡我們宣告 `openapi_url` 設定，預設值同樣是 `"/openapi.json"`。

接著在建立 `FastAPI` 應用時使用它。

然後你可以將環境變數 `OPENAPI_URL` 設為空字串，以停用 OpenAPI（包含文件 UI），如下：

<div class="termy">

```console
$ OPENAPI_URL= uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

之後若你造訪 `/openapi.json`、`/docs` 或 `/redoc`，會看到如下的 `404 Not Found` 錯誤：

```JSON
{
    "detail": "Not Found"
}
```
