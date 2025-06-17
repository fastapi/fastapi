# 環境變數

/// tip

如果你已經知道什麼是「環境變數」並且知道如何使用它們，你可以放心跳過這一部分。

///

環境變數（也稱為「**env var**」）是一個獨立於 Python 程式碼**之外**的變數，它存在於**作業系統**中，可以被你的 Python 程式碼（或其他程式）讀取。

環境變數對於處理應用程式**設定**（作為 Python **安裝**的一部分等方面）非常有用。

## 建立和使用環境變數

你在 **shell（終端機）**中就可以**建立**和使用環境變數，並不需要用到 Python：

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// 你可以使用以下指令建立一個名為 MY_NAME 的環境變數
$ export MY_NAME="Wade Wilson"

// 然後，你可以在其他程式中使用它，例如
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// 建立一個名為 MY_NAME 的環境變數
$ $Env:MY_NAME = "Wade Wilson"

// 在其他程式中使用它，例如
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## 在 Python 中讀取環境變數

你也可以在 Python **之外**的終端機中建立環境變數（或使用其他方法），然後在 Python 中**讀取**它們。

例如，你可以建立一個名為 `main.py` 的檔案，其中包含以下內容：

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip

第二個參數是 <a href="https://docs.python.org/zh-tw/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> 的預設回傳值。

如果沒有提供，預設值為 `None`，這裡我們提供 `"World"` 作為預設值。

///

然後你可以呼叫這個 Python 程式：

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// 這裡我們還沒有設定環境變數
$ python main.py

// 因為我們沒有設定環境變數，所以我們得到的是預設值

Hello World from Python

// 但是如果我們事先建立過一個環境變數
$ export MY_NAME="Wade Wilson"

// 然後再次呼叫程式
$ python main.py

// 現在就可以讀取到環境變數了

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// 這裡我們還沒有設定環境變數
$ python main.py

// 因為我們沒有設定環境變數，所以我們得到的是預設值

Hello World from Python

// 但是如果我們事先建立過一個環境變數
$ $Env:MY_NAME = "Wade Wilson"

// 然後再次呼叫程式
$ python main.py

// 現在就可以讀取到環境變數了

Hello Wade Wilson from Python
```

</div>

////

由於環境變數可以在程式碼之外設定，但可以被程式碼讀取，並且不必與其他檔案一起儲存（提交到 `git`），因此通常用於配置或**設定**。

你還可以為**特定的程式呼叫**建立特定的環境變數，該環境變數僅對該程式可用，且僅在其執行期間有效。

要實現這一點，只需在同一行內（程式本身之前）建立它：

<div class="termy">

```console
// 在這個程式呼叫的同一行中建立一個名為 MY_NAME 的環境變數
$ MY_NAME="Wade Wilson" python main.py

// 現在就可以讀取到環境變數了

Hello Wade Wilson from Python

// 在此之後這個環境變數將不再存在
$ python main.py

Hello World from Python
```

</div>

/// tip

你可以在 <a href="https://12factor.net/zh_cn/config" class="external-link" target="_blank">The Twelve-Factor App: 配置</a>中了解更多資訊。

///

## 型別和驗證

這些環境變數只能處理**文字字串**，因為它們是位於 Python 範疇之外的，必須與其他程式和作業系統的其餘部分相容（甚至與不同的作業系統相容，如 Linux、Windows、macOS）。

這意味著從環境變數中讀取的**任何值**在 Python 中都將是一個 `str`，任何型別轉換或驗證都必須在程式碼中完成。

你將在[進階使用者指南 - 設定和環境變數](./advanced/settings.md)中了解更多關於使用環境變數處理**應用程式設定**的資訊。

## `PATH` 環境變數

有一個**特殊的**環境變數稱為 **`PATH`**，作業系統（Linux、macOS、Windows）用它來查找要執行的程式。

`PATH` 變數的值是一個長字串，由 Linux 和 macOS 上的冒號 `:` 分隔的目錄組成，而在 Windows 上則是由分號 `;` 分隔的。

例如，`PATH` 環境變數可能如下所示：

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

這意味著系統應該在以下目錄中查找程式：

-   `/usr/local/bin`
-   `/usr/bin`
-   `/bin`
-   `/usr/sbin`
-   `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

這意味著系統應該在以下目錄中查找程式：

-   `C:\Program Files\Python312\Scripts`
-   `C:\Program Files\Python312`
-   `C:\Windows\System32`

////

當你在終端機中輸入一個**指令**時，作業系統會在 `PATH` 環境變數中列出的**每個目錄**中**查找**程式。

例如，當你在終端機中輸入 `python` 時，作業系統會在該列表中的**第一個目錄**中查找名為 `python` 的程式。

如果找到了，那麼作業系統將**使用它**；否則，作業系統會繼續在**其他目錄**中查找。

### 安裝 Python 並更新 `PATH`

安裝 Python 時，可能會詢問你是否要更新 `PATH` 環境變數。

//// tab | Linux, macOS

假設你安裝了 Python，並將其安裝在目錄 `/opt/custompython/bin` 中。

如果你選擇更新 `PATH` 環境變數，那麼安裝程式會將 `/opt/custompython/bin` 加入到 `PATH` 環境變數中。

它看起來大致會是這樣：

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

如此一來，當你在終端機輸入 `python` 時，系統會在 `/opt/custompython/bin` 中找到 Python 程式（最後一個目錄）並使用它。

////

//// tab | Windows

假設你安裝了 Python，並將其安裝在目錄 `C:\opt\custompython\bin` 中。

如果你選擇更新 `PATH` 環境變數（在 Python 安裝程式中，這個選項是名為 `Add Python x.xx to PATH` 的勾選框——譯者註），那麼安裝程式會將 `C:\opt\custompython\bin` 加入到 `PATH` 環境變數中。

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

如此一來，當你在終端機輸入 `python` 時，系統會在 `C:\opt\custompython\bin` 中找到 Python 程式（最後一個目錄）並使用它。

////

因此，如果你輸入：

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

系統會在 `/opt/custompython/bin` 中**找到** `python` 程式並執行它。

這大致等同於輸入以下指令：

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

系統會在 `C:\opt\custompython\bin\python` 中**找到** `python` 程式並執行它。

這大致等同於輸入以下指令：

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

當學習[虛擬環境](virtual-environments.md)時，這些資訊將會很有用。

## 結論

透過這個教學，你應該對**環境變數**是什麼以及如何在 Python 中使用它們有了基本的了解。

你也可以在<a href="https://zh.wikipedia.org/wiki/%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F" class="external-link" target="_blank">環境變數 - 維基百科</a> (<a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia for Environment Variable</a>) 中了解更多關於它們的資訊。

在許多情況下，環境變數的用途和適用性可能不會立刻顯現。但是在開發過程中，它們會在許多不同的場景中出現，因此瞭解它們是非常必要的。

例如，你在接下來的[虛擬環境](virtual-environments.md)章節中將需要這些資訊。
