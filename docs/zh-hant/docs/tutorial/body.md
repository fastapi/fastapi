# 請求本文 { #request-body }

當你需要從用戶端（例如瀏覽器）將資料傳送到你的 API 時，會把它作為**請求本文**送出。

**請求**本文是用戶端傳給你的 API 的資料。**回應**本文是你的 API 傳回給用戶端的資料。

你的 API 幾乎總是需要傳回**回應**本文。但用戶端不一定每次都要送出**請求本文**，有時只會請求某個路徑，可能帶一些查詢參數，但不會傳送本文。

要宣告**請求**本文，你會使用 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> 模型，享受其完整的功能與優點。

/// info

要傳送資料，應使用下列其中一種方法：`POST`（最常見）、`PUT`、`DELETE` 或 `PATCH`。

在規範中，於 `GET` 請求中攜帶本文的行為是未定義的。不過，FastAPI 仍支援它，但僅適用於非常複雜／極端的情境。

由於不建議這麼做，使用 Swagger UI 的互動式文件在使用 `GET` 時不會顯示本文的文件，而且中間的代理伺服器也可能不支援。

///

## 匯入 Pydantic 的 `BaseModel` { #import-pydantics-basemodel }

首先，從 `pydantic` 匯入 `BaseModel`：

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## 建立你的資料模型 { #create-your-data-model }

接著，你將資料模型宣告為繼承自 `BaseModel` 的類別。

對所有屬性使用標準的 Python 型別：

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}

就和宣告查詢參數時一樣，當模型屬性有預設值時，它就不是必填；否則就是必填。使用 `None` 可使其成為選填。

例如，上述模型對應的 JSON「`object`」（或 Python `dict`）如下：

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...由於 `description` 與 `tax` 是選填（預設為 `None`），以下這個 JSON「`object`」也有效：

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## 將它宣告為參數 { #declare-it-as-a-parameter }

要把它加到你的*路徑操作（path operation）*中，宣告方式與路徑與查詢參數相同：

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

...並將其型別宣告為你建立的模型 `Item`。

## 效果 { #results }

只靠這樣的 Python 型別宣告，**FastAPI** 會：

- 將請求本文讀取為 JSON。
- （必要時）轉換為對應的型別。
- 驗證資料。
    - 若資料無效，會回傳清楚易懂的錯誤，指出哪裡、哪筆資料不正確。
- 把接收到的資料放在參數 `item` 中提供給你。
    - 由於你在函式中將其宣告為 `Item` 型別，你也會獲得完整的編輯器支援（自動完成等）以及所有屬性與其型別。
- 為你的模型產生 <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> 定義，如有需要，你也可以在專案中的其他地方使用。
- 這些 schema 會成為產生的 OpenAPI schema 的一部分，並由自動文件 <abbr title="User Interfaces - 使用者介面">UIs</abbr> 使用。

## 自動文件 { #automatic-docs }

你的模型的 JSON Schema 會納入產生的 OpenAPI schema，並顯示在互動式 API 文件中：

<img src="/img/tutorial/body/image01.png">

也會用於每個需要它們的*路徑操作*內的 API 文件：

<img src="/img/tutorial/body/image02.png">

## 編輯器支援 { #editor-support }

在編輯器裡、於你的函式中，你會在各處獲得型別提示與自動完成（如果你接收的是 `dict` 而不是 Pydantic 模型，就不會有這些）：

<img src="/img/tutorial/body/image03.png">

你也會獲得對不正確型別操作的錯誤檢查：

<img src="/img/tutorial/body/image04.png">

這不是偶然，整個框架就是圍繞這個設計而建。

而且在實作之前的設計階段就已徹底測試，確保能在各種編輯器中運作良好。

甚至為了支援這點，Pydantic 本身也做了些修改。

前面的螢幕截圖是使用 <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a> 拍的。

但你在 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> 與大多數其它 Python 編輯器中也會得到相同的編輯器支援：

<img src="/img/tutorial/body/image05.png">

/// tip

如果你使用 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> 作為編輯器，可以安裝 <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a>。

它能增強 Pydantic 模型的編輯器支援，包含：

- 自動完成
- 型別檢查
- 重構
- 搜尋
- 程式碼檢查

///

## 使用該模型 { #use-the-model }

在函式內，你可以直接存取模型物件的所有屬性：

{* ../../docs_src/body/tutorial002_py310.py *}

## 請求本文 + 路徑參數 { #request-body-path-parameters }

你可以同時宣告路徑參數與請求本文。

**FastAPI** 會辨識出與路徑參數相符的函式參數應該從**路徑**取得，而宣告為 Pydantic 模型的函式參數應該從**請求本文**取得。

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}

## 請求本文 + 路徑 + 查詢參數 { #request-body-path-query-parameters }

你也可以同時宣告**本文**、**路徑**與**查詢**參數。

**FastAPI** 會分別辨識並從正確的位置取得資料。

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

函式參數的辨識方式如下：

- 如果參數同時在**路徑**中宣告，則作為路徑參數。
- 如果參數是**單一型別**（像是 `int`、`float`、`str`、`bool` 等），會被視為**查詢**參數。
- 如果參數宣告為 **Pydantic 模型** 型別，會被視為請求**本文**。

/// note

FastAPI 會因為預設值 `= None` 而知道 `q` 的值不是必填。

`str | None` 並非 FastAPI 用來判斷是否必填的依據；它會因為有預設值 `= None` 而知道不是必填。

但加入這些型別註解能讓你的編輯器提供更好的支援與錯誤偵測。

///

## 不使用 Pydantic { #without-pydantic }

若你不想使用 Pydantic 模型，也可以使用 **Body** 參數。請參考[Body - 多個參數：本文中的單一值](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}。
