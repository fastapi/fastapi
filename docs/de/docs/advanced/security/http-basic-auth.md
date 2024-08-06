# HTTP Basic Auth

Für die einfachsten Fälle können Sie <abbr title="HTTP-Basisauthentifizierung">HTTP Basic Auth</abbr> verwenden.

Bei HTTP Basic Auth erwartet die Anwendung einen Header, der einen Benutzernamen und ein Passwort enthält.

Wenn sie diesen nicht empfängt, gibt sie den HTTP-Error 401 „Unauthorized“ zurück.

Und gibt einen Header `WWW-Authenticate` mit dem Wert `Basic` und einem optionalen `realm`-Parameter („Bereich“) zurück.

Dadurch wird der Browser angewiesen, die integrierte Eingabeaufforderung für einen Benutzernamen und ein Passwort anzuzeigen.

Wenn Sie dann den Benutzernamen und das Passwort eingeben, sendet der Browser diese automatisch im Header.

## Einfaches HTTP Basic Auth

* Importieren Sie `HTTPBasic` und `HTTPBasicCredentials`.
* Erstellen Sie mit `HTTPBasic` ein „`security`-Schema“.
* Verwenden Sie dieses `security` mit einer Abhängigkeit in Ihrer *Pfadoperation*.
* Diese gibt ein Objekt vom Typ `HTTPBasicCredentials` zurück:
    * Es enthält den gesendeten `username` und das gesendete `password`.

//// tab | Python 3.9+

```Python hl_lines="4  8  12"
{!> ../../../docs_src/security/tutorial006_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="2  7  11"
{!> ../../../docs_src/security/tutorial006_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="2  6  10"
{!> ../../../docs_src/security/tutorial006.py!}
```

////

Wenn Sie versuchen, die URL zum ersten Mal zu öffnen (oder in der Dokumentation auf den Button „Execute“ zu klicken), wird der Browser Sie nach Ihrem Benutzernamen und Passwort fragen:

<img src="/img/tutorial/security/image12.png">

## Den Benutzernamen überprüfen

Hier ist ein vollständigeres Beispiel.

Verwenden Sie eine Abhängigkeit, um zu überprüfen, ob Benutzername und Passwort korrekt sind.

Verwenden Sie dazu das Python-Standardmodul <a href="https://docs.python.org/3/library/secrets.html" class="external-link" target="_blank">`secrets`</a>, um den Benutzernamen und das Passwort zu überprüfen.

`secrets.compare_digest()` benötigt `bytes` oder einen `str`, welcher nur ASCII-Zeichen (solche der englischen Sprache) enthalten darf, das bedeutet, dass es nicht mit Zeichen wie `á`, wie in `Sebastián`, funktionieren würde.

Um dies zu lösen, konvertieren wir zunächst den `username` und das `password` in UTF-8-codierte `bytes`.

Dann können wir `secrets.compare_digest()` verwenden, um sicherzustellen, dass `credentials.username` `"stanleyjobson"` und `credentials.password` `"swordfish"` ist.

//// tab | Python 3.9+

```Python hl_lines="1  12-24"
{!> ../../../docs_src/security/tutorial007_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  12-24"
{!> ../../../docs_src/security/tutorial007_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="1  11-21"
{!> ../../../docs_src/security/tutorial007.py!}
```

////

Dies wäre das gleiche wie:

```Python
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # Einen Error zurückgeben
    ...
```

Aber durch die Verwendung von `secrets.compare_digest()` ist dieser Code sicher vor einer Art von Angriffen, die „Timing-Angriffe“ genannt werden.

### Timing-Angriffe

Aber was ist ein „Timing-Angriff“?

Stellen wir uns vor, dass einige Angreifer versuchen, den Benutzernamen und das Passwort zu erraten.

Und sie senden eine Anfrage mit dem Benutzernamen `johndoe` und dem Passwort `love123`.

Dann würde der Python-Code in Ihrer Anwendung etwa so aussehen:

```Python
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Aber genau in dem Moment, in dem Python das erste `j` in `johndoe` mit dem ersten `s` in `stanleyjobson` vergleicht, gibt es `False` zurück, da es bereits weiß, dass diese beiden Strings nicht identisch sind, und denkt, „Es besteht keine Notwendigkeit, weitere Berechnungen mit dem Vergleich der restlichen Buchstaben zu verschwenden“. Und Ihre Anwendung wird zurückgeben „Incorrect username or password“.

Doch dann versuchen es die Angreifer mit dem Benutzernamen `stanleyjobsox` und dem Passwort `love123`.

Und Ihr Anwendungscode macht etwa Folgendes:

```Python
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Python muss das gesamte `stanleyjobso` in `stanleyjobsox` und `stanleyjobson` vergleichen, bevor es erkennt, dass beide Zeichenfolgen nicht gleich sind. Daher wird es einige zusätzliche Mikrosekunden dauern, bis die Antwort „Incorrect username or password“ erfolgt.

#### Die Zeit zum Antworten hilft den Angreifern

Wenn die Angreifer zu diesem Zeitpunkt feststellen, dass der Server einige Mikrosekunden länger braucht, um die Antwort „Incorrect username or password“ zu senden, wissen sie, dass sie _etwas_ richtig gemacht haben, einige der Anfangsbuchstaben waren richtig.

Und dann können sie es noch einmal versuchen, wohl wissend, dass es wahrscheinlich eher etwas mit `stanleyjobsox` als mit `johndoe` zu tun hat.

#### Ein „professioneller“ Angriff

Natürlich würden die Angreifer das alles nicht von Hand versuchen, sondern ein Programm dafür schreiben, möglicherweise mit Tausenden oder Millionen Tests pro Sekunde. Und würden jeweils nur einen zusätzlichen richtigen Buchstaben erhalten.

Aber so hätten die Angreifer in wenigen Minuten oder Stunden mit der „Hilfe“ unserer Anwendung den richtigen Benutzernamen und das richtige Passwort erraten, indem sie die Zeitspanne zur Hilfe nehmen, die diese zur Beantwortung benötigt.

#### Das Problem beheben mittels `secrets.compare_digest()`

Aber in unserem Code verwenden wir tatsächlich `secrets.compare_digest()`.

Damit wird, kurz gesagt, der Vergleich von `stanleyjobsox` mit `stanleyjobson` genauso lange dauern wie der Vergleich von `johndoe` mit `stanleyjobson`. Und das Gleiche gilt für das Passwort.

So ist Ihr Anwendungscode, dank der Verwendung von `secrets.compare_digest()`, vor dieser ganzen Klasse von Sicherheitsangriffen geschützt.

### Den Error zurückgeben

Nachdem Sie festgestellt haben, dass die Anmeldeinformationen falsch sind, geben Sie eine `HTTPException` mit dem Statuscode 401 zurück (derselbe, der auch zurückgegeben wird, wenn keine Anmeldeinformationen angegeben werden) und fügen den Header `WWW-Authenticate` hinzu, damit der Browser die Anmeldeaufforderung erneut anzeigt:

//// tab | Python 3.9+

```Python hl_lines="26-30"
{!> ../../../docs_src/security/tutorial007_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="26-30"
{!> ../../../docs_src/security/tutorial007_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="23-27"
{!> ../../../docs_src/security/tutorial007.py!}
```

////
