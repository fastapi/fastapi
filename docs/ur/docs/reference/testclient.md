# Test Client - `TestClient`

آپ `TestClient` class کو FastAPI applications کی جانچ کرنے کے لیے استعمال کر سکتے ہیں بغیر کوئی حقیقی HTTP اور socket connection بنائے، بس FastAPI code کے ساتھ براہ راست بات چیت کر کے۔

اس کے بارے میں مزید پڑھیں [FastAPI دستاویزات میں Testing](https://fastapi.tiangolo.com/tutorial/testing/)۔

آپ اسے براہ راست `fastapi.testclient` سے import کر سکتے ہیں:

```python
from fastapi.testclient import TestClient
```

::: fastapi.testclient.TestClient
