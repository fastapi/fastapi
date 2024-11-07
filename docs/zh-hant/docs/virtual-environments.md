# 虛擬環境

當你在 Python 專案中工作時，你可能會需要使用一個**虛擬環境**（或類似的機制）來隔離你為每個專案安裝的套件。

/// info

如果你已經了解虛擬環境，知道如何創建和使用它們，你可以考慮跳過這一部分。🤓

///

/// tip

**虛擬環境**和**環境變數**是不同的。

**環境變數**是系統中的一個變數，可以被程式使用。

**虛擬環境**是一個包含一些檔案的目錄。

///

/// info

這個頁面將教你如何使用**虛擬環境**以及了解它們的工作原理。

如果你計畫使用一個**可以為你管理一切的工具**（包括安裝 Python），試試 <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">uv</a>。

///

## 創建一個專案

首先，為你的專案創建一個目錄。

我（指原作者 —— 譯者注）通常會在我的主目錄下創建一個名為 `code` 的目錄。

在這個目錄下，我再為每個專案創建一個目錄。

<div class="termy">

```console
// 進入主目錄
$ cd
// 創建一個用於存放所有程式碼專案的目錄
$ mkdir code
// 進入 code 目錄
$ cd code
// 創建一個用於存放這個專案的目錄
$ mkdir awesome-project
// 進入這個專案的目錄
$ cd awesome-project
```

</div>

## 創建一個虛擬環境

在開始一個 Python 專案的**第一時間**，**<abbr title="還有其他做法，此處僅作為一個簡單的指引">在你的專案內部</abbr>**創建一個虛擬環境。

/// tip

你只需要 **在每個專案中操作一次**，而不是每次工作時都操作。

///

//// tab | `venv`

你可以使用 Python 自帶的 `venv` 模組來創建一個虛擬環境。

<div class="termy">

```console
$ python -m venv .venv
```

</div>

/// details | 上述命令的含義

* `python`: 使用名為 `python` 的程式
* `-m`: 以腳本的方式調用一個模組，我們將告訴它接下來使用哪個模組
* `venv`: 使用名為 `venv` 的模組，這個模組通常隨 Python 一起安裝
* `.venv`: 在新目錄 `.venv` 中創建虛擬環境

///

////

//// tab | `uv`

如果你安裝了 <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">`uv`</a>，你也可以使用它來創建一個虛擬環境。

<div class="termy">

```console
$ uv venv
```

</div>

/// tip

預設情況下，`uv` 會在一個名為 `.venv` 的目錄中創建一個虛擬環境。

但你可以通過傳遞一個額外的參數來自訂它，指定目錄的名稱。

///

////

這個命令會在一個名為 `.venv` 的目錄中創建一個新的虛擬環境。

/// details | `.venv`，或是其他名稱

你可以在不同的目錄下創建虛擬環境，但通常我們會把它命名為 `.venv`。

///

## 啟動虛擬環境

啟動新的虛擬環境來確保你運行的任何 Python 指令或安裝的套件都能使用到它。

/// tip

**每次**開始一個 **新的終端會話** 來工作在這個專案時，你都需要執行這個操作。

///

//// tab | Linux, macOS

<div class="termy">

```console
$ source .venv/bin/activate
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ .venv\Scripts\Activate.ps1
```

</div>

////

//// tab | Windows Bash

或者，如果你在 Windows 上使用 Bash（例如 <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>）：

<div class="termy">

```console
$ source .venv/Scripts/activate
```

</div>

////

/// tip

每次你在這個環境中安裝一個 **新的套件** 時，都需要 **重新啟動** 這個環境。

這麼做確保了當你使用一個由這個套件安裝的 **終端（<abbr title="命令列界面">CLI</abbr>）程式** 時，你使用的是你的虛擬環境中的程式，而不是全域安裝、可能版本不同的程式。

///

## 檢查虛擬環境是否啟動

檢查虛擬環境是否啟動（前面的指令是否生效）。

/// tip

這是 **可選的**，但這是一個很好的方法，可以 **檢查** 一切是否按預期工作，以及你是否使用了你打算使用的虛擬環境。

///

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
$ which python

/home/user/code/awesome-project/.venv/bin/python
```

</div>

如果它顯示了在你專案（在這個例子中是 `awesome-project`）的 `.venv/bin/python` 中的 `python` 二進位檔案，那麼它就生效了。🎉

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ Get-Command python

C:\Users\user\code\awesome-project\.venv\Scripts\python
```

</div>

如果它顯示了在你專案（在這個例子中是 `awesome-project`）的 `.venv\Scripts\python` 中的 `python` 二進位檔案，那麼它就生效了。🎉

////

## 升級 `pip`

/// tip

如果你使用 <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">`uv`</a> 來安裝內容，而不是 `pip`，那麼你就不需要升級 `pip`。😎

///

如果你使用 `pip` 來安裝套件（它是 Python 的預設元件），你應該將它 **升級** 到最新版本。

在安裝套件時出現的許多奇怪的錯誤都可以通過先升級 `pip` 來解決。

/// tip

通常你只需要在創建虛擬環境後 **執行一次** 這個操作。

///

確保虛擬環境是啟動的（使用上面的指令），然後運行：

<div class="termy">

```console
$ python -m pip install --upgrade pip

---> 100%
```

</div>

## 添加 `.gitignore`

如果你使用 **Git**（這是你應該使用的），添加一個 `.gitignore` 檔案來排除你的 `.venv` 中的所有內容。

/// tip

如果你使用 <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">`uv`</a> 來創建虛擬環境，它會自動為你完成這個操作，你可以跳過這一步。😎

///

/// tip

通常你只需要在創建虛擬環境後 **執行一次** 這個操作。

///

<div class="termy">

```console
$ echo "*" > .venv/.gitignore
```

</div>

/// details | 上述指令的含義

* `echo "*"`: 將在終端中 "顯示" 文本 `*`（接下來的部分會對這個操作進行一些修改）
* `>`: 使左邊的指令顯示到終端的任何內容實際上都不會被顯示，而是會被寫入到右邊的檔案中
* `.gitignore`: 被寫入文本的檔案的名稱

而 `*` 對於 Git 來說意味著 "所有內容"。所以，它會忽略 `.venv` 目錄中的所有內容。

該指令會創建一個名為 .gitignore 的檔案，內容如下：

```gitignore
*
```
