# Templates

Sie können jede gewünschte Template-Engine mit **FastAPI** verwenden.

Eine häufige Wahl ist Jinja2, dasselbe, was auch von Flask und anderen Tools verwendet wird.

Es gibt Werkzeuge zur einfachen Konfiguration, die Sie direkt in Ihrer **FastAPI**-Anwendung verwenden können (bereitgestellt von Starlette).

## Abhängigkeiten installieren

Installieren Sie `jinja2`:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## Verwendung von `Jinja2Templates`

* Importieren Sie `Jinja2Templates`.
* Erstellen Sie ein `templates`-Objekt, das Sie später wiederverwenden können.
* Deklarieren Sie einen `Request`-Parameter in der *Pfadoperation*, welcher ein Template zurückgibt.
* Verwenden Sie die von Ihnen erstellten `templates`, um eine `TemplateResponse` zu rendern und zurückzugeben, übergeben Sie den Namen des Templates, das Requestobjekt und ein „Kontext“-Dictionary mit Schlüssel-Wert-Paaren, die innerhalb des Jinja2-Templates verwendet werden sollen.

```Python hl_lines="4  11  15-18"
{!../../../docs_src/templates/tutorial001.py!}
```

/// note | "Hinweis"

Vor FastAPI 0.108.0 und Starlette 0.29.0 war `name` der erste Parameter.

Außerdem wurde in früheren Versionen das `request`-Objekt als Teil der Schlüssel-Wert-Paare im Kontext für Jinja2 übergeben.

///

/// tip | "Tipp"

Durch die Deklaration von `response_class=HTMLResponse` kann die Dokumentationsoberfläche erkennen, dass die Response HTML sein wird.

///

/// note | "Technische Details"

Sie können auch `from starlette.templating import Jinja2Templates` verwenden.

**FastAPI** bietet dasselbe `starlette.templating` auch via `fastapi.templating` an, als Annehmlichkeit für Sie, den Entwickler. Es kommt aber direkt von Starlette. Das Gleiche gilt für `Request` und `StaticFiles`.

///

## Templates erstellen

Dann können Sie unter `templates/item.html` ein Template erstellen, mit z. B. folgendem Inhalt:

```jinja hl_lines="7"
{!../../../docs_src/templates/templates/item.html!}
```

### Template-Kontextwerte

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

### Template-`url_for`-Argumente

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

## Templates und statische Dateien

Sie können `url_for()` innerhalb des Templates auch beispielsweise mit den `StaticFiles` verwenden, die Sie mit `name="static"` gemountet haben.

```jinja hl_lines="4"
{!../../../docs_src/templates/templates/item.html!}
```

In diesem Beispiel würde das zu einer CSS-Datei unter `static/styles.css` verlinken, mit folgendem Inhalt:

```CSS hl_lines="4"
{!../../../docs_src/templates/static/styles.css!}
```

Und da Sie `StaticFiles` verwenden, wird diese CSS-Datei automatisch von Ihrer **FastAPI**-Anwendung unter der URL `/static/styles.css` bereitgestellt.

## Mehr Details

Weitere Informationen, einschließlich, wie man Templates testet, finden Sie in der <a href="https://www.starlette.io/templates/" class="external-link" target="_blank">Starlette Dokumentation zu Templates</a>.
