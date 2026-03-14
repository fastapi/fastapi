# `Response` class

آپ *path operation function* یا dependency میں `Response` type کا parameter declare کر سکتے ہیں اور پھر response کے لیے ڈیٹا جیسے headers یا cookies سیٹ کر سکتے ہیں۔

آپ اسے براہ راست ایک instance بنانے اور اپنی *path operations* سے واپس کرنے کے لیے بھی استعمال کر سکتے ہیں۔

اس کے بارے میں مزید پڑھیں [FastAPI دستاویزات میں حسب ضرورت Response واپس کرنا](https://fastapi.tiangolo.com/advanced/response-directly/#returning-a-custom-response)

آپ اسے براہ راست `fastapi` سے import کر سکتے ہیں:

```python
from fastapi import Response
```

::: fastapi.Response
