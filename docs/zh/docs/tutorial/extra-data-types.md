# 额外的数据类型

到现在，你已经使用过如下这样的通用数据类型了：

* `int`
* `float`
* `str`
* `bool`

但是你还能使用更多复杂数据类型。

并且到这里仍能拥有相同的功能：

* 强大的编辑器支持。
* 请求的数据转换。
* 响应的数据转换。
* 数据验证。
* 自动注释和文档。

## 其他数据类型

这里是一些你能使用的额外数据类型：

* `UUID`：
    * 一个标准的“通用唯一标识符”，在许多数据库和系统中通常作为ID使用。
    * 在请求和响应里会表示为 `str`。
* `datetime.datetime`：
    * Python里的`datetime.datetime`。
    * 在请求和响应里会以 ISO 8601 格式表示为`str`，就像：`2008-09-15T15:53:00+05:00`。
* `datetime.date`:
    * Python里的`datetime.date`。
    * 在请求和响应里会以 ISO 8601 格式表示为`str`，就像：`2008-09-15T`。
* `datetime.time`:
    * Python里的`datetime.time`。
    * 在请求和响应里会以 ISO 8601 格式表示为`str`，就像：`14:23:55.003`。 
* `datetime.timedelta`:
    * Python里的`datetime.timedelta`。
    * 在请求和响应中以`float`类型表示的总秒数。
    * Pydantic 也允许表示为 “ISO 8601时间差编码”, <a href="https://pydantic-docs.helpmanual.io/#json-serialisation" class="external-link" target="_blank">see the docs for more info</a>.
* `frozenset`:
    * 在请求和响应中，与`set`一样对待。
        * 在请求里，将读取列表，去重并转换为`set`。
        * 在响应里，`set`会被转化为`list`。
        * 生成的模式会指定`set`值是唯一的（使用JSON Schema的`uniqueItems`）。
* `bytes`:
    * 标准的Python`bytes`。
    * 在请求和响应里会以`str`对待。
    * 生成的模式会用指定这是一个`str`格式的`binary`。
* `Decimal`:
    * 标准的Python`Decimal`。
    * 在请求和响应里，用`float`一样的方式处理
* 你可以在这检查所有有效的 pydantic 数据类型：<a href="https://pydantic-docs.helpmanual.io/usage/types" class="external-link" target="_blank">Pydantic data types</a>。 

## Example

这里是个用某些上述类型作为参数的*路径操作*示例。

```Python hl_lines="1  3  12-16"
{!../../../docs_src/extra_data_types/tutorial001.py!}
```

注意函数内的参数有它们自然数据类型，并且你也能执行正常的日期操作，就像：

```Python hl_lines="18-19"
{!../../../docs_src/extra_data_types/tutorial001.py!}
```
