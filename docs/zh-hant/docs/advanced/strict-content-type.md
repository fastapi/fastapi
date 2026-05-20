# 嚴格的 Content-Type 檢查 { #strict-content-type-checking }

預設情況下，FastAPI 會對 JSON 請求主體使用嚴格的 `Content-Type` 標頭檢查。也就是說，JSON 請求必須包含有效的 `Content-Type` 標頭（例如 `application/json`），請求主體（body）才能被解析為 JSON。

## CSRF 風險 { #csrf-risk }

這個預設行為在某個非常特定的情境下，能對一類跨站請求偽造（CSRF, Cross-Site Request Forgery）攻擊提供保護。

這類攻擊利用了瀏覽器在以下情況下允許腳本發送請求而不進行任何 CORS 預檢（preflight）檢查的事實：

- 沒有 `Content-Type` 標頭（例如以 `fetch()` 並使用 `Blob` 作為 body）
- 且沒有送出任何身分驗證憑證

這種攻擊主要與以下情境相關：

- 應用在本機（例如 `localhost`）或內部網路中執行
- 並且應用沒有任何身分驗證，假設同一個網路中的任何請求都可被信任

## 攻擊範例 { #example-attack }

假設你打造了一個在本機執行 AI 代理（AI agent）的方法。

它提供一個 API：

```
http://localhost:8000/v1/agents/multivac
```

同時也有一個前端：

```
http://localhost:8000
```

/// tip | 提示

請注意兩者的主機（host）相同。

///

接著你可以透過前端讓 AI 代理代你執行動作。

由於它在本機執行、而非公開的網際網路上，你決定不設定任何身分驗證，只信任對本機網路的存取。

然後你的某位使用者可能安裝並在本機執行它。

接著他可能打開一個惡意網站，例如：

```
https://evilhackers.example.com
```

該惡意網站會使用 `fetch()` 並以 `Blob` 作為 body，向本機的 API 發送請求：

```
http://localhost:8000/v1/agents/multivac
```

即使惡意網站與本機應用的主機不同，瀏覽器也不會觸發 CORS 預檢請求，因為：

- 它在未經任何身分驗證的情況下執行，不需要送出任何憑證。
- 由於缺少 `Content-Type` 標頭，瀏覽器認為它並未傳送 JSON。

接著，惡意網站就能讓本機的 AI 代理替使用者向前老闆發飆傳訊... 或做更糟的事。😅

## 公開的網際網路 { #open-internet }

如果你的應用部署在公開的網際網路上，你不會「信任網路」而允許任何人在未經身分驗證的情況下發送具權限的請求。

攻擊者可以直接執行腳本向你的 API 發送請求，無需透過瀏覽器互動，因此你多半已經對任何具權限的端點做了防護。

在這種情況下，這種攻擊／風險不適用於你。

此風險與攻擊主要與應用只在本機或內部網路上執行，且「僅依賴此為保護」的情境相關。

## 允許沒有 Content-Type 的請求 { #allowing-requests-without-content-type }

若你需要支援未送出 `Content-Type` 標頭的客戶端，可以將 `strict_content_type=False` 以停用嚴格檢查：

{* ../../docs_src/strict_content_type/tutorial001_py310.py hl[4] *}

啟用此設定後，缺少 `Content-Type` 標頭的請求會將其主體解析為 JSON，這與舊版 FastAPI 的行為相同。

/// info | 資訊

此行為與設定新增於 FastAPI 0.132.0。

///
