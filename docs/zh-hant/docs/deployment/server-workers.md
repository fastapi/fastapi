# 伺服器工作處理序 - 使用 Uvicorn Workers { #server-workers-uvicorn-with-workers }

我們回顧一下先前提到的部署概念：

* 安全 - HTTPS
* 系統啟動時執行
* 重啟
* **副本（正在執行的處理序數量）**
* 記憶體
* 啟動前的前置作業

到目前為止，依照文件中的教學，你大多是透過 `fastapi` 指令啟動一個執行 Uvicorn 的伺服器程式，且只跑單一處理序。

在部署應用時，你通常會希望有一些處理序的複製來善用多核心，並能處理更多請求。

如同前一章關於 [部署概念](concepts.md){.internal-link target=_blank} 所示，你可以採用多種策略。

這裡會示範如何使用 `fastapi` 指令或直接使用 `uvicorn` 指令，搭配 Uvicorn 的工作處理序（worker processes）。

/// info

如果你使用容器（例如 Docker 或 Kubernetes），我會在下一章說明更多：[容器中的 FastAPI - Docker](docker.md){.internal-link target=_blank}。

特別是，在 **Kubernetes** 上執行時，你多半會選擇不要使用 workers，而是每個容器只跑一個 **Uvicorn 單一處理序**。我會在該章節中進一步說明。

///

## 多個工作處理序 { #multiple-workers }

你可以用命令列選項 `--workers` 來啟動多個 workers：

//// tab | `fastapi`

如果你使用 `fastapi` 指令：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run --workers 4 <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started parent process <b>[</b><font color="#34E2E2"><b>27365</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27368</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27369</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27370</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27367</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

////

//// tab | `uvicorn`

如果你偏好直接使用 `uvicorn` 指令：

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
<font color="#A6E22E">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8080</b> (Press CTRL+C to quit)
<font color="#A6E22E">INFO</font>:     Started parent process [<font color="#A1EFE4"><b>27365</b></font>]
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27368</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27369</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27370</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27367</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
```

</div>

////

這裡唯一新增的選項是 `--workers`，告訴 Uvicorn 要啟動 4 個工作處理序。

你也會看到它顯示每個處理序的 **PID**，`27365` 是父處理序（這是**處理序管理器**），另外每個工作處理序各有一個：`27368`、`27369`、`27370`、`27367`。

## 部署概念 { #deployment-concepts }

你已經看到如何使用多個 **workers** 來將應用的執行進行**平行化**，善用 CPU 的**多核心**，並能服務**更多請求**。

在上面的部署概念清單中，使用 workers 主要能幫助到**副本**這一塊，並對**重啟**也有一點幫助，但你仍需要處理其他部分：

* **安全 - HTTPS**
* **系統啟動時執行**
* ***重啟***
* 副本（正在執行的處理序數量）
* **記憶體**
* **啟動前的前置作業**

## 容器與 Docker { #containers-and-docker }

在下一章 [容器中的 FastAPI - Docker](docker.md){.internal-link target=_blank} 我會說明一些策略，幫你處理其他的**部署概念**。

我會示範如何**從零建立你的映像檔**來執行單一 Uvicorn 處理序。這個流程相當簡單，而且在使用像 **Kubernetes** 這類分散式容器管理系統時，大多情況也會這麼做。

## 重點回顧 { #recap }

你可以在 `fastapi` 或 `uvicorn` 指令中使用 `--workers` 這個 CLI 選項來啟動多個工作處理序，以善用**多核心 CPU**，**平行**執行多個處理序。

如果你要自行建置**自己的部署系統**，你可以運用這些工具與想法，同時自行處理其他部署概念。

接著看看下一章關於在容器（例如 Docker 與 Kubernetes）中使用 **FastAPI**。你會看到那些工具也有簡單的方法來解決其他**部署概念**。✨
