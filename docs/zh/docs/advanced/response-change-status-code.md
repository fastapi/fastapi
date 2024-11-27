# 响应 - 更改状态码

你可能之前已经了解到，你可以设置默认的[响应状态码](../tutorial/response-status-code.md){.internal-link target=_blank}。

但在某些情况下，你需要返回一个不同于默认值的状态码。

## 使用场景

例如，假设你想默认返回一个HTTP状态码为“OK”`200`。

但如果数据不存在，你想创建它，并返回一个HTTP状态码为“CREATED”`201`。

但你仍然希望能够使用`response_model`过滤和转换你返回的数据。

对于这些情况，你可以使用一个`Response`参数。

## 使用 `Response` 参数

你可以在你的*路径操作函数*中声明一个`Response`类型的参数（就像你可以为cookies和头部做的那样）。

然后你可以在这个*临时*响应对象中设置`status_code`。

{* ../../docs_src/response_change_status_code/tutorial001.py hl[1,9,12] *}

然后你可以像平常一样返回任何你需要的对象（例如一个`dict`或者一个数据库模型）。如果你声明了一个`response_model`，它仍然会被用来过滤和转换你返回的对象。

**FastAPI**将使用这个临时响应来提取状态码（也包括cookies和头部），并将它们放入包含你返回的值的最终响应中，该响应由任何`response_model`过滤。

你也可以在依赖项中声明`Response`参数，并在其中设置状态码。但请注意，最后设置的状态码将会生效。
