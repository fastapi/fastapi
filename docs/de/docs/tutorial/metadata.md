# Metadaten und URLs der Dokumentationen

Sie können mehrere Metadaten-Einstellungen für Ihre **FastAPI**-Anwendung konfigurieren.

## Metadaten für die API

Sie können die folgenden Felder festlegen, welche in der OpenAPI-Spezifikation und den Benutzeroberflächen der automatischen API-Dokumentation verwendet werden:

| Parameter | Typ | Beschreibung |
|------------|------|-------------|
| `title` | `str` | Der Titel der API. |
| `summary` | `str` | Eine kurze Zusammenfassung der API. <small>Verfügbar seit OpenAPI 3.1.0, FastAPI 0.99.0.</small> |
| `description` | `str` | Eine kurze Beschreibung der API. Kann Markdown verwenden. |
| `version` | `string` | Die Version der API. Das ist die Version Ihrer eigenen Anwendung, nicht die von OpenAPI. Zum Beispiel `2.5.0`. |
| `terms_of_service` | `str` | Eine URL zu den Nutzungsbedingungen für die API. Falls angegeben, muss es sich um eine URL handeln. |
| `contact` | `dict` | Die Kontaktinformationen für die verfügbar gemachte API. Kann mehrere Felder enthalten. <details><summary><code>contact</code>-Felder</summary><table><thead><tr><th>Parameter</th><th>Typ</th><th>Beschreibung</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>Der identifizierende Name der Kontaktperson/Organisation.</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>Die URL, die auf die Kontaktinformationen verweist. MUSS im Format einer URL vorliegen.</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>Die E-Mail-Adresse der Kontaktperson/Organisation. MUSS im Format einer E-Mail-Adresse vorliegen.</td></tr></tbody></table></details> |
| `license_info` | `dict` | Die Lizenzinformationen für die verfügbar gemachte API. Kann mehrere Felder enthalten. <details><summary><code>license_info</code>-Felder</summary><table><thead><tr><th>Parameter</th><th>Typ</th><th>Beschreibung</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>ERFORDERLICH</strong> (wenn eine <code>license_info</code> festgelegt ist). Der für die API verwendete Lizenzname.</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>Ein <a href="https://spdx.org/licenses/" class="external-link" target="_blank">SPDX</a>-Lizenzausdruck für die API. Das Feld <code>identifier</code> und das Feld <code>url</code> schließen sich gegenseitig aus. <small>Verfügbar seit OpenAPI 3.1.0, FastAPI 0.99.0.</small></td></tr><tr><td><code>url</code></td><td><code >str</code></td><td>Eine URL zur Lizenz, die für die API verwendet wird. MUSS im Format einer URL vorliegen.</td></tr></tbody></table></details> |

Sie können diese wie folgt setzen:

```Python hl_lines="3-16  19-32"
{!../../../docs_src/metadata/tutorial001.py!}
```

/// tip | "Tipp"

Sie können Markdown in das Feld `description` schreiben und es wird in der Ausgabe gerendert.

///

Mit dieser Konfiguration würde die automatische API-Dokumentation wie folgt aussehen:

<img src="/img/tutorial/metadata/image01.png">

## Lizenz-ID

Seit OpenAPI 3.1.0 und FastAPI 0.99.0 können Sie die `license_info` auch mit einem `identifier` anstelle einer `url` festlegen.

Zum Beispiel:

```Python hl_lines="31"
{!../../../docs_src/metadata/tutorial001_1.py!}
```

## Metadaten für Tags

Sie können mit dem Parameter `openapi_tags` auch zusätzliche Metadaten für die verschiedenen Tags hinzufügen, die zum Gruppieren Ihrer Pfadoperationen verwendet werden.

Es wird eine Liste benötigt, die für jedes Tag ein Dict enthält.

Jedes Dict kann Folgendes enthalten:

* `name` (**erforderlich**): ein `str` mit demselben Tag-Namen, den Sie im Parameter `tags` in Ihren *Pfadoperationen* und `APIRouter`n verwenden.
* `description`: ein `str` mit einer kurzen Beschreibung für das Tag. Sie kann Markdown enthalten und wird in der Benutzeroberfläche der Dokumentation angezeigt.
* `externalDocs`: ein `dict`, das externe Dokumentation beschreibt mit:
     * `description`: ein `str` mit einer kurzen Beschreibung für die externe Dokumentation.
     * `url` (**erforderlich**): ein `str` mit der URL für die externe Dokumentation.

### Metadaten für Tags erstellen

Versuchen wir das an einem Beispiel mit Tags für `users` und `items`.

Erstellen Sie Metadaten für Ihre Tags und übergeben Sie sie an den Parameter `openapi_tags`:

```Python hl_lines="3-16  18"
{!../../../docs_src/metadata/tutorial004.py!}
```

Beachten Sie, dass Sie Markdown in den Beschreibungen verwenden können. Beispielsweise wird „login“ in Fettschrift (**login**) und „fancy“ in Kursivschrift (_fancy_) angezeigt.

/// tip | "Tipp"

Sie müssen nicht für alle von Ihnen verwendeten Tags Metadaten hinzufügen.

///

### Ihre Tags verwenden

Verwenden Sie den Parameter `tags` mit Ihren *Pfadoperationen* (und `APIRouter`n), um diese verschiedenen Tags zuzuweisen:

```Python hl_lines="21  26"
{!../../../docs_src/metadata/tutorial004.py!}
```

/// info

Lesen Sie mehr zu Tags unter [Pfadoperation-Konfiguration](path-operation-configuration.md#tags){.internal-link target=_blank}.

///

### Die Dokumentation anschauen

Wenn Sie nun die Dokumentation ansehen, werden dort alle zusätzlichen Metadaten angezeigt:

<img src="/img/tutorial/metadata/image02.png">

### Reihenfolge der Tags

Die Reihenfolge der Tag-Metadaten-Dicts definiert auch die Reihenfolge, in der diese in der Benutzeroberfläche der Dokumentation angezeigt werden.

Auch wenn beispielsweise `users` im Alphabet nach `items` kommt, wird es vor diesen angezeigt, da wir seine Metadaten als erstes Dict der Liste hinzugefügt haben.

## OpenAPI-URL

Standardmäßig wird das OpenAPI-Schema unter `/openapi.json` bereitgestellt.

Sie können das aber mit dem Parameter `openapi_url` konfigurieren.

Um beispielsweise festzulegen, dass es unter `/api/v1/openapi.json` bereitgestellt wird:

```Python hl_lines="3"
{!../../../docs_src/metadata/tutorial002.py!}
```

Wenn Sie das OpenAPI-Schema vollständig deaktivieren möchten, können Sie `openapi_url=None` festlegen, wodurch auch die Dokumentationsbenutzeroberflächen deaktiviert werden, die es verwenden.

## URLs der Dokumentationen

Sie können die beiden enthaltenen Dokumentationsbenutzeroberflächen konfigurieren:

* **Swagger UI**: bereitgestellt unter `/docs`.
     * Sie können deren URL mit dem Parameter `docs_url` festlegen.
     * Sie können sie deaktivieren, indem Sie `docs_url=None` festlegen.
* **ReDoc**: bereitgestellt unter `/redoc`.
     * Sie können deren URL mit dem Parameter `redoc_url` festlegen.
     * Sie können sie deaktivieren, indem Sie `redoc_url=None` festlegen.

Um beispielsweise Swagger UI so einzustellen, dass sie unter `/documentation` bereitgestellt wird, und ReDoc zu deaktivieren:

```Python hl_lines="3"
{!../../../docs_src/metadata/tutorial003.py!}
```
