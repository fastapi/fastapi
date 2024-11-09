# Background Tasks - `BackgroundTasks`

You can declare a parameter in a *path operation function* or dependency function with the type `BackgroundTasks`, and then you can use it to schedule the execution of background tasks after the response is sent.

You can import it directly from `fastapi`:

```python
from fastapi import BackgroundTasks
```

::: fastapi.BackgroundTasks
