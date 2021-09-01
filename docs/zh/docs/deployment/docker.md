# 使用 Docker 部署

本章的主要内容如下：

* 创建最高性能的  **FastAPI** 应用 Docker 镜像/容器。**约 5 分钟**；
* （可选）开发者需要了解的 HTTPS 知识；
* 使用自动 HTTPS 设置 Docker Swarm 模式集群，同样适用于 5美元/月的简单服务器。**约 20 分钟**；
* 使用 Docker Swarm 与 HTTPS 生成并部署完整的 **FastAPI** 应用。**约 10 分钟**。

使用 <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a> 部署应用具有安全、可复制、开发简单等优势。

如果使用 Docker，推荐使用官方 Docker 镜像：

## <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>

这个镜像内置了**自动调优**机制，只需添加代码，就能开发出高性能的应用，而且不用付出任何代价。

您依然可以使用环境变量或配置文件更改配置。

!!! tip "提示"

    要查看所有配置和选项，请参阅 Docker 镜像页面: <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>。

## 创建 `Dockerfile`

* 进入项目文件夹
* 创建包含以下内容的 `Dockerfile`：

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app
```

### 大型应用

参照创建[多文件大型应用](../tutorial/bigger-applications.md){.internal-link target=_blank}一章，`Dockerfile` 的内容是类似这样的：

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app/app
```

### 树莓派与其它架构

如果在（使用 ARM 处理器的）树莓派或其它任何架构中运行 Docker，要基于 Python 基础镜像（多架构）从头创建 `Dockerfile`，并单独使用 Uvicorn。

本例中，`Dockerfile` 的内容如下：

```Dockerfile
FROM python:3.7

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

## 创建 **FastAPI** 代码

* 创建 `app` 文件夹，并进入文件夹
* 使用以下代码创建 `main.py`：

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

* 文件夹架构如下：

```
.
├── app
│   └── main.py
└── Dockerfile
```

## 构建 Docker 镜像

* 进入项目文件夹（`Dockerfile` 所在的文件夹，包含 `app` 文件夹）
* 构建 FastAPI 镜像：

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

## 启动 Docker 容器

* 运行基于镜像的容器：

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

这样，就在 Docker 容器中创建了一个优化过的 FastAPI 服务器。并对当前服务器（和 CPU 内核数）进行了自动调优。

## 查看文档

查看Docker容器的 URL，例如：<a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> 或 <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a>（或使用 Docker 主机）。

返回的响应如下：

```JSON
{"item_id": 5, "q": "somequery"}
```

## API 文档

现在跳转至 <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> 或 <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a>（或使用 Docker 主机）。

查看自动交互的（<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>） API 文档。

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## 备选 API 文档

跳转至 <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> 或  <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a>（或 Docker 主机）。

查看（<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>）备选 API 文档：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Traefik

<a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a> 是高性能反向代理/加载均衡器，用于执行 **TLS 终止代理**任务（其它功能除外）。

它集成了 Let's Encrypt，可以处理所有 HTTPS 组件，包括获取与更新证书。

Traefik 还集成了 Docker，可以在每个应用配置中声明域，用它读取配置，生成 HTTPS 证书，为应用自动提供 HTTPS 服务，而且无需在配置中进行任何更改。

---

有了这些信息与工具，就可以继续下一节组合所有内容。

## 支持 Traefik 与 HTTPS 的 Docker Swarm  mode 集群

设置 Docker Swarm Mode 集群大约需要 20 分钟，还包括使用 Traefik 处理 HTTPS（包括证书获取与更新）。

使用 Docker Swarm Mode 可以启用单机 “集群”（仅 5 美元/月 服务器），然后再按需添加更多服务器。

使用 Traefik 与 HTTPS 设置 Docker Swarm Mode 集群，要遵循以下指南：

<a href="https://medium.com/@tiangolo/docker-swarm-mode-and-traefik-for-a-https-cluster-20328dba6232" class="external-link" target="_blank">用于 HTTPS 集群的 Docker Swarm Mode 与 Traefik</a>

### 部署 FastAPI 应用

完成这些设置的最简单方式是使用 [**FastAPI** 项目生成器](../project-generation.md){.internal-link target=_blank}。

项目生成器集成了 Docker Swarm 集群与 Traefik 与 HTTPS。

生成项目只需要大约 2 分钟。

生成的项目提供了部署说明，再用 2 分钟就可以完成部署。

