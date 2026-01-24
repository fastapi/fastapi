# 额外数据类型 { #extra-data-types }

到目前为止，你一直在使用常见的数据类型，例如：

* `int`
* `float`
* `str`
* `bool`

但你也可以使用更复杂的数据类型。

并且你仍然会拥有到目前为止所看到的相同特性：

* 很棒的编辑器支持。
* 传入请求的数据转换。
* 响应数据转换。
* 数据验证。
* 自动注解和文档。

## 其他数据类型 { #other-data-types }

下面是一些你可以使用的额外数据类型：

* `UUID`:
    * 一种标准的“通用唯一标识符”（Universally Unique Identifier），在许多数据库和系统中常用作 ID。
    * 在请求和响应中将以 `str` 表示。
* `datetime.datetime`:
    * 一个 Python `datetime.datetime`。
    * 在请求和响应中将表示为 ISO 8601 格式的 `str`，比如：`2008-09-15T15:53:00+05:00`。
* `datetime.date`:
    * Python `datetime.date`。
    * 在请求和响应中将表示为 ISO 8601 格式的 `str`，比如：`2008-09-15`。
* `datetime.time`:
    * 一个 Python `datetime.time`。
    * 在请求和响应中将表示为 ISO 8601 格式的 `str`，比如：`14:23:55.003`。
* `datetime.timedelta`:
    * 一个 Python `datetime.timedelta`。
    * 在请求和响应中将表示为总秒数的 `float`。
    * Pydantic 也允许将其表示为 “ISO 8601 time diff encoding”，<a href="https://docs.pydantic.dev/latest/concepts/serialization/#custom-serializers" class="external-link" target="_blank">查看文档了解更多信息</a>。
* `frozenset`:
    * 在请求和响应中，与 `set` 的处理方式相同：
        * 在请求中，将读取一个 list，消除重复并将其转换为 `set`。
        * 在响应中，`set` 将被转换为 `list`。
        * 生成的 schema 会指定这些 `set` 的值是唯一的（使用 JSON Schema 的 `uniqueItems`）。
* `bytes`:
    * 标准 Python `bytes`。
    * 在请求和响应中将被当作 `str` 处理。
    * 生成的 schema 将指定它是一个带有 `binary` “format”的 `str`。
* `Decimal`:
    * 标准 Python `Decimal`。
    * 在请求和响应中，处理方式与 `float` 相同。
* 你可以在这里查看所有有效的 Pydantic 数据类型：<a href="https://docs.pydantic.dev/latest/usage/types/types/" class="external-link" target="_blank">Pydantic data types</a>。

## 示例 { #example }

下面是一个使用了上述一些类型作为参数的 *路径操作* 示例。

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[1,3,12:16] *}

注意，函数内的参数具有其自然的数据类型，例如，你可以执行正常的日期操作，比如：

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[18:19] *}
