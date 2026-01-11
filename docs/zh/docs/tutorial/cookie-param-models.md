# Cookie 参数模型 { #cookie-parameter-models }

如果你有一组相关的 **cookies**，你可以创建一个 **Pydantic 模型**来声明它们。🍪

这将允许你在**多个地方**能够**重用模型**，并且可以一次性声明所有参数的验证方式和元数据。😎

/// note | 注意

自 FastAPI 版本 `0.115.0` 起支持此功能。🤓

///

/// tip | 提示

此技术同样适用于 `Query`、`Cookie` 和 `Header`。😎

///

## 带有 Pydantic 模型的 Cookie { #cookies-with-a-pydantic-model }

在 **Pydantic** 模型中声明所需的 **cookie** 参数，然后将参数声明为 `Cookie`：

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI** 将从请求中接收到的 **cookies** 中**提取**出**每个字段**的数据，并提供你定义的 Pydantic 模型。

## 查看文档 { #check-the-docs }

你可以在文档 UI 的 `/docs` 中查看定义的 cookies：

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// info | 信息

请记住，由于**浏览器**以特殊方式**处理 cookies**，并在后台进行操作，因此它们**不会**轻易允许 **JavaScript** 访问这些 cookies。

如果你访问 `/docs` 的 **API 文档 UI**，你将能够查看你*路径操作*的 cookies **文档**。

但是即使你**填写数据**并点击“执行”，由于文档界面使用 **JavaScript**，cookies 将不会被发送，而你会看到一条**错误**消息，就好像你没有输入任何值一样。

///

## 禁止额外的 Cookie { #forbid-extra-cookies }

在某些特殊使用情况下（可能并不常见），你可能希望**限制**你想要接收的 cookies。

你的 API 现在可以控制自己的 <abbr title="This is a joke, just in case. It has nothing to do with cookie consents, but it's funny that even the API can now reject the poor cookies. Have a cookie. 🍪">cookie consent</abbr>。🤪🍪

你可以使用 Pydantic 的模型配置来 `forbid` 任何 `extra` 字段：

{* ../../docs_src/cookie_param_models/tutorial002_an_py310.py hl[10] *}

如果客户端尝试发送一些**额外的 cookies**，他们将收到**错误**响应。

可怜的 cookie 通知条，费尽心思为了获得你的同意，却被<abbr title="This is another joke. Don't pay attention to me. Have some coffee for your cookie. ☕">API to reject it</abbr>。🍪

例如，如果客户端尝试发送一个值为 `good-list-please` 的 `santa_tracker` cookie，客户端将收到一个**错误**响应，告知他们 `santa_tracker` <abbr title="Santa disapproves the lack of cookies. 🎅 Okay, no more cookie jokes.">cookie is not allowed</abbr>：

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

## 总结 { #summary }

你可以使用 **Pydantic 模型**在 **FastAPI** 中声明 <abbr title="Have a last cookie before you go. 🍪">**cookies**</abbr>。😎
