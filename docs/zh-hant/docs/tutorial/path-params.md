# 路徑參數 { #path-parameters }

你可以用與 Python 格式化字串相同的語法來宣告路徑「參數」或「變數」：

{* ../../docs_src/path_params/tutorial001_py310.py hl[6:7] *}

路徑參數 `item_id` 的值會作為引數 `item_id` 傳入你的函式。

所以，如果你執行這個範例並前往 <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>，你會看到這樣的回應：

```JSON
{"item_id":"foo"}
```

## 具型別的路徑參數 { #path-parameters-with-types }

你可以在函式中使用標準的 Python 型別註記為路徑參數宣告型別：

{* ../../docs_src/path_params/tutorial002_py310.py hl[7] *}

在這個例子裡，`item_id` 被宣告為 `int`。

/// check

這會在你的函式中提供編輯器支援，包括錯誤檢查、自動完成等。

///

## 資料 <dfn title="也稱為：序列化、解析、封送">轉換</dfn> { #data-conversion }

如果你執行這個範例並在瀏覽器開啟 <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a>，你會看到這樣的回應：

```JSON
{"item_id":3}
```

/// check

注意你的函式接收（並回傳）的值是 `3`，也就是 Python 的 `int`，而不是字串 `"3"`。

因此，有了這個型別宣告，**FastAPI** 會自動為你處理請求的 <dfn title="將 HTTP 請求中的字串轉換為 Python 資料">「解析」</dfn>。

///

## 資料驗證 { #data-validation }

但如果你在瀏覽器前往 <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>，你會看到漂亮的 HTTP 錯誤：

```JSON
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo"
    }
  ]
}
```

因為路徑參數 `item_id` 的值是 `"foo"`，它不是 `int`。

同樣的錯誤也會在你提供 `float` 而不是 `int` 時出現，例如：<a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

/// check

因此，搭配相同的 Python 型別宣告，**FastAPI** 會為你進行資料驗證。

注意錯誤也清楚指出驗證未通過的確切位置。

這在開發與除錯與你的 API 互動的程式碼時非常有幫助。

///

## 文件 { #documentation }

當你在瀏覽器開啟 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>，你會看到自動產生、可互動的 API 文件，例如：

<img src="/img/tutorial/path-params/image01.png">

/// check

同樣地，只要使用那個 Python 型別宣告，**FastAPI** 就會提供自動、互動式的文件（整合 Swagger UI）。

注意路徑參數被宣告為整數。

///

## 基於標準的優勢與替代文件 { #standards-based-benefits-alternative-documentation }

而且因為產生的 schema 來自 <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a> 標準，有很多相容的工具可用。

因此，**FastAPI** 本身也提供另一種 API 文件（使用 ReDoc），你可以在 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> 存取：

<img src="/img/tutorial/path-params/image02.png">

同樣地，也有許多相容工具可用，包括支援多種語言的程式碼產生工具。

## Pydantic { #pydantic }

所有資料驗證都由 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> 在底層處理，因此你能直接受惠。而且你可以放心使用。

你可以用相同的型別宣告搭配 `str`、`float`、`bool` 與許多更複雜的資料型別。

這些之中的好幾個會在接下來的教學章節中介紹。

## 順序很重要 { #order-matters }

在建立「路徑操作」時，你可能會遇到有固定路徑的情況。

像是 `/users/me`，假設它用來取得目前使用者的資料。

然後你也可能有一個路徑 `/users/{user_id}` 用來依使用者 ID 取得特定使用者的資料。

因為「路徑操作」會依宣告順序來比對，你必須確保 `/users/me` 的路徑在 `/users/{user_id}` 之前宣告：

{* ../../docs_src/path_params/tutorial003_py310.py hl[6,11] *}

否則，`/users/{user_id}` 的路徑也會匹配 `/users/me`，並「認為」它收到一個值為 `"me"` 的 `user_id` 參數。

同樣地，你不能重新定義同一路徑操作：

{* ../../docs_src/path_params/tutorial003b_py310.py hl[6,11] *}

因為第一個會被優先使用（路徑先匹配到）。

## 預先定義的值 { #predefined-values }

如果你有一個接收「路徑參數」的「路徑操作」，但你希望可用的「路徑參數」值是預先定義好的，你可以使用標準的 Python <abbr title="Enumeration - 列舉">`Enum`</abbr>。

### 建立 `Enum` 類別 { #create-an-enum-class }

匯入 `Enum` 並建立一個同時繼承自 `str` 與 `Enum` 的子類別。

繼承自 `str` 之後，API 文件就能知道這些值的型別必須是 `string`，並能正確地呈現。

然後建立具有固定值的類別屬性，這些就是可用的有效值：

{* ../../docs_src/path_params/tutorial005_py310.py hl[1,6:9] *}

/// tip

如果你在想，「AlexNet」、「ResNet」和「LeNet」只是一些機器學習 <dfn title="嚴格來說是深度學習的模型架構">模型</dfn> 的名字。

///

### 宣告一個「路徑參數」 { #declare-a-path-parameter }

接著使用你建立的列舉類別（`ModelName`）作為型別註記，建立一個「路徑參數」：

{* ../../docs_src/path_params/tutorial005_py310.py hl[16] *}

### 查看文件 { #check-the-docs }

因為「路徑參數」的可用值是預先定義的，互動式文件可以很漂亮地顯示它們：

<img src="/img/tutorial/path-params/image03.png">

### 使用 Python「列舉」 { #working-with-python-enumerations }

「路徑參數」的值會是一個「列舉成員」。

#### 比較「列舉成員」 { #compare-enumeration-members }

你可以把它與你建立的列舉 `ModelName` 中的「列舉成員」比較：

{* ../../docs_src/path_params/tutorial005_py310.py hl[17] *}

#### 取得「列舉值」 { #get-the-enumeration-value }

你可以用 `model_name.value` 取得實際的值（在這個例子中是 `str`），一般而言就是 `your_enum_member.value`：

{* ../../docs_src/path_params/tutorial005_py310.py hl[20] *}

/// tip

你也可以用 `ModelName.lenet.value` 取得值 `"lenet"`。

///

#### 回傳「列舉成員」 { #return-enumeration-members }

你可以從「路徑操作」回傳「列舉成員」，即使是巢狀在 JSON 主體（例如 `dict`）裡。

在回傳給用戶端之前，它們會被轉成對應的值（此例為字串）：

{* ../../docs_src/path_params/tutorial005_py310.py hl[18,21,23] *}

你的用戶端會收到像這樣的 JSON 回應：

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## 包含路徑的路徑參數 { #path-parameters-containing-paths }

假設你有一個路徑為 `/files/{file_path}` 的「路徑操作」。

但你需要 `file_path` 本身就包含一個「路徑」，像是 `home/johndoe/myfile.txt`。

所以，該檔案的 URL 會是：`/files/home/johndoe/myfile.txt`。

### OpenAPI 支援 { #openapi-support }

OpenAPI 並不支援直接宣告一個「路徑參數」內再包含一個「路徑」，因為那會導致難以測試與定義的情況。

然而，你仍可在 **FastAPI** 中這樣做，方法是使用 Starlette 的其中一個內部工具。

而文件依然能運作，只是它不會額外說明該參數應該包含一個路徑。

### 路徑轉換器 { #path-convertor }

使用 Starlette 提供的選項，你可以用像這樣的 URL 來宣告一個包含「路徑」的「路徑參數」：

```
/files/{file_path:path}
```

在這個例子裡，參數名稱是 `file_path`，而最後面的 `:path` 表示該參數應該匹配任意「路徑」。

所以你可以這樣使用它：

{* ../../docs_src/path_params/tutorial004_py310.py hl[6] *}

/// tip

你可能需要這個參數包含 `/home/johndoe/myfile.txt`，也就是前面帶有斜線（`/`）。

在那種情況下，URL 會是：`/files//home/johndoe/myfile.txt`，在 `files` 與 `home` 之間有兩個斜線（`//`）。

///

## 回顧 { #recap }

使用 **FastAPI**，只要撰寫簡短、直覺且標準的 Python 型別宣告，你就能獲得：

* 編輯器支援：錯誤檢查、自動完成等
* 資料 "<dfn title="將 HTTP 請求中的字串轉換為 Python 資料">解析</dfn>"
* 資料驗證
* API 註解與自動產生文件

而且你只要宣告一次就好。

這大概是 **FastAPI** 相較於其他框架最明顯的優勢之一（除了原始效能之外）。
