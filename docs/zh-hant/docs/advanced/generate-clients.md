# 產生 SDK { #generating-sdks }

由於 **FastAPI** 建立在 **OpenAPI** 規格之上，其 API 能以許多工具都能理解的標準格式來描述。

這讓你能輕鬆產生最新的**文件**、多語言的用戶端程式庫（<abbr title="Software Development Kits - 軟體開發套件">**SDKs**</abbr>），以及與程式碼保持同步的**測試**或**自動化工作流程**。

在本指南中，你將學會如何為你的 FastAPI 後端產生 **TypeScript SDK**。

## 開源 SDK 產生器 { #open-source-sdk-generators }

其中一個相當萬用的選擇是 <a href="https://openapi-generator.tech/" class="external-link" target="_blank">OpenAPI Generator</a>，它支援**多種程式語言**，並能從你的 OpenAPI 規格產生 SDK。

針對 **TypeScript 用戶端**，<a href="https://heyapi.dev/" class="external-link" target="_blank">Hey API</a> 是專門打造的解決方案，為 TypeScript 生態系提供最佳化的體驗。

你可以在 <a href="https://openapi.tools/#sdk" class="external-link" target="_blank">OpenAPI.Tools</a> 找到更多 SDK 產生器。

/// tip

FastAPI 會自動產生 **OpenAPI 3.1** 規格，因此你使用的任何工具都必須支援這個版本。

///

## 來自 FastAPI 贊助商的 SDK 產生器 { #sdk-generators-from-fastapi-sponsors }

本節重點介紹由贊助 FastAPI 的公司提供的**創投支持**與**公司維運**的解決方案。這些產品在高品質的自動產生 SDK 之外，還提供**額外功能**與**整合**。

透過 ✨ [**贊助 FastAPI**](../help-fastapi.md#sponsor-the-author){.internal-link target=_blank} ✨，這些公司幫助確保框架與其**生態系**維持健康且**永續**。

他們的贊助也展現對 FastAPI **社群**（你）的高度承諾，不僅關心提供**優良服務**，也支持 **FastAPI** 作為一個**穩健且蓬勃的框架**。🙇

例如，你可以嘗試：

* <a href="https://speakeasy.com/editor?utm_source=fastapi+repo&utm_medium=github+sponsorship" class="external-link" target="_blank">Speakeasy</a>
* <a href="https://www.stainless.com/?utm_source=fastapi&utm_medium=referral" class="external-link" target="_blank">Stainless</a>
* <a href="https://developers.liblab.com/tutorials/sdk-for-fastapi?utm_source=fastapi" class="external-link" target="_blank">liblab</a>

其中有些方案也可能是開源或提供免費方案，讓你不需財務承諾就能試用。其他商業的 SDK 產生器也不少，你可以在網路上找到。🤓

## 建立 TypeScript SDK { #create-a-typescript-sdk }

先從一個簡單的 FastAPI 應用開始：

{* ../../docs_src/generate_clients/tutorial001_py310.py hl[7:9,12:13,16:17,21] *}

注意這些 *路徑操作* 為請求與回應的有效載荷定義了所用的模型，使用了 `Item` 與 `ResponseMessage` 這兩個模型。

### API 文件 { #api-docs }

如果你前往 `/docs`，你會看到其中包含了請求要送出的資料與回應接收的資料之**結構（schemas）**：

<img src="/img/tutorial/generate-clients/image01.png">

你之所以能看到這些結構，是因為它們在應用內以模型宣告了。

這些資訊都在應用的 **OpenAPI 結構**中，並顯示在 API 文件裡。

同樣包含在 OpenAPI 中的模型資訊，也可以用來**產生用戶端程式碼**。

### Hey API { #hey-api }

當我們有含模型的 FastAPI 應用後，就能用 Hey API 來產生 TypeScript 用戶端。最快的方法是透過 npx：

```sh
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

這會在 `./src/client` 產生一個 TypeScript SDK。

你可以在他們的網站了解如何<a href="https://heyapi.dev/openapi-ts/get-started" class="external-link" target="_blank">安裝 `@hey-api/openapi-ts`</a>，以及閱讀<a href="https://heyapi.dev/openapi-ts/output" class="external-link" target="_blank">產生的輸出內容</a>。

### 使用 SDK { #using-the-sdk }

現在你可以匯入並使用用戶端程式碼。大致看起來會像這樣，你會發現方法有自動完成：

<img src="/img/tutorial/generate-clients/image02.png">

你也會對要送出的有效載荷獲得自動完成：

<img src="/img/tutorial/generate-clients/image03.png">

/// tip

注意 `name` 與 `price` 的自動完成，這是由 FastAPI 應用中的 `Item` 模型所定義。

///

你在送出的資料上也會看到行內錯誤：

<img src="/img/tutorial/generate-clients/image04.png">

回應物件同樣有自動完成：

<img src="/img/tutorial/generate-clients/image05.png">

## 含標籤的 FastAPI 應用 { #fastapi-app-with-tags }

在許多情況下，你的 FastAPI 應用會更大，你可能會用標籤將不同群組的 *路徑操作* 分開。

例如，你可以有一個 **items** 區塊與另一個 **users** 區塊，並透過標籤區分：

{* ../../docs_src/generate_clients/tutorial002_py310.py hl[21,26,34] *}

### 使用標籤產生 TypeScript 用戶端 { #generate-a-typescript-client-with-tags }

若你為使用標籤的 FastAPI 應用產生用戶端，產生器通常也會依標籤將用戶端程式碼分開。

如此一來，用戶端程式碼就能有條理地正確分組與排列：

<img src="/img/tutorial/generate-clients/image06.png">

在此例中，你會有：

* `ItemsService`
* `UsersService`

### 用戶端方法名稱 { #client-method-names }

目前像 `createItemItemsPost` 這樣的產生方法名稱看起來不太俐落：

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

……那是因為用戶端產生器對每個 *路徑操作* 都使用 OpenAPI 內部的**操作 ID（operation ID）**。

OpenAPI 要求每個操作 ID 在所有 *路徑操作* 之間必須唯一，因此 FastAPI 會用**函式名稱**、**路徑**與 **HTTP 方法/操作**來產生該操作 ID，如此便能確保操作 ID 的唯一性。

接下來我會示範如何把它變得更好看。🤓

## 自訂 Operation ID 與更好的方法名稱 { #custom-operation-ids-and-better-method-names }

你可以**修改**這些操作 ID 的**產生方式**，讓它們更簡潔，並在用戶端中得到**更簡潔的方法名稱**。

在這種情況下，你需要用其他方式確保每個操作 ID 都是**唯一**的。

例如，你可以確保每個 *路徑操作* 都有標籤，接著根據**標籤**與 *路徑操作* 的**名稱**（函式名稱）來產生操作 ID。

### 自訂唯一 ID 產生函式 { #custom-generate-unique-id-function }

FastAPI 會為每個 *路徑操作* 使用一個**唯一 ID**，它會被用於**操作 ID**，以及任何請求或回應所需的自訂模型名稱。

你可以自訂該函式。它接收一個 APIRoute 並回傳字串。

例如，下面使用第一個標籤（你通常只會有一個標籤）以及 *路徑操作* 的名稱（函式名稱）。

接著你可以將這個自訂函式以 `generate_unique_id_function` 參數傳給 **FastAPI**：

{* ../../docs_src/generate_clients/tutorial003_py310.py hl[6:7,10] *}

### 使用自訂 Operation ID 產生 TypeScript 用戶端 { #generate-a-typescript-client-with-custom-operation-ids }

現在，如果你再次產生用戶端，會看到方法名稱已改善：

<img src="/img/tutorial/generate-clients/image07.png">

如你所見，方法名稱現在包含標籤與函式名稱，不再包含 URL 路徑與 HTTP 操作的資訊。

### 為用戶端產生器預處理 OpenAPI 規格 { #preprocess-the-openapi-specification-for-the-client-generator }

產生的程式碼仍有一些**重複資訊**。

我們已經知道這個方法與 **items** 相關，因為該字已出現在 `ItemsService`（取自標籤）中，但方法名稱仍然加上了標籤名稱做前綴。😕

對於 OpenAPI 本身，我們可能仍想保留，因為那能確保操作 ID 是**唯一**的。

但就產生用戶端而言，我們可以在產生前**修改** OpenAPI 的操作 ID，來讓方法名稱更**簡潔**、更**乾淨**。

我們可以把 OpenAPI JSON 下載到 `openapi.json` 檔案，然後用像這樣的腳本**移除該標籤前綴**：

{* ../../docs_src/generate_clients/tutorial004_py310.py *}

//// tab | Node.js

```Javascript
{!> ../../docs_src/generate_clients/tutorial004.js!}
```

////

如此一來，操作 ID 會從 `items-get_items` 之類的字串，變成單純的 `get_items`，讓用戶端產生器能產生更簡潔的方法名稱。

### 使用預處理後的 OpenAPI 產生 TypeScript 用戶端 { #generate-a-typescript-client-with-the-preprocessed-openapi }

由於最終結果現在是在 `openapi.json` 檔案中，你需要更新輸入位置：

```sh
npx @hey-api/openapi-ts -i ./openapi.json -o src/client
```

產生新的用戶端後，你現在會得到**乾淨的方法名稱**，同時保有所有的**自動完成**、**行內錯誤**等功能：

<img src="/img/tutorial/generate-clients/image08.png">

## 好處 { #benefits }

使用自動產生的用戶端時，你會得到以下項目的**自動完成**：

* 方法
* 本文中的請求有效載荷、查詢參數等
* 回應的有效載荷

你也會對所有內容獲得**行內錯誤**提示。

而且每當你更新後端程式碼並**重新產生**前端（用戶端），新的 *路徑操作* 會以方法形式可用、舊的會被移除，其他任何變更也都會反映到產生的程式碼中。🤓

這也代表只要有任何變更，便會自動**反映**到用戶端程式碼；而當你**建置**用戶端時，如果使用的資料有任何**不匹配**，就會直接報錯。

因此，你能在開發週期的很早期就**偵測到許多錯誤**，而不必等到錯誤在正式環境的最終使用者那裡才出現，然後才開始追查問題所在。✨
