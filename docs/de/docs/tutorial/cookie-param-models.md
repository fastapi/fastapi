# Cookie-Parameter-Modelle { #cookie-parameter-models }

Wenn Sie eine Gruppe von **Cookies** haben, die zusammengehören, können Sie ein **Pydantic-Modell** erstellen, um diese zu deklarieren. 🍪

Damit können Sie das Modell an **mehreren Stellen wiederverwenden** und auch Validierungen und Metadaten für alle Parameter gleichzeitig deklarieren. 😎

/// note | Hinweis

Dies wird seit FastAPI Version `0.115.0` unterstützt. 🤓

///

/// tip | Tipp

Diese gleiche Technik gilt für `Query`, `Cookie` und `Header`. 😎

///

## Cookies mit einem Pydantic-Modell { #cookies-with-a-pydantic-model }

Deklarieren Sie die **Cookie**-Parameter, die Sie benötigen, in einem **Pydantic-Modell**, und deklarieren Sie dann den Parameter als `Cookie`:

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI** wird die Daten für **jedes Feld** aus den im <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> empfangenen **Cookies** **extrahieren** und Ihnen das von Ihnen definierte Pydantic-Modell bereitstellen.

## Die Dokumentation testen { #check-the-docs }

Sie können die definierten Cookies in der Dokumentationsoberfläche unter `/docs` sehen:

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// info | Info

Bitte beachten Sie, dass Browser Cookies auf spezielle Weise und im Hintergrund bearbeiten, sodass sie **nicht** leicht **JavaScript** erlauben, diese zu berühren.

Wenn Sie zur **API-Dokumentationsoberfläche** unter `/docs` gehen, können Sie die **Dokumentation** für Cookies für Ihre *Pfadoperationen* sehen.

Aber selbst wenn Sie die **Daten ausfüllen** und auf „Ausführen“ klicken, werden aufgrund der Tatsache, dass die Dokumentationsoberfläche mit **JavaScript** arbeitet, die Cookies nicht gesendet, und Sie werden eine **Fehlermeldung** sehen, als ob Sie keine Werte eingegeben hätten.

///

## Zusätzliche Cookies verbieten { #forbid-extra-cookies }

In einigen speziellen Anwendungsfällen (wahrscheinlich nicht sehr häufig) möchten Sie möglicherweise die Cookies, die Sie empfangen möchten, **einschränken**.

Ihre API hat jetzt die Macht, ihre eigene <abbr title="Das ist ein Scherz, nur für den Fall. Es hat nichts mit Cookie-Einwilligungen zu tun, aber es ist witzig, dass selbst die API jetzt die armen Cookies ablehnen kann. Haben Sie einen Keks. 🍪">Cookie-Einwilligung</abbr> zu kontrollieren. 🤪🍪

Sie können die Modellkonfiguration von Pydantic verwenden, um `extra` Felder zu verbieten (`forbid`):

{* ../../docs_src/cookie_param_models/tutorial002_an_py39.py hl[10] *}

Wenn ein Client versucht, einige **zusätzliche Cookies** zu senden, erhält er eine **Error-<abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr>**.

Arme Cookie-Banner, wie sie sich mühen, Ihre Einwilligung zu erhalten, dass die <abbr title="Das ist ein weiterer Scherz. Beachten Sie mich nicht. Trinken Sie einen Kaffee zu Ihrem Keks. ☕">API sie ablehnen darf</abbr>. 🍪

Wenn der Client beispielsweise versucht, ein `santa_tracker`-Cookie mit einem Wert von `good-list-please` zu senden, erhält der Client eine **Error-Response**, die ihm mitteilt, dass das `santa_tracker` <abbr title="Santa beschwert sich über den Mangel an Cookies. 🎅 Okay, keine Cookie-Witze mehr.">Cookie nicht erlaubt ist</abbr>:

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

## Zusammenfassung { #summary }

Sie können **Pydantic-Modelle** verwenden, um <abbr title="Nehmen Sie einen letzten Keks, bevor Sie gehen. 🍪">**Cookies**</abbr> in **FastAPI** zu deklarieren. 😎
