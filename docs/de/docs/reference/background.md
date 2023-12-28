# Hintergrundtasks – `BackgroundTasks`

Sie können einen Parameter in einer *Pfadoperation-Funktion* oder einer Abhängigkeitsfunktion mit dem Typ `BackgroundTasks` deklarieren und diesen danach verwenden, um die Ausführung von Hintergrundtasks nach dem Senden der Response zu definieren.

Sie können `BackgroundTasks` direkt von `fastapi` importieren:

```python
from fastapi import BackgroundTasks
```

::: fastapi.BackgroundTasks
