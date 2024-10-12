# 手动运行服务器 - Uvicorn

在远程服务器计算机上运行 **FastAPI** 应用程序所需的主要东西是 ASGI 服务器程序，例如 **Uvicorn**。

有 3 个主要可选方案：

* <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>：高性能 ASGI 服务器。
* <a href="https://hypercorn.readthedocs.io/" class="external-link" target="_blank">Hypercorn</a>：与 HTTP/2 和 Trio 等兼容的 ASGI 服务器。
* <a href="https://github.com/django/daphne" class="external-link" target="_blank">Daphne</a>：为 Django Channels 构建的 ASGI 服务器。

## 服务器主机和服务器程序

关于名称，有一个小细节需要记住。 💡

“**服务器**”一词通常用于指远程/云计算机（物理机或虚拟机）以及在该计算机上运行的程序（例如 Uvicorn）。

请记住，当您一般读到“服务器”这个名词时，它可能指的是这两者之一。

当提到远程主机时，通常将其称为**服务器**，但也称为**机器**(machine)、**VM**（虚拟机）、**节点**。 这些都是指某种类型的远程计算机，通常运行 Linux，您可以在其中运行程序。


## 安装服务器程序

您可以使用以下命令安装 ASGI 兼容服务器：

//// tab | Uvicorn

* <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>，一个快如闪电 ASGI 服务器，基于 uvloop 和 httptools 构建。

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

/// tip

通过添加`standard`，Uvicorn 将安装并使用一些推荐的额外依赖项。

其中包括`uvloop`，它是`asyncio`的高性能替代品，它提供了巨大的并发性能提升。

///

////

//// tab | Hypercorn

* <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>，一个也与 HTTP/2 兼容的 ASGI 服务器。

<div class="termy">

```console
$ pip install hypercorn

---> 100%
```

</div>

...或任何其他 ASGI 服务器。

////

## 运行服务器程序

您可以按照之前教程中的相同方式运行应用程序，但不使用`--reload`选项，例如：

//// tab | Uvicorn

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

////

//// tab | Hypercorn

<div class="termy">

```console
$ hypercorn main:app --bind 0.0.0.0:80

Running on 0.0.0.0:8080 over http (CTRL + C to quit)
```

</div>

////

/// warning

如果您正在使用`--reload`选项，请记住删除它。

 `--reload` 选项消耗更多资源，并且更不稳定。

 它在**开发**期间有很大帮助，但您**不应该**在**生产环境**中使用它。

///

## Hypercorn with Trio

Starlette 和 **FastAPI** 基于 <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a>， 所以它们才能同时与 Python 的标准库 <a href="https://docs.python.org/3/library/asyncio-task.html" class="external-link" target="_blank">asyncio</a> 和<a href="https://trio.readthedocs.io/en/stable/" class="external-link" target="_blank">Trio</a> 兼容。

尽管如此，Uvicorn 目前仅与 asyncio 兼容，并且通常使用 <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a >, 它是`asyncio`的高性能替代品。

但如果你想直接使用**Trio**，那么你可以使用**Hypercorn**，因为它支持它。 ✨

### 安装具有 Trio 的 Hypercorn

首先，您需要安装具有 Trio 支持的 Hypercorn：

<div class="termy">

```console
$ pip install "hypercorn[trio]"
---> 100%
```

</div>

### Run with Trio

然后你可以传递值`trio`给命令行选项`--worker-class`:

<div class="termy">

```console
$ hypercorn main:app --worker-class trio
```

</div>

这将通过您的应用程序启动 Hypercorn，并使用 Trio 作为后端。

现在您可以在应用程序内部使用 Trio。 或者更好的是，您可以使用 AnyIO，使您的代码与 Trio 和 asyncio 兼容。 🎉

## 部署概念

这些示例运行服务器程序（例如 Uvicorn），启动**单个进程**，在所有 IP（`0.0.0.0`)上监听预定义端口（例如`80`)。

这是基本思路。 但您可能需要处理一些其他事情，例如：

* 安全性 - HTTPS
* 启动时运行
* 重新启动
* Replication（运行的进程数）
* 内存
* 开始前的步骤

在接下来的章节中，我将向您详细介绍每个概念、如何思考它们，以及一些具体示例以及处理它们的策略。 🚀
