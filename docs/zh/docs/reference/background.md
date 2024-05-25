# 后台任务 - `BackgroundTasks`

您可以在 *路径操作函数* 或依赖函数中声明一个类型为`BackgroundTasks`的参数，然后在发送响应后使用它来安排后台任务的执行。

您可以直接从 `fastapi` 中导入：

```python
from fastapi import BackgroundTasks
```

::: fastapi.BackgroundTasks
