# Statische Dateien { #static-files }

Mit `StaticFiles` können Sie statische Dateien aus einem Verzeichnis automatisch bereitstellen.

## `StaticFiles` verwenden { #use-staticfiles }

* Importieren Sie `StaticFiles`.
* „Mounten“ Sie eine `StaticFiles()`-Instanz in einem bestimmten Pfad.

{* ../../docs_src/static_files/tutorial001.py hl[2,6] *}

/// note | Technische Details

Sie könnten auch `from starlette.staticfiles import StaticFiles` verwenden.

**FastAPI** stellt dasselbe `starlette.staticfiles` auch via `fastapi.staticfiles` bereit, als Annehmlichkeit für Sie, den Entwickler. Es kommt aber tatsächlich direkt von Starlette.

///

### Was ist „Mounten“ { #what-is-mounting }

„Mounten“ bedeutet das Hinzufügen einer vollständigen „unabhängigen“ Anwendung an einem bestimmten Pfad, die sich dann um die Handhabung aller Unterpfade kümmert.

Dies unterscheidet sich von der Verwendung eines `APIRouter`, da eine gemountete Anwendung völlig unabhängig ist. Die OpenAPI und Dokumentation Ihrer Hauptanwendung enthalten nichts von der gemounteten Anwendung, usw.

Weitere Informationen hierzu finden Sie im [Handbuch für fortgeschrittene Benutzer](../advanced/index.md){.internal-link target=_blank}.

## Einzelheiten { #details }

Das erste `"/static"` bezieht sich auf den Unterpfad, auf dem diese „Unteranwendung“ „gemountet“ wird. Daher wird jeder Pfad, der mit `"/static"` beginnt, von ihr verarbeitet.

Das `directory="static"` bezieht sich auf den Namen des Verzeichnisses, das Ihre statischen Dateien enthält.

Das `name="static"` gibt dieser Unteranwendung einen Namen, der intern von **FastAPI** verwendet werden kann.

Alle diese Parameter können anders als „`static`“ lauten, passen Sie sie an die Bedürfnisse und spezifischen Details Ihrer eigenen Anwendung an.

## Weitere Informationen { #more-info }

Weitere Details und Optionen finden Sie in der <a href="https://www.starlette.dev/staticfiles/" class="external-link" target="_blank">Dokumentation von Starlette zu statischen Dateien</a>.
