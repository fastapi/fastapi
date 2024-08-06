# Separate OpenAPI-Schemas für Eingabe und Ausgabe oder nicht

Bei Verwendung von **Pydantic v2** ist die generierte OpenAPI etwas genauer und **korrekter** als zuvor. 😎

Tatsächlich gibt es in einigen Fällen sogar **zwei JSON-Schemas** in OpenAPI für dasselbe Pydantic-Modell für Eingabe und Ausgabe, je nachdem, ob sie **Defaultwerte** haben.

Sehen wir uns an, wie das funktioniert und wie Sie es bei Bedarf ändern können.

## Pydantic-Modelle für Eingabe und Ausgabe

Nehmen wir an, Sie haben ein Pydantic-Modell mit Defaultwerten wie dieses:

//// tab | Python 3.10+

```Python hl_lines="7"
{!> ../../../docs_src/separate_openapi_schemas/tutorial001_py310.py[ln:1-7]!}

# Code unterhalb weggelassen 👇
```

<details>
<summary>👀 Vollständige Dateivorschau</summary>

```Python
{!> ../../../docs_src/separate_openapi_schemas/tutorial001_py310.py!}
```

</details>

////

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/separate_openapi_schemas/tutorial001_py39.py[ln:1-9]!}

# Code unterhalb weggelassen 👇
```

<details>
<summary>👀 Vollständige Dateivorschau</summary>

```Python
{!> ../../../docs_src/separate_openapi_schemas/tutorial001_py39.py!}
```

</details>

////

//// tab | Python 3.8+

```Python hl_lines="9"
{!> ../../../docs_src/separate_openapi_schemas/tutorial001.py[ln:1-9]!}

# Code unterhalb weggelassen 👇
```

<details>
<summary>👀 Vollständige Dateivorschau</summary>

```Python
{!> ../../../docs_src/separate_openapi_schemas/tutorial001.py!}
```

</details>

////

### Modell für Eingabe

Wenn Sie dieses Modell wie hier als Eingabe verwenden:

//// tab | Python 3.10+

```Python hl_lines="14"
{!> ../../../docs_src/separate_openapi_schemas/tutorial001_py310.py[ln:1-15]!}

# Code unterhalb weggelassen 👇
```

<details>
<summary>👀 Vollständige Dateivorschau</summary>

```Python
{!> ../../../docs_src/separate_openapi_schemas/tutorial001_py310.py!}
```

</details>

////

//// tab | Python 3.9+

```Python hl_lines="16"
{!> ../../../docs_src/separate_openapi_schemas/tutorial001_py39.py[ln:1-17]!}

# Code unterhalb weggelassen 👇
```

<details>
<summary>👀 Vollständige Dateivorschau</summary>

```Python
{!> ../../../docs_src/separate_openapi_schemas/tutorial001_py39.py!}
```

</details>

////

//// tab | Python 3.8+

```Python hl_lines="16"
{!> ../../../docs_src/separate_openapi_schemas/tutorial001.py[ln:1-17]!}

# Code unterhalb weggelassen 👇
```

<details>
<summary>👀 Vollständige Dateivorschau</summary>

```Python
{!> ../../../docs_src/separate_openapi_schemas/tutorial001.py!}
```

</details>

////

... dann ist das Feld `description` **nicht erforderlich**. Weil es den Defaultwert `None` hat.

### Eingabemodell in der Dokumentation

Sie können überprüfen, dass das Feld `description` in der Dokumentation kein **rotes Sternchen** enthält, es ist nicht als erforderlich markiert:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image01.png">
</div>

### Modell für die Ausgabe

Wenn Sie jedoch dasselbe Modell als Ausgabe verwenden, wie hier:

//// tab | Python 3.10+

```Python hl_lines="19"
{!> ../../../docs_src/separate_openapi_schemas/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="21"
{!> ../../../docs_src/separate_openapi_schemas/tutorial001_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="21"
{!> ../../../docs_src/separate_openapi_schemas/tutorial001.py!}
```

////

... dann, weil  `description` einen Defaultwert hat, wird es, wenn Sie für dieses Feld **nichts zurückgeben**, immer noch diesen **Defaultwert** haben.

### Modell für Ausgabe-Responsedaten

Wenn Sie mit der Dokumentation interagieren und die Response überprüfen, enthält die JSON-Response den Defaultwert (`null`), obwohl der Code nichts in eines der `description`-Felder geschrieben hat:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image02.png">
</div>

Das bedeutet, dass es **immer einen Wert** hat, der Wert kann jedoch manchmal `None` sein (oder `null` in JSON).

Das bedeutet, dass Clients, die Ihre API verwenden, nicht prüfen müssen, ob der Wert vorhanden ist oder nicht. Sie können davon ausgehen, dass das Feld immer vorhanden ist. In einigen Fällen hat es jedoch nur den Defaultwert `None`.

Um dies in OpenAPI zu kennzeichnen, markieren Sie dieses Feld als **erforderlich**, da es immer vorhanden sein wird.

Aus diesem Grund kann das JSON-Schema für ein Modell unterschiedlich sein, je nachdem, ob es für **Eingabe oder Ausgabe** verwendet wird:

* für die **Eingabe** ist `description` **nicht erforderlich**
* für die **Ausgabe** ist es **erforderlich** (und möglicherweise `None` oder, in JSON-Begriffen, `null`)

### Ausgabemodell in der Dokumentation

Sie können das Ausgabemodell auch in der Dokumentation überprüfen. **Sowohl** `name` **als auch** `description` sind mit einem **roten Sternchen** als **erforderlich** markiert:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image03.png">
</div>

### Eingabe- und Ausgabemodell in der Dokumentation

Und wenn Sie alle verfügbaren Schemas (JSON-Schemas) in OpenAPI überprüfen, werden Sie feststellen, dass es zwei gibt, ein `Item-Input` und ein `Item-Output`.

Für `Item-Input` ist `description` **nicht erforderlich**, es hat kein rotes Sternchen.

Aber für `Item-Output` ist `description` **erforderlich**, es hat ein rotes Sternchen.

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image04.png">
</div>

Mit dieser Funktion von **Pydantic v2** ist Ihre API-Dokumentation **präziser**, und wenn Sie über automatisch generierte Clients und SDKs verfügen, sind diese auch präziser, mit einer besseren **Entwicklererfahrung** und Konsistenz. 🎉

## Schemas nicht trennen

Nun gibt es einige Fälle, in denen Sie möglicherweise **dasselbe Schema für Eingabe und Ausgabe** haben möchten.

Der Hauptanwendungsfall hierfür besteht wahrscheinlich darin, dass Sie das mal tun möchten, wenn Sie bereits über einige automatisch generierte Client-Codes/SDKs verfügen und im Moment nicht alle automatisch generierten Client-Codes/SDKs aktualisieren möchten, möglicherweise später, aber nicht jetzt.

In diesem Fall können Sie diese Funktion in **FastAPI** mit dem Parameter `separate_input_output_schemas=False` deaktivieren.

/// info

Unterstützung für `separate_input_output_schemas` wurde in FastAPI `0.102.0` hinzugefügt. 🤓

///

//// tab | Python 3.10+

```Python hl_lines="10"
{!> ../../../docs_src/separate_openapi_schemas/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="12"
{!> ../../../docs_src/separate_openapi_schemas/tutorial002_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="12"
{!> ../../../docs_src/separate_openapi_schemas/tutorial002.py!}
```

////

### Gleiches Schema für Eingabe- und Ausgabemodelle in der Dokumentation

Und jetzt wird es ein einziges Schema für die Eingabe und Ausgabe des Modells geben, nur `Item`, und es wird `description` als **nicht erforderlich** kennzeichnen:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image05.png">
</div>

Dies ist das gleiche Verhalten wie in Pydantic v1. 🤓
