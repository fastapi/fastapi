# `UploadFile`-Klasse

Sie können *Pfadoperation-Funktionsparameter* als Parameter vom Typ `UploadFile` definieren, um Dateien aus dem Request zu erhalten.

Sie können es direkt von `fastapi` importieren:

```python
from fastapi import UploadFile
```

::: fastapi.UploadFile
    options:
        members:
            - file
            - filename
            - size
            - headers
            - content_type
            - read
            - write
            - seek
            - close
