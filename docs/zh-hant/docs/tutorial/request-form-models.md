# 表單模型 { #form-models }

你可以使用 **Pydantic 模型** 在 FastAPI 中宣告 **表單欄位**。

/// note | 注意

要使用表單，首先安裝 [`python-multipart`](https://github.com/Kludex/python-multipart)。

將它加入你的專案：

```console
$ uv add python-multipart
```

///

/// note | 注意

此功能自 FastAPI 版本 `0.113.0` 起支援。🤓

///

## 針對表單的 Pydantic 模型 { #pydantic-models-for-forms }

你只需要宣告一個 **Pydantic 模型**，包含你要接收為 **表單欄位** 的欄位，然後將參數宣告為 `Form`：

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI** 會從請求中的 **表單資料** **擷取** **每個欄位** 的資料，並給你所定義的 Pydantic 模型。

對於 [HTML 核取方塊](request-forms.md#boolean-form-fields)，請宣告預設值為 `False` 的布林欄位。

## 檢視文件 { #check-the-docs }

你可以在 `/docs` 的文件 UI 中驗證：

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## 禁止額外的表單欄位 { #forbid-extra-form-fields }

在某些特殊情況（可能不常見）下，你可能希望將 **表單欄位** **限制** 為只有 Pydantic 模型中宣告的欄位。並**禁止**任何**額外**欄位。

/// note | 注意

此功能自 FastAPI 版本 `0.114.0` 起支援。🤓

///

你可以使用 Pydantic 的模型設定來 `forbid` 任何 `extra` 欄位：

{* ../../docs_src/request_form_models/tutorial002_an_py310.py hl[12] *}

如果用戶端嘗試傳送額外資料，將會收到**錯誤**回應。

例如，用戶端若送出以下表單欄位：

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

他們會收到一個錯誤回應，告知欄位 `extra` 不被允許：

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## 組合表單模型 { #combine-form-models }

你可以將多個表單模型與個別的 `Form` 參數組合使用。

{* ../../docs_src/request_form_models/tutorial003_an_py310.py hl[9:14,19:21] *}

用戶端以表單欄位傳送 `name`、`tags` 和 `token`。每個模型會獨立驗證表單欄位。

每個模型的 `extra` 設定都會套用至所有表單欄位，包括在其他參數或依賴項中宣告的欄位和檔案。使用 `extra="forbid"` 時，模型以外的任何欄位都會被拒絕。使用 `extra="allow"` 時，這些欄位會作為模型的額外資料納入。

如果多個宣告使用相同的表單欄位名稱，每個宣告都會驗證該欄位的值。請為共用欄位使用相容的型別和限制條件，讓 OpenAPI schema 能一致地描述這些欄位。

## 可選的表單模型 { #optional-form-models }

宣告表單模型時使用 `| None` 並將預設值設為 `None`，即可讓整組欄位變為可選。

{* ../../docs_src/request_form_models/tutorial005_an_py310.py hl[17] *}

如果既未傳送 `name` 也未傳送 `age`，`profile` 就會是 `None`。如果傳送了其中任一欄位，FastAPI 就會驗證模型，並要求提供這兩個欄位。提交空值也算是提供了欄位。

使用 `| None` 但未設定預設值時，該參數仍為必填。

額外欄位會遵循模型的 `extra` 設定。被忽略的額外欄位不會使模型被視為已提供。

僅包含未勾選核取方塊的可選模型會被省略。傳送如 `enabled=false` 這樣的值，即可明確提供該模型。

## 可選的表單模型聯集 { #optional-unions-of-form-models }

你也可以使用可選的模型聯集。

{* ../../docs_src/request_form_models/tutorial006_an_py310.py hl[9:16,21] *}

如果未傳送任何表單欄位，`contact` 就會是 `None`。請傳送 `kind=person` 搭配 `name`，或 `kind=company` 搭配 `company_name`。判別欄位會決定要驗證哪個模型。

## 組合表單模型聯集 { #combine-unions-of-form-models }

你可以將聯集與其他表單模型、個別的 `Form` 參數及 `File` 參數組合使用。每個聯集都會獨立驗證。

{* ../../docs_src/request_form_models/tutorial007_an_py310.py hl[31:35] *}

在同一份表單中傳送所有欄位。例如，傳送 `contact_type=person`、`name=Rick`、`notification_type=email`、`email=rick@example.com` 和 `token=secret`。

省略通知欄位即可讓 `notification` 保持為 `None`。

## 表單模型與檔案 { #form-models-and-files }

你也可以將表單模型與[檔案參數](request-files.md)組合使用。

{* ../../docs_src/request_form_models/tutorial004_an_py310.py hl[14] *}

在此，用戶端使用 `multipart/form-data` 傳送 `name` 欄位和 `avatar` 檔案。

## 摘要 { #summary }

你可以使用 Pydantic 模型在 FastAPI 中宣告表單欄位。😎
