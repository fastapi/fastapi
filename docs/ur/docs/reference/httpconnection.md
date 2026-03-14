# `HTTPConnection` class

جب آپ ایسی dependencies define کرنا چاہیں جو HTTP اور WebSockets دونوں کے ساتھ مطابقت رکھتی ہوں، تو آپ `Request` یا `WebSocket` کی بجائے `HTTPConnection` لینے والا parameter define کر سکتے ہیں۔

آپ اسے `fastapi.requests` سے import کر سکتے ہیں:

```python
from fastapi.requests import HTTPConnection
```

::: fastapi.requests.HTTPConnection
