# Body - 多個參數 { #body-multiple-parameters }

現在我們已經知道如何使用 `Path` 與 `Query`，接下來看看更進階的請求主體（request body）宣告用法。

## 混用 `Path`、`Query` 與 Body 參數 { #mix-path-query-and-body-parameters }

首先，當然你可以自由混用 `Path`、`Query` 與請求 Body 參數的宣告，**FastAPI** 會知道該怎麼做。

你也可以將 Body 參數宣告為可選，方法是將預設值設為 `None`：

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

/// note | 注意

請注意，在此情況下，從 body 取得的 `item` 是可選的，因為它的預設值是 `None`。

///

## 多個 Body 參數 { #multiple-body-parameters }

在前一個範例中，路徑操作（path operation）會期望一個包含 `Item` 屬性的 JSON 主體，例如：

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

但你也可以宣告多個 Body 參數，例如 `item` 與 `user`：

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}

在此情況下，**FastAPI** 會注意到函式中有多個 Body 參數（有兩個參數是 Pydantic 模型）。

因此，它會使用參數名稱作為 body 中的鍵（欄位名稱），並期望如下的主體：

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

/// note | 注意

儘管 `item` 的宣告方式與先前相同，現在預期它會位於 body 內，且鍵為 `item`。

///

**FastAPI** 會自動從請求中進行轉換，讓參數 `item` 收到對應內容，`user` 亦同。

它會對複合資料進行驗證，並在 OpenAPI 結構與自動文件中如此描述。

## Body 中的單一值 { #singular-values-in-body }

就像你可以用 `Query` 與 `Path` 為查詢與路徑參數定義額外資訊一樣，**FastAPI** 也提供對應的 `Body`。

例如，延伸前述模型，你可以決定在相同的 Body 中，除了 `item` 與 `user` 外，還要有另一個鍵 `importance`。

如果直接這樣宣告，因為它是單一值，**FastAPI** 會將其視為查詢參數。

但你可以使用 `Body` 指示 **FastAPI** 將其視為另一個 Body 鍵：

{* ../../docs_src/body_multiple_params/tutorial003_an_py310.py hl[23] *}

在此情況下，**FastAPI** 會期望如下的主體：

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
```

同樣地，它會進行型別轉換、驗證、文件化等。

## 多個 Body 參數與 Query { #multiple-body-params-and-query }

當然，你也可以在任何 Body 參數之外，視需要宣告額外的查詢參數。

由於預設情況下，單一值會被解讀為查詢參數，你不必明確使用 `Query`，直接這樣寫即可：

```Python
q: str | None = None
```

例如：

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[28] *}

/// info | 注意

`Body` 也具有與 `Query`、`Path` 以及之後你會看到的其他工具相同的額外驗證與中繼資料參數。

///

## 嵌入單一 Body 參數 { #embed-a-single-body-parameter }

假設你只有一個來自 Pydantic 模型 `Item` 的單一 `item` Body 參數。

預設情況下，**FastAPI** 會直接期望該模型的內容作為請求主體。

但如果你想讓它像宣告多個 Body 參數時那樣，期望一個帶有 `item` 鍵、其內含模型內容的 JSON，你可以使用 `Body` 的特殊參數 `embed`：

```Python
item: Item = Body(embed=True)
```

如下：

{* ../../docs_src/body_multiple_params/tutorial005_an_py310.py hl[17] *}

在此情況下 **FastAPI** 會期望如下的主體：

```JSON hl_lines="2"
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

而不是：

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## 小結 { #recap }

即便一個請求只能有單一主體，你仍可在你的路徑操作函式中宣告多個 Body 參數。

但 **FastAPI** 會處理好這一切，在你的函式中提供正確的資料，並在路徑操作中驗證與文件化正確的結構。

你也可以將單一值宣告為 Body 的一部分來接收。

即使只宣告了一個參數，也可以指示 **FastAPI** 將 Body 以某個鍵進行嵌入。
