# Abhängigkeiten – `Depends()` und `Security()`

## `Depends()`

Abhängigkeiten werden hauptsächlich mit der speziellen Funktion `Depends()` behandelt, die ein Callable entgegennimmt.

Hier finden Sie deren Referenz und Parameter.

Sie können sie direkt von `fastapi` importieren:

```python
from fastapi import Depends
```

::: fastapi.Depends

## `Security()`

In vielen Szenarien können Sie die Sicherheit (Autorisierung, Authentifizierung usw.) mit Abhängigkeiten handhaben, indem Sie `Depends()` verwenden.

Wenn Sie jedoch auch OAuth2-Scopes deklarieren möchten, können Sie `Security()` anstelle von `Depends()` verwenden.

Sie können `Security()` direkt von `fastapi` importieren:

```python
from fastapi import Security
```

::: fastapi.Security
