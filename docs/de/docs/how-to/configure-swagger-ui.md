# Swagger-Oberfläche konfigurieren { #configure-swagger-ui }

Sie können einige zusätzliche <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">Parameter der Swagger-Oberfläche</a> konfigurieren.

Um diese zu konfigurieren, übergeben Sie das Argument `swagger_ui_parameters` beim Erstellen des `FastAPI()`-App-Objekts oder an die Funktion `get_swagger_ui_html()`.

`swagger_ui_parameters` empfängt ein <abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">Dictionary</abbr> mit den Konfigurationen, die direkt an die Swagger-Oberfläche übergeben werden.

FastAPI konvertiert die Konfigurationen nach **JSON**, um diese mit JavaScript kompatibel zu machen, da die Swagger-Oberfläche das benötigt.

## Syntaxhervorhebung deaktivieren { #disable-syntax-highlighting }

Sie könnten beispielsweise die Syntaxhervorhebung in der Swagger-Oberfläche deaktivieren.

Ohne Änderung der Einstellungen ist die Syntaxhervorhebung standardmäßig aktiviert:

<img src="/img/tutorial/extending-openapi/image02.png">

Sie können sie jedoch deaktivieren, indem Sie `syntaxHighlight` auf `False` setzen:

{* ../../docs_src/configure_swagger_ui/tutorial001.py hl[3] *}

... und dann zeigt die Swagger-Oberfläche die Syntaxhervorhebung nicht mehr an:

<img src="/img/tutorial/extending-openapi/image03.png">

## Das Theme ändern { #change-the-theme }

Auf die gleiche Weise könnten Sie das Theme der Syntaxhervorhebung mit dem Schlüssel `"syntaxHighlight.theme"` festlegen (beachten Sie, dass er einen Punkt in der Mitte hat):

{* ../../docs_src/configure_swagger_ui/tutorial002.py hl[3] *}

Obige Konfiguration würde das Theme für die Farbe der Syntaxhervorhebung ändern:

<img src="/img/tutorial/extending-openapi/image04.png">

## Defaultparameter der Swagger-Oberfläche ändern { #change-default-swagger-ui-parameters }

FastAPI enthält einige Defaultkonfigurationsparameter, die für die meisten Anwendungsfälle geeignet sind.

Es umfasst die folgenden Defaultkonfigurationen:

{* ../../fastapi/openapi/docs.py ln[8:23] hl[17:23] *}

Sie können jede davon überschreiben, indem Sie im Argument `swagger_ui_parameters` einen anderen Wert festlegen.

Um beispielsweise `deepLinking` zu deaktivieren, könnten Sie folgende Einstellungen an `swagger_ui_parameters` übergeben:

{* ../../docs_src/configure_swagger_ui/tutorial003.py hl[3] *}

## Andere Parameter der Swagger-Oberfläche { #other-swagger-ui-parameters }

Um alle anderen möglichen Konfigurationen zu sehen, die Sie verwenden können, lesen Sie die offizielle <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">Dokumentation für die Parameter der Swagger-Oberfläche</a>.

## Nur-JavaScript-Einstellungen { #javascript-only-settings }

Die Swagger-Oberfläche erlaubt, dass andere Konfigurationen auch **Nur-JavaScript**-Objekte sein können (z. B. JavaScript-Funktionen).

FastAPI umfasst auch diese Nur-JavaScript-`presets`-Einstellungen:

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

Dabei handelt es sich um **JavaScript**-Objekte, nicht um Strings, daher können Sie diese nicht direkt vom Python-Code aus übergeben.

Wenn Sie solche JavaScript-Konfigurationen verwenden müssen, können Sie einen der früher genannten Wege verwenden. Überschreiben Sie alle *Pfadoperationen* der Swagger-Oberfläche und schreiben Sie manuell jedes benötigte JavaScript.
