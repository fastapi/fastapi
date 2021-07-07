# 教程 - 用户指南 - 简介

本教程将逐步介绍 **FastAPI** 的绝大部分功能。

每章的内容循序渐进，但又围绕着各自的主题，您可以直接阅读所需的章节。

本教程还可以作为参考手册。

供您随时查阅。

## 运行代码

所有实例代码都可以直接使用（实际上，这些代码都是测试过的 Python 文件）。

把代码复制到 `main.py`，就可以运行教程中的示例，然后，用以下命令启动 `uvicorn`：

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

**强烈建议**您在本机编辑、运行教程中的示例代码，上手体验实际的效果。

FastAPI 真正的优势在于对编辑器的支持：只需手动输入很少的代码，支持所有类型检查，代码补全等功能。

---

## 安装 FastAPI

第一步是安装 FastAPI。

学习本教程，需要安装所有可选依赖支持库：

<div class="termy">

```console
$ pip install fastapi[all]

---> 100%
```

</div>

......上述命令还安装了运行 FastAPI 代码的服务器 -  `uvicorn`。

!!! note "笔记"

    可以单独安装每个支持库。
    
    将应用部署到生产环境，执行以下命令：
    
    ```
    pip install fastapi
    ```
    
    此外，还要安装 `uvicorn` 作为服务器：
    
    ```
    pip install uvicorn[standard]
    ```
    
    其他可选依赖支持库也可以单独安装。

## 高级用户指南

学习完**用户指南**后，您还可以继续学习**高级用户指南**。

**高级用户指南**基于本教程，核心概念是一样的，但介绍了更多功能。

建议您首先阅读**本教程**（即**用户指南**）。

只要学完**本教程**，就可以开发完整的应用，然后再根据需要，使用**高级用户指南**中的功能，扩展应用。
