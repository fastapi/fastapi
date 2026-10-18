# 虚拟环境 { #virtual-environments }

当你在 Python 工程中工作时，你应该使用**虚拟环境**来隔离为每个工程安装的包。

对于 FastAPI 工程，我推荐使用 [uv](https://docs.astral.sh/uv/) 来管理工程、依赖项和虚拟环境。

## 创建工程 { #create-a-project }

使用[官方安装指南](https://docs.astral.sh/uv/getting-started/installation/)安装 `uv`，然后创建一个工程：

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"
```

</div>

`uv` 会自动为工程创建虚拟环境。你不需要自己创建或激活虚拟环境。

使用 `uv run` 在工程环境中运行命令，例如：

<div class="termy">

```console
$ uv run fastapi dev
```

</div>

## 了解更多 { #learn-more }

阅读[虚拟环境指南](https://tiangolo.com/guides/virtual-environments/)以了解虚拟环境在底层是如何工作的，包括激活以及替代的 `python -m venv` 和 `pip` 工作流。
