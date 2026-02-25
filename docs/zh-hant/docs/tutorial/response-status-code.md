# 回應狀態碼 { #response-status-code }

就像你可以指定回應模型一樣，你也可以在任一個「路徑操作（path operation）」的參數 `status_code` 中宣告回應所使用的 HTTP 狀態碼：

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* 等等

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

/// note | 注意

請注意，`status_code` 是「裝飾器（decorator）」方法（`get`、`post` 等等）的參數，而不是你的「路徑操作函式」的參數，就像所有的參數與 body 一樣。

///

參數 `status_code` 接受一個數字作為 HTTP 狀態碼。

/// info | 資訊

`status_code` 也可以接收一個 `IntEnum`，例如 Python 的 <a href="https://docs.python.org/3/library/http.html#http.HTTPStatus" class="external-link" target="_blank">`http.HTTPStatus`</a>。

///

它會：

* 在回應中傳回該狀態碼。
* 在 OpenAPI 結構中如此記錄（因此也會反映在使用者介面中）：

<img src="/img/tutorial/response-status-code/image01.png">

/// note | 注意

有些回應碼（見下一節）表示回應不包含本文（body）。

FastAPI 知道這點，並會產生聲明「無回應本文」的 OpenAPI 文件。

///

## 關於 HTTP 狀態碼 { #about-http-status-codes }

/// note | 注意

如果你已經知道什麼是 HTTP 狀態碼，可以直接跳到下一節。

///

在 HTTP 中，你會在回應的一部分傳回 3 位數的狀態碼。

這些狀態碼有對應的名稱以便辨識，但重點是數字本身。

簡而言之：

* `100 - 199` 表示「資訊」。你很少會直接使用它們。這些狀態碼的回應不可包含本文。
* **`200 - 299`** 表示「成功」。這是你最常使用的一組。
    * `200` 是預設狀態碼，表示一切「OK」。
    * 另一個例子是 `201`，代表「已建立」。常用於在資料庫中建立新紀錄之後。
    * 一個特殊情況是 `204`，代表「無內容」。當沒有內容要回傳給用戶端時使用，因此回應不得有本文。
* **`300 - 399`** 表示「重新導向」。這些狀態碼的回應可能有或沒有本文，唯獨 `304`（「未修改」）必須沒有本文。
* **`400 - 499`** 表示「用戶端錯誤」。這大概是你第二常用的一組。
    * 例如 `404`，代表「找不到」。
    * 對於一般性的用戶端錯誤，你可以使用 `400`。
* `500 - 599` 表示伺服器錯誤。你幾乎不會直接使用它們。當你的應用程式或伺服器某處出錯時，會自動回傳其中一個狀態碼。

/// tip | 提示

想深入瞭解各狀態碼與其用途，請參考 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status" class="external-link" target="_blank"><abbr title="Mozilla Developer Network - Mozilla 開發者網路">MDN</abbr> 關於 HTTP 狀態碼的文件</a>。

///

## 快速記住名稱 { #shortcut-to-remember-the-names }

再看一次前面的範例：

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

`201` 是「已建立（Created）」的狀態碼。

但你不需要背下每個代碼代表什麼。

你可以使用 `fastapi.status` 提供的便利變數。

{* ../../docs_src/response_status_code/tutorial002_py310.py hl[1,6] *}

它們只是方便用的常數，值與數字相同，但這樣你可以用編輯器的自動完成來找到它們：

<img src="/img/tutorial/response-status-code/image02.png">

/// note | 技術細節

你也可以使用 `from starlette import status`。

**FastAPI** 將同一個 `starlette.status` 以 `fastapi.status` 形式提供，純粹是為了讓你（開發者）方便。但它直接來自 Starlette。

///

## 變更預設值 { #changing-the-default }

稍後在 [進階使用者指南](../advanced/response-change-status-code.md){.internal-link target=_blank} 中，你會看到如何回傳一個不同於此處所宣告預設值的狀態碼。
