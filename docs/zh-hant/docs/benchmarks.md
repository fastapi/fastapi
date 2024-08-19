# 基準測試

由第三方機構 TechEmpower 的基準測試表明在 Uvicorn 下運行的 **FastAPI** 應用程式是 <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">最快的 Python 可用框架之一</a>，僅次於 Starlette 和 Uvicorn 本身（於 FastAPI 內部使用）。

但是在查看基準得分和對比時，請注意以下幾點。

## 基準測試和速度

當你查看基準測試時，時常會見到幾個不同類型的工具被同時進行測試。

具體來說，是將 Uvicorn、Starlette 和 FastAPI 同時進行比較（以及許多其他工具）。

該工具解決的問題越簡單，其效能就越好。而且大多數基準測試不會測試該工具提供的附加功能。

層次結構如下：

* **Uvicorn**：ASGI 伺服器
    * **Starlette**：（使用 Uvicorn）一個網頁微框架
        * **FastAPI**：（使用 Starlette）一個 API 微框架，具有用於建立 API 的多個附加功能、資料驗證等。

* **Uvicorn**：
    * 具有最佳效能，因為除了伺服器本身之外，它沒有太多額外的程式碼。
    * 你不會直接在 Uvicorn 中編寫應用程式。這意味著你的程式碼必須或多或少地包含 Starlette（或 **FastAPI**）提供的所有程式碼。如果你這樣做，你的最終應用程式將具有與使用框架相同的開銷並最大限度地減少應用程式程式碼和錯誤。
    * 如果你要比較 Uvicorn，請將其與 Daphne、Hypercorn、uWSGI 等應用程式伺服器進行比較。
* **Starlette**：
    * 繼 Uvicorn 之後的次佳表現。事實上，Starlette 使用 Uvicorn 來運行。因此它將可能只透過執行更多程式碼而變得比 Uvicorn「慢」。
    * 但它為你提供了建立簡單網頁應用程式的工具，以及基於路徑的路由等。
    * 如果你要比較 Starlette，請將其與 Sanic、Flask、Django 等網頁框架（或微框架）進行比較。
* **FastAPI**：
    * 就像 Starlette 使用 Uvicorn 並不能比它更快一樣， **FastAPI** 使用 Starlette，所以它不能比它更快。
    * FastAPI 在 Starlette 基礎之上提供了更多功能。包含建構 API 時所需要的功能，例如資料驗證和序列化。FastAPI 可以幫助你自動產生 API 文件，（應用程式啟動時將會自動生成文件，所以不會增加應用程式運行時的開銷）。
    * 如果你沒有使用 FastAPI 而是直接使用 Starlette（或其他工具，如 Sanic、Flask、Responder 等），你將必須自行實現所有資料驗證和序列化。因此，你的最終應用程式仍然具有與使用 FastAPI 建置相同的開銷。在許多情況下，這種資料驗證和序列化是應用程式中編寫最大量的程式碼。
    * 因此透過使用 FastAPI，你可以節省開發時間、錯誤與程式碼數量，並且相比不使用 FastAPI 你很大可能會獲得相同或更好的效能（因為那樣你必須在程式碼中實現所有相同的功能）。
    * 如果你要與 FastAPI 比較，請將其與能夠提供資料驗證、序列化和文件的網頁應用程式框架（或工具集）進行比較，例如 Flask-apispec、NestJS、Molten 等框架。
