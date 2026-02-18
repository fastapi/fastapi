# 安全性 - 入門 { #security-first-steps }

想像你有一個部署在某個網域的後端 API。

還有一個前端在另一個網域，或同一網域的不同路徑（或是行動應用程式）。

你希望前端能用使用者名稱與密碼向後端進行身分驗證。

我們可以用 OAuth2 搭配 FastAPI 來實作。

但不必通讀整份冗長規格只為了找出你需要的幾個重點。

就用 FastAPI 提供的工具處理安全性。

## 看起來如何 { #how-it-looks }

先直接跑範例看效果，再回頭理解其原理。

## 建立 `main.py` { #create-main-py }

將範例複製到檔案 `main.py`：

{* ../../docs_src/security/tutorial001_an_py310.py *}

## 執行 { #run-it }

/// info

當你使用 `pip install "fastapi[standard]"` 指令安裝時，<a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> 套件會隨 FastAPI 自動安裝。

不過若只執行 `pip install fastapi`，預設不會包含 `python-multipart`。

若要手動安裝，請先建立並啟用一個[虛擬環境](../../virtual-environments.md){.internal-link target=_blank}，接著執行：

```console
$ pip install python-multipart
```

因為 OAuth2 會以「form data」傳送 `username` 與 `password`。

///

用以下指令執行範例：

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## 檢查 { #check-it }

開啟互動式文件：<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你會看到類似這樣：

<img src="/img/tutorial/security/image01.png">

/// check | Authorize 按鈕！

你會看到一個新的「Authorize」按鈕。

而你的「路徑操作」右上角也會出現一個小鎖頭可以點擊。

///

點擊後會跳出一個小視窗，讓你輸入 `username` 與 `password`（以及其他可選欄位）：

<img src="/img/tutorial/security/image02.png">

/// note | 注意

不管你在表單輸入什麼，現在都還不會成功；等等我們會把它完成。

///

這當然不是給最終使用者用的前端，但它是用來互動式文件化整個 API 的極佳自動化工具。

前端團隊（也可能就是你）可以使用它。

第三方應用或系統也能使用它。

你也能用它來除錯、檢查與測試同一個應用。

## `password` 流程 { #the-password-flow }

現在回頭理解剛剛那些是什麼。

在 OAuth2 中，`password` 是處理安全與身分驗證的其中一種「流程」（flow）。

OAuth2 的設計讓後端或 API 可以獨立於執行使用者驗證的伺服器。

但在這個例子中，同一個 FastAPI 應用會同時處理 API 與驗證。

簡化來看流程如下：

- 使用者在前端輸入 `username` 與 `password`，按下 `Enter`。
- 前端（在使用者的瀏覽器中執行）把 `username` 與 `password` 傳到我們 API 的特定 URL（在程式中宣告為 `tokenUrl="token"`）。
- API 檢查 `username` 與 `password`，並回傳一個「token（權杖）」（我們還沒實作這部分）。
    - 「token（權杖）」就是一段字串，之後可用來識別並驗證此使用者。
    - 通常 token 會設定一段時間後失效。
        - 因此使用者之後需要重新登入。
        - 若 token 被竊取，風險也較低；它不像永遠有效的萬用鑰匙（多數情況下）。
- 前端會暫存這個 token。
- 使用者在前端點擊前往其他頁面/區段。
- 前端需要再向 API 取得資料。
    - 但該端點需要驗證。
    - 因此為了向 API 驗證，請求會帶上一個 `Authorization` 標頭，值為 `Bearer ` 加上 token。
    - 例如 token 是 `foobar`，則 `Authorization` 標頭內容為：`Bearer foobar`。

## FastAPI 的 `OAuth2PasswordBearer` { #fastapis-oauth2passwordbearer }

FastAPI 提供多層抽象的工具來實作這些安全機制。

本例將使用 OAuth2 的 Password 流程，並以 Bearer token 進行驗證；我們會用 `OAuth2PasswordBearer` 類別來完成。

/// info

「Bearer」token 不是唯一選項。

但對本例最合適。

通常對多數情境也足夠，除非你是 OAuth2 專家並確信有更適合你的選項。

在那種情況下，FastAPI 也提供相應工具讓你自行組合。

///

當我們建立 `OAuth2PasswordBearer` 類別的實例時，會傳入 `tokenUrl` 參數。這個參數包含了客戶端（在使用者瀏覽器中執行的前端）用來送出 `username` 與 `password` 以取得 token 的 URL。

{* ../../docs_src/security/tutorial001_an_py310.py hl[8] *}

/// tip

這裡的 `tokenUrl="token"` 指的是尚未建立的相對 URL `token`。因為是相對 URL，所以等同於 `./token`。

由於使用了相對 URL，若你的 API 位於 `https://example.com/`，那它會指向 `https://example.com/token`；但若你的 API 位於 `https://example.com/api/v1/`，那它會指向 `https://example.com/api/v1/token`。

使用相對 URL 很重要，能確保你的應用在像是[在 Proxy 後方](../../advanced/behind-a-proxy.md){.internal-link target=_blank}這類進階情境中仍能正常運作。

///

這個參數不會建立該端點／「路徑操作」，而是宣告 `/token` 將是客戶端用來取得 token 的 URL。這些資訊會出現在 OpenAPI，並被互動式 API 文件系統使用。

我們很快也會建立實際的路徑操作。

/// info

如果你是非常嚴格的「Pythonista」，可能不喜歡參數名稱用 `tokenUrl` 而不是 `token_url`。

那是因為它沿用了 OpenAPI 規格中的名稱。如此一來，若你要深入查閱這些安全方案，便能直接複製貼上去搜尋更多資訊。

///

變數 `oauth2_scheme` 是 `OAuth2PasswordBearer` 的實例，但同時它也是「可呼叫的」（callable）。

它可以這樣被呼叫：

```Python
oauth2_scheme(some, parameters)
```

因此它可以配合 `Depends` 使用。

### 如何使用 { #use-it }

現在你可以在相依性中傳入 `oauth2_scheme` 與 `Depends` 搭配。

{* ../../docs_src/security/tutorial001_an_py310.py hl[12] *}

此相依性會提供一個 `str`，指派給「路徑操作函式」的參數 `token`。

FastAPI 會知道可以使用這個相依性，在 OpenAPI（以及自動產生的 API 文件）中定義一個「安全性方案」。

/// info | 技術細節

FastAPI 之所以知道可以用（相依性中宣告的）`OAuth2PasswordBearer` 類別，在 OpenAPI 中定義安全性方案，是因為它繼承自 `fastapi.security.oauth2.OAuth2`，而後者又繼承自 `fastapi.security.base.SecurityBase`。

所有能與 OpenAPI（以及自動 API 文件）整合的安全工具都繼承自 `SecurityBase`，FastAPI 才能知道如何把它們整合進 OpenAPI。

///

## 它做了什麼 { #what-it-does }

它會從請求中尋找 `Authorization` 標頭，檢查其值是否為 `Bearer ` 加上一段 token，並將該 token 以 `str` 回傳。

若未找到 `Authorization` 標頭，或其值不是 `Bearer ` token，則會直接回傳 401（`UNAUTHORIZED`）錯誤。

你不必再自行檢查 token 是否存在；你可以確信只要你的函式被執行，該 token 參數就一定會是 `str`。

你可以在互動式文件中試試看：

<img src="/img/tutorial/security/image03.png">

我們還沒驗證 token 是否有效，但這已是個開始。

## 小結 { #recap }

只需多寫 3、4 行，就能有一個基本的安全機制。
