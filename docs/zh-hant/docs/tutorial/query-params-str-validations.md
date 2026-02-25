# 查詢參數與字串驗證 { #query-parameters-and-string-validations }

FastAPI 允許你為參數宣告額外的資訊與驗證。

以下面這個應用為例：

{* ../../docs_src/query_params_str_validations/tutorial001_py310.py hl[7] *}

查詢參數 `q` 的型別是 `str | None`，表示它是 `str` 但也可以是 `None`，而且預設值就是 `None`，因此 FastAPI 會知道它不是必填。

/// note | 注意

FastAPI 會因為預設值是 `= None` 而知道 `q` 不是必填。

使用 `str | None` 也能讓你的編輯器提供更好的支援並偵測錯誤。

///

## 額外驗證 { #additional-validation }

我們要強制：即使 `q` 是可選，只要提供了，長度就不能超過 50 個字元。

### 匯入 `Query` 與 `Annotated` { #import-query-and-annotated }

要達成這點，先匯入：

- 從 `fastapi` 匯入 `Query`
- 從 `typing` 匯入 `Annotated`

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[1,3] *}

/// info | 說明

FastAPI 自 0.95.0 版起加入並開始推薦使用 `Annotated`。

如果你的版本較舊，嘗試使用 `Annotated` 會出錯。

請先至少 [升級 FastAPI 版本](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank} 到 0.95.1 再使用 `Annotated`。

///

## 在 `q` 參數的型別中使用 `Annotated` { #use-annotated-in-the-type-for-the-q-parameter }

還記得先前在 [Python 型別介紹](../python-types.md#type-hints-with-metadata-annotations){.internal-link target=_blank} 提到可以用 `Annotated` 為參數加入中繼資料嗎？

現在就用在 FastAPI 上吧。🚀

我們原本的型別註記是：

```Python
q: str | None = None
```

接著把它用 `Annotated` 包起來，變成：

```Python
q: Annotated[str | None] = None
```

這兩種寫法代表的意思相同：`q` 可以是 `str` 或 `None`，且預設是 `None`。

現在來做有趣的部分。🎉

## 在 `q` 參數的 `Annotated` 中加入 `Query` { #add-query-to-annotated-in-the-q-parameter }

既然我們有可以放更多資訊的 `Annotated`（在此是額外驗證），就把 `Query` 放進 `Annotated`，並把參數 `max_length` 設為 `50`：

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[9] *}

注意預設值仍然是 `None`，所以這個參數仍是可選。

不過，現在在 `Annotated` 裡有 `Query(max_length=50)`，我們就告訴 FastAPI 要對這個值做「額外驗證」，最多 50 個字元即可。😎

/// tip | 提示

這裡用的是 `Query()`，因為這是「查詢參數」。稍後你會看到 `Path()`、`Body()`、`Header()`、`Cookie()` 等，它們也接受與 `Query()` 相同的參數。

///

FastAPI 現在會：

- 驗證資料，確保長度最多 50 個字元
- 當資料不合法時，回給用戶端清楚的錯誤
- 在 OpenAPI 的路徑操作中文件化該參數（因此會出現在自動文件 UI）

## 替代方式（舊）：將 `Query` 作為預設值 { #alternative-old-query-as-the-default-value }

舊版 FastAPI（<dfn title="2023-03 之前">0.95.0</dfn> 以前）需要把 `Query` 當成參數的預設值，而不是放在 `Annotated` 裡。你很可能會在各處看到這種寫法，所以我也會說明一下。

/// tip | 提示

新程式碼且在可能的情況下，請依上面說明使用 `Annotated`。它有多項優點（如下所述），而沒有缺點。🍰

///

這是把 `Query()` 作為函式參數預設值的寫法，並把參數 `max_length` 設為 50：

{* ../../docs_src/query_params_str_validations/tutorial002_py310.py hl[7] *}

在這種情況下（未使用 `Annotated`），我們必須用 `Query()` 取代函式中的預設值 `None`，因此需要用 `Query(default=None)` 來設定預設值；對 FastAPI 而言，這達到相同目的。

所以：

```Python
q: str | None = Query(default=None)
```

…會讓參數變為可選、預設值是 `None`，等同於：

```Python
q: str | None = None
```

但用 `Query` 的版本會明確宣告它是查詢參數。

接著，我們可以傳更多參數給 `Query`。此例中是用於字串的 `max_length` 參數：

```Python
q: str | None = Query(default=None, max_length=50)
```

這一樣會驗證資料、在資料不合法時顯示清楚錯誤，並在 OpenAPI 的路徑操作中文件化該參數。

### 將 `Query` 作為預設值或放在 `Annotated` 中 { #query-as-the-default-value-or-in-annotated }

注意，把 `Query` 放在 `Annotated` 內時，不能使用 `Query` 的 `default` 參數。

請改用函式參數的實際預設值。否則會不一致。

例如，這是不允許的：

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

…因為不清楚預設值到底該是 `"rick"` 還是 `"morty"`。

因此，你可以（且更推薦）這樣寫：

```Python
q: Annotated[str, Query()] = "rick"
```

…或在較舊的程式碼中你會看到：

```Python
q: str = Query(default="rick")
```

### `Annotated` 的優點 { #advantages-of-annotated }

建議使用 `Annotated`，而不是在函式參數上使用（舊式的）預設值寫法，理由很多，且更好。🤓

函式參數的「預設值」就是「實際的預設值」，這在 Python 的直覺上更一致。😌

你也可以在沒有 FastAPI 的其他地方「直接呼叫」同一個函式，而且能「如預期」運作。若有「必填」參數（沒有預設值），你的「編輯器」會提示錯誤，「Python」在執行時也會抱怨你未傳遞必填參數。

若不使用 `Annotated`、改用「（舊式）預設值」寫法，你在沒有 FastAPI 的「其他地方」呼叫該函式時，就得「記得」傳入正確參數，否則值會和預期不同（例如會得到 `QueryInfo` 或類似的東西，而不是 `str`）。你的編輯器不會提示，Python 執行該函式時也不會抱怨，只有在內部操作失敗時才會出錯。

因為 `Annotated` 可以有多個中繼資料註解，你甚至可以用同一個函式配合其他工具，例如 <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a>。🚀

## 加入更多驗證 { #add-more-validations }

你也可以加入 `min_length` 參數：

{* ../../docs_src/query_params_str_validations/tutorial003_an_py310.py hl[10] *}

## 加入正規表示式 { #add-regular-expressions }

你可以定義參數必須符合的 <dfn title="正規表示式（regex、regexp）是一組用於定義字串搜尋樣式的字元序列。">regular expression</dfn> `pattern`：

{* ../../docs_src/query_params_str_validations/tutorial004_an_py310.py hl[11] *}

這個特定的正規表示式樣式會檢查收到的參數值是否：

- `^`：以後續的字元開頭，前面不能有其他字元。
- `fixedquery`：必須正好等於 `fixedquery`。
- `$`：在此結束，`fixedquery` 後面不能再有其他字元。

如果你對「正規表示式」感到困惑，別擔心。這對很多人來說都不容易。你仍然可以先不使用正規表示式就完成很多事情。

現在你知道，當你需要它們時，可以在 FastAPI 中使用它們。

## 預設值 { #default-values }

當然，你可以使用 `None` 以外的預設值。

假設你想宣告查詢參數 `q` 的 `min_length` 是 `3`，且預設值是 `"fixedquery"`：

{* ../../docs_src/query_params_str_validations/tutorial005_an_py310.py hl[9] *}

/// note | 注意

只要有任何型別的預設值（包含 `None`），參數就是可選（非必填）。

///

## 必填參數 { #required-parameters }

當我們不需要宣告更多的驗證或中繼資料時，只要不提供預設值，就能讓查詢參數 `q` 成為必填，例如：

```Python
q: str
```

而不是：

```Python
q: str | None = None
```

但現在我們要搭配 `Query` 來宣告，例如：

```Python
q: Annotated[str | None, Query(min_length=3)] = None
```

因此，在使用 `Query` 時若要宣告值為必填，只要不要宣告預設值即可：

{* ../../docs_src/query_params_str_validations/tutorial006_an_py310.py hl[9] *}

### 必填，但可為 `None` { #required-can-be-none }

你可以宣告參數可以接受 `None`，但仍然是必填。這會強制用戶端一定要送出一個值，即使該值是 `None`。

要做到這點，你可以宣告 `None` 是合法型別，但不要宣告預設值：

{* ../../docs_src/query_params_str_validations/tutorial006c_an_py310.py hl[9] *}

## 查詢參數清單／多個值 { #query-parameter-list-multiple-values }

當你用 `Query` 明確定義查詢參數時，也可以讓它接收一個值的清單；換句話說，就是「多個值」。

例如，要宣告查詢參數 `q` 可以在 URL 中出現多次，你可以這樣寫：

{* ../../docs_src/query_params_str_validations/tutorial011_an_py310.py hl[9] *}

若使用這樣的 URL：

```
http://localhost:8000/items/?q=foo&q=bar
```

你會在路徑操作函式的參數 `q` 中，收到多個 `q` 查詢參數的值（`foo` 與 `bar`），以 Python 的 `list` 形式。

因此，對該 URL 的回應會是：

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | 提示

要宣告型別為 `list` 的查詢參數（如上例），需要明確使用 `Query`，否則它會被解讀為請求本文。

///

互動式 API 文件也會相應更新，以便支援多個值：

<img src="/img/tutorial/query-params-str-validations/image02.png">

### 查詢參數清單／多個值的預設值 { #query-parameter-list-multiple-values-with-defaults }

也可以在未提供任何值時，定義 `list` 型別的預設值：

{* ../../docs_src/query_params_str_validations/tutorial012_an_py310.py hl[9] *}

如果你前往：

```
http://localhost:8000/items/
```

`q` 的預設值會是：`["foo", "bar"]`，而回應會是：

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### 只使用 `list` { #using-just-list }

你也可以直接使用 `list`，而不是 `list[str]`：

{* ../../docs_src/query_params_str_validations/tutorial013_an_py310.py hl[9] *}

/// note | 注意

注意，在這種情況下，FastAPI 不會檢查清單的內容。

例如，`list[int]` 會檢查（並文件化）清單內容為整數；但單獨使用 `list` 則不會。

///

## 宣告更多中繼資料 { #declare-more-metadata }

你可以為參數加入更多資訊。

這些資訊會被包含在產生的 OpenAPI 中，供文件 UI 與外部工具使用。

/// note | 注意

請留意，不同工具對 OpenAPI 的支援程度可能不同。

有些工具可能暫時還不會顯示所有額外資訊；不過多半這些缺漏功能已在開發規劃中。

///

你可以加入 `title`：

{* ../../docs_src/query_params_str_validations/tutorial007_an_py310.py hl[10] *}

以及 `description`：

{* ../../docs_src/query_params_str_validations/tutorial008_an_py310.py hl[14] *}

## 別名參數 { #alias-parameters }

想像你希望參數名稱是 `item-query`。

像這樣：

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

但 `item-query` 不是合法的 Python 變數名稱。

最接近的大概是 `item_query`。

但你仍然需要它就是 `item-query`...

那你可以宣告一個 `alias`，實際上就會用這個別名來讀取參數值：

{* ../../docs_src/query_params_str_validations/tutorial009_an_py310.py hl[9] *}

## 棄用參數 { #deprecating-parameters }

現在假設你不再喜歡這個參數了。

你必須暫時保留它，因為還有用戶端在用，但你希望文件能清楚標示它是<dfn title="過時，不建議使用">已棄用</dfn>。

接著把參數 `deprecated=True` 傳給 `Query`：

{* ../../docs_src/query_params_str_validations/tutorial010_an_py310.py hl[19] *}

文件會這樣顯示：

<img src="/img/tutorial/query-params-str-validations/image01.png">

## 從 OpenAPI 排除參數 { #exclude-parameters-from-openapi }

若要把某個查詢參數從產生的 OpenAPI（以及自動文件系統）中排除，將 `Query` 的 `include_in_schema` 設為 `False`：

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}

## 自訂驗證 { #custom-validation }

有時你需要做一些上述參數無法處理的「自訂驗證」。

這種情況下，你可以使用「自訂驗證函式」，它會在一般驗證之後套用（例如先確認值是 `str` 之後）。

你可以在 `Annotated` 中使用 <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-after-validator" class="external-link" target="_blank">Pydantic 的 `AfterValidator`</a> 來達成。

/// tip | 提示

Pydantic 也有 <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-before-validator" class="external-link" target="_blank">`BeforeValidator`</a> 等等。🤓

///

例如，以下自訂驗證器會檢查項目 ID 是否以 `isbn-` 開頭（<abbr title="International Standard Book Number - 國際標準書號">ISBN</abbr> 書籍編號），或以 `imdb-` 開頭（<abbr title="Internet Movie Database - 互聯網電影資料庫: 含有電影資訊的網站">IMDB</abbr> 電影 URL 的 ID）：

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py hl[5,16:19,24] *}

/// info | 說明

這需搭配 Pydantic 2 或以上版本。😎

///

/// tip | 提示

如果你需要做任何需要與「外部元件」溝通的驗證（例如資料庫或其他 API），應該改用「FastAPI 依賴」（FastAPI Dependencies），你稍後會學到。

這些自訂驗證器適用於只需使用請求中「同一份資料」即可完成的檢查。

///

### 理解這段程式碼 { #understand-that-code }

重點就是在 `Annotated` 中使用「`AfterValidator` 搭配函式」。如果你願意，可以略過這一節。🤸

---

但如果你對這個範例感到好奇且仍有興致，以下是一些額外細節。

#### 使用 `value.startswith()` 的字串 { #string-with-value-startswith }

你注意到了嗎？字串的 `value.startswith()` 可以接收一個 tuple，並逐一檢查 tuple 中的每個值：

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[16:19] hl[17] *}

#### 隨機項目 { #a-random-item }

透過 `data.items()` 我們會得到一個包含每個字典項目鍵值對 tuple 的 <dfn title="可以用 for 迴圈遍歷的東西，例如 list、set 等等。">iterable object</dfn>。

我們用 `list(data.items())` 把這個可疊代物件轉成正式的 `list`。

接著用 `random.choice()` 從清單中取得一個「隨機值」，也就是一個 `(id, name)` 的 tuple。可能像是 `("imdb-tt0371724", "The Hitchhiker's Guide to the Galaxy")`。

然後把這個 tuple 的兩個值分別指定給變數 `id` 和 `name`。

因此，即使使用者沒有提供 item ID，仍然會收到一個隨機建議。

……而這全部只用一行簡單的程式碼完成。🤯 你不愛 Python 嗎？🐍

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[22:30] hl[29] *}

## 重點回顧 { #recap }

你可以為參數宣告額外的驗證與中繼資料。

通用的驗證與中繼資料：

- `alias`
- `title`
- `description`
- `deprecated`

字串專用的驗證：

- `min_length`
- `max_length`
- `pattern`

使用 `AfterValidator` 的自訂驗證。

在這些範例中，你看到了如何為 `str` 值宣告驗證。

接下來的章節會示範如何為其他型別（像是數字）宣告驗證。
