# 更多数据类型

至此，我们使用的都是常见数据类型，如：

* `int`
* `float`
* `str`
* `bool`

但其实也可以使用更复杂的数据类型。

而且，拥有同样强悍的功能：

* 强大的编辑器支持
* 转换请求数据
* 转换响应数据
* 数据校验
* 自动补全和自动文档

## 其他数据类型

下面介绍更多数据类型：

* `UUID`：
    * 标准的「通用唯一标识符」，在数据库和系统中常用作 ID
    * 在请求和响应中为 `str`
* `datetime.datetime`：
    *  Python `datetime.datetime`
    * 在请求和响应中为 ISO 8601 格式的 `str`，例如：`2008-09-15T15:53:00+05:00`
* `datetime.date`：
    * Python `datetime.date`
    * 在请求和响应中为 ISO 8601 格式的 `str`，例如：`2008-09-15`
* `datetime.time`：
    * Python `datetime.time`
    * 在请求和响应中为 ISO 8601 格式的 `str`，例如：`14:23:55.003`
* `datetime.timedelta`：
    * Python `datetime.timedelta`
    * 在请求和响应中为 `float`，表示总秒数
    * Pydantic 还支持「ISO 8601 时间差异编码」, <a href="https://pydantic-docs.helpmanual.io/#json-serialisation" class="external-link" target="_blank">详见文档</a>
* `frozenset`：
    * 在请求和响应中与 `set` 相同：
        * 在请求中，读取列表，去除重复项，并转换为 `set`
        * 在响应中， 把 `set` 转换为 `list`
        * 生成的概图（使用 JSON Schema 的 `uniqueItems`）指明 `set` 中的值是唯一的 
* `bytes`：
    * 标准的 Python `bytes`
    * 在请求和响应中为 `str`
    * 生成的概图指明该 `str` 是 `binary`「格式」
* `Decimal`：
    * 标准的 Python `Decimal`
    * 在请求和响应中作为 `float` 处理
*  <a href="https://pydantic-docs.helpmanual.io/usage/types" class="external-link" target="_blank">Pydantic 数据类型</a>中介绍了所有 Pydantic 数据类型

## 示例

下例展示了如何在*路径操作*中使用上述类型作为参数。

```Python hl_lines="1  3  12-16"
{!../../../docs_src/extra_data_types/tutorial001.py!}
```

注意，函数的参数依然支持原生数据类型，例如，可以使用以下方式执行常规的日期操作：

```Python hl_lines="18-19"
{!../../../docs_src/extra_data_types/tutorial001.py!}
```

