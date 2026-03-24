# 使用 Base64 表示位元組的 JSON { #json-with-bytes-as-base64 }

如果你的應用需要收發 JSON 資料，但其中需要包含二進位資料，你可以將它以 base64 編碼。

## Base64 與檔案 { #base64-vs-files }

請先考慮是否能用 [請求檔案](../tutorial/request-files.md) 來上傳二進位資料，並用 [自訂回應 - FileResponse](./custom-response.md#fileresponse--fileresponse-) 來傳送二進位資料，而不是把它們編碼進 JSON。

JSON 只能包含 UTF-8 編碼的字串，因此無法直接包含原始位元組。

Base64 可以把二進位資料編碼成字串，但為此會使用比原始二進位資料更多的字元，因此通常比直接使用檔案來得沒那麼有效率。

只有在確實必須把二進位資料包含在 JSON 裡，且無法改用檔案時，才使用 base64。

## Pydantic `bytes` { #pydantic-bytes }

你可以宣告含有 `bytes` 欄位的 Pydantic 模型，並在模型設定中使用 `val_json_bytes`，使其在驗證輸入的 JSON 資料時使用 base64；在驗證過程中，它會將 base64 字串解碼為位元組。

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:9,29:35] hl[9] *}

如果你查看 `/docs`，會看到欄位 `data` 需要 base64 編碼的位元組：

<div class="screenshot">
<img src="/img/tutorial/json-base64-bytes/image01.png">
</div>

你可以發送如下的請求：

```json
{
    "description": "Some data",
    "data": "aGVsbG8="
}
```

/// tip

`aGVsbG8=` 是 `hello` 的 base64 編碼。

///

接著 Pydantic 會將該 base64 字串解碼，並在模型的 `data` 欄位中提供原始位元組。

你會收到類似以下的回應：

```json
{
  "description": "Some data",
  "content": "hello"
}
```

## Pydantic `bytes` 用於輸出資料 { #pydantic-bytes-for-output-data }

你也可以在模型設定中搭配 `ser_json_bytes` 使用 `bytes` 欄位來處理輸出資料；當產生 JSON 回應時，Pydantic 會將位元組以 base64 進行序列化。

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,12:16,29,38:41] hl[16] *}

## Pydantic `bytes` 用於輸入與輸出資料 { #pydantic-bytes-for-input-and-output-data }

當然，你也可以使用同一個以 base64 設定的模型，同時處理輸入（以 `val_json_bytes` 驗證）與輸出（以 `ser_json_bytes` 序列化）的 JSON 資料。

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,19:26,29,44:46] hl[23:26] *}
