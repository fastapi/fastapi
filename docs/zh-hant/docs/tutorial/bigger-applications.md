# 更大型的應用程式 - 多個檔案 { #bigger-applications-multiple-files }

如果你正在建置一個應用程式或 Web API，很少會把所有東西都放在單一檔案裡。

FastAPI 提供了一個方便的工具，讓你在維持彈性的同時，幫你組織應用程式的結構。

/// info | 資訊

如果你來自 Flask，這相當於 Flask 的 Blueprints。

///

## 範例檔案結構 { #an-example-file-structure }

假設你有如下的檔案結構：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

/// tip | 提示

有好幾個 `__init__.py` 檔案：每個目錄或子目錄各一個。

這讓我們可以把一個檔案中的程式碼匯入到另一個檔案。

例如，在 `app/main.py` 你可以有一行：

```
from app.routers import items
```

///

* `app` 目錄包含所有內容。它有一個空的 `app/__init__.py` 檔案，所以它是一個「Python 套件」（「Python 模組」的集合）：`app`。
* 它包含一個 `app/main.py` 檔案。因為它在一個 Python 套件中（有 `__init__.py` 檔案的目錄），它是該套件的一個「模組」：`app.main`。
* 還有一個 `app/dependencies.py` 檔案，就像 `app/main.py` 一樣，它是一個「模組」：`app.dependencies`。
* 有一個子目錄 `app/routers/`，裡面有另一個 `__init__.py` 檔案，所以它是一個「Python 子套件」：`app.routers`。
* 檔案 `app/routers/items.py` 在一個套件 `app/routers/` 內，因此它是一個子模組：`app.routers.items`。
* 同樣地，`app/routers/users.py` 是另一個子模組：`app.routers.users`。
* 還有一個子目錄 `app/internal/`，裡面有另一個 `__init__.py` 檔案，所以它又是一個「Python 子套件」：`app.internal`。
* 檔案 `app/internal/admin.py` 是另一個子模組：`app.internal.admin`。

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

同樣的檔案結構，附上註解：

```bash
.
├── app                  # 「app」是一個 Python 套件
│   ├── __init__.py      # 這個檔案讓「app」成為「Python 套件」
│   ├── main.py          # 「main」模組，例如 import app.main
│   ├── dependencies.py  # 「dependencies」模組，例如 import app.dependencies
│   └── routers          # 「routers」是一個「Python 子套件」
│   │   ├── __init__.py  # 讓「routers」成為「Python 子套件」
│   │   ├── items.py     # 「items」子模組，例如 import app.routers.items
│   │   └── users.py     # 「users」子模組，例如 import app.routers.users
│   └── internal         # 「internal」是一個「Python 子套件」
│       ├── __init__.py  # 讓「internal」成為「Python 子套件」
│       └── admin.py     # 「admin」子模組，例如 import app.internal.admin
```

## `APIRouter` { #apirouter }

假設專門處理使用者的檔案是位於 `/app/routers/users.py` 的子模組。

你希望把與使用者相關的「路徑操作 (path operation)」從其他程式碼分離，讓結構更有條理。

但它仍然是同一個 FastAPI 應用程式 / Web API 的一部分（屬於同一個「Python 套件」）。

你可以使用 `APIRouter` 為該模組建立路徑操作。

### 匯入 `APIRouter` { #import-apirouter }

你可以像對 `FastAPI` 類別那樣匯入並建立一個「實例」：

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[1,3] title["app/routers/users.py"] *}

### 使用 `APIRouter` 宣告路徑操作 { #path-operations-with-apirouter }

然後用它來宣告你的路徑操作。

用法就和 `FastAPI` 類別一樣：

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[6,11,16] title["app/routers/users.py"] *}

你可以把 `APIRouter` 想成是「迷你版的 `FastAPI`」類別。

所有相同的選項都支援。

同樣的 `parameters`、`responses`、`dependencies`、`tags` 等全都可用。

/// tip | 提示

在這個範例中，變數名叫 `router`，但你可以用任何你想用的名稱。

///

我們稍後會把這個 `APIRouter` 加進主要的 `FastAPI` 應用程式中，但先來看看相依性與另一個 `APIRouter`。

## 相依性 { #dependencies }

我們發現應用程式的多個地方會用到一些相依性。

所以把它們放進獨立的 `dependencies` 模組（`app/dependencies.py`）。

接下來我們會用一個簡單的相依性來讀取自訂的 `X-Token` 標頭：

{* ../../docs_src/bigger_applications/app_an_py310/dependencies.py hl[3,6:8] title["app/dependencies.py"] *}

/// tip | 提示

為了簡化範例，我們使用了一個虛構的標頭。

但在真實情況下，使用內建的 [安全工具](security/index.md) 會有更好的效果。

///

## 另一個帶有 `APIRouter` 的模組 { #another-module-with-apirouter }

假設你還有一個模組 `app/routers/items.py`，專門處理應用程式中的「items」。

你有以下路徑操作：

* `/items/`
* `/items/{item_id}`

其結構與 `app/routers/users.py` 相同。

但我們想要更聰明地簡化一些程式碼。

我們知道這個模組中的所有路徑操作都有相同的：

* 路徑 `prefix`：`/items`
* `tags`：（只有一個標籤：`items`）
* 額外的 `responses`
* `dependencies`：它們都需要我們先前建立的 `X-Token` 相依性

因此，我們可以不必把這些都加在每個路徑操作上，而是把它們加在 `APIRouter` 上。

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[5:10,16,21] title["app/routers/items.py"] *}

由於每個路徑操作的路徑都必須以 `/` 開頭，例如：

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...所以 prefix 末尾不能帶有 `/`。

因此，此處的 prefix 是 `/items`。

我們也可以加上一個 `tags` 清單，以及會套用在此 router 內所有路徑操作上的額外 `responses`。

我們還可以加上一個 `dependencies` 清單，這些相依性會加入此 router 內所有的路徑操作，並在對它們的每個請求上執行 / 解決。

/// tip | 提示

請注意，就像在[路徑操作裝飾器中的相依性](dependencies/dependencies-in-path-operation-decorators.md)一樣，不會把任何值傳遞給你的路徑操作函式（path operation function）。

///

最後的結果是這些 item 的路徑如下：

* `/items/`
* `/items/{item_id}`

...正如我們預期的。

* 它們會被標記為只有一個字串 `"items"` 的標籤清單。
    * 這些「標籤」對自動互動式文件系統（使用 OpenAPI）特別有用。
* 它們都會包含預先定義的 `responses`。
* 這些路徑操作都會在執行前評估 / 執行其 `dependencies` 清單。
    * 如果你也在特定的路徑操作中宣告了相依性，這些相依性也會被執行。
    * Router 的相依性會先執行，然後是[裝飾器中的 `dependencies`](dependencies/dependencies-in-path-operation-decorators.md)，最後是一般參數相依性。
    * 你也可以加入帶有 `scopes` 的 [`Security` 相依性](../advanced/security/oauth2-scopes.md)。

/// tip | 提示

在 `APIRouter` 中設定 `dependencies`，例如可以用來對一整組路徑操作要求驗證。即使沒有在每個路徑操作個別加入相依性也沒關係。

///

/// check | 檢查

`prefix`、`tags`、`responses` 與 `dependencies` 參數（就像許多其他情況一樣）只是 FastAPI 提供的功能，幫助你避免重複程式碼。

///

### 匯入相依性 { #import-the-dependencies }

這段程式碼在模組 `app.routers.items`（檔案 `app/routers/items.py`）中。

我們需要從模組 `app.dependencies`（檔案 `app/dependencies.py`）取得相依性函式。

因此我們用 `..` 做相對匯入相依性：

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[3] title["app/routers/items.py"] *}

#### 相對匯入如何運作 { #how-relative-imports-work }

/// tip | 提示

如果你對匯入的運作方式十分了解，可以直接跳到下一節。

///

單一的點號 `.`，如下：

```Python
from .dependencies import get_token_header
```

代表：

* 從此模組（檔案 `app/routers/items.py`）所在的相同套件（目錄 `app/routers/`）開始...
* 找到模組 `dependencies`（想像的檔案 `app/routers/dependencies.py`）...
* 並從中匯入函式 `get_token_header`。

但那個檔案不存在，我們的相依性在 `app/dependencies.py`。

回想一下我們的應用 / 檔案結構長這樣：

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

---

兩個點號 `..`，如下：

```Python
from ..dependencies import get_token_header
```

代表：

* 從此模組（檔案 `app/routers/items.py`）所在的相同套件（目錄 `app/routers/`）開始...
* 前往其父套件（目錄 `app/`）...
* 然後在那裡找到模組 `dependencies`（檔案 `app/dependencies.py`）...
* 並從中匯入函式 `get_token_header`。

這就正確了！🎉

---

同樣地，如果我們用三個點號 `...`，如下：

```Python
from ...dependencies import get_token_header
```

就代表：

* 從此模組（檔案 `app/routers/items.py`）所在的相同套件（目錄 `app/routers/`）開始...
* 前往其父套件（目錄 `app/`）...
* 再前往那個套件的父層（沒有更上層的套件了，`app` 已是最上層 😱）...
* 然後在那裡找到模組 `dependencies`（檔案 `app/dependencies.py`）...
* 並從中匯入函式 `get_token_header`。

那會指向 `app/` 之上的某個套件，該套件需有自己的 `__init__.py` 等等。但我們沒有。所以在這個例子中會丟出錯誤。🚨

不過現在你知道它的運作方式了，因此無論你的應用有多複雜，你都可以使用相對匯入。🤓

### 加上一些自訂的 `tags`、`responses` 與 `dependencies` { #add-some-custom-tags-responses-and-dependencies }

我們沒有把 `/items` 的 prefix 以及 `tags=["items"]` 加在每個路徑操作上，因為我們已經把它們加在 `APIRouter` 上了。

但我們仍可以在特定的路徑操作上再加上更多的 `tags`，以及一些只屬於該路徑操作的額外 `responses`：

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[30:31] title["app/routers/items.py"] *}

/// tip | 提示

這最後一個路徑操作會有組合後的標籤：`["items", "custom"]`。

而且在文件中同時會有 `404` 與 `403` 兩種回應。

///

## 主程式 `FastAPI` { #the-main-fastapi }

現在，來看看 `app/main.py` 這個模組。

你會在這裡匯入並使用 `FastAPI` 類別。

這會是你的應用程式中把一切串起來的主檔案。

而隨著大多數的邏輯都放在各自的模組中，主檔案會相當簡潔。

### 匯入 `FastAPI` { #import-fastapi }

照常匯入並建立 `FastAPI` 類別。

我們甚至可以宣告[全域相依性](dependencies/global-dependencies.md)，它們會與各 `APIRouter` 的相依性合併：

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[1,3,7] title["app/main.py"] *}

### 匯入 `APIRouter` { #import-the-apirouter }

現在我們匯入包含 `APIRouter` 的其他子模組：

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[4:5] title["app/main.py"] *}

由於 `app/routers/users.py` 與 `app/routers/items.py` 是同一個 Python 套件 `app` 的子模組，我們可以用單一的點號 `.` 來進行「相對匯入」。

### 匯入如何運作 { #how-the-importing-works }

這段：

```Python
from .routers import items, users
```

代表：

* 從此模組（檔案 `app/main.py`）所在的相同套件（目錄 `app/`）開始...
* 尋找子套件 `routers`（目錄 `app/routers/`）...
* 並從中匯入子模組 `items`（檔案 `app/routers/items.py`）與 `users`（檔案 `app/routers/users.py`）...

模組 `items` 會有一個變數 `router`（`items.router`）。這就是我們在 `app/routers/items.py` 建立的那個 `APIRouter` 物件。

接著我們對 `users` 模組做一樣的事。

我們也可以這樣匯入：

```Python
from app.routers import items, users
```

/// info | 資訊

第一種是「相對匯入」：

```Python
from .routers import items, users
```

第二種是「絕對匯入」：

```Python
from app.routers import items, users
```

想了解更多關於 Python 套件與模組，請閱讀[官方的模組說明文件](https://docs.python.org/3/tutorial/modules.html)。

///

### 避免名稱衝突 { #avoid-name-collisions }

我們直接匯入子模組 `items`，而不是只匯入它的變數 `router`。

這是因為在子模組 `users` 中也有另一個名為 `router` 的變數。

如果我們像下面這樣一個接一個匯入：

```Python
from .routers.items import router
from .routers.users import router
```

來自 `users` 的 `router` 會覆蓋掉 `items` 的 `router`，我們就無法同時使用兩者。

因此，為了能在同一個檔案中同時使用它們，我們直接匯入子模組：

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[5] title["app/main.py"] *}

### 將 `users` 與 `items` 的 `APIRouter` 納入 { #include-the-apirouters-for-users-and-items }

現在，把子模組 `users` 與 `items` 的 `router` 納入：

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[10:11] title["app/main.py"] *}

/// info | 資訊

`users.router` 是位於 `app/routers/users.py` 檔案內的 `APIRouter`。

而 `items.router` 是位於 `app/routers/items.py` 檔案內的 `APIRouter`。

///

透過 `app.include_router()`，我們可以把每個 `APIRouter` 加到主要的 `FastAPI` 應用程式。

它會把該 router 的所有路由都納入成為應用的一部分。

/// note | 技術細節

實際上，它會在內部為 `APIRouter` 中宣告的每一個「路徑操作」建立一個對應的「路徑操作」。

所以在幕後，它實際運作起來就像是一個單一的應用。

///

/// check | 檢查

把 router 納入時不需要擔心效能。

這只會在啟動時花費微秒等級，且只發生一次。

因此不會影響效能。⚡

///

### 以自訂的 `prefix`、`tags`、`responses` 與 `dependencies` 納入一個 `APIRouter` { #include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies }

現在，假設你的組織提供了一個 `app/internal/admin.py` 檔案給你。

它包含一個帶有一些管理員路徑操作的 `APIRouter`，並在組織內多個專案之間共用。

為了這個範例它會非常簡單。但假設因為它會與組織內的其他專案共用，我們不能直接修改它並把 `prefix`、`dependencies`、`tags` 等加在 `APIRouter` 上：

{* ../../docs_src/bigger_applications/app_an_py310/internal/admin.py hl[3] title["app/internal/admin.py"] *}

但當我們把這個 `APIRouter` 納入時，仍然希望設定自訂的 `prefix`，讓它所有的路徑操作都以 `/admin` 開頭；我們想用這個專案已經有的 `dependencies` 來保護它，並且要加入 `tags` 與 `responses`。

我們可以在不修改原始 `APIRouter` 的情況下，將這些參數傳給 `app.include_router()` 來達成：

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[14:17] title["app/main.py"] *}

如此一來，原始的 `APIRouter` 將保持不變，因此我們仍然可以把同一個 `app/internal/admin.py` 檔案與組織中的其他專案共用。

結果是在我們的應用中，來自 `admin` 模組的每個路徑操作都會有：

* 前綴 `/admin`
* 標籤 `admin`
* 相依性 `get_token_header`
* 回應 `418` 🍵

但這只會影響我們應用中的那個 `APIRouter`，不會影響任何其他使用它的程式碼。

例如，其他專案可以用不同的驗證方式搭配相同的 `APIRouter`。

### 加上一個路徑操作 { #include-a-path-operation }

我們也可以直接把路徑操作加到 `FastAPI` 應用中。

這裡我們就加一下... 只是為了示範可以這麼做 🤷：

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[21:23] title["app/main.py"] *}

而且它會和透過 `app.include_router()` 加入的其他路徑操作正確地一起運作。

/// info | 非常技術細節

注意：這是個非常技術性的細節，你大概可以直接略過。

---

`APIRouter` 不是被「掛載 (mount)」的，它們不會與應用的其他部分隔離開來。

這是因為我們要把它們的路徑操作包含進 OpenAPI 結構與使用者介面中。

由於無法將它們隔離並獨立「掛載」，所以這些路徑操作會被「複製」（重新建立），而不是直接包含進來。

///

## 在 `pyproject.toml` 設定 `entrypoint` { #configure-the-entrypoint-in-pyproject-toml }

因為你的 FastAPI `app` 物件位在 `app/main.py`，你可以在 `pyproject.toml` 檔案中這樣設定 `entrypoint`：

```toml
[tool.fastapi]
entrypoint = "app.main:app"
```

這等同於這樣匯入：

```python
from app.main import app
```

如此一來 `fastapi` 指令就會知道去哪裡找到你的 app。

/// Note | 注意

你也可以把路徑直接傳給指令，例如：

```console
$ fastapi dev app/main.py
```

但你每次呼叫 `fastapi` 指令時都得記得傳入正確的路徑。

此外，其他工具可能找不到它，例如 [VS Code 擴充套件](../editor-support.md) 或 [FastAPI Cloud](https://fastapicloud.com)，因此建議在 `pyproject.toml` 中使用 `entrypoint`。

///

## 檢查自動產生的 API 文件 { #check-the-automatic-api-docs }

現在，執行你的應用：

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

然後開啟位於 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 的文件。

你會看到自動產生的 API 文件，包含來自所有子模組的路徑，使用正確的路徑（與前綴）與正確的標籤：

<img src="/img/tutorial/bigger-applications/image01.png">

## 以不同的 `prefix` 多次納入同一個 router { #include-the-same-router-multiple-times-with-different-prefix }

你也可以用不同的前綴，對同一個 router 多次呼叫 `.include_router()`。

例如，這對於在不同前綴下提供相同的 API 很有用，如 `/api/v1` 與 `/api/latest`。

這是進階用法，你可能不會需要，但若有需要它就在那裡。

## 在另一個 `APIRouter` 中納入一個 `APIRouter` { #include-an-apirouter-in-another }

就像你可以在 `FastAPI` 應用中納入一個 `APIRouter` 一樣，你也可以在另一個 `APIRouter` 中納入一個 `APIRouter`，用法如下：

```Python
router.include_router(other_router)
```

請確保在把 `router` 納入 `FastAPI` 應用之前先這麼做，這樣 `other_router` 的路徑操作也會被包含進去。
