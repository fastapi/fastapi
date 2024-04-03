# Beispiel-Request-Daten deklarieren

Sie können Beispiele für die Daten deklarieren, die Ihre Anwendung empfangen kann.

Hier sind mehrere Möglichkeiten, das zu tun.

## Zusätzliche JSON-Schemadaten in Pydantic-Modellen

Sie können `examples` („Beispiele“) für ein Pydantic-Modell deklarieren, welche dem generierten JSON-Schema hinzugefügt werden.

=== "Python 3.10+ Pydantic v2"

    ```Python hl_lines="13-24"
    {!> ../../../docs_src/schema_extra_example/tutorial001_py310.py!}
    ```

=== "Python 3.10+ Pydantic v1"

    ```Python hl_lines="13-23"
    {!> ../../../docs_src/schema_extra_example/tutorial001_py310_pv1.py!}
    ```

=== "Python 3.8+ Pydantic v2"

    ```Python hl_lines="15-26"
    {!> ../../../docs_src/schema_extra_example/tutorial001.py!}
    ```

=== "Python 3.8+ Pydantic v1"

    ```Python hl_lines="15-25"
    {!> ../../../docs_src/schema_extra_example/tutorial001_pv1.py!}
    ```

Diese zusätzlichen Informationen werden unverändert zum für dieses Modell ausgegebenen **JSON-Schema** hinzugefügt und in der API-Dokumentation verwendet.

=== "Pydantic v2"

    In Pydantic Version 2 würden Sie das Attribut `model_config` verwenden, das ein `dict` akzeptiert, wie beschrieben in <a href="https://docs.pydantic.dev/latest/api/config/" class="external-link" target="_blank">Pydantic-Dokumentation: Configuration</a>.

    Sie können `json_schema_extra` setzen, mit einem `dict`, das alle zusätzlichen Daten enthält, die im generierten JSON-Schema angezeigt werden sollen, einschließlich `examples`.

=== "Pydantic v1"

    In Pydantic Version 1 würden Sie eine interne Klasse `Config` und `schema_extra` verwenden, wie beschrieben in <a href="https://docs.pydantic.dev/1.10/usage/schema/#schema-customization" class="external-link" target="_blank">Pydantic-Dokumentation: Schema customization</a>.

    Sie können `schema_extra` setzen, mit einem `dict`, das alle zusätzlichen Daten enthält, die im generierten JSON-Schema angezeigt werden sollen, einschließlich `examples`.

!!! tip "Tipp"
    Mit derselben Technik können Sie das JSON-Schema erweitern und Ihre eigenen benutzerdefinierten Zusatzinformationen hinzufügen.

    Sie könnten das beispielsweise verwenden, um Metadaten für eine Frontend-Benutzeroberfläche usw. hinzuzufügen.

!!! info
    OpenAPI 3.1.0 (verwendet seit FastAPI 0.99.0) hat Unterstützung für `examples` hinzugefügt, was Teil des **JSON Schema** Standards ist.

    Zuvor unterstützte es nur das Schlüsselwort `example` mit einem einzigen Beispiel. Dieses wird weiterhin von OpenAPI 3.1.0 unterstützt, ist jedoch <abbr title="deprecated – obsolet, veraltet: Es soll nicht mehr verwendet werden">deprecated</abbr> und nicht Teil des JSON Schema Standards. Wir empfehlen Ihnen daher, von `example` nach `examples` zu migrieren. 🤓

    Mehr erfahren Sie am Ende dieser Seite.

## Zusätzliche Argumente für `Field`

Wenn Sie `Field()` mit Pydantic-Modellen verwenden, können Sie ebenfalls zusätzliche `examples` deklarieren:

=== "Python 3.10+"

    ```Python hl_lines="2  8-11"
    {!> ../../../docs_src/schema_extra_example/tutorial002_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="4  10-13"
    {!> ../../../docs_src/schema_extra_example/tutorial002.py!}
    ```

## `examples` im JSON-Schema – OpenAPI

Bei Verwendung von:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

können Sie auch eine Gruppe von `examples` mit zusätzlichen Informationen deklarieren, die zu ihren **JSON-Schemas** innerhalb von **OpenAPI** hinzugefügt werden.

### `Body` mit `examples`

Hier übergeben wir `examples`, welches ein einzelnes Beispiel für die in `Body()` erwarteten Daten enthält:

=== "Python 3.10+"

    ```Python hl_lines="22-29"
    {!> ../../../docs_src/schema_extra_example/tutorial003_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="22-29"
    {!> ../../../docs_src/schema_extra_example/tutorial003_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="23-30"
    {!> ../../../docs_src/schema_extra_example/tutorial003_an.py!}
    ```

=== "Python 3.10+ nicht annotiert"

    !!! tip "Tipp"
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="18-25"
    {!> ../../../docs_src/schema_extra_example/tutorial003_py310.py!}
    ```

=== "Python 3.8+ nicht annotiert"

    !!! tip "Tipp"
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="20-27"
    {!> ../../../docs_src/schema_extra_example/tutorial003.py!}
    ```

### Beispiel in der Dokumentations-Benutzeroberfläche

Mit jeder der oben genannten Methoden würde es in `/docs` so aussehen:

<img src="/img/tutorial/body-fields/image01.png">

### `Body` mit mehreren `examples`

Sie können natürlich auch mehrere `examples` übergeben:

=== "Python 3.10+"

    ```Python hl_lines="23-38"
    {!> ../../../docs_src/schema_extra_example/tutorial004_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="23-38"
    {!> ../../../docs_src/schema_extra_example/tutorial004_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="24-39"
    {!> ../../../docs_src/schema_extra_example/tutorial004_an.py!}
    ```

=== "Python 3.10+ nicht annotiert"

    !!! tip "Tipp"
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="19-34"
    {!> ../../../docs_src/schema_extra_example/tutorial004_py310.py!}
    ```

=== "Python 3.8+ nicht annotiert"

    !!! tip "Tipp"
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="21-36"
    {!> ../../../docs_src/schema_extra_example/tutorial004.py!}
    ```

Wenn Sie das tun, werden die Beispiele Teil des internen **JSON-Schemas** für diese Body-Daten.

<abbr title="26.08.2023">Während dies geschrieben wird</abbr>, unterstützt Swagger UI, das für die Anzeige der Dokumentations-Benutzeroberfläche zuständige Tool, jedoch nicht die Anzeige mehrerer Beispiele für die Daten in **JSON Schema**. Aber lesen Sie unten für einen Workaround weiter.

### OpenAPI-spezifische `examples`

Schon bevor **JSON Schema** `examples` unterstützte, unterstützte OpenAPI ein anderes Feld, das auch `examples` genannt wurde.

Diese **OpenAPI-spezifischen** `examples` finden sich in einem anderen Abschnitt der OpenAPI-Spezifikation. Sie sind **Details für jede *Pfadoperation***, nicht für jedes JSON-Schema.

Und Swagger UI unterstützt dieses spezielle Feld `examples` schon seit einiger Zeit. Sie können es also verwenden, um verschiedene **Beispiele in der Benutzeroberfläche der Dokumentation anzuzeigen**.

Das Format dieses OpenAPI-spezifischen Felds `examples` ist ein `dict` mit **mehreren Beispielen** (anstelle einer `list`e), jedes mit zusätzlichen Informationen, die auch zu **OpenAPI** hinzugefügt werden.

Dies erfolgt nicht innerhalb jedes in OpenAPI enthaltenen JSON-Schemas, sondern außerhalb, in der *Pfadoperation*.

### Verwendung des Parameters `openapi_examples`

Sie können die OpenAPI-spezifischen `examples` in FastAPI mit dem Parameter `openapi_examples` deklarieren, für:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

Die Schlüssel des `dict` identifizieren jedes Beispiel, und jeder Wert (`"value"`) ist ein weiteres `dict`.

Jedes spezifische Beispiel-`dict` in den `examples` kann Folgendes enthalten:

* `summary`: Kurze Beschreibung für das Beispiel.
* `description`: Eine lange Beschreibung, die Markdown-Text enthalten kann.
* `value`: Dies ist das tatsächlich angezeigte Beispiel, z. B. ein `dict`.
* `externalValue`: Alternative zu `value`, eine URL, die auf das Beispiel verweist. Allerdings wird dies möglicherweise nicht von so vielen Tools unterstützt wie `value`.

Sie können es so verwenden:

=== "Python 3.10+"

    ```Python hl_lines="23-49"
    {!> ../../../docs_src/schema_extra_example/tutorial005_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="23-49"
    {!> ../../../docs_src/schema_extra_example/tutorial005_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="24-50"
    {!> ../../../docs_src/schema_extra_example/tutorial005_an.py!}
    ```

=== "Python 3.10+ nicht annotiert"

    !!! tip "Tipp"
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="19-45"
    {!> ../../../docs_src/schema_extra_example/tutorial005_py310.py!}
    ```

=== "Python 3.8+ nicht annotiert"

    !!! tip "Tipp"
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="21-47"
    {!> ../../../docs_src/schema_extra_example/tutorial005.py!}
    ```

### OpenAPI-Beispiele in der Dokumentations-Benutzeroberfläche

Wenn `openapi_examples` zu `Body()` hinzugefügt wird, würde `/docs` so aussehen:

<img src="/img/tutorial/body-fields/image02.png">

## Technische Details

!!! tip "Tipp"
    Wenn Sie bereits **FastAPI** Version **0.99.0 oder höher** verwenden, können Sie diese Details wahrscheinlich **überspringen**.

    Sie sind für ältere Versionen relevanter, bevor OpenAPI 3.1.0 verfügbar war.

    Sie können dies als eine kurze **Geschichtsstunde** zu OpenAPI und JSON Schema betrachten. 🤓

!!! warning "Achtung"
    Dies sind sehr technische Details zu den Standards **JSON Schema** und **OpenAPI**.

    Wenn die oben genannten Ideen bereits für Sie funktionieren, reicht das möglicherweise aus und Sie benötigen diese Details wahrscheinlich nicht, überspringen Sie sie gerne.

Vor OpenAPI 3.1.0 verwendete OpenAPI eine ältere und modifizierte Version von **JSON Schema**.

JSON Schema hatte keine `examples`, daher fügte OpenAPI seiner eigenen modifizierten Version ein eigenes `example`-Feld hinzu.

OpenAPI fügte auch die Felder `example` und `examples` zu anderen Teilen der Spezifikation hinzu:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#parameter-object" class="external-link" target="_blank">`Parameter Object` (in der Spezifikation)</a>, das verwendet wurde von FastAPIs:
    * `Path()`
    * `Query()`
    * `Header()`
    * `Cookie()`
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#media-type-object" class="external-link" target="_blank">`Request Body Object` im Feld `content` des `Media Type Object`s (in der Spezifikation)</a>, das verwendet wurde von FastAPIs:
    * `Body()`
    * `File()`
    * `Form()`

!!! info
    Dieser alte, OpenAPI-spezifische `examples`-Parameter heißt seit FastAPI `0.103.0` jetzt `openapi_examples`.

### JSON Schemas Feld `examples`

Aber dann fügte JSON Schema ein <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a>-Feld zu einer neuen Version der Spezifikation hinzu.

Und dann basierte das neue OpenAPI 3.1.0 auf der neuesten Version (JSON Schema 2020-12), die dieses neue Feld `examples` enthielt.

Und jetzt hat dieses neue `examples`-Feld Vorrang vor dem alten (und benutzerdefinierten) `example`-Feld, im Singular, das jetzt deprecated ist.

Dieses neue `examples`-Feld in JSON Schema ist **nur eine `list`e** von Beispielen, kein Dict mit zusätzlichen Metadaten wie an den anderen Stellen in OpenAPI (oben beschrieben).

!!! info
    Selbst, nachdem OpenAPI 3.1.0 veröffentlicht wurde, mit dieser neuen, einfacheren Integration mit JSON Schema, unterstützte Swagger UI, das Tool, das die automatische Dokumentation bereitstellt, eine Zeit lang OpenAPI 3.1.0 nicht (das tut es seit Version 5.0.0 🎉).

    Aus diesem Grund verwendeten Versionen von FastAPI vor 0.99.0 immer noch Versionen von OpenAPI vor 3.1.0.

### Pydantic- und FastAPI-`examples`

Wenn Sie `examples` innerhalb eines Pydantic-Modells hinzufügen, indem Sie `schema_extra` oder `Field(examples=["something"])` verwenden, wird dieses Beispiel dem **JSON-Schema** für dieses Pydantic-Modell hinzugefügt.

Und dieses **JSON-Schema** des Pydantic-Modells ist in der **OpenAPI** Ihrer API enthalten und wird dann in der Benutzeroberfläche der Dokumentation verwendet.

In Versionen von FastAPI vor 0.99.0 (0.99.0 und höher verwenden das neuere OpenAPI 3.1.0), wenn Sie `example` oder `examples` mit einem der anderen Werkzeuge (`Query()`, `Body()`, usw.) verwendet haben, wurden diese Beispiele nicht zum JSON-Schema hinzugefügt, das diese Daten beschreibt (nicht einmal zur OpenAPI-eigenen Version von JSON Schema), sondern direkt zur *Pfadoperation*-Deklaration in OpenAPI (außerhalb der Teile von OpenAPI, die JSON Schema verwenden).

Aber jetzt, da FastAPI 0.99.0 und höher, OpenAPI 3.1.0 verwendet, das JSON Schema 2020-12 verwendet, und Swagger UI 5.0.0 und höher, ist alles konsistenter und die Beispiele sind in JSON Schema enthalten.

### Swagger-Benutzeroberfläche und OpenAPI-spezifische `examples`.

Da die Swagger-Benutzeroberfläche derzeit nicht mehrere JSON Schema Beispiele unterstützt (Stand: 26.08.2023), hatten Benutzer keine Möglichkeit, mehrere Beispiele in der Dokumentation anzuzeigen.

Um dieses Problem zu lösen, hat FastAPI `0.103.0` **Unterstützung** für die Deklaration desselben alten **OpenAPI-spezifischen** `examples`-Felds mit dem neuen Parameter `openapi_examples` hinzugefügt. 🤓

### Zusammenfassung

Ich habe immer gesagt, dass ich Geschichte nicht so sehr mag ... und jetzt schauen Sie mich an, wie ich „Technikgeschichte“-Unterricht gebe. 😅

Kurz gesagt: **Upgraden Sie auf FastAPI 0.99.0 oder höher**, und die Dinge sind viel **einfacher, konsistenter und intuitiver**, und Sie müssen nicht alle diese historischen Details kennen. 😎
