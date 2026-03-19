# 子應用程式 - 掛載 { #sub-applications-mounts }

若你需要兩個彼此獨立的 FastAPI 應用程式，各自擁有獨立的 OpenAPI 與文件 UI，你可以有一個主應用，並「掛載」一個（或多個）子應用程式。

## 掛載一個 **FastAPI** 應用程式 { #mounting-a-fastapi-application }

「掛載」是指在某個特定路徑下加入一個完全「獨立」的應用程式，之後該應用程式會負責處理該路徑底下的一切，使用該子應用程式中宣告的*路徑操作（path operation）*。

### 頂層應用程式 { #top-level-application }

先建立主（頂層）**FastAPI** 應用程式以及它的*路徑操作*：

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[3, 6:8] *}

### 子應用程式 { #sub-application }

接著，建立你的子應用程式及其*路徑操作*。

這個子應用程式就是另一個標準的 FastAPI 應用，但這個會被「掛載」：

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[11, 14:16] *}

### 掛載子應用程式 { #mount-the-sub-application }

在你的頂層應用程式 `app` 中，掛載子應用程式 `subapi`。

在此範例中，它會被掛載在路徑 `/subapi`：

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[11, 19] *}

### 檢查自動 API 文件 { #check-the-automatic-api-docs }

現在，用你的檔案執行 `fastapi` 指令：

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

然後開啟位於 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> 的文件。

你會看到主應用的自動 API 文件，只包含它自己的*路徑操作*：

<img src="/img/tutorial/sub-applications/image01.png">

接著，開啟子應用程式的文件：<a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">http://127.0.0.1:8000/subapi/docs</a>。

你會看到子應用程式的自動 API 文件，只包含它自己的*路徑操作*，而且都在正確的子路徑前綴 `/subapi` 之下：

<img src="/img/tutorial/sub-applications/image02.png">

如果你嘗試在任一介面中互動，它們都會正常運作，因為瀏覽器能與各自的應用程式或子應用程式通訊。

### 技術細節：`root_path` { #technical-details-root-path }

當你像上面那樣掛載子應用程式時，FastAPI 會使用 ASGI 規範中的一個機制 `root_path`，將子應用程式的掛載路徑告知它。

如此一來，子應用程式就會知道在文件 UI 使用該路徑前綴。

而且子應用程式也能再掛載自己的子應用程式，一切都能正確運作，因為 FastAPI 會自動處理所有這些 `root_path`。

你可以在[在代理伺服器之後](behind-a-proxy.md){.internal-link target=_blank}一節中進一步了解 `root_path` 與如何顯式使用它。
