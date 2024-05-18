# 状态码

你可以直接从 `fastapi` 中导入 `status`:

```python
from fastapi import status
```

`status` 由 Starlette 直接提供。

它包含一组带有整数状态代码的命名常量（变量）。

例如：

* 200: `status.HTTP_200_OK`
* 403: `status.HTTP_403_FORBIDDEN`
* etc.

在应用程序中使用名称自动完成功能快速访问 HTTP（和 WebSocket）状态代码非常方便，无需记忆整数状态代码。

请参阅 [FastAPI docs about Response Status Code](https://fastapi.tiangolo.com/zh/tutorial/response-status-code/).

## 示例

```python
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/items/", status_code=status.HTTP_418_IM_A_TEAPOT)
def read_items():
    return [{"name": "Plumbus"}, {"name": "Portal Gun"}]
```

::: fastapi.status
