# JSON 兼容编码器

在某些情况下，您可能需要将数据类型(如 Pydantic 模型)转换为与 JSON 兼容的数据类型(如 `dict`, `list` 等)。

例如，如果需要将其存储在数据库中。

为此， **FastAPI** 提供了一个 `jsonable_encoder()` 函数。

## 使用 `jsonable_encoder`

假设您有一个数据库 `fake_db` ”，它只接收与 JSON 兼容的数据。

例如，它不接收 `datetime` 对象，因为这些对象与 JSON 不兼容。

因此，一个 `datetime` 对象必须转换为一个 `str` ，其中包含 <a href="https://en.wikipedia.org/wiki/ISO_8601" class="external-link" target="_blank">ISO 格式</a>的数据。

这样，这个数据库不会接收一个 Pydantic 模型(一个具有属性的对象)，而只接收一个 `dict` 。

你可以使用 `jsonable_encoder` 来实现。

它接收一个对象，像一个Pydantic模型，并返回一个 JSON 兼容的版本:

```Python hl_lines="5  22"
{!../../../docs_src/encoder/tutorial001.py!}
```

在本例中，它将把 Pydantic 模型转换为 `dict`，将 `datetime` 转换为  `str`.

调用它的结果可以用 Python 标准 <a href="https://docs.python.org/3/library/json.html#json.dumps" class="external-link" target="_blank">`json.dumps()`</a> 进行编码。

它并不会返回一个包含 JSON 格式数据的大型 `str` (为一个字符串). 它返回一个 Pytho n标准数据结构 (如 一个 `dict`) 其中的值和子值都与 JSON 兼容。

!!! note
    `jsonable_encoder` 实际上由 **FastAPI** 在内部使用来转换数据。但它在许多其他情况下也很有用。
