# `Request` class

آپ *path operation function* یا dependency میں `Request` type کا parameter declare کر سکتے ہیں اور پھر بغیر کسی validation وغیرہ کے خام request object تک براہ راست رسائی حاصل کر سکتے ہیں۔

اس کے بارے میں مزید پڑھیں [FastAPI دستاویزات میں Request کو براہ راست استعمال کرنا](https://fastapi.tiangolo.com/advanced/using-request-directly/)

آپ اسے براہ راست `fastapi` سے import کر سکتے ہیں:

```python
from fastapi import Request
```

/// tip | مشورہ

جب آپ ایسی dependencies define کرنا چاہیں جو HTTP اور WebSockets دونوں کے ساتھ مطابقت رکھتی ہوں، تو آپ `Request` یا `WebSocket` کی بجائے `HTTPConnection` لینے والا parameter define کر سکتے ہیں۔

///

::: fastapi.Request
