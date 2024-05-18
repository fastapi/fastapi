# 请求参数

这里是请求参数的参考信息。

这些是特殊函数，你可以把它们放在 *path 操作函数 * 参数或带有`注释`的依赖函数中，以便从请求中获取数据。

其中包括：

* `Query()`
* `Path()`
* `Body()`
* `Cookie()`
* `Header()`
* `Form()`
* `File()`

您可以直接从 `fastapi` 中导入它们：

```python
from fastapi import Body, Cookie, File, Form, Header, Path, Query
```

::: fastapi.Query

::: fastapi.Path

::: fastapi.Body

::: fastapi.Cookie

::: fastapi.Header

::: fastapi.Form

::: fastapi.File
