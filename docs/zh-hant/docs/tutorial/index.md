# 教學 - 使用者指南 { #tutorial-user-guide }

本教學將一步一步展示如何使用 **FastAPI** 及其大多數功能。

每個部分都是在前一部分的基礎上逐步建置的，但內容結構是按主題分開的，因此你可以直接跳到任何特定的部分，解決你具體的 API 需求。

它也被設計成可作為未來的參考，讓你隨時回來查看所需的內容。

## 運行程式碼 { #run-the-code }

所有程式碼區塊都可以直接複製和使用（它們實際上是經過測試的 Python 檔案）。

要運行任何範例，請將程式碼複製到 `main.py` 檔案，並使用 `uv run` 啟動 `fastapi dev`：

<div class="termy">

```console
$ <font color="#4E9A06">uv run fastapi</font> dev

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

第一步是設定你的專案並加入 FastAPI。

安裝 [`uv`](https://docs.astral.sh/uv/getting-started/installation/)，然後建立專案並加入 FastAPI：

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"

---> 100%
```

</div>

`uv add` 會在 `.venv` 中建立專案的虛擬環境，將 FastAPI 加入 `pyproject.toml`，並建立 `uv.lock`，讓之後可以安裝相同的套件版本。

/// details | 這些指令的作用

* `uv init`：建立新的 Python 專案。
* `awesome-project`：在具有此名稱的新目錄中建立專案。
* `--bare`：只建立最小的 `pyproject.toml` 檔案，不產生範例 `main.py`、`README.md` 或其他檔案。你將在本教學的後續步驟中自行建立應用程式檔案。

接著 `cd awesome-project` 會在加入 FastAPI 前進入新的專案目錄。

`uv` 會使用你系統上已安裝的相容 Python 版本，或在需要時下載一個。

當你運行 `uv add` 時，它會選擇 FastAPI 與 FastAPI 依賴的所有套件的相容版本。它會將確切版本記錄在 `uv.lock` 中，讓之後在另一台電腦或部署應用程式時，可以安裝相同的套件版本。

建立或更新這個檔案稱為[**鎖定**專案依賴項](https://docs.astral.sh/uv/concepts/projects/sync/)。`uv` 會在你加入套件時自動完成。

///

/// details | FastAPI 安裝選項

當你使用 `uv add "fastapi[standard]"` 安裝時，會包含一些預設的可選標準依賴項，其中包括 `fastapi-cloud-cli`，它可以讓你部署到 [FastAPI Cloud](https://fastapicloud.com)。

如果你不想包含那些可選的依賴項，你可以改為安裝 `uv add fastapi`。

如果你想安裝標準依賴項，但不包含 `fastapi-cloud-cli`，可以使用 `uv add "fastapi[standard-no-fastapi-cloud-cli]"` 安裝。

///

/// details | 改用 `pip`

如果你偏好手動管理虛擬環境與套件，請建立並啟用虛擬環境，然後使用 `pip install "fastapi[standard]"` 安裝 FastAPI。

請閱讀[虛擬環境指南](https://tiangolo.com/guides/virtual-environments/)以取得詳細步驟。

///

## AI Agent 技能 { #ai-agent-skills }

FastAPI 包含給 AI coding agent 使用的官方技能。它隨套件一起提供，因此其指引會與你專案中安裝的 FastAPI 版本保持一致，並在你更新 FastAPI 時一起更新。

在你的專案中安裝 FastAPI 後，你可以使用 <a href="https://library-skills.io">Library Skills</a> 安裝這個技能：

```bash
uvx library-skills
```

/// note

`uvx` 是 `uv tool run` 的別名。它會在暫時且隔離的環境中運行 Library Skills，同時 Library Skills 會掃描你專案中已安裝的套件。

///

這個技能相容於 Codex、Claude Code、Cursor、GitHub Copilot、Gemini CLI、Pi、OpenCode，以及大多數其他 coding agent。若使用 Claude Code，當系統詢問要將技能安裝到哪裡時，請選擇 `.claude/skills`。

## 進階使用者指南 { #advanced-user-guide }

還有一個**進階使用者指南**你可以在讀完這個**教學 - 使用者指南**後再閱讀。

**進階使用者指南**建立在這個教學之上，使用相同的概念，並教你一些額外的功能。

但首先你應該閱讀**教學 - 使用者指南**（你正在閱讀的內容）。

它被設計成你可以使用**教學 - 使用者指南**來建立一個完整的應用程式，然後根據你的需求，使用**進階使用者指南**中的一些額外想法，以不同方式擴展它。
