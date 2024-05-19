# 异常处理 - `HTTPException` and `WebSocketException`

这些异常可以用来向客户端显示错误。

当您引发异常时，就像在普通 Python 中一样，其余的执行将被中止。这样，您就可以在代码的任何地方引发这些异常，以终止请求并向客户端显示错误。

您可以使用：

* `HTTPException`
* `WebSocketException`

可以直接从 `fastapi` 中导入这些异常：

```python
from fastapi import HTTPException, WebSocketException
```

::: fastapi.HTTPException

::: fastapi.WebSocketException
