# 响应Cookies

## 使用 `Response` 参数

你可以在 *路径函数* 中定义一个类型为 `Response`的参数，这样你就可以在这个临时响应对象中设置cookie了。

```Python hl_lines="1  8-9"
{!../../../docs_src/response_cookies/tutorial002.py!}
```

而且你还可以根据你的需要响应不同的对象，比如常用的 `dict`，数据库model等。

如果你定义了 `response_model`，程序会自动根据`response_model`来过滤和转换你响应的对象。

**FastAPI** 会使用这个 *临时* 响应对象去装在这些cookies信息 (同样还有headers和状态码等信息), 最终会将这些信息和通过`response_model`转化过的数据合并到最终的响应里。

你也可以在depend中定义`Response`参数，并设置cookie和header。

## 直接响应 `Response`

你还可以在直接响应`Response`时直接创建cookies。

你可以参考[Return a Response Directly](response-directly.md){.internal-link target=_blank}来创建response

然后设置Cookies，并返回：

```Python hl_lines="10-12"
{!../../../docs_src/response_cookies/tutorial001.py!}
```

!!! tip
    需要注意，如果你直接反馈一个response对象，而不是使用`Response`入参，FastAPI则会直接反馈你封装的response对象。

    所以你需要确保你响应数据类型的正确性，如：你可以使用`JSONResponse`来兼容JSON的场景。

    同时，你也应当仅反馈通过`response_model`过滤过的数据。

### 更多信息

!!! note "技术细节"
    你也可以使用`from starlette.responses import Response` 或者 `from starlette.responses import JSONResponse`。

    为了方便开发者，**FastAPI** 封装了相同数据类型，如`starlette.responses` 和 `fastapi.responses`。不过大部分response对象都是直接引用自Starlette。

    因为`Response`对象可以非常便捷的设置headers和cookies，所以 **FastAPI** 同时也封装了`fastapi.Response`。

如果你想查看所有可用的参数和选项，可以参考 <a href="https://www.starlette.io/responses/#set-cookie" class="external-link" target="_blank">Starlette帮助文档</a>
