# 子应用 - 挂载 { #sub-applications-mounts }

如果需要两个独立的 FastAPI 应用，各自拥有独立的 OpenAPI 和各自的文档 UI，你可以创建一个主应用，并“挂载”一个（或多个）子应用。

## 挂载 **FastAPI** 应用 { #mounting-a-fastapi-application }

“挂载”是指在特定路径中添加一个完全“独立”的应用，然后该应用会用子应用中声明的 _path operations_ 来处理该路径下的所有事务。

### 顶层应用 { #top-level-application }

首先，创建主（顶层）**FastAPI** 应用及其 *path operations*：

{* ../../docs_src/sub_applications/tutorial001_py39.py hl[3, 6:8] *}

### 子应用 { #sub-application }

接下来，创建子应用及其 *path operations*。

该子应用只是另一个标准 FastAPI 应用，但它就是将被“挂载”的那个应用：

{* ../../docs_src/sub_applications/tutorial001_py39.py hl[11, 14:16] *}

### 挂载子应用 { #mount-the-sub-application }

在你的顶层应用 `app` 中，挂载子应用 `subapi`。

本例中，它将被挂载到路径 `/subapi`：

{* ../../docs_src/sub_applications/tutorial001_py39.py hl[11, 19] *}

### 查看自动 API 文档 { #check-the-automatic-api-docs }

现在，使用你的文件运行 `fastapi` 命令：

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

然后打开文档：<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你将看到主应用的自动 API 文档，只包含它自身的 _path operations_：

<img src="/img/tutorial/sub-applications/image01.png">

然后打开子应用的文档：<a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">http://127.0.0.1:8000/subapi/docs</a>。

你将看到子应用的自动 API 文档，只包含它自身的 _path operations_，并且全部都在正确的子路径前缀 `/subapi` 下：

<img src="/img/tutorial/sub-applications/image02.png">

如果你尝试与任意一个用户界面交互，它们都会正常工作，因为浏览器能够与每个指定的应用或子应用通信。

### 技术细节：`root_path` { #technical-details-root-path }

当你按上述方式挂载子应用时，FastAPI 会使用 ASGI 规范中一个名为 `root_path` 的机制来负责传递子应用的挂载路径。

这样，子应用就会知道在文档 UI 中使用该路径前缀。

并且子应用也可以再挂载它自己的子应用，一切都会正常运行，因为 FastAPI 会自动处理所有这些 `root_path`。

你将在 [Behind a Proxy](behind-a-proxy.md){.internal-link target=_blank} 一节中了解更多关于 `root_path` 以及如何显式使用它的内容。
