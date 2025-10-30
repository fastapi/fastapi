# JSON-kompatibler Encoder { #json-compatible-encoder }

Es gibt Fälle, da möchten Sie einen Datentyp (etwa ein Pydantic-Modell) in etwas konvertieren, das kompatibel mit JSON ist (etwa ein `dict`, eine `list`, usw.).

Zum Beispiel, wenn Sie es in einer Datenbank speichern möchten.

Dafür bietet **FastAPI** eine Funktion `jsonable_encoder()`.

## `jsonable_encoder` verwenden { #using-the-jsonable-encoder }

Stellen wir uns vor, Sie haben eine Datenbank `fake_db`, die nur JSON-kompatible Daten entgegennimmt.

Sie akzeptiert zum Beispiel keine `datetime`-Objekte, da die nicht kompatibel mit JSON sind.

Ein `datetime`-Objekt müsste also in einen `str` umgewandelt werden, der die Daten im <a href="https://en.wikipedia.org/wiki/ISO_8601" class="external-link" target="_blank">ISO-Format</a> enthält.

Genauso würde die Datenbank kein Pydantic-Modell (ein Objekt mit Attributen) akzeptieren, sondern nur ein `dict`.

Sie können für diese Fälle `jsonable_encoder` verwenden.

Es nimmt ein Objekt entgegen, wie etwa ein Pydantic-Modell, und gibt eine JSON-kompatible Version zurück:

{* ../../docs_src/encoder/tutorial001_py310.py hl[4,21] *}

In diesem Beispiel wird das Pydantic-Modell in ein `dict`, und das `datetime`-Objekt in ein `str` konvertiert.

Das Resultat dieses Aufrufs ist etwas, das mit Pythons Standard-<a href="https://docs.python.org/3/library/json.html#json.dumps" class="external-link" target="_blank">`json.dumps()`</a> kodiert werden kann.

Es wird also kein großer `str` zurückgegeben, der die Daten im JSON-Format (als String) enthält. Es wird eine Python-Standarddatenstruktur (z. B. ein `dict`) zurückgegeben, mit Werten und Unterwerten, die alle mit JSON kompatibel sind.

/// note | Hinweis

`jsonable_encoder` wird tatsächlich von **FastAPI** intern verwendet, um Daten zu konvertieren. Aber es ist in vielen anderen Szenarien hilfreich.

///
