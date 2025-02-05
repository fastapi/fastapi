# 调试

你可以在编辑器中连接调试器，例如使用 Visual Studio Code 或 PyCharm。

## 调用 `uvicorn`

在你的 FastAPI 应用中直接导入 `uvicorn` 并运行：

{* ../../docs_src/debugging/tutorial001.py hl[1,15] *}

### 关于 `__name__ == "__main__"`

`__name__ == "__main__"` 的主要目的是使用以下代码调用文件时执行一些代码：

<div class="termy">

```console
$ python myapp.py
```

</div>

而当其它文件导入它时并不会被调用，像这样：

```Python
from myapp import app
```

#### 更多细节

假设你的文件命名为 `myapp.py`。

如果你这样运行：

<div class="termy">

```console
$ python myapp.py
```

</div>

那么文件中由 Python 自动创建的内部变量 `__name__`，会将字符串 `"__main__"` 作为值。

所以，下面这部分代码才会运行：

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

如果你是导入这个模块（文件）就不会这样。

因此，如果你的另一个文件 `importer.py` 像这样：

```Python
from myapp import app

# Some more code
```

在这种情况下，`myapp.py` 内部的自动变量不会有值为 `"__main__"` 的变量 `__name__`。

所以，下面这一行不会被执行：

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

/// info

更多信息请检查 <a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">Python 官方文档</a>.

///

## 使用你的调试器运行代码

由于是从代码直接运行的 Uvicorn 服务器，所以你可以从调试器直接调用 Python 程序（你的 FastAPI 应用）。

---

例如，你可以在 Visual Studio Code 中：

* 进入到「调试」面板。
* 「添加配置...」。
* 选中「Python」
* 运行「Python：当前文件（集成终端）」选项的调试器。

然后它会使用你的 **FastAPI** 代码开启服务器，停在断点处，等等。

看起来可能是这样：

<img src="/img/tutorial/debugging/image01.png">

---

如果使用 Pycharm，你可以：

* 打开「运行」菜单。
* 选中「调试...」。
* 然后出现一个上下文菜单。
* 选择要调试的文件（本例中的 `main.py`）。

然后它会使用你的 **FastAPI** 代码开启服务器，停在断点处，等等。

看起来可能是这样：

<img src="/img/tutorial/debugging/image02.png">
