# Cookie 参数模型

如果您有一组相关的 **cookie**，您可以创建一个 **Pydantic 模型**来声明它们。🍪

这将允许您在**多个地方**能够**重用模型**，并且可以一次性声明所有参数的验证方式和元数据。😎

/// note

自 FastAPI 版本 `0.115.0` 起支持此功能。🤓

///

/// tip

此技术同样适用于 `Query` 、 `Cookie` 和 `Header` 。😎

///

## 带有 Pydantic 模型的 Cookie

在 **Pydantic** 模型中声明所需的 **cookie** 参数，然后将参数声明为 `Cookie` ：

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI** 将从请求中接收到的 **cookie** 中**提取**出**每个字段**的数据，并提供您定义的 Pydantic 模型。

## 查看文档

您可以在文档 UI 的 `/docs` 中查看定义的 cookie：

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// info

请记住，由于**浏览器**以特殊方式**处理 cookie**，并在后台进行操作，因此它们**不会**轻易允许 **JavaScript** 访问这些 cookie。

如果您访问 `/docs` 的 **API 文档 UI**，您将能够查看您*路径操作*的 cookie **文档**。

但是即使您**填写数据**并点击“执行”，由于文档界面使用 **JavaScript**，cookie 将不会被发送。而您会看到一条**错误**消息，就好像您没有输入任何值一样。

///

## 禁止额外的 Cookie

在某些特殊使用情况下（可能并不常见），您可能希望**限制**您想要接收的 cookie。

您的 API 现在可以控制自己的 <abbr title="顺带一提，这是一个笑话。它与 cookie 同意无关，但现在连API都能拒绝那些可怜的 cookie，真是太有意思了。来，吃块小饼干（cookie）吧。🍪">cookie 同意</abbr>。🤪🍪

您可以使用 Pydantic 的模型配置来禁止（ `forbid` ）任何额外（ `extra` ）字段：

{* ../../docs_src/cookie_param_models/tutorial002_an_py39.py hl[10] *}

如果客户尝试发送一些**额外的 cookie**，他们将收到**错误**响应。

可怜的 cookie 通知条，费尽心思为了获得您的同意，却被<abbr title="这又是一个笑话，别管我了，给您的小饼干（cookie）配上点咖啡吧。☕">API 拒绝了</abbr>。🍪

例如，如果客户端尝试发送一个值为 `good-list-please` 的 `santa_tracker` cookie，客户端将收到一个**错误**响应，告知他们 `santa_tracker` <abbr title="圣诞老人（Santa）不赞成没有小饼干（cookie）。🎅 好吧，不会再开 cookie 的玩笑了。">cookie 是不允许的</abbr>：

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

## 总结

您可以使用 **Pydantic 模型**在 **FastAPI** 中声明 <abbr title="走之前再来块小饼干吧。 🍪">**cookie**</abbr>。😎
