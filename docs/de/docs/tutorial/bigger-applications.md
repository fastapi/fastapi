# Größere Anwendungen – mehrere Dateien { #bigger-applications-multiple-files }

Wenn Sie eine Anwendung oder eine Web-API erstellen, ist es selten der Fall, dass Sie alles in einer einzigen Datei unterbringen können.

**FastAPI** bietet ein praktisches Werkzeug zur Strukturierung Ihrer Anwendung bei gleichzeitiger Wahrung der Flexibilität.

/// info | Info

Wenn Sie von Flask kommen, wäre dies das Äquivalent zu Flasks Blueprints.

///

## Eine Beispiel-Dateistruktur { #an-example-file-structure }

Nehmen wir an, Sie haben eine Dateistruktur wie diese:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

/// tip | Tipp

Es gibt mehrere `__init__.py`-Dateien: eine in jedem Verzeichnis oder Unterverzeichnis.

Das ermöglicht den Import von Code aus einer Datei in eine andere.

In `app/main.py` könnten Sie beispielsweise eine Zeile wie diese haben:

```
from app.routers import items
```

///

* Das Verzeichnis `app` enthält alles. Und es hat eine leere Datei `app/__init__.py`, es handelt sich also um ein „Python-Package“ (eine Sammlung von „Python-Modulen“): `app`.
* Es enthält eine Datei `app/main.py`. Da sie sich in einem Python-Package (einem Verzeichnis mit einer Datei `__init__.py`) befindet, ist sie ein „Modul“ dieses Packages: `app.main`.
* Es gibt auch eine Datei `app/dependencies.py`, genau wie `app/main.py` ist sie ein „Modul“: `app.dependencies`.
* Es gibt ein Unterverzeichnis `app/routers/` mit einer weiteren Datei `__init__.py`, es handelt sich also um ein „Python-Subpackage“: `app.routers`.
* Die Datei `app/routers/items.py` befindet sich in einem Package, `app/routers/`, also ist sie ein Submodul: `app.routers.items`.
* Das Gleiche gilt für `app/routers/users.py`, es ist ein weiteres Submodul: `app.routers.users`.
* Es gibt auch ein Unterverzeichnis `app/internal/` mit einer weiteren Datei `__init__.py`, es handelt sich also um ein weiteres „Python-Subpackage“: `app.internal`.
* Und die Datei `app/internal/admin.py` ist ein weiteres Submodul: `app.internal.admin`.

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

Die gleiche Dateistruktur mit Kommentaren:

```
.
├── app                  # „app“ ist ein Python-Package
│   ├── __init__.py      # diese Datei macht „app“ zu einem „Python-Package“
│   ├── main.py          # „main“-Modul, z. B. import app.main
│   ├── dependencies.py  # „dependencies“-Modul, z. B. import app.dependencies
│   └── routers          # „routers“ ist ein „Python-Subpackage“
│   │   ├── __init__.py  # macht „routers“ zu einem „Python-Subpackage“
│   │   ├── items.py     # „items“-Submodul, z. B. import app.routers.items
│   │   └── users.py     # „users“-Submodul, z. B. import app.routers.users
│   └── internal         # „internal“ ist ein „Python-Subpackage“
│       ├── __init__.py  # macht „internal“ zu einem „Python-Subpackage“
│       └── admin.py     # „admin“-Submodul, z. B. import app.internal.admin
```

## `APIRouter` { #apirouter }

Nehmen wir an, die Datei, die nur für die Verwaltung von Benutzern zuständig ist, ist das Submodul unter `/app/routers/users.py`.

Sie möchten die *Pfadoperationen* für Ihre Benutzer vom Rest des Codes trennen, um ihn organisiert zu halten.

Aber es ist immer noch Teil derselben **FastAPI**-Anwendung/Web-API (es ist Teil desselben „Python-Packages“).

Sie können die *Pfadoperationen* für dieses Modul mit `APIRouter` erstellen.

### `APIRouter` importieren { #import-apirouter }

Sie importieren ihn und erstellen eine „Instanz“ auf die gleiche Weise wie mit der Klasse `FastAPI`:

```Python hl_lines="1  3" title="app/routers/users.py"
{!../../docs_src/bigger_applications/app/routers/users.py!}
```

### *Pfadoperationen* mit `APIRouter` { #path-operations-with-apirouter }

Und dann verwenden Sie ihn, um Ihre *Pfadoperationen* zu deklarieren.

Verwenden Sie ihn auf die gleiche Weise wie die Klasse `FastAPI`:

```Python hl_lines="6  11  16" title="app/routers/users.py"
{!../../docs_src/bigger_applications/app/routers/users.py!}
```

Sie können sich `APIRouter` als eine „Mini-`FastAPI`“-Klasse vorstellen.

Alle die gleichen Optionen werden unterstützt.

Alle die gleichen `parameters`, `responses`, `dependencies`, `tags`, usw.

/// tip | Tipp

In diesem Beispiel heißt die Variable `router`, aber Sie können ihr einen beliebigen Namen geben.

///

Wir werden diesen `APIRouter` in die Hauptanwendung `FastAPI` einbinden, aber zuerst kümmern wir uns um die Abhängigkeiten und einen anderen `APIRouter`.

## Abhängigkeiten { #dependencies }

Wir sehen, dass wir einige Abhängigkeiten benötigen, die an mehreren Stellen der Anwendung verwendet werden.

Also fügen wir sie in ihr eigenes `dependencies`-Modul (`app/dependencies.py`) ein.

Wir werden nun eine einfache Abhängigkeit verwenden, um einen benutzerdefinierten `X-Token`-Header zu lesen:

//// tab | Python 3.9+

```Python hl_lines="3  6-8" title="app/dependencies.py"
{!> ../../docs_src/bigger_applications/app_an_py39/dependencies.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  5-7" title="app/dependencies.py"
{!> ../../docs_src/bigger_applications/app_an/dependencies.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | Tipp

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="1  4-6" title="app/dependencies.py"
{!> ../../docs_src/bigger_applications/app/dependencies.py!}
```

////

/// tip | Tipp

Um dieses Beispiel zu vereinfachen, verwenden wir einen erfundenen Header.

Aber in der Praxis werden Sie mit den integrierten [Sicherheits-Werkzeugen](security/index.md){.internal-link target=_blank} bessere Ergebnisse erzielen.

///

## Ein weiteres Modul mit `APIRouter` { #another-module-with-apirouter }

Nehmen wir an, Sie haben im Modul unter `app/routers/items.py` auch die Endpunkte, die für die Verarbeitung von Artikeln („Items“) aus Ihrer Anwendung vorgesehen sind.

Sie haben *Pfadoperationen* für:

* `/items/`
* `/items/{item_id}`

Es ist alles die gleiche Struktur wie bei `app/routers/users.py`.

Aber wir wollen schlauer sein und den Code etwas vereinfachen.

Wir wissen, dass alle *Pfadoperationen* in diesem Modul folgendes haben:

* Pfad-`prefix`: `/items`.
* `tags`: (nur ein Tag: `items`).
* Zusätzliche `responses`.
* `dependencies`: Sie alle benötigen die von uns erstellte `X-Token`-Abhängigkeit.

Anstatt also alles zu jeder *Pfadoperation* hinzuzufügen, können wir es dem `APIRouter` hinzufügen.

```Python hl_lines="5-10  16  21" title="app/routers/items.py"
{!../../docs_src/bigger_applications/app/routers/items.py!}
```

Da der Pfad jeder *Pfadoperation* mit `/` beginnen muss, wie in:

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

... darf das Präfix kein abschließendes `/` enthalten.

Das Präfix lautet in diesem Fall also `/items`.

Wir können auch eine Liste von `tags` und zusätzliche `responses` hinzufügen, die auf alle in diesem Router enthaltenen *Pfadoperationen* angewendet werden.

Und wir können eine Liste von `dependencies` hinzufügen, die allen *Pfadoperationen* im Router hinzugefügt und für jeden an sie gerichteten <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> ausgeführt/aufgelöst werden.

/// tip | Tipp

Beachten Sie, dass ähnlich wie bei [Abhängigkeiten in *Pfadoperation-Dekoratoren*](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank} kein Wert an Ihre *Pfadoperation-Funktion* übergeben wird.

///

Das Endergebnis ist, dass die Pfade für diese Artikel jetzt wie folgt lauten:

* `/items/`
* `/items/{item_id}`

... wie wir es beabsichtigt hatten.

* Sie werden mit einer Liste von Tags gekennzeichnet, die einen einzelnen String `"items"` enthält.
    * Diese „Tags“ sind besonders nützlich für die automatischen interaktiven Dokumentationssysteme (unter Verwendung von OpenAPI).
* Alle enthalten die vordefinierten `responses`.
* Für alle diese *Pfadoperationen* wird die Liste der `dependencies` ausgewertet/ausgeführt, bevor sie selbst ausgeführt werden.
    * Wenn Sie außerdem Abhängigkeiten in einer bestimmten *Pfadoperation* deklarieren, **werden diese ebenfalls ausgeführt**.
    * Zuerst werden die Router-Abhängigkeiten ausgeführt, dann die [`dependencies` im Dekorator](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank} und dann die normalen Parameterabhängigkeiten.
    * Sie können auch [`Security`-Abhängigkeiten mit `scopes`](../advanced/security/oauth2-scopes.md){.internal-link target=_blank} hinzufügen.

/// tip | Tipp

`dependencies` im `APIRouter` können beispielsweise verwendet werden, um eine Authentifizierung für eine ganze Gruppe von *Pfadoperationen* zu erfordern. Selbst wenn die Abhängigkeiten nicht jeder einzeln hinzugefügt werden.

///

/// check | Testen

Die Parameter `prefix`, `tags`, `responses` und `dependencies` sind (wie in vielen anderen Fällen) nur ein Feature von **FastAPI**, um Ihnen dabei zu helfen, Codeverdoppelung zu vermeiden.

///

### Die Abhängigkeiten importieren { #import-the-dependencies }

Der folgende Code befindet sich im Modul `app.routers.items`, also in der Datei `app/routers/items.py`.

Und wir müssen die Abhängigkeitsfunktion aus dem Modul `app.dependencies` importieren, also aus der Datei `app/dependencies.py`.

Daher verwenden wir einen relativen Import mit `..` für die Abhängigkeiten:

```Python hl_lines="3" title="app/routers/items.py"
{!../../docs_src/bigger_applications/app/routers/items.py!}
```

#### Wie relative Importe funktionieren { #how-relative-imports-work }

/// tip | Tipp

Wenn Sie genau wissen, wie Importe funktionieren, fahren Sie mit dem nächsten Abschnitt unten fort.

///

Ein einzelner Punkt `.`, wie in:

```Python
from .dependencies import get_token_header
```

würde bedeuten:

* Beginnend im selben Package, in dem sich dieses Modul (die Datei `app/routers/items.py`) befindet (das Verzeichnis `app/routers/`) ...
* finde das Modul `dependencies` (eine imaginäre Datei unter `app/routers/dependencies.py`) ...
* und importiere daraus die Funktion `get_token_header`.

Aber diese Datei existiert nicht, unsere Abhängigkeiten befinden sich in einer Datei unter `app/dependencies.py`.

Erinnern Sie sich, wie unsere Anwendungs-/Dateistruktur aussieht:

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

---

Die beiden Punkte `..`, wie in:

```Python
from ..dependencies import get_token_header
```

bedeuten:

* Beginnend im selben Package, in dem sich dieses Modul (die Datei `app/routers/items.py`) befindet (das Verzeichnis `app/routers/`) ...
* gehe zum übergeordneten Package (das Verzeichnis `app/`) ...
* und finde dort das Modul `dependencies` (die Datei unter `app/dependencies.py`) ...
* und importiere daraus die Funktion `get_token_header`.

Das funktioniert korrekt! 🎉

---

Das Gleiche gilt, wenn wir drei Punkte `...` verwendet hätten, wie in:

```Python
from ...dependencies import get_token_header
```

Das würde bedeuten:

* Beginnend im selben Package, in dem sich dieses Modul (die Datei `app/routers/items.py`) befindet (das Verzeichnis `app/routers/`) ...
* gehe zum übergeordneten Package (das Verzeichnis `app/`) ...
* gehe dann zum übergeordneten Package dieses Packages (es gibt kein übergeordnetes Package, `app` ist die oberste Ebene 😱) ...
* und finde dort das Modul `dependencies` (die Datei unter `app/dependencies.py`) ...
* und importiere daraus die Funktion `get_token_header`.

Das würde sich auf ein Paket oberhalb von `app/` beziehen, mit seiner eigenen Datei `__init__.py`, usw. Aber das haben wir nicht. Das würde in unserem Beispiel also einen Fehler auslösen. 🚨

Aber jetzt wissen Sie, wie es funktioniert, sodass Sie relative Importe in Ihren eigenen Anwendungen verwenden können, egal wie komplex diese sind. 🤓

### Einige benutzerdefinierte `tags`, `responses`, und `dependencies` hinzufügen { #add-some-custom-tags-responses-and-dependencies }

Wir fügen weder das Präfix `/items` noch `tags=["items"]` zu jeder *Pfadoperation* hinzu, da wir sie zum `APIRouter` hinzugefügt haben.

Aber wir können immer noch _mehr_ `tags` hinzufügen, die auf eine bestimmte *Pfadoperation* angewendet werden, sowie einige zusätzliche `responses`, die speziell für diese *Pfadoperation* gelten:

```Python hl_lines="30-31" title="app/routers/items.py"
{!../../docs_src/bigger_applications/app/routers/items.py!}
```

/// tip | Tipp

Diese letzte Pfadoperation wird eine Kombination von Tags haben: `["items", "custom"]`.

Und sie wird auch beide <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Responses</abbr> in der Dokumentation haben, eine für `404` und eine für `403`.

///

## Das Haupt-`FastAPI` { #the-main-fastapi }

Sehen wir uns nun das Modul unter `app/main.py` an.

Hier importieren und verwenden Sie die Klasse `FastAPI`.

Dies ist die Hauptdatei Ihrer Anwendung, die alles zusammenfügt.

Und da sich der Großteil Ihrer Logik jetzt in seinem eigenen spezifischen Modul befindet, wird die Hauptdatei recht einfach sein.

### `FastAPI` importieren { #import-fastapi }

Sie importieren und erstellen wie gewohnt eine `FastAPI`-Klasse.

Und wir können sogar [globale Abhängigkeiten](dependencies/global-dependencies.md){.internal-link target=_blank} deklarieren, die mit den Abhängigkeiten für jeden `APIRouter` kombiniert werden:

```Python hl_lines="1  3  7" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

### Den `APIRouter` importieren { #import-the-apirouter }

Jetzt importieren wir die anderen Submodule, die `APIRouter` haben:

```Python hl_lines="4-5" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

Da es sich bei den Dateien `app/routers/users.py` und `app/routers/items.py` um Submodule handelt, die Teil desselben Python-Packages `app` sind, können wir einen einzelnen Punkt `.` verwenden, um sie mit „relativen Imports“ zu importieren.

### Wie das Importieren funktioniert { #how-the-importing-works }

Die Sektion:

```Python
from .routers import items, users
```

bedeutet:

* Beginnend im selben Package, in dem sich dieses Modul (die Datei `app/main.py`) befindet (das Verzeichnis `app/`) ...
* Suche nach dem Subpackage `routers` (das Verzeichnis unter `app/routers/`) ...
* und importiere daraus die Submodule `items` (die Datei unter `app/routers/items.py`) und `users` (die Datei unter `app/routers/users.py`) ...

Das Modul `items` verfügt über eine Variable `router` (`items.router`). Das ist dieselbe, die wir in der Datei `app/routers/items.py` erstellt haben, es ist ein `APIRouter`-Objekt.

Und dann machen wir das gleiche für das Modul `users`.

Wir könnten sie auch wie folgt importieren:

```Python
from app.routers import items, users
```

/// info | Info

Die erste Version ist ein „relativer Import“:

```Python
from .routers import items, users
```

Die zweite Version ist ein „absoluter Import“:

```Python
from app.routers import items, users
```

Um mehr über Python-Packages und -Module zu erfahren, lesen Sie <a href="https://docs.python.org/3/tutorial/modules.html" class="external-link" target="_blank">die offizielle Python-Dokumentation über Module</a>.

///

### Namenskollisionen vermeiden { #avoid-name-collisions }

Wir importieren das Submodul `items` direkt, anstatt nur seine Variable `router` zu importieren.

Das liegt daran, dass wir im Submodul `users` auch eine weitere Variable namens `router` haben.

Wenn wir eine nach der anderen importiert hätten, etwa:

```Python
from .routers.items import router
from .routers.users import router
```

würde der `router` von `users` den von `items` überschreiben und wir könnten sie nicht gleichzeitig verwenden.

Um also beide in derselben Datei verwenden zu können, importieren wir die Submodule direkt:

```Python hl_lines="5" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

### Die `APIRouter` für `users` und `items` inkludieren { #include-the-apirouters-for-users-and-items }

Inkludieren wir nun die `router` aus diesen Submodulen `users` und `items`:

```Python hl_lines="10-11" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

/// info | Info

`users.router` enthält den `APIRouter` in der Datei `app/routers/users.py`.

Und `items.router` enthält den `APIRouter` in der Datei `app/routers/items.py`.

///

Mit `app.include_router()` können wir jeden `APIRouter` zur Hauptanwendung `FastAPI` hinzufügen.

Es wird alle Routen von diesem Router als Teil von dieser inkludieren.

/// note | Technische Details

Tatsächlich wird intern eine *Pfadoperation* für jede *Pfadoperation* erstellt, die im `APIRouter` deklariert wurde.

Hinter den Kulissen wird es also tatsächlich so funktionieren, als ob alles dieselbe einzige Anwendung wäre.

///

/// check | Testen

Bei der Einbindung von Routern müssen Sie sich keine Gedanken über die Performanz machen.

Dies dauert Mikrosekunden und geschieht nur beim Start.

Es hat also keinen Einfluss auf die Leistung. ⚡

///

### Einen `APIRouter` mit benutzerdefinierten `prefix`, `tags`, `responses` und `dependencies` einfügen { #include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies }

Stellen wir uns nun vor, dass Ihre Organisation Ihnen die Datei `app/internal/admin.py` gegeben hat.

Sie enthält einen `APIRouter` mit einigen administrativen *Pfadoperationen*, die Ihre Organisation zwischen mehreren Projekten teilt.

In diesem Beispiel wird es ganz einfach sein. Nehmen wir jedoch an, dass wir, da sie mit anderen Projekten in der Organisation geteilt wird, sie nicht ändern und kein `prefix`, `dependencies`, `tags`, usw. direkt zum `APIRouter` hinzufügen können:

```Python hl_lines="3" title="app/internal/admin.py"
{!../../docs_src/bigger_applications/app/internal/admin.py!}
```

Aber wir möchten immer noch ein benutzerdefiniertes `prefix` festlegen, wenn wir den `APIRouter` einbinden, sodass alle seine *Pfadoperationen* mit `/admin` beginnen, wir möchten es mit den `dependencies` sichern, die wir bereits für dieses Projekt haben, und wir möchten `tags` und `responses` hinzufügen.

Wir können das alles deklarieren, ohne den ursprünglichen `APIRouter` ändern zu müssen, indem wir diese Parameter an `app.include_router()` übergeben:

```Python hl_lines="14-17" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

Auf diese Weise bleibt der ursprüngliche `APIRouter` unverändert, sodass wir dieselbe `app/internal/admin.py`-Datei weiterhin mit anderen Projekten in der Organisation teilen können.

Das Ergebnis ist, dass in unserer Anwendung jede der *Pfadoperationen* aus dem Modul `admin` Folgendes haben wird:

* Das Präfix `/admin`.
* Den Tag `admin`.
* Die Abhängigkeit `get_token_header`.
* Die Response `418`. 🍵

Dies wirkt sich jedoch nur auf diesen `APIRouter` in unserer Anwendung aus, nicht auf anderen Code, der ihn verwendet.

So könnten beispielsweise andere Projekte denselben `APIRouter` mit einer anderen Authentifizierungsmethode verwenden.

### Eine *Pfadoperation* hinzufügen { #include-a-path-operation }

Wir können *Pfadoperationen* auch direkt zur `FastAPI`-App hinzufügen.

Hier machen wir es ... nur um zu zeigen, dass wir es können 🤷:

```Python hl_lines="21-23" title="app/main.py"
{!../../docs_src/bigger_applications/app/main.py!}
```

und es wird korrekt funktionieren, zusammen mit allen anderen *Pfadoperationen*, die mit `app.include_router()` hinzugefügt wurden.

/// info | Sehr technische Details

**Hinweis**: Dies ist ein sehr technisches Detail, das Sie wahrscheinlich **einfach überspringen** können.

---

Die `APIRouter` sind nicht „gemountet“, sie sind nicht vom Rest der Anwendung isoliert.

Das liegt daran, dass wir deren *Pfadoperationen* in das OpenAPI-Schema und die Benutzeroberflächen einbinden möchten.

Da wir sie nicht einfach isolieren und unabhängig vom Rest „mounten“ können, werden die *Pfadoperationen* „geklont“ (neu erstellt) und nicht direkt einbezogen.

///

## Es in der automatischen API-Dokumentation testen { #check-the-automatic-api-docs }

Führen Sie nun Ihre App aus:

<div class="termy">

```console
$ fastapi dev app/main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

und öffnen Sie die Dokumentation unter <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Sie sehen die automatische API-Dokumentation, einschließlich der Pfade aller Submodule, mit den richtigen Pfaden (und Präfixen) und den richtigen Tags:

<img src="/img/tutorial/bigger-applications/image01.png">

## Den gleichen Router mehrmals mit unterschiedlichem `prefix` inkludieren { #include-the-same-router-multiple-times-with-different-prefix }

Sie können `.include_router()` auch mehrmals mit *demselben* Router und unterschiedlichen Präfixen verwenden.

Dies könnte beispielsweise nützlich sein, um dieselbe API unter verschiedenen Präfixen verfügbar zu machen, z. B. `/api/v1` und `/api/latest`.

Dies ist eine fortgeschrittene Verwendung, die Sie möglicherweise nicht wirklich benötigen, aber für den Fall, dass Sie sie benötigen, ist sie vorhanden.

## Einen `APIRouter` in einen anderen einfügen { #include-an-apirouter-in-another }

Auf die gleiche Weise, wie Sie einen `APIRouter` in eine `FastAPI`-Anwendung einbinden können, können Sie einen `APIRouter` in einen anderen `APIRouter` einbinden, indem Sie Folgendes verwenden:

```Python
router.include_router(other_router)
```

Stellen Sie sicher, dass Sie dies tun, bevor Sie `router` in die `FastAPI`-App einbinden, damit auch die *Pfadoperationen* von `other_router` inkludiert werden.
