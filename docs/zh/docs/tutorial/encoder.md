# JSON 兼容编码器 { #json-compatible-encoder }

在某些情况下，你可能需要将数据类型（如 Pydantic model）转换为与 JSON 兼容的类型（如 `dict`、`list` 等）。

例如，如果你需要将其存储在数据库中。

为此，**FastAPI** 提供了 `jsonable_encoder()` 函数。

## 使用 `jsonable_encoder` { #using-the-jsonable-encoder }

让我们假设你有一个名为 `fake_db` 的数据库，它只接收与 JSON 兼容的数据。

例如，它不接收 `datetime` 对象，因为这些对象与 JSON 不兼容。

因此，`datetime` 对象必须被转换为一个 `str`，其中包含 <a href="https://en.wikipedia.org/wiki/ISO_8601" class="external-link" target="_blank">ISO format</a> 的数据。

同样，这个数据库也不会接收 Pydantic model（带属性的对象），只接收 `dict`。

对此你可以使用 `jsonable_encoder`。

它接收一个对象，比如 Pydantic model，并返回一个与 JSON 兼容的版本：

{* ../../docs_src/encoder/tutorial001_py310.py hl[4,21] *}

在这个例子中，它会将 Pydantic model 转换为 `dict`，并将 `datetime` 转换为 `str`。

调用它的结果是可以用 Python 标准库的 <a href="https://docs.python.org/3/library/json.html#json.dumps" class="external-link" target="_blank">`json.dumps()`</a> 编码的内容。

它不会返回一个包含 JSON 格式数据（以字符串形式）的巨大 `str`。它会返回一个 Python 标准数据结构（例如 `dict`），其中的值和子值都与 JSON 兼容。

/// note | 注意

`jsonable_encoder` 实际上是 **FastAPI** 在内部用来转换数据的。但它在许多其他场景中也很有用。

///
