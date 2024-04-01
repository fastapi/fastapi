# Exceptions – `HTTPException` und `WebSocketException`

Dies sind die <abbr title="Exception – Ausnahme, Fehler: Python-Objekt, das einen Fehler nebst Metadaten repräsentiert">Exceptions</abbr>, die Sie auslösen können, um dem Client Fehler zu berichten.

Wenn Sie eine Exception auslösen, wird, wie es bei normalem Python der Fall wäre, der Rest der Ausführung abgebrochen. Auf diese Weise können Sie diese Exceptions von überall im Code werfen, um einen Request abzubrechen und den Fehler dem Client anzuzeigen.

Sie können Folgendes verwenden:

* `HTTPException`
* `WebSocketException`

Diese Exceptions können direkt von `fastapi` importiert werden:

```python
from fastapi import HTTPException, WebSocketException
```

::: fastapi.HTTPException

::: fastapi.WebSocketException
