# 使用密碼（與雜湊）的 OAuth2、以 Bearer 搭配 JWT 權杖 { #oauth2-with-password-and-hashing-bearer-with-jwt-tokens }

現在我們已經有完整的安全流程了，接下來用 <abbr title="JSON Web Tokens - JSON 網路權杖">JWT</abbr> 權杖與安全的密碼雜湊，讓應用真正安全。

這份程式碼可以直接用在你的應用中，把密碼雜湊存進資料庫等等。

我們會從上一章的內容繼續往下擴充。

## 關於 JWT { #about-jwt }

JWT 的意思是「JSON Web Tokens」。

它是一種把 JSON 物件編碼成一段長且緊密（沒有空白）的字串的標準。看起來像這樣：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

它不是加密的，所以任何人都可以從內容還原出資訊。

但它是簽名過的。因此當你收到一個你所簽發的權杖時，你可以驗證確實是你簽發的。

如此一來，你可以建立一個（例如）有效期為 1 週的權杖。當使用者隔天帶著這個權杖回來時，你就知道該使用者仍然登入在你的系統中。

一週後，權杖會過期，使用者就不再被授權，需要再次登入以取得新的權杖。而如果使用者（或第三方）試圖修改權杖來改變有效期，你也能發現，因為簽名不會相符。

如果你想玩玩看 JWT 權杖並了解其運作，請參考 <a href="https://jwt.io/" class="external-link" target="_blank">https://jwt.io</a>。

## 安裝 `PyJWT` { #install-pyjwt }

我們需要安裝 `PyJWT` 才能在 Python 中產生與驗證 JWT 權杖。

請先建立並啟用一個[虛擬環境](../../virtual-environments.md){.internal-link target=_blank}，然後安裝 `pyjwt`：

<div class="termy">

```console
$ pip install pyjwt

---> 100%
```

</div>

/// info | 說明

如果你打算使用像 RSA 或 ECDSA 這類的數位簽章演算法，應該安裝帶有加密函式庫相依的 `pyjwt[crypto]`。

更多內容可參考 <a href="https://pyjwt.readthedocs.io/en/latest/installation.html" class="external-link" target="_blank">PyJWT 安裝文件</a>。

///

## 密碼雜湊 { #password-hashing }

「雜湊」是指把某些內容（此處為密碼）轉換成一串看起來像亂碼的位元組序列（其實就是字串）。

每當你輸入完全相同的內容（完全相同的密碼），就會得到完全相同的亂碼。

但你無法從這串亂碼再反推回原本的密碼。

### 為什麼要用密碼雜湊 { #why-use-password-hashing }

如果你的資料庫被偷了，竊賊拿到的不是使用者的明文密碼，而只是雜湊值。

因此，竊賊無法直接拿該密碼去嘗試登入其他系統（由於許多使用者在各處都用同一組密碼，這會很危險）。

## 安裝 `pwdlib` { #install-pwdlib }

pwdlib 是一個很棒的 Python 套件，用來處理密碼雜湊。

它支援多種安全的雜湊演算法與相關工具。

建議使用的演算法是「Argon2」。

請先建立並啟用一個[虛擬環境](../../virtual-environments.md){.internal-link target=_blank}，然後以 Argon2 支援安裝 pwdlib：

<div class="termy">

```console
$ pip install "pwdlib[argon2]"

---> 100%
```

</div>

/// tip | 提示

使用 `pwdlib`，你甚至可以把它設定為能讀取由 **Django**、**Flask** 的安全外掛或其他許多系統所建立的密碼。

例如，你可以讓 Django 應用與 FastAPI 應用共用同一個資料庫中的資料。或者逐步遷移一個 Django 應用，同樣使用該資料庫。

而你的使用者可以同時從 Django 應用或 **FastAPI** 應用登入。

///

## 雜湊與驗證密碼 { #hash-and-verify-the-passwords }

從 `pwdlib` 匯入我們需要的工具。

用建議設定建立一個 PasswordHash 執行個體——它會用於雜湊與驗證密碼。

/// tip | 提示

pwdlib 也支援 bcrypt 雜湊演算法，但不包含傳統（legacy）演算法——若需要處理過時的雜湊，建議使用 passlib 函式庫。

例如，你可以用它讀取並驗證由其他系統（如 Django）產生的密碼，但針對任何新密碼則改用像 Argon2 或 Bcrypt 這類的不同演算法來雜湊。

並同時與所有這些格式相容。

///

建立一個工具函式來雜湊使用者送來的密碼。

再建立另一個工具來驗證收到的密碼是否符合已儲存的雜湊。

以及另一個用於驗證並回傳使用者的工具。

{* ../../docs_src/security/tutorial004_an_py310.py hl[8,49,51,58:59,62:63,72:79] *}

當以不存在於資料庫的使用者名稱呼叫 `authenticate_user` 時，我們仍然會拿一個假的雜湊去跑一次 `verify_password`。

這可確保無論使用者名稱是否有效，端點的回應時間都大致相同，避免可用來枚舉既有使用者名稱的「計時攻擊」（timing attacks）。

/// note | 注意

如果你查看新的（假）資料庫 `fake_users_db`，你會看到雜湊後的密碼現在長這樣：`"$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc"`。

///

## 處理 JWT 權杖 { #handle-jwt-tokens }

匯入剛安裝的模組。

建立一把隨機的密鑰（secret key）用於簽署 JWT 權杖。

要產生安全的隨機密鑰可使用以下指令：

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

將輸出的值複製到變數 `SECRET_KEY`（不要使用範例中的那一組）。

建立變數 `ALGORITHM` 指定用來簽署 JWT 權杖的演算法，設為 `"HS256"`。

建立一個權杖有效期的變數。

定義一個用於權杖端點回應的 Pydantic Model。

建立一個工具函式來產生新的 access token。

{* ../../docs_src/security/tutorial004_an_py310.py hl[4,7,13:15,29:31,82:90] *}

## 更新相依項目 { #update-the-dependencies }

更新 `get_current_user`，讓它仍接收相同的權杖，但這次改用 JWT 權杖。

解碼收到的權杖、驗證它，並回傳目前的使用者。

如果權杖無效，立即回傳一個 HTTP 錯誤。

{* ../../docs_src/security/tutorial004_an_py310.py hl[93:110] *}

## 更新 `/token` 路徑操作 { #update-the-token-path-operation }

用權杖有效期建立一個 `timedelta`。

建立真正的 JWT access token 並回傳它。

{* ../../docs_src/security/tutorial004_an_py310.py hl[121:136] *}

### 關於 JWT「主體」`sub` 的技術細節 { #technical-details-about-the-jwt-subject-sub }

JWT 規範說有個鍵 `sub`，代表權杖的主體（subject）。

使用它是可選的，但通常會把使用者的識別資訊放在這裡，所以我們在此採用。

JWT 除了用來識別使用者並允許他直接對你的 API 執行操作外，也可用於其他用途。

例如，你可以識別一台「車」或一篇「部落格文章」。

接著可以替該實體加上權限，如「drive」（對車而言）或「edit」（對文章而言）。

然後你可以把該 JWT 權杖交給某個使用者（或機器人），他們就能用它來執行那些動作（開車、或編輯文章），甚至不需要有帳號，只要使用你的 API 所產生的 JWT 權杖即可。

基於這些概念，JWT 能用在更複雜的情境中。

在那些情境裡，數個實體可能擁有相同的 ID，例如 `foo`（使用者 `foo`、車 `foo`、以及文章 `foo`）。

為了避免 ID 衝突，在為使用者建立 JWT 權杖時，你可以替 `sub` 的值加上前綴，例如 `username:`。因此在這個例子中，`sub` 的值可以是：`username:johndoe`。

要記住的重要點是：`sub` 必須是在整個應用中唯一的識別子，並且必須是字串。

## 試試看 { #check-it }

啟動伺服器並前往文件頁：<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你會看到這樣的介面：

<img src="/img/tutorial/security/image07.png">

用和先前相同的方式授權應用。

使用下列認證資訊：

Username: `johndoe`
Password: `secret`

/// check | 檢查

注意在程式碼中完全沒有明文密碼「`secret`」，我們只有雜湊後的版本。

///

<img src="/img/tutorial/security/image08.png">

呼叫端點 `/users/me/`，你會得到類似這樣的回應：

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="/img/tutorial/security/image09.png">

如果你打開開發者工具，可以看到送出的資料只包含權杖；密碼只會在第一次請求（用來驗證使用者並取得 access token）時送出，之後就不會再送：

<img src="/img/tutorial/security/image10.png">

/// note | 注意

留意標頭 `Authorization`，其值是以 `Bearer ` 開頭。

///

## 進階用法：`scopes` { #advanced-usage-with-scopes }

OAuth2 有「scopes」的概念。

你可以用它們替 JWT 權杖加上一組特定的權限。

接著你可以把這個權杖直接交給某個使用者或第三方，讓他們在一組受限條件下與你的 API 互動。

你可以在之後的「進階使用者指南」學到如何使用它們，以及它們如何整合進 **FastAPI**。

## 小結 { #recap }

依照你目前學到的內容，你可以用 OAuth2 與 JWT 等標準，設定一個安全的 **FastAPI** 應用。

在幾乎任何框架中，安全性處理都會很快變得相當複雜。

許多能大幅簡化工作的套件，往往必須在資料模型、資料庫與可用功能上做出很多取捨。而有些過度簡化的套件底層其實存在安全弱點。

---

**FastAPI** 不會在任何資料庫、資料模型或工具上做妥協。

它給你完全的彈性，讓你挑選最適合你專案的組合。

而且你可以直接使用許多維護良好且被廣泛採用的套件，例如 `pwdlib` 與 `PyJWT`，因為 **FastAPI** 不需要任何複雜機制就能整合外部套件。

同時它也提供工具來在不犧牲彈性、穩健或安全的前提下，盡可能地簡化流程。

你可以用相對簡單的方式使用並實作像 OAuth2 這樣的安全標準協定。

你可以在「進階使用者指南」進一步了解如何使用 OAuth2 的「scopes」，以實作更細緻的權限系統，並遵循相同的標準。帶有 scopes 的 OAuth2 是許多大型身份驗證供應商（如 Facebook、Google、GitHub、Microsoft、X（Twitter）等）用來授權第三方應用代表其使用者與其 API 互動的機制。
