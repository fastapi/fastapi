# 直接使用 Request { #using-the-request-directly }

到目前為止，你都是用對應的型別來宣告你需要的請求各部分。

例如從以下來源取得資料：

- 路徑中的參數。
- 標頭。
- Cookies。
- 等等。

這麼做時，FastAPI 會自動驗證並轉換這些資料，還會為你的 API 產生文件。

但有些情況你可能需要直接存取 `Request` 物件。

## 關於 `Request` 物件的細節 { #details-about-the-request-object }

由於 FastAPI 底層其實是 Starlette，再加上一層工具，因此在需要時你可以直接使用 Starlette 的 <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">`Request`</a> 物件。

同時也代表，如果你直接從 `Request` 物件取得資料（例如讀取 body），FastAPI 不會替它做驗證、轉換或文件化（透過 OpenAPI 為自動化的 API 介面產生文件）。

不過，其他以一般方式宣告的參數（例如以 Pydantic 模型宣告的 body）仍然會被驗證、轉換、加上標註等。

但在某些特定情境下，直接取得 `Request` 物件會很實用。

## 直接使用 `Request` 物件 { #use-the-request-object-directly }

假設你想在你的 路徑操作函式（path operation function） 中取得用戶端的 IP 位址／主機。

為此，你需要直接存取請求。

{* ../../docs_src/using_request_directly/tutorial001_py310.py hl[1,7:8] *}

只要在 路徑操作函式 中宣告一個型別為 `Request` 的參數，FastAPI 就會將當前的 `Request` 傳入該參數。

/// tip

注意在這個例子中，除了 request 參數之外，我們也宣告了一個路徑參數。

因此，路徑參數會被擷取、驗證、轉換為指定型別，並在 OpenAPI 中加入標註。

同理，你可以照常宣告其他參數，並另外同時取得 `Request`。

///

## `Request` 文件 { #request-documentation }

你可以在 <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">Starlette 官方文件站點中的 `Request` 物件</a> 了解更多細節。

/// note | 技術細節

你也可以使用 `from starlette.requests import Request`。

FastAPI 之所以直接提供它，是為了讓開發者更方便；但它本身是來自 Starlette。

///
