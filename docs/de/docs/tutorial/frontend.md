# Frontend { #frontend }

Sie können statische Frontend-Apps mit `app.frontend()` (oder `router.frontend()`) bereitstellen.

Das ist nützlich für Frontend-Tools, die statische Dateien generieren, wie React mit Vite, TanStack Router, Astro, Vue, Svelte, Angular, Solid und andere.

Mit diesen Tools haben Sie normalerweise einen Schritt, der das Frontend baut, mit einem Befehl wie:

```bash
npm run build
```

Das würde ein Verzeichnis wie `./dist/` mit Ihren Frontend-Dateien generieren.

Sie können `app.frontend()` verwenden, um dieses Verzeichnis gemäß den Konventionen bereitzustellen, die von diesen Frontend-Frameworks benötigt werden.

**FastAPI** prüft zuerst *Pfadoperationen*. Die Frontend-Dateien werden nur geprüft, wenn keine normale Route gepasst hat, sodass Ihre API nicht beeinträchtigt wird.

## Ein Frontend bereitstellen { #serve-a-frontend }

Nachdem Sie Ihr Frontend gebaut haben, zum Beispiel mit `npm run build`, legen Sie die generierten Dateien in ein Verzeichnis, zum Beispiel `dist`.

Ihre Projektstruktur könnte so aussehen:

```text
.
├── pyproject.toml
├── app
│   ├── __init__.py
│   └── main.py
└── dist
    ├── index.html
    └── assets
        └── app.js
```

Stellen Sie es dann mit `app.frontend()` bereit:

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

Damit kann ein Request für `/assets/app.js` `dist/assets/app.js` ausliefern.

Wenn Sie außerdem eine **FastAPI**-*Pfadoperation* haben, gewinnt die *Pfadoperation*.

## Clientseitiges Routing { #client-side-routing }

Viele Frontend-Apps, einschließlich **Single-Page-Apps** (SPAs), verwenden clientseitiges Routing. Ein Pfad wie `/dashboard/settings` ist möglicherweise keine echte Datei, aber das Framework würde sich darum kümmern, ihn zu handhaben.

Wenn also direkt auf diese URL zugegriffen wird (statt durch die App zu navigieren), sollte das Backend die Frontend-App von `index.html` bereitstellen, sodass das Frontend-Framework anschließend das clientseitige Routing handhaben kann.

Verwenden Sie dafür `fallback="index.html"`:

{* ../../docs_src/frontend/tutorial002_py310.py hl[5] *}

**FastAPI** verwendet diesen Fallback nur für `GET`- und `HEAD`-Requests, die wie Browser-Navigation aussehen. Fehlende Dateien wie JavaScript, CSS und Bilder geben weiterhin `404` zurück.

Requests mit anderen Methoden, wie `POST` oder `PUT`, an Pfade, die nur zum Frontend-Fallback passen, geben ebenfalls `404` zurück. Reguläre **FastAPI**-*Pfadoperationen* haben weiterhin eine höhere Priorität als Frontend-Routen.

/// tip | Tipp

Standardmäßig hat `fallback` einen Wert von `fallback="auto"`. In den meisten Fällen müssen Sie `fallback` nicht angeben. Lesen Sie weiter unten die Details.

///

Das ist das, was Sie bei vielen Frontend-Apps möchten, die clientseitiges Routing verwenden, zum Beispiel React mit TanStack Router, Vue, Angular, SvelteKit oder Solid.

## Benutzerdefinierte 404-Seite { #custom-404-page }

Sie können auch eine statische `404.html`-Seite für fehlende Frontend-Pfade ausliefern:

{* ../../docs_src/frontend/tutorial003_py310.py hl[5] *}

Diese Response behält einen Statuscode von `404`.

In diesem Fall liefert **FastAPI** für fehlende Frontend-Pfade nicht `index.html` aus. Stattdessen wird die Datei `404.html` zurückgegeben.

/// tip | Tipp

Standardmäßig hat `fallback` einen Wert von `fallback="auto"`. Damit wird, wenn eine `404.html`-Datei gefunden wird, diese automatisch als Fallback verwendet.

Sie können das `fallback`-Argument also normalerweise weglassen.

///

Das ist nützlich bei Frontend-Tools, die für jede Seite statische HTML-Dateien generieren, wie Astro.

## Automatischer Fallback { #fallback-auto }

Standardmäßig verwendet `app.frontend()` `fallback="auto"`.

Wenn es im Frontend-Verzeichnis eine `404.html`-Datei gibt, liefern fehlende Frontend-Pfade diese Datei mit dem Statuscode `404` aus.

Andernfalls, wenn es eine `index.html`-Datei gibt, liefern fehlende Browser-Navigationspfade `index.html` aus, was viele Frontend-Apps mit clientseitigem Routing erwarten.

In den meisten Fällen können Sie also `app.frontend("/", directory="dist")` verwenden, ohne das `fallback`-Argument anzugeben.

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

## Fallback deaktivieren { #disable-fallback }

Wenn Sie keine Fallback-Datei für fehlende Frontend-Pfade ausliefern möchten, verwenden Sie `fallback=None`:

{* ../../docs_src/frontend/tutorial005_py310.py hl[5] *}

Dann geben fehlende Frontend-Pfade das normale `404` zurück.

## Verzeichnis prüfen { #check-directory }

Standardmäßig prüft `app.frontend()`, dass das Verzeichnis existiert, wenn die App erstellt wird.

Das hilft, Konfigurationsfehler früh zu erkennen. Wenn zum Beispiel das Output-Verzeichnis des Frontend-Builds fehlt, löst **FastAPI** beim Startup einen Fehler aus.

Wenn Ihre Frontend-Dateien später erstellt werden, zum Beispiel durch einen separaten Build-Schritt, nachdem das App-Objekt erstellt wurde, setzen Sie `check_dir=False`:

{* ../../docs_src/frontend/tutorial006_py310.py hl[5] *}

Mit `check_dir=False` prüft **FastAPI** das Verzeichnis nicht, wenn die App erstellt wird. Wenn das konfigurierte Verzeichnis beim Verarbeiten eines Requests immer noch fehlt, löst **FastAPI** dann einen Fehler aus.

## Mit `APIRouter` verwenden { #use-it-with-apirouter }

Sie können Frontend-Dateien auch zu einem `APIRouter` hinzufügen und ihn mit einem Präfix einbinden:

{* ../../docs_src/frontend/tutorial004_py310.py hl[6,7] *}

In diesem Beispiel werden Frontend-Pfade unter `/app` bereitgestellt.

Alle regulären *Pfadoperationen* in der App haben weiterhin Vorrang, auch in anderen Routern.

## Nur statischer Build-Output { #static-build-output-only }

`app.frontend()` liefert Dateien aus, die bereits von Ihrem Frontend-Build generiert wurden.

Es führt kein serverseitiges Rendering aus. Es ist für Frontend-Frameworks gedacht, die statische Dateien generieren, nicht für Frameworks, die dynamisches Rendering auf dem Server für jeden Request benötigen.
