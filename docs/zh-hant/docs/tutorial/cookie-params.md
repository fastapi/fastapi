# Cookie 參數 { #cookie-parameters }

你可以用與定義 `Query` 與 `Path` 參數相同的方式定義 Cookie 參數。

## 匯入 `Cookie` { #import-cookie }

先匯入 `Cookie`：

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## 宣告 `Cookie` 參數 { #declare-cookie-parameters }

然後用與 `Path`、`Query` 相同的結構宣告 `Cookie` 參數。

你可以設定預設值，以及所有額外的驗證或註解參數：

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | 技術細節

`Cookie` 是 `Path` 與 `Query` 的「姊妹」類別。它同樣繼承自共同的 `Param` 類別。

但請記住，當你從 `fastapi` 匯入 `Query`、`Path`、`Cookie` 等時，它們實際上是回傳特殊類別的函式。

///

/// info

要宣告 cookies，你需要使用 `Cookie`，否則參數會被當作查詢參數（query parameters）來解析。

///

/// info

請注意，由於瀏覽器以特殊且在背後處理的方式管理 cookies，它們通常不允許 JavaScript 輕易存取它們。

如果你前往位於 `/docs` 的 API 文件介面，你可以在你的路徑操作（path operations）的文件中看到 cookies 的說明。

但即使你填入資料並點擊「Execute」，由於該文件介面是以 JavaScript 運作，cookies 不會被送出，你會看到一則錯誤訊息，就好像你沒有填任何值一樣。

///

## 總結 { #recap }

使用 `Cookie` 來宣告 cookies，遵循與 `Query`、`Path` 相同的通用寫法。
