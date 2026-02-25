# 生命週期事件 { #lifespan-events }

你可以定義在應用程式**啟動**之前要執行的邏輯（程式碼）。也就是說，這段程式碼會在應用開始接收請求**之前**、**只執行一次**。

同樣地，你也可以定義在應用程式**關閉**時要執行的邏輯（程式碼）。在這種情況下，這段程式碼會在處理了**許多請求**之後、**只執行一次**。

因為這些程式碼分別在應用開始接收請求**之前**與**完成**處理請求之後執行，所以涵蓋了整個應用的**生命週期**（「lifespan」這個詞稍後會很重要 😉）。

這對於為整個應用設定需要**共用**於多個請求的**資源**，以及在之後進行**清理**，非常有用。比如資料庫連線池、或載入一個共用的機器學習模型。

## 使用情境 { #use-case }

先從一個**使用情境**開始，然後看看如何用這個機制解決。

想像你有一些要用來處理請求的**機器學習模型**。🤖

同一組模型會在多個請求間共用，所以不是每個請求或每個使用者各有一個模型。

再想像一下，載入模型**需要一段時間**，因為它必須從**磁碟**讀取大量資料。所以你不想在每個請求都做一次。

你可以在模組／檔案的最上層載入，但這也表示即使只是要跑一個簡單的自動化測試，也會去**載入模型**，導致測試**變慢**，因為它得等模型載入完才能執行與模型無關的程式碼部分。

我們要解決的正是這件事：在開始處理請求之前再載入模型，但只在應用程式即將開始接收請求時載入，而不是在匯入程式碼時就載入。

## 生命週期（Lifespan） { #lifespan }

你可以使用 `FastAPI` 應用的 `lifespan` 參數，搭配「context manager」（稍後會示範），來定義這些 *startup* 與 *shutdown* 邏輯。

先看一個例子，接著再深入說明。

我們建立一個帶有 `yield` 的非同步函式 `lifespan()`，如下：

{* ../../docs_src/events/tutorial003_py310.py hl[16,19] *}

這裡我們透過在 `yield` 之前把（假的）模型函式放進機器學習模型的字典中，來模擬昂貴的 *startup* 載入模型操作。這段程式會在應用**開始接收請求之前**執行，也就是 *startup* 階段。

接著，在 `yield` 之後，我們卸載模型。這段程式會在應用**完成處理請求之後**、也就是 *shutdown* 前執行。這可以用來釋放資源，例如記憶體或 GPU。

/// tip

`shutdown` 會在你**停止**應用程式時發生。

也許你要啟動新版本，或只是不想再跑它了。🤷

///

### Lifespan 函式 { #lifespan-function }

首先要注意的是，我們定義了一個帶有 `yield` 的 async 函式。這和帶有 `yield` 的依賴（Dependencies）非常相似。

{* ../../docs_src/events/tutorial003_py310.py hl[14:19] *}

函式在 `yield` 之前的部分，會在應用啟動前先執行。

`yield` 之後的部分，會在應用結束後再執行。

### 非同步內容管理器（Async Context Manager） { #async-context-manager }

你會看到這個函式被 `@asynccontextmanager` 裝飾。

它會把函式轉換成所謂的「**非同步內容管理器（async context manager）**」。

{* ../../docs_src/events/tutorial003_py310.py hl[1,13] *}

Python 中的**內容管理器（context manager）**可以用在 `with` 陳述式中，例如 `open()` 可以作為內容管理器使用：

```Python
with open("file.txt") as file:
    file.read()
```

在較新的 Python 版本中，也有**非同步內容管理器**。你可以用 `async with` 來使用它：

```Python
async with lifespan(app):
    await do_stuff()
```

當你像上面那樣建立一個內容管理器或非同步內容管理器時，在進入 `with` 區塊之前，會先執行 `yield` 之前的程式碼；離開 `with` 區塊之後，會執行 `yield` 之後的程式碼。

在我們的範例中，並不是直接用它，而是把它傳給 FastAPI 來使用。

`FastAPI` 應用的 `lifespan` 參數需要一個**非同步內容管理器**，所以我們可以把剛寫好的 `lifespan` 非同步內容管理器傳給它。

{* ../../docs_src/events/tutorial003_py310.py hl[22] *}

## 替代事件（已棄用） { #alternative-events-deprecated }

/// warning

目前建議使用上面所述，透過 `FastAPI` 應用的 `lifespan` 參數來處理 *startup* 與 *shutdown*。如果你提供了 `lifespan` 參數，`startup` 與 `shutdown` 事件處理器將不會被呼叫。要嘛全用 `lifespan`，要嘛全用事件，不能同時混用。

你大概可以直接跳過這一節。

///

也有另一種方式可以定義在 *startup* 與 *shutdown* 期間要執行的邏輯。

你可以定義事件處理器（函式）來在應用啟動前或關閉時執行。

這些函式可以用 `async def` 或一般的 `def` 宣告。

### `startup` 事件 { #startup-event }

要加入一個在應用啟動前執行的函式，使用事件 `"startup"` 來宣告：

{* ../../docs_src/events/tutorial001_py310.py hl[8] *}

在這個例子中，`startup` 事件處理器函式會用一些值來初始化 items 的「資料庫」（其實就是個 `dict`）。

你可以註冊多個事件處理函式。

而且在所有 `startup` 事件處理器都完成之前，你的應用不會開始接收請求。

### `shutdown` 事件 { #shutdown-event }

要加入一個在應用關閉時執行的函式，使用事件 `"shutdown"` 來宣告：

{* ../../docs_src/events/tutorial002_py310.py hl[6] *}

在這裡，`shutdown` 事件處理器函式會把一行文字 `"Application shutdown"` 寫入檔案 `log.txt`。

/// info

在 `open()` 函式中，`mode="a"` 表示「append（附加）」；也就是說，這行文字會加在檔案現有內容之後，而不會覆寫先前的內容。

///

/// tip

注意這裡我們使用的是標準 Python 的 `open()` 函式來操作檔案。

這涉及 I/O（輸入／輸出），也就是需要「等待」資料寫入磁碟。

但 `open()` 並不使用 `async` 與 `await`。

所以我們用一般的 `def` 來宣告事件處理器，而不是 `async def`。

///

### 同時使用 `startup` 與 `shutdown` { #startup-and-shutdown-together }

你的 *startup* 與 *shutdown* 邏輯很可能是相關聯的：你可能會先啟動某個東西再把它結束、先取得資源再釋放它，等等。

如果把它們拆成兩個彼此不共享邏輯或變數的獨立函式，會比較麻煩，你得把值存在全域變數或用其他技巧。

因此，現在建議改用上面介紹的 `lifespan`。

## 技術細節 { #technical-details }

給有興趣鑽研的同好一點技術細節。🤓

在底層的 ASGI 技術規範中，這屬於 <a href="https://asgi.readthedocs.io/en/latest/specs/lifespan.html" class="external-link" target="_blank">Lifespan Protocol</a> 的一部分，並定義了 `startup` 與 `shutdown` 兩種事件。

/// info

你可以在 <a href="https://www.starlette.dev/lifespan/" class="external-link" target="_blank">Starlette 的 Lifespan 文件</a> 讀到更多關於 Starlette `lifespan` 處理器的資訊。

也包含如何處理可在程式其他區域使用的 lifespan 狀態。

///

## 子應用程式 { #sub-applications }

🚨 請記住，這些生命週期事件（startup 與 shutdown）只會在主應用程式上執行，不會在[子應用程式 - 掛載](sub-applications.md){.internal-link target=_blank}上執行。
