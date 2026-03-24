# Eine Response direkt zurückgeben { #return-a-response-directly }

Wenn Sie eine **FastAPI** *Pfadoperation* erstellen, können Sie normalerweise beliebige Daten davon zurückgeben: ein `dict`, eine `list`, ein Pydantic-Modell, ein Datenbankmodell, usw.

Wenn Sie ein [Responsemodell](../tutorial/response-model.md) deklarieren, wird FastAPI es verwenden, um die Daten mithilfe von Pydantic nach JSON zu serialisieren.

Wenn Sie kein Responsemodell deklarieren, verwendet FastAPI den `jsonable_encoder`, wie in [JSON-kompatibler Encoder](../tutorial/encoder.md) erläutert, und packt die Daten in eine `JSONResponse`.

Sie könnten auch direkt eine `JSONResponse` erstellen und zurückgeben.

/// tip | Tipp

Normalerweise erzielen Sie eine deutlich bessere Leistung, wenn Sie ein [Responsemodell](../tutorial/response-model.md) verwenden, als wenn Sie direkt eine `JSONResponse` zurückgeben, da die Serialisierung der Daten dabei mit Pydantic in Rust erfolgt.

///

## Eine `Response` zurückgeben { #return-a-response }

Tatsächlich können Sie jede `Response` oder jede Unterklasse davon zurückgeben.

/// info | Info

`JSONResponse` selbst ist eine Unterklasse von `Response`.

///

Und wenn Sie eine `Response` zurückgeben, wird **FastAPI** diese direkt weiterleiten.

Es wird keine Datenkonvertierung mit Pydantic-Modellen durchführen, es wird den Inhalt nicht in irgendeinen Typ konvertieren, usw.

Dadurch haben Sie viel Flexibilität. Sie können jeden Datentyp zurückgeben, jede Datendeklaration oder -validierung überschreiben, usw.

Das bringt Ihnen aber auch viel Verantwortung. Sie müssen sicherstellen, dass die von Ihnen zurückgegebenen Daten korrekt sind, das richtige Format haben, serialisierbar sind, usw.

## Verwendung des `jsonable_encoder` in einer `Response` { #using-the-jsonable-encoder-in-a-response }

Da **FastAPI** keine Änderungen an einer von Ihnen zurückgegebenen `Response` vornimmt, müssen Sie sicherstellen, dass deren Inhalt dafür bereit ist.

Sie können beispielsweise kein Pydantic-Modell in eine `JSONResponse` einfügen, ohne es zuvor in ein `dict` zu konvertieren, bei dem alle Datentypen (wie `datetime`, `UUID`, usw.) in JSON-kompatible Typen konvertiert wurden.

In diesen Fällen können Sie den `jsonable_encoder` verwenden, um Ihre Daten zu konvertieren, bevor Sie sie an eine Response übergeben:

{* ../../docs_src/response_directly/tutorial001_py310.py hl[5:6,20:21] *}

/// note | Technische Details

Sie könnten auch `from starlette.responses import JSONResponse` verwenden.

**FastAPI** bietet dieselben `starlette.responses` auch via `fastapi.responses` an, als Annehmlichkeit für Sie, den Entwickler. Die meisten verfügbaren Responses kommen aber direkt von Starlette.

///

## Eine benutzerdefinierte `Response` zurückgeben { #returning-a-custom-response }

Das obige Beispiel zeigt alle Teile, die Sie benötigen, ist aber noch nicht sehr nützlich, da Sie das `item` einfach direkt hätten zurückgeben können, und **FastAPI** würde es für Sie in eine `JSONResponse` einfügen, es in ein `dict` konvertieren, usw. All das standardmäßig.

Sehen wir uns nun an, wie Sie damit eine benutzerdefinierte Response zurückgeben können.

Nehmen wir an, Sie möchten eine [XML](https://en.wikipedia.org/wiki/XML)-Response zurückgeben.

Sie könnten Ihren XML-Inhalt als String in eine `Response` einfügen und sie zurückgeben:

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## Funktionsweise eines Responsemodells { #how-a-response-model-works }

Wenn Sie in einer Pfadoperation ein [Responsemodell - Rückgabetyp](../tutorial/response-model.md) deklarieren, wird **FastAPI** es verwenden, um die Daten mithilfe von Pydantic nach JSON zu serialisieren.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

Da dies auf der Rust-Seite geschieht, ist die Leistung deutlich besser, als wenn es mit normalem Python und der Klasse `JSONResponse` erfolgen würde.

Wenn Sie ein `response_model` oder einen Rückgabetyp verwenden, nutzt FastAPI weder den `jsonable_encoder` (was langsamer wäre) zur Konvertierung der Daten noch die Klasse `JSONResponse`.

Stattdessen nimmt es die von Pydantic mithilfe des Responsemodells (oder Rückgabetyps) generierten JSON-Bytes und gibt direkt eine `Response` mit dem richtigen Mediatyp für JSON (`application/json`) zurück.

## Anmerkungen { #notes }

Wenn Sie eine `Response` direkt zurücksenden, werden deren Daten weder validiert, konvertiert (serialisiert), noch automatisch dokumentiert.

Sie können sie aber trotzdem wie unter [Zusätzliche Responses in OpenAPI](additional-responses.md) beschrieben dokumentieren.

In späteren Abschnitten erfahren Sie, wie Sie diese benutzerdefinierten `Response`s verwenden/deklarieren und gleichzeitig über automatische Datenkonvertierung, Dokumentation, usw. verfügen.
