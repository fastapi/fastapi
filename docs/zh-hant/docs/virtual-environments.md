# 虛擬環境 { #virtual-environments }

當你在 Python 專案中工作時，你應該使用**虛擬環境**來隔離每個專案安裝的套件。

對於 FastAPI 專案，我建議使用 [uv](https://docs.astral.sh/uv/) 來管理專案、其依賴項和虛擬環境。

## 建立一個專案 { #create-a-project }

使用[官方安裝指南](https://docs.astral.sh/uv/getting-started/installation/)安裝 `uv`，然後建立一個專案：

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"
```

</div>

`uv` 會自動為專案建立虛擬環境。你不需要自己建立或啟動虛擬環境。

使用 `uv run` 在專案環境中執行指令，例如：

<div class="termy">

```console
$ uv run fastapi dev
```

</div>

## 了解更多 { #learn-more }

閱讀[虛擬環境指南](https://tiangolo.com/guides/virtual-environments/)來了解虛擬環境在底層如何運作，包括啟動，以及替代的 `python -m venv` 和 `pip` 工作流程。
