# 靜態檔案 { #static-files }

你可以使用 `StaticFiles` 從某個目錄自動提供靜態檔案。

## 使用 `StaticFiles` { #use-staticfiles }

- 匯入 `StaticFiles`。
- 在特定路徑上「掛載」一個 `StaticFiles()` 實例。

{* ../../docs_src/static_files/tutorial001_py310.py hl[2,6] *}

/// note | 技術細節

你也可以使用 `from starlette.staticfiles import StaticFiles`。

**FastAPI** 為了方便開發者，提供與 `starlette.staticfiles` 相同的介面作為 `fastapi.staticfiles`。但它其實是直接來自 Starlette。

///

### 什麼是「掛載」 { #what-is-mounting }

「掛載（mounting）」是指在特定路徑下加入一個完整且「獨立」的應用，之後所有該路徑下的子路徑都由它處理。

這與使用 `APIRouter` 不同，因為被掛載的應用是完全獨立的。主應用的 OpenAPI 與文件不會包含掛載應用的任何內容，等等。

你可以在[進階使用者指南](../advanced/index.md){.internal-link target=_blank}中閱讀更多相關內容。

## 細節 { #details }

第一個 `"/static"` 指的是這個「子應用」要被「掛載」的子路徑。因此，任何以 `"/static"` 開頭的路徑都會由它處理。

`directory="static"` 指向包含你靜態檔案的目錄名稱。

`name="static"` 為它指定一個可供 **FastAPI** 內部使用的名稱。

以上參數都不一定要是 "`static`"，請依你的應用需求與細節調整。

## 更多資訊 { #more-info }

如需更多細節與選項，請參考 <a href="https://www.starlette.dev/staticfiles/" class="external-link" target="_blank">Starlette 關於靜態檔案的文件</a>。
