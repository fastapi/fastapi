# 是否將輸入與輸出使用不同的 OpenAPI 結構描述 { #separate-openapi-schemas-for-input-and-output-or-not }

自從 Pydantic v2 發佈後，生成的 OpenAPI 比以往更精確也更正確。😎

實際上，在某些情況下，同一個 Pydantic 模型在 OpenAPI 中會同時有兩個 JSON Schema：分別用於輸入與輸出，這取決於它是否有預設值。

來看看它如何運作，以及若需要時該如何調整。

## 作為輸入與輸出的 Pydantic 模型 { #pydantic-models-for-input-and-output }

假設你有一個帶有預設值的 Pydantic 模型，如下所示：

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:7] hl[7] *}

### 輸入用模型 { #model-for-input }

如果你把這個模型用作輸入，如下所示：

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:15] hl[14] *}

...則 `description` 欄位將不是必填。因為它的預設值是 `None`。

### 文件中的輸入模型 { #input-model-in-docs }

你可以在文件中確認，`description` 欄位沒有紅色星號，表示不是必填：

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image01.png">
</div>

### 輸出用模型 { #model-for-output }

但如果你把同一個模型用作輸出，如下所示：

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py hl[19] *}

...由於 `description` 有預設值，就算你沒有為該欄位回傳任何內容，它仍會有那個預設值。

### 輸出回應資料的模型 { #model-for-output-response-data }

在互動式文件中試用並檢視回應時，儘管程式碼沒有為其中一個 `description` 欄位加入任何內容，JSON 回應仍包含預設值（`null`）：

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image02.png">
</div>

這代表該欄位一定會有值，只是有時候值可能是 `None`（在 JSON 中為 `null`）。

因此，使用你 API 的用戶端不必檢查值是否存在，可以假設該欄位一定存在；只是有些情況下它的值會是預設的 `None`。

在 OpenAPI 中，描述這種情況的方式是將該欄位標記為必填，因為它一定存在。

因此，同一個模型的 JSON Schema 會依用於輸入或輸出而不同：

- 用於輸入時，`description` 不是必填
- 用於輸出時，`description` 是必填（且可能為 `None`，在 JSON 中為 `null`）

### 文件中的輸出模型 { #model-for-output-in-docs }

你也可以在文件中檢視輸出模型，`name` 與 `description` 都以紅色星號標示為必填：

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image03.png">
</div>

### 文件中的輸入與輸出模型 { #model-for-input-and-output-in-docs }

如果你查看 OpenAPI 中所有可用的結構描述（JSON Schema），會看到有兩個：`Item-Input` 與 `Item-Output`。

對於 `Item-Input`，`description` 不是必填，沒有紅色星號。

但對於 `Item-Output`，`description` 是必填，有紅色星號。

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image04.png">
</div>

有了 Pydantic v2 的這個特性，你的 API 文件會更精確；若你有自動產生的用戶端與 SDK，它們也會更精確，提供更好的開發者體驗與一致性。🎉

## 不要分開結構描述 { #do-not-separate-schemas }

不過，在某些情況下，你可能會希望輸入與輸出使用相同的結構描述。

最常見的情境是：你已經有一些自動產生的用戶端程式碼／SDK，目前還不想全部更新；也許之後會做，但不是現在。

在這種情況下，你可以在 FastAPI 中透過參數 `separate_input_output_schemas=False` 停用這個功能。

/// info

自 FastAPI `0.102.0` 起新增 `separate_input_output_schemas` 的支援。🤓

///

{* ../../docs_src/separate_openapi_schemas/tutorial002_py310.py hl[10] *}

### 文件中輸入與輸出使用相同結構描述的模型 { #same-schema-for-input-and-output-models-in-docs }

此時輸入與輸出將共用同一個模型結構描述，只有 `Item`，其中 `description` 不是必填：

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image05.png">
</div>
