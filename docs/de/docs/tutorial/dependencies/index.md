# Abhängigkeiten

**FastAPI** hat ein sehr mächtiges, aber intuitives **<abbr title="Dependency Injection – Einbringen von Abhängigkeiten: Auch bekannt als Komponenten, Ressourcen, Provider, Services, Injectables">Dependency Injection</abbr>** System.

Es ist so konzipiert, sehr einfach zu verwenden zu sein und es jedem Entwickler sehr leicht zu machen, andere Komponenten mit **FastAPI** zu integrieren.

## Was ist "Dependency Injection"

**"Dependency Injection"** bedeutet in der Programmierung, dass es für Ihren Code (in diesem Fall Ihre *Pfadoperation-Funktionen*) eine Möglichkeit gibt, Dinge zu deklarieren, die er verwenden möchte und die er zum Funktionieren benötigt: "Abhängigkeiten" – "Dependencies".

Das System (in diesem Fall **FastAPI**) kümmert sich dann darum, Ihren Code mit den erforderlichen Abhängigkeiten zu versorgen ("die Abhängigkeiten einfügen" – "inject the dependencies").

Das ist sehr nützlich, wenn Sie:

* Eine gemeinsame Logik haben (dieselbe Code-Logik immer und immer wieder).
* Datenbankverbindungen teilen.
* Sicherheit, Authentifizierung, Rollenanforderungen, usw. durchsetzen.
* Und viele andere Dinge ...

All dies, während Sie Codeverdoppelung minimieren.

## Erste Schritte

Sehen wir uns ein sehr einfaches Beispiel an. Es ist so einfach, dass es vorerst nicht sehr nützlich ist.

Aber so können wir uns besser auf die Funktionsweise des **Dependency Injection** Systems konzentrieren.

### Erstellen Sie eine Abhängigkeit (<abbr title="Das von dem abhängt, die zu verwendende Abhängigkeit">"Dependable"</abbr>)

Konzentrieren wir uns zunächst auf die Abhängigkeit - die Dependency.

Es handelt sich einfach um eine Funktion, die die gleichen Parameter entgegennimmt wie eine *Pfadoperation-Funktion*:
=== "Python 3.10+"

    ```Python hl_lines="8-9"
    {!> ../../../docs_src/dependencies/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="8-11"
    {!> ../../../docs_src/dependencies/tutorial001_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="9-12"
    {!> ../../../docs_src/dependencies/tutorial001_an.py!}
    ```

=== "Python 3.10+ nicht annotiert"

    !!! tip
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="6-7"
    {!> ../../../docs_src/dependencies/tutorial001_py310.py!}
    ```

=== "Python 3.6+ nicht annotiert"

    !!! tip
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="8-11"
    {!> ../../../docs_src/dependencies/tutorial001.py!}
    ```

Das war's schon.

**Zwei Zeilen**.

Und sie hat die gleiche Form und Struktur wie alle Ihre *Pfadoperation-Funktionen*.

Sie können sie sich als *Pfadoperation-Funktion* ohne den "Dekorator" (ohne `@app.get("/some-path")`) vorstellen.

Und sie kann alles zurückgeben, was Sie möchten.

In diesem Fall erwartet diese Abhängigkeit:

* Einen optionalen Query-Parameter `q`, der ein `str` ist.
* Einen optionalen Query-Parameter `skip`, der ein `int` ist und standardmäßig `0` ist.
* Einen optionalen Query-Parameter `limit`, der ein `int` ist und standardmäßig `100` ist.

Und dann wird einfach ein `dict` zurückgegeben, welches diese Werte enthält.

!!! info
    FastAPI unterstützt (und empfiehlt die Verwendung von) `Annotated` seit Version 0.95.0.

    Wenn Sie eine ältere Version haben, werden Sie Fehler angezeigt bekommen, wenn Sie versuchen, `Annotated` zu verwenden.

    Bitte [aktualisieren Sie FastAPI](../../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank} daher mindestens zu Version 0.95.1, bevor Sie `Annotated` verwenden.

### `Depends` importieren

=== "Python 3.10+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/dependencies/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/dependencies/tutorial001_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/dependencies/tutorial001_an.py!}
    ```

=== "Python 3.10+ nicht annotiert"

    !!! tip
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="1"
    {!> ../../../docs_src/dependencies/tutorial001_py310.py!}
    ```

=== "Python 3.6+ nicht annotiert"

    !!! tip
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="3"
    {!> ../../../docs_src/dependencies/tutorial001.py!}
    ```

### Deklarieren der Abhängigkeit im <abbr title="Das Abhängige, der Verwender der Abhängigkeit">"Dependant"</abbr>

So wie auch `Body`, `Query`, usw., verwenden Sie `Depends` mit den Parametern Ihrer *Pfadoperation-Funktion*:

=== "Python 3.10+"

    ```Python hl_lines="13  18"
    {!> ../../../docs_src/dependencies/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="15  20"
    {!> ../../../docs_src/dependencies/tutorial001_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="16  21"
    {!> ../../../docs_src/dependencies/tutorial001_an.py!}
    ```

=== "Python 3.10+ nicht annotiert"

    !!! tip
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="11  16"
    {!> ../../../docs_src/dependencies/tutorial001_py310.py!}
    ```

=== "Python 3.6+ nicht annotiert"

    !!! tip
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="15  20"
    {!> ../../../docs_src/dependencies/tutorial001.py!}
    ```

Obwohl Sie `Depends` in den Parametern Ihrer Funktion genauso verwenden wie `Body`, `Query`, usw., funktioniert `Depends` etwas anders.

Sie übergeben `Depends` nur einen einzigen Parameter.

Dieser Parameter muss so etwas wie eine Funktion sein.

Sie **rufen diese nicht direkt auf** (fügen Sie am Ende keine Klammern hinzu), sondern übergeben sie einfach als Parameter an `Depends()`.

Und diese Funktion akzeptiert Parameter auf die gleiche Weise wie *Pfadoperation-Funktionen*.

!!! tip
    Im nächsten Kapitel erfahren Sie, welche anderen "Dinge", außer Funktionen, Sie als Abhängigkeiten verwenden können.

Immer wenn ein neuer Request eintrifft, kümmert sich **FastAPI** darum:

* Ihre Abhängigkeitsfunktion ("dependable") mit den richtigen Parametern aufzurufen.
* Sich das Ergebnis von dieser Funktion zu holen.
* Dieses Ergebnis dem Parameter Ihrer *Pfadoperation-Funktion* zuzuweisen.

```mermaid
graph TB

common_parameters(["common_parameters"])
read_items["/items/"]
read_users["/users/"]

common_parameters --> read_items
common_parameters --> read_users
```

Auf diese Weise schreiben Sie gemeinsam genutzten Code nur einmal, und **FastAPI** kümmert sich darum, ihn für Ihre *Pfadoperationen* aufzurufen.

!!! check
    Beachten Sie, dass Sie keine spezielle Klasse erstellen und diese irgendwo an **FastAPI** übergeben müssen, um sie zu "registrieren" oder so ähnlich.

    Sie übergeben es einfach an `Depends` und **FastAPI** weiß, wie der Rest erledigt wird.

## `Annotated`-Abhängigkeiten wiederverwenden

In den Beispielen oben sehen Sie, dass es ein kleines bisschen **Codeverdoppelung** gibt.

Wenn Sie die Abhängigkeit `common_parameters()` verwenden, müssen Sie den gesamten Parameter mit der Typ-Annotation und `Depends()` schreiben:

```Python
commons: Annotated[dict, Depends(common_parameters)]
```

Da wir jedoch `Annotated` verwenden, können wir diesen `Annotated`-Wert in einer Variablen speichern und an mehreren Stellen verwenden:

=== "Python 3.10+"

    ```Python hl_lines="12  16  21"
    {!> ../../../docs_src/dependencies/tutorial001_02_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="14  18  23"
    {!> ../../../docs_src/dependencies/tutorial001_02_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="15  19  24"
    {!> ../../../docs_src/dependencies/tutorial001_02_an.py!}
    ```

!!! tip
    Das ist schlicht Standard Python, es wird als "Typ-Alias" bezeichnet und ist eigentlich nicht **FastAPI**-spezifisch.

    Da **FastAPI** jedoch auf Standard Python, einschließlich `Annotated`, basiert, können Sie diesen Trick in Ihrem Code verwenden. 😎

Die Abhängigkeiten funktionieren weiterhin wie erwartet, und das **Beste daran** ist, dass die **Typinformationen erhalten bleiben**, was bedeutet, dass Ihr Editor Ihnen weiterhin **automatische Vervollständigung**, **Inline-Fehler**, usw. bieten kann. Das Gleiche gilt für andere Tools wie `mypy`.

Das ist besonders nützlich, wenn Sie es in einer **großen Codebasis** verwenden, in der Sie in **vielen *Pfadoperationen*** immer wieder **die gleichen Abhängigkeiten** verwenden.

## `async` oder nicht `async`

Da Abhängigkeiten auch von **FastAPI** aufgerufen werden (so wie Ihre *Pfadoperation-Funktionen*), gelten beim Definieren Ihrer Funktionen dieselben Regeln.

Sie können `async def` oder einfach `def` verwenden.

Und Sie können Abhängigkeiten mit `async def` innerhalb normaler `def`-*Pfadoperation-Funktionen* oder `def`-Abhängigkeiten innerhalb von `async def`-*Pfadoperation-Funktionen*, usw. deklarieren.

Es spielt keine Rolle. **FastAPI** weiß, was zu tun ist.

!!! note "Hinweis"
    Wenn Ihnen das nichts sagt, lesen Sie den [Async: *"In a hurry?"*](../../async.md){.internal-link target=_blank}-Abschnitt über `async` und `await` in der Dokumentation.

## Integriert in OpenAPI

Alle Request-Deklarationen, -Validierungen und -Anforderungen Ihrer Abhängigkeiten (und Unterabhängigkeiten) werden in dasselbe OpenAPI-Schema integriert.

Die interaktive Dokumentation enthält also auch alle Informationen aus diesen Abhängigkeiten:

<img src="/img/tutorial/dependencies/image01.png">

## Einfache Verwendung

Näher betrachtet, werden *Pfadoperation-Funktionen* deklariert, um verwendet zu werden, wann immer ein *Pfad* und eine *Operation* übereinstimmen, und dann kümmert sich **FastAPI** darum, die Funktion mit den richtigen Parametern aufzurufen, die Daten aus der Anfrage extrahierend.

Tatsächlich funktionieren alle (oder die meisten) Web-Frameworks auf die gleiche Weise.

Sie rufen diese Funktionen niemals direkt auf. Sie werden von Ihrem Framework aufgerufen (in diesem Fall **FastAPI**).

Mit dem Dependency Injection System können Sie **FastAPI** ebenfalls mitteilen, dass Ihre *Pfadoperation-Funktion* von etwas anderem "abhängt", das vor Ihrer *Pfadoperation-Funktion* ausgeführt werden soll, und **FastAPI** kümmert sich darum, es auszuführen und die Ergebnisse zu "injizieren".

Andere gebräuchliche Begriffe für dieselbe Idee der "Abhängigkeitsinjektion" sind:

* Ressourcen
* Provider
* Services
* Injectables
* Komponenten

## **FastAPI**-Plug-ins

Integrationen und "Plug-in"s können mit dem **Dependency Injection** System erstellt werden. Aber tatsächlich besteht **keine Notwendigkeit, "Plug-ins" zu erstellen**, da es durch die Verwendung von Abhängigkeiten möglich ist, eine unendliche Anzahl von Integrationen und Interaktionen zu deklarieren, die dann für Ihre *Pfadoperation-Funktionen* verfügbar sind.

Und Abhängigkeiten können auf sehr einfache und intuitive Weise erstellt werden, sodass Sie einfach die benötigten Python-Packages importieren und sie in wenigen Codezeilen, *im wahrsten Sinne des Wortes*, mit Ihren API-Funktionen integrieren.

Beispiele hierfür finden Sie in den nächsten Kapiteln zu relationalen und NoSQL-Datenbanken, Sicherheit usw.

## **FastAPI**-Kompatibilität

Die Einfachheit des Dependency Injection Systems macht **FastAPI** kompatibel mit:

* allen relationalen Datenbanken
* NoSQL-Datenbanken
* externen Packages
* externen APIs
* Authentifizierungs- und Autorisierungssystemen
* API-Nutzungs-Überwachungssystemen
* Responsedaten-Injektionssystemen
* usw.

## Einfach und leistungsstark

Obwohl das hierarchische Dependency Injection System sehr einfach zu definieren und zu verwenden ist, ist es dennoch sehr mächtig.

Sie können Abhängigkeiten definieren, die selbst wiederum Abhängigkeiten definieren können.

Am Ende wird ein hierarchischer Baum von Abhängigkeiten erstellt, und das **Dependency Injection** System kümmert sich darum, alle diese Abhängigkeiten (und deren Unterabhängigkeiten) für Sie aufzulösen und die Ergebnisse bei jedem Schritt einzubinden (zu injizieren).

Nehmen wir zum Beispiel an, Sie haben vier API-Endpunkte (*Pfadoperationen*):

* `/items/public/`
* `/items/private/`
* `/users/{user_id}/activate`
* `/items/pro/`

Dann könnten Sie für jeden davon unterschiedliche Berechtigungsanforderungen hinzufügen, nur mit Abhängigkeiten und Unterabhängigkeiten:

```mermaid
graph TB

current_user(["current_user"])
active_user(["active_user"])
admin_user(["admin_user"])
paying_user(["paying_user"])

public["/items/public/"]
private["/items/private/"]
activate_user["/users/{user_id}/activate"]
pro_items["/items/pro/"]

current_user --> active_user
active_user --> admin_user
active_user --> paying_user

current_user --> public
active_user --> private
admin_user --> activate_user
paying_user --> pro_items
```

## Integriert mit **OpenAPI**

Alle diese Abhängigkeiten, während sie ihre Anforderungen deklarieren, fügen auch Parameter, Validierungen, usw. zu Ihren *Pfadoperationen* hinzu.

**FastAPI** kümmert sich darum, alles zum OpenAPI-Schema hinzuzufügen, damit es in den interaktiven Dokumentationssystemen angezeigt wird.
