# FastAPI CLI { #fastapi-cli }

**FastAPI <abbr title="command line interface - 命令行接口">CLI</abbr>** 是一个命令行程序，你可以用它来部署和运行你的 FastAPI 应用、管理 FastAPI 项目，等等。

当你安装 FastAPI（例如使用 `pip install "fastapi[standard]"`）时，会附带一个可以在终端中运行的命令行程序。

要在开发环境中运行你的 FastAPI 应用，可以使用 `fastapi dev` 命令：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

/// tip | 提示

在生产环境中，你会使用 `fastapi run` 而不是 `fastapi dev`。🚀

///

在内部，**FastAPI CLI** 使用 [Uvicorn](https://www.uvicorn.dev)，这是一个高性能、适用于生产环境的 ASGI 服务器。😎

`fastapi` CLI 会尝试自动检测要运行的 FastAPI 应用，默认假设它是文件 `main.py` 中名为 `app` 的对象（或少数其他变体）。

但你也可以显式配置要使用的应用。

## 在 `pyproject.toml` 中配置应用的 `entrypoint` { #configure-the-app-entrypoint-in-pyproject-toml }

你可以在 `pyproject.toml` 文件中配置应用的位置，例如：

```toml
[tool.fastapi]
entrypoint = "main:app"
```

这个 `entrypoint` 会告诉 `fastapi` 命令按如下方式导入应用：

```python
from main import app
```

如果你的代码结构如下：

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

那么你可以将 `entrypoint` 设置为：

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

这等价于：

```python
from backend.main import app
```

### 带路径的 `fastapi dev` { #fastapi-dev-with-path }

你也可以把文件路径传给 `fastapi dev` 命令，它会猜测要使用的 FastAPI 应用对象：

```console
$ fastapi dev main.py
```

但每次运行 `fastapi` 命令都需要记得传入正确的路径。

另外，其他工具可能找不到它，例如 [VS Code 扩展](editor-support.md) 或 [FastAPI Cloud](https://fastapicloud.com)，因此推荐在 `pyproject.toml` 中使用 `entrypoint`。

## `fastapi dev` { #fastapi-dev }

当你运行 `fastapi dev` 时，它将以开发模式运行。

默认情况下，它会启用**自动重载**，因此当你更改代码时，它会自动重新加载服务器。该功能是资源密集型的，且相较不启用时更不稳定，因此你应该仅在开发环境下使用它。它还会监听 IP 地址 `127.0.0.1`，这是你的机器仅与自身通信的 IP（`localhost`）。

## `fastapi run` { #fastapi-run }

当你运行 `fastapi run` 时，它默认以生产环境模式运行。

默认情况下，**自动重载是禁用的**。它将监听 IP 地址 `0.0.0.0`，即所有可用的 IP 地址，这样任何能够与该机器通信的人都可以公开访问它。这通常是你在生产环境中运行它的方式，例如在容器中运行。

在大多数情况下，你会（且应该）有一个“终止代理”在上层为你处理 HTTPS，这取决于你如何部署应用程序，你的服务提供商可能会为你处理此事，或者你可能需要自己设置。

/// tip | 提示

你可以在[部署文档](deployment/index.md)中了解更多。

///
