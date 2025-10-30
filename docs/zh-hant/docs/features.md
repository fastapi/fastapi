# 特性

## FastAPI 特性

**FastAPI** 提供了以下内容：

### 建立在開放標準的基礎上

* 使用 <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> 來建立 API，包含<abbr title="path，也被叫做: endpoints, routes">路徑</abbr><abbr title="也叫做 HTTP 方法，例如 POST, GET, PUT, DELETE">操作</abbr>、參數、請求內文、安全性等聲明。
* 使用 <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a>（因為 OpenAPI 本身就是基於 JSON Schema）自動生成資料模型文件。
* 經過縝密的研究後圍繞這些標準進行設計，而不是事後在已有系統上附加的一層功能。
* 這也讓我們在多種語言中可以使用自動**用戶端程式碼生成**。

### 能夠自動生成文件

FastAPI 能生成互動式 API 文件和探索性的 Web 使用者介面。由於該框架基於 OpenAPI，因此有多種選擇，預設提供了兩種。

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a> 提供互動式探索，讓你可以直接從瀏覽器呼叫並測試你的 API 。

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a> 提供結構性的文件，讓你可以在瀏覽器中查看。

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)


### 現代 Python

這一切都基於標準的 **Python 型別**宣告（感謝 Pydantic）。無需學習新的語法，只需使用標準的現代 Python。

如果你需要 2 分鐘來學習如何使用 Python 型別（即使你不使用 FastAPI），可以看看這個簡短的教學：[Python 型別](python-types.md){.internal-link target=_blank}。

如果你寫帶有 Python 型別的程式碼：

```python
from datetime import date

from pydantic import BaseModel

# 宣告一個變數為 string
# 並在函式中獲得 editor support
def main(user_id: str):
    return user_id


# 宣告一個 Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```


可以像這樣來使用：

```python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```


/// info

`**second_user_data` 意思是:

將 `second_user_data` 字典直接作為 key-value 引數傳遞，等同於：`User(id=4, name="Mary", joined="2018-11-30")`

///

### 多種編輯器支援

整個框架的設計是為了讓使用變得簡單且直觀，在開始開發之前，所有決策都在多個編輯器上進行了測試，以確保提供最佳的開發體驗。

在最近的 Python 開發者調查中，我們能看到<a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank"> 被使用最多的功能是 autocompletion</a>，此功能可以預測將要輸入文字，並自動補齊。

整個 **FastAPI** 框架就是基於這一點，任何地方都可以進行自動補齊。

你幾乎不需要經常來回看文件。

在這裡，你的編輯器可能會這樣幫助你：

* <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a> 中:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> 中:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

你將能進行程式碼補齊，這是在之前你可能曾認為不可能的事。例如，請求 JSON body（可能是巢狀的）中的鍵 `price`。

這樣比較不會輸錯鍵名，不用來回翻看文件，也不用來回滾動尋找你最後使用的 `username` 或者 `user_name`。



### 簡潔

FastAPI 為你提供了**預設值**，讓你不必在初期進行繁瑣的配置，一切都可以自動運作。如果你有更具體的需求，則可以進行調整和自定義，

但在大多數情況下，你只需要直接使用預設值，就能順利完成 API 開發。

### 驗證

所有的驗證都由完善且強大的 **Pydantic** 處理。

* 驗證大部分（甚至所有？）的 Python **資料型別**，包括：
    * JSON 物件 (`dict`)。
    * JSON 陣列 (`list`) 定義項目型別。
    * 字串 (`str`) 欄位，定義最小或最大長度。
    * 數字 (`int`, `float`) 與其最大值和最小值等。

* 驗證外來的型別，比如:
    * URL
    * Email
    * UUID


### 安全性及身份驗證

FastAPI 已經整合了安全性和身份驗證的功能，但不會強制與特定的資料庫或資料模型進行綁定。

OpenAPI 中定義的安全模式，包括：

* HTTP 基本認證。
* **OAuth2**（也使用 **JWT tokens**）。在 [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank} 查看教學。
* API 密鑰，在：
    * 標頭（Header）
    * 查詢參數
    * Cookies，等等。

加上来自 Starlette（包括 **session cookie**）的所有安全特性。

所有的這些都是可重複使用的工具和套件，可以輕鬆與你的系統、資料儲存（Data Stores）、關聯式資料庫（RDBMS）以及非關聯式資料庫（NoSQL）等等整合。


### 依賴注入（Dependency Injection）

FastAPI 有一個使用簡單，但是非常強大的<abbr title='也叫做 "components", "resources", "services", "providers"'><strong>依賴注入</strong></abbr>系統。

* 依賴項甚至可以有自己的依賴，從而形成一個層級或**依賴圖**的結構。
* 所有**自動化處理**都由框架完成。
* 依賴項不僅能從請求中提取資料，還能**對 API 的路徑操作進行強化**，並自動生成文檔。
* 即使是依賴項中定義的*路徑操作參數*，也會**自動進行驗證**。
* 支持複雜的用戶身份驗證系統、**資料庫連接**等。
* 不與資料庫、前端等進行強制綁定，但能輕鬆整合它們。


### 無限制「擴充功能」

或者說，無需其他額外配置，直接導入並使用你所需要的程式碼。

任何整合都被設計得非常簡單易用（通過依賴注入），你只需用與*路徑操作*相同的結構和語法，用兩行程式碼就能為你的應用程式建立一個「擴充功能」。


### 測試

* 100% 的<abbr title="有自動測試的程式碼">測試覆蓋率</abbr>。
* 100% 的程式碼有<abbr title="Python 型別註釋，有了這個你的編輯器和外部工具可以給你更好的支援">型別註釋</abbr>。
* 已能夠在生產環境應用程式中使用。

## Starlette 特性

**FastAPI** 完全相容且基於 <a href="https://www.starlette.dev/" class="external-link" target="_blank"><strong>Starlette</strong></a>。所以，你有其他的 Starlette 程式碼也能正常運作。FastAPI 繼承了 Starlette 的所有功能，如果你已經知道或者使用過 Starlette，大部分的功能會以相同的方式運作。

通過 **FastAPI** 你可以獲得所有 **Starlette** 的特性（FastAPI 就像加強版的 Starlette）：

* 性能極其出色。它是 <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">Python 可用的最快框架之一，和 **NodeJS** 及 **Go** 相當</a>。
* **支援 WebSocket**。
* 能在行程內處理背景任務。
* 支援啟動和關閉事件。
* 有基於 HTTPX 的測試用戶端。
* 支援 **CORS**、GZip、靜態檔案、串流回應。
* 支援 **Session 和 Cookie** 。
* 100% 測試覆蓋率。
* 100% 型別註釋的程式碼庫。

## Pydantic 特性

**FastAPI** 完全相容且基於 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank"><strong>Pydantic</strong></a>。所以，你有其他 Pydantic 程式碼也能正常工作。

相容包括基於 Pydantic 的外部函式庫， 例如用於資料庫的 <abbr title="Object-Relational Mapper">ORM</abbr>s, <abbr title="Object-Document Mapper">ODM</abbr>s。

這也意味著在很多情況下，你可以把從請求中獲得的物件**直接傳到資料庫**，因為所有資料都會自動進行驗證。

反之亦然，在很多情況下，你也可以把從資料庫中獲取的物件**直接傳給客戶端**。

通過 **FastAPI** 你可以獲得所有 **Pydantic** 的特性（FastAPI 基於 Pydantic 做了所有的資料處理）：

* **更簡單**：
    * 不需要學習新的 micro-language 來定義結構。
    * 如果你知道 Python 型別，你就知道如何使用 Pydantic。
* 和你的 **<abbr title="Integrated Development Environment，和程式碼編輯器類似">IDE</abbr>/<abbr title="一個檢查程式碼錯誤的工具">linter</abbr>/brain** 都能好好配合：
    * 因為 Pydantic 的資料結構其實就是你自己定義的類別實例，所以自動補齊、linting、mypy 以及你的直覺都能很好地在經過驗證的資料上發揮作用。
* 驗證**複雜結構**：
    * 使用 Pydantic 模型時，你可以把資料結構分層設計，並且用 Python 的 `List` 和 `Dict` 等型別來定義。
    * 驗證器讓我們可以輕鬆地定義和檢查複雜的資料結構，並把它們轉換成 JSON Schema 進行記錄。
    * 你可以擁有深層**巢狀的 JSON** 物件，並對它們進行驗證和註釋。
* **可擴展**：
    * Pydantic 讓我們可以定義客製化的資料型別，或者你可以使用帶有 validator 裝飾器的方法來擴展模型中的驗證功能。
* 100% 測試覆蓋率。
