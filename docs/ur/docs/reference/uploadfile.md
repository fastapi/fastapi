# `UploadFile` class

آپ *path operation function* کے parameters کو `UploadFile` type کا define کر سکتے ہیں تاکہ request سے files وصول کی جا سکیں۔

آپ اسے براہ راست `fastapi` سے import کر سکتے ہیں:

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
