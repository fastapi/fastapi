# 請求中的表單與檔案 { #request-forms-and-files }

你可以使用 `File` 與 `Form` 同時定義檔案與表單欄位。

/// info

要接收上傳的檔案與/或表單資料，請先安裝 <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>。

請先建立並啟用一個 [虛擬環境](../virtual-environments.md){.internal-link target=_blank}，然後再安裝，例如：

```console
$ pip install python-multipart
```

///

## 匯入 `File` 與 `Form` { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py310.py hl[3] *}

## 定義 `File` 與 `Form` 參數 { #define-file-and-form-parameters }

以與 `Body` 或 `Query` 相同的方式建立檔案與表單參數：

{* ../../docs_src/request_forms_and_files/tutorial001_an_py310.py hl[10:12] *}

檔案與表單欄位會作為表單資料上傳，而你將能接收到這些檔案與欄位。

你也可以將部分檔案宣告為 `bytes`，另一些宣告為 `UploadFile`。

/// warning

你可以在一個路徑操作 (path operation) 中宣告多個 `File` 與 `Form` 參數，但不能同時再宣告預期以 JSON 接收的 `Body` 欄位，因為該請求的本文會使用 `multipart/form-data` 而非 `application/json` 進行編碼。

這不是 **FastAPI** 的限制，這是 HTTP 通訊協定本身的規範。

///

## 小結 { #recap }

當你需要在同一個請求中同時接收資料與檔案時，請搭配使用 `File` 與 `Form`。
