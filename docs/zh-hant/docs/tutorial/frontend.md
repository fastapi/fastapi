# 前端 { #frontend }

你可以使用 `app.frontend()`（或 `router.frontend()`）來提供靜態前端應用程式。

這對會產生靜態檔案的前端工具很有用，例如搭配 Vite 的 React、TanStack Router、Astro、Vue、Svelte、Angular、Solid 等。

使用這些工具時，你通常會有一個建置前端的步驟，使用像這樣的指令：

```bash
npm run build
```

那會產生像 `./dist/` 這樣的目錄，裡面包含你的前端檔案。

你可以使用 `app.frontend()` 依照這些前端框架所需的慣例來提供該目錄。

**FastAPI** 會先檢查*路徑操作*。只有在沒有一般路由符合時，才會檢查前端檔案，因此你的 API 不會受到影響。

## 提供前端 { #serve-a-frontend }

在建置前端之後，例如使用 `npm run build`，將產生的檔案放在某個目錄中，例如 `dist`。

你的專案結構可能如下：

```text
.
├── pyproject.toml
├── app
│   ├── __init__.py
│   └── main.py
└── dist
    ├── index.html
    └── assets
        └── app.js
```

然後使用 `app.frontend()` 來提供它：

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

如此一來，對 `/assets/app.js` 的請求就可以提供 `dist/assets/app.js`。

如果你也有 **FastAPI** *路徑操作*，則*路徑操作*會優先。

## 用戶端路由 { #client-side-routing }

許多前端應用程式，包括 **single-page apps**（SPAs），都會使用用戶端路由。像 `/dashboard/settings` 這樣的路徑可能不是真實檔案，而是由框架負責處理。

因此，如果直接存取該 URL（而不是透過應用程式內導覽），後端應該從 `index.html` 提供前端應用程式，讓前端框架接著處理用戶端路由。

為此，請使用 `fallback="index.html"`：

{* ../../docs_src/frontend/tutorial002_py310.py hl[5] *}

**FastAPI** 只會對看起來像瀏覽器導覽的 `GET` 和 `HEAD` 請求使用這個 fallback。遺失的檔案，例如 JavaScript、CSS 和圖片，仍會回傳 `404`。

對於只符合前端 fallback 的路徑，使用其他方法的請求，例如 `POST` 或 `PUT`，也會回傳 `404`。一般的 **FastAPI** *路徑操作*仍然比前端路由有更高優先順序。

/// tip

預設情況下，`fallback` 的值是 `fallback="auto"`。在大多數情況下，你不需要指定 `fallback`。請閱讀下方內容以了解詳細資訊。

///

這正是許多使用用戶端路由的前端應用程式所需要的行為，例如搭配 TanStack Router 的 React、Vue、Angular、SvelteKit 或 Solid。

## 自訂 404 頁面 { #custom-404-page }

你也可以為遺失的前端路徑提供靜態 `404.html` 頁面：

{* ../../docs_src/frontend/tutorial003_py310.py hl[5] *}

該回應會保留 `404` 狀態碼。

在這種情況下，**FastAPI** 不會為遺失的前端路徑提供 `index.html`。它會改為回傳 `404.html` 檔案。

/// tip

預設情況下，`fallback` 的值是 `fallback="auto"`。如此一來，如果找到 `404.html` 檔案，就會自動將其用作 fallback。

因此，你通常可以省略 `fallback` 引數。

///

這對會為每個頁面產生靜態 HTML 檔案的前端工具很有用，例如 Astro。

## 自動 Fallback { #fallback-auto }

預設情況下，`app.frontend()` 會使用 `fallback="auto"`。

如果前端目錄中有 `404.html` 檔案，遺失的前端路徑會提供該檔案，並使用狀態碼 `404`。

否則，如果有 `index.html` 檔案，遺失的瀏覽器導覽路徑會提供 `index.html`，這正是許多使用用戶端路由的前端應用程式所預期的行為。

因此，在大多數情況下，你可以使用 `app.frontend("/", directory="dist")`，而不需要指定 `fallback` 引數。

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

## 停用 Fallback { #disable-fallback }

如果你不想為遺失的前端路徑提供 fallback 檔案，請使用 `fallback=None`：

{* ../../docs_src/frontend/tutorial005_py310.py hl[5] *}

接著，遺失的前端路徑會回傳一般的 `404`。

## 檢查目錄 { #check-directory }

預設情況下，`app.frontend()` 會在建立應用程式時檢查目錄是否存在。

這有助於及早發現設定錯誤。例如，如果缺少前端建置輸出目錄，**FastAPI** 會在啟動時引發錯誤。

如果你的前端檔案稍後才會建立，例如在建立 app 物件之後由另一個建置步驟產生，請設定 `check_dir=False`：

{* ../../docs_src/frontend/tutorial006_py310.py hl[5] *}

使用 `check_dir=False` 時，**FastAPI** 不會在建立應用程式時檢查目錄。如果在處理請求時，設定的目錄仍然不存在，**FastAPI** 會在那時引發錯誤。

## 與 `APIRouter` 搭配使用 { #use-it-with-apirouter }

你也可以將前端檔案加入 `APIRouter`，並使用前綴包含它：

{* ../../docs_src/frontend/tutorial004_py310.py hl[6,7] *}

在這個範例中，前端路徑會在 `/app` 底下提供。

應用程式中的任何一般*路徑操作*仍會優先，包括其他 router 中的路徑操作。

## 依賴項與中介軟體 { #dependencies-and-middleware }

前端回應會在一般的 **FastAPI** 應用程式內執行，因此 HTTP middleware 會套用到它們。

來自 app、`APIRouter` 和 `include_router()` 的 dependencies 也會套用到前端回應。這對使用 cookie authentication 或類似方式保護前端很有用。

## 僅限靜態建置輸出 { #static-build-output-only }

`app.frontend()` 會提供你的前端建置已經產生的檔案。

它不會執行 server-side rendering。它適用於會產生靜態檔案的前端框架，不適用於需要在伺服器上為每個請求進行動態 rendering 的框架。
