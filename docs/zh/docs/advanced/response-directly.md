# 直接返回一个响应 

When you create a **FastAPI** *path operation* you can normally return any data from it: a `dict`, a `list`, a Pydantic model, a database model, etc.
当你创建一个 **FastAPI** *路径操作* 时，通常可以返回以下任意类型：`dict`，`list`，Pydantic 模型，数据库模型等等

默认情况下，**FastAPI** 会自动用`jsonable_encoder`（详情见[JSON Compatible Encoder](../tutorial/encoder.md){.internal-link target=_blank}.）将返回值转换为 JSON。

然后，它会在后台把 JSON 兼容的数据（比如 `dict`）放到`JSONResponse`里向客户端发送响应。

不过你可以直接从 *路径操作* 里返回`JSONResponse`。

这可能很有用，比如说返回自定义的请求头部或者 cookies。

## 返回 `Response`

实际上，你可以返回任意 `Response` 或者它的任意子类。

!!! tip
    `JSONResponse` 本身是一个 `Response` 的子类。

当你返回`Response`时，**FastAPI** 会直接继续传递。

它不会用 Pydantic 模型进行任何数据转换，也不会将内容转换为其他类型等等。

这给了你很大的灵活性，你可以返回任何数据类型，覆盖任何数据声明或验证等。

## 在`Response`中使用`jsonable_encoder`

因为 **FastAPI** 不会对你返回的`Response`做任何改动，所以你必须保证内容已经就绪。

例如，你不能将 Pydantic 模型放在 JSONResponse 中，除非先把所有数据类型（例如 datetime，UUID 等）都转换为 JSON 兼容类型的`dict`。

对于这些情况，可以在将数据传递到响应之前使用`jsonable_encoder`进行转换：


```Python hl_lines="6 7  21 22"
{!../../../docs_src/response_directly/tutorial001.py!}
```

!!! note "技术细节"
	你也能这么写 `from starlette.responses import JSONResponse`。

    **FastAPI** 提供了和 `starlette.responses` 一样的 `fastapi.responses`，主要是为了方便开发者。不过大多数的可用响应类型都是直接从 Starlette 里来的。

## 返回自定义 `Response`

上面这个例子展示了需要的所有部分，但它其实没什么用，因为你可以直接返回`item`，然后 **FastAPI** 会放到`JSONResponse`里，转换成`dict`之类的。这些都是默认的。

现在我们看一下，怎么用它来返回自定义响应。

我们假设你需要返回一个 <a href="https://en.wikipedia.org/wiki/XML" class="external-link" target="_blank">XML</a> 响应。

You could put your XML content in a string, put it in a `Response`, and return it:
你需要把 XML 内容转换成字符串放到 `Response` 里，然后返回：

```Python hl_lines="1  18"
{!../../../docs_src/response_directly/tutorial002.py!}
```

## Notes

当你直接返回`Response`时，数据不会被校验、转换（序列化），也不会自动生成文档。

不过你仍可以通过这里描述的方法写文档：[Additional Responses in OpenAPI](additional-responses.md){.internal-link target=_blank}.

你会在后面的章节里看到怎么使用/定义这些自定义`Response`，同时仍具有数据自动转换，自动生成文档等功能。
