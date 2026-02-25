# 背景任務 { #background-tasks }

你可以定義背景任務，讓它們在傳回回應之後執行。

這對於那些需要在請求之後發生、但用戶端其實不必在收到回應前等它完成的操作很有用。

例如：

* 在執行某個動作後發送電子郵件通知：
    * 由於連線到郵件伺服器並寄送郵件通常較「慢」（數秒），你可以先立即回應，並在背景中發送郵件通知。
* 處理資料：
    * 例如，收到一個需要經過較慢處理流程的檔案時，你可以先回應「Accepted」（HTTP 202），再在背景處理該檔案。

## 使用 `BackgroundTasks` { #using-backgroundtasks }

首先，匯入 `BackgroundTasks`，並在你的路徑操作函式中定義一個型別為 `BackgroundTasks` 的參數：

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[1,13] *}

**FastAPI** 會為你建立 `BackgroundTasks` 物件，並以該參數傳入。

## 建立任務函式 { #create-a-task-function }

建立一個作為背景任務執行的函式。

它只是個可接收參數的一般函式。

它可以是 `async def`，也可以是一般的 `def`，**FastAPI** 都能正確處理。

在此例中，任務函式會寫入檔案（模擬寄送電子郵件）。

由於寫入操作未使用 `async` 與 `await`，因此以一般的 `def` 定義該函式：

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[6:9] *}

## 新增背景任務 { #add-the-background-task }

在路徑操作函式內，使用 `.add_task()` 將任務函式加入背景任務物件：

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[14] *}

`.add_task()` 的引數包括：

* 要在背景執行的任務函式（`write_notification`）。
* 依序傳給任務函式的位置引數（`email`）。
* 要傳給任務函式的關鍵字引數（`message="some notification"`）。

## 相依性注入 { #dependency-injection }

在相依性注入系統中也可使用 `BackgroundTasks`。你可以在多個層級宣告 `BackgroundTasks` 型別的參數：路徑操作函式、相依項（dependable）、次級相依項等。

**FastAPI** 會在各種情況下正確處理並重用同一個物件，將所有背景任務合併，並在之後於背景執行：

{* ../../docs_src/background_tasks/tutorial002_an_py310.py hl[13,15,22,25] *}

在此範例中，訊息會在回應送出之後寫入 `log.txt` 檔案。

如果請求中有查詢參數，會以背景任務寫入日誌。

接著，在路徑操作函式中建立的另一個背景任務會使用 `email` 路徑參數寫入訊息。

## 技術細節 { #technical-details }

類別 `BackgroundTasks` 直接來自 <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">`starlette.background`</a>。

它被直接匯入/包含到 FastAPI 中，因此你可以從 `fastapi` 匯入它，並避免不小心從 `starlette.background` 匯入另一個同名的 `BackgroundTask`（結尾沒有 s）。

只使用 `BackgroundTasks`（而非 `BackgroundTask`）時，你就能把它當作路徑操作函式的參數，並讓 **FastAPI** 幫你處理其餘部分，就像直接使用 `Request` 物件一樣。

在 FastAPI 中仍可單獨使用 `BackgroundTask`，但你需要在程式碼中自行建立該物件，並回傳包含它的 Starlette `Response`。

更多細節請參閱 <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">Starlette 官方的 Background Tasks 文件</a>。

## 注意事項 { #caveat }

如果你需要執行繁重的背景計算，且不一定要由同一個行程執行（例如不需要共用記憶體、變數等），可以考慮使用更大型的工具，例如 <a href="https://docs.celeryq.dev" class="external-link" target="_blank">Celery</a>。

這類工具通常需要較複雜的設定，以及訊息/工作佇列管理器（如 RabbitMQ 或 Redis），但它們允許你在多個行程，甚至多台伺服器上執行背景任務。

但如果你需要存取同一個 **FastAPI** 應用中的變數與物件，或只需執行小型的背景任務（例如寄送郵件通知），僅使用 `BackgroundTasks` 即可。

## 重點回顧 { #recap }

在路徑操作函式與相依項中匯入並使用 `BackgroundTasks` 參數，以新增背景任務。
