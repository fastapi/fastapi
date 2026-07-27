# 安全性 { #security }

有許多方式可以處理安全性、身分驗證與授權。

而且這通常是一個複雜且「困難」的主題。

在許多框架與系統中，光是處理安全性與身分驗證就要花費大量心力與程式碼（很多情況下可能佔了全部程式碼的 50% 以上）。

**FastAPI** 提供多種工具，讓你能以標準方式輕鬆、快速地處理「安全性」，而不必先研究並學會所有安全性規範。

但在此之前，先釐清幾個小概念。

## 急著上手？ { #in-a-hurry }

如果你不在意這些術語，只需要立刻加入以使用者名稱與密碼為基礎的身分驗證與安全性，就直接跳到後續章節。

## OAuth2 { #oauth2 }

OAuth2 是一套規範，定義了多種處理身分驗證與授權的方法。

它相當龐大，涵蓋許多複雜的使用情境。

它也包含使用「第三方」進行身分驗證的方式。

這正是各種「使用 Facebook、Google、X（Twitter）、GitHub 登入」系統在底層採用的機制。

### OAuth 1 { #oauth-1 }

過去有 OAuth 1，和 OAuth2 非常不同，也更複雜，因為它直接規範了如何加密通訊。

它現在並不流行，也很少被使用。

OAuth2 不規範通訊如何加密，而是假設你的應用會透過 HTTPS 提供服務。

/// tip | 提示
在部署相關章節中，你會看到如何使用 Traefik 與 Let's Encrypt 免費設定 HTTPS。
///

## OpenID Connect { #openid-connect }

OpenID Connect 是基於 **OAuth2** 的另一套規範。

它只是擴充了 OAuth2，釐清了 OAuth2 中相對模糊的部份，以提升互通性。

例如，Google 登入使用的是 OpenID Connect（其底層使用 OAuth2）。

但 Facebook 登入不支援 OpenID Connect，它有自己風格的 OAuth2。

### OpenID（不是「OpenID Connect」） { #openid-not-openid-connect }

過去也有一個「OpenID」規範。它試圖解決與 **OpenID Connect** 相同的問題，但不是建立在 OAuth2 之上。

因此，它是一套完全額外、獨立的系統。

它現在並不流行，也很少被使用。

## OpenAPI { #openapi }

OpenAPI（先前稱為 Swagger）是一套用於構建 API 的開放規範（現為 Linux 基金會的一部分）。

**FastAPI** 建立在 **OpenAPI** 之上。

這使得它能提供多種自動化的互動式文件介面、程式碼產生等功能。

OpenAPI 提供定義多種安全性「方案」。

透過使用它們，你可以善用這些基於標準的工具，包括這些互動式文件系統。

OpenAPI 定義了下列安全性方案：

* `apiKey`：應用程式特定的金鑰，來源可以是：
    * 查詢參數。
    * 標頭（header）。
    * Cookie。
* `http`：標準的 HTTP 驗證系統，包括：
    * `bearer`：使用 `Authorization` 標頭，值為 `Bearer ` 加上一個 token。這是從 OAuth2 延伸而來。
    * HTTP Basic 驗證。
    * HTTP Digest 等。
* `oauth2`：所有 OAuth2 的安全性處理方式（稱為「flows」）。
    * 其中數個 flow 適合用來建立 OAuth 2.0 身分驗證提供者（如 Google、Facebook、X（Twitter）、GitHub 等）：
        * `implicit`
        * `clientCredentials`
        * `authorizationCode`
    * 但有一個特定的 flow 可直接在同一個應用中處理身分驗證：
        * `password`：後續幾個章節會示範這個。
* `openIdConnect`：提供一種方式來定義如何自動發現 OAuth2 的身分驗證資訊。
    * 這種自動探索機制即由 OpenID Connect 規範定義。

/// tip | 提示
整合像 Google、Facebook、X（Twitter）、GitHub 等其他身分驗證/授權提供者也是可行而且相對容易。

最複雜的部分其實是打造一個類似那樣的身分驗證/授權提供者，但 **FastAPI** 提供了工具，能替你處理繁重工作，讓你更輕鬆完成。
///

## **FastAPI** 工具 { #fastapi-utilities }

FastAPI 在 `fastapi.security` 模組中為上述各種安全性方案提供了多種工具，讓這些機制更容易使用。

接下來的章節會示範如何使用這些 **FastAPI** 提供的工具，為你的 API 加入安全性。

你也會看到它如何自動整合到互動式文件系統中。
