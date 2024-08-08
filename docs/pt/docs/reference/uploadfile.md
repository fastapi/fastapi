# Classe `UploadFile`

Você pode definir parâmetros na função de operação de rota do tipo `UploadFile` para receber arquivos da requisição.

Você pode importá-la diretamente de `fastapi`:

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
