# 测试客户端 - `TestClient` 类

您可以使用 `TestClient` 类测试 FastAPI 应用程序，而无需创建实际的 HTTP 和套接字连接，只需直接与 FastAPI 代码通信即可。

请参阅 [FastAPI docs for Testing](https://fastapi.tiangolo.com/tutorial/testing/)，了解更多相关信息。

您可以直接从 `fastapi.testclient` 中导入该类：

```python
from fastapi.testclient import TestClient
```

::: fastapi.testclient.TestClient
