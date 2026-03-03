# 簡易 OAuth2：Password 與 Bearer { #simple-oauth2-with-password-and-bearer }

現在從上一章延伸，補上缺少的部分，完成整個安全流程。

## 取得 `username` 與 `password` { #get-the-username-and-password }

我們要使用 **FastAPI** 提供的安全性工具來取得 `username` 與 `password`。

OAuth2 規範中，當使用「password flow」（我們現在使用的）時，用戶端／使用者必須以表單資料送出 `username` 與 `password` 欄位。

而且規範要求欄位名稱必須就是這兩個，所以像是 `user-name` 或 `email` 都不行。

但別擔心，你在前端要怎麼呈現給最終使用者都可以。

而你的資料庫模型也可以使用任何你想要的欄位名稱。

不過在登入的路徑操作（path operation）裡，我們需要使用這些名稱，才能符合規範（例如才能使用整合的 API 文件系統）。

規範也說明 `username` 與 `password` 必須以表單資料傳送（也就是這裡不能用 JSON）。

### `scope` { #scope }

規範也說用戶端可以再送一個表單欄位「`scope`」。

欄位名稱是單數的 `scope`，但實際上是由多個以空白分隔的「scopes」組成的一長串字串。

每個「scope」就是一個（不含空白的）字串。

它們通常用來宣告特定的權限，例如：

- `users:read` 或 `users:write` 是常見的例子
- `instagram_basic` 用在 Facebook / Instagram
- `https://www.googleapis.com/auth/drive` 用在 Google

/// info

在 OAuth2 裡，「scope」只是用來宣告特定所需權限的一個字串。

不論裡面是否包含像 `:` 之類的字元，或是否是一個 URL，都沒差。

那些都是實作細節。

對 OAuth2 而言，它們就是字串而已。

///

## 取得 `username` 與 `password` 的程式碼 { #code-to-get-the-username-and-password }

現在用 **FastAPI** 提供的工具來處理。

### `OAuth2PasswordRequestForm` { #oauth2passwordrequestform }

先匯入 `OAuth2PasswordRequestForm`，並在 `/token` 的路徑操作中，搭配 `Depends` 當作依賴使用：

{* ../../docs_src/security/tutorial003_an_py310.py hl[4,78] *}

`OAuth2PasswordRequestForm` 是一個類別型依賴，它宣告了一個表單本文，包含：

- `username`
- `password`
- 可選的 `scope` 欄位，內容是一個由空白分隔的長字串
- 可選的 `grant_type`

/// tip

依規範，實際上需要一個 `grant_type` 欄位且固定值為 `password`，但 `OAuth2PasswordRequestForm` 並不會強制檢查。

如果你需要強制檢查，請改用 `OAuth2PasswordRequestFormStrict` 取代 `OAuth2PasswordRequestForm`。

///

- 可選的 `client_id`（本例不需要）
- 可選的 `client_secret`（本例不需要）

/// info

`OAuth2PasswordRequestForm` 並不是像 `OAuth2PasswordBearer` 那樣對 **FastAPI** 來說的特殊類別。

`OAuth2PasswordBearer` 會讓 **FastAPI** 知道它是一個 security scheme，因此會以那種方式加入 OpenAPI。

但 `OAuth2PasswordRequestForm` 只是你也可以自己撰寫的一個類別型依賴，或是你也可以直接宣告 `Form` 參數。

只是因為這是很常見的用例，所以 **FastAPI** 直接內建提供，讓事情更簡單。

///

### 使用表單資料 { #use-the-form-data }

/// tip

`OAuth2PasswordRequestForm` 這個依賴類別的實例不會有以空白分隔長字串的 `scope` 屬性，而是會有一個 `scopes` 屬性，裡面是各個 scope 的實際字串清單。

本示例沒有使用 `scopes`，但如果你需要，功能已經在那裡了。

///

現在，從（假的）資料庫裡用表單欄位的 `username` 取得使用者資料。

如果沒有該使用者，就回傳「Incorrect username or password」的錯誤。

我們用 `HTTPException` 這個例外來回傳錯誤：

{* ../../docs_src/security/tutorial003_an_py310.py hl[3,79:81] *}

### 檢查密碼 { #check-the-password }

這時我們已經有來自資料庫的使用者資料，但還沒檢查密碼。

先把那些資料放進 Pydantic 的 `UserInDB` 模型。

你絕對不要以純文字儲存密碼，所以我們會使用（假的）密碼雜湊系統。

如果密碼不匹配，我們回傳同樣的錯誤。

#### 密碼雜湊（hashing） { #password-hashing }

「雜湊」的意思是：把一些內容（這裡是密碼）轉換成一串看起來像亂碼的位元組序列（就是字串）。

只要你輸入完全相同的內容（完全相同的密碼），就會得到完全相同的亂碼。

但你無法從這串亂碼還原回原本的密碼。

##### 為何要做密碼雜湊 { #why-use-password-hashing }

如果你的資料庫被竊取，攻擊者拿到的不是使用者的純文字密碼，而只是雜湊值。

因此攻擊者無法嘗試把那些密碼用在其他系統上（因為很多使用者在各處都用同一組密碼，這會很危險）。

{* ../../docs_src/security/tutorial003_an_py310.py hl[82:85] *}

#### 關於 `**user_dict**` { #about-user-dict }

`UserInDB(**user_dict)` 的意思是：

把 `user_dict` 的鍵和值直接當作具名參數傳入，等同於：

```Python
UserInDB(
    username = user_dict["username"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    disabled = user_dict["disabled"],
    hashed_password = user_dict["hashed_password"],
)
```

/// info

想更完整地了解 `**user_dict`，請回到[**額外模型** 的文件](../extra-models.md#about-user-in-dict){.internal-link target=_blank}。

///

## 回傳 token { #return-the-token }

`token` 端點的回應必須是 JSON 物件。

它應該有一個 `token_type`。在本例中，我們使用「Bearer」tokens，token 類型應該是「`bearer`」。

而且它還應該有一個 `access_token`，其值為包含我們存取權杖的字串。

在這個簡單示例中，我們會不安全地直接回傳相同的 `username` 當作 token。

/// tip

下一章你會看到真正安全的實作，包含密碼雜湊與 <abbr title="JSON Web Tokens - JSON 網頁權杖">JWT</abbr> tokens。

但現在先把注意力放在我們需要的這些細節上。

///

{* ../../docs_src/security/tutorial003_an_py310.py hl[87] *}

/// tip

依照規範，你應該回傳一個包含 `access_token` 與 `token_type` 的 JSON，就像這個範例。

這部分需要你自己在程式中完成，並確保使用這些 JSON key。

這幾乎是你為了符合規範而必須自行記得正確處理的唯一事情。

其餘的 **FastAPI** 都會幫你處理。

///

## 更新依賴項 { #update-the-dependencies }

接著我們要更新依賴項。

我們只想在使用者為啟用狀態時取得 `current_user`。

所以，我們新增一個依賴 `get_current_active_user`，而它本身又依賴 `get_current_user`。

這兩個依賴會在使用者不存在或未啟用時回傳 HTTP 錯誤。

因此，在端點中，只有在使用者存在、已正確驗證且為啟用狀態時，我們才會取得使用者：

{* ../../docs_src/security/tutorial003_an_py310.py hl[58:66,69:74,94] *}

/// info

這裡我們一併回傳值為 `Bearer` 的額外標頭 `WWW-Authenticate`，這也是規範的一部分。

任何 HTTP（錯誤）狀態碼 401「UNAUTHORIZED」都應該同時回傳 `WWW-Authenticate` 標頭。

在 bearer tokens（我們的情況）下，該標頭的值應該是 `Bearer`。

其實你可以省略這個額外標頭，功能仍會正常。

但此處加上它是為了遵循規範。

同時也可能有工具會期待並使用它（現在或未來），而這可能對你或你的使用者有幫助，現在或未來皆然。

這就是標準的好處...

///

## 實際操作看看 { #see-it-in-action }

開啟互動式文件：<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

### 驗證身分 { #authenticate }

點選「Authorize」按鈕。

使用下列帳密：

User: `johndoe`

Password: `secret`

<img src="/img/tutorial/security/image04.png">

在系統中完成驗證後，你會看到如下畫面：

<img src="/img/tutorial/security/image05.png">

### 取得自己的使用者資料 { #get-your-own-user-data }

現在使用 `GET` 方法呼叫路徑 `/users/me`。

你會取得自己的使用者資料，如：

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false,
  "hashed_password": "fakehashedsecret"
}
```

<img src="/img/tutorial/security/image06.png">

如果你點擊鎖頭圖示登出，然後再次嘗試相同操作，你會得到 HTTP 401 錯誤：

```JSON
{
  "detail": "Not authenticated"
}
```

### 未啟用的使用者 { #inactive-user }

現在改用一個未啟用的使用者，使用以下帳密驗證：

User: `alice`

Password: `secret2`

然後再呼叫 `GET` 方法的 `/users/me`。

你會得到「Inactive user」的錯誤，例如：

```JSON
{
  "detail": "Inactive user"
}
```

## 小結 { #recap }

你現在已經有足夠的工具，能為你的 API 以 `username` 與 `password` 實作一個完整的安全性系統。

使用這些工具，你可以讓安全性系統相容於任何資料庫，以及任何使用者或資料模型。

唯一尚未補上的細節是：它現在其實還不「安全」。

在下一章，你會看到如何使用安全的密碼雜湊函式庫與 <abbr title="JSON Web Tokens - JSON 網頁權杖">JWT</abbr> tokens。
