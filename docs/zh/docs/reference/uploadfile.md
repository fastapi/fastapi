# `UploadFile` 类

您可以定义 *path operation function* 参数为 `UploadFile` 类型，以便从请求中接收文件。

你可以直接从 `fastapi` 中导入：

```python
from fastapi import UploadFile
```

::: fastapi.UploadFile
    options:
        members:
            - file
            - filename
            - size
            - headers
            - content_type
            - read
            - write
            - seek
            - close
