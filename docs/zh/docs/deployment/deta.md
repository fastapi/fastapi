# 在 Deta 上部署 FastAPI

本节介绍如何使用 <a href="https://www.deta.sh/?ref=fastapi" class="external-link" target="_blank">Deta</a> 免费方案部署 **FastAPI** 应用。🎁

部署操作需要大约 10 分钟。

!!! info "说明"

    <a href="https://www.deta.sh/?ref=fastapi" class="external-link" target="_blank">Deta</a> 是 **FastAPI** 的赞助商。 🎉

## 基础 **FastAPI** 应用

* 创建应用文件夹，例如 `./fastapideta/`，进入文件夹

### FastAPI 代码

* 创建包含如下代码的 `main.py`：

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

### 需求项

在文件夹里新建包含如下内容的 `requirements.txt` 文件：

```text
fastapi
```

!!! tip "提示"

    在 Deta 上部署时无需安装 Uvicorn，虽然在本地测试应用时需要安装。

### 文件夹架构

`./fastapideta/` 文件夹中现在有两个文件：

```
.
└── main.py
└── requirements.txt
```

## 创建免费 Deta 账号

创建<a href="https://www.deta.sh/?ref=fastapi" class="external-link" target="_blank">免费的 Deta 账号</a>，只需要电子邮件和密码。

甚至不需要信用卡。

## 安装 CLI

创建账号后，安装 Deta <abbr title="Command Line Interface application">CLI</abbr>：

=== "Linux, macOS"

    <div class="termy">

    ```console
    $ curl -fsSL https://get.deta.dev/cli.sh | sh
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ iwr https://get.deta.dev/cli.ps1 -useb | iex
    ```

    </div>

安装完 CLI 后，打开新的 Terminal，就能检测到刚安装的 CLI。

在新的 Terminal 里，用以下命令确认 CLI 是否正确安装：

<div class="termy">

```console
$ deta --help

Deta command line interface for managing deta micros.
Complete documentation available at https://docs.deta.sh

Usage:
  deta [flags]
  deta [command]

Available Commands:
  auth        Change auth settings for a deta micro

...
```

</div>

!!! tip "提示"

    安装 CLI 遇到问题时，请参阅 <a href="https://docs.deta.sh/docs/micros/getting_started?ref=fastapi" class="external-link" target="_blank">Deta 官档</a>。

## 使用 CLI 登录

现在，使用 CLI 登录 Deta：

<div class="termy">

```console
$ deta login

Please, log in from the web page. Waiting..
Logged in successfully.
```

</div>

这个命令会打开浏览器并自动验证身份。

## 使用 Deta 部署

接下来，使用 Deta CLI 部署应用：

<div class="termy">

```console
$ deta new

Successfully created a new micro

// Notice the "endpoint" 🔍

{
    "name": "fastapideta",
    "runtime": "python3.7",
    "endpoint": "https://qltnci.deta.dev",
    "visor": "enabled",
    "http_auth": "enabled"
}

Adding dependencies...


---> 100%


Successfully installed fastapi-0.61.1 pydantic-1.7.2 starlette-0.13.6
```

</div>

您会看到如下 JSON 信息：

```JSON hl_lines="4"
{
        "name": "fastapideta",
        "runtime": "python3.7",
        "endpoint": "https://qltnci.deta.dev",
        "visor": "enabled",
        "http_auth": "enabled"
}
```

!!! tip "提示"

    您部署时的 `"endpoint"` URL 可能会有所不同。

## 查看效果

打开浏览器，跳转到 `endpoint` URL。本例中是 `https://qltnci.deta.dev`，但您的链接可能与此不同。

FastAPI 应用会返回如下 JSON 响应：

```JSON
{
    "Hello": "World"
}
```

接下来，跳转到 API 文档 `/docs`，本例中是 `https://qltnci.deta.dev/docs`。

文档显示如下：

<img src="/img/deployment/deta/image01.png">

## 启用公开访问

默认情况下，Deta 使用您的账号 Cookies 处理身份验证。

应用一切就绪之后，使用如下命令让公众也能看到您的应用：

<div class="termy">

```console
$ deta auth disable

Successfully disabled http auth
```

</div>

现在，就可以把 URL 分享给大家，他们就能访问您的 API 了。🚀

## HTTPS

恭喜！您已经在 Deta 上部署了 FastAPI 应用！🎉 🍰

还要注意，Deta 能够正确处理 HTTPS，因此您不必操心 HTTPS，您的客户端肯定能有安全加密的连接。 ✅ 🔒

## 查看 Visor

从 API 文档（URL 是 `https://gltnci.deta.dev/docs`）发送请求至*路径操作* `/items/{item_id}`。

例如，ID `5`。

现在跳转至 <a href="https://web.deta.sh/" class="external-link" target="_blank">https://web.deta.sh。</a>

左边栏有个 <abbr title="it comes from Micro(server)">"Micros"</abbr> 标签，里面是所有的应用。

还有一个 **Details** 和 **Visor** 标签，跳转到 **Visor** 标签。

在这里查看最近发送给应用的请求。

您可以编辑或重新使用这些请求。

<img src="/img/deployment/deta/image02.png">

## 更多内容

如果要持久化保存应用数据，可以使用提供了**免费方案**的 <a href="https://docs.deta.sh/docs/base/py_tutorial?ref=fastapi" class="external-link" target="_blank">Deta Base</a>。

详见 <a href="https://docs.deta.sh?ref=fastapi" class="external-link" target="_blank">Deta 官档</a>。
