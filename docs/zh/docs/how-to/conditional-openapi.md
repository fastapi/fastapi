# 按条件配置 OpenAPI { #conditional-openapi }

如果需要，你可以使用设置和环境变量，按环境有条件地配置 OpenAPI，甚至完全禁用它。

## 关于安全、API 和文档 { #about-security-apis-and-docs }

在生产环境隐藏文档界面并不应该成为保护 API 的方式。

这并不会给你的 API 增加任何额外的安全性，*路径操作* 仍然会在原来的位置可用。

如果你的代码里有安全漏洞，它仍然存在。

隐藏文档只会让理解如何与 API 交互变得更困难，也可能让你在生产环境中调试更困难。这大体上可以被视为一种 <a href="https://en.wikipedia.org/wiki/Security_through_obscurity" class="external-link" target="_blank">通过隐藏实现安全</a> 的做法。

如果你想保护你的 API，有很多更好的措施，例如：

- 确保为请求体和响应定义完善的 Pydantic 模型。
- 使用依赖配置所需的权限和角色。
- 绝不要存储明文密码，只存储密码哈希。
- 实现并使用成熟的密码学工具，比如 pwdlib 和 JWT 令牌等。
- 在需要的地方使用 OAuth2 作用域添加更细粒度的权限控制。
- ...等。

尽管如此，你可能确实有非常特定的用例，需要在某些环境（例如生产环境）禁用 API 文档，或根据环境变量的配置来决定。

## 基于设置和环境变量的条件式 OpenAPI { #conditional-openapi-from-settings-and-env-vars }

你可以很容易地使用相同的 Pydantic 设置来配置生成的 OpenAPI 和文档 UI。

例如：

{* ../../docs_src/conditional_openapi/tutorial001_py310.py hl[6,11] *}

这里我们声明了设置项 `openapi_url`，其默认值同样是 `"/openapi.json"`。

然后在创建 `FastAPI` 应用时使用它。

接着，你可以通过把环境变量 `OPENAPI_URL` 设为空字符串来禁用 OpenAPI（包括文档 UI），例如：

<div class="termy">

```console
$ OPENAPI_URL= uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

然后如果你访问 `/openapi.json`、`/docs` 或 `/redoc`，就会得到一个 `404 Not Found` 错误，例如：

```JSON
{
    "detail": "Not Found"
}
```
