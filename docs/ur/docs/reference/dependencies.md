# Dependencies - `Depends()` اور `Security()`

## `Depends()`

Dependencies کو بنیادی طور پر خاص function `Depends()` کے ذریعے سنبھالا جاتا ہے جو ایک callable لیتا ہے۔

یہاں اس کی اور اس کے parameters کی حوالہ جاتی معلومات ہیں۔

آپ اسے براہ راست `fastapi` سے import کر سکتے ہیں:

```python
from fastapi import Depends
```

::: fastapi.Depends

## `Security()`

بہت سے منظرناموں میں، آپ `Depends()` استعمال کر کے dependencies کے ذریعے security (authorization، authentication، وغیرہ) کو سنبھال سکتے ہیں۔

لیکن جب آپ OAuth2 scopes بھی declare کرنا چاہیں، تو آپ `Depends()` کی بجائے `Security()` استعمال کر سکتے ہیں۔

آپ `Security()` کو براہ راست `fastapi` سے import کر سکتے ہیں:

```python
from fastapi import Security
```

::: fastapi.Security
