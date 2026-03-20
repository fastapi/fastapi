# Strikte Content-Type-Prüfung { #strict-content-type-checking }

Standardmäßig verwendet **FastAPI** eine strikte Prüfung des `Content-Type`-Headers für JSON-Requestbodys. Das bedeutet, dass JSON-Requests einen gültigen `Content-Type`-Header (z. B. `application/json`) enthalten MÜSSEN, damit der Body als JSON geparst wird.

## CSRF-Risiko { #csrf-risk }

Dieses Standardverhalten schützt vor einer Klasse von **Cross-Site Request Forgery (CSRF)**-Angriffen in einem sehr spezifischen Szenario.

Diese Angriffe nutzen aus, dass Browser Skripte Requests senden lassen, ohne einen CORS-Preflight-Check durchzuführen, wenn sie:

* keinen `Content-Type`-Header haben (z. B. mit `fetch()` und einem `Blob`-Body)
* und keine Authentifizierungsdaten senden.

Diese Art von Angriff ist vor allem relevant, wenn:

* die Anwendung lokal läuft (z. B. auf `localhost`) oder in einem internen Netzwerk
* und die Anwendung keine Authentifizierung hat, sondern erwartet, dass jeder Request aus demselben Netzwerk vertrauenswürdig ist.

## Beispielangriff { #example-attack }

Stellen Sie sich vor, Sie bauen eine Möglichkeit, lokal einen KI-Agenten auszuführen.

Er stellt eine API bereit unter

```
http://localhost:8000/v1/agents/multivac
```

Es gibt auch ein Frontend unter

```
http://localhost:8000
```

/// tip | Tipp

Beachten Sie, dass beide denselben Host haben.

///

Dann können Sie über das Frontend den KI-Agenten Dinge in Ihrem Namen erledigen lassen.

Da er **lokal** läuft und nicht im offenen Internet, entscheiden Sie sich, **keine Authentifizierung** einzurichten und vertrauen stattdessen einfach auf den Zugriff im lokalen Netzwerk.

Dann könnte einer Ihrer Benutzer es installieren und lokal ausführen.

Anschließend könnte er eine bösartige Website öffnen, z. B. so etwas wie

```
https://evilhackers.example.com
```

Und diese bösartige Website sendet Requests mit `fetch()` und einem `Blob`-Body an die lokale API unter

```
http://localhost:8000/v1/agents/multivac
```

Obwohl der Host der bösartigen Website und der lokalen App unterschiedlich ist, löst der Browser keinen CORS-Preflight-Request aus, weil:

* sie ohne Authentifizierung läuft, es müssen keine Credentials gesendet werden.
* der Browser annimmt, dass kein JSON gesendet wird (wegen des fehlenden `Content-Type`-Headers).

Dann könnte die bösartige Website den lokalen KI-Agenten dazu bringen, wütende Nachrichten an den Ex-Chef des Benutzers zu schicken ... oder Schlimmeres. 😅

## Offenes Internet { #open-internet }

Wenn Ihre App im offenen Internet läuft, würden Sie nicht „dem Netzwerk vertrauen“ und jedem erlauben, privilegierte Requests ohne Authentifizierung zu senden.

Angreifer könnten einfach ein Skript ausführen, um Requests an Ihre API zu senden, es ist keine Browserinteraktion nötig. Daher sichern Sie wahrscheinlich schon alle privilegierten Endpunkte.

In diesem Fall gilt **dieser Angriff / dieses Risiko nicht für Sie**.

Dieses Risiko und dieser Angriff sind vor allem relevant, wenn die App im **lokalen Netzwerk** läuft und das die **einzige angenommene Schutzmaßnahme** ist.

## Requests ohne Content-Type erlauben { #allowing-requests-without-content-type }

Wenn Sie Clients unterstützen müssen, die keinen `Content-Type`-Header senden, können Sie die strikte Prüfung deaktivieren, indem Sie `strict_content_type=False` setzen:

{* ../../docs_src/strict_content_type/tutorial001_py310.py hl[4] *}

Mit dieser Einstellung werden Requests ohne `Content-Type`-Header im Body als JSON geparst. Das entspricht dem Verhalten älterer FastAPI-Versionen.

/// info | Info

Dieses Verhalten und diese Konfiguration wurden in FastAPI 0.132.0 hinzugefügt.

///
