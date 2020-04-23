# 部署

部署 **FastAPI** 应用相对比较简单。

根据特定使用情况和使用工具有几种不同的部署方式。

接下来的章节，你将了解到一些关于部署方式的内容。

## FastAPI 版本

许多应用和系统已经在生产环境使用 **FastAPI**。其测试覆盖率保持在 100%。但该项目仍在快速开发。

我们会经常加入新的功能，定期错误修复，同时也在不断的优化项目代码。

这也是为什么当前版本仍然是 `0.x.x`，我们以此表明每个版本都可能有重大改变。

现在就可以使用 **FastAPI** 创建生产应用（你可能已经使用一段时间了）。你只需要确保使用的版本和代码其他部分能够正常兼容。

### 指定你的 `FastAPI` 版本

你应该做的第一件事情，是为你正在使用的 **FastAPI** 指定一个能够正确运行你的应用的最新版本。

例如，假设你的应用中正在使用版本 `0.45.0`。

如果你使用 `requirements.txt` 文件，你可以这样指定版本：

```txt
fastapi==0.45.0
```

这表明你将使用 `0.45.0` 版本的 `FastAPI`。

或者你也可以这样指定：

```txt
fastapi>=0.45.0,<0.46.0
```

这表明你将使用 `0.45.0` 及以上，但低于 `0.46.0` 的版本，例如，`0.45.2` 依然可以接受。

如果使用其他工具管理你的安装，比如 Poetry，Pipenv，或者其他工具，它们都有各自指定包的版本的方式。

### 可用版本

你可以在 [发行说明](release-notes.md){.internal-link target=_blank} 中查看可用的版本（比如：检查最新版本是什么）。


### 关于版本

FastAPI 遵循语义版本控制约定，`1.0.0` 以下的任何版本都可能加入重大变更。

FastAPI 也遵循这样的约定：任何 ”PATCH“ 版本变更都是用来修复 bug 和向下兼容的变更。

!!! tip
    "PATCH" 是指版本号的最后一个数字，例如，在 `0.2.3` 中，PATCH 版本是 `3`。

所以，你应该像这样指定版本：

```txt
fastapi>=0.45.0,<0.46.0
```

不兼容变更和新特性在 "MINOR" 版本中添加。

!!! tip
    "MINOR" 是版本号中间的数字，例如，在 `0.2.3` 中，MINOR 版本是 `2`。

### 更新 FaseAPI 版本

你应该为你的应用添加测试。

使用 **FastAPI** 测试应用非常容易（归功于 Starlette），查看文档：[测试](tutorial/testing.md){.internal-link target=_blank}

有了测试之后，就可以将 **FastAPI** 更新到最近的一个的版本，然后通过运行测试来确定你所有代码都可以正确工作。

如果一切正常，或者做了必要的修改之后，所有的测试都通过了，就可以把 `FastAPI` 版本指定为那个比较新的版本了。

### 关于 Starlette

不要指定 `starlette` 的版本。

不同版本的 **FastAPI** 会使用特定版本的 Starlette。

所以你只要让 **FastAPI** 自行选择正确的 Starlette 版本。

### 关于 Pydantic

Pydantic 自身的测试中已经包含了 **FastAPI** 的测试，所以最新版本的 Pydantic （`1.0.0` 以上版本）总是兼容 **FastAPI**。

你可以指定 Pydantic 为任意一个高于 `1.0.0` 且低于的 `2.0.0` 的版本。

例如：

```txt
pydantic>=1.2.0,<2.0.0
```

## Docker

这部分，你将通过指引和链接了解到：

* 如何将你的 **FastAPI** 应用制作成最高性能的 **Docker** 映像/容器。约需五分钟。
* （可选）理解作为一个开发者需要知道的 HTTPS 相关知识。
* 使用自动化 HTTPS 设置一个 Docker Swarm 模式的集群，即使是在一个简单的 $5 USD/month 的服务器上。约需要 20 分钟。
* 使用 Docker Swarm 集群以及 HTTP 等等，生成和部署一个完整的 **FastAPI** 应用。约需 10 分钟。

可以使用 <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a> 进行部署。它具有安全性、可复制性、开发简单性等优点。

如果你正在使用 Docker，你可以使用官方 Docker 镜像：

### <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>

该映像包含一个「自动调优」的机制，这样就可以仅仅添加代码就能自动获得超高性能，而不用做出牺牲。

不过你仍然可以使用环境变量或配置文件更改和更新所有配置。

!!! tip
    查看全部配置和选项，请移步 Docker 镜像页面：<a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>。

### 创建 `Dockerfile`

* 进入你的项目目录。
* 使用如下命令创建一个 `Dockerfile`：

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app
```

#### 大型应用

如果遵循创建 [多文件大型应用](tutorial/bigger-applications.md){.internal-link target=_blank} 的章节，你的 Dockerfile 可能看起来是这样:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app/app
```

#### 树莓派以及其他架构

如果你在树莓派或者任何其他架构中运行 Docker，可以基于 Python 基础镜像（它是多架构的）从头创建一个 `Dockerfile` 并单独使用 Uvicorn。

这种情况下，你的 `Dockerfile` 可能是这样的：

```Dockerfile
FROM python:3.7

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

### 创建 **FastAPI** 代码

* 创建一个 `app` 目录并进入该目录。
* 创建一个 `main.py` 文件，内容如下：

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

* 现在目录结构如下：

```
.
├── app
│   └── main.py
└── Dockerfile
```

### 构建 Docker 镜像

* 进入项目目录（在 `Dockerfile` 所在的位置，包含 `app` 目录）
* 构建 **FastAPI** 镜像

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

### 启动 Docker 容器

* 运行基于你的镜像容器：

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

现在你在 Docker 容器中有了一个根据当前服务器（和CPU核心的数量）自动优化好的 FastAPI 服务器。

### 检查一下

你应该能够在 Docker 容器的 URL 中检查它。例如：<a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> 或者 <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a> （或者类似的，使用Docker主机）。

得到类似的输出：

```JSON
{"item_id": 5, "q": "somequery"}
```

### 交互式 API 文档

现在可以访问 <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> 或者 <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a> （或者类似的，使用Docker主机）。

你会看到一个交互式的 API 文档 （由 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 可选的 API 文档

你也可以访问 <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> 或者 <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a> （或者类似的，使用Docker主机）。

你将看到一个可选的自动化文档（由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> 提供）

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## HTTPS

### 关于 HTTPS

我们当然可以假设 HTTPS 只是某种「启用」或「不启用」的东西。

但是事实比这要复杂的多。

!!! tip
    如果你着急或者不关心这部分内容，请继续按照下一章节的步骤进行配置。

要从用户的角度学习 HTTPS 的基础，请移步 <a href="https://howhttps.works/" class="external-link" target="_blank">https://howhttps.works/</a>。

从开发人员的角度来看，在考虑 HTTPS 时有以下几点需要注意：

* 对 HTTPS 来说，服务端需要有第三方生成的「证书」。
    * 实际上这些证书是从第三方获取的，而非「生成」的。
* 证书有生命周期。
    * 证书会过期。
    * 证书过期之后需要更新，重新从第三方获取。
* 连接的加密发生在 TCP 层。
    * TCP 层在 HTTP 之下一层。
    * 因此，证书和加密处理在 HTTP 之前完成。
* TCP 不知道「域名」，只知道 IP 地址。
    * 指定域名的请求信息在 HTTP 的数据中。
* HTTPS 证书「认证」某个特定域名，但是协议和加密在知道要处理哪个域名之前就已经在 TCP 层发生了。
* 默认情况下，一个 IP 地址仅有一个 HTTPS 证书。
    * 无论你的服务器大小，都是如此。
    * 但是对此有解决办法。
* TSL 协议（在 TCP 层处理加密的协议，发生在 HTTP 之前）有一个扩展，叫 <a href="https://en.wikipedia.org/wiki/Server_Name_Indication" class="external-link" target="_blank"><abbr title="Server Name Indication">SNI</abbr></a>。
    * SNI 扩展允许一个服务器（一个 IP 地址）有多个 HTTPS 证书，为多个 HTTPS 域名/应用 提供服务。
    * 要使其工作，服务器运行的单一组件（程序）监听公网 IP 地址，所有 HTTPS 证书必须都在该服务器上。
* 在获得一个安全连接之后，通讯协议仍然是 HTTP。
    * HTTP 内容是加密的，即使这些内容使用 HTTP 协议传输。

常见的做法是在服务器（机器，主机等等）上运行一个程序或 HTTP 服务来管理所有的 HTTPS 部分：将解密后的 HTTP 请求发送给在同一服务器运行的真实 HTTP 应用（在这里是 **FastAPI** 应用），从应用获得 HTTP 响应，使用适当的证书加密响应然后使用 HTTPS 将其发回客户端。这个服务器常被称作 <a href="https://en.wikipedia.org/wiki/TLS_termination_proxy" class="external-link" target="_blank">TLS 终止代理</a>。


### Let's Encrypt

在 Let's Encrypt 出现之前，这些 HTTPS 证书由受信任的第三方出售。

获取这些证书的过程曾经非常繁琐，需要大量的文书工作，而且证书的价格也相当昂贵。

但是紧接着 <a href="https://letsencrypt.org/" class="external-link" target="_blank">Let's Encrypt</a> 被创造了。

这是一个来自 Linux 基金会的项目。它以自动化的方式免费提供 HTTPS 证书。这些证书使用所有的标准加密措施，且证书生命周期很短（大约 3 个月），正是由于它们生命周期的减短，所以实际上安全性更高。

对域名进行安全验证并自动生成证书。同时也允许自动更新这些证书。

其想法是自动获取和更新这些证书，这样就可以一直免费获得安全的 HTTPS。

### Traefik

<a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a> 是一个高性能的反向代理/负载均衡器。它能够完成「TLS 终止代理」的工作（其他特性除外）。

Traefik 集成了 Let's Encrypt，所以能够处理全部 HTTPS 的部分，包括证书获取与更新。

Traefik 也集成了 Docker，所以你也可以在每个应用的配置中声明你的域名并可以让它读取这些配置，生成 HTTPS 证书并自动将 HTTPS 提供给你的应用程序，而你不需要对其配置进行任何更改。

---

有了这些信息和工具，就可以进入下一节把所有内容结合到一起。

## 通过 Traefik 和 HTTPS 搭建 Docker Swarm mode 集群

通过一个主要的 Traefik 来处理 HTTPS （包括证书获取和更新），大约 20 分钟就可以搭建好一个 Docker Swarm mode 集群。

借助 Docker Swarm mode，你可以从单个机器的集群开始（甚至可以是 $5 /月的服务器），然后你可以根据需要添加更多的服务器来进行扩展。

要使用 Traefik 和 HTTPS 处理来构建 Docker Swarm Mode 集群，请遵循以下指南:

### <a href="https://medium.com/@tiangolo/docker-swarm-mode-and-traefik-for-a-https-cluster-20328dba6232" class="external-link" target="_blank">Docker Swarm Mode 和 Traefik 用于 HTTPS 集群</a>

### 部署一个 FastAPI 应用

部署的最简单方式就是使用 [**FastAPI** 项目生成器](project-generation.md){.internal-link target=_blank}。

它被设计成与上述带有 Traefik 和 HTTPS 的 Docker Swarm 集群整合到一起。

你可以在大概两分钟内生成一个项目。

生成的项目有部署说明，需要再花两分钟部署项目。

## 或者，不用 Docker 部署 **FastAPI**

你也可以不用 Docker 直接部署 **FastAPI**。

只需要安装一个兼容 ASGI 的服务器：

* <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>，一个轻量快速的 ASGI 服务器，基于 uvloop 和 httptools 构建。

<div class="termy">

```console
$ pip install uvicorn

---> 100%
```

</div>

* <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>，一个也兼容 HTTP/2 的 ASGI 服务器。

<div class="termy">

```console
$ pip install hypercorn

---> 100%
```

</div>

...或者任何其他的 ASGI 服务器。

然后使用教程中同样的方式来运行你的应用，但是不要加 `--reload` 选项，比如：

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

或者使用 Hypercorn：

<div class="termy">

```console
$ hypercorn main:app --bind 0.0.0.0:80

Running on 0.0.0.0:8080 over http (CTRL + C to quit)
```

</div>

也许你想编写一些工具来确保它停止时会自动重启。

或者安装 <a href="https://gunicorn.org/" class="external-link" target="_blank">Gunicorn</a> 并 <a href="https://www.uvicorn.org/#running-with-gunicorn" class="external-link" target="_blank">将其作为 Uvicorn 的管理器</a>，或者使用多职程（worker）的 Hypercorn。

或者保证精确调整职程的数量等等。

但是如果你正做这些，你可能只需要使用 Docker 镜像就能够自动做到这些了。
