# 教程 - 用户指南

本教程将一步步向你展示如何使用 **FastAPI** 的绝大部分特性。

各个章节的内容循序渐进，但是又围绕着单独的主题，所以你可以直接跳转到某个章节以解决你的特定需求。

本教程同样可以作为将来的参考手册，所以你可以随时回到本教程并查阅你需要的内容。

## 运行代码

所有代码片段都可以复制后直接使用（它们实际上是经过测试的 Python 文件）。

要运行任何示例，请将代码复制到 `main.py` 文件中，然后使用以下命令启动 `fastapi`：

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

**强烈建议**你在本地编写或复制代码，对其进行编辑并运行。

在编辑器中使用 FastAPI 会真正地展现出它的优势：只需要编写很少的代码，所有的类型检查，代码补全等等。

---

## 安装 FastAPI

第一个步骤是安装 FastAPI。

确保你创建了一个 [虚拟环境](../virtual-environments.md){.internal-link target=_blank}，激活它，然后 **安装 FastAPI**：

<div class="termy">

```console
$ pip install "fastapi[all]"

---> 100%
```

</div>

/// note

当你通过 `pip install "fastapi[standard]"` 进行安装时，它带有一些默认的可选标准依赖项。

如果你不想安装这些可选的依赖项，你可以通过 `pip install fastapi`进行安装。

///

## 高级用户指南

在本**教程-用户指南**之后，你可以阅读**高级用户指南**。

**高级用户指南**以本教程为基础，使用相同的概念，并教授一些额外的特性。

但是你应该先阅读**教程-用户指南**（即你现在正在阅读的内容）。

教程经过精心设计，使你可以仅通过**教程-用户指南**来开发一个完整的应用程序，然后根据你的需要，使用**高级用户指南**中的一些其他概念，以不同的方式来扩展它。
