# Cookie 參數模型 { #cookie-parameter-models }

如果你有一組彼此相關的「**Cookie**」，你可以建立一個「**Pydantic 模型**」來宣告它們。🍪

這樣你就能在**多處**重複使用該模型，並且能一次性為所有參數宣告**驗證**與**中繼資料**。😎

/// note | 注意

自 FastAPI 版本 `0.115.0` 起支援。🤓

///

/// tip

同樣的技巧也適用於 `Query`、`Cookie` 與 `Header`。😎

///

## 以 Pydantic 模型宣告 Cookie { #cookies-with-a-pydantic-model }

在 **Pydantic 模型**中宣告所需的 **Cookie** 參數，接著將參數宣告為 `Cookie`：

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI** 會從請求收到的 **Cookie** 中擷取 **每個欄位** 的資料，並交給你定義的 Pydantic 模型。

## 查看文件 { #check-the-docs }

你可以在 `/docs` 的文件介面中看到已定義的 Cookie：

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// info

請注意，由於**瀏覽器會以特殊且在背景進行的方式處理 Cookie**，因此**不會**輕易允許 **JavaScript** 存取它們。

當你前往位於 `/docs` 的 **API 文件介面**時，可以看到路徑操作的 Cookie 說明。

但即使你**填入資料**並點擊「Execute」，因為該文件介面是以 **JavaScript** 運作，Cookie 不會被送出，你會看到**錯誤**訊息，就像完全沒有填任何值一樣。

///

## 禁止額外的 Cookie { #forbid-extra-cookies }

在某些特殊情境（可能不太常見）下，你可能會想**限制**允許接收的 Cookie。

你的 API 現在也能掌控自己的 <dfn title="這只是個玩笑，提醒一下。這與 Cookie 同意無關，但有趣的是連 API 現在也能拒絕可憐的 Cookie。請收下這塊餅乾。🍪">Cookie 同意</dfn>。🤪🍪

你可以使用 Pydantic 的模型設定來 `forbid` 任何 `extra` 欄位：

{* ../../docs_src/cookie_param_models/tutorial002_an_py310.py hl[10] *}

如果客戶端嘗試送出**額外的 Cookie**，會收到**錯誤**回應。

可憐的 Cookie 橫幅辛苦收集你的同意，最後卻是為了<dfn title="又是一個玩笑。別理我。來杯咖啡配餅乾吧。☕">讓 API 拒絕它</dfn>。🍪

例如，若客戶端嘗試送出名為 `santa_tracker`、值為 `good-list-please` 的 Cookie，客戶端會收到**錯誤**回應，告知 `santa_tracker` 這個 <dfn title="聖誕老人不贊同沒有餅乾。🎅 好的，不再講餅乾笑話了。">Cookie 不被允許</dfn>：

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
```

## 摘要 { #summary }

你可以在 **FastAPI** 中使用 **Pydantic 模型**來宣告 <dfn title="走之前再來一塊餅乾吧。🍪">**Cookie**</dfn>。😎
