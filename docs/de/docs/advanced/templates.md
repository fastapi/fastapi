# Templates { #templates }

Sie können jede gewünschte Template-Engine mit **FastAPI** verwenden.

Eine häufige Wahl ist Jinja2, dasselbe, was auch von Flask und anderen Tools verwendet wird.

Es gibt Werkzeuge zur einfachen Konfiguration, die Sie direkt in Ihrer **FastAPI**-Anwendung verwenden können (bereitgestellt von Starlette).

## Abhängigkeiten installieren { #install-dependencies }

Stellen Sie sicher, dass Sie eine [virtuelle Umgebung](../virtual-environments.md){.internal-link target=_blank} erstellen, sie aktivieren und `jinja2` installieren:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## `Jinja2Templates` verwenden { #using-jinja2templates }

* Importieren Sie `Jinja2Templates`.
* Erstellen Sie ein `templates`-Objekt, das Sie später wiederverwenden können.
* Deklarieren Sie einen `<abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr>`-Parameter in der *Pfadoperation*, welcher ein Template zurückgibt.
* Verwenden Sie die von Ihnen erstellten `templates`, um eine `TemplateResponse` zu rendern und zurückzugeben, übergeben Sie den Namen des Templates, das Requestobjekt und ein „Kontext“-<abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">Dictionary</abbr> mit Schlüssel-Wert-Paaren, die innerhalb des Jinja2-Templates verwendet werden sollen.

{* ../../docs_src/templates/tutorial001.py hl[4,11,15:18] *}

/// note | Hinweis

Vor FastAPI 0.108.0 und Starlette 0.29.0 war `name` der erste Parameter.

Außerdem wurde in früheren Versionen das `request`-Objekt als Teil der Schlüssel-Wert-Paare im Kontext für Jinja2 übergeben.

///

/// tip | Tipp

Durch die Deklaration von `response_class=HTMLResponse` kann die Dokumentationsoberfläche erkennen, dass die <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> HTML sein wird.

///

/// note | Technische Details

Sie können auch `from starlette.templating import Jinja2Templates` verwenden.

**FastAPI** bietet dasselbe `starlette.templating` auch via `fastapi.templating` an, als Annehmlichkeit für Sie, den Entwickler. Aber die meisten der verfügbaren Responses kommen direkt von Starlette. Das Gleiche gilt für `Request` und `StaticFiles`.

///

## Templates erstellen { #writing-templates }

Dann können Sie unter `templates/item.html` ein Template erstellen, mit z. B. folgendem Inhalt:

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### Template-Kontextwerte { #template-context-values }

Im HTML, welches enthält:

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

... wird die `id` angezeigt, welche dem „Kontext“-`dict` entnommen wird, welches Sie übergeben haben:

```Python
{"id": id}
```

Mit beispielsweise einer ID `42` würde das wie folgt gerendert werden:

```html
Item ID: 42
```

### Template-`url_for`-Argumente { #template-url-for-arguments }

Sie können `url_for()` auch innerhalb des Templates verwenden, es nimmt als Argumente dieselben Argumente, die von Ihrer *Pfadoperation-Funktion* verwendet werden.

Der Abschnitt mit:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

... generiert also einen Link zu derselben URL, welche von der *Pfadoperation-Funktion* `read_item(id=id)` gehandhabt werden würde.

Mit beispielsweise der ID `42` würde dies Folgendes ergeben:

```html
<a href="/items/42">
```

## Templates und statische Dateien { #templates-and-static-files }

Sie können `url_for()` innerhalb des Templates auch beispielsweise mit den `StaticFiles` verwenden, die Sie mit `name="static"` gemountet haben.

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

In diesem Beispiel würde das zu einer CSS-Datei unter `static/styles.css` verlinken, mit folgendem Inhalt:

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

Und da Sie `StaticFiles` verwenden, wird diese CSS-Datei automatisch von Ihrer **FastAPI**-Anwendung unter der URL `/static/styles.css` ausgeliefert.

## Mehr Details { #more-details }

Weitere Informationen, einschließlich, wie man Templates testet, finden Sie in <a href="https://www.starlette.dev/templates/" class="external-link" target="_blank">Starlettes Dokumentation zu Templates</a>.
