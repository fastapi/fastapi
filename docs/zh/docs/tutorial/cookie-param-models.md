# Cookie 参数模型 { #cookie-parameter-models }

如果你有一组相关的 **cookie**，你可以创建一个 **Pydantic 模型**来声明它们。🍪

这将允许你在**多个地方**能够**重用模型**，并且可以一次性声明所有参数的验证方式和元数据。😎

/// note | 注意

自 FastAPI 版本 `0.115.0` 起支持此功能。🤓

///

/// tip | 提示

此技术同样适用于 `Query` 、 `Cookie` 和 `Header` 。😎

///

## 带有 Pydantic 模型的 Cookie { #cookies-with-a-pydantic-model }

在 **Pydantic** 模型中声明所需的 **cookie** 参数，然后将参数声明为 `Cookie` ：

{* ../../docs_src/cookie_param_models/tutorial001.py hl[9:12,16] *}

**FastAPI** 将从请求中接收到的 **cookie** 中**提取**出**每个字段**的数据，并提供你定义的 Pydantic 模型。

## 查看文档 { #check-the-docs }

你可以在文档 UI 的 `/docs` 中查看定义的 cookie：

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// note | 注意

请记住，由于**浏览器**以特殊方式**处理 cookie**，并在后台进行操作，因此它们**不会**轻易允许 **JavaScript** 访问这些 cookie。

如果你访问 `/docs` 的 **API 文档 UI**，你将能够查看你*路径操作*的 cookie **文档**。

但是即使你**填写数据**并点击“执行”，由于文档界面使用 **JavaScript**，cookie 将不会被发送。而你会看到一条**错误**消息，就好像你没有输入任何值一样。

///

## 禁止额外的 Cookie { #forbid-extra-cookies }

在某些特殊使用情况下（可能并不常见），你可能希望**限制**你想要接收的 cookie。

你的 API 现在可以控制自己的 <dfn title="只是个玩笑，别当真。和 cookie 同意无关，不过连 API 现在都能拒绝可怜的 cookie，挺好玩的。来，吃块小饼干吧。🍪">cookie 同意</dfn>。🤪🍪

你可以使用 Pydantic 的模型配置来禁止（ `forbid` ）任何额外（ `extra` ）字段：

{* ../../docs_src/cookie_param_models/tutorial002.py hl[10] *}

如果客户端尝试发送一些**额外的 cookie**，他们将收到**错误**响应。

可怜的 cookie 通知条，费尽心思为了获得你的同意，却被<dfn title="又是个玩笑，别理我。给你的小饼干配点咖啡吧。☕">API 拒绝了</dfn>。🍪

例如，如果客户端尝试发送一个值为 `good-list-please` 的 `santa_tracker` cookie，客户端将收到一个**错误**响应，告知他们 `santa_tracker` <dfn title="圣诞老人不赞成没有小饼干。🎅 好吧，不再讲 cookie 的笑话了。">cookie 是不允许的</dfn>：

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

## 组合参数模型 { #combine-parameter-models }

你可以将多个 cookie 参数模型与单独的 cookie 参数及依赖项组合使用。每个模型都会独立提取和验证，具体说明请参阅[查询参数模型](query-param-models.md#combine-parameter-models)。

每个模型的 `extra` 配置适用于所有 cookie 参数，包括在其他模型或依赖项中声明的参数。使用 `extra="forbid"` 时，该模型之外的任何 cookie 都会被拒绝。使用 `extra="allow"` 时，这些 cookie 会作为模型的额外字段包含在内。

## 可选 Cookie 参数模型 { #optional-cookie-parameter-models }

使用 `| None` 并将默认值设为 `None` 来声明 cookie 参数模型，即可将这组参数设为可选。

{* ../../docs_src/cookie_param_models/tutorial003.py hl[15] *}

如果既未发送 `theme` 也未发送 `locale`，则 `preferences` 为 `None`。如果发送了其中任意一个，FastAPI 就会验证模型，并要求两个字段都存在。

默认值、额外字段和 OpenAPI 的规则与[可选查询参数模型](query-param-models.md#optional-query-parameter-models)相同。

## 总结 { #summary }

你可以使用 **Pydantic 模型**在 **FastAPI** 中声明 <dfn title="临走前再吃一块小饼干吧。🍪">**cookie**</dfn>。😎
