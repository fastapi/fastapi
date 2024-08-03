# Testclient – `TestClient`

Sie können die `TestClient`-Klasse verwenden, um FastAPI-Anwendungen zu testen, ohne eine tatsächliche HTTP- und Socket-Verbindung zu erstellen, Sie kommunizieren einfach direkt mit dem FastAPI-Code.

Lesen Sie mehr darüber in der [FastAPI-Dokumentation über Testen](../tutorial/testing.md).

Sie können sie direkt von `fastapi.testclient` importieren:

```python
from fastapi.testclient import TestClient
```

::: fastapi.testclient.TestClient
