# 利用Docker部署你的应用

在本章节中，你将会获取完成如下事情的指引:

* 为你的**FastAPI**应用制作高性能Docker镜像。（需要大约5分钟）
* （可选）会了解到作为一个开发者需要知道的HTTPS的一切。
* 在一个只需要5美金/月的服务器上搭建具有HTTPS的Docker集群。（需要大约20分钟）
* 利用Docker集群和HTTPS生成和部署一个完整的**FastAPI**应用。（需要大约10分钟）

你可以使用 <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a> 进行应用的部署。Dcoker在安全性、可复用性、开发的便捷性等方面具有不错的优点。

如果你正在使用Docker，你可以使用如下的官方Docker镜像

## <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>

这个镜像包含了"auto-tuning"机制，这可以在没有其他任何损失的前提下，自动使你的代码获取非常高的性能。

即使如此，你任然可以对全部的环境变量和配置文件进行改变。

!!! 要点
    想来了解所有的配置和选项，这个页面有你想知道的一切：<a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>。

## 创建`Dockerfile`

* 进入你的项目的根目录
* 创建一个具有如下内容的`Dockerfile`

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app
```

### 更复杂一些的应用

如果你已经阅读过如下章节,[Bigger Applications with Multiple Files](../tutorial/bigger-applications.md){.internal-link target=_blank}，你的`Dockerfile`可以会像下面这个样子:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app/app
```

### 树莓派等其他架构

如果你的Docker是运行在树莓派(具有ARM的处理器)或者其他架构上面，你可以基于Python基础镜像(多架构)从头创建一个Dockerfile，并单独使用Uvicorn。

在这种情况下，你的`Dockerfile`可能看起来像:

```Dockerfile
FROM python:3.7

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

## 编写你的**FastAPI**代码

* 创建并进入一个名为`app`的文件夹
* 在该文件夹下面创建一个`main.py`的python文件，并写入如下内容:

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

* 文件创建完成之后，目录结构如下:

```
.
├── app
│   └── main.py
└── Dockerfile
```

## 构建Docker镜像

* 回到项目的根目录(即`Dockerfile`所在的目录，这个目录包含上面创建的`app`文件夹)
* 利用如下命令构建你的FastAPI镜像

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

## 启动一个Docker容器

* 根据上面制作完成的镜像，利用如下命令启动一个容器:

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

现在你已经拥有一个优化过的FastAPI服务器。

## 检查服务运行状态

你可以通过容器暴露出来的URL检查服务的运行状态，例如: <a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> 或者 <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a> (或者等同地, 使用Docker host).

你将会看到如下内容:

```JSON
{"item_id": 5, "q": "somequery"}
```

## 访问交互式API文档

现在你可以进行如下地址: <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> 或者 <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a> (或者等同地, 使用Docker host).

你将会看到由Swagger提供交互式的API文档(provided by <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## 可选的API文档

并且你可以进入如下地址<a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> 或者 <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a> (或者等同地, 使用Docker host).

你将会看到由ReDoc提供的交互式API文档(provided by <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Traefik

<a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a> 是一个高性能反向代理/负载均衡器. 它可以做"TLS Termination Prox"工作(除了其他功能)。

它已经与Let’s Encrypt集成。因此，它可以处理所有HTTPS部分，包括证书的获取和更新。

它还与Docker进行了集成。因此，你可以在每个应用程序配置中声明您的域名，并让它读取这些配置，生成HTTPS证书并自动将HTTPS提供给您的应用程序，而不需要对其配置进行任何更改。

---

有了这些信息和工具，就可以继续下一章节的内容了。

## 利用Traefik和HTTPS搭建Docker集群模式（Docker Swarm mode）

你可以在几分钟(大约20分钟)内建立一个Docker Swarm模式的集群，使用主Traefik处理HTTPS(包括证书获取和更新)。

通过使用Docker Swarm模式，你可以从只有一台机器的"集群"开始(它甚至可以是一个5美元/月的云服务器)，然后你可以随着你需求增加而增加更多的服务器。

要使用Traefik和HTTPS处理建立Docker Swarm Mode集群，请遵循以下指南:

### <a href="https://medium.com/@tiangolo/docker-swarm-mode-and-traefik-for-a-https-cluster-20328dba6232" class="external-link" target="_blank">Docker Swarm Mode and Traefik for an HTTPS cluster</a>

### 部署一个FastAPI应用

设置一个FastAOI项目的所有初始化内容的最简单方法是使用 [**FastAPI** Project Generators](../project-generation.md){.internal-link target=_blank}.

它的设计目的是方便Docker集群与Traefik和上述HTTPS集成。

你可以使用它在大约2分钟内生成一个项目。

生成的项目有部署它的指令，完成它需要另外2分钟。
