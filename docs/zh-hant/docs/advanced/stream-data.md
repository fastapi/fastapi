# 串流資料 { #stream-data }

如果你要串流可用 JSON 結構化的資料，應該[串流 JSON Lines](../tutorial/stream-json-lines.md)。

但如果你想串流純二進位資料或字串，以下是做法。

/// info

已在 FastAPI 0.134.0 新增。

///

## 使用情境 { #use-cases }

當你想串流純字串時可以用這個機制，例如直接轉發來自 AI LLM 服務的輸出。

你也可以用它來串流大型二進位檔案，邊讀邊將每個區塊（chunk）串流出去，而不必一次把整個檔案載入記憶體。

你也可以用同樣方式串流視訊或音訊，甚至可以在處理的同時即時產生並傳送。

## 使用 `yield` 的 `StreamingResponse` { #a-streamingresponse-with-yield }

如果在你的路徑操作函式中宣告 `response_class=StreamingResponse`，就可以用 `yield` 逐一送出每個資料區塊。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[1:23] hl[20,23] *}

FastAPI 會如實將每個資料區塊交給 `StreamingResponse`，不會嘗試將其轉換為 JSON 或其他格式。

### 非 async 路徑操作函式 { #non-async-path-operation-functions }

你也可以使用一般的 `def` 函式（沒有 `async`），並以相同方式使用 `yield`。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[26:29] hl[27] *}

### 不需要型別註解 { #no-annotation }

對於串流二進位資料，其實不需要宣告回傳型別註解。

由於 FastAPI 不會試圖用 Pydantic 將資料轉成 JSON，或以其他方式序列化，在這種情況下，型別註解僅供編輯器與工具使用，FastAPI 並不會用到它。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[32:35] hl[33] *}

這也意味著使用 `StreamingResponse` 時，你擁有自由與責任，需依需求自行產生並編碼要傳送的位元組資料，與型別註解無關。 🤓

### 串流位元組 { #stream-bytes }

一個主要用例是串流 `bytes` 而非字串，當然可以這麼做。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[44:47] hl[47] *}

## 自訂 `PNGStreamingResponse` { #a-custom-pngstreamingresponse }

在上述範例中，雖然串流了資料位元組，但回應沒有 `Content-Type` 標頭，因此用戶端不知道接收到的是哪種資料型別。

你可以建立 `StreamingResponse` 的自訂子類別，將 `Content-Type` 標頭設定為你要串流的資料型別。

例如，你可以建立 `PNGStreamingResponse`，透過 `media_type` 屬性把 `Content-Type` 設為 `image/png`：

{* ../../docs_src/stream_data/tutorial002_py310.py ln[6,19:20] hl[20] *}

接著在路徑操作函式中用 `response_class=PNGStreamingResponse` 使用這個新類別：

{* ../../docs_src/stream_data/tutorial002_py310.py ln[23:27] hl[23] *}

### 模擬檔案 { #simulate-a-file }

此範例中我們用 `io.BytesIO` 模擬檔案。它是只存在於記憶體中的類檔案物件，但提供相同的介面。

例如，我們可以像讀取一般檔案一樣，透過迭代來消耗其內容。

{* ../../docs_src/stream_data/tutorial002_py310.py ln[1:27] hl[3,12:13,25] *}

/// note | 技術細節

另外兩個變數 `image_base64` 與 `binary_image`，分別是先將影像以 Base64 編碼，接著轉成位元組，最後再傳給 `io.BytesIO`。

這只是為了讓範例能放在同一個檔案中，方便你直接複製並執行。 🥚

///

使用 `with` 區塊可確保在產生器函式（包含 `yield` 的函式）完成後關閉該類檔案物件，也就是在送完回應之後。

在這個範例中因為是存在記憶體的假檔案（`io.BytesIO`），影響不大；但若是實際檔案，務必在處理完成後關閉檔案。

### 檔案與 Async { #files-and-async }

多數情況下，類檔案物件預設不相容於 async/await。

例如，它們沒有 `await file.read()`，也不支援 `async for chunk in file`。

而且在許多情況下，讀取它們會是阻塞操作（可能阻塞事件迴圈），因為資料是從磁碟或網路讀取。

/// info

上面的範例其實是例外，因為 `io.BytesIO` 物件已在記憶體中，讀取不會阻塞任何東西。

但在多數情況下，讀取檔案或類檔案物件會造成阻塞。

///

為了避免阻塞事件迴圈，你可以將路徑操作函式宣告為一般的 `def`（而非 `async def`），這樣 FastAPI 會在 threadpool worker 上執行它，避免阻塞主事件迴圈。

{* ../../docs_src/stream_data/tutorial002_py310.py ln[30:34] hl[31] *}

/// tip

如果你需要在 async 函式內呼叫阻塞程式碼，或在阻塞函式中呼叫 async 函式，你可以使用 [Asyncer](https://asyncer.tiangolo.com)，它是 FastAPI 的姊妹函式庫。

///

### `yield from` { #yield-from }

當你在迭代某個物件（如類檔案物件），並對每個項目使用 `yield` 時，也可以用 `yield from` 直接逐項產出，省略 `for` 迴圈。

這不是 FastAPI 特有的功能，而是 Python 語法；不過這招很實用。 😎

{* ../../docs_src/stream_data/tutorial002_py310.py ln[37:40] hl[40] *}
