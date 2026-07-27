# 用覆寫測試相依 { #testing-dependencies-with-overrides }

## 在測試期間覆寫相依 { #overriding-dependencies-during-testing }

有些情境你可能想在測試時覆寫（override）某個相依（dependency）。

你不希望執行原本的相依（以及它可能具有的任何子相依）。

相反地，你想提供一個只在測試期間使用的不同相依（可能只在特定測試中），並回傳一個可以在原本相依值被使用之處使用的值。

### 使用情境：外部服務 { #use-cases-external-service }

例如你有一個需要呼叫的外部驗證提供者。

你傳送一個 token，它會回傳一個已驗證的使用者。

這個提供者可能按每個請求收費，而且呼叫它可能比在測試中使用固定的模擬使用者多花一些時間。

你大概只想對外部提供者測試一次，而不需要在每個測試都呼叫它。

在這種情況下，你可以覆寫用來呼叫該提供者的相依，並在測試中使用自訂的相依來回傳一個模擬使用者。

### 使用 `app.dependency_overrides` 屬性 { #use-the-app-dependency-overrides-attribute }

對這些情況，你的 FastAPI 應用程式有一個屬性 `app.dependency_overrides`，它是一個簡單的 `dict`。

要在測試時覆寫某個相依，把原始相依（函式）作為鍵，並把你的覆寫相依（另一個函式）作為值。

接著 FastAPI 會呼叫這個覆寫，而不是原本的相依。

{* ../../docs_src/dependency_testing/tutorial001_an_py310.py hl[26:27,30] *}

/// tip

你可以為應用程式中任何地方使用到的相依設定覆寫。

原始相依可以用在*路徑操作函式*、*路徑操作裝飾器*（當你不使用其回傳值時）、`.include_router()` 呼叫等。

FastAPI 仍然能夠將其覆寫。

///

然後你可以將 `app.dependency_overrides` 設為空的 `dict` 以重設（移除）所有覆寫：

```Python
app.dependency_overrides = {}
```

/// tip

如果只想在某些測試中覆寫相依，你可以在測試開始時（測試函式內）設定覆寫，並在結束時（測試函式結尾）重設。

///
