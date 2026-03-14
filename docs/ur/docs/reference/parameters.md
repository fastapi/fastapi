# Request Parameters

یہاں request parameters کی حوالہ جاتی معلومات ہیں۔

یہ وہ خاص functions ہیں جو آپ *path operation function* کے parameters یا dependency functions میں `Annotated` کے ساتھ استعمال کر کے request سے ڈیٹا حاصل کر سکتے ہیں۔

اس میں شامل ہیں:

* `Query()`
* `Path()`
* `Body()`
* `Cookie()`
* `Header()`
* `Form()`
* `File()`

آپ ان سب کو براہ راست `fastapi` سے import کر سکتے ہیں:

```python
from fastapi import Body, Cookie, File, Form, Header, Path, Query
```

::: fastapi.Query

::: fastapi.Path

::: fastapi.Body

::: fastapi.Cookie

::: fastapi.Header

::: fastapi.Form

::: fastapi.File
