# 取得目前使用者 { #get-current-user }

在前一章，基於依賴注入系統的安全機制會把一個 `token`（作為 `str`）提供給*路徑操作函式*：

{* ../../docs_src/security/tutorial001_an_py310.py hl[12] *}

但這還不太有用。

讓它改為回傳目前使用者吧。

## 建立使用者模型 { #create-a-user-model }

先建立一個 Pydantic 的使用者模型。

就像用 Pydantic 宣告請求體一樣，我們也可以在其他地方使用它：

{* ../../docs_src/security/tutorial002_an_py310.py hl[5,12:6] *}

## 建立 `get_current_user` 依賴 { #create-a-get-current-user-dependency }

讓我們建立一個依賴 `get_current_user`。

記得依賴可以有子依賴嗎？

`get_current_user` 會依賴我們先前建立的相同 `oauth2_scheme`。

如同先前在*路徑操作*中直接做的一樣，新的依賴 `get_current_user` 會從子依賴 `oauth2_scheme` 接收一個作為 `str` 的 `token`：

{* ../../docs_src/security/tutorial002_an_py310.py hl[25] *}

## 取得使用者 { #get-the-user }

`get_current_user` 會使用我們建立的（假的）工具函式，它接收一個作為 `str` 的 token，並回傳我們的 Pydantic `User` 模型：

{* ../../docs_src/security/tutorial002_an_py310.py hl[19:22,26:27] *}

## 注入目前使用者 { #inject-the-current-user }

現在我們可以在*路徑操作*中用相同的 `Depends` 來使用 `get_current_user`：

{* ../../docs_src/security/tutorial002_an_py310.py hl[31] *}

注意我們把 `current_user` 的型別宣告為 Pydantic 的 `User` 模型。

這能在函式內提供自動補全與型別檢查的協助。

/// tip | 提示

你可能記得，請求體也會用 Pydantic 模型宣告。

這裡因為你使用了 `Depends`，**FastAPI** 不會混淆。

///

/// check | 檢查

這個依賴系統的設計讓我們可以有不同的依賴（不同的 "dependables"），都回傳 `User` 模型。

我們不受限於只能有一個能回傳該類型資料的依賴。

///

## 其他模型 { #other-models }

現在你可以在*路徑操作函式*中直接取得目前使用者，並在**依賴注入**層處理安全機制，使用 `Depends`。

而且你可以為安全需求使用任意模型或資料（本例中是 Pydantic 模型 `User`）。

但你不受限於某個特定的資料模型、類別或型別。

想在模型中只有 `id` 與 `email` 而沒有任何 `username`？當然可以。你可以用同樣的工具達成。

想只用一個 `str`？或只用一個 `dict`？或直接使用資料庫類別的模型實例？都可以，一樣運作。

你的應用其實沒有真人使用者登入，而是機器人、bot，或其他系統，只持有 access token？同樣沒有問題。

只要用任何你的應用需要的模型、類別或資料庫即可。**FastAPI** 的依賴注入系統都支援。

## 程式碼大小 { #code-size }

這個範例看起來可能有點冗長。記住我們把安全、資料模型、工具函式與*路徑操作*混在同一個檔案中。

但重點在這裡。

安全與依賴注入相關的內容只需要寫一次。

你可以把它設計得再複雜都沒問題，仍然只需在單一位置寫一次，依然具備完整的彈性。

但你可以有成千上萬個端點（*路徑操作*）共用同一套安全系統。

而且它們全部（或你想要的一部分）都可以重用這些依賴，或你建立的其他依賴。

而所有這些上千個*路徑操作*都可以小到只要 3 行：

{* ../../docs_src/security/tutorial002_an_py310.py hl[30:32] *}

## 回顧 { #recap }

現在你可以在*路徑操作函式*中直接取得目前使用者。

我們已經完成一半了。

我們只需要再新增一個*路徑操作*，讓使用者/用戶端實際送出 `username` 與 `password`。

下一步就會做。
