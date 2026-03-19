# Body - 更新 { #body-updates }

## 使用 `PUT` 取代式更新 { #update-replacing-with-put }

要更新一個項目，你可以使用 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">HTTP `PUT`</a> 操作。

你可以使用 `jsonable_encoder` 將輸入資料轉換為可儲存為 JSON 的資料（例如用於 NoSQL 資料庫）。例如把 `datetime` 轉成 `str`。

{* ../../docs_src/body_updates/tutorial001_py310.py hl[28:33] *}

`PUT` 用於接收應該取代現有資料的資料。

### 關於取代的警告 { #warning-about-replacing }

這表示，如果你想用 `PUT` 並在 body 中包含以下內容來更新項目 `bar`：

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

由於這裡沒有包含已儲存的屬性 `"tax": 20.2`，輸入的模型會採用預設值 `"tax": 10.5`。

最終資料會以這個「新的」 `tax` 值 `10.5` 被儲存。

## 使用 `PATCH` 進行部分更新 { #partial-updates-with-patch }

你也可以使用 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">HTTP `PATCH`</a> 操作來進行*部分*更新。

這表示你只需傳送想要更新的資料，其餘保持不變。

/// note | 注意

`PATCH` 相較於 `PUT` 較少被使用、也較不為人知。

許多團隊甚至在部分更新時也只用 `PUT`。

你可以依需求自由選用，**FastAPI** 不會強制規範。

但本指南會大致示範它們各自的設計用法。

///

### 使用 Pydantic 的 `exclude_unset` 參數 { #using-pydantics-exclude-unset-parameter }

如果要接收部分更新，在 Pydantic 模型的 `.model_dump()` 中使用 `exclude_unset` 參數非常實用。

例如 `item.model_dump(exclude_unset=True)`。

這會產生一個只包含建立 `item` 模型時實際設定過之欄位的 `dict`，不含預設值。

接著你可以用它來生成只包含實際設定（請求中傳來）的資料之 `dict`，省略預設值：

{* ../../docs_src/body_updates/tutorial002_py310.py hl[32] *}

### 使用 Pydantic 的 `update` 參數 { #using-pydantics-update-parameter }

接著，你可以用 `.model_copy()` 建立現有模型的副本，並傳入含有要更新資料之 `dict` 到 `update` 參數。

例如 `stored_item_model.model_copy(update=update_data)`：

{* ../../docs_src/body_updates/tutorial002_py310.py hl[33] *}

### 部分更新摘要 { #partial-updates-recap }

總結一下，若要套用部分更新，你可以：

*（可選）使用 `PATCH` 取代 `PUT`。
* 取回已儲存的資料。
* 將該資料放入一個 Pydantic 模型。
* 從輸入模型產生一個不含預設值的 `dict`（使用 `exclude_unset`）。
    * 如此即可只更新使用者實際設定的值，而不會以模型的預設值覆寫已儲存的值。
* 建立已儲存模型的副本，並以收到的部分更新值更新其屬性（使用 `update` 參數）。
* 將該副本模型轉成可儲存到資料庫的型別（例如使用 `jsonable_encoder`）。
    * 這與再次使用模型的 `.model_dump()` 類似，但它會確保（並轉換）所有值為可轉為 JSON 的資料型別，例如把 `datetime` 轉為 `str`。
* 將資料儲存到資料庫。
* 回傳更新後的模型。

{* ../../docs_src/body_updates/tutorial002_py310.py hl[28:35] *}

/// tip | 提示

其實你也可以在 HTTP `PUT` 操作中使用同一套技巧。

但此處示例使用 `PATCH`，因為它正是為這類情境設計的。

///

/// note | 注意

請注意，輸入的模型依然會被驗證。

因此，如果你希望接收可以省略所有屬性的部分更新，你需要一個所有屬性皆為可選（具預設值或為 `None`）的模型。

為了區分用於更新（全部可選）與用於建立（欄位為必填）的模型，你可以參考 [額外模型](extra-models.md){.internal-link target=_blank} 中的做法。

///
