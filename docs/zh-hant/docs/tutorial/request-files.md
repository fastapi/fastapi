# 請求中的檔案 { #request-files }

你可以使用 `File` 定義由用戶端上傳的檔案。

/// info

若要接收上傳的檔案，請先安裝 <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>。

請先建立並啟用一個[虛擬環境](../virtual-environments.md){.internal-link target=_blank}，然後安裝，例如：

```console
$ pip install python-multipart
```

因為上傳的檔案是以「表單資料」送出的。

///

## 匯入 `File` { #import-file }

從 `fastapi` 匯入 `File` 與 `UploadFile`：

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[3] *}

## 定義 `File` 參數 { #define-file-parameters }

和 `Body` 或 `Form` 一樣的方式建立檔案參數：

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[9] *}

/// info

`File` 是直接繼承自 `Form` 的類別。

但請記住，當你從 `fastapi` 匯入 `Query`、`Path`、`File` 等時，它們其實是回傳特殊類別的函式。

///

/// tip

要宣告檔案本文，必須使用 `File`，否則參數會被解讀為查詢參數或本文（JSON）參數。

///

檔案會以「表單資料」上傳。

如果你將路徑操作函式（path operation function）的參數型別宣告為 `bytes`，**FastAPI** 會替你讀取檔案，你會以 `bytes` 取得內容。

請注意，這表示整個內容會存放在記憶體中，適合小檔案。

但在許多情況下，使用 `UploadFile` 會更好。

## 使用 `UploadFile` 的檔案參數 { #file-parameters-with-uploadfile }

將檔案參數型別設為 `UploadFile`：

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[14] *}

使用 `UploadFile` 相較於 `bytes` 有數個優點：

* 你不必在參數的預設值使用 `File()`。
* 它使用「spooled」檔案：
    * 檔案在記憶體中保存到某個大小上限，超過上限後會存到磁碟。
* 因此適合處理大型檔案（例如圖片、影片、大型二進位檔等），而不會耗盡記憶體。
* 你可以取得上傳檔案的中繼資料。
* 它提供一個<a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">類檔案</a>的 `async` 介面。
* 它會提供實際的 Python <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> 物件，你可以直接傳給需要類檔案物件的其他函式或函式庫。

### `UploadFile` { #uploadfile }

`UploadFile` 具有以下屬性：

* `filename`：一個 `str`，為上傳的原始檔名（例如 `myimage.jpg`）。
* `content_type`：一個 `str`，為內容類型（MIME type / media type）（例如 `image/jpeg`）。
* `file`：一個 <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a>（<a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">類檔案</a>物件）。這是真正的 Python 檔案物件，你可以直接傳給期待「類檔案」物件的其他函式或函式庫。

`UploadFile` 有以下 `async` 方法。它們底層會呼叫對應的檔案方法（使用內部的 `SpooledTemporaryFile`）。

* `write(data)`：將 `data`（`str` 或 `bytes`）寫入檔案。
* `read(size)`：讀取檔案的 `size`（`int`）個位元組/字元。
* `seek(offset)`：移動到檔案中的位元組位置 `offset`（`int`）。
    * 例如，`await myfile.seek(0)` 會移到檔案開頭。
    * 當你已經執行過 `await myfile.read()`，之後需要再次讀取內容時特別有用。
* `close()`：關閉檔案。

由於這些都是 `async` 方法，你需要以 await 呼叫它們。

例如，在 `async` 的路徑操作函式中可這樣讀取內容：

```Python
contents = await myfile.read()
```

若是在一般的 `def` 路徑操作函式中，你可以直接存取 `UploadFile.file`，例如：

```Python
contents = myfile.file.read()
```

/// note | `async` 技術細節

當你使用這些 `async` 方法時，**FastAPI** 會在執行緒池中執行對應的檔案方法並等待結果。

///

/// note | Starlette 技術細節

**FastAPI** 的 `UploadFile` 直接繼承自 **Starlette** 的 `UploadFile`，但新增了一些必要部分，使其與 **Pydantic** 及 FastAPI 其他部分相容。

///

## 什麼是「表單資料」 { #what-is-form-data }

HTML 表單（`<form></form>`）送到伺服器的資料通常使用一種「特殊」編碼，與 JSON 不同。

**FastAPI** 會從正確的位置讀取該資料，而不是當作 JSON。

/// note | 技術細節

表單資料在不包含檔案時，通常使用媒體型別 `application/x-www-form-urlencoded` 編碼。

但當表單包含檔案時，會使用 `multipart/form-data` 編碼。若你使用 `File`，**FastAPI** 會知道要從請求本文的正確部分取得檔案。

若想進一步了解這些編碼與表單欄位，請參考 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network - Mozilla 開發者網路">MDN</abbr> Web Docs 的 <code>POST</code></a>。

///

/// warning

你可以在一個路徑操作中宣告多個 `File` 與 `Form` 參數，但不能同時宣告預期以 JSON 接收的 `Body` 欄位，因為此請求的本文會使用 `multipart/form-data` 而不是 `application/json`。

這不是 **FastAPI** 的限制，而是 HTTP 協定本身的規範。

///

## 可選的檔案上傳 { #optional-file-upload }

可透過一般型別註解並將預設值設為 `None` 使檔案成為可選：

{* ../../docs_src/request_files/tutorial001_02_an_py310.py hl[9,17] *}

## `UploadFile` 搭配額外中繼資料 { #uploadfile-with-additional-metadata }

你也可以在 `UploadFile` 上搭配 `File()`，例如用來設定額外的中繼資料：

{* ../../docs_src/request_files/tutorial001_03_an_py310.py hl[9,15] *}

## 多檔案上傳 { #multiple-file-uploads }

可以同時上傳多個檔案。

它們會同屬於以「表單資料」送出的同一個表單欄位。

要這麼做，將型別宣告為 `bytes` 或 `UploadFile` 的 `list`：

{* ../../docs_src/request_files/tutorial002_an_py310.py hl[10,15] *}

你會如宣告所示，收到由 `bytes` 或 `UploadFile` 組成的 `list`。

/// note | 技術細節

你也可以使用 `from starlette.responses import HTMLResponse`。

**FastAPI** 為了讓你（開發者）更方便，提供與 `starlette.responses` 相同的內容作為 `fastapi.responses`。但大多數可用的回應類型其實直接來自 Starlette。

///

### 多檔案上傳且包含額外中繼資料 { #multiple-file-uploads-with-additional-metadata }

同樣地，即使對 `UploadFile`，你也可以用 `File()` 設定額外參數：

{* ../../docs_src/request_files/tutorial003_an_py310.py hl[11,18:20] *}

## 小結 { #recap }

使用 `File`、`bytes` 與 `UploadFile` 來宣告請求中要上傳的檔案，這些檔案會以表單資料送出。
