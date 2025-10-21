# Den Request direkt verwenden { #using-the-request-directly }

Bisher haben Sie die Teile des <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Requests</abbr>, die Sie benötigen, mithilfe von deren Typen deklariert.

Daten nehmend von:

* Dem Pfad als Parameter.
* Headern.
* Cookies.
* usw.

Und indem Sie das tun, validiert **FastAPI** diese Daten, konvertiert sie und generiert automatisch Dokumentation für Ihre API.

Es gibt jedoch Situationen, in denen Sie möglicherweise direkt auf das `Request`-Objekt zugreifen müssen.

## Details zum `Request`-Objekt { #details-about-the-request-object }

Da **FastAPI** unter der Haube eigentlich **Starlette** ist, mit einer Ebene von mehreren Tools darüber, können Sie Starlettes <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">`Request`</a>-Objekt direkt verwenden, wenn Sie es benötigen.

Das bedeutet allerdings auch, dass, wenn Sie Daten direkt vom `Request`-Objekt nehmen (z. B. dessen Body lesen), diese von FastAPI nicht validiert, konvertiert oder dokumentiert werden (mit OpenAPI, für die automatische API-Benutzeroberfläche).

Obwohl jeder andere normal deklarierte Parameter (z. B. der Body, mit einem Pydantic-Modell) dennoch validiert, konvertiert, annotiert, usw. werden würde.

Es gibt jedoch bestimmte Fälle, in denen es nützlich ist, auf das `Request`-Objekt zuzugreifen.

## Das `Request`-Objekt direkt verwenden { #use-the-request-object-directly }

Angenommen, Sie möchten auf die IP-Adresse/den Host des Clients in Ihrer *Pfadoperation-Funktion* zugreifen.

Dazu müssen Sie direkt auf den Request zugreifen.

{* ../../docs_src/using_request_directly/tutorial001.py hl[1,7:8] *}

Durch die Deklaration eines *Pfadoperation-Funktionsparameters*, dessen Typ der `Request` ist, weiß **FastAPI**, dass es den `Request` diesem Parameter übergeben soll.

/// tip | Tipp

Beachten Sie, dass wir in diesem Fall einen Pfad-Parameter zusätzlich zum Request-Parameter deklarieren.

Der Pfad-Parameter wird also extrahiert, validiert, in den spezifizierten Typ konvertiert und mit OpenAPI annotiert.

Auf die gleiche Weise können Sie wie gewohnt jeden anderen Parameter deklarieren und zusätzlich auch den `Request` erhalten.

///

## `Request`-Dokumentation { #request-documentation }

Weitere Details zum <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">`Request`-Objekt finden Sie in der offiziellen Starlette-Dokumentation</a>.

/// note | Technische Details

Sie können auch `from starlette.requests import Request` verwenden.

**FastAPI** stellt es direkt zur Verfügung, als Komfort für Sie, den Entwickler. Es kommt aber direkt von Starlette.

///
