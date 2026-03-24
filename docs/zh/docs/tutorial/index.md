# 教程 - 用户指南 { #tutorial-user-guide }

本教程将一步步向您展示如何使用 **FastAPI** 的绝大部分特性。

各个章节的内容循序渐进，但是又围绕着单独的主题，所以您可以直接跳转到某个章节以解决您的特定 API 需求。

本教程同样可以作为将来的参考手册，所以您可以随时回到本教程并查阅您需要的内容。

## 运行代码 { #run-the-code }

所有代码片段都可以复制后直接使用（它们实际上是经过测试的 Python 文件）。

要运行任何示例，请将代码复制到 `main.py` 文件中，然后启动 `fastapi dev`：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

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

**强烈建议**您在本地编写或复制代码，对其进行编辑并运行。

在编辑器中使用 FastAPI 会真正地展现出它的优势：只需要编写很少的代码，所有的类型检查，代码补全等等。

---

## 安装 FastAPI { #install-fastapi }

第一个步骤是安装 FastAPI.

请确保您创建并激活一个[虚拟环境](../virtual-environments.md)，然后**安装 FastAPI**：

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note | 注意

当您使用 `pip install "fastapi[standard]"` 安装时，它会附带一些默认的可选标准依赖项，其中包括 `fastapi-cloud-cli`，它可以让您部署到 [FastAPI Cloud](https://fastapicloud.com)。

如果您不想安装这些可选依赖，可以选择安装 `pip install fastapi`。

如果您想安装标准依赖但不包含 `fastapi-cloud-cli`，可以使用 `pip install "fastapi[standard-no-fastapi-cloud-cli]"` 安装。

///

/// tip | 提示

FastAPI 提供了一个[VS Code 官方扩展](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode)（也支持 Cursor），包含众多功能，例如路径操作浏览器、路径操作搜索、测试中的 CodeLens 导航（从测试跳转到定义），以及从编辑器内进行 FastAPI Cloud 部署和查看日志。

///

## 进阶用户指南 { #advanced-user-guide }

在本**教程-用户指南**之后，您可以阅读**进阶用户指南**。

**进阶用户指南**以本教程为基础，使用相同的概念，并教授一些额外的特性。

但是您应该先阅读**教程-用户指南**（即您现在正在阅读的内容）。

教程经过精心设计，使您可以仅通过**教程-用户指南**来开发一个完整的应用程序，然后根据您的需要，使用**进阶用户指南**中的一些其他概念，以不同的方式来扩展它。
