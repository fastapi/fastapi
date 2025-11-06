# Body – Felder { #body-fields }

So wie Sie zusätzliche Validierung und Metadaten in Parametern der *Pfadoperation-Funktion* mittels `Query`, `Path` und `Body` deklarieren, können Sie auch innerhalb von Pydantic-Modellen zusätzliche Validierung und Metadaten deklarieren, mittels Pydantics `Field`.

## `Field` importieren { #import-field }

Importieren Sie es zuerst:

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[4] *}

/// warning | Achtung

Beachten Sie, dass `Field` direkt von `pydantic` importiert wird, nicht von `fastapi`, wie die anderen (`Query`, `Path`, `Body`, usw.)

///

## Modellattribute deklarieren { #declare-model-attributes }

Dann können Sie `Field` mit Modellattributen deklarieren:

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[11:14] *}

`Field` funktioniert genauso wie `Query`, `Path` und `Body`, es hat die gleichen Parameter, usw.

/// note | Technische Details

Tatsächlich erstellen `Query`, `Path` und andere, die Sie als nächstes sehen werden, Instanzen von Unterklassen einer allgemeinen Klasse `Param`, welche selbst eine Unterklasse von Pydantics `FieldInfo`-Klasse ist.

Und Pydantics `Field` gibt ebenfalls eine Instanz von `FieldInfo` zurück.

`Body` gibt auch direkt Instanzen einer Unterklasse von `FieldInfo` zurück. Später werden Sie andere sehen, die Unterklassen der `Body`-Klasse sind.

Denken Sie daran, dass `Query`, `Path` und andere, wenn Sie sie von `fastapi` importieren, tatsächlich Funktionen sind, die spezielle Klassen zurückgeben.

///

/// tip | Tipp

Beachten Sie, wie jedes Attribut eines Modells mit einem Typ, Defaultwert und `Field` die gleiche Struktur hat wie ein Parameter einer *Pfadoperation-Funktion*, nur mit `Field` statt `Path`, `Query`, `Body`.

///

## Zusätzliche Information hinzufügen { #add-extra-information }

Sie können zusätzliche Information in `Field`, `Query`, `Body`, usw. deklarieren. Und es wird im generierten JSON-Schema untergebracht.

Sie werden später mehr darüber lernen, wie man zusätzliche Information unterbringt, wenn Sie lernen, Beispiele zu deklarieren.

/// warning | Achtung

Extra-Schlüssel, die `Field` überreicht werden, werden auch im resultierenden OpenAPI-Schema Ihrer Anwendung gelistet. Da diese Schlüssel möglicherweise nicht Teil der OpenAPI-Spezifikation sind, könnten einige OpenAPI-Tools, wie etwa [der OpenAPI-Validator](https://validator.swagger.io/), nicht mit Ihrem generierten Schema funktionieren.

///

## Zusammenfassung { #recap }

Sie können Pydantics `Field` verwenden, um zusätzliche Validierungen und Metadaten für Modellattribute zu deklarieren.

Sie können auch die zusätzlichen Schlüsselwortargumente verwenden, um zusätzliche JSON-Schema-Metadaten zu übergeben.
