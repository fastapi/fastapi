# 進階相依 { #advanced-dependencies }


## 參數化的相依 { #parameterized-dependencies }

到目前為止看到的相依都是固定的函式或類別。

但有些情況下，你可能想要能為相依設定參數，而不必宣告許多不同的函式或類別。

想像我們想要一個相依，用來檢查查詢參數 `q` 是否包含某些固定內容。

同時我們希望能將那個固定內容參數化。

## 「callable」的實例 { #a-callable-instance }

在 Python 中有一種方式可以讓一個類別的實例變成「callable」。

不是類別本身（類別本來就可呼叫），而是該類別的實例。

要做到這點，我們宣告一個 `__call__` 方法：

{* ../../docs_src/dependencies/tutorial011.py hl[12] *}

在這個情境中，**FastAPI** 會用這個 `__call__` 來檢查額外的參數與子相依，並在之後呼叫它，把回傳值傳遞給你的「路徑操作函式」中的參數。

## 讓實例可參數化 { #parameterize-the-instance }

接著，我們可以用 `__init__` 來宣告這個實例的參數，用以「參數化」這個相依：

{* ../../docs_src/dependencies/tutorial011.py hl[9] *}

在這裡，**FastAPI** 完全不會接觸或在意 `__init__`，我們會直接在自己的程式碼中使用它。

## 建立一個實例 { #create-an-instance }

我們可以這樣建立該類別的實例：

{* ../../docs_src/dependencies/tutorial011.py hl[18] *}

如此一來我們就能「參數化」相依，現在它內部含有 `"bar"`，作為屬性 `checker.fixed_content`。

## 將實例作為相依使用 { #use-the-instance-as-a-dependency }

然後，我們可以在 `Depends(checker)` 中使用這個 `checker`，而不是 `Depends(FixedContentQueryChecker)`，因為相依是那個實例 `checker`，不是類別本身。

當解析相依時，**FastAPI** 會像這樣呼叫這個 `checker`：

```Python
checker(q="somequery")
```

...並將其回傳值，作為相依的值，以參數 `fixed_content_included` 傳給我們的「路徑操作函式」：

{* ../../docs_src/dependencies/tutorial011.py hl[22] *}

/// tip | 提示

這一切現在看起來也許有點牽強，而且目前可能還不太清楚有何用途。

這些範例刻意保持簡單，但展示了整個機制如何運作。

在關於安全性的章節裡，有一些工具函式也是用同樣的方式實作。

如果你理解了以上內容，你其實已經知道那些安全性工具在底層是如何運作的。

///

## 限制相依的並行數 { #limit-dependency-concurrency }

在某些情況下，你可能想限制同時能使用某個相依的請求數量。

例如，你的資料庫可能只有有限的可用連線。你可以讓新的請求在建立 session 之前等待，直到另一個請求使用完它的 session。

你可以透過 `Depends()` 中的 `max_concurrency` 來達成這點。

讓我們更新 [SQL 資料庫教學](../tutorial/sql-databases.md)中的 `SessionDep` 別名：

```Python
SessionDep = Annotated[Session, Depends(get_session, max_concurrency=5)]
```

現在，同一時間最多有**五個請求**能透過這個相依保持資料庫 session 開啟。

如果另一個請求需要 session，它會等待，直到其中一個 session 關閉。

等待期間，它**不會占用工作執行緒**，因此這些執行緒可以用來執行其他程式碼。

這個值必須是正整數。預設值為 `None`，表示 FastAPI 不會限制該相依同時執行的次數。

### 在路由之間共用限制 { #share-the-limit-between-routes }

該範例中的所有路由都使用相同的 `SessionDep` 別名，因此它們共用五個 session 的限制。

若要共用限制，請重複使用**同一個 `Depends()` 物件**，例如將它放在像這樣的 `Annotated` 別名中。

如果你為每個路由各自撰寫一個新的 `Depends(get_session, max_concurrency=5)`，每個路由都會有各自的五個 session 限制。即使它們都使用相同的 `get_session` 函式，也是如此。

在另一個應用中重複使用同一個 `SessionDep` 也會共用限制，只要兩個應用在同一個事件迴圈中執行。這也包含掛載的應用。

例如，如果兩個應用對同一個資料庫連線池使用這個 `SessionDep`，它們透過這個相依開啟的 session 合計最多只能有五個。

如果應用使用不同的連線池，且需要各自獨立的限制，請為每個應用建立獨立的 `Depends()` 物件。

### 關閉 session 後才允許建立下一個 { #close-the-session-before-allowing-another-one }

在這個範例中，`get_session` 使用 `yield`。在結束程式碼完成關閉 session 之前，該 session 都會計入限制。

相依的 `scope` 決定結束程式碼何時執行：

* 使用預設的 `scope="request"` 時，它會在回應送出之後執行。
* 使用 `scope="function"` 時，它會在「路徑操作函式」執行完畢後、發送回應之前執行。

你可以閱讀更多關於[提前結束與 scope](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope) 的說明。

對於不含 `yield` 的相依，該次呼叫只會在函式執行完畢之前計入限制。

如果你在 WebSocket 處理函式中使用含有 `yield` 的相依，它會持續計入限制，直到處理函式結束，且相依的結束程式碼執行完畢。

/// note | 注意

重複使用[快取的相依值](../tutorial/dependencies/sub-dependencies.md#using-the-same-dependency-multiple-times)不會再次計入限制。如果不同的宣告共用該值，只有實際呼叫相依的宣告才會計入它的限制。

///

### 為你的應用選擇限制 { #choose-a-limit-for-your-application }

請根據這些 session 可用的資料庫連線數量，選擇合適的限制。

如果應用的其他部分也會使用這些連線，請同樣為它們預留空間。FastAPI 不知道你的資料庫連線池大小。

每個工作處理程序都有各自的限制。例如，兩個使用這個相依的工作處理程序，合計最多可以開啟十個 session。

/// note | 技術細節

每個事件迴圈的限制也各自獨立。在不同事件迴圈中執行的應用不會共用限制，即使它們重複使用同一個 `Depends()` 物件也是如此。

///

### 需要多個資源的相依 { #dependencies-that-need-more-than-one-resource }

FastAPI 會先執行相依的子相依，再套用該相依的限制。

因此，若要限制資料庫 session 的數量，請將 `max_concurrency` 設定在建立 session 的 `Depends(get_session, ...)` 上。

如果請求仍持有一個直到請求結束才會關閉的 session，卻又需要另一個 session，就可能卡住。

例如，假設同一個請求中使用了兩次共用的 `Depends(get_session, max_concurrency=1, use_cache=False)`。

第一次呼叫會建立 session。第二次呼叫會等待它關閉。但第一個 session 必須等到請求結束才能關閉，而請求卻正在等待第二次呼叫。

如果一個請求持有 session 並等待另一個資源，而另一個請求持有該資源並等待 session，這兩個請求也可能卡住。

如果你的請求需要多個資源，請以相同的順序取得它們。FastAPI 會分別套用每個限制，不會事先保留請求所需的所有資源。

## 同時含有 `yield`、`HTTPException`、`except` 與背景任務的相依 { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning | 警告

你很可能不需要這些技術細節。

這些細節主要在於：如果你有一個 0.121.0 之前的 FastAPI 應用，並且在使用含有 `yield` 的相依時遇到問題，會對你有幫助。

///

含有 `yield` 的相依隨著時間演進，以涵蓋不同的使用情境並修正一些問題。以下是變更摘要。

### 含有 `yield` 與 `scope` 的相依 { #dependencies-with-yield-and-scope }

在 0.121.0 版中，FastAPI 為含有 `yield` 的相依加入了 `Depends(scope="function")` 的支援。

使用 `Depends(scope="function")` 時，`yield` 之後的結束程式碼會在「路徑操作函式」執行完畢後立刻執行，在回應發送回客戶端之前。

而當使用 `Depends(scope="request")`（預設值）時，`yield` 之後的結束程式碼會在回應送出之後才執行。

你可以在文件中閱讀更多：[含有 `yield` 的相依 - 提前結束與 `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope)。

### 含有 `yield` 與 `StreamingResponse` 的相依，技術細節 { #dependencies-with-yield-and-streamingresponse-technical-details }

在 FastAPI 0.118.0 之前，如果你使用含有 `yield` 的相依，它會在「路徑操作函式」回傳之後、發送回應之前，執行結束程式碼。

這樣做的用意是避免在等待回應穿越網路時，比必要的時間更久地占用資源。

但這也意味著，如果你回傳的是 `StreamingResponse`，該含有 `yield` 的相依的結束程式碼早已執行完畢。

例如，如果你在含有 `yield` 的相依中使用了一個資料庫 session，`StreamingResponse` 在串流資料時將無法使用該 session，因為它已在 `yield` 之後的結束程式碼中被關閉了。

這個行為在 0.118.0 被還原，使得 `yield` 之後的結束程式碼會在回應送出之後才被執行。

/// note | 注意

如下所見，這與 0.106.0 之前的行為非常類似，但對一些邊界情況做了多項改進與錯誤修正。

///

#### 需要提早執行結束程式碼的情境 { #use-cases-with-early-exit-code }

有些特定條件的使用情境，可能會受益於舊行為（在送出回應之前執行含有 `yield` 的相依的結束程式碼）。

例如，假設你在含有 `yield` 的相依中只用資料庫 session 來驗證使用者，而這個 session 之後並未在「路徑操作函式」中使用，僅在相依中使用，且回應需要很長時間才會送出，例如一個慢速傳送資料的 `StreamingResponse`，但它並沒有使用資料庫。

在這種情況下，資料庫 session 會一直被保留到回應傳送完畢為止，但如果你根本不會用到它，就沒有必要一直持有它。

可能會像這樣：

{* ../../docs_src/dependencies/tutorial013.py *}

結束程式碼（自動關閉 `Session`）在：

{* ../../docs_src/dependencies/tutorial013.py ln[19:21] *}

...會在回應完成傳送這些慢速資料後才執行：

{* ../../docs_src/dependencies/tutorial013.py ln[30:38] hl[31:33] *}

但因為 `generate_stream()` 並未使用資料庫 session，實際上不需要在傳送回應時保持 session 開啟。

如果你用的是 SQLModel（或 SQLAlchemy）且有這種特定情境，你可以在不再需要時明確關閉該 session：

{* ../../docs_src/dependencies/tutorial014.py ln[24:28] hl[28] *}

如此一來，該 session 就會釋放資料庫連線，讓其他請求可以使用。

如果你有不同的情境，需要從含有 `yield` 的相依中提早結束，請建立一個 [GitHub 討論問題](https://github.com/fastapi/fastapi/discussions/new?category=questions)，描述你的具體情境，以及為何提早關閉含有 `yield` 的相依對你有幫助。

如果有令人信服的案例需要在含有 `yield` 的相依中提前關閉，我會考慮加入一種新的選項，讓你可以選擇性啟用提前關閉。

### 含有 `yield` 與 `except` 的相依，技術細節 { #dependencies-with-yield-and-except-technical-details }

在 FastAPI 0.110.0 之前，如果你使用含有 `yield` 的相依，並且在該相依中用 `except` 捕捉到例外，且沒有再次拋出，那個例外會自動被拋出／轉交給任何例外處理器或內部伺服器錯誤處理器。

在 0.110.0 版本中，這被修改以修復沒有處理器（內部伺服器錯誤）而被轉交的例外所造成的未處理記憶體消耗，並使其行為與一般 Python 程式碼一致。

### 背景任務與含有 `yield` 的相依，技術細節 { #background-tasks-and-dependencies-with-yield-technical-details }

在 FastAPI 0.106.0 之前，不可能在 `yield` 之後拋出例外；含有 `yield` 的相依的結束程式碼會在回應送出之後才執行，因此[例外處理器](../tutorial/handling-errors.md#install-custom-exception-handlers) 早就已經跑完了。

當初這樣設計主要是為了允許在背景任務中使用由相依「yield」出來的同一組物件，因為結束程式碼會在背景任務結束後才執行。

在 FastAPI 0.106.0 中，這個行為被修改，目的是在等待回應穿越網路的期間，不要持有資源。

/// tip | 提示

此外，背景任務通常是一組獨立的邏輯，應該用自己的資源（例如自己的資料庫連線）來處理。

這樣你的程式碼通常會更乾淨。

///

如果你先前依賴這種行為，現在應該在背景任務本身裡建立所需資源，並且只使用不依賴含有 `yield` 的相依之資源的資料。

例如，不要共用同一個資料庫 session，而是在背景任務中建立一個新的資料庫 session，並用這個新的 session 從資料庫取得物件。接著，在呼叫背景任務函式時，不是傳遞資料庫物件本身，而是傳遞該物件的 ID，然後在背景任務函式內再透過這個 ID 取得物件。
