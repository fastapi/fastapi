# FastAPI CLI { #fastapi-cli }

**FastAPI CLI** 是一個命令列程式，能用來運行你的 FastAPI 應用程式、管理你的 FastAPI 專案等。

當你安裝 FastAPI（例如使用 `pip install "fastapi[standard]"`），它會包含一個叫做 `fastapi-cli` 的套件，這個套件提供了 `fastapi` 命令。

要運行你的 FastAPI 應用程式來進行開發，你可以使用 `fastapi dev` 命令：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

名為 `fastapi` 的命令列程式就是 **FastAPI CLI**。

FastAPI CLI 接收你的 Python 程式路徑（例如 `main.py`），並自動檢測 `FastAPI` 實例（通常命名為 `app`），確定正確的引入模組流程，然後運行該應用程式。

在生產環境，你應該使用 `fastapi run` 命令。 🚀

**FastAPI CLI** 內部使用了 <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>，這是一個高效能、適合生產環境的 ASGI 伺服器。 😎

## `fastapi dev` { #fastapi-dev }

執行 `fastapi dev` 會啟動開發模式。

預設情況下，**auto-reload** 功能是啟用的，當你對程式碼進行修改時，伺服器會自動重新載入。這會消耗較多資源，並且可能比禁用時更不穩定。因此，你應該只在開發環境中使用此功能。它也會在 IP 位址 `127.0.0.1` 上監聽，這是用於你的機器與自身通訊的 IP 位址（`localhost`）。

## `fastapi run` { #fastapi-run }

執行 `fastapi run` 會以生產模式啟動 FastAPI。

預設情況下，**auto-reload** 功能是禁用的。它也會在 IP 位址 `0.0.0.0` 上監聽，表示會監聽所有可用的 IP 位址，這樣任何能與該機器通訊的人都可以公開存取它。這通常是你在生產環境中運行應用程式的方式，例如在容器中運行時。

在大多數情況下，你會（也應該）有一個「終止代理」在外層幫你處理 HTTPS；這取決於你如何部署應用程式，你的服務供應商可能會幫你處理，或者你需要自己設置。

/// tip

你可以在[部署文件](deployment/index.md){.internal-link target=_blank}中了解更多相關資訊。

///
