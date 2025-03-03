# 教學 - 使用者指南

本教學將一步一步展示如何使用 **FastAPI** 及其大多數功能。

每個部分都是在前一部分的基礎上逐步建置的，但內容結構是按主題分開的，因此你可以直接跳到任何特定的部分，解決你具體的 API 需求。

它也被設計成可作為未來的參考，讓你隨時回來查看所需的內容。

## 運行程式碼

所有程式碼區塊都可以直接複製和使用（它們實際上是經過測試的 Python 檔案）。

要運行任何範例，請將程式碼複製到 `main.py` 檔案，並使用以下命令啟動 `fastapi dev`：

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
</pre>
```

</div>

**強烈建議**你編寫或複製程式碼、進行修改並在本地端運行。

在編輯器中使用它，才能真正體會到 FastAPI 的好處，可以看到你只需編寫少量程式碼，以及所有的型別檢查、自動補齊等功能。

---

## 安裝 FastAPI

第一步是安裝 FastAPI。

確保你建立一個[虛擬環境](../virtual-environments.md){.internal-link target=_blank}，啟用它，然後**安裝 FastAPI**：

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note

當你使用 `pip install "fastapi[standard]"` 安裝時，會包含一些預設的可選標準依賴項。

如果你不想包含那些可選的依賴項，你可以使用 `pip install fastapi` 來安裝。

///

## 進階使用者指南

還有一個**進階使用者指南**你可以稍後閱讀。

**進階使用者指南**建立在這個教學之上，使用相同的概念，並教你一些額外的功能。

但首先你應該閱讀**教學 - 使用者指南**（你正在閱讀的內容）。

它被設計成你可以使用**教學 - 使用者指南**來建立一個完整的應用程式，然後根據你的需求，使用一些額外的想法來擴展它。
