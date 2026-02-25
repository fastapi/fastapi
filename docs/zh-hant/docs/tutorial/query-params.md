# 查詢參數 { #query-parameters }

當你宣告不是路徑參數的其他函式參數時，會自動被視為「查詢（query）」參數。

{* ../../docs_src/query_params/tutorial001_py310.py hl[9] *}

查詢是出現在 URL 中 `?` 之後的一組鍵值對，以 `&` 字元分隔。

例如，URL：

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

...查詢參數為：

* `skip`：值為 `0`
* `limit`：值為 `10`

因為它們是 URL 的一部分，天生是字串。

但當你以 Python 型別宣告它們（如上例中的 `int`），它們會被轉換成該型別並據此驗證。

對於查詢參數，會套用與路徑參數相同的處理流程：

* 編輯器支援（當然）
* 資料 <dfn title="將來自 HTTP 請求的字串轉換為 Python 資料">「解析」</dfn>
* 資料驗證
* 自動文件

## 預設值 { #defaults }

由於查詢參數不是路徑的固定部分，因此可以是選填並具有預設值。

在上面的例子中，預設值為 `skip=0` 與 `limit=10`。

因此，造訪下列 URL：

```
http://127.0.0.1:8000/items/
```

等同於造訪：

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

但如果你改為造訪：

```
http://127.0.0.1:8000/items/?skip=20
```

函式中的參數值會是：

* `skip=20`：因為你在 URL 中設定了它
* `limit=10`：因為那是預設值

## 選用參數 { #optional-parameters }

同樣地，你可以將預設值設為 `None` 來宣告選用的查詢參數：

{* ../../docs_src/query_params/tutorial002_py310.py hl[7] *}

在這種情況下，函式參數 `q` 為選用，且預設為 `None`。

/// check | 注意

另外請注意，FastAPI 能辨識出路徑參數 `item_id` 是路徑參數，而 `q` 不是，因此 `q` 會被當作查詢參數。

///

## 查詢參數型別轉換 { #query-parameter-type-conversion }

你也可以宣告 `bool` 型別，值會被自動轉換：

{* ../../docs_src/query_params/tutorial003_py310.py hl[7] *}

在這種情況下，如果你造訪：

```
http://127.0.0.1:8000/items/foo?short=1
```

或

```
http://127.0.0.1:8000/items/foo?short=True
```

或

```
http://127.0.0.1:8000/items/foo?short=true
```

或

```
http://127.0.0.1:8000/items/foo?short=on
```

或

```
http://127.0.0.1:8000/items/foo?short=yes
```

或任何其他大小寫變化（全大寫、首字母大寫等），你的函式會將參數 `short` 視為 `bool` 值 `True`。否則為 `False`。

## 多個路徑與查詢參數 { #multiple-path-and-query-parameters }

你可以同時宣告多個路徑參數與查詢參數，FastAPI 會自動分辨。

而且不必按特定順序宣告。

會依名稱辨識：

{* ../../docs_src/query_params/tutorial004_py310.py hl[6,8] *}

## 必填查詢參數 { #required-query-parameters }

當你為非路徑參數（目前我們只看到查詢參數）宣告了預設值時，它就不是必填。

若你不想提供特定預設值、只想讓它為選填，將預設值設為 `None`。

但若你要讓查詢參數成為必填，只要不要宣告任何預設值：

{* ../../docs_src/query_params/tutorial005_py310.py hl[6:7] *}

此處查詢參數 `needy` 是必填的 `str`。

如果你在瀏覽器中開啟如下的 URL：

```
http://127.0.0.1:8000/items/foo-item
```

...沒有加上必填的 `needy` 參數，你會看到類似這樣的錯誤：

```JSON
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "needy"
      ],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

由於 `needy` 是必填參數，你需要在 URL 中設定它：

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

...這樣就會成功：

```JSON
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

當然，你可以同時定義部分參數為必填、部分有預設值、部分為選填：

{* ../../docs_src/query_params/tutorial006_py310.py hl[8] *}

在此例中，有 3 個查詢參數：

* `needy`，必填的 `str`。
* `skip`，具有預設值 `0` 的 `int`。
* `limit`，選填的 `int`。

/// tip | 提示

你也可以像在[路徑參數](path-params.md#predefined-values){.internal-link target=_blank}中一樣使用 `Enum`。

///
