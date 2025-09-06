# Einfaches OAuth2 mit Password und Bearer { #simple-oauth2-with-password-and-bearer }

Lassen Sie uns nun auf dem vorherigen Kapitel aufbauen und die fehlenden Teile hinzufügen, um einen vollständigen Sicherheits-Flow zu erhalten.

## `username` und `password` entgegennehmen { #get-the-username-and-password }

Wir werden **FastAPIs** Sicherheits-Werkzeuge verwenden, um den `username` und das `password` entgegenzunehmen.

OAuth2 spezifiziert, dass der Client/Benutzer bei Verwendung des „Password Flow“ (den wir verwenden) die Felder `username` und `password` als Formulardaten senden muss.

Und die Spezifikation sagt, dass die Felder so benannt werden müssen. `user-name` oder `email` würde also nicht funktionieren.

Aber keine Sorge, Sie können sie Ihren Endbenutzern im Frontend so anzeigen, wie Sie möchten.

Und Ihre Datenbankmodelle können beliebige andere Namen verwenden.

Aber für die Login-*Pfadoperation* müssen wir diese Namen verwenden, um mit der Spezifikation kompatibel zu sein (und beispielsweise das integrierte API-Dokumentationssystem verwenden zu können).

Die Spezifikation besagt auch, dass `username` und `password` als Formulardaten gesendet werden müssen (hier also kein JSON).

### <abbr title="Geltungsbereich">`scope`</abbr> { #scope }

Ferner sagt die Spezifikation, dass der Client ein weiteres Formularfeld "`scope`" („Geltungsbereich“) senden kann.

Der Name des Formularfelds lautet `scope` (im Singular), tatsächlich handelt es sich jedoch um einen langen String mit durch Leerzeichen getrennten „Scopes“.

Jeder „Scope“ ist nur ein String (ohne Leerzeichen).

Diese werden normalerweise verwendet, um bestimmte Sicherheitsberechtigungen zu deklarieren, zum Beispiel:

* `users:read` oder `users:write` sind gängige Beispiele.
* `instagram_basic` wird von Facebook / Instagram verwendet.
* `https://www.googleapis.com/auth/drive` wird von Google verwendet.

/// info | Info

In OAuth2 ist ein „Scope“ nur ein String, der eine bestimmte erforderliche Berechtigung deklariert.

Es spielt keine Rolle, ob er andere Zeichen wie `:` enthält oder ob es eine URL ist.

Diese Details sind implementierungsspezifisch.

Für OAuth2 sind es einfach nur Strings.

///

## Code, um `username` und `password` entgegenzunehmen { #code-to-get-the-username-and-password }

Lassen Sie uns nun die von **FastAPI** bereitgestellten Werkzeuge verwenden, um das zu erledigen.

### `OAuth2PasswordRequestForm` { #oauth2passwordrequestform }

Importieren Sie zunächst `OAuth2PasswordRequestForm` und verwenden Sie es als Abhängigkeit mit `Depends` in der *Pfadoperation* für `/token`:

{* ../../docs_src/security/tutorial003_an_py310.py hl[4,78] *}

`OAuth2PasswordRequestForm` ist eine Klassenabhängigkeit, die einen Formularbody deklariert mit:

* Dem `username`.
* Dem `password`.
* Einem optionalen `scope`-Feld als langem String, bestehend aus durch Leerzeichen getrennten Strings.
* Einem optionalen <abbr title="Art der Anmeldung">`grant_type`</abbr>.

/// tip | Tipp

Die OAuth2-Spezifikation *erfordert* tatsächlich ein Feld `grant_type` mit dem festen Wert `password`, aber `OAuth2PasswordRequestForm` erzwingt dies nicht.

Wenn Sie es erzwingen müssen, verwenden Sie `OAuth2PasswordRequestFormStrict` anstelle von `OAuth2PasswordRequestForm`.

///

* Eine optionale `client_id` (benötigen wir für unser Beispiel nicht).
* Ein optionales `client_secret` (benötigen wir für unser Beispiel nicht).

/// info | Info

`OAuth2PasswordRequestForm` ist keine spezielle Klasse für **FastAPI**, so wie `OAuth2PasswordBearer`.

`OAuth2PasswordBearer` lässt **FastAPI** wissen, dass es sich um ein Sicherheitsschema handelt. Daher wird es auf diese Weise zu OpenAPI hinzugefügt.

Aber `OAuth2PasswordRequestForm` ist nur eine Klassenabhängigkeit, die Sie selbst hätten schreiben können, oder Sie hätten `Form`ular-Parameter direkt deklarieren können.

Da es sich jedoch um einen häufigen Anwendungsfall handelt, wird er zur Vereinfachung direkt von **FastAPI** bereitgestellt.

///

### Die Formulardaten verwenden { #use-the-form-data }

/// tip | Tipp

Die Instanz der Klassenabhängigkeit `OAuth2PasswordRequestForm` verfügt, statt eines Attributs `scope` mit dem durch Leerzeichen getrennten langen String, über das Attribut `scopes` mit einer tatsächlichen Liste von Strings, einem für jeden gesendeten Scope.

In diesem Beispiel verwenden wir keine `scopes`, aber die Funktionalität ist vorhanden, wenn Sie sie benötigen.

///

Rufen Sie nun die Benutzerdaten aus der (gefakten) Datenbank ab, für diesen `username` aus dem Formularfeld.

Wenn es keinen solchen Benutzer gibt, geben wir die Fehlermeldung „Incorrect username or password“ zurück.

Für den Fehler verwenden wir die Exception `HTTPException`:

{* ../../docs_src/security/tutorial003_an_py310.py hl[3,79:81] *}

### Das Passwort überprüfen { #check-the-password }

Zu diesem Zeitpunkt liegen uns die Benutzerdaten aus unserer Datenbank vor, das Passwort haben wir jedoch noch nicht überprüft.

Lassen Sie uns diese Daten zunächst in das Pydantic-Modell `UserInDB` einfügen.

Sie sollten niemals Klartext-Passwörter speichern, daher verwenden wir ein (gefaktes) Passwort-Hashing-System.

Wenn die Passwörter nicht übereinstimmen, geben wir denselben Fehler zurück.

#### Passwort-Hashing { #password-hashing }

„Hashing“ bedeutet: Konvertieren eines Inhalts (in diesem Fall eines Passworts) in eine Folge von Bytes (ein schlichter String), die wie Kauderwelsch aussieht.

Immer wenn Sie genau den gleichen Inhalt (genau das gleiche Passwort) übergeben, erhalten Sie genau den gleichen Kauderwelsch.

Sie können jedoch nicht vom Kauderwelsch zurück zum Passwort konvertieren.

##### Warum Passwort-Hashing verwenden? { #why-use-password-hashing }

Wenn Ihre Datenbank gestohlen wird, hat der Dieb nicht die Klartext-Passwörter Ihrer Benutzer, sondern nur die Hashes.

Der Dieb kann also nicht versuchen, die gleichen Passwörter in einem anderen System zu verwenden (da viele Benutzer überall das gleiche Passwort verwenden, wäre dies gefährlich).

{* ../../docs_src/security/tutorial003_an_py310.py hl[82:85] *}

#### Über `**user_dict` { #about-user-dict }

`UserInDB(**user_dict)` bedeutet:

*Übergib die Schlüssel und Werte des `user_dict` direkt als Schlüssel-Wert-Argumente, äquivalent zu:*

```Python
UserInDB(
    username = user_dict["username"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    disabled = user_dict["disabled"],
    hashed_password = user_dict["hashed_password"],
)
```

/// info | Info

Eine ausführlichere Erklärung von `**user_dict` finden Sie in [der Dokumentation für **Extra Modelle**](../extra-models.md#about-user-in-dict){.internal-link target=_blank}.

///

## Den Token zurückgeben { #return-the-token }

Die <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> des `token`-Endpunkts muss ein JSON-Objekt sein.

Es sollte einen `token_type` haben. Da wir in unserem Fall „Bearer“-Token verwenden, sollte der Token-Typ "`bearer`" sein.

Und es sollte einen `access_token` haben, mit einem String, der unseren Zugriffstoken enthält.

In diesem einfachen Beispiel gehen wir einfach völlig unsicher vor und geben denselben `username` wie der Token zurück.

/// tip | Tipp

Im nächsten Kapitel sehen Sie eine wirklich sichere Implementierung mit Passwort-Hashing und <abbr title="JSON Web Tokens">JWT</abbr>-Tokens.

Aber konzentrieren wir uns zunächst auf die spezifischen Details, die wir benötigen.

///

{* ../../docs_src/security/tutorial003_an_py310.py hl[87] *}

/// tip | Tipp

Gemäß der Spezifikation sollten Sie ein JSON mit einem `access_token` und einem `token_type` zurückgeben, genau wie in diesem Beispiel.

Das müssen Sie selbst in Ihrem Code tun und sicherstellen, dass Sie diese JSON-Schlüssel verwenden.

Es ist fast das Einzige, woran Sie denken müssen, es selbst richtigzumachen und die Spezifikationen einzuhalten.

Den Rest erledigt **FastAPI** für Sie.

///

## Die Abhängigkeiten aktualisieren { #update-the-dependencies }

Jetzt werden wir unsere Abhängigkeiten aktualisieren.

Wir möchten den `current_user` *nur* erhalten, wenn dieser Benutzer aktiv ist.

Daher erstellen wir eine zusätzliche Abhängigkeit `get_current_active_user`, die wiederum `get_current_user` als Abhängigkeit verwendet.

Beide Abhängigkeiten geben nur dann einen HTTP-Error zurück, wenn der Benutzer nicht existiert oder inaktiv ist.

In unserem Endpunkt erhalten wir also nur dann einen Benutzer, wenn der Benutzer existiert, korrekt authentifiziert wurde und aktiv ist:

{* ../../docs_src/security/tutorial003_an_py310.py hl[58:66,69:74,94] *}

/// info | Info

Der zusätzliche Header `WWW-Authenticate` mit dem Wert `Bearer`, den wir hier zurückgeben, ist ebenfalls Teil der Spezifikation.

Jeder HTTP-(Fehler-)Statuscode 401 „UNAUTHORIZED“ soll auch einen `WWW-Authenticate`-Header zurückgeben.

Im Fall von Bearer-Tokens (in unserem Fall) sollte der Wert dieses Headers `Bearer` lauten.

Sie können diesen zusätzlichen Header tatsächlich weglassen und es würde trotzdem funktionieren.

Aber er wird hier bereitgestellt, um den Spezifikationen zu entsprechen.

Außerdem gibt es möglicherweise Tools, die ihn erwarten und verwenden (jetzt oder in der Zukunft) und das könnte für Sie oder Ihre Benutzer jetzt oder in der Zukunft nützlich sein.

Das ist der Vorteil von Standards ...

///

## Es in Aktion sehen { #see-it-in-action }

Öffnen Sie die interaktive Dokumentation: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

### Authentifizieren { #authenticate }

Klicken Sie auf den Button „Authorize“.

Verwenden Sie die Anmeldedaten:

Benutzer: `johndoe`

Passwort: `secret`.

<img src="/img/tutorial/security/image04.png">

Nach der Authentifizierung im System sehen Sie Folgendes:

<img src="/img/tutorial/security/image05.png">

### Die eigenen Benutzerdaten ansehen { #get-your-own-user-data }

Verwenden Sie nun die Operation `GET` mit dem Pfad `/users/me`.

Sie erhalten Ihre Benutzerdaten:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false,
  "hashed_password": "fakehashedsecret"
}
```

<img src="/img/tutorial/security/image06.png">

Wenn Sie auf das Schlosssymbol klicken und sich abmelden und dann den gleichen Vorgang nochmal versuchen, erhalten Sie einen HTTP 401 Error:

```JSON
{
  "detail": "Not authenticated"
}
```

### Inaktiver Benutzer { #inactive-user }

Versuchen Sie es nun mit einem inaktiven Benutzer und authentisieren Sie sich mit:

Benutzer: `alice`.

Passwort: `secret2`.

Und versuchen Sie, die Operation `GET` mit dem Pfad `/users/me` zu verwenden.

Sie erhalten die Fehlermeldung „Inactive user“:

```JSON
{
  "detail": "Inactive user"
}
```

## Zusammenfassung { #recap }

Sie verfügen jetzt über die Tools, um ein vollständiges Sicherheitssystem basierend auf `username` und `password` für Ihre API zu implementieren.

Mit diesen Tools können Sie das Sicherheitssystem mit jeder Datenbank und jedem Benutzer oder Datenmodell kompatibel machen.

Das einzige fehlende Detail ist, dass es noch nicht wirklich „sicher“ ist.

Im nächsten Kapitel erfahren Sie, wie Sie eine sichere Passwort-Hashing-Bibliothek und <abbr title="JSON Web Tokens">JWT</abbr>-Token verwenden.
