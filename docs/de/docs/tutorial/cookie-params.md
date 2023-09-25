# Cookie-Parameter

So wie `Query`- und `Path`-Parameter können Sie auch <abbr title='Cookie – "Keks": Mechanismus, der kurze Daten in Textform im Browser des Benutzers speichert und abfragt'>Cookie</abbr>-Parameter definieren.

## `Cookie` importieren

Importieren Sie zuerst `Cookie`:

=== "Python 3.10+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/cookie_params/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/cookie_params/tutorial001_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/cookie_params/tutorial001_an.py!}
    ```

=== "Python 3.10+ nicht annotiert"

    !!! tip
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="1"
    {!> ../../../docs_src/cookie_params/tutorial001_py310.py!}
    ```

=== "Python 3.6+ nicht annotiert"

    !!! tip
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="3"
    {!> ../../../docs_src/cookie_params/tutorial001.py!}
    ```

## `Cookie`-Parameter deklarieren

Dann deklarieren Sie Cookie-Parameter, auf die gleiche Weise, wie Sie auch `Path`- und `Query`-Parameter deklarieren.

Der erste Wert ist der Typ. Sie können `Cookie` die gehabten Extra-Validierungs- und Beschreibungs-Parameter hinzufügen. Danach können Sie einen Defaultwert vergeben:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/cookie_params/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/cookie_params/tutorial001_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/cookie_params/tutorial001_an.py!}
    ```

=== "Python 3.10+ nicht annotiert"

    !!! tip
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="7"
    {!> ../../../docs_src/cookie_params/tutorial001_py310.py!}
    ```

=== "Python 3.6+ nicht annotiert"

    !!! tip
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="9"
    {!> ../../../docs_src/cookie_params/tutorial001.py!}
    ```

!!! Hinweis "Technische Details"
    `Cookie` ist eine Schwesterklasse von `Path` und `Query`. Sie erbt von derselben gemeinsamen `Param`-Elternklasse.

    Aber erinnern Sie sich, dass, wenn Sie `Query`, `Path` und `Cookie` von `fastapi` importieren, diese tatsächlich Funktionen sind, welche spezielle Klassen zurückgeben.

!!! info
    Um Cookies zu deklarieren, müssen Sie `Cookie` verwenden, da diese Parameter sonst als Query-Parameter interpretiert werden würden.

## Rekapitulation

Deklarieren Sie Cookies mittels `Cookie`, auf die gleiche Weise wie bei `Query` und `Path`.
