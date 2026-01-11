# 直接返回响应 { #return-a-response-directly }

当你创建一个 **FastAPI** *路径操作* 时，你通常可以从中返回任意数据：`dict`、`list`、Pydantic 模型、数据库模型等。

默认情况下，**FastAPI** 会使用 [JSON 兼容编码器](../tutorial/encoder.md){.internal-link target=_blank} 中介绍的 `jsonable_encoder` 自动将该返回值转换为 JSON。

然后，它会在后台把这些兼容 JSON 的数据（例如 `dict`）放入一个 `JSONResponse` 中，用于将响应发送给客户端。

但你也可以直接从你的 *路径操作* 返回一个 `JSONResponse`。

例如，这在返回自定义 headers 或 cookies 时可能会很有用。

## 返回 `Response` { #return-a-response }

事实上，你可以返回任意 `Response` 或者它的任意子类。

/// tip | 提示

`JSONResponse` 本身是 `Response` 的子类。

///

当你返回一个 `Response` 时，**FastAPI** 会直接传递它。

它不会使用 Pydantic 模型进行任何数据转换，也不会把内容转换成任何类型等。

这给了你很大的灵活性。你可以返回任何数据类型、覆盖任何数据声明或校验等。

## 在 `Response` 中使用 `jsonable_encoder` { #using-the-jsonable-encoder-in-a-response }

因为 **FastAPI** 不会对你返回的 `Response` 做任何修改，你必须确保它的内容已经准备好。

例如，如果不先将 Pydantic 模型转换为 `dict`，并把所有数据类型（如 `datetime`、`UUID` 等）转换为兼容 JSON 的类型，你就不能将其放入 `JSONResponse` 中。

对于这些情况，你可以在把数据传给响应之前，使用 `jsonable_encoder` 来转换你的数据：

{* ../../docs_src/response_directly/tutorial001_py310.py hl[5:6,20:21] *}

/// note | 注意 | 技术细节

你也可以使用 `from starlette.responses import JSONResponse`。

**FastAPI** 提供与 `starlette.responses` 相同的 `fastapi.responses` 只是为了方便你（开发者）。但大多数可用的响应都直接来自 Starlette。

///

## 返回自定义 `Response` { #returning-a-custom-response }

上面的例子展示了你需要的所有部分，但它还不是很有用，因为你本可以直接返回 `item`，而 **FastAPI** 会默认帮你把它放进 `JSONResponse` 中，将其转换为 `dict` 等。默认情况下这些都会自动完成。

现在，让我们看看你如何用它来返回自定义响应。

假设你想要返回一个 <a href="https://en.wikipedia.org/wiki/XML" class="external-link" target="_blank">XML</a> 响应。

你可以把 XML 内容放到一个字符串中，把它放入 `Response`，然后返回：

{* ../../docs_src/response_directly/tutorial002_py39.py hl[1,18] *}

## 说明 { #notes }

当你直接返回 `Response` 时，它的数据不会被校验、转换（序列化），也不会自动生成文档。

但是你仍然可以按照 [OpenAPI 中的额外响应](additional-responses.md){.internal-link target=_blank} 中所述为它编写文档。

你可以在后续章节中看到如何在仍然保留自动数据转换、文档等功能的同时，使用/声明这些自定义 `Response`。
