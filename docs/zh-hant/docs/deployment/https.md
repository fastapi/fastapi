# 關於 HTTPS { #about-https }

人們很容易以為 HTTPS 只是「啟用或未啟用」的功能。

但實際上複雜得多。

/// tip

如果你趕時間或不在意細節，可以直接看後續章節，依照逐步指引用不同方式完成設定。

///

想從使用者角度學習 HTTPS 基礎，請參考 <a href="https://howhttps.works/" class="external-link" target="_blank">https://howhttps.works/</a>。

接著以開發者角度，談幾個關於 HTTPS 需要注意的重點：

* 對於 HTTPS，伺服器需要擁有由**第三方**簽發的**「憑證」**。
    * 這些憑證實際上是向第三方**取得**，不是「自己產生」。
* 憑證有**有效期**。
    * 會**過期**。
    * 過期後需要**續期**，也就是再向第三方**重新取得**。
* 連線加密發生在 **TCP 層**。
    * 那是在 **HTTP 的下一層**。
    * 因此，**憑證與加密**的處理會在 **進入 HTTP 之前**完成。
* **TCP 不知道「網域」**，只知道 IP 位址。
    * 關於**特定網域**的資訊會放在 **HTTP 資料**中。
* **HTTPS 憑證**是為某個**特定網域**背書，但通訊協定與加密在 TCP 層進行，發生在**尚未知道**要處理哪個網域之前。
* **預設**情況下，這表示你每個 IP 位址**只能**使用**一張 HTTPS 憑證**。
    * 不論你的伺服器多強或你在上面跑的應用多小。
    * 不過，這是有**解法**的。
* 在 **TLS** 協定（在 HTTP 之前於 TCP 層處理加密的協定）上有個**擴充**稱為 **<a href="https://en.wikipedia.org/wiki/Server_Name_Indication" class="external-link" target="_blank"><abbr title="Server Name Indication - 伺服器名稱指示">SNI</abbr></a>**。
    * 這個 SNI 擴充讓單一伺服器（單一 IP 位址）可以擁有**多張 HTTPS 憑證**，並服務**多個 HTTPS 網域／應用**。
    * 要讓它運作，伺服器上必須有一個**單一**的元件（程式）在**公用 IP**上監聽，且持有伺服器上的**所有 HTTPS 憑證**。
* 在取得安全連線**之後**，通訊協定**仍然是 HTTP**。
    * 雖然透過 **HTTP 協定**傳送，但內容是**加密**的。

常見做法是讓伺服器（機器、主機等）上跑**一個程式／HTTP 伺服器**來**管理所有 HTTPS 相關工作**：接收**加密的 HTTPS 請求**、將其**解密**成**純 HTTP 請求**轉交給同台伺服器上實際運行的 HTTP 應用（本例為 **FastAPI** 應用）、從應用取得 **HTTP 回應**、再用合適的 **HTTPS 憑證**將其**加密**並以 **HTTPS** 傳回給用戶端。這類伺服器常被稱為 **<a href="https://en.wikipedia.org/wiki/TLS_termination_proxy" class="external-link" target="_blank">TLS 終止代理 (TLS Termination Proxy)</a>**。

可作為 TLS 終止代理的選項包括：

* Traefik（也可處理憑證續期）
* Caddy（也可處理憑證續期）
* Nginx
* HAProxy

## Let's Encrypt { #lets-encrypt }

在 Let's Encrypt 之前，這些 **HTTPS 憑證**是由受信任的第三方販售。

取得這些憑證的流程過去相當繁瑣，需要許多手續，且憑證相當昂貴。

之後出現了 **<a href="https://letsencrypt.org/" class="external-link" target="_blank">Let's Encrypt</a>**。

它是 Linux Foundation 的專案，能**免費**且自動化地提供 **HTTPS 憑證**。這些憑證採用標準的密碼學安全機制，且有效期較短（約 3 個月），因此因為壽命短，**安全性其實更好**。

網域會被安全驗證，憑證會自動產生。這也讓憑證續期得以自動化。

目標是讓憑證的申請與續期自動化，讓你**永遠免費使用安全的 HTTPS**。

## 給開發者的 HTTPS { #https-for-developers }

以下以逐步範例說明一個 HTTPS API 可能長什麼樣子，著重於對開發者重要的概念。

### 網域名稱 { #domain-name }

通常會先**取得**一個**網域名稱**，接著在 DNS 伺服器（可能是同一個雲端供應商）中設定它。

你可能會租一台雲端伺服器（虛擬機）或類似的服務，並擁有一個<dfn title="不會隨時間改變；非動態的">固定</dfn>的**公用 IP 位址**。

在 DNS 伺服器中，你會設定一個紀錄（「`A record`」）指向**你的網域**所對應的**伺服器公用 IP 位址**。

這通常在初次建置時設定一次即可。

/// tip

「網域名稱」是發生在 HTTPS 之前的事情，但一切都依賴網域與 IP 位址，因此在此一併說明。

///

### DNS { #dns }

現在聚焦在實際的 HTTPS 部分。

首先，瀏覽器會向 **DNS 伺服器**查詢該**網域的 IP**，例如 `someapp.example.com`。

DNS 伺服器會回覆要使用的**IP 位址**，那就是你在 DNS 伺服器中設定的、伺服器對外的公用 IP 位址。

<img src="/img/deployment/https/https01.drawio.svg">

### TLS 握手開始 { #tls-handshake-start }

接著瀏覽器會連線到該 IP 的 **443 埠**（HTTPS 預設埠）。

通訊的第一部分是建立用戶端與伺服器之間的連線，並協商要使用哪些金鑰等密碼參數。

<img src="/img/deployment/https/https02.drawio.svg">

用戶端與伺服器為建立 TLS 連線而進行的這段互動稱為 **TLS 握手**。

### 帶 SNI 擴充的 TLS { #tls-with-sni-extension }

在特定的**IP 位址**與特定**埠**上，同一時間**只能有一個行程**在監聽。可以在同一個 IP 上監聽不同埠，但每個 IP 與埠的組合只能有一個行程。

TLS（HTTPS）預設使用 `443` 埠，因此我們需要用到這個埠。

由於只能有一個行程監聽該埠，負責監聽的會是 **TLS 終止代理**。

TLS 終止代理會存取一張或多張 **TLS 憑證**（HTTPS 憑證）。

透過上面提到的 **SNI 擴充**，TLS 終止代理會根據用戶端預期的網域，從可用的 TLS（HTTPS）憑證中挑選本次連線要用的憑證。

在這個例子中，會使用 `someapp.example.com` 的憑證。

<img src="/img/deployment/https/https03.drawio.svg">

用戶端**信任**簽發該 TLS 憑證的單位（本例為 Let's Encrypt，稍後會再談），因此可以**驗證**憑證有效。

接著，用戶端與 TLS 終止代理會以該憑證為基礎，**協商後續如何加密**整段 **TCP 通訊**。至此完成 **TLS 握手**。

之後，用戶端與伺服器之間就有一條**已加密的 TCP 連線**，這就是 TLS 所提供的能力。接著他們可以在這條連線上開始實際的 **HTTP** 通訊。

這也就是 **HTTPS** 的本質：在**安全的 TLS 連線**內傳送一般的 **HTTP**，而非在純（未加密）的 TCP 連線上。

/// tip

請注意，加密發生在 **TCP 層**，不是在 HTTP 層。

///

### HTTPS 請求 { #https-request }

現在用戶端與伺服器（更精確地說，是瀏覽器與 TLS 終止代理）之間已有**加密的 TCP 連線**，他們可以開始進行 **HTTP** 通訊。

因此，用戶端送出一個 **HTTPS 請求**。它其實就是透過加密的 TLS 連線發送的一個 HTTP 請求。

<img src="/img/deployment/https/https04.drawio.svg">

### 解密請求 { #decrypt-the-request }

TLS 終止代理會依照先前協商的方式**解密請求**，並將**純（已解密）的 HTTP 請求**轉交給運行應用的行程（例如以 Uvicorn 執行的 FastAPI 應用行程）。

<img src="/img/deployment/https/https05.drawio.svg">

### HTTP 回應 { #http-response }

應用會處理該請求，並將**純（未加密）的 HTTP 回應**送回 TLS 終止代理。

<img src="/img/deployment/https/https06.drawio.svg">

### HTTPS 回應 { #https-response }

TLS 終止代理接著會依照先前協商（起點是 `someapp.example.com` 的憑證）的方式**加密回應**，並傳回給瀏覽器。

接著，瀏覽器會驗證回應是否合法、是否使用正確的金鑰加密等。然後**解密回應**並處理。

<img src="/img/deployment/https/https07.drawio.svg">

用戶端（瀏覽器）會知道回應來自正確的伺服器，因為它使用了先前依據 **HTTPS 憑證**所協商的密碼機制。

### 多個應用 { #multiple-applications }

同一台（或多台）伺服器上可以有**多個應用**，例如其他 API 程式或資料庫。

雖然只有一個行程可以處理特定 IP 與埠的組合（本例中的 TLS 終止代理），但其他應用／行程也都能在伺服器上運行，只要它們不使用相同的**公用 IP 與埠**組合即可。

<img src="/img/deployment/https/https08.drawio.svg">

如此一來，TLS 終止代理就能為**多個網域**、多個應用處理 HTTPS 與憑證，並把請求轉發到對應的應用。

### 憑證續期 { #certificate-renewal }

在未來某個時間點，每張憑證都會**過期**（自取得起約 3 個月）。

之後，會有另一個程式（有時是另一個程式，有時也可能就是同一個 TLS 終止代理）與 Let's Encrypt 溝通並續期憑證。

<img src="/img/deployment/https/https.drawio.svg">

**TLS 憑證**是**綁定網域名稱**，不是綁定 IP 位址。

因此，要續期憑證時，續期程式需要向憑證機構（Let's Encrypt）**證明**它的確**擁有並控制該網域**。

為了達成這點、並兼顧不同應用情境，有幾種常見方式：

* **修改部分 DNS 紀錄**。
    * 為此，續期程式需要支援該 DNS 供應商的 API，因此依你使用的 DNS 供應商不同，這方式可能可行或不可行。
* **作為伺服器運行**（至少在憑證申請過程中）於該網域對應的公用 IP 上。
    * 如前所述，同一時間只有一個行程能在特定 IP 與埠上監聽。
    * 這也是為什麼讓同一個 TLS 終止代理一併處理憑證續期非常實用的原因之一。
    * 否則你可能得暫停 TLS 終止代理、啟動續期程式申請憑證、將憑證配置到 TLS 終止代理，然後再重啟 TLS 終止代理。這並不理想，因為在 TLS 終止代理停機期間，你的應用將不可用。

在不中斷服務的同時完成整個續期流程，是你會想用**獨立系統（TLS 終止代理）來處理 HTTPS**、而不是直接把 TLS 憑證掛在應用伺服器（例如 Uvicorn）上的主要原因之一。

## 代理轉發標頭 { #proxy-forwarded-headers }

當你使用代理處理 HTTPS 時，你的**應用伺服器**（例如透過 FastAPI CLI 啟動的 Uvicorn）其實不知道任何 HTTPS 的處理流程，它是用純 HTTP 與 **TLS 終止代理**通訊。

這個**代理**通常會在把請求轉發給**應用伺服器**之前，臨時加入一些 HTTP 標頭，讓應用伺服器知道該請求是由代理**轉發**過來的。

/// note | 技術細節

這些代理標頭包括：

* <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For" class="external-link" target="_blank">X-Forwarded-For</a>
* <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto" class="external-link" target="_blank">X-Forwarded-Proto</a>
* <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host" class="external-link" target="_blank">X-Forwarded-Host</a>

///

然而，因為**應用伺服器**並不知道自己在受信任的**代理**之後，預設情況下它不會信任這些標頭。

但你可以設定**應用伺服器**去信任由**代理**送來的「轉發」標頭。若你使用 FastAPI CLI，可以用 *CLI 參數* `--forwarded-allow-ips` 指定應信任哪些 IP 來的「轉發」標頭。

例如，如果**應用伺服器**只會接收來自受信任**代理**的連線，你可以設定 `--forwarded-allow-ips="*"`，也就是信任所有來源 IP，因為實際上它只會收到**代理**那個 IP 送來的請求。

如此一來，應用就能知道自己的對外 URL、是否使用 HTTPS、網域為何等資訊。

這在正確處理重新導向等情境時很有用。

/// tip

你可以在文件 [在代理後方 - 啟用代理轉發標頭](../advanced/behind-a-proxy.md#enable-proxy-forwarded-headers){.internal-link target=_blank} 中了解更多。

///

## 重點回顧 { #recap }

擁有 **HTTPS** 非常重要，而且在多數情況都相當**關鍵**。作為開發者，你在 HTTPS 上的大部分投入其實是**理解這些概念**及其運作方式。

一旦掌握了**給開發者的 HTTPS 基礎**，你就能輕鬆組合並設定不同工具，讓一切管理變得簡單。

在接下來的章節中，我會示範幾個為 **FastAPI** 應用設定 **HTTPS** 的具體例子。🔒
