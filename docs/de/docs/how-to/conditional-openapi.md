# Bedingte OpenAPI { #conditional-openapi }

Bei Bedarf können Sie OpenAPI mithilfe von Einstellungen und Umgebungsvariablen abhängig von der Umgebung bedingt konfigurieren und sogar vollständig deaktivieren.

## Über Sicherheit, APIs und Dokumentation { #about-security-apis-and-docs }

Das Verstecken Ihrer Dokumentationsoberflächen in der Produktion *sollte nicht* die Methode sein, Ihre API zu schützen.

Dadurch wird Ihrer API keine zusätzliche Sicherheit hinzugefügt, die *Pfadoperationen* sind weiterhin dort verfügbar, wo sie sich befinden.

Wenn Ihr Code eine Sicherheitslücke aufweist, ist diese weiterhin vorhanden.

Das Verstecken der Dokumentation macht es nur schwieriger zu verstehen, wie mit Ihrer API interagiert werden kann, und könnte es auch schwieriger machen, diese in der Produktion zu debuggen. Man könnte es einfach als eine Form von <a href="https://en.wikipedia.org/wiki/Security_through_obscurity" class="external-link" target="_blank">Sicherheit durch Verschleierung</a> betrachten.

Wenn Sie Ihre API sichern möchten, gibt es mehrere bessere Dinge, die Sie tun können, zum Beispiel:

* Stellen Sie sicher, dass Sie über gut definierte Pydantic-Modelle für Ihre <abbr title="Anfragekörper">Requestbodys</abbr> und <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Responses</abbr> verfügen.
* Konfigurieren Sie alle erforderlichen Berechtigungen und Rollen mithilfe von Abhängigkeiten.
* Speichern Sie niemals Klartext-Passwörter, sondern nur Passwort-Hashes.
* Implementieren und verwenden Sie gängige kryptografische Tools wie pwdlib und JWT-Tokens, usw.
* Fügen Sie bei Bedarf detailliertere Berechtigungskontrollen mit OAuth2-Scopes hinzu.
* ... usw.

Dennoch kann es sein, dass Sie einen ganz bestimmten Anwendungsfall haben, bei dem Sie die API-Dokumentation für eine bestimmte Umgebung (z. B. für die Produktion) oder abhängig von Konfigurationen aus Umgebungsvariablen wirklich deaktivieren müssen.

## Bedingte OpenAPI aus Einstellungen und Umgebungsvariablen { #conditional-openapi-from-settings-and-env-vars }

Sie können problemlos dieselben Pydantic-Einstellungen verwenden, um Ihre generierte OpenAPI und die Dokumentationsoberflächen zu konfigurieren.

Zum Beispiel:

{* ../../docs_src/conditional_openapi/tutorial001.py hl[6,11] *}

Hier deklarieren wir die Einstellung `openapi_url` mit dem gleichen Defaultwert `"/openapi.json"`.

Und dann verwenden wir es beim Erstellen der `FastAPI`-App.

Dann könnten Sie OpenAPI (einschließlich der Dokumentationsoberflächen) deaktivieren, indem Sie die Umgebungsvariable `OPENAPI_URL` auf einen leeren String setzen, wie zum Beispiel:

<div class="termy">

```console
$ OPENAPI_URL= uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Wenn Sie dann zu den URLs unter `/openapi.json`, `/docs` oder `/redoc` gehen, erhalten Sie lediglich einen `404 Not Found`-Fehler, wie:

```JSON
{
    "detail": "Not Found"
}
```
