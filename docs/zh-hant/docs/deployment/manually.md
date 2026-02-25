# 手動執行伺服器 { #run-a-server-manually }

## 使用 `fastapi run` 指令 { #use-the-fastapi-run-command }

簡而言之，使用 `fastapi run` 來啟動你的 FastAPI 應用：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>2306215</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
```

</div>

這在多數情況下都適用。😎

你可以用這個指令在容器、伺服器等環境中啟動你的 FastAPI 應用。

## ASGI 伺服器 { #asgi-servers }

我們再深入一些細節。

FastAPI 採用建立 Python 網頁框架與伺服器的標準 <abbr title="Asynchronous Server Gateway Interface - 非同步伺服器閘道介面">ASGI</abbr>。FastAPI 是一個 ASGI 網頁框架。

在遠端伺服器機器上執行 FastAPI 應用（或任何 ASGI 應用）所需的關鍵是 ASGI 伺服器程式，例如 Uvicorn；`fastapi` 指令預設就是使用它。

有數個替代方案，包括：

* <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a>：高效能 ASGI 伺服器。
* <a href="https://hypercorn.readthedocs.io/" class="external-link" target="_blank">Hypercorn</a>：支援 HTTP/2 與 Trio 等功能的 ASGI 伺服器。
* <a href="https://github.com/django/daphne" class="external-link" target="_blank">Daphne</a>：為 Django Channels 打造的 ASGI 伺服器。
* <a href="https://github.com/emmett-framework/granian" class="external-link" target="_blank">Granian</a>：針對 Python 應用的 Rust HTTP 伺服器。
* <a href="https://unit.nginx.org/howto/fastapi/" class="external-link" target="_blank">NGINX Unit</a>：NGINX Unit 是輕量且多功能的網頁應用執行環境。

## 伺服器機器與伺服器程式 { #server-machine-and-server-program }

有個命名上的小細節請留意。💡

「server（伺服器）」一詞常同時用來指遠端／雲端電腦（實體或虛擬機器），也用來指在該機器上執行的程式（例如 Uvicorn）。

因此看到「server」時，文意可能指這兩者之一。

指涉遠端機器時，常稱為 server、machine、VM（虛擬機器）、node 等，這些都指某種遠端機器（通常執行 Linux），你會在其上執行程式。

## 安裝伺服器程式 { #install-the-server-program }

安裝 FastAPI 時會附帶一個可用於生產環境的伺服器 Uvicorn，你可以用 `fastapi run` 來啟動它。

但你也可以手動安裝 ASGI 伺服器。

請先建立並啟用一個 [虛擬環境](../virtual-environments.md){.internal-link target=_blank}，接著再安裝伺服器程式。

例如，安裝 Uvicorn：

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

其他 ASGI 伺服器的安裝流程也大致相同。

/// tip

加入 `standard` 會讓 Uvicorn 安裝並使用一些建議的額外相依套件。

其中包含 `uvloop`，它是 `asyncio` 的高效能替代實作，可大幅提升並行效能。

當你用 `pip install "fastapi[standard]"` 安裝 FastAPI 時，也會一併取得 `uvicorn[standard]`。

///

## 執行伺服器程式 { #run-the-server-program }

如果你是手動安裝 ASGI 伺服器，通常需要提供特定格式的 import 字串，讓它能匯入你的 FastAPI 應用：

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note

指令 `uvicorn main:app` 指的是：

* `main`：檔案 `main.py`（Python「模組」）。
* `app`：在 `main.py` 中以 `app = FastAPI()` 建立的物件。

等同於：

```Python
from main import app
```

///

其他 ASGI 伺服器也有類似的指令，詳見各自的文件。

/// warning

Uvicorn 與其他伺服器支援 `--reload` 選項，對開發期間很有幫助。

`--reload` 會消耗更多資源，也較不穩定等。

它在開發階段很實用，但在生產環境中不應使用。

///

## 部署觀念 { #deployment-concepts }

上述範例會啟動伺服器程式（如 Uvicorn），以單一行程在指定連接埠（如 `80`）上監聽所有 IP（`0.0.0.0`）。

這是基本概念。但你很可能還需要處理一些額外事項，例如：

* 安全性 - HTTPS
* 開機自動啟動
* 自動重啟
* 多副本（執行的行程數量）
* 記憶體
* 啟動前需要執行的前置步驟

在下一章節我會進一步說明這些觀念、思考方式，以及對應的處理策略與實作範例。🚀
