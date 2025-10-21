# Zusätzliche Responses in OpenAPI { #additional-responses-in-openapi }

/// warning | Achtung

Dies ist ein eher fortgeschrittenes Thema.

Wenn Sie mit **FastAPI** beginnen, benötigen Sie dies möglicherweise nicht.

///

Sie können zusätzliche <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Responses</abbr> mit zusätzlichen Statuscodes, Medientypen, Beschreibungen, usw. deklarieren.

Diese zusätzlichen Responses werden in das OpenAPI-Schema aufgenommen, sodass sie auch in der API-Dokumentation erscheinen.

Für diese zusätzlichen Responses müssen Sie jedoch sicherstellen, dass Sie eine `Response`, wie etwa `JSONResponse`, direkt zurückgeben, mit Ihrem Statuscode und Inhalt.

## Zusätzliche Response mit `model` { #additional-response-with-model }

Sie können Ihren *Pfadoperation-Dekoratoren* einen Parameter `responses` übergeben.

Der nimmt ein <abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">`dict`</abbr> entgegen, die Schlüssel sind Statuscodes für jede Response, wie etwa `200`, und die Werte sind andere `dict`s mit den Informationen für jede Response.

Jedes dieser Response-`dict`s kann einen Schlüssel `model` haben, welcher ein Pydantic-Modell enthält, genau wie `response_model`.

**FastAPI** nimmt dieses Modell, generiert dessen JSON-Schema und fügt es an der richtigen Stelle in OpenAPI ein.

Um beispielsweise eine weitere Response mit dem Statuscode `404` und einem Pydantic-Modell `Message` zu deklarieren, können Sie schreiben:

{* ../../docs_src/additional_responses/tutorial001.py hl[18,22] *}

/// note | Hinweis

Beachten Sie, dass Sie die `JSONResponse` direkt zurückgeben müssen.

///

/// info | Info

Der `model`-Schlüssel ist nicht Teil von OpenAPI.

**FastAPI** nimmt das Pydantic-Modell von dort, generiert das JSON-Schema und fügt es an der richtigen Stelle ein.

Die richtige Stelle ist:

* Im Schlüssel `content`, der als Wert ein weiteres JSON-Objekt (`dict`) hat, welches Folgendes enthält:
    * Ein Schlüssel mit dem Medientyp, z. B. `application/json`, der als Wert ein weiteres JSON-Objekt hat, welches Folgendes enthält:
        * Ein Schlüssel `schema`, der als Wert das JSON-Schema aus dem Modell hat, hier ist die richtige Stelle.
            * **FastAPI** fügt hier eine Referenz auf die globalen JSON-Schemas an einer anderen Stelle in Ihrer OpenAPI hinzu, anstatt es direkt einzubinden. Auf diese Weise können andere Anwendungen und Clients diese JSON-Schemas direkt verwenden, bessere Tools zur Codegenerierung bereitstellen, usw.

///

Die generierten Responses in der OpenAPI für diese *Pfadoperation* lauten:

```JSON hl_lines="3-12"
{
    "responses": {
        "404": {
            "description": "Additional Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Message"
                    }
                }
            }
        },
        "200": {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Item"
                    }
                }
            }
        },
        "422": {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                    }
                }
            }
        }
    }
}
```

Die Schemas werden von einer anderen Stelle innerhalb des OpenAPI-Schemas referenziert:

```JSON hl_lines="4-16"
{
    "components": {
        "schemas": {
            "Message": {
                "title": "Message",
                "required": [
                    "message"
                ],
                "type": "object",
                "properties": {
                    "message": {
                        "title": "Message",
                        "type": "string"
                    }
                }
            },
            "Item": {
                "title": "Item",
                "required": [
                    "id",
                    "value"
                ],
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Id",
                        "type": "string"
                    },
                    "value": {
                        "title": "Value",
                        "type": "string"
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            }
        }
    }
}
```

## Zusätzliche Medientypen für die Haupt-Response { #additional-media-types-for-the-main-response }

Sie können denselben `responses`-Parameter verwenden, um verschiedene Medientypen für dieselbe Haupt-Response hinzuzufügen.

Sie können beispielsweise einen zusätzlichen Medientyp `image/png` hinzufügen und damit deklarieren, dass Ihre *Pfadoperation* ein JSON-Objekt (mit dem Medientyp `application/json`) oder ein PNG-Bild zurückgeben kann:

{* ../../docs_src/additional_responses/tutorial002.py hl[19:24,28] *}

/// note | Hinweis

Beachten Sie, dass Sie das Bild direkt mit einer `FileResponse` zurückgeben müssen.

///

/// info | Info

Sofern Sie in Ihrem Parameter `responses` nicht explizit einen anderen Medientyp angeben, geht FastAPI davon aus, dass die Response denselben Medientyp wie die Haupt-Response-Klasse hat (Standardmäßig `application/json`).

Wenn Sie jedoch eine benutzerdefinierte Response-Klasse mit `None` als Medientyp angegeben haben, verwendet FastAPI `application/json` für jede zusätzliche Response, die über ein zugehöriges Modell verfügt.

///

## Informationen kombinieren { #combining-information }

Sie können auch Response-Informationen von mehreren Stellen kombinieren, einschließlich der Parameter `response_model`, `status_code` und `responses`.

Sie können ein `response_model` deklarieren, indem Sie den Standardstatuscode `200` (oder bei Bedarf einen benutzerdefinierten) verwenden und dann zusätzliche Informationen für dieselbe Response in `responses` direkt im OpenAPI-Schema deklarieren.

**FastAPI** behält die zusätzlichen Informationen aus `responses` und kombiniert sie mit dem JSON-Schema aus Ihrem Modell.

Sie können beispielsweise eine Response mit dem Statuscode `404` deklarieren, die ein Pydantic-Modell verwendet und über eine benutzerdefinierte Beschreibung (`description`) verfügt.

Und eine Response mit dem Statuscode `200`, die Ihr `response_model` verwendet, aber ein benutzerdefiniertes Beispiel (`example`) enthält:

{* ../../docs_src/additional_responses/tutorial003.py hl[20:31] *}

Es wird alles kombiniert und in Ihre OpenAPI eingebunden und in der API-Dokumentation angezeigt:

<img src="/img/tutorial/additional-responses/image01.png">

## Vordefinierte und benutzerdefinierte Responses kombinieren { #combine-predefined-responses-and-custom-ones }

Möglicherweise möchten Sie einige vordefinierte Responses haben, die für viele *Pfadoperationen* gelten, Sie möchten diese jedoch mit benutzerdefinierten Responses kombinieren, die für jede *Pfadoperation* erforderlich sind.

In diesen Fällen können Sie die Python-Technik zum „Entpacken“ eines `dict`s mit `**dict_to_unpack` verwenden:

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

Hier wird `new_dict` alle Schlüssel-Wert-Paare von `old_dict` plus das neue Schlüssel-Wert-Paar enthalten:

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

Mit dieser Technik können Sie einige vordefinierte Responses in Ihren *Pfadoperationen* wiederverwenden und sie mit zusätzlichen benutzerdefinierten Responses kombinieren.

Zum Beispiel:

{* ../../docs_src/additional_responses/tutorial004.py hl[13:17,26] *}

## Weitere Informationen zu OpenAPI-Responses { #more-information-about-openapi-responses }

Um zu sehen, was genau Sie in die Responses aufnehmen können, können Sie die folgenden Abschnitte in der OpenAPI-Spezifikation überprüfen:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object" class="external-link" target="_blank">OpenAPI Responses Object</a>, enthält das `Response Object`.
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object" class="external-link" target="_blank">OpenAPI Response Object</a>, Sie können alles davon direkt in jede Response innerhalb Ihres `responses`-Parameter einfügen. Einschließlich `description`, `headers`, `content` (darin deklarieren Sie verschiedene Medientypen und JSON-Schemas) und `links`.
