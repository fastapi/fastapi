# 教學 - 使用者指南 { #tutorial-user-guide }

本教學將一步一步展示如何使用 **FastAPI** 及其大多數功能。

每個部分都是在前一部分的基礎上逐步建置的，但內容結構是按主題分開的，因此你可以直接跳到任何特定的部分，解決你具體的 API 需求。

它也被設計成可作為未來的參考，讓你隨時回來查看所需的內容。

## 運行程式碼 { #run-the-code }

所有程式碼區塊都可以直接複製和使用（它們實際上是經過測試的 Python 檔案）。

要運行任何範例，請將程式碼複製到 `main.py` 檔案，並使用以下命令啟動 `fastapi dev`：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

**強烈建議**你編寫或複製程式碼、進行修改並在本地端運行。

在編輯器中使用它，才能真正體會到 FastAPI 的好處，可以看到你只需編寫少量程式碼，以及所有的型別檢查、自動補齊等功能。

---

## 安裝 FastAPI { #install-fastapi }

第一步是安裝 FastAPI。

確保你建立一個[虛擬環境](../virtual-environments.md){.internal-link target=_blank}，啟用它，然後**安裝 FastAPI**：

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note | 注意

當你使用 `pip install "fastapi[standard]"` 安裝時，會包含一些預設的可選標準依賴項，包含 `fastapi-cloud-cli`，它允許你部署到 <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>。

如果你不想包含那些可選的依賴項，你可以改為安裝 `pip install fastapi`。

如果你想安裝標準依賴項，但不包含 `fastapi-cloud-cli`，你可以使用 `pip install "fastapi[standard-no-fastapi-cloud-cli]"` 來安裝。

///

## 進階使用者指南 { #advanced-user-guide }

還有一個**進階使用者指南**你可以在閱讀完這份**教學 - 使用者指南**後再看。

**進階使用者指南**建立在這個教學之上，使用相同的概念，並教你一些額外的功能。

但首先你應該閱讀**教學 - 使用者指南**（你正在閱讀的內容）。

它被設計成你可以使用**教學 - 使用者指南**來建立一個完整的應用程式，然後根據你的需求，使用**進階使用者指南**中的一些額外想法，以不同方式來擴展它。
