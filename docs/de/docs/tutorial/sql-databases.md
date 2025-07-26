# SQL (Relationale) Datenbanken

**FastAPI** erfordert nicht, dass Sie eine SQL (relationale) Datenbank verwenden. Aber Sie können **jede beliebige Datenbank** verwenden, die Sie möchten.

Hier werden wir ein Beispiel mit <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a> sehen.

**SQLModel** basiert auf <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a> und Pydantic. Es wurde vom selben Autor wie **FastAPI** entwickelt, um die perfekte Ergänzung für FastAPI-Anwendungen zu sein, die **SQL-Datenbanken** verwenden müssen.

/// tip | Tipp

Sie könnten jede andere SQL- oder NoSQL-Datenbankbibliothek verwenden, die Sie möchten (in einigen Fällen als <abbr title="Object Relational Mapper, ein ausgefallener Begriff für eine Bibliothek, bei der einige Klassen SQL-Tabellen darstellen und Instanzen Zeilen in diesen Tabellen repräsentieren">„ORMs“</abbr> bezeichnet), FastAPI zwingt Sie nicht, irgendetwas zu verwenden. 😎

///

Da SQLModel auf SQLAlchemy basiert, können Sie problemlos **jede von SQLAlchemy unterstützte Datenbank** verwenden (was auch bedeutet, dass sie von SQLModel unterstützt werden), wie:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server usw.

In diesem Beispiel verwenden wir **SQLite**, da es eine einzige Datei verwendet und Python integrierte Unterstützung bietet. Sie können dieses Beispiel kopieren und direkt so ausführen.

Später, für Ihre Produktionsanwendung, möchten Sie möglicherweise einen Datenbankserver wie **PostgreSQL** verwenden.

/// tip | Tipp

Es gibt einen offiziellen Projektgenerator mit **FastAPI** und **PostgreSQL**, einschließlich eines Frontends und weiterer Tools: <a href="https://github.com/fastapi/full-stack-fastapi-template" class="external-link" target="_blank">https://github.com/fastapi/full-stack-fastapi-template</a>

///

Dies ist ein sehr einfaches und kurzes Tutorial. Wenn Sie mehr über Datenbanken im Allgemeinen, über SQL oder fortgeschrittenere Funktionen erfahren möchten, gehen Sie zu den <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel-Dokumentationen</a>.

## Installieren Sie `SQLModel`

Stellen Sie zunächst sicher, dass Sie Ihre [virtuelle Umgebung](../virtual-environments.md){.internal-link target=_blank} erstellen, sie aktivieren und dann `sqlmodel` installieren:

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## Erstellen Sie die Anwendung mit einem einzigen Modell

Wir erstellen zuerst die einfachste erste Version der Anwendung mit einem einzigen **SQLModel**-Modell.

Später werden wir sie verbessern, indem wir die Sicherheit und die Vielseitigkeit mit **mehreren Modellen** weiter unten erhöhen. 🤓

### Modelle erstellen

Importieren Sie `SQLModel` und erstellen Sie ein Datenbankmodell:

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

Die `Hero`-Klasse ist einem Pydantic-Modell sehr ähnlich (tatsächlich ist sie darunter tatsächlich *ein Pydantic-Modell*).

Es gibt einige Unterschiede:

* `table=True` sagt SQLModel, dass dies ein *Tabellenmodell* ist, es soll eine **Tabelle** in der SQL-Datenbank darstellen, es ist nicht nur ein *Datenmodell* (wie es jede andere reguläre Pydantic-Klasse wäre).

* `Field(primary_key=True)` sagt SQLModel, dass die `id` der **Primärschlüssel** in der SQL-Datenbank ist (Sie können mehr über SQL-Primärschlüssel in den SQLModel-Dokumentationen erfahren).

  Durch das Festlegen des Typs als `int | None` wird SQLModel wissen, dass diese Spalte ein `INTEGER` in der SQL-Datenbank sein sollte und dass sie `NULLABLE` sein sollte.

* `Field(index=True)` sagt SQLModel, dass es einen **SQL-Index** für diese Spalte erstellen soll, der schnellere Lookups in der Datenbank ermöglicht, wenn Daten durch diese Spalte gefiltert gelesen werden.

  SQLModel wird verstehen, dass etwas, das als `str` deklariert ist, eine SQL-Spalte des Typs `TEXT` (oder `VARCHAR`, abhängig von der Datenbank) sein wird.

### Erstellen Sie einen Engine

Eine SQLModel `engine` (darunter ist es tatsächlich eine SQLAlchemy `engine`) ist das, was die **Verbindungen** zur Datenbank hält.

Sie würden **ein einzelnes `engine`-Objekt** für Ihren gesamten Code verwenden, um sich mit demselben Datenbank zu verbinden.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

Die Verwendung von `check_same_thread=False` erlaubt FastAPI, dieselbe SQLite-Datenbank in verschiedenen Threads zu verwenden. Dies ist notwendig, da **eine einzige Anfrage** **mehr als einen Thread** verwenden könnte (zum Beispiel in Abhängigkeiten).

Keine Sorge, mit der Art und Weise, wie der Code strukturiert ist, werden wir sicherstellen, dass wir **eine einzige SQLModel-Session pro Anfrage** später verwenden, dies ist tatsächlich das, was `check_same_thread` zu erreichen versucht.

### Erstellen Sie die Tabellen

Dann fügen wir eine Funktion hinzu, die `SQLModel.metadata.create_all(engine)` verwendet, um die **Tabellen für alle Tabellenmodelle** zu erstellen.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### Erstellen Sie eine Session-Abhängigkeit

Eine **`Session`** speichert die **Objekte im Speicher** und verfolgt alle notwendigen Änderungen in den Daten, dann **verwendet sie die `engine`**, um mit der Datenbank zu kommunizieren.

Wir werden eine FastAPI **Abhängigkeit** mit `yield` erstellen, die eine neue `Session` für jede Anfrage bereitstellt. Dies ist das, was sicherstellt, dass wir eine einzige Session pro Anfrage verwenden. 🤓

Dann erstellen wir eine `Annotated` Abhängigkeit `SessionDep`, um den Rest des Codes zu vereinfachen, der diese Abhängigkeit nutzen wird.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### Erstellen Sie die Datenbanktabellen beim Start

Wir werden die Datenbanktabellen erstellen, wenn die Anwendung startet.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

Hier erstellen wir die Tabellen bei einem Anwendungsstart-Event.

Für die Produktion würden Sie wahrscheinlich ein Migrationsskript verwenden, das ausgeführt wird, bevor Sie Ihre App starten. 🤓

/// tip | Tipp

SQLModel wird Migrationstools mit Alembic bereitstellen, aber vorerst können Sie <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a> direkt verwenden.

///

### Erstellen Sie einen Helden

Da jedes SQLModel-Modell auch ein Pydantic-Modell ist, können Sie es in denselben **Typ-Annotationen** verwenden, die Sie für Pydantic-Modelle verwenden könnten.

Wenn Sie beispielsweise einen Parameter vom Typ `Hero` deklarieren, wird er aus dem **JSON-Body** gelesen.

Auf die gleiche Weise können Sie ihn als Rückgabewert der Funktion deklarieren, und dann wird die Form der Daten in der automatischen API-Dokumentations-UI angezeigt.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

Hier verwenden wir die `SessionDep`-Abhängigkeit (eine `Session`), um den neuen `Hero` zum `Session`-Objekt hinzuzufügen, die Änderungen in der Datenbank zu übermitteln, die Daten im `hero` zu aktualisieren und dann zurückzugeben.

### Helden lesen

Wir können **Helden** aus der Datenbank mit `select()` lesen. Wir können ein `limit` und `offset` einfügen, um die Ergebnisse zu paginieren.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### Einen Helden lesen

Wir können einen einzelnen **Helden** lesen.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### Einen Helden löschen

Wir können auch einen **Helden** löschen.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### Führen Sie die App aus

Sie können die App ausführen:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Gehen Sie dann zur `/docs` UI, Sie werden sehen, dass **FastAPI** diese **Modelle** verwendet, um die API zu **dokumentieren**, und es wird sie verwenden, um die Daten zu **serialisieren** und zu **validieren**.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## Aktualisieren Sie die App mit mehreren Modellen

Jetzt lassen Sie uns diese App ein wenig **umstellen**, um die **Sicherheit** und **Vielseitigkeit** zu erhöhen.

Wenn Sie die vorherige App überprüfen, können Sie in der UI sehen, dass sie dem Client erlaubt, die `id` des zu erstellenden `Hero` zu entscheiden. 😱

Das sollten wir nicht zulassen, sie könnten eine `id` überschreiben, die wir bereits in der DB zugewiesen haben. Das Festlegen der `id` sollte vom **Backend** oder der **Datenbank**, **nicht vom Client** erfolgen.

Darüber hinaus erstellen wir einen `secret_name` für den Helden, aber bisher geben wir ihn überall zurück, das ist nicht sehr **geheim**... 😅

Wir werden diese Dinge beheben, indem wir ein paar **zusätzliche Modelle** hinzufügen. Hier wird SQLModel glänzen. ✨

### Mehrere Modelle erstellen

In **SQLModel** ist jede Modellklasse, die `table=True` hat, ein **Tabellenmodell**.

Und jede Modellklasse, die `table=True` nicht hat, ist ein **Datenmodell**, diese sind tatsächlich nur Pydantic-Modelle (mit ein paar kleinen zusätzlichen Funktionen). 🤓

Mit SQLModel können wir **Vererbung** verwenden, um **doppelte Felder** in allen Fällen zu **vermeiden**.

#### `HeroBase` - die Basisklasse

Beginnen wir mit einem `HeroBase`-Modell, das alle **Felder, die von allen Modellen gemeinsam genutzt werden**, enthält:

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - das *Tabellenmodell*

Dann erstellen wir `Hero`, das eigentliche *Tabellenmodell*, mit den **zusätzlichen Feldern**, die nicht immer in den anderen Modellen sind:

* `id`
* `secret_name`

Da `Hero` von `HeroBase` erbt, hat es **auch** die **Felder**, die in `HeroBase` deklariert sind, sodass alle Felder für `Hero` sind:

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - das öffentliche *Datenmodell*

Als nächstes erstellen wir ein `HeroPublic`-Modell, dies ist das, das **an die API-Clients zurückgegeben** wird.

Es hat dieselben Felder wie `HeroBase`, also wird es `secret_name` nicht enthalten.

Endlich ist die Identität unserer Helden geschützt! 🥷

Es erklärt auch `id: int` neu. Indem wir dies tun, schließen wir einen **Vertrag** mit den API-Clients ab, sodass sie immer erwarten können, dass die `id` vorhanden ist und ein `int` ist (sie wird niemals `None` sein).

/// tip | Tipp

Dass das Rückgabemodell sicherstellt, dass ein Wert immer verfügbar ist und immer `int` ist (nicht `None`), ist sehr nützlich für die API-Clients, sie können viel einfacheren Code schreiben, wenn sie diese Sicherheit haben.

Auch **automatisch generierte Clients** werden einfachere Schnittstellen haben, sodass die Entwickler, die mit Ihrer API kommunizieren, eine viel bessere Zeit haben können, mit Ihrer API zu arbeiten. 😎

///

Alle Felder in `HeroPublic` sind die gleichen wie in `HeroBase`, mit `id` als `int` (nicht `None`):

* `id`
* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - das *Datenmodell* um einen Helden zu erstellen

Jetzt erstellen wir ein `HeroCreate`-Modell, das die Daten von den Clients **validieren** wird.

Es hat die gleichen Felder wie `HeroBase`, und es hat auch `secret_name`.

Jetzt, wenn die Clients **einen neuen Helden erstellen**, senden sie den `secret_name`, er wird in der Datenbank gespeichert, aber diese geheimen Namen werden in der API nicht an die Clients zurückgegeben.

/// tip | Tipp

So würden Sie **Passwörter** behandeln. Sie empfangen sie, aber geben sie nicht in der API zurück.

Sie würden auch **die Werte der Passwörter hashieren**, bevor Sie sie speichern, **niemals im Klartext speichern**.

///

Die Felder von `HeroCreate` sind:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - das *Datenmodell* um einen Helden zu aktualisieren

Wir hatten keine Möglichkeit, **einen Helden zu aktualisieren** in der vorherigen Version der App, aber jetzt mit **mehreren Modellen**, können wir es. 🎉

Das `HeroUpdate` *Datenmodell* ist etwas Besonderes, es hat **alle gleichen Felder**, die benötigt werden, um einen neuen Helden zu erstellen, aber alle Felder sind **optional** (sie haben alle einen Defaultwert). Auf diese Weise, wenn Sie einen Helden aktualisieren, können Sie nur die Felder senden, die Sie aktualisieren möchten.

Da sich alle **Felder wirklich ändern** (der Typ enthält nun `None` und sie haben jetzt einen Defaultwert von `None`), müssen wir sie **neu deklarieren**.

Wir müssen nicht wirklich von `HeroBase` erben, da wir alle Felder neu deklarieren. Ich lasse es einfach nur aus Gründen der Konsistenz erben, aber das ist nicht notwendig. Es ist mehr eine Frage des persönlichen Geschmacks. 🤷

Die Felder von `HeroUpdate` sind:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### Erstellen mit `HeroCreate` und Rückgabe eines `HeroPublic`

Jetzt, da wir **mehrere Modelle** haben, können wir die Teile der App aktualisieren, die sie verwenden.

Wir empfangen in der Anfrage ein `HeroCreate` *Datenmodell*, und daraus erstellen wir ein `Hero` *Tabellenmodell*.

Dieses neue *Tabellenmodell* `Hero` wird die Felder haben, die vom Client gesendet wurden, und wird auch eine `id` haben, die von der Datenbank generiert wird.

Dann geben wir das gleiche *Tabellenmodell* `Hero` wie aus der Funktion aus zurück. Aber da wir das `response_model` mit dem `HeroPublic` *Datenmodell* deklarieren, wird **FastAPI** `HeroPublic` verwenden, um die Daten zu validieren und zu serialisieren.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip | Tipp

Jetzt verwenden wir `response_model=HeroPublic` anstelle der **Rückgabetyp-Annotation** `-> HeroPublic`, weil der Wert, den wir zurückgeben, tatsächlich *kein* `HeroPublic` ist.

Hätten wir `-> HeroPublic` deklariert, würde Ihr Editor und Linter (berechtigterweise) meckern, dass Sie ein `Hero` statt eines `HeroPublic` zurückgeben.

Durch die Deklaration in `response_model` sagen wir **FastAPI**, dass es sein Ding machen soll, ohne die Typ-Annotationen und die Hilfe Ihres Editors und anderer Tools zu stören.

///

### Helden mit `HeroPublic` lesen

Wir können dasselbe wie zuvor tun, um **Helden zu lesen**, erneut verwenden wir `response_model=list[HeroPublic]`, um sicherzustellen, dass die Daten korrekt validiert und serialisiert werden.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### Einen Helden mit `HeroPublic` lesen

Wir können einen einzelnen **Helden** lesen:

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### Update einen Helden mit `HeroUpdate`

Wir können einen **Helden aktualisieren**. Dafür verwenden wir eine HTTP `PATCH`-Operation.

Und im Code erhalten wir ein `dict` mit allen Daten, die vom Client gesendet wurden, **nur die Daten, die vom Client gesendet wurden**, ohne Werte, die nur für die Defaultwerte vorhanden wären. Dazu verwenden wir `exclude_unset=True`. Dies ist der Haupttrick. 🪄

Dann verwenden wir `hero_db.sqlmodel_update(hero_data)`, um das `hero_db` mit den Daten von `hero_data` zu aktualisieren.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### Einen Helden erneut löschen

Das **Löschen** eines Helden bleibt weitgehend gleich.

Wir werden das Verlangen, alles in diesem Fall umzugestalten, nicht befriedigen. 😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### Führen Sie die App erneut aus

Sie können die App noch einmal ausführen:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Wenn Sie zur `/docs` API UI gehen, werden Sie sehen, dass diese jetzt aktualisiert wurde. Sie wird nicht erwarten, die `id` vom Client zu erhalten, wenn sie einen Helden erstellt, usw.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## Zusammenfassung

Sie können <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">**SQLModel**</a> verwenden, um mit einer SQL-Datenbank zu interagieren und den Code mit *Datenmodellen* und *Tabellenmodellen* zu vereinfachen.

Sie können viel mehr in den **SQLModel**-Dokumentationen lernen, es gibt ein längeres Mini <a href="https://sqlmodel.tiangolo.com/tutorial/fastapi/" class="external-link" target="_blank">Tutorial über die Verwendung von SQLModel mit **FastAPI**</a>. 🚀
