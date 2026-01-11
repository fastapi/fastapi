# Cookie 参数 { #cookie-parameters }

你可以像定义 `Query` 和 `Path` 参数一样定义 Cookie 参数。

## 导入 `Cookie` { #import-cookie }

首先，导入 `Cookie`：

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## 声明 `Cookie` 参数 { #declare-cookie-parameters }

然后，使用与 `Path` 和 `Query` 相同的结构来声明 cookie 参数。

你可以定义默认值，以及所有额外的验证或注释参数：

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | 技术细节

`Cookie` 是 `Path` 和 `Query` 的“姊妹”类。它也继承自相同的公共 `Param` 类。

但请记住，当你从 `fastapi` 导入 `Query`、`Path`、`Cookie` 等时，它们实际上是返回特殊类的函数。

///

/// info | 信息

要声明 cookie，你需要使用 `Cookie`，否则这些参数会被解释为查询参数。

///

/// info | 信息

请记住，由于**浏览器会以特殊方式并在幕后处理 cookies**，它们并**不**容易允许 **JavaScript** 去触碰它们。

如果你在 `/docs` 的 **API docs UI** 中，你将能够看到针对你的*路径操作*的 cookies **文档**。

但即使你**填写了数据**并点击 “Execute”，因为 docs UI 使用 **JavaScript** 工作，cookies 也不会被发送，你会看到一条**错误**消息，就像你没有写任何值一样。

///

## 小结 { #recap }

使用 `Cookie` 声明 cookies，使用与 `Query` 和 `Path` 相同的通用模式。
