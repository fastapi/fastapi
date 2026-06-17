# Separate OpenAPI-Schemas für Eingabe und Ausgabe oder nicht { #separate-openapi-schemas-for-input-and-output-or-not }

Seit der Veröffentlichung von **Pydantic v2** ist die generierte OpenAPI etwas genauer und **korrekter** als zuvor. 😎

Tatsächlich gibt es in einigen Fällen sogar **zwei JSON-Schemas** in OpenAPI für dasselbe Pydantic-Modell, für Eingabe und Ausgabe, je nachdem, ob sie **Defaultwerte** haben.

Sehen wir uns an, wie das funktioniert und wie Sie es bei Bedarf ändern können.

## Pydantic-Modelle für Eingabe und Ausgabe { #pydantic-models-for-input-and-output }

Nehmen wir an, Sie haben ein Pydantic-Modell mit Defaultwerten wie dieses:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:7] hl[7] *}

### Modell für Eingabe { #model-for-input }

Wenn Sie dieses Modell wie hier als Eingabe verwenden:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:15] hl[14] *}

... dann ist das Feld `description` **nicht erforderlich**. Weil es den Defaultwert `None` hat.

### Eingabemodell in der Dokumentation { #input-model-in-docs }

Sie können überprüfen, dass das Feld `description` in der Dokumentation kein **rotes Sternchen** enthält, es ist nicht als erforderlich markiert:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image01.png">
</div>

### Modell für die Ausgabe { #model-for-output }

Wenn Sie jedoch dasselbe Modell als Ausgabe verwenden, wie hier:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py hl[19] *}

... dann, weil `description` einen Defaultwert hat, wird es, wenn Sie für dieses Feld **nichts zurückgeben**, immer noch diesen **Defaultwert** haben.

### Modell für Ausgabe-Responsedaten { #model-for-output-response-data }

Wenn Sie mit der Dokumentation interagieren und die <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> überprüfen, enthält die JSON-Response den Defaultwert (`null`), obwohl der Code nichts in eines der `description`-Felder geschrieben hat:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image02.png">
</div>

Das bedeutet, dass es **immer einen Wert** hat, der Wert kann jedoch manchmal `None` sein (oder `null` in JSON).

Das bedeutet, dass Clients, die Ihre API verwenden, nicht prüfen müssen, ob der Wert vorhanden ist oder nicht. Sie können davon ausgehen, dass das Feld immer vorhanden ist. In einigen Fällen hat es jedoch nur den Defaultwert `None`.

Um dies in OpenAPI zu kennzeichnen, markieren Sie dieses Feld als **erforderlich**, da es immer vorhanden sein wird.

Aus diesem Grund kann das JSON-Schema für ein Modell unterschiedlich sein, je nachdem, ob es für **Eingabe oder Ausgabe** verwendet wird:

* für die **Eingabe** ist `description` **nicht erforderlich**
* für die **Ausgabe** ist es **erforderlich** (und möglicherweise `None` oder, in JSON-Begriffen, `null`)

### Ausgabemodell in der Dokumentation { #model-for-output-in-docs }

Sie können das Ausgabemodell auch in der Dokumentation überprüfen. **Sowohl** `name` **als auch** `description` sind mit einem **roten Sternchen** als **erforderlich** markiert:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image03.png">
</div>

### Eingabe- und Ausgabemodell in der Dokumentation { #model-for-input-and-output-in-docs }

Und wenn Sie alle verfügbaren Schemas (JSON-Schemas) in OpenAPI überprüfen, werden Sie feststellen, dass es zwei gibt, ein `Item-Input` und ein `Item-Output`.

Für `Item-Input` ist `description` **nicht erforderlich**, es hat kein rotes Sternchen.

Aber für `Item-Output` ist `description` **erforderlich**, es hat ein rotes Sternchen.

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image04.png">
</div>

Mit dieser Funktion von **Pydantic v2** ist Ihre API-Dokumentation **präziser**, und wenn Sie über automatisch generierte Clients und SDKs verfügen, sind diese auch präziser, mit einer besseren **Entwicklererfahrung** und Konsistenz. 🎉

## Schemas nicht trennen { #do-not-separate-schemas }

Nun gibt es einige Fälle, in denen Sie möglicherweise **dasselbe Schema für Eingabe und Ausgabe** haben möchten.

Der Hauptanwendungsfall hierfür besteht wahrscheinlich darin, dass Sie das mal tun möchten, wenn Sie bereits über einige automatisch generierte Client-Codes/SDKs verfügen und im Moment nicht alle automatisch generierten Client-Codes/SDKs aktualisieren möchten, möglicherweise später, aber nicht jetzt.

In diesem Fall können Sie diese Funktion in **FastAPI** mit dem Parameter `separate_input_output_schemas=False` deaktivieren.

/// note | Hinweis

Unterstützung für `separate_input_output_schemas` wurde in FastAPI `0.102.0` hinzugefügt. 🤓

///

{* ../../docs_src/separate_openapi_schemas/tutorial002_py310.py hl[10] *}

### Gleiches Schema für Eingabe- und Ausgabemodelle in der Dokumentation { #same-schema-for-input-and-output-models-in-docs }

Und jetzt wird es ein einziges Schema für die Eingabe und Ausgabe des Modells geben, nur `Item`, und es wird `description` als **nicht erforderlich** kennzeichnen:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image05.png">
</div>
