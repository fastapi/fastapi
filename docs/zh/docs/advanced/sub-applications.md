# 子应用 - 挂载

如果需要两个独立的 FastAPI 应用，拥有各自独立的 OpenAPI 与文档，则需设置一个主应用，并**挂载**一个（或多个）子应用。

## 挂载 **FastAPI** 应用

**挂载**是指在特定路径中添加完全**独立**的应用，然后在该路径下使用*路径操作*声明的子应用处理所有事务。

### 顶层应用

首先，创建主（顶层）**FastAPI** 应用及其*路径操作*：

{* ../../docs_src/sub_applications/tutorial001.py hl[3,6:8] *}

### 子应用

接下来，创建子应用及其*路径操作*。

子应用只是另一个标准 FastAPI 应用，但这个应用是被**挂载**的应用：

{* ../../docs_src/sub_applications/tutorial001.py hl[11,14:16] *}

### 挂载子应用

在顶层应用 `app` 中，挂载子应用 `subapi`。

本例的子应用挂载在 `/subapi` 路径下：

{* ../../docs_src/sub_applications/tutorial001.py hl[11,19] *}

### 查看文档

如果主文件是 `main.py`，则用以下 `uvicorn` 命令运行主应用：

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

查看文档 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs。</a>

下图显示的是主应用 API 文档，只包括其自有的*路径操作*。

<img src="/img/tutorial/sub-applications/image01.png">

然后查看子应用文档 <a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">http://127.0.0.1:8000/subapi/docs。</a>

下图显示的是子应用的 API 文档，也是只包括其自有的*路径操作*，所有这些路径操作都在 `/subapi` 子路径前缀下。

<img src="/img/tutorial/sub-applications/image02.png">

两个用户界面都可以正常运行，因为浏览器能够与每个指定的应用或子应用会话。

### 技术细节：`root_path`

以上述方式挂载子应用时，FastAPI 使用 ASGI 规范中的 `root_path` 机制处理挂载子应用路径之间的通信。

这样，子应用就可以为自动文档使用路径前缀。

并且子应用还可以再挂载子应用，一切都会正常运行，FastAPI 可以自动处理所有 `root_path`。

关于 `root_path` 及如何显式使用 `root_path` 的内容，详见[使用代理](behind-a-proxy.md){.internal-link target=_blank}一章。
