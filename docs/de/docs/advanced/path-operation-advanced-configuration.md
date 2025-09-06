# Fortgeschrittene Konfiguration der Pfadoperation { #path-operation-advanced-configuration }

## OpenAPI operationId { #openapi-operationid }

/// warning | Achtung

Wenn Sie kein „Experte“ für OpenAPI sind, brauchen Sie dies wahrscheinlich nicht.

///

Mit dem Parameter `operation_id` können Sie die OpenAPI `operationId` festlegen, die in Ihrer *Pfadoperation* verwendet werden soll.

Sie müssten sicherstellen, dass sie für jede Operation eindeutig ist.

{* ../../docs_src/path_operation_advanced_configuration/tutorial001.py hl[6] *}

### Verwendung des Namens der *Pfadoperation-Funktion* als operationId { #using-the-path-operation-function-name-as-the-operationid }

Wenn Sie die Funktionsnamen Ihrer API als `operationId`s verwenden möchten, können Sie über alle iterieren und die `operation_id` jeder *Pfadoperation* mit deren `APIRoute.name` überschreiben.

Sie sollten dies tun, nachdem Sie alle Ihre *Pfadoperationen* hinzugefügt haben.

{* ../../docs_src/path_operation_advanced_configuration/tutorial002.py hl[2, 12:21, 24] *}

/// tip | Tipp

Wenn Sie `app.openapi()` manuell aufrufen, sollten Sie vorher die `operationId`s aktualisiert haben.

///

/// warning | Achtung

Wenn Sie dies tun, müssen Sie sicherstellen, dass jede Ihrer *Pfadoperation-Funktionen* einen eindeutigen Namen hat.

Auch wenn diese sich in unterschiedlichen Modulen (Python-Dateien) befinden.

///

## Von OpenAPI ausschließen { #exclude-from-openapi }

Um eine *Pfadoperation* aus dem generierten OpenAPI-Schema (und damit aus den automatischen Dokumentationssystemen) auszuschließen, verwenden Sie den Parameter `include_in_schema` und setzen Sie ihn auf `False`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial003.py hl[6] *}

## Fortgeschrittene Beschreibung mittels Docstring { #advanced-description-from-docstring }

Sie können die verwendeten Zeilen aus dem Docstring einer *Pfadoperation-Funktion* einschränken, die für OpenAPI verwendet werden.

Das Hinzufügen eines `\f` (ein maskiertes „Form Feed“-Zeichen) führt dazu, dass **FastAPI** die für OpenAPI verwendete Ausgabe an dieser Stelle abschneidet.

Sie wird nicht in der Dokumentation angezeigt, aber andere Tools (z. B. Sphinx) können den Rest verwenden.

{* ../../docs_src/path_operation_advanced_configuration/tutorial004.py hl[19:29] *}

## Zusätzliche Responses { #additional-responses }

Sie haben wahrscheinlich gesehen, wie man das `response_model` und den `status_code` für eine *Pfadoperation* deklariert.

Das definiert die Metadaten der Haupt-<abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> einer *Pfadoperation*.

Sie können auch zusätzliche Responses mit deren Modellen, Statuscodes usw. deklarieren.

Es gibt hier in der Dokumentation ein ganzes Kapitel darüber, Sie können es unter [Zusätzliche Responses in OpenAPI](additional-responses.md){.internal-link target=_blank} lesen.

## OpenAPI-Extra { #openapi-extra }

Wenn Sie in Ihrer Anwendung eine *Pfadoperation* deklarieren, generiert **FastAPI** automatisch die relevanten Metadaten dieser *Pfadoperation*, die in das OpenAPI-Schema aufgenommen werden sollen.

/// note | Technische Details

In der OpenAPI-Spezifikation wird das <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Operationsobjekt</a> genannt.

///

Es hat alle Informationen zur *Pfadoperation* und wird zur Erstellung der automatischen Dokumentation verwendet.

Es enthält `tags`, `parameters`, `requestBody`, `responses`, usw.

Dieses *Pfadoperation*-spezifische OpenAPI-Schema wird normalerweise automatisch von **FastAPI** generiert, Sie können es aber auch erweitern.

/// tip | Tipp

Dies ist ein Low-Level-Erweiterungspunkt.

Wenn Sie nur zusätzliche Responses deklarieren müssen, können Sie dies bequemer mit [Zusätzliche Responses in OpenAPI](additional-responses.md){.internal-link target=_blank} tun.

///

Sie können das OpenAPI-Schema für eine *Pfadoperation* erweitern, indem Sie den Parameter `openapi_extra` verwenden.

### OpenAPI-Erweiterungen { #openapi-extensions }

Dieses `openapi_extra` kann beispielsweise hilfreich sein, um [OpenAPI-Erweiterungen](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions) zu deklarieren:

{* ../../docs_src/path_operation_advanced_configuration/tutorial005.py hl[6] *}

Wenn Sie die automatische API-Dokumentation öffnen, wird Ihre Erweiterung am Ende der spezifischen *Pfadoperation* angezeigt.

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

Und wenn Sie die resultierende OpenAPI sehen (unter `/openapi.json` in Ihrer API), sehen Sie Ihre Erweiterung auch als Teil der spezifischen *Pfadoperation*:

```JSON hl_lines="22"
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "x-aperture-labs-portal": "blue"
            }
        }
    }
}
```

### Benutzerdefiniertes OpenAPI-*Pfadoperation*-Schema { #custom-openapi-path-operation-schema }

Das <abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">Dictionary</abbr> in `openapi_extra` wird mit dem automatisch generierten OpenAPI-Schema für die *Pfadoperation* zusammengeführt (mittels Deep Merge).

Sie können dem automatisch generierten Schema also zusätzliche Daten hinzufügen.

Sie könnten sich beispielsweise dafür entscheiden, den <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> mit Ihrem eigenen Code zu lesen und zu validieren, ohne die automatischen Funktionen von FastAPI mit Pydantic zu verwenden, aber Sie könnten den Request trotzdem im OpenAPI-Schema definieren wollen.

Das könnte man mit `openapi_extra` machen:

{* ../../docs_src/path_operation_advanced_configuration/tutorial006.py hl[19:36, 39:40] *}

In diesem Beispiel haben wir kein Pydantic-Modell deklariert. Tatsächlich wird der Requestbody nicht einmal als JSON <abbr title="von einem einfachen Format, wie Bytes, in Python-Objekte konvertieren">geparst</abbr>, sondern direkt als `bytes` gelesen und die Funktion `magic_data_reader()` wäre dafür verantwortlich, ihn in irgendeiner Weise zu parsen.

Dennoch können wir das zu erwartende Schema für den Requestbody deklarieren.

### Benutzerdefinierter OpenAPI-Content-Type { #custom-openapi-content-type }

Mit demselben Trick könnten Sie ein Pydantic-Modell verwenden, um das JSON-Schema zu definieren, das dann im benutzerdefinierten Abschnitt des OpenAPI-Schemas für die *Pfadoperation* enthalten ist.

Und Sie könnten dies auch tun, wenn der Datentyp im Request nicht JSON ist.

In der folgenden Anwendung verwenden wir beispielsweise weder die integrierte Funktionalität von FastAPI zum Extrahieren des JSON-Schemas aus Pydantic-Modellen noch die automatische Validierung für JSON. Tatsächlich deklarieren wir den Request-Content-Type als YAML und nicht als JSON:

//// tab | Pydantic v2

{* ../../docs_src/path_operation_advanced_configuration/tutorial007.py hl[17:22, 24] *}

////

//// tab | Pydantic v1

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_pv1.py hl[17:22, 24] *}

////

/// info | Info

In Pydantic Version 1 hieß die Methode zum Abrufen des JSON-Schemas für ein Modell `Item.schema()`, in Pydantic Version 2 heißt die Methode `Item.model_json_schema()`.

///

Obwohl wir nicht die standardmäßig integrierte Funktionalität verwenden, verwenden wir dennoch ein Pydantic-Modell, um das JSON-Schema für die Daten, die wir in YAML empfangen möchten, manuell zu generieren.

Dann verwenden wir den Request direkt und extrahieren den Body als `bytes`. Das bedeutet, dass FastAPI nicht einmal versucht, den Request-Payload als JSON zu parsen.

Und dann parsen wir in unserem Code diesen YAML-Inhalt direkt und verwenden dann wieder dasselbe Pydantic-Modell, um den YAML-Inhalt zu validieren:

//// tab | Pydantic v2

{* ../../docs_src/path_operation_advanced_configuration/tutorial007.py hl[26:33] *}

////

//// tab | Pydantic v1

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_pv1.py hl[26:33] *}

////

/// info | Info

In Pydantic Version 1 war die Methode zum Parsen und Validieren eines Objekts `Item.parse_obj()`, in Pydantic Version 2 heißt die Methode `Item.model_validate()`.

///

/// tip | Tipp

Hier verwenden wir dasselbe Pydantic-Modell wieder.

Aber genauso hätten wir es auch auf andere Weise validieren können.

///
