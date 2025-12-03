# FastAPI CLI

**FastAPI CLI** 是一个命令行程序，你可以用它来部署和运行你的 FastAPI 应用程序，管理你的 FastAPI 项目，等等。

当你安装 FastAPI 时（例如使用 `pip install FastAPI` 命令），会包含一个名为 `fastapi-cli` 的软件包，该软件包在终端中提供 `fastapi` 命令。

要在开发环境中运行你的 FastAPI 应用，你可以使用 `fastapi dev` 命令：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

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

该命令行程序 `fastapi` 就是 **FastAPI CLI**。

FastAPI CLI 接收你的 Python 程序路径，自动检测包含 FastAPI 的变量（通常命名为 `app`）及其导入方式，然后启动服务。

在生产环境中，你应该使用 `fastapi run` 命令。🚀

在内部，**FastAPI CLI** 使用了 <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>，这是一个高性能、适用于生产环境的 ASGI 服务器。😎

## `fastapi dev`

当你运行 `fastapi dev` 时，它将以开发模式运行。

默认情况下，它会启用**自动重载**，因此当你更改代码时，它会自动重新加载服务器。该功能是资源密集型的，且相较不启用时更不稳定，因此你应该仅在开发环境下使用它。

默认情况下，它将监听 IP 地址 `127.0.0.1`，这是你的机器与自身通信的 IP 地址（`localhost`）。

## `fastapi run`

当你运行 `fastapi run` 时，它默认以生产环境模式运行。

默认情况下，**自动重载是禁用的**。

它将监听 IP 地址 `0.0.0.0`，即所有可用的 IP 地址，这样任何能够与该机器通信的人都可以公开访问它。这通常是你在生产环境中运行它的方式，例如在容器中运行。

在大多数情况下，你会（且应该）有一个“终止代理”在上层为你处理 HTTPS，这取决于你如何部署应用程序，你的服务提供商可能会为你处理此事，或者你可能需要自己设置。

/// tip | 提示

你可以在 [deployment documentation](deployment/index.md){.internal-link target=_blank} 获得更多信息。

///
