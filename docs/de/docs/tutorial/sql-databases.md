# SQL (Relationale) Datenbanken { #sql-relational-databases }

**FastAPI** erfordert nicht, dass Sie eine SQL (relationale) Datenbank verwenden. Sondern Sie können **jede beliebige Datenbank** verwenden, die Sie möchten.

Hier werden wir ein Beispiel mit <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a> sehen.

**SQLModel** basiert auf <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a> und Pydantic. Es wurde vom selben Autor wie **FastAPI** entwickelt, um die perfekte Ergänzung für FastAPI-Anwendungen zu sein, die **SQL-Datenbanken** verwenden müssen.

/// tip | Tipp

Sie könnten jede andere SQL- oder NoSQL-Datenbankbibliothek verwenden, die Sie möchten (in einigen Fällen als <abbr title="Object Relational Mapper – Objektrelationaler Mapper: Ein Fachbegriff für eine Bibliothek, in der einige Klassen SQL-Tabellen und Instanzen Zeilen in diesen Tabellen darstellen">„ORMs“</abbr> bezeichnet), FastAPI zwingt Sie nicht, irgendetwas zu verwenden. 😎

///

Da SQLModel auf SQLAlchemy basiert, können Sie problemlos **jede von SQLAlchemy unterstützte Datenbank** verwenden (was auch bedeutet, dass sie von SQLModel unterstützt werden), wie:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server, usw.

In diesem Beispiel verwenden wir **SQLite**, da es eine einzelne Datei verwendet und Python integrierte Unterstützung bietet. Sie können also dieses Beispiel kopieren und direkt ausführen.

Später, für Ihre Produktionsanwendung, möchten Sie möglicherweise einen Datenbankserver wie **PostgreSQL** verwenden.

/// tip | Tipp

Es gibt einen offiziellen Projektgenerator mit **FastAPI** und **PostgreSQL**, einschließlich eines Frontends und weiterer Tools: <a href="https://github.com/fastapi/full-stack-fastapi-template" class="external-link" target="_blank">https://github.com/fastapi/full-stack-fastapi-template</a>

///

Dies ist ein sehr einfaches und kurzes Tutorial. Wenn Sie mehr über Datenbanken im Allgemeinen, über SQL oder fortgeschrittenere Funktionen erfahren möchten, besuchen Sie die <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel-Dokumentation</a>.

## `SQLModel` installieren { #install-sqlmodel }

Stellen Sie zunächst sicher, dass Sie Ihre [virtuelle Umgebung](../virtual-environments.md){.internal-link target=_blank} erstellen, sie aktivieren und dann `sqlmodel` installieren:

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## Die App mit einem einzelnen Modell erstellen { #create-the-app-with-a-single-model }

Wir erstellen zuerst die einfachste erste Version der App mit einem einzigen **SQLModel**-Modell.

Später werden wir sie verbessern, indem wir unter der Haube **mehrere Modelle** verwenden, um Sicherheit und Vielseitigkeit zu erhöhen. 🤓

### Modelle erstellen { #create-models }

Importieren Sie `SQLModel` und erstellen Sie ein Datenbankmodell:

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

Die `Hero`-Klasse ist einem Pydantic-Modell sehr ähnlich (faktisch ist sie darunter tatsächlich *ein Pydantic-Modell*).

Es gibt ein paar Unterschiede:

* `table=True` sagt SQLModel, dass dies ein *Tabellenmodell* ist, es soll eine **Tabelle** in der SQL-Datenbank darstellen, es ist nicht nur ein *Datenmodell* (wie es jede andere reguläre Pydantic-Klasse wäre).

* `Field(primary_key=True)` sagt SQLModel, dass die `id` der **Primärschlüssel** in der SQL-Datenbank ist (Sie können mehr über SQL-Primärschlüssel in der SQLModel-Dokumentation erfahren).

    Durch das Festlegen des Typs als `int | None` wird SQLModel wissen, dass diese Spalte ein `INTEGER` in der SQL-Datenbank sein sollte und dass sie `NULLABLE` sein sollte.

* `Field(index=True)` sagt SQLModel, dass es einen **SQL-Index** für diese Spalte erstellen soll, was schnelleres Suchen in der Datenbank ermöglicht, wenn Daten mittels dieser Spalte gefiltert werden.

    SQLModel wird verstehen, dass etwas, das als `str` deklariert ist, eine SQL-Spalte des Typs `TEXT` (oder `VARCHAR`, abhängig von der Datenbank) sein wird.

### Eine Engine erstellen { #create-an-engine }

Eine SQLModel-`engine` (darunter ist es tatsächlich eine SQLAlchemy-`engine`) ist das, was die **Verbindungen** zur Datenbank hält.

Sie hätten **ein einziges `engine`-Objekt** für Ihren gesamten Code, um sich mit derselben Datenbank zu verbinden.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

Die Verwendung von `check_same_thread=False` erlaubt FastAPI, dieselbe SQLite-Datenbank in verschiedenen Threads zu verwenden. Dies ist notwendig, da **ein einzelner <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr>** **mehr als einen Thread** verwenden könnte (zum Beispiel in Abhängigkeiten).

Keine Sorge, so wie der Code strukturiert ist, werden wir später sicherstellen, dass wir **eine einzige SQLModel-*Session* pro Request** verwenden, das ist eigentlich das, was `check_same_thread` erreichen möchte.

### Die Tabellen erstellen { #create-the-tables }

Dann fügen wir eine Funktion hinzu, die `SQLModel.metadata.create_all(engine)` verwendet, um die **Tabellen für alle *Tabellenmodelle* zu erstellen**.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### Eine Session-Abhängigkeit erstellen { #create-a-session-dependency }

Eine <abbr title="Sitzung">**`Session`**</abbr> speichert die **Objekte im Speicher** und verfolgt alle Änderungen, die an den Daten vorgenommen werden müssen, dann **verwendet sie die `engine`**, um mit der Datenbank zu kommunizieren.

Wir werden eine FastAPI **Abhängigkeit** mit `yield` erstellen, die eine neue `Session` für jeden Request bereitstellt. Das ist es, was sicherstellt, dass wir eine einzige Session pro Request verwenden. 🤓

Dann erstellen wir eine `Annotated`-Abhängigkeit `SessionDep`, um den Rest des Codes zu vereinfachen, der diese Abhängigkeit nutzen wird.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### Die Datenbanktabellen beim Start erstellen { #create-database-tables-on-startup }

Wir werden die Datenbanktabellen erstellen, wenn die Anwendung startet.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

Hier erstellen wir die Tabellen bei einem Anwendungsstart-Event.

Für die Produktion würden Sie wahrscheinlich ein Migrationsskript verwenden, das ausgeführt wird, bevor Sie Ihre App starten. 🤓

/// tip | Tipp

SQLModel wird Migrationstools haben, die Alembic wrappen, aber im Moment können Sie <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a> direkt verwenden.

///

### Einen Helden erstellen { #create-a-hero }

Da jedes SQLModel-Modell auch ein Pydantic-Modell ist, können Sie es in denselben **Typannotationen** verwenden, die Sie für Pydantic-Modelle verwenden könnten.

Wenn Sie beispielsweise einen Parameter vom Typ `Hero` deklarieren, wird er aus dem **JSON-Body** gelesen.

Auf die gleiche Weise können Sie es als **Rückgabetyp** der Funktion deklarieren, und dann wird die Form der Daten in der automatischen API-Dokumentation angezeigt.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

Hier verwenden wir die `SessionDep`-Abhängigkeit (eine `Session`), um den neuen `Hero` zur `Session`-Instanz hinzuzufügen, die Änderungen an der Datenbank zu committen, die Daten im `hero` zu aktualisieren und ihn anschließend zurückzugeben.

### Helden lesen { #read-heroes }

Wir können `Hero`s aus der Datenbank mit einem `select()` **lesen**. Wir können ein `limit` und `offset` hinzufügen, um die Ergebnisse zu paginieren.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### Einen Helden lesen { #read-one-hero }

Wir können einen einzelnen `Hero` **lesen**.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### Einen Helden löschen { #delete-a-hero }

Wir können auch einen `Hero` **löschen**.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### Die App ausführen { #run-the-app }

Sie können die App ausführen:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Gehen Sie dann zur `/docs`-UI, Sie werden sehen, dass **FastAPI** diese **Modelle** verwendet, um die API zu **dokumentieren**, und es wird sie auch verwenden, um die Daten zu **serialisieren** und zu **validieren**.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## Die App mit mehreren Modellen aktualisieren { #update-the-app-with-multiple-models }

Jetzt lassen Sie uns diese App ein wenig **refaktorisieren**, um die **Sicherheit** und **Vielseitigkeit** zu erhöhen.

Wenn Sie die vorherige App überprüfen, können Sie in der UI sehen, dass sie bis jetzt dem Client erlaubt, die `id` des zu erstellenden `Hero` zu bestimmen. 😱

Das sollten wir nicht zulassen, sie könnten eine `id` überschreiben, die wir bereits in der DB zugewiesen haben. Die Entscheidung über die `id` sollte vom **Backend** oder der **Datenbank** getroffen werden, **nicht vom Client**.

Außerdem erstellen wir einen `secret_name` für den Helden, aber bisher geben wir ihn überall zurück, das ist nicht sehr **geheim** ... 😅

Wir werden diese Dinge beheben, indem wir ein paar **zusätzliche Modelle** hinzufügen. Hier wird SQLModel glänzen. ✨

### Mehrere Modelle erstellen { #create-multiple-models }

In **SQLModel** ist jede Modellklasse, die `table=True` hat, ein **Tabellenmodell**.

Und jede Modellklasse, die `table=True` nicht hat, ist ein **Datenmodell**, diese sind tatsächlich nur Pydantic-Modelle (mit ein paar kleinen zusätzlichen Funktionen). 🤓

Mit SQLModel können wir **Vererbung** verwenden, um **doppelte Felder** in allen Fällen zu **vermeiden**.

#### `HeroBase` – die Basisklasse { #herobase-the-base-class }

Fangen wir mit einem `HeroBase`-Modell an, das alle **Felder hat, die von allen Modellen geteilt werden**:

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` – das *Tabellenmodell* { #hero-the-table-model }

Dann erstellen wir `Hero`, das tatsächliche *Tabellenmodell*, mit den **zusätzlichen Feldern**, die nicht immer in den anderen Modellen enthalten sind:

* `id`
* `secret_name`

Da `Hero` von `HeroBase` erbt, hat es **auch** die **Felder**, die in `HeroBase` deklariert sind, also sind alle Felder von `Hero`:

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` – das öffentliche *Datenmodell* { #heropublic-the-public-data-model }

Als nächstes erstellen wir ein `HeroPublic`-Modell, das an die API-Clients **zurückgegeben** wird.

Es hat dieselben Felder wie `HeroBase`, sodass es `secret_name` nicht enthält.

Endlich ist die Identität unserer Helden geschützt! 🥷

Es deklariert auch `id: int` erneut. Indem wir dies tun, machen wir einen **Vertrag** mit den API-Clients, damit sie immer damit rechnen können, dass die `id` vorhanden ist und ein `int` ist (sie wird niemals `None` sein).

/// tip | Tipp

Es ist sehr nützlich für die API-Clients, wenn das Rückgabemodell sicherstellt, dass ein Wert immer verfügbar und immer `int` (nicht `None`) ist, sie können viel einfacheren Code schreiben, wenn sie diese Sicherheit haben.

Auch **automatisch generierte Clients** werden einfachere Schnittstellen haben, damit die Entwickler, die mit Ihrer API kommunizieren, viel mehr Freude an der Arbeit mit Ihrer API haben können. 😎

///

Alle Felder in `HeroPublic` sind dieselben wie in `HeroBase`, mit `id`, das als `int` (nicht `None`) deklariert ist:

* `id`
* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` – das *Datenmodell* zum Erstellen eines Helden { #herocreate-the-data-model-to-create-a-hero }

Nun erstellen wir ein `HeroCreate`-Modell, das die Daten der Clients **validiert**.

Es hat dieselben Felder wie `HeroBase`, und es hat auch `secret_name`.

Wenn die Clients **einen neuen Helden erstellen**, senden sie jetzt den `secret_name`, er wird in der Datenbank gespeichert, aber diese geheimen Namen werden den API-Clients nicht zurückgegeben.

/// tip | Tipp

So würden Sie **Passwörter** handhaben. Empfangen Sie sie, aber geben Sie sie nicht in der API zurück.

Sie würden auch die Werte der Passwörter **hashen**, bevor Sie sie speichern, und sie **niemals im Klartext** speichern.

///

Die Felder von `HeroCreate` sind:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` – das *Datenmodell* zum Aktualisieren eines Helden { #heroupdate-the-data-model-to-update-a-hero }

In der vorherigen Version der App hatten wir keine Möglichkeit, einen Helden **zu aktualisieren**, aber jetzt mit **mehreren Modellen** können wir es. 🎉

Das `HeroUpdate`-*Datenmodell* ist etwas Besonderes, es hat **die selben Felder**, die benötigt werden, um einen neuen Helden zu erstellen, aber alle Felder sind **optional** (sie haben alle einen Defaultwert). Auf diese Weise, wenn Sie einen Helden aktualisieren, können Sie nur die Felder senden, die Sie aktualisieren möchten.

Da sich tatsächlich **alle Felder ändern** (der Typ enthält jetzt `None` und sie haben jetzt einen Standardwert von `None`), müssen wir sie erneut **deklarieren**.

Wir müssen wirklich nicht von `HeroBase` erben, weil wir alle Felder neu deklarieren. Ich lasse es aus Konsistenzgründen erben, aber das ist nicht notwendig. Es ist mehr eine Frage des persönlichen Geschmacks. 🤷

Die Felder von `HeroUpdate` sind:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### Mit `HeroCreate` erstellen und ein `HeroPublic` zurückgeben { #create-with-herocreate-and-return-a-heropublic }

Nun, da wir **mehrere Modelle** haben, können wir die Teile der App aktualisieren, die sie verwenden.

Wir empfangen im Request ein `HeroCreate`-*Datenmodell* und daraus erstellen wir ein `Hero`-*Tabellenmodell*.

Dieses neue *Tabellenmodell* `Hero` wird die vom Client gesendeten Felder haben und zusätzlich eine `id`, die von der Datenbank generiert wird.

Dann geben wir das gleiche *Tabellenmodell* `Hero` von der Funktion zurück. Aber da wir das `response_model` mit dem `HeroPublic`-*Datenmodell* deklarieren, wird **FastAPI** `HeroPublic` verwenden, um die Daten zu validieren und zu serialisieren.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip | Tipp

Jetzt verwenden wir `response_model=HeroPublic` anstelle der **Rückgabetyp-Annotation** `-> HeroPublic`, weil der Wert, den wir zurückgeben, tatsächlich *kein* `HeroPublic` ist.

Wenn wir `-> HeroPublic` deklariert hätten, würden Ihr Editor und Linter (zu Recht) reklamieren, dass Sie ein `Hero` anstelle eines `HeroPublic` zurückgeben.

Durch die Deklaration in `response_model` sagen wir **FastAPI**, dass es seine Aufgabe erledigen soll, ohne die Typannotationen und die Hilfe von Ihrem Editor und anderen Tools zu beeinträchtigen.

///

### Helden mit `HeroPublic` lesen { #read-heroes-with-heropublic }

Wir können dasselbe wie zuvor tun, um `Hero`s zu **lesen**, und erneut verwenden wir `response_model=list[HeroPublic]`, um sicherzustellen, dass die Daten ordnungsgemäß validiert und serialisiert werden.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### Einen einzelnen Helden mit `HeroPublic` lesen { #read-one-hero-with-heropublic }

Wir können einen einzelnen Helden **lesen**:

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### Einen Helden mit `HeroUpdate` aktualisieren { #update-a-hero-with-heroupdate }

Wir können einen Helden **aktualisieren**. Dafür verwenden wir eine HTTP-`PATCH`-Operation.

Und im Code erhalten wir ein <abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">`dict`</abbr> mit allen Daten, die vom Client gesendet wurden, **nur die Daten, die vom Client gesendet wurden**, unter Ausschluss von Werten, die dort nur als Defaultwerte vorhanden wären. Um dies zu tun, verwenden wir `exclude_unset=True`. Das ist der Haupttrick. 🪄

Dann verwenden wir `hero_db.sqlmodel_update(hero_data)`, um die `hero_db` mit den Daten aus `hero_data` zu aktualisieren.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### Einen Helden wieder löschen { #delete-a-hero-again }

Das **Löschen** eines Helden bleibt ziemlich gleich.

Wir werden dieses Mal nicht dem Wunsch nachgeben, alles zu refaktorisieren. 😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### Die App erneut ausführen { #run-the-app-again }

Sie können die App erneut ausführen:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Wenn Sie zur `/docs`-API-UI gehen, werden Sie sehen, dass sie jetzt aktualisiert ist und nicht mehr erwarten wird, die `id` vom Client beim Erstellen eines Helden zu erhalten, usw.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## Zusammenfassung { #recap }

Sie können <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">**SQLModel**</a> verwenden, um mit einer SQL-Datenbank zu interagieren und den Code mit *Datenmodellen* und *Tabellenmodellen* zu vereinfachen.

Sie können viel mehr in der **SQLModel**-Dokumentation lernen, es gibt ein längeres Mini-<a href="https://sqlmodel.tiangolo.com/tutorial/fastapi/" class="external-link" target="_blank">Tutorial zur Verwendung von SQLModel mit **FastAPI**</a>. 🚀
