# Statuscodes

Sie können das Modul `status` von `fastapi` importieren:

```python
from fastapi import status
```

`status` wird direkt von Starlette bereitgestellt.

Es enthält eine Gruppe benannter Konstanten (Variablen) mit ganzzahligen Statuscodes.

Zum Beispiel:

* 200: `status.HTTP_200_OK`
* 403: `status.HTTP_403_FORBIDDEN`
* usw.

Es kann praktisch sein, schnell auf HTTP- (und WebSocket-)Statuscodes in Ihrer Anwendung zuzugreifen, indem Sie die automatische Vervollständigung für den Namen verwenden, ohne sich die Zahlen für die Statuscodes merken zu müssen.

Lesen Sie mehr darüber in der [FastAPI-Dokumentation zu Response-Statuscodes](../tutorial/response-status-code.md).

## Beispiel

```python
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/items/", status_code=status.HTTP_418_IM_A_TEAPOT)
def read_items():
    return [{"name": "Plumbus"}, {"name": "Portal Gun"}]
```

::: fastapi.status
