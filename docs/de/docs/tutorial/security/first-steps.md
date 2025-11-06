# Sicherheit – Erste Schritte { #security-first-steps }

Stellen wir uns vor, dass Sie Ihre **Backend**-API auf einer Domain haben.

Und Sie haben ein **Frontend** auf einer anderen Domain oder in einem anderen Pfad derselben Domain (oder in einer Mobile-Anwendung).

Und Sie möchten eine Möglichkeit haben, dass sich das Frontend mithilfe eines **Benutzernamens** und eines **Passworts** beim Backend authentisieren kann.

Wir können **OAuth2** verwenden, um das mit **FastAPI** zu erstellen.

Aber ersparen wir Ihnen die Zeit, die gesamte lange Spezifikation zu lesen, nur um die kleinen Informationen zu finden, die Sie benötigen.

Lassen Sie uns die von **FastAPI** bereitgestellten Tools verwenden, um Sicherheit zu gewährleisten.

## Wie es aussieht { #how-it-looks }

Lassen Sie uns zunächst einfach den Code verwenden und sehen, wie er funktioniert, und dann kommen wir zurück, um zu verstehen, was passiert.

## `main.py` erstellen { #create-main-py }

Kopieren Sie das Beispiel in eine Datei `main.py`:

{* ../../docs_src/security/tutorial001_an_py39.py *}

## Ausführen { #run-it }

/// info | Info

Das Paket <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> wird automatisch mit **FastAPI** installiert, wenn Sie den Befehl `pip install "fastapi[standard]"` ausführen.

Wenn Sie jedoch den Befehl `pip install fastapi` verwenden, ist das Paket `python-multipart` nicht standardmäßig enthalten.

Um es manuell zu installieren, stellen Sie sicher, dass Sie eine [Virtuelle Umgebung](../../virtual-environments.md){.internal-link target=_blank} erstellen, sie aktivieren und es dann mit:

```console
$ pip install python-multipart
```

installieren.

Das liegt daran, dass **OAuth2** „Formulardaten“ zum Senden von `username` und `password` verwendet.

///

Führen Sie das Beispiel aus mit:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## Es testen { #check-it }

Gehen Sie zu der interaktiven Dokumentation unter: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Sie werden etwa Folgendes sehen:

<img src="/img/tutorial/security/image01.png">

/// check | Authorize-Button!

Sie haben bereits einen glänzenden, neuen „Authorize“-Button.

Und Ihre *Pfadoperation* hat in der oberen rechten Ecke ein kleines Schloss, auf das Sie klicken können.

///

Und wenn Sie darauf klicken, erhalten Sie ein kleines Anmeldeformular zur Eingabe eines `username` und `password` (und anderer optionaler Felder):

<img src="/img/tutorial/security/image02.png">

/// note | Hinweis

Es spielt keine Rolle, was Sie in das Formular eingeben, es wird noch nicht funktionieren. Wir kommen dahin.

///

Dies ist natürlich nicht das Frontend für die Endbenutzer, aber es ist ein großartiges automatisches Tool, um Ihre gesamte API interaktiv zu dokumentieren.

Es kann vom Frontend-Team verwendet werden (das auch Sie selbst sein können).

Es kann von Anwendungen und Systemen Dritter verwendet werden.

Und es kann auch von Ihnen selbst verwendet werden, um dieselbe Anwendung zu debuggen, zu prüfen und zu testen.

## Der `password`-Flow { #the-password-flow }

Lassen Sie uns nun etwas zurückgehen und verstehen, was das alles ist.

Der `password`-„Flow“ ist eine der in OAuth2 definierten Wege („Flows“) zur Handhabung von Sicherheit und Authentifizierung.

OAuth2 wurde so konzipiert, dass das Backend oder die API unabhängig vom Server sein kann, der den Benutzer authentifiziert.

In diesem Fall handhabt jedoch dieselbe **FastAPI**-Anwendung sowohl die API als auch die Authentifizierung.

Betrachten wir es also aus dieser vereinfachten Sicht:

* Der Benutzer gibt den `username` und das `password` im Frontend ein und drückt `Enter`.
* Das Frontend (das im Browser des Benutzers läuft) sendet diesen `username` und das `password` an eine bestimmte URL in unserer API (deklariert mit `tokenUrl="token"`).
* Die API überprüft den `username` und das `password` und antwortet mit einem „Token“ (wir haben davon noch nichts implementiert).
    * Ein „Token“ ist lediglich ein String mit einem Inhalt, den wir später verwenden können, um diesen Benutzer zu verifizieren.
    * Normalerweise läuft ein Token nach einiger Zeit ab.
        * Daher muss sich der Benutzer irgendwann später erneut anmelden.
        * Und wenn der Token gestohlen wird, ist das Risiko geringer. Es handelt sich nicht um einen dauerhaften Schlüssel, der (in den meisten Fällen) für immer funktioniert.
* Das Frontend speichert diesen Token vorübergehend irgendwo.
* Der Benutzer klickt im Frontend, um zu einem anderen Abschnitt der Frontend-Web-Anwendung zu gelangen.
* Das Frontend muss weitere Daten von der API abrufen.
    * Es benötigt jedoch eine Authentifizierung für diesen bestimmten Endpunkt.
    * Um sich also bei unserer API zu authentifizieren, sendet es einen Header `Authorization` mit dem Wert `Bearer ` plus dem Token.
    * Wenn der Token `foobar` enthielte, wäre der Inhalt des `Authorization`-Headers: `Bearer foobar`.

## **FastAPI**s `OAuth2PasswordBearer` { #fastapis-oauth2passwordbearer }

**FastAPI** bietet mehrere Tools auf unterschiedlichen Abstraktionsebenen zur Implementierung dieser Sicherheitsfunktionen.

In diesem Beispiel verwenden wir **OAuth2** mit dem **Password**-Flow und einem **Bearer**-Token. Wir machen das mit der Klasse `OAuth2PasswordBearer`.

/// info | Info

Ein „Bearer“-Token ist nicht die einzige Option.

Aber es ist die beste für unseren Anwendungsfall.

Und es ist wahrscheinlich auch für die meisten anderen Anwendungsfälle die beste, es sei denn, Sie sind ein OAuth2-Experte und wissen genau, warum es eine andere Option gibt, die Ihren Anforderungen besser entspricht.

In dem Fall gibt Ihnen **FastAPI** ebenfalls die Tools, die Sie zum Erstellen brauchen.

///

Wenn wir eine Instanz der Klasse `OAuth2PasswordBearer` erstellen, übergeben wir den Parameter `tokenUrl`. Dieser Parameter enthält die URL, die der Client (das Frontend, das im Browser des Benutzers ausgeführt wird) verwendet, wenn er den `username` und das `password` sendet, um einen Token zu erhalten.

{* ../../docs_src/security/tutorial001_an_py39.py hl[8] *}

/// tip | Tipp

Hier bezieht sich `tokenUrl="token"` auf eine relative URL `token`, die wir noch nicht erstellt haben. Da es sich um eine relative URL handelt, entspricht sie `./token`.

Da wir eine relative URL verwenden, würde sich das, wenn sich Ihre API unter `https://example.com/` befindet, auf `https://example.com/token` beziehen. Wenn sich Ihre API jedoch unter `https://example.com/api/v1/` befände, würde es sich auf `https://example.com/api/v1/token` beziehen.

Die Verwendung einer relativen URL ist wichtig, um sicherzustellen, dass Ihre Anwendung auch in einem fortgeschrittenen Anwendungsfall, wie [hinter einem Proxy](../../advanced/behind-a-proxy.md){.internal-link target=_blank}, weiterhin funktioniert.

///

Dieser Parameter erstellt nicht diesen Endpunkt / diese *Pfadoperation*, sondern deklariert, dass die URL `/token` diejenige sein wird, die der Client verwenden soll, um den Token abzurufen. Diese Information wird in OpenAPI und dann in den interaktiven API-Dokumentationssystemen verwendet.

Wir werden demnächst auch die eigentliche Pfadoperation erstellen.

/// info | Info

Wenn Sie ein sehr strenger „Pythonista“ sind, missfällt Ihnen möglicherweise die Schreibweise des Parameternamens `tokenUrl` anstelle von `token_url`.

Das liegt daran, dass FastAPI denselben Namen wie in der OpenAPI-Spezifikation verwendet. Sodass Sie, wenn Sie mehr über eines dieser Sicherheitsschemas herausfinden möchten, den Namen einfach kopieren und einfügen können, um weitere Informationen darüber zu erhalten.

///

Die Variable `oauth2_scheme` ist eine Instanz von `OAuth2PasswordBearer`, aber auch ein „Callable“.

Es könnte wie folgt aufgerufen werden:

```Python
oauth2_scheme(some, parameters)
```

Es kann also mit `Depends` verwendet werden.

### Verwenden { #use-it }

Jetzt können Sie dieses `oauth2_scheme` als Abhängigkeit `Depends` übergeben.

{* ../../docs_src/security/tutorial001_an_py39.py hl[12] *}

Diese Abhängigkeit stellt einen `str` bereit, der dem Parameter `token` der *Pfadoperation-Funktion* zugewiesen wird.

**FastAPI** weiß, dass es diese Abhängigkeit verwenden kann, um ein „Sicherheitsschema“ im OpenAPI-Schema (und der automatischen API-Dokumentation) zu definieren.

/// info | Technische Details

**FastAPI** weiß, dass es die Klasse `OAuth2PasswordBearer` (deklariert in einer Abhängigkeit) verwenden kann, um das Sicherheitsschema in OpenAPI zu definieren, da es von `fastapi.security.oauth2.OAuth2` erbt, das wiederum von `fastapi.security.base.SecurityBase` erbt.

Alle Sicherheits-Werkzeuge, die in OpenAPI integriert sind (und die automatische API-Dokumentation), erben von `SecurityBase`, so weiß **FastAPI**, wie es sie in OpenAPI integrieren muss.

///

## Was es macht { #what-it-does }

FastAPI wird im <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> nach diesem `Authorization`-Header suchen, prüfen, ob der Wert `Bearer ` plus ein Token ist, und den Token als `str` zurückgeben.

Wenn es keinen `Authorization`-Header sieht, oder der Wert keinen `Bearer `-Token hat, antwortet es direkt mit einem 401-Statuscode-Error (`UNAUTHORIZED`).

Sie müssen nicht einmal prüfen, ob der Token existiert, um einen Fehler zurückzugeben. Seien Sie sicher, dass Ihre Funktion, wenn sie ausgeführt wird, ein `str` in diesem Token enthält.

Sie können das bereits in der interaktiven Dokumentation ausprobieren:

<img src="/img/tutorial/security/image03.png">

Wir überprüfen im Moment noch nicht die Gültigkeit des Tokens, aber das ist bereits ein Anfang.

## Zusammenfassung { #recap }

Mit nur drei oder vier zusätzlichen Zeilen haben Sie so bereits eine primitive Form der Sicherheit.
