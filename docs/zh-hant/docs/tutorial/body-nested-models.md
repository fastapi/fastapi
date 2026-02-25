# Body - 巢狀模型 { #body-nested-models }

使用 **FastAPI**，你可以定義、驗證、文件化，並使用任意深度的巢狀模型（感謝 Pydantic）。

## 列表欄位 { #list-fields }

你可以將屬性定義為某個子型別。例如，Python 的 `list`：

{* ../../docs_src/body_nested_models/tutorial001_py310.py hl[12] *}

這會讓 `tags` 成為一個列表，儘管尚未宣告列表元素的型別。

## 具有型別參數的列表欄位 { #list-fields-with-type-parameter }

不過，Python 有一種專門的方式來宣告具有內部型別（「型別參數」）的列表：

### 宣告帶有型別參數的 `list` { #declare-a-list-with-a-type-parameter }

要宣告具有型別參數（內部型別）的型別，例如 `list`、`dict`、`tuple`，使用方括號 `[` 與 `]` 傳入內部型別作為「型別參數」：

```Python
my_list: list[str]
```

以上都是標準的 Python 型別宣告語法。

對於具有內部型別的模型屬性，也使用相同的標準語法。

因此，在我們的範例中，可以讓 `tags` 明確成為「字串的列表」：

{* ../../docs_src/body_nested_models/tutorial002_py310.py hl[12] *}

## 集合型別 { #set-types }

但進一步思考後，我們會意識到 `tags` 不應該重覆，應該是唯一的字串。

而 Python 有一種用於唯一元素集合的特殊資料型別：`set`。

因此我們可以將 `tags` 宣告為字串的 `set`：

{* ../../docs_src/body_nested_models/tutorial003_py310.py hl[12] *}

這樣一來，即使收到包含重覆資料的請求，也會被轉換為由唯一元素組成的 `set`。

之後只要輸出該資料，即使來源有重覆，也會以唯一元素的 `set` 輸出。

並且也會在註解／文件中相應標示。

## 巢狀模型 { #nested-models }

每個 Pydantic 模型的屬性都有型別。

而該型別本身也可以是另一個 Pydantic 模型。

因此，你可以宣告具有特定屬性名稱、型別與驗證的深度巢狀 JSON「物件」。

而且可以任意深度巢狀。

### 定義子模型 { #define-a-submodel }

例如，我們可以定義一個 `Image` 模型：

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[7:9] *}

### 將子模型作為型別使用 { #use-the-submodel-as-a-type }

然後把它作為某個屬性的型別使用：

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[18] *}

這表示 **FastAPI** 會期望一個類似如下的本文：

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

只需進行上述宣告，使用 **FastAPI** 你就能獲得：

- 編輯器支援（自動完成等），即使是巢狀模型
- 資料轉換
- 資料驗證
- 自動產生文件

## 特殊型別與驗證 { #special-types-and-validation }

除了 `str`、`int`、`float` 等一般的單一型別外，你也可以使用繼承自 `str` 的更複雜單一型別。

若要查看所有可用選項，請參閱 <a href="https://docs.pydantic.dev/latest/concepts/types/" class="external-link" target="_blank">Pydantic 的型別總覽</a>。你會在下一章看到一些範例。

例如，在 `Image` 模型中有一個 `url` 欄位，我們可以將其宣告為 Pydantic 的 `HttpUrl`，而不是 `str`：

{* ../../docs_src/body_nested_models/tutorial005_py310.py hl[2,8] *}

該字串會被檢查是否為有效的 URL，並在 JSON Schema / OpenAPI 中相應註記。

## 具有子模型列表的屬性 { #attributes-with-lists-of-submodels }

你也可以將 Pydantic 模型作為 `list`、`set` 等的子型別使用：

{* ../../docs_src/body_nested_models/tutorial006_py310.py hl[18] *}

這會期望（並進行轉換、驗證、文件化等）如下的 JSON 本文：

```JSON hl_lines="11"
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
```

/// info

注意 `images` 鍵現在是一個由 image 物件組成的列表。

///

## 深度巢狀模型 { #deeply-nested-models }

你可以定義任意深度的巢狀模型：

{* ../../docs_src/body_nested_models/tutorial007_py310.py hl[7,12,18,21,25] *}

/// info

請注意，`Offer` 具有一個 `Item` 的列表，而每個 `Item` 又有一個可選的 `Image` 列表。

///

## 純列表的本文 { #bodies-of-pure-lists }

如果你期望的 JSON 本文頂層值是一個 JSON `array`（Python 的 `list`），可以像在 Pydantic 模型中那樣，直接在函式參數上宣告其型別：

```Python
images: list[Image]
```

如下所示：

{* ../../docs_src/body_nested_models/tutorial008_py310.py hl[13] *}

## 隨處可得的編輯器支援 { #editor-support-everywhere }

你將在各處獲得編輯器支援。

即使是列表中的項目也一樣：

<img src="/img/tutorial/body-nested-models/image01.png">

若直接操作 `dict` 而不是使用 Pydantic 模型，就無法獲得這種等級的編輯器支援。

但你也不必擔心，傳入的 dict 會自動被轉換，而你的輸出也會自動轉換為 JSON。

## 任意 `dict` 的本文 { #bodies-of-arbitrary-dicts }

你也可以將本文宣告為一個 `dict`，其鍵為某種型別、值為另一種型別。

如此一來，你無需事先知道有效的欄位／屬性名稱為何（不像使用 Pydantic 模型時需要）。

這在你想接收尚未預知的鍵時很有用。

---

另一個實用情境是當你希望鍵是其他型別（例如，`int`）時。

這正是我們在此要示範的。

在此情況下，只要是擁有 `int` 鍵且對應 `float` 值的 `dict` 都會被接受：

{* ../../docs_src/body_nested_models/tutorial009_py310.py hl[7] *}

/// tip

請記住，JSON 只支援 `str` 作為鍵。

但 Pydantic 具有自動資料轉換。

這表示即使你的 API 用戶端只能以字串作為鍵，只要這些字串是純整數，Pydantic 會自動轉換並驗證它們。

而你作為 `weights` 所接收的 `dict`，實際上會擁有 `int` 鍵與 `float` 值。

///

## 總結 { #recap }

使用 **FastAPI**，你在保持程式碼簡潔優雅的同時，亦可擁有 Pydantic 模型所提供的高度彈性。

同時還具備以下優點：

- 編輯器支援（到處都有自動完成！）
- 資料轉換（亦即 parsing／serialization）
- 資料驗證
- 結構描述（Schema）文件
- 自動產生文件
