# SQL（關聯式）資料庫 { #sql-relational-databases }

FastAPI 不強制你使用 SQL（關聯式）資料庫。你可以使用任何你想要的資料庫。

這裡我們會用 <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a> 作為範例。

SQLModel 建立在 <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a> 與 Pydantic 之上。它由 FastAPI 的作者開發，非常適合需要使用 SQL 資料庫的 FastAPI 應用。

/// tip | 提示

你可以使用任何你想用的 SQL 或 NoSQL 資料庫函式庫（有時稱為 <abbr title="Object Relational Mapper - 物件關聯對應器：一個用來描述某些類別代表 SQL 資料表且其實例代表資料表中資料列的函式庫的術語">"ORMs"</abbr>），FastAPI 不會強迫你使用特定工具。😎

///

因為 SQLModel 建立在 SQLAlchemy 之上，你可以輕鬆使用 SQLAlchemy 所支援的任何資料庫（因此 SQLModel 也支援），例如：

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server，等等。

在這個範例中，我們會使用 SQLite，因為它只用到單一檔案，而且 Python 內建支援。你可以直接複製這個範例並原樣執行。

之後，在你的正式環境應用中，你可能會想使用像 PostgreSQL 這類的資料庫伺服器。

/// tip | 提示

有一個包含 FastAPI 與 PostgreSQL 的官方專案腳手架，還有前端與更多工具：<a href="https://github.com/fastapi/full-stack-fastapi-template" class="external-link" target="_blank">https://github.com/fastapi/full-stack-fastapi-template</a>

///

這是一份非常簡短的教學，如果你想更全面學習資料庫、SQL，或更進階的功能，請參考 <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel 文件</a>。

## 安裝 `SQLModel` { #install-sqlmodel }

首先，請先建立你的[虛擬環境](../virtual-environments.md){.internal-link target=_blank}、啟用它，然後安裝 `sqlmodel`：

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## 建立只有單一模型的應用 { #create-the-app-with-a-single-model }

我們先用單一 SQLModel 模型建立這個應用的最簡版。

接著我們會在下方用多個模型來提升安全性與彈性。🤓

### 建立模型 { #create-models }

匯入 `SQLModel` 並建立一個資料庫模型：

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

`Hero` 類別與 Pydantic 模型非常相似（事實上，在底層它就是一個 Pydantic 模型）。

有幾點差異：

* `table=True` 告訴 SQLModel 這是一個「資料表模型」（table model），它應該代表 SQL 資料庫中的一個資料表，而不僅僅是「資料模型」（就像一般的 Pydantic 類別）。

* `Field(primary_key=True)` 告訴 SQLModel，`id` 是 SQL 資料庫中的「主鍵」。 （你可以在 SQLModel 文件中進一步了解 SQL 主鍵）

    注意：我們在主鍵欄位使用 `int | None`，這樣在 Python 程式碼中我們可以「在沒有 `id` 的情況下建立物件」（`id=None`），假設資料庫在儲存時會「自動產生」。SQLModel 瞭解資料庫會提供 `id`，並且在資料庫綱要中「將該欄位定義為非空的 `INTEGER`」。詳情請見 <a href="https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#primary-key-id" class="external-link" target="_blank">SQLModel 文件：主鍵</a>。

* `Field(index=True)` 告訴 SQLModel 應為此欄位建立「SQL 索引」，以便在用此欄位過濾讀取資料時更快查詢。

    SQLModel 會知道宣告為 `str` 的欄位在 SQL 中會是 `TEXT`（或 `VARCHAR`，依資料庫而定）。

### 建立引擎 { #create-an-engine }

SQLModel 的 `engine`（底層實際上是 SQLAlchemy 的 `engine`）是用來「維護與資料庫連線」的東西。

你的程式中應該只有「單一 `engine` 物件」來連到同一個資料庫。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

使用 `check_same_thread=False` 允許 FastAPI 在不同執行緒中使用同一個 SQLite 資料庫。這是必要的，因為「單一請求」可能會使用「多個執行緒」（例如在依賴項中）。

別擔心，依照我們的程式結構，稍後我們會確保「每個請求只使用單一 SQLModel 的 session」，這其實就是 `check_same_thread` 想要達成的事。

### 建立資料表 { #create-the-tables }

接著我們新增一個函式，使用 `SQLModel.metadata.create_all(engine)` 為所有「資料表模型」建立資料表。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### 建立 Session 依賴 { #create-a-session-dependency }

「`Session`」會在記憶體中保存物件並追蹤資料需要的任何變更，然後透過「`engine`」與資料庫溝通。

我們會用 `yield` 建立一個 FastAPI 的「依賴」，為每個請求提供一個新的 `Session`。這可確保每個請求只使用單一的 session。🤓

接著我們建立一個 `Annotated` 的依賴 `SessionDep`，讓後續使用這個依賴的程式碼更簡潔。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### 在啟動時建立資料表 { #create-database-tables-on-startup }

我們會在應用啟動時建立資料庫的資料表。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

這裡我們在應用的啟動事件中建立資料表。

在正式環境中，你大概會在啟動應用前使用遷移腳本來處理。🤓

/// tip | 提示

SQLModel 之後會提供包裝 Alembic 的遷移工具，但目前你可以直接使用 <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a>。

///

### 建立 Hero { #create-a-hero }

因為每個 SQLModel 模型同時也是一個 Pydantic 模型，你可以在「型別標註」中像使用 Pydantic 模型一樣使用它。

例如，如果你宣告一個參數型別為 `Hero`，它會從「JSON body」中讀取。

同樣地，你也可以將它宣告為函式的「回傳型別」，然後在自動產生的 API 文件 UI 中就會顯示其資料結構。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

這裡我們使用 `SessionDep` 依賴（即一個 `Session`），把新的 `Hero` 加入 `Session` 實例，提交變更到資料庫，刷新 `hero` 的資料，然後回傳它。

### 讀取多個 Hero { #read-heroes }

我們可以用 `select()` 從資料庫「讀取」多個 `Hero`。可以加入 `limit` 與 `offset` 來分頁。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### 讀取單一 Hero { #read-one-hero }

我們可以「讀取」單一的 `Hero`。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### 刪除 Hero { #delete-a-hero }

我們也可以「刪除」一個 `Hero`。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### 執行應用 { #run-the-app }

你可以執行應用：

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

然後前往 `/docs` 的 UI，你會看到 FastAPI 使用這些模型來「文件化」API，也會用它們來「序列化」與「驗證」資料。

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## 用多個模型更新應用 { #update-the-app-with-multiple-models }

現在我們稍微「重構」一下這個應用，以提升「安全性」與「彈性」。

如果你檢查前一版的應用，在 UI 中你會看到，到目前為止它讓用戶端自己決定要建立的 `Hero` 的 `id`。😱

我們不該允許這樣，因為他們可能會覆蓋資料庫中我們已分配的 `id`。決定 `id` 應該由「後端」或「資料庫」來做，「不是用戶端」。

另外，我們為 hero 建立了 `secret_name`，但目前我們在各處都把它回傳出去，這一點都不「保密」... 😅

我們會透過加入一些「額外模型」來修正這些問題。這正是 SQLModel 大放異彩的地方。✨

### 建立多個模型 { #create-multiple-models }

在 SQLModel 中，任何設了 `table=True` 的模型類別都是「資料表模型」。

而沒有設 `table=True` 的模型類別就是「資料模型」，這些其實就是 Pydantic 模型（只有一點小增強）。🤓

使用 SQLModel，我們可以利用「繼承」來「避免重複」在各種情況下一再宣告所有欄位。

#### `HeroBase` - 基底類別 { #herobase-the-base-class }

先從 `HeroBase` 模型開始，它包含所有模型「共享」的欄位：

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - 資料表模型 { #hero-the-table-model }

接著建立 `Hero`，也就是實際的「資料表模型」，它包含不一定會出現在其他模型中的「額外欄位」：

* `id`
* `secret_name`

因為 `Hero` 繼承自 `HeroBase`，它「也」擁有 `HeroBase` 中宣告的「欄位」，因此 `Hero` 的完整欄位為：

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - 公開的資料模型 { #heropublic-the-public-data-model }

接下來建立 `HeroPublic` 模型，它是要「回傳」給 API 用戶端的模型。

它擁有與 `HeroBase` 相同的欄位，因此不會包含 `secret_name`。

終於，我們英雄的真實身分受保護了！🥷

它也重新宣告了 `id: int`。這麼做是與 API 用戶端訂立一個「契約」，讓他們可以確定 `id` 一定存在而且是 `int`（不會是 `None`）。

/// tip | 提示

讓回傳模型保證某個值一定存在、而且一定是 `int`（不是 `None`），對 API 用戶端非常有幫助。他們在有這個確信下可以寫出更簡單的程式碼。

此外，透過「自動產生的客戶端」也會有更簡潔的介面，讓要使用你 API 的開發者能有更好的開發體驗。😎

///

`HeroPublic` 中的欄位與 `HeroBase` 相同，僅 `id` 宣告為 `int`（非 `None`）：

* `id`
* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - 用於建立 Hero 的資料模型 { #herocreate-the-data-model-to-create-a-hero }

現在我們建立 `HeroCreate` 模型，這是用來「驗證」用戶端送來資料的模型。

它具有與 `HeroBase` 相同的欄位，並且還有 `secret_name`。

接下來，當用戶端「建立新 hero」時，他們會送上 `secret_name`，它會被儲存在資料庫中，但這些祕密名稱不會在 API 中回傳給用戶端。

/// tip | 提示

這也就是你處理「密碼」的方式。接收它們，但不要在 API 中回傳。

你也應該在儲存前先對密碼做「雜湊」，「永遠不要以明文儲存」。

///

`HeroCreate` 的欄位有：

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - 用於更新 Hero 的資料模型 { #heroupdate-the-data-model-to-update-a-hero }

在前一版的應用中，我們沒有「更新 hero」的方式，但現在有了「多個模型」，我們就能做到。🎉

`HeroUpdate` 這個資料模型有點特別，它包含「建立新 hero 所需的所有欄位」，但所有欄位都是「可選的」（都有預設值）。這樣在更新時，你只需要送出想要更新的欄位即可。

因為所有欄位的「型別其實都改變了」（型別現在包含 `None`，而且預設值為 `None`），我們需要「重新宣告」它們。

其實不一定要繼承 `HeroBase`，因為我們會重新宣告所有欄位。我這裡保留繼承只是為了一致性，並非必要。這主要是個人偏好的問題。🤷

`HeroUpdate` 的欄位有：

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### 用 `HeroCreate` 建立並回傳 `HeroPublic` { #create-with-herocreate-and-return-a-heropublic }

現在我們有了「多個模型」，可以更新應用中使用它們的部分。

我們在請求中接收 `HeroCreate`（資料模型），並由它建立一個 `Hero`（資料表模型）。

這個新的資料表模型 `Hero` 會有用戶端傳來的欄位，並且會由資料庫產生一個 `id`。

然後我們直接從函式回傳這個資料表模型 `Hero`。但因為我們用 `HeroPublic` 當作 `response_model`，FastAPI 會用 `HeroPublic` 來驗證與序列化資料。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip | 提示

現在我們用 `response_model=HeroPublic`，而不是用回傳型別標註 `-> HeroPublic`，因為我們實際回傳的值其實「不是」`HeroPublic`。

如果我們宣告 `-> HeroPublic`，你的編輯器與 linter 會（理所當然地）抱怨你回傳的是 `Hero` 而不是 `HeroPublic`。

在 `response_model` 中宣告，就是要讓 FastAPI 去做它該做的事，而不影響型別標註，以及你的編輯器與其他工具提供的協助。

///

### 使用 `HeroPublic` 讀取多個 Hero { #read-heroes-with-heropublic }

我們可以像先前一樣「讀取」多個 `Hero`。同樣地，我們使用 `response_model=list[HeroPublic]` 來確保資料被正確驗證與序列化。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### 使用 `HeroPublic` 讀取單一 Hero { #read-one-hero-with-heropublic }

我們可以「讀取」單一 hero：

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### 使用 `HeroUpdate` 更新 Hero { #update-a-hero-with-heroupdate }

我們可以「更新 hero」。為此我們使用 HTTP 的 `PATCH` 操作。

在程式碼中，我們會取得一個只包含用戶端有傳送的資料的 `dict`，不包含只是因為有預設值而存在的欄位。為了達成這點，我們使用 `exclude_unset=True`。這是關鍵。🪄

然後我們使用 `hero_db.sqlmodel_update(hero_data)` 以 `hero_data` 的資料更新 `hero_db`。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### 再次刪除 Hero { #delete-a-hero-again }

「刪除」 hero 基本上維持不變。

我們不會為了重構而重構一切。😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### 再次執行應用 { #run-the-app-again }

你可以再次執行應用：

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

如果你前往 `/docs` 的 API UI，你會看到它已更新，建立 hero 時不再期待從用戶端接收 `id`，等等。

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## 總結 { #recap }

你可以使用 <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a> 與 SQL 資料庫互動，並用「資料模型」與「資料表模型」讓程式碼更簡潔。

你可以在 SQLModel 文件學到更多內容，這裡還有一份更長的 <a href="https://sqlmodel.tiangolo.com/tutorial/fastapi/" class="external-link" target="_blank">使用 SQLModel 與 FastAPI 的教學</a>。🚀
