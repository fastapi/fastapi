# 用户指南 - 简介

本指南将逐步介绍 **FastAPI** 的绝大部分功能。

每个章节都循序渐进，但又有各自的主题，您可以直接阅读所需章节，解决特定的 API 需求。

本指南还是参考手册。

供您随时查阅。

## 运行代码

本指南中的所有代码都能直接复制使用（实际上，这些代码都是经过测试的 Python 文件）。

要运行示例，只需把代码复制到 `main.py`，用以下命令启动 `uvicorn`：

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

**强烈建议**您在本机编辑并运行这些代码。

只在有编辑器中输入代码时，您才能真正感受到 FastAPI 的优势，体验到需要输入的代码到底有多少，还有类型检查、自动补全等功能。

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

......上述命令还安装了运行 FastAPI 应用的服务器 -  `uvicorn`。

!!! note "笔记"

    您可以单独安装各个支持库。
    
    需要把应用部署到生产环境时，首先要安装 FastAPI：
    
    ```
    pip install fastapi
    ```
    
    然后，还要安装服务器 `uvicorn`：
    
    ```
    pip install uvicorn[standard]
    ```
    
    按需单独安装其它可选依赖支持库。

## 高级用户指南

学完**用户指南**后，您还可以继续学习**高级用户指南**。

**高级用户指南**基于本指南，核心概念都一样，但介绍了更多功能。

建议您先阅读**用户指南**。

学完**用户指南**就能开发完整的 FastAPI 应用。然后，再使用**高级用户指南**中的功能扩展应用。
