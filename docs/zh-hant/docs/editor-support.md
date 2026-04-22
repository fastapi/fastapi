# 編輯器支援 { #editor-support }

官方的 [FastAPI 擴充套件](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode) 透過支援路徑操作（path operation）探索、導覽，以及 FastAPI Cloud 部署與即時日誌串流，強化你的 FastAPI 開發流程。

想了解更多關於此擴充套件的細節，請參考其 [GitHub 儲存庫](https://github.com/fastapi/fastapi-vscode) 中的 README。

## 安裝與設定 { #setup-and-installation }

**FastAPI 擴充套件** 同時提供給 [VS Code](https://code.visualstudio.com/) 與 [Cursor](https://www.cursor.com/)。你可以在各編輯器的擴充套件面板中直接安裝：搜尋「FastAPI」，並選擇由 **FastAPI Labs** 發佈的擴充套件。此擴充套件同樣可在瀏覽器版編輯器（如 [vscode.dev](https://vscode.dev) 與 [github.dev](https://github.dev)）中使用。

### 應用程式探索 { #application-discovery }

預設情況下，擴充套件會自動在你的工作區中，掃描會實例化 `FastAPI()` 的檔案，以發現 FastAPI 應用程式。若自動偵測無法因應你的專案結構，你可以在 `pyproject.toml` 的 `[tool.fastapi]` 中，或在 VS Code 設定的 `fastapi.entryPoint` 中，使用模組標記法（例如 `myapp.main:app`）指定入口點。

## 功能 { #features }

- **Path Operation Explorer** - 顯示應用程式中所有 <dfn title="路由、端點">*路徑操作*</dfn> 的側邊欄樹狀檢視。點擊即可跳至任一路由或 router 定義。
- **Route Search** - 使用 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>（macOS：<kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>）依路徑、方法或名稱進行搜尋。
- **CodeLens Navigation** - 在測試用 client 呼叫（例如 `client.get('/items')`）上方提供可點連結，一鍵跳至對應的路徑操作，讓你在測試與實作間快速切換。
- **Deploy to FastAPI Cloud** - 一鍵將你的應用程式部署到 [FastAPI Cloud](https://fastapicloud.com/)。
- **Stream Application Logs** - 從部署於 FastAPI Cloud 的應用程式即時串流日誌，並支援層級篩選與文字搜尋。

若你想熟悉此擴充套件的功能，可開啟命令面板（<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>；macOS：<kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>），選擇 "Welcome: Open walkthrough..."，然後挑選 "Get started with FastAPI" walkthrough。
