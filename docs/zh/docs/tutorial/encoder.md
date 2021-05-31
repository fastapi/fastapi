# JSON 编码器

有时，我们需要把 Pydantic 模型等数据类型转换为 `dict`、`list` 等与 JSON 兼容的格式。

例如， 把 Pydantic 模型存入数据库时就需要进行转换。

为此， **FastAPI** 提供了 `jsonable_encoder()` 函数。

## 使用 `jsonable_encoder`

假设数据库 `fake_db` 只接收与 JSON 兼容的数据。

该数据库不能接收与 JSON 不兼容的 `datetime` 对象。

因此，必须把 `datetime` 对象转换为包含 <a href="https://en.wikipedia.org/wiki/ISO_8601" class="external-link" target="_blank">ISO 格式</a>数据的 `str`。

同理，该数据库也不能接收 Pydantic 模型（带属性的对象），只能接收 `dict`。

如需接收 Pydantic 模型，就要使用 `jsonable_encoder`。

`jsonable_encoder` 函数接收 Pydantic 模型等对象，返回的是兼容 JSON 的数据：

```Python hl_lines="5  22"
{!../../../docs_src/encoder/tutorial001.py!}
```

本例把 Pydantic 模型转换为 `dict`，并把 `datetime` 转换为  `str`。

该函数的输出结果可以用 Python <a href="https://docs.python.org/3/library/json.html#json.dumps" class="external-link" target="_blank">`json.dumps()`</a> 编码。

`jsonable_encoder` 函数返回的不是包含 JSON 格式数据的长字符串（ `str`），而是返回值与子值都兼容 JSON 的 Python 标准数据结构，如  `dict`。

!!! note "笔记"

实际上，`jsonable_encoder` 用于在 **FastAPI** 内部转换数据，但在其它场景下也可以使用。