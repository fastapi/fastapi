# 表單模型 { #form-models }

你可以使用 **Pydantic 模型** 在 FastAPI 中宣告 **表單欄位**。

/// info | 說明

要使用表單，首先安裝 <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>。

請先建立[虛擬環境](../virtual-environments.md){.internal-link target=_blank}、啟用後再安裝，例如：

```console
$ pip install python-multipart
```

///

/// note | 注意

此功能自 FastAPI 版本 `0.113.0` 起支援。🤓

///

## 針對表單的 Pydantic 模型 { #pydantic-models-for-forms }

你只需要宣告一個 **Pydantic 模型**，包含你要接收為 **表單欄位** 的欄位，然後將參數宣告為 `Form`：

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI** 會從請求中的 **表單資料** 擷取 **各欄位** 的資料，並將這些資料組成你定義的 Pydantic 模型實例。

## 檢視文件 { #check-the-docs }

你可以在 `/docs` 的文件 UI 中驗證：

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## 禁止額外的表單欄位 { #forbid-extra-form-fields }

在某些特殊情況（可能不常見）下，你可能希望僅允許 Pydantic 模型中宣告的表單欄位，並禁止任何額外欄位。

/// note | 注意

此功能自 FastAPI 版本 `0.114.0` 起支援。🤓

///

你可以使用 Pydantic 的模型設定來 `forbid` 任何 `extra` 欄位：

{* ../../docs_src/request_form_models/tutorial002_an_py310.py hl[12] *}

如果用戶端嘗試傳送額外資料，將會收到錯誤回應。

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

## 摘要 { #summary }

你可以使用 Pydantic 模型在 FastAPI 中宣告表單欄位。😎
