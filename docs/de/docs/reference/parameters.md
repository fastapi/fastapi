# Request-Parameter

Hier die Referenzinformationen für die Request-Parameter.

Dies sind die Sonderfunktionen, die Sie mittels `Annotated` in *Pfadoperation-Funktion*-Parameter oder Abhängigkeitsfunktionen einfügen können, um Daten aus dem Request abzurufen.

Dies beinhaltet:

* `Query()`
* `Path()`
* `Body()`
* `Cookie()`
* `Header()`
* `Form()`
* `File()`

Sie können diese alle direkt von `fastapi` importieren:

```python
from fastapi import Body, Cookie, File, Form, Header, Path, Query
```

::: fastapi.Query

::: fastapi.Path

::: fastapi.Body

::: fastapi.Cookie

::: fastapi.Header

::: fastapi.Form

::: fastapi.File
