# Background Tasks - `BackgroundTasks`

آپ *path operation function* یا dependency function میں `BackgroundTasks` type کا parameter declare کر سکتے ہیں، اور پھر اسے response بھیجنے کے بعد background tasks کے عمل کو schedule کرنے کے لیے استعمال کر سکتے ہیں۔

آپ اسے براہ راست `fastapi` سے import کر سکتے ہیں:

```python
from fastapi import BackgroundTasks
```

::: fastapi.BackgroundTasks
