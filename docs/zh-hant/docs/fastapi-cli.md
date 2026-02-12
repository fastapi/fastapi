# FastAPI CLI

**FastAPI CLI** 是一個命令列程式，能用來運行你的 FastAPI 應用程式、管理你的 FastAPI 專案等。

當你安裝 FastAPI（例如使用 `pip install "fastapi[standard]"`），它會包含一個叫做 `fastapi-cli` 的套件，這個套件提供了 `fastapi` 命令。

要運行你的 FastAPI 應用程式來進行開發，你可以使用 `fastapi dev` 命令：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:single">main.py</u>
<font color="#3465A4">INFO    </font> Using path <font color="#3465A4">main.py</font>
<font color="#3465A4">INFO    </font> Resolved absolute path <font color="#75507B">/home/user/code/awesomeapp/</font><font color="#AD7FA8">main.py</font>
<font color="#3465A4">INFO    </font> Searching for package file structure from directories with <font color="#3465A4">__init__.py</font> files
<font color="#3465A4">INFO    </font> Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

 ╭─ <font color="#8AE234"><b>Python module file</b></font> ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯

<font color="#3465A4">INFO    </font> Importing module <font color="#4E9A06">main</font>
<font color="#3465A4">INFO    </font> Found importable FastAPI app

 ╭─ <font color="#8AE234"><b>Importable FastAPI app</b></font> ─╮
 │                          │
 │  <span style="background-color:#272822"><font color="#FF4689">from</font></span><span style="background-color:#272822"><font color="#F8F8F2"> main </font></span><span style="background-color:#272822"><font color="#FF4689">import</font></span><span style="background-color:#272822"><font color="#F8F8F2"> app</font></span><span style="background-color:#272822">  </span>  │
 │                          │
 ╰──────────────────────────╯

<font color="#3465A4">INFO    </font> Using import string <font color="#8AE234"><b>main:app</b></font>

 <span style="background-color:#C4A000"><font color="#2E3436">╭────────── FastAPI CLI - Development mode ───────────╮</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Serving at: http://127.0.0.1:8000                  │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  API docs: http://127.0.0.1:8000/docs               │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Running in development mode, for production use:   │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  </font></span><span style="background-color:#C4A000"><font color="#555753"><b>fastapi run</b></font></span><span style="background-color:#C4A000"><font color="#2E3436">                                        │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">╰─────────────────────────────────────────────────────╯</font></span>

<font color="#4E9A06">INFO</font>:     Will watch for changes in these directories: [&apos;/home/user/code/awesomeapp&apos;]
<font color="#4E9A06">INFO</font>:     Uvicorn running on <b>http://127.0.0.1:8000</b> (Press CTRL+C to quit)
<font color="#4E9A06">INFO</font>:     Started reloader process [<font color="#34E2E2"><b>2265862</b></font>] using <font color="#34E2E2"><b>WatchFiles</b></font>
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">2265873</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
```

</div>

`fastapi` 命令列程式就是 **FastAPI CLI**。

FastAPI CLI 接收你的 Python 程式路徑（例如 `main.py`），並自動檢測 FastAPI 實例（通常命名為 `app`），確定正確的引入模組流程，然後運行該應用程式。

在生產環境，你應該使用 `fastapi run` 命令。 🚀

**FastAPI CLI** 內部使用了 <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>，這是一個高效能、適合生產環境的 ASGI 伺服器。 😎

## `fastapi dev`

執行 `fastapi dev` 會啟動開發模式。

預設情況下，**auto-reload** 功能是啟用的，當你對程式碼進行修改時，伺服器會自動重新載入。這會消耗較多資源，並且可能比禁用時更不穩定。因此，你應該只在開發環境中使用此功能。它也會在 IP 位址 `127.0.0.1` 上監聽，這是用於你的機器與自身通訊的 IP 位址（`localhost`）。

## `fastapi run`

執行 `fastapi run` 會以生產模式啟動 FastAPI。

預設情況下，**auto-reload** 功能是禁用的。它也會在 IP 位址 `0.0.0.0` 上監聽，表示會監聽所有可用的 IP 地址，這樣任何能與該機器通訊的人都可以公開存取它。這通常是你在生產環境中運行應用程式的方式，例如在容器中運行時。

在大多數情況下，你會（也應該）有一個「終止代理」來處理 HTTPS，這取決於你如何部署你的應用程式，你的服務供應商可能會為你做這件事，或者你需要自己設置它。

/// tip

你可以在[部署文件](deployment/index.md){.internal-link target=_blank}中了解更多相關資訊。

///
