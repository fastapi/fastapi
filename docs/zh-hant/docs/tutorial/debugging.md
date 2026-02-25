# 偵錯 { #debugging }

你可以在編輯器中連接偵錯器，例如 Visual Studio Code 或 PyCharm。

## 呼叫 `uvicorn` { #call-uvicorn }

在你的 FastAPI 應用程式中，直接匯入並執行 `uvicorn`：

{* ../../docs_src/debugging/tutorial001_py310.py hl[1,15] *}

### 關於 `__name__ == "__main__"` { #about-name-main }

`__name__ == "__main__"` 的主要目的是，當你的檔案以以下方式呼叫時，執行某些程式碼：

<div class="termy">

```console
$ python myapp.py
```

</div>

但當其他檔案匯入它時不會執行，例如：

```Python
from myapp import app
```

#### 更多細節 { #more-details }

假設你的檔名是 `myapp.py`。

如果你用以下方式執行它：

<div class="termy">

```console
$ python myapp.py
```

</div>

那麼在你的檔案中，由 Python 自動建立的內部變數 `__name__`，其值會是字串 `"__main__"`。

因此，這段：

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

會被執行。

---

如果你是匯入該模組（檔案），就不會發生這件事。

所以，如果你有另一個檔案 `importer.py`，內容如下：

```Python
from myapp import app

# Some more code
```

在那種情況下，`myapp.py` 中自動建立的變數 `__name__` 就不會是 `"__main__"`。

因此，這一行：

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

就不會被執行。

/// info | 說明

想了解更多，參考 <a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">Python 官方文件</a>。

///

## 用偵錯器執行你的程式碼 { #run-your-code-with-your-debugger }

因為你是直接從程式碼中執行 Uvicorn 伺服器，所以你可以直接從偵錯器呼叫你的 Python 程式（你的 FastAPI 應用程式）。

---

例如，在 Visual Studio Code 中，你可以：

* 前往 "Debug" 面板
* 點選 "Add configuration..."
* 選擇 "Python"
* 使用選項 "`Python: Current File (Integrated Terminal)`" 啟動偵錯器

接著它會用你的 **FastAPI** 程式碼啟動伺服器、在你的中斷點停下等。

可能會長這樣：

<img src="/img/tutorial/debugging/image01.png">

---

如果你使用 PyCharm，你可以：

* 開啟 "Run" 選單
* 選擇 "Debug..."
* 會出現一個情境選單
* 選擇要偵錯的檔案（此例為 `main.py`）

接著它會用你的 **FastAPI** 程式碼啟動伺服器、在你的中斷點停下等。

可能會長這樣：

<img src="/img/tutorial/debugging/image02.png">
