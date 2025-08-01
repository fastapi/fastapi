# Cookie-Parameter-Modelle

Wenn Sie eine Gruppe von **Cookies** haben, die zusammengehören, können Sie ein **Pydantic-Modell** erstellen, um sie zu deklarieren. 🍪

Dies ermöglicht es Ihnen, das **Modell** an **mehreren Stellen wiederzuverwenden** und auch Validierungen und Metadaten für alle Parameter auf einmal zu deklarieren. 😎

/// note | Hinweis

Dies wird seit der FastAPI-Version `0.115.0` unterstützt. 🤓

///

/// tip | Tipp

Diese Technik funktioniert genauso für `Query`, `Cookie` und `Header`. 😎

///

## Cookies mit einem Pydantic-Modell

Deklarieren Sie die benötigten **Cookie**-Parameter in einem **Pydantic-Modell**, und deklarieren Sie dann den Parameter als `Cookie`:

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI** wird die Daten für **jedes Feld** aus den in der Anfrage erhaltenen **Cookies** extrahieren und Ihnen das von Ihnen definierte Pydantic-Modell bereitstellen.

## Überprüfen Sie die Dokumentation

Sie können die definierten Cookies in der Docs-Oberfläche unter `/docs` sehen:

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// info | Hinweis

Berücksichtigen Sie, dass **Browser Cookies** auf spezielle Weise und im Hintergrund handhaben und sie **JavaScript** nicht leicht erlauben, diese zu berühren.

Wenn Sie zur **API-Dokumentations-Oberfläche** unter `/docs` gehen, können Sie die **Dokumentation** für Cookies für Ihre *Pfadoperationen* sehen.

Aber selbst wenn Sie die **Daten ausfüllen** und auf "Ausführen" klicken, werden die Cookies nicht gesendet, da die Docs-Oberfläche mit **JavaScript** arbeitet, und Sie erhalten eine **Fehlermeldung**, als ob Sie keine Werte eingegeben hätten.

///

## Zusätzliche Cookies verbieten

In einigen speziellen Anwendungsfällen (vermutlich nicht sehr häufig) möchten Sie möglicherweise die Cookies, die Sie erhalten möchten, **einschränken**.

Ihre API hat jetzt die Macht, ihre eigene <abbr title="Das ist ein Scherz, nur für den Fall. Es hat nichts mit Cookie-Zustimmungen zu tun, aber es ist witzig, dass selbst die API die armen Cookies jetzt ablehnen kann. Haben Sie einen Cookie. 🍪">Cookie-Zustimmung</abbr> zu kontrollieren. 🤪🍪

Sie können die Modellkonfiguration von Pydantic verwenden, um alle `extra` Felder zu `verbieten`:

{* ../../docs_src/cookie_param_models/tutorial002_an_py39.py hl[10] *}

Wenn ein Client versucht, einige **zusätzliche Cookies** zu senden, erhält er eine **Error-Response**.

Arme Cookie-Banner mit all ihrer Mühe, Ihre Zustimmung für die <abbr title="Das ist ein weiterer Scherz. Achtung: Nehmen Sie mich nicht zu ernst. Haben Sie einen Kaffee zu Ihrem Cookie. ☕">API zu bekommen, um sie abzulehnen</abbr>. 🍪

Wenn der Client beispielsweise versucht, ein `santa_tracker`-Cookie mit dem Wert `good-list-please` zu senden, erhält der Client eine **Error-Response**, die ihm mitteilt, dass das `santa_tracker`-<abbr title="Santa lehnt den Mangel an Cookies ab. 🎅 Okay, keine Cookie-Witze mehr.">Cookie nicht erlaubt</abbr> ist:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
```

## Zusammenfassung

Sie können **Pydantic-Modelle** verwenden, um <abbr title="Nehmen Sie sich einen letzten Cookie, bevor Sie gehen. 🍪">**Cookies**</abbr> in **FastAPI** zu deklarieren. 😎
