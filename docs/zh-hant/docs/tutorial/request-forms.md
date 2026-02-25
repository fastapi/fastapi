# 表單資料 { #form-data }

當你需要接收表單欄位而不是 JSON 時，可以使用 `Form`。

/// info

要使用表單，請先安裝 <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>。

請先建立並啟用一個[虛擬環境](../virtual-environments.md){.internal-link target=_blank}，然後再安裝，例如：

```console
$ pip install python-multipart
```

///

## 匯入 `Form` { #import-form }

從 `fastapi` 匯入 `Form`：

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[3] *}

## 定義 `Form` 參數 { #define-form-parameters }

以與 `Body` 或 `Query` 相同的方式建立表單參數：

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[9] *}

例如，在 OAuth2 規範的一種用法（稱為「password flow」）中，必須以表單欄位傳送 `username` 與 `password`。

該 <dfn title="規範">規範</dfn> 要求欄位名稱必須正好是 `username` 和 `password`，而且必須以表單欄位傳送，而不是 JSON。

使用 `Form` 時，你可以宣告與 `Body`（以及 `Query`、`Path`、`Cookie`）相同的設定，包括驗證、範例、別名（例如用 `user-name` 取代 `username`）等。

/// info

`Form` 是一個直接繼承自 `Body` 的類別。

///

/// tip

要宣告表單的請求本文，你需要明確使用 `Form`，否則這些參數會被解讀為查詢參數或請求本文（JSON）參數。

///

## 關於「表單欄位」 { #about-form-fields }

HTML 表單（`<form></form>`）向伺服器傳送資料時，通常會使用一種「特殊」的編碼方式，與 JSON 不同。

**FastAPI** 會從正確的位置讀取那些資料，而不是從 JSON。

/// note | 技術細節

表單資料通常會使用「媒體類型」`application/x-www-form-urlencoded` 進行編碼。

但當表單包含檔案時，會使用 `multipart/form-data`。你會在下一章閱讀如何處理檔案。

若想進一步了解這些編碼與表單欄位，請參考 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network - Mozilla 開發者網路">MDN</abbr> 的 <code>POST</code> 網頁文件</a>。

///

/// warning

你可以在一個 *路徑操作（path operation）* 中宣告多個 `Form` 參數，但不能同時再宣告期望以 JSON 接收的 `Body` 欄位，因為該請求的本文會使用 `application/x-www-form-urlencoded` 編碼，而不是 `application/json`。

這不是 **FastAPI** 的限制，而是 HTTP 協定本身的規定。

///

## 回顧 { #recap }

使用 `Form` 來宣告表單資料的輸入參數。
