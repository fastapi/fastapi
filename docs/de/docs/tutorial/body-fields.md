# Body - Felder

So wie Sie zusätzliche Validation und Metadaten in **Pfad-Operation-Funktion**-Parametern mittels `Query`, `Path` und `Body` deklarieren, können Sie auch innerhalb von Pydantic-Modellen zusätzliche Validation und Metadaten deklarieren, mittels Pydantics `Field`.

## `Field` importieren

Importieren Sie es zuerst:

=== "Python 3.10+"

    ```Python hl_lines="4"
    {!> ../../../docs_src/body_fields/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="4"
    {!> ../../../docs_src/body_fields/tutorial001_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="4"
    {!> ../../../docs_src/body_fields/tutorial001_an.py!}
    ```

=== "Python 3.10+ nicht annotiert"

    !!! tip
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="2"
    {!> ../../../docs_src/body_fields/tutorial001_py310.py!}
    ```

=== "Python 3.6+ nicht annotiert"

    !!! tip
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="4"
    {!> ../../../docs_src/body_fields/tutorial001.py!}
    ```

!!! warning
    Beachten Sie, dass `Field` direkt von `pydantic` importiert wird, nicht von `fastapi`, wie die anderen (`Query`, `Path`, `Body`, usw.)

## Modell-Attribute deklarieren

Dann können Sie `Field` mit Modell-Attributen deklarieren:

=== "Python 3.10+"

    ```Python hl_lines="11-14"
    {!> ../../../docs_src/body_fields/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="11-14"
    {!> ../../../docs_src/body_fields/tutorial001_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="12-15"
    {!> ../../../docs_src/body_fields/tutorial001_an.py!}
    ```

=== "Python 3.10+ nicht annotiert"

    !!! tip
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="9-12"
    {!> ../../../docs_src/body_fields/tutorial001_py310.py!}
    ```

=== "Python 3.6+ nicht annotiert"

    !!! tip
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="11-14"
    {!> ../../../docs_src/body_fields/tutorial001.py!}
    ```

`Field` funktioniert genauso wie `Query`, `Path` und `Body`, es hat die gleichen Parameter, usw.

!!! Hinweis "Technische Details"
    Tatsächlich erstellen `Query`, `Path` und andere, die sie kennenlernen werden, Instanzen von Kindklassen einer allgemeinen Klasse `Param`, die ihrerseits eine Kindklasse von Pydantics `FieldInfo`-Klasse ist.

    Und Pydantics `Field` gibt ebenfalls eine Instanz von `FieldInfo` zurück.

    `Body` gibt auch Instanzen einer Kindklasse von `FieldInfo` zurück. Und später werden Sie andere sehen, die Kindklassen der `Body`-Klasse sind.

    Denken Sie daran, dass `Query`, `Path` und andere von `fastapi` tatsächlich Funktionen sind, die spezielle Klassen zurückgeben.

!!! tip
    Beachten Sie, dass jedes Modell-Attribut, mit einem Typ, Defaultwert und `Field`, die gleiche Struktur hat wie ein Pfad-Operation-Funktion-Parameter, nur mit `Field` statt `Path`, `Query`, `Body`.

## Zusätzliche Information hinzufügen

Sie können zusätzliche Information in `Field`, `Query`, `Body`, usw. deklarieren. Und es wird im generierten JSON-Schema untergebracht.

Sie werden später mehr darüber lernen, wie man zusätzliche Information unterbringt, wenn Sie lernen, Beispiele zu deklarieren.

!!! warning
    Extra-Schlüssel, die `Field` überreicht werden, werden auch im resultierenden OpenAPI-Schema ihrer Anwendung gelistet. Da diese Schlüssel nicht notwendigerweise Teil der OpenAPI-Spezifikation sind, könnten einige OpenAPI-Tools, wie etwa [der OpenAPI-Validator](https://validator.swagger.io/), nicht mit Ihrem generierten Schema funktionieren.

## Rekapitulation

Sie können Pydantics `Field` verwenden, um zusätzliche Validierungen und Metadaten für Modell-Attribute zu deklarieren.

Sie können auch Extra-Schlüssel verwenden, um zusätzliche JSON-Schema-Metadaten zu überreichen.
