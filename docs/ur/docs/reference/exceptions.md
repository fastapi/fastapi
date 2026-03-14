# Exceptions - `HTTPException` اور `WebSocketException`

یہ وہ exceptions ہیں جو آپ client کو غلطیاں دکھانے کے لیے raise کر سکتے ہیں۔

جب آپ کوئی exception raise کرتے ہیں، جیسا کہ عام Python میں ہوتا ہے، باقی کا عمل روک دیا جاتا ہے۔ اس طرح آپ code میں کہیں سے بھی یہ exceptions raise کر کے request کو روک سکتے ہیں اور client کو غلطی دکھا سکتے ہیں۔

آپ یہ استعمال کر سکتے ہیں:

* `HTTPException`
* `WebSocketException`

یہ exceptions براہ راست `fastapi` سے import کی جا سکتی ہیں:

```python
from fastapi import HTTPException, WebSocketException
```

::: fastapi.HTTPException

::: fastapi.WebSocketException
