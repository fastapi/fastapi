# Den Request direkt verwenden

Bisher haben Sie die Teile des Requests, die Sie benötigen, mithilfe von deren Typen deklariert.

Daten nehmend von:

* Dem Pfad als Parameter.
* Headern.
* Cookies.
* usw.

Und indem Sie das tun, validiert **FastAPI** diese Daten, konvertiert sie und generiert automatisch Dokumentation für Ihre API.

Es gibt jedoch Situationen, in denen Sie möglicherweise direkt auf das `Request`-Objekt zugreifen müssen.

## Details zum `Request`-Objekt

Da **FastAPI** unter der Haube eigentlich **Starlette** ist, mit einer Ebene von mehreren Tools darüber, können Sie Starlette's <a href="https://www.starlette.io/requests/" class="external-link" target="_blank">`Request`</a>-Objekt direkt verwenden, wenn Sie es benötigen.

Das bedeutet allerdings auch, dass, wenn Sie Daten direkt vom `Request`-Objekt nehmen (z. B. dessen Body lesen), diese von FastAPI nicht validiert, konvertiert oder dokumentiert werden (mit OpenAPI, für die automatische API-Benutzeroberfläche).

Obwohl jeder andere normal deklarierte Parameter (z. B. der Body, mit einem Pydantic-Modell) dennoch validiert, konvertiert, annotiert, usw. werden würde.

Es gibt jedoch bestimmte Fälle, in denen es nützlich ist, auf das `Request`-Objekt zuzugreifen.

## Das `Request`-Objekt direkt verwenden

Angenommen, Sie möchten auf die IP-Adresse/den Host des Clients in Ihrer *Pfadoperation-Funktion* zugreifen.

Dazu müssen Sie direkt auf den Request zugreifen.

```Python hl_lines="1  7-8"
{!../../../docs_src/using_request_directly/tutorial001.py!}
```

Durch die Deklaration eines *Pfadoperation-Funktionsparameters*, dessen Typ der `Request` ist, weiß **FastAPI**, dass es den `Request` diesem Parameter übergeben soll.

/// tip | "Tipp"

Beachten Sie, dass wir in diesem Fall einen Pfad-Parameter zusätzlich zum Request-Parameter deklarieren.

Der Pfad-Parameter wird also extrahiert, validiert, in den spezifizierten Typ konvertiert und mit OpenAPI annotiert.

Auf die gleiche Weise können Sie wie gewohnt jeden anderen Parameter deklarieren und zusätzlich auch den `Request` erhalten.

///

## `Request`-Dokumentation

Weitere Details zum <a href="https://www.starlette.io/requests/" class="external-link" target="_blank">`Request`-Objekt finden Sie in der offiziellen Starlette-Dokumentation</a>.

/// note | "Technische Details"

Sie können auch `from starlette.requests import Request` verwenden.

**FastAPI** stellt es direkt zur Verfügung, als Komfort für Sie, den Entwickler. Es kommt aber direkt von Starlette.

///
