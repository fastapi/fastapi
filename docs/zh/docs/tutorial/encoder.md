# JSON 兼容编码器

在某些情况下，您可能需要将数据类型（如Pydantic模型）转换为与JSON兼容的数据类型（如`dict`、`list`等）。

比如，如果您需要将其存储在数据库中。

对于这种要求， **FastAPI**提供了`jsonable_encoder()`函数。

## 使用`jsonable_encoder`

让我们假设你有一个数据库名为`fake_db`，它只能接收与JSON兼容的数据。

例如，它不接收`datetime`这类的对象，因为这些对象与JSON不兼容。

因此，`datetime`对象必须将转换为包含<a href="https://en.wikipedia.org/wiki/ISO_8601" class="external-link" target="_blank">ISO格式化</a>的`str`类型对象。

同样，这个数据库也不会接收Pydantic模型（带有属性的对象），而只接收`dict`。

对此你可以使用`jsonable_encoder`。

它接收一个对象，比如Pydantic模型，并会返回一个JSON兼容的版本：

{* ../../docs_src/encoder/tutorial001_py310.py hl[4,21] *}

在这个例子中，它将Pydantic模型转换为`dict`，并将`datetime`转换为`str`。

调用它的结果后就可以使用Python标准编码中的<a href="https://docs.python.org/3/library/json.html#json.dumps" class="external-link" target="_blank">`json.dumps()`</a>。

这个操作不会返回一个包含JSON格式（作为字符串）数据的庞大的`str`。它将返回一个Python标准数据结构（例如`dict`），其值和子值都与JSON兼容。

/// note

`jsonable_encoder`实际上是FastAPI内部用来转换数据的。但是它在许多其他场景中也很有用。

///
