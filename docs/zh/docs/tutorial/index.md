# 教程 - 用户指南 - 简介

本教程将一步步向你展示如何使用 **FastAPI** 的绝大部分特性。

各个章节的内容循序渐进，但是又围绕着单独的主题，所以你可以直接跳转到某个章节以解决你的特定需求。

本教程同样可以作为将来的参考手册。

你可以随时回到本教程并查阅你需要的内容。

## 运行代码

所有代码片段都可以复制后直接使用（它们实际上是经过测试的 Python 文件）。

要运行任何示例，请将代码复制到 `main.py` 文件中，然后使用以下命令启动 `uvicorn`：

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

强烈建议你在本地编写或复制代码，对其进行编辑并运行。

在编辑器中使用 FastAPI 会真正地展现出它的优势：只需要编写很少的代码，所有的类型检查，代码补全等等。

---

## 安装 FastAPI

第一个步骤是安装 FastAPI。

为了使用本教程，你可能需要安装所有的可选依赖及对应功能：

<div class="termy">

```console
$ pip install "fastapi[all]"

---> 100%
```

</div>

......以上安装还包括了 `uvicorn`，你可以将其用作运行代码的服务器。

!!! note
    你也可以分开来安装。

    假如你想将应用程序部署到生产环境，你可能要执行以下操作：

    ```
    pip install fastapi
    ```

    并且安装`uvicorn`来作为服务器：

    ```
    pip install "uvicorn[standard]"
    ```

    然后对你想使用的每个可选依赖项也执行相同的操作。

## 进阶用户指南

在本**教程-用户指南**之后，你可以阅读**进阶用户指南**。

**进阶用户指南**以本教程为基础，使用相同的概念，并教授一些额外的特性。

但是你应该先阅读**教程-用户指南**（即你现在正在阅读的内容）。

教程经过精心设计，使你可以仅通过**教程-用户指南**来开发一个完整的应用程序，然后根据你的需要，使用**进阶用户指南**中的一些其他概念，以不同的方式来扩展它。
