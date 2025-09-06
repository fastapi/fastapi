# Statische Assets der Dokumentationsoberfläche (Selbst-Hosting) { #custom-docs-ui-static-assets-self-hosting }

Die API-Dokumentation verwendet **Swagger UI** und **ReDoc**, und jede dieser Dokumentationen benötigt einige JavaScript- und CSS-Dateien.

Standardmäßig werden diese Dateien von einem <abbr title="Content Delivery Network – Inhalte auslieferndes Netzwerk: Ein Dienst, der normalerweise aus mehreren Servern besteht und statische Dateien wie JavaScript und CSS bereitstellt. Er wird häufig verwendet, um diese Dateien vom Server bereitzustellen, der näher am Client liegt, wodurch die Leistung verbessert wird.">CDN</abbr> bereitgestellt.

Es ist jedoch möglich, das anzupassen, ein bestimmtes CDN festzulegen oder die Dateien selbst bereitzustellen.

## Benutzerdefiniertes CDN für JavaScript und CSS { #custom-cdn-for-javascript-and-css }

Nehmen wir an, Sie möchten ein anderes <abbr title="Content Delivery Network – Inhalte auslieferndes Netzwerk">CDN</abbr> verwenden, zum Beispiel möchten Sie `https://unpkg.com/` verwenden.

Das kann nützlich sein, wenn Sie beispielsweise in einem Land leben, in dem bestimmte URLs eingeschränkt sind.

### Die automatischen Dokumentationen deaktivieren { #disable-the-automatic-docs }

Der erste Schritt besteht darin, die automatischen Dokumentationen zu deaktivieren, da diese standardmäßig das Standard-CDN verwenden.

Um diese zu deaktivieren, setzen Sie deren URLs beim Erstellen Ihrer `FastAPI`-App auf `None`:

{* ../../docs_src/custom_docs_ui/tutorial001.py hl[8] *}

### Die benutzerdefinierten Dokumentationen hinzufügen { #include-the-custom-docs }

Jetzt können Sie die *Pfadoperationen* für die benutzerdefinierten Dokumentationen erstellen.

Sie können die internen Funktionen von FastAPI wiederverwenden, um die HTML-Seiten für die Dokumentation zu erstellen und ihnen die erforderlichen Argumente zu übergeben:

* `openapi_url`: die URL, unter welcher die HTML-Seite für die Dokumentation das OpenAPI-Schema für Ihre API abrufen kann. Sie können hier das Attribut `app.openapi_url` verwenden.
* `title`: der Titel Ihrer API.
* `oauth2_redirect_url`: Sie können hier `app.swagger_ui_oauth2_redirect_url` verwenden, um die Standardeinstellung zu verwenden.
* `swagger_js_url`: die URL, unter welcher der HTML-Code für Ihre Swagger-UI-Dokumentation die **JavaScript**-Datei abrufen kann. Dies ist die benutzerdefinierte CDN-URL.
* `swagger_css_url`: die URL, unter welcher der HTML-Code für Ihre Swagger-UI-Dokumentation die **CSS**-Datei abrufen kann. Dies ist die benutzerdefinierte CDN-URL.

Und ähnlich für ReDoc ...

{* ../../docs_src/custom_docs_ui/tutorial001.py hl[2:6,11:19,22:24,27:33] *}

/// tip | Tipp

Die *Pfadoperation* für `swagger_ui_redirect` ist ein Hilfsmittel bei der Verwendung von OAuth2.

Wenn Sie Ihre API mit einem OAuth2-Anbieter integrieren, können Sie sich authentifizieren und mit den erworbenen Anmeldeinformationen zur API-Dokumentation zurückkehren. Und mit ihr interagieren, die echte OAuth2-Authentifizierung verwendend.

Swagger UI erledigt das hinter den Kulissen für Sie, benötigt aber diesen „Umleitungs“-Helfer.

///

### Eine *Pfadoperation* erstellen, um es zu testen { #create-a-path-operation-to-test-it }

Um nun testen zu können, ob alles funktioniert, erstellen Sie eine *Pfadoperation*:

{* ../../docs_src/custom_docs_ui/tutorial001.py hl[36:38] *}

### Es testen { #test-it }

Jetzt sollten Sie in der Lage sein, zu Ihrer Dokumentation auf <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> zu gehen und die Seite neu zu laden, die Assets werden nun vom neuen CDN geladen.

## JavaScript und CSS für die Dokumentation selbst hosten { #self-hosting-javascript-and-css-for-docs }

Das Selbst-Hosting von JavaScript und CSS kann nützlich sein, wenn Sie beispielsweise möchten, dass Ihre Anwendung auch offline, ohne bestehenden Internetzugang oder in einem lokalen Netzwerk weiter funktioniert.

Hier erfahren Sie, wie Sie diese Dateien selbst in derselben FastAPI-App bereitstellen und die Dokumentation für deren Verwendung konfigurieren.

### Projektdateistruktur { #project-file-structure }

Nehmen wir an, die Dateistruktur Ihres Projekts sieht folgendermaßen aus:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

Erstellen Sie jetzt ein Verzeichnis zum Speichern dieser statischen Dateien.

Ihre neue Dateistruktur könnte so aussehen:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### Die Dateien herunterladen { #download-the-files }

Laden Sie die für die Dokumentation benötigten statischen Dateien herunter und legen Sie diese im Verzeichnis `static/` ab.

Sie können wahrscheinlich mit der rechten Maustaste auf jeden Link klicken und eine Option wie etwa „Link speichern unter ...“ auswählen.

**Swagger UI** verwendet folgende Dateien:

* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js" class="external-link" target="_blank">`swagger-ui-bundle.js`</a>
* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" class="external-link" target="_blank">`swagger-ui.css`</a>

Und **ReDoc** verwendet diese Datei:

* <a href="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js" class="external-link" target="_blank">`redoc.standalone.js`</a>

Danach könnte Ihre Dateistruktur wie folgt aussehen:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static
    ├── redoc.standalone.js
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
```

### Die statischen Dateien bereitstellen { #serve-the-static-files }

* Importieren Sie `StaticFiles`.
* „Mounten“ Sie eine `StaticFiles()`-Instanz in einem bestimmten Pfad.

{* ../../docs_src/custom_docs_ui/tutorial002.py hl[7,11] *}

### Die statischen Dateien testen { #test-the-static-files }

Starten Sie Ihre Anwendung und gehen Sie auf <a href="http://127.0.0.1:8000/static/redoc.standalone.js" class="external-link" target="_blank">http://127.0.0.1:8000/static/redoc.standalone.js</a>.

Sie sollten eine sehr lange JavaScript-Datei für **ReDoc** sehen.

Sie könnte beginnen mit etwas wie:

```JavaScript
/*! For license information please see redoc.standalone.js.LICENSE.txt */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t(require("null")):
...
```

Das zeigt, dass Sie statische Dateien aus Ihrer Anwendung bereitstellen können und dass Sie die statischen Dateien für die Dokumentation an der richtigen Stelle platziert haben.

Jetzt können wir die Anwendung so konfigurieren, dass sie diese statischen Dateien für die Dokumentation verwendet.

### Die automatischen Dokumentationen für statische Dateien deaktivieren { #disable-the-automatic-docs-for-static-files }

Wie bei der Verwendung eines benutzerdefinierten CDN besteht der erste Schritt darin, die automatischen Dokumentationen zu deaktivieren, da diese standardmäßig das CDN verwenden.

Um sie zu deaktivieren, setzen Sie deren URLs beim Erstellen Ihrer `FastAPI`-App auf `None`:

{* ../../docs_src/custom_docs_ui/tutorial002.py hl[9] *}

### Die benutzerdefinierten Dokumentationen für statische Dateien hinzufügen { #include-the-custom-docs-for-static-files }

Und genau wie bei einem benutzerdefinierten CDN können Sie jetzt die *Pfadoperationen* für die benutzerdefinierten Dokumentationen erstellen.

Auch hier können Sie die internen Funktionen von FastAPI wiederverwenden, um die HTML-Seiten für die Dokumentationen zu erstellen und ihnen die erforderlichen Argumente zu übergeben:

* `openapi_url`: die URL, unter der die HTML-Seite für die Dokumentation das OpenAPI-Schema für Ihre API abrufen kann. Sie können hier das Attribut `app.openapi_url` verwenden.
* `title`: der Titel Ihrer API.
* `oauth2_redirect_url`: Sie können hier `app.swagger_ui_oauth2_redirect_url` verwenden, um die Standardeinstellung zu verwenden.
* `swagger_js_url`: die URL, unter welcher der HTML-Code für Ihre Swagger-UI-Dokumentation die **JavaScript**-Datei abrufen kann. **Das ist die, welche jetzt von Ihrer eigenen Anwendung bereitgestellt wird**.
* `swagger_css_url`: die URL, unter welcher der HTML-Code für Ihre Swagger-UI-Dokumentation die **CSS**-Datei abrufen kann. **Das ist die, welche jetzt von Ihrer eigenen Anwendung bereitgestellt wird**.

Und ähnlich für ReDoc ...

{* ../../docs_src/custom_docs_ui/tutorial002.py hl[2:6,14:22,25:27,30:36] *}

/// tip | Tipp

Die *Pfadoperation* für `swagger_ui_redirect` ist ein Hilfsmittel bei der Verwendung von OAuth2.

Wenn Sie Ihre API mit einem OAuth2-Anbieter integrieren, können Sie sich authentifizieren und mit den erworbenen Anmeldeinformationen zur API-Dokumentation zurückkehren. Und mit ihr interagieren, die echte OAuth2-Authentifizierung verwendend.

Swagger UI erledigt das hinter den Kulissen für Sie, benötigt aber diesen „Umleitungs“-Helfer.

///

### Eine *Pfadoperation* erstellen, um statische Dateien zu testen { #create-a-path-operation-to-test-static-files }

Um nun testen zu können, ob alles funktioniert, erstellen Sie eine *Pfadoperation*:

{* ../../docs_src/custom_docs_ui/tutorial002.py hl[39:41] *}

### Benutzeroberfläche mit statischen Dateien testen { #test-static-files-ui }

Jetzt sollten Sie in der Lage sein, Ihr WLAN zu trennen, gehen Sie zu Ihrer Dokumentation unter <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> und laden Sie die Seite neu.

Und selbst ohne Internet können Sie die Dokumentation für Ihre API sehen und mit ihr interagieren.
