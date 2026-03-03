# HTTP 基本認證 { #http-basic-auth }

在最簡單的情況下，你可以使用 HTTP Basic 認證。

在 HTTP Basic 認證中，應用程式會期待一個包含使用者名稱與密碼的標頭。

如果沒有接收到，會回傳 HTTP 401「Unauthorized」錯誤。

並回傳一個 `WWW-Authenticate` 標頭，其值為 `Basic`，以及可選的 `realm` 參數。

這會告訴瀏覽器顯示內建的使用者名稱與密碼提示視窗。

接著，當你輸入該使用者名稱與密碼時，瀏覽器會自動在標頭中送出它們。

## 簡單的 HTTP 基本認證 { #simple-http-basic-auth }

- 匯入 `HTTPBasic` 與 `HTTPBasicCredentials`。
- 使用 `HTTPBasic` 建立一個「`security` scheme」。
- 在你的*路徑操作*中以依賴的方式使用該 `security`。
- 它會回傳一個 `HTTPBasicCredentials` 型別的物件：
    - 其中包含傳來的 `username` 與 `password`。

{* ../../docs_src/security/tutorial006_an_py310.py hl[4,8,12] *}

當你第一次嘗試開啟該 URL（或在文件中點擊 "Execute" 按鈕）時，瀏覽器會要求輸入你的使用者名稱與密碼：

<img src="/img/tutorial/security/image12.png">

## 檢查使用者名稱 { #check-the-username }

以下是一個更完整的範例。

使用一個依賴來檢查使用者名稱與密碼是否正確。

為此，使用 Python 標準模組 <a href="https://docs.python.org/3/library/secrets.html" class="external-link" target="_blank">`secrets`</a> 來比對使用者名稱與密碼。

`secrets.compare_digest()` 需要接收 `bytes`，或是只包含 ASCII 字元（英文字符）的 `str`。這表示它無法處理像 `á` 這樣的字元，例如 `Sebastián`。

為了處理這點，我們會先將 `username` 與 `password` 以 UTF-8 編碼成 `bytes`。

接著我們可以使用 `secrets.compare_digest()` 來確認 `credentials.username` 等於 `"stanleyjobson"`，而 `credentials.password` 等於 `"swordfish"`。

{* ../../docs_src/security/tutorial007_an_py310.py hl[1,12:24] *}

這大致等同於：

```Python
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # 回傳錯誤
    ...
```

但藉由使用 `secrets.compare_digest()`，可以防禦一種稱為「計時攻擊」的攻擊。

### 計時攻擊 { #timing-attacks }

什麼是「計時攻擊」呢？

想像有攻擊者在嘗試猜測使用者名稱與密碼。

他們送出一個帶有使用者名稱 `johndoe` 與密碼 `love123` 的請求。

接著，你的應用程式中的 Python 程式碼等同於：

```Python
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

當 Python 比較 `johndoe` 的第一個 `j` 與 `stanleyjobson` 的第一個 `s` 時，會立刻回傳 `False`，因為已經知道兩個字串不同，覺得「沒必要浪費計算資源繼續比較剩下的字元」。你的應用程式便會回應「Incorrect username or password」。

但接著攻擊者改用使用者名稱 `stanleyjobsox` 與密碼 `love123` 嘗試。

你的應用程式程式碼會做類似：

```Python
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Python 會必須先比較完整的 `stanleyjobso`（在 `stanleyjobsox` 與 `stanleyjobson` 之中都一樣），才會發現兩個字串不同。因此回覆「Incorrect username or password」會多花一些微秒。

#### 回應時間幫了攻擊者 { #the-time-to-answer-helps-the-attackers }

此時，透過觀察伺服器回覆「Incorrect username or password」多花了幾個微秒，攻擊者就知道他們有某些地方猜對了，前幾個字母是正確的。

接著他們會再嘗試，知道它更可能接近 `stanleyjobsox` 而不是 `johndoe`。

#### 「專業」的攻擊 { #a-professional-attack }

當然，攻擊者不會手動嘗試這一切，他們會寫程式來做，可能每秒進行上千或上百萬次測試，一次只多猜中一個正確字母。

但這樣做，幾分鐘或幾小時內，他們就能在我們應用程式「協助」下，僅靠回應時間就猜出正確的使用者名稱與密碼。

#### 用 `secrets.compare_digest()` 修正 { #fix-it-with-secrets-compare-digest }

但在我們的程式碼中實際使用的是 `secrets.compare_digest()`。

簡而言之，將 `stanleyjobsox` 與 `stanleyjobson` 比較所花的時間，會與將 `johndoe` 與 `stanleyjobson` 比較所花的時間相同；密碼也一樣。

如此一來，在應用程式程式碼中使用 `secrets.compare_digest()`，就能安全地防禦這整類的安全攻擊。

### 回傳錯誤 { #return-the-error }

在偵測到憑證不正確之後，回傳一個狀態碼為 401 的 `HTTPException`（與未提供憑證時相同），並加上 `WWW-Authenticate` 標頭，讓瀏覽器再次顯示登入提示：

{* ../../docs_src/security/tutorial007_an_py310.py hl[26:30] *}
