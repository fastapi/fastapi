# 在容器中使用 FastAPI - Docker { #fastapi-in-containers-docker }

部署 FastAPI 應用時，一個常見做法是建置一個「Linux 容器映像（container image）」。通常使用 <a href="https://www.docker.com/" class="external-link" target="_blank">Docker</a> 來完成。之後你可以用多種方式部署該容器映像。

使用 Linux 容器有多種優點，包括安全性、可重現性、簡單性等。

/// tip | 提示

趕時間而且已經懂這些？直接跳到下面的 [`Dockerfile` 👇](#build-a-docker-image-for-fastapi)。

///

<details>
<summary>Dockerfile 預覽 👀</summary>

```Dockerfile
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# 若在 Nginx 或 Traefik 等代理伺服器後方執行，請加入 --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

</details>

## 什麼是容器 { #what-is-a-container }

容器（主要是 Linux 容器）是一種非常輕量的方式，用來封裝應用及其所有相依與必要檔案，並讓其與同一系統中的其他容器（其他應用或元件）隔離。

Linux 容器使用與主機（機器、虛擬機、雲端伺服器等）相同的 Linux kernel。這意味著它們非常輕量（相較於完整模擬整個作業系統的虛擬機）。

因此，容器只消耗很少的資源，與直接執行行程相當（而虛擬機會消耗更多）。

容器也有其各自隔離的執行行程（通常只有一個行程）、檔案系統與網路，簡化部署、安全性與開發等。

## 什麼是容器映像 { #what-is-a-container-image }

容器是由容器映像啟動執行的。

容器映像是所有檔案、環境變數，以及在容器中應該執行的預設指令/程式的靜態版本。這裡的「靜態」意指容器映像不在執行，它只是被封裝的檔案與 metadata。

相對於儲存的靜態內容「容器映像」，「容器」通常指執行中的實例，也就是正在被執行的東西。

當容器啟動並執行時（自容器映像啟動），它可以建立或變更檔案、環境變數等。這些變更只會存在於該容器中，不會持久化回底層的容器映像（不會寫回磁碟）。

容器映像可類比為程式檔與其內容，例如 `python` 與某個 `main.py` 檔案。

而容器本身（相對於容器映像）是映像的實際執行實例，類比為「行程」。事實上，容器只有在有行程執行時才在運作（通常只有單一行程）。當其中沒有行程在執行時，容器就會停止。

## 容器映像 { #container-images }

Docker 是用來建立與管理容器映像與容器的主要工具之一。

也有一個公開的 <a href="https://hub.docker.com/" class="external-link" target="_blank">Docker Hub</a>，內含許多工具、環境、資料庫與應用的預先製作「官方映像」。

例如，有官方的 <a href="https://hub.docker.com/_/python" class="external-link" target="_blank">Python 映像</a>。

也有許多其他針對不同用途的映像，例如資料庫：

* <a href="https://hub.docker.com/_/postgres" class="external-link" target="_blank">PostgreSQL</a>
* <a href="https://hub.docker.com/_/mysql" class="external-link" target="_blank">MySQL</a>
* <a href="https://hub.docker.com/_/mongo" class="external-link" target="_blank">MongoDB</a>
* <a href="https://hub.docker.com/_/redis" class="external-link" target="_blank">Redis</a> 等。

使用預製的容器映像很容易「組合」並使用不同工具。例如，嘗試一個新資料庫。多數情況下，你可以使用官方映像，並僅用環境變數加以設定。

如此，你可以學會關於容器與 Docker 的知識，並將這些知識重複運用到許多不同工具與元件上。

因此，你會執行多個容器，內容各不相同，例如一個資料庫、一個 Python 應用、一個帶有 React 前端應用的網頁伺服器，並透過它們的內部網路把它們連接在一起。

所有容器管理系統（例如 Docker 或 Kubernetes）都內建了這些網路功能。

## 容器與行程 { #containers-and-processes }

容器映像通常在其 metadata 中包含當容器啟動時應執行的預設程式或指令，以及要傳給該程式的參數。這與在命令列要執行的內容非常類似。

當容器啟動時，它會執行該指令/程式（雖然你可以覆寫它，讓它執行不同的指令/程式）。

只要主要行程（指令或程式）在執行，容器就會運作。

容器通常只有單一行程，但也可以由主要行程啟動子行程，如此你會在同一個容器內有多個行程。

但不可能在沒有至少一個執行中行程的情況下讓容器運作。若主要行程停止，容器也會停止。

## 建置 FastAPI 的 Docker 映像 { #build-a-docker-image-for-fastapi }

好了，現在來動手做點東西吧！🚀

我會示範如何從零開始，基於官方的 Python 映像，為 FastAPI 建置一個 Docker 映像。

這是你在多數情況下會想做的事，例如：

* 使用 Kubernetes 或類似工具
* 在 Raspberry Pi 上執行
* 使用會替你執行容器映像的雲端服務等

### 套件需求 { #package-requirements }

你的應用通常會把「套件需求」放在某個檔案中。

這主要取決於你用什麼工具來安裝那些需求。

最常見的方式是準備一個 `requirements.txt` 檔案，逐行列出套件名稱與版本。

當然，你會用與在 [關於 FastAPI 版本](versions.md){.internal-link target=_blank} 中讀到的相同概念，來設定版本範圍。

例如，你的 `requirements.txt` 可能像這樣：

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

接著你通常會用 `pip` 來安裝這些套件相依，例如：

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

</div>

/// info | 資訊

還有其他格式與工具可以用來定義與安裝套件相依。

///

### 建立 FastAPI 程式碼 { #create-the-fastapi-code }

* 建立一個 `app` 目錄並進入。
* 建立一個空的 `__init__.py` 檔案。
* 建立一個 `main.py` 檔案，內容如下：

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### Dockerfile { #dockerfile }

現在在同一個專案目錄建立一個 `Dockerfile` 檔案，內容如下：

```{ .dockerfile .annotate }
# (1)!
FROM python:3.14

# (2)!
WORKDIR /code

# (3)!
COPY ./requirements.txt /code/requirements.txt

# (4)!
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)!
COPY ./app /code/app

# (6)!
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

1. 從官方的 Python 基底映像開始。

2. 將目前工作目錄設為 `/code`。

    我們會把 `requirements.txt` 檔案與 `app` 目錄放在這裡。

3. 將需求檔案複製到 `/code` 目錄。

    先只複製需求檔案，不要複製其他程式碼。

    因為這個檔案不常變動，Docker 能偵測並在此步驟使用快取，也能啟用下一步的快取。

4. 安裝需求檔案中的套件相依。

    `--no-cache-dir` 選項告訴 `pip` 不要把下載的套件保存在本機，因為那只在 `pip` 之後還會再次安裝相同套件時才有用，而在使用容器時並非如此。

    /// note | 注意

    `--no-cache-dir` 只跟 `pip` 有關，與 Docker 或容器無關。

    ///

    `--upgrade` 選項告訴 `pip` 若套件已安裝則升級它們。

    因為前一步複製檔案可能被 Docker 快取偵測到，這一步也會在可用時使用 Docker 快取。

    在此步驟使用快取可以在開發期間反覆建置映像時，為你省下大量時間，而不必每次都重新下載並安裝所有相依。

5. 將 `./app` 目錄複製到 `/code` 目錄中。

    由於這包含了所有程式碼，也是最常變動的部分，Docker 的快取在這一步或之後的步驟將不容易被使用。

    因此，重要的是把這一步放在 `Dockerfile` 的接近結尾處，以最佳化容器映像的建置時間。

6. 設定指令使用 `fastapi run`，其底層使用 Uvicorn。

    `CMD` 接受字串清單，每個字串對應你在命令列中用空白分隔所輸入的內容。

    這個指令會從目前的工作目錄執行，也就是你先前用 `WORKDIR /code` 設定的 `/code` 目錄。

/// tip | 提示

點擊程式碼中的每個數字泡泡來查看每一行在做什麼。👆

///

/// warning | 警告

務必「總是」使用 `CMD` 指令的「exec 形式」，如下所述。

///

#### 使用 `CMD` 的 Exec 形式 { #use-cmd-exec-form }

Docker 的 <a href="https://docs.docker.com/reference/dockerfile/#cmd" class="external-link" target="_blank">`CMD`</a> 指令可以有兩種寫法：

✅ Exec 形式：

```Dockerfile
# ✅ 請這樣做
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

⛔️ Shell 形式：

```Dockerfile
# ⛔️ 請不要這樣做
CMD fastapi run app/main.py --port 80
```

務必總是使用 exec 形式，以確保 FastAPI 能夠優雅地關閉，並觸發 [lifespan events](../advanced/events.md){.internal-link target=_blank}。

你可以在 <a href="https://docs.docker.com/reference/dockerfile/#shell-and-exec-form" class="external-link" target="_blank">Docker 關於 shell 與 exec 形式的文件</a>閱讀更多。

使用 `docker compose` 時這會特別明顯。技術細節請見這段 Docker Compose 常見問題：<a href="https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop" class="external-link" target="_blank">為什麼我的服務要花 10 秒才重新建立或停止？</a>

#### 目錄結構 { #directory-structure }

你現在應該會有如下的目錄結構：

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### 位於 TLS 終止代理之後 { #behind-a-tls-termination-proxy }

如果你在 TLS 終止代理（負載平衡器）如 Nginx 或 Traefik 之後執行容器，請加上 `--proxy-headers` 選項，這會告訴 Uvicorn（透過 FastAPI CLI）信任該代理所送來的標頭，表示應用在 HTTPS 後方執行等。

```Dockerfile
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

#### Docker 快取 { #docker-cache }

這個 `Dockerfile` 中有個重要技巧：我們先只複製「相依檔案」，而不是其他程式碼。原因如下。

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

Docker 與其他工具會「增量式」建置容器映像，從 `Dockerfile` 頂端開始，逐層加入，每個指令所建立的檔案都會形成一層。

Docker 與類似工具在建置映像時也會使用內部快取；如果某檔案自上次建置以來未變更，則會重用上次建立的同一層，而不是再次複製並從零建立新層。

僅僅避免複製檔案本身或許幫助不大，但因為該步驟使用了快取，接下來的步驟也就能「使用快取」。例如，安裝相依的這個指令就能使用快取：

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

套件相依的檔案「不會經常變動」。因此，只複製該檔案，Docker 就能在此步驟「使用快取」。

接著，Docker 也就能對下一步「下載並安裝這些相依」使用快取。這正是我們能「省下大量時間」的地方。✨ 也能避免無聊的等待。😪😆

下載與安裝套件相依「可能要花好幾分鐘」，但使用「快取」最多只需幾秒。

在開發期間，你會一再建置容器映像以測試程式碼變更是否生效，累積下來這能省下許多時間。

之後，在 `Dockerfile` 的接近結尾處，我們才複製所有程式碼。由於這是「最常變動」的部分，我們把它放在接近結尾，因為幾乎總是此步驟之後的任何步驟都無法使用快取。

```Dockerfile
COPY ./app /code/app
```

### 建置 Docker 映像 { #build-the-docker-image }

現在所有檔案就緒，來建置容器映像。

* 進到專案目錄（你的 `Dockerfile` 所在，且包含 `app` 目錄）。
* 建置你的 FastAPI 映像：

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

/// tip | 提示

注意最後的 `.`，等同於 `./`，它告訴 Docker 要用哪個目錄來建置容器映像。

這裡是目前的目錄（`.`）。

///

### 啟動 Docker 容器 { #start-the-docker-container }

* 以你的映像為基礎執行一個容器：

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## 檢查 { #check-it }

你應該可以透過 Docker 容器的網址檢查，例如：<a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> 或 <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a>（或等效的、使用你的 Docker 主機）。

你會看到類似這樣：

```JSON
{"item_id": 5, "q": "somequery"}
```

## 互動式 API 文件 { #interactive-api-docs }

現在你可以前往 <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> 或 <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a>（或等效的、使用你的 Docker 主機）。

你會看到自動產生的互動式 API 文件（由 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## 替代的 API 文件 { #alternative-api-docs }

你也可以前往 <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> 或 <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a>（或等效的、使用你的 Docker 主機）。

你會看到另一種自動產生的文件（由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 為單檔 FastAPI 建置 Docker 映像 { #build-a-docker-image-with-a-single-file-fastapi }

如果你的 FastAPI 是單一檔案，例如沒有 `./app` 目錄的 `main.py`，你的檔案結構可能像這樣：

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

接著你只需要在 `Dockerfile` 中調整對應的路徑以複製該檔案：

```{ .dockerfile .annotate hl_lines="10  13" }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)!
COPY ./main.py /code/

# (2)!
CMD ["fastapi", "run", "main.py", "--port", "80"]
```

1. 將 `main.py` 直接複製到 `/code` 目錄（不需要 `./app` 目錄）。

2. 使用 `fastapi run` 來服務單檔的 `main.py` 應用。

當你把檔案傳給 `fastapi run`，它會自動偵測這是一個單一檔案而非套件的一部分，並知道如何匯入並服務你的 FastAPI 應用。😎

## 部署概念 { #deployment-concepts }

我們用容器的角度再談一次部分相同的[部署概念](concepts.md){.internal-link target=_blank}。

容器主要是簡化應用「建置與部署」流程的工具，但它們不強制特定的方式來處理這些「部署概念」，而是有多種策略可選。

好消息是，每種不同的策略都能涵蓋所有部署概念。🎉

讓我們用容器的角度回顧這些部署概念：

* HTTPS
* 開機自動執行
* 失敗重啟
* 複本（執行的行程數量）
* 記憶體
* 啟動前的前置步驟

## HTTPS { #https }

若僅聚焦於 FastAPI 應用的「容器映像」（以及稍後的執行中「容器」），HTTPS 通常會由另一個工具在「外部」處理。

它可以是另一個容器，例如使用 <a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a>，來處理「HTTPS」以及「自動」取得「憑證」。

/// tip | 提示

Traefik 與 Docker、Kubernetes 等整合良好，因此為你的容器設定與配置 HTTPS 非常容易。

///

或者，HTTPS 也可能由雲端供應商以其服務來處理（同時應用仍以容器執行）。

## 開機自動執行與重啟 { #running-on-startup-and-restarts }

通常會有另一個工具負責「啟動並執行」你的容器。

可能是直接用 Docker、Docker Compose、Kubernetes、某個雲端服務等。

在大多數（或全部）情況下，都有簡單的選項可以在開機時自動執行容器，並在失敗時重啟。例如，在 Docker 中，可用命令列選項 `--restart`。

如果不使用容器，讓應用在開機時自動執行並支援重啟可能既繁瑣又困難。但在「使用容器」時，這類功能在多數情況下都是預設包含的。✨

## 複本 - 行程數量 { #replication-number-of-processes }

如果你在有 Kubernetes、Docker Swarm Mode、Nomad，或其他類似的分散式容器管理系統的「叢集」上運作，那你大概會希望在「叢集層級」處理「複本」，而不是在每個容器內使用「行程管理器」（例如帶有 workers 的 Uvicorn）。

像 Kubernetes 這類的分散式容器管理系統，通常內建處理「容器複本」以及支援進入請求的「負載平衡」的能力——全部都在「叢集層級」。

在這些情況下，你大概會想要如[上面所述](#dockerfile)從零開始建置一個 Docker 映像，安裝你的相依，並且只執行「單一 Uvicorn 行程」，而不是使用多個 Uvicorn workers。

### 負載平衡器 { #load-balancer }

使用容器時，通常會有某個元件在「主埠口」上監聽。它也可能是另一個同時做為「TLS 終止代理」的容器來處理「HTTPS」，或類似的工具。

由於這個元件會承接請求的「負載」，並將其分配給 workers，使其（希望）「平衡」，因此也常被稱為「負載平衡器（Load Balancer）」。

/// tip | 提示

用於 HTTPS 的同一個「TLS 終止代理」元件通常也會是「負載平衡器」。

///

而在使用容器時，你用來啓動與管理它們的系統，已內建把「網路通訊」（例如 HTTP 請求）從該「負載平衡器」（也可能是「TLS 終止代理」）傳遞到你的應用容器的工具。

### 一個負載平衡器 - 多個工作容器 { #one-load-balancer-multiple-worker-containers }

使用 Kubernetes 或類似的分散式容器管理系統時，使用其內部網路機制可以讓在主「埠口」上監聽的單一「負載平衡器」，把通訊（請求）傳遞給可能的「多個執行你應用的容器」。

每個執行你應用的容器通常只有「單一行程」（例如執行你的 FastAPI 應用的 Uvicorn 行程）。它們都是「相同的容器」，執行相同的東西，但各自擁有自己的行程、記憶體等。如此即可在 CPU 的「不同核心」、甚至是「不同機器」上發揮「平行化」的效益。

而分散式容器系統中的「負載平衡器」會「輪流」把請求分配給各個執行你應用的容器。因此，每個請求都可能由多個「複製的容器」中的其中一個來處理。

通常這個「負載平衡器」也能處理送往叢集中「其他」應用的請求（例如不同網域，或不同 URL 路徑前綴），並把通訊轉送到該「其他」應用對應的容器。

### 每個容器一個行程 { #one-process-per-container }

在這種情境中，你大概會希望「每個容器只有一個（Uvicorn）行程」，因為你已在叢集層級處理了複本。

所以這種情況下，你「不會」想在容器中使用多個 workers（例如用 `--workers` 命令列選項）。你會想每個容器只執行「一個 Uvicorn 行程」（但可能有多個容器）。

在容器內再放一個行程管理器（如同多 workers 的情況）只會增加「不必要的複雜度」，而你很可能已用叢集系統處理好了。

### 多行程容器與特殊情境 { #containers-with-multiple-processes-and-special-cases }

當然，有些「特殊情況」你可能會想在「一個容器內」執行數個「Uvicorn worker 行程」。

在這些情況中，你可以用 `--workers` 命令列選項來設定要啟動的 workers 數量：

```{ .dockerfile .annotate }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# (1)!
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

1. 這裡我們使用 `--workers` 命令列選項把 worker 數量設定為 4。

以下是一些合理的例子：

#### 簡單應用 { #a-simple-app }

如果你的應用「足夠簡單」，可以在「單一伺服器」而非叢集上執行，你可能會希望在容器內使用行程管理器。

#### Docker Compose { #docker-compose }

如果你部署到「單一伺服器」（非叢集），且使用「Docker Compose」，那麼你無法輕易（用 Docker Compose）在保有共用網路與「負載平衡」的同時管理容器複本。

那你可能會想要「單一容器」搭配「行程管理器」，在其中啟動「多個 worker 行程」。

---

重點是，這些「都不是」必須盲目遵守的「鐵律」。你可以用這些想法來「評估你的使用情境」，並決定對你的系統最好的做法，看看如何管理以下概念：

* 安全性 - HTTPS
* 開機自動執行
* 失敗重啟
* 複本（執行的行程數量）
* 記憶體
* 啟動前的前置步驟

## 記憶體 { #memory }

如果你採用「每個容器一個行程」，那每個容器（若有複本則多個容器）所消耗的記憶體會是相對明確、穩定且有限的。

接著你可以在容器管理系統（例如 Kubernetes）的設定中為容器設定相同的記憶體限制與需求。如此，它就能在「可用的機器」上「複製容器」，並考量容器所需的記憶體量與叢集中機器的可用記憶體。

若你的應用「很簡單」，這可能「不是問題」，你可能不需要指定嚴格的記憶體限制。但如果你「使用大量記憶體」（例如使用機器學習模型），你應該檢查實際消耗的記憶體，並調整「每台機器上執行的容器數量」（也許還要為叢集加機器）。

若你採用「每個容器多個行程」，你就得確保啟動的行程數量不會「超過可用記憶體」。

## 啟動前的前置步驟與容器 { #previous-steps-before-starting-and-containers }

如果你使用容器（例如 Docker、Kubernetes），那有兩種主要做法可用。

### 多個容器 { #multiple-containers }

如果你有「多個容器」，且每個容器大概都只執行「單一行程」（例如在一個 Kubernetes 叢集中），那你可能會想要一個「獨立的容器」來完成「前置步驟」的工作，並只在單一容器、單一行程中執行，接著才啟動多個複本的工作容器。

/// info | 資訊

如果你使用 Kubernetes，這大概會是一個 <a href="https://kubernetes.io/docs/concepts/workloads/pods/init-containers/" class="external-link" target="_blank">Init Container</a>。

///

如果你的情境中，讓那些前置步驟「平行重複執行多次」沒有問題（例如不是在跑資料庫遷移，而只是檢查資料庫是否就緒），那也可以把這些步驟放在每個容器中、在啟動主要行程前執行。

### 單一容器 { #single-container }

如果你的架構很簡單，只有「單一容器」，接著在其中啟動多個「worker 行程」（或也可能就一個行程），那你可以在相同的容器中、於啟動應用行程前先執行這些前置步驟。

### 基底 Docker 映像 { #base-docker-image }

曾經有一個官方的 FastAPI Docker 映像：<a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>。但現在已被棄用。⛔️

你大概「不應該」使用這個基底 Docker 映像（或其他類似的）。

如果你使用 Kubernetes（或其他）並已在叢集層級設定「複本」、使用多個「容器」。在這些情況下，更好的做法是如上所述[從零建置映像](#build-a-docker-image-for-fastapi)。

若你需要多個 workers，只要使用 `--workers` 命令列選項即可。

/// note | 技術細節

這個 Docker 映像是在 Uvicorn 尚未支援管理與重啟死亡 workers 的年代所建立，因此需要用 Gunicorn 搭配 Uvicorn，為了讓 Gunicorn 管理並重啟 Uvicorn workers，而引入了相當多的複雜度。

但現在 Uvicorn（以及 `fastapi` 指令）已支援使用 `--workers`，因此沒有理由使用一個基底 Docker 映像，而不是建置你自己的（而且實際上程式碼量也差不多 😅）。

///

## 部署容器映像 { #deploy-the-container-image }

擁有容器（Docker）映像後，有多種部署方式。

例如：

* 在單一伺服器上使用 Docker Compose
* 使用 Kubernetes 叢集
* 使用 Docker Swarm Mode 叢集
* 使用像 Nomad 之類的其他工具
* 使用會接收你的容器映像並代為部署的雲端服務

## 使用 `uv` 的 Docker 映像 { #docker-image-with-uv }

如果你使用 <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">uv</a> 來安裝與管理專案，你可以參考他們的 <a href="https://docs.astral.sh/uv/guides/integration/docker/" class="external-link" target="_blank">uv Docker 指南</a>。

## 總結 { #recap }

使用容器系統（例如 Docker 與 Kubernetes）可以相對直接地處理所有「部署概念」：

* HTTPS
* 開機自動執行
* 失敗重啟
* 複本（執行的行程數量）
* 記憶體
* 啟動前的前置步驟

多數情況下，你大概不會想用任何基底映像，而是「從零建置容器映像」，以官方的 Python Docker 映像為基礎。

善用 `Dockerfile` 中指令的「順序」與「Docker 快取」，你可以「最小化建置時間」，提升生產力（並避免無聊）。😎
