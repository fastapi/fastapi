# OAuth2 mit Password (und Hashing), Bearer mit JWT-Tokens

Da wir nun über den gesamten Sicherheitsablauf verfügen, machen wir die Anwendung tatsächlich sicher, indem wir <abbr title="JSON Web Tokens">JWT</abbr>-Tokens und sicheres Passwort-Hashing verwenden.

Diesen Code können Sie tatsächlich in Ihrer Anwendung verwenden, die Passwort-Hashes in Ihrer Datenbank speichern, usw.

Wir bauen auf dem vorherigen Kapitel auf.

## Über JWT

JWT bedeutet „JSON Web Tokens“.

Es ist ein Standard, um ein JSON-Objekt in einem langen, kompakten String ohne Leerzeichen zu kodieren. Das sieht so aus:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

Da er nicht verschlüsselt ist, kann jeder die Informationen aus dem Inhalt wiederherstellen.

Aber er ist signiert. Wenn Sie also einen von Ihnen gesendeten Token zurückerhalten, können Sie überprüfen, ob Sie ihn tatsächlich gesendet haben.

Auf diese Weise können Sie einen Token mit einer Gültigkeitsdauer von beispielsweise einer Woche erstellen. Und wenn der Benutzer am nächsten Tag mit dem Token zurückkommt, wissen Sie, dass der Benutzer immer noch bei Ihrem System angemeldet ist.

Nach einer Woche läuft der Token ab und der Benutzer wird nicht autorisiert und muss sich erneut anmelden, um einen neuen Token zu erhalten. Und wenn der Benutzer (oder ein Dritter) versuchen würde, den Token zu ändern, um das Ablaufdatum zu ändern, würden Sie das entdecken, weil die Signaturen nicht übereinstimmen würden.

Wenn Sie mit JWT-Tokens spielen und sehen möchten, wie sie funktionieren, schauen Sie sich <a href="https://jwt.io/" class="external-link" target="_blank">https://jwt.io</a> an.

## `python-jose` installieren.

Wir müssen <abbr title="JOSE: JavaScript Object Signing and Encryption">`python-jose`</abbr> installieren, um die JWT-Tokens in Python zu generieren und zu verifizieren:

<div class="termy">

```console
$ pip install "python-jose[cryptography]"

---> 100%
```

</div>

<a href="https://github.com/mpdavis/python-jose" class="external-link" target="_blank">python-jose</a> erfordert zusätzlich ein kryptografisches Backend.

Hier verwenden wir das empfohlene: <a href="https://cryptography.io/" class="external-link" target="_blank">pyca/cryptography</a>.

!!! tip "Tipp"
    Dieses Tutorial verwendete zuvor <a href="https://pyjwt.readthedocs.io/" class="external-link" target="_blank">PyJWT</a>.

    Es wurde jedoch aktualisiert, stattdessen python-jose zu verwenden, da dieses alle Funktionen von PyJWT sowie einige Extras bietet, die Sie später möglicherweise benötigen, wenn Sie Integrationen mit anderen Tools erstellen.

## Passwort-Hashing

„Hashing“ bedeutet: Konvertieren eines Inhalts (in diesem Fall eines Passworts) in eine Folge von Bytes (ein schlichter String), die wie Kauderwelsch aussieht.

Immer wenn Sie genau den gleichen Inhalt (genau das gleiche Passwort) übergeben, erhalten Sie genau den gleichen Kauderwelsch.

Sie können jedoch nicht vom Kauderwelsch zurück zum Passwort konvertieren.

### Warum Passwort-Hashing verwenden?

Wenn Ihre Datenbank gestohlen wird, hat der Dieb nicht die Klartext-Passwörter Ihrer Benutzer, sondern nur die Hashes.

Der Dieb kann also nicht versuchen, die gleichen Passwörter in einem anderen System zu verwenden (da viele Benutzer überall das gleiche Passwort verwenden, wäre dies gefährlich).

## `passlib` installieren

PassLib ist ein großartiges Python-Package, um Passwort-Hashes zu handhaben.

Es unterstützt viele sichere Hashing-Algorithmen und Werkzeuge, um mit diesen zu arbeiten.

Der empfohlene Algorithmus ist „Bcrypt“.

Installieren Sie also PassLib mit Bcrypt:

<div class="termy">

```console
$ pip install "passlib[bcrypt]"

---> 100%
```

</div>

!!! tip "Tipp"
    Mit `passlib` können Sie sogar konfigurieren, Passwörter zu lesen, die von **Django**, einem **Flask**-Sicherheit-Plugin, oder vielen anderen erstellt wurden.

    So könnten Sie beispielsweise die gleichen Daten aus einer Django-Anwendung in einer Datenbank mit einer FastAPI-Anwendung teilen. Oder schrittweise eine Django-Anwendung migrieren, während Sie dieselbe Datenbank verwenden.

    Und Ihre Benutzer könnten sich gleichzeitig über Ihre Django-Anwendung oder Ihre **FastAPI**-Anwendung anmelden.

## Die Passwörter hashen und überprüfen

Importieren Sie die benötigten Tools aus `passlib`.

Erstellen Sie einen PassLib-„Kontext“. Der wird für das Hashen und Verifizieren von Passwörtern verwendet.

!!! tip "Tipp"
    Der PassLib-Kontext kann auch andere Hashing-Algorithmen verwenden, einschließlich deprecateter Alter, um etwa nur eine Verifizierung usw. zu ermöglichen.

    Sie könnten ihn beispielsweise verwenden, um von einem anderen System (wie Django) generierte Passwörter zu lesen und zu verifizieren, aber alle neuen Passwörter mit einem anderen Algorithmus wie Bcrypt zu hashen.

    Und mit allen gleichzeitig kompatibel sein.

Erstellen Sie eine Hilfsfunktion, um ein vom Benutzer stammendes Passwort zu hashen.

Und eine weitere, um zu überprüfen, ob ein empfangenes Passwort mit dem gespeicherten Hash übereinstimmt.

Und noch eine, um einen Benutzer zu authentifizieren und zurückzugeben.

=== "Python 3.10+"

    ```Python hl_lines="7  48  55-56  59-60  69-75"
    {!> ../../../docs_src/security/tutorial004_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="7  48  55-56  59-60  69-75"
    {!> ../../../docs_src/security/tutorial004_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="7  49  56-57  60-61  70-76"
    {!> ../../../docs_src/security/tutorial004_an.py!}
    ```

=== "Python 3.10+ nicht annotiert"

    !!! tip "Tipp"
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="6  47  54-55  58-59  68-74"
    {!> ../../../docs_src/security/tutorial004_py310.py!}
    ```

=== "Python 3.8+ nicht annotiert"

    !!! tip "Tipp"
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="7  48  55-56  59-60  69-75"
    {!> ../../../docs_src/security/tutorial004.py!}
    ```

!!! note "Hinweis"
    Wenn Sie sich die neue (gefakte) Datenbank `fake_users_db` anschauen, sehen Sie, wie das gehashte Passwort jetzt aussieht: `"$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"`.

## JWT-Token verarbeiten

Importieren Sie die installierten Module.

Erstellen Sie einen zufälligen geheimen Schlüssel, der zum Signieren der JWT-Tokens verwendet wird.

Um einen sicheren zufälligen geheimen Schlüssel zu generieren, verwenden Sie den folgenden Befehl:

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

Und kopieren Sie die Ausgabe in die Variable `SECRET_KEY` (verwenden Sie nicht die im Beispiel).

Erstellen Sie eine Variable `ALGORITHM` für den Algorithmus, der zum Signieren des JWT-Tokens verwendet wird, und setzen Sie sie auf `"HS256"`.

Erstellen Sie eine Variable für das Ablaufdatum des Tokens.

Definieren Sie ein Pydantic-Modell, das im Token-Endpunkt für die Response verwendet wird.

Erstellen Sie eine Hilfsfunktion, um einen neuen Zugriffstoken zu generieren.

=== "Python 3.10+"

    ```Python hl_lines="6  12-14  28-30  78-86"
    {!> ../../../docs_src/security/tutorial004_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="6  12-14  28-30  78-86"
    {!> ../../../docs_src/security/tutorial004_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="6  13-15  29-31 79-87"
    {!> ../../../docs_src/security/tutorial004_an.py!}
    ```

=== "Python 3.10+ nicht annotiert"

    !!! tip "Tipp"
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="5  11-13  27-29  77-85"
    {!> ../../../docs_src/security/tutorial004_py310.py!}
    ```

=== "Python 3.8+ nicht annotiert"

    !!! tip "Tipp"
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="6  12-14  28-30  78-86"
    {!> ../../../docs_src/security/tutorial004.py!}
    ```

## Die Abhängigkeiten aktualisieren

Aktualisieren Sie `get_current_user`, um den gleichen Token wie zuvor zu erhalten, dieses Mal jedoch unter Verwendung von JWT-Tokens.

Dekodieren Sie den empfangenen Token, validieren Sie ihn und geben Sie den aktuellen Benutzer zurück.

Wenn der Token ungültig ist, geben Sie sofort einen HTTP-Fehler zurück.

=== "Python 3.10+"

    ```Python hl_lines="89-106"
    {!> ../../../docs_src/security/tutorial004_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="89-106"
    {!> ../../../docs_src/security/tutorial004_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="90-107"
    {!> ../../../docs_src/security/tutorial004_an.py!}
    ```

=== "Python 3.10+ nicht annotiert"

    !!! tip "Tipp"
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="88-105"
    {!> ../../../docs_src/security/tutorial004_py310.py!}
    ```

=== "Python 3.8+ nicht annotiert"

    !!! tip "Tipp"
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="89-106"
    {!> ../../../docs_src/security/tutorial004.py!}
    ```

## Die *Pfadoperation* `/token` aktualisieren

Erstellen Sie ein <abbr title="Zeitdifferenz">`timedelta`</abbr> mit der Ablaufzeit des Tokens.

Erstellen Sie einen echten JWT-Zugriffstoken und geben Sie ihn zurück.

=== "Python 3.10+"

    ```Python hl_lines="117-132"
    {!> ../../../docs_src/security/tutorial004_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="117-132"
    {!> ../../../docs_src/security/tutorial004_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="118-133"
    {!> ../../../docs_src/security/tutorial004_an.py!}
    ```

=== "Python 3.10+ nicht annotiert"

    !!! tip "Tipp"
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="114-129"
    {!> ../../../docs_src/security/tutorial004_py310.py!}
    ```

=== "Python 3.8+ nicht annotiert"

    !!! tip "Tipp"
        Bevorzugen Sie die `Annotated`-Version, falls möglich.

    ```Python hl_lines="115-130"
    {!> ../../../docs_src/security/tutorial004.py!}
    ```

### Technische Details zum JWT-„Subjekt“ `sub`

Die JWT-Spezifikation besagt, dass es einen Schlüssel `sub` mit dem Subjekt des Tokens gibt.

Die Verwendung ist optional, aber dort würden Sie die Identifikation des Benutzers speichern, daher verwenden wir das hier.

JWT kann auch für andere Dinge verwendet werden, abgesehen davon, einen Benutzer zu identifizieren und ihm zu erlauben, Operationen direkt auf Ihrer API auszuführen.

Sie könnten beispielsweise ein „Auto“ oder einen „Blog-Beitrag“ identifizieren.

Anschließend könnten Sie Berechtigungen für diese Entität hinzufügen, etwa „Fahren“ (für das Auto) oder „Bearbeiten“ (für den Blog).

Und dann könnten Sie diesen JWT-Token einem Benutzer (oder Bot) geben und dieser könnte ihn verwenden, um diese Aktionen auszuführen (das Auto fahren oder den Blog-Beitrag bearbeiten), ohne dass er überhaupt ein Konto haben müsste, einfach mit dem JWT-Token, den Ihre API dafür generiert hat.

Mit diesen Ideen kann JWT für weitaus anspruchsvollere Szenarien verwendet werden.

In diesen Fällen könnten mehrere dieser Entitäten die gleiche ID haben, sagen wir `foo` (ein Benutzer `foo`, ein Auto `foo` und ein Blog-Beitrag `foo`).

Deshalb, um ID-Kollisionen zu vermeiden, könnten Sie beim Erstellen des JWT-Tokens für den Benutzer, dem Wert des `sub`-Schlüssels ein Präfix, z. B. `username:` voranstellen. In diesem Beispiel hätte der Wert von `sub` also auch `username:johndoe` sein können.

Der wesentliche Punkt ist, dass der `sub`-Schlüssel in der gesamten Anwendung eine eindeutige Kennung haben sollte, und er sollte ein String sein.

## Es testen

Führen Sie den Server aus und gehen Sie zur Dokumentation: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Die Benutzeroberfläche sieht wie folgt aus:

<img src="/img/tutorial/security/image07.png">

Melden Sie sich bei der Anwendung auf die gleiche Weise wie zuvor an.

Verwenden Sie die Anmeldeinformationen:

Benutzername: `johndoe`
Passwort: `secret`.

!!! check
    Beachten Sie, dass im Code nirgendwo das Klartext-Passwort "`secret`" steht, wir haben nur die gehashte Version.

<img src="/img/tutorial/security/image08.png">

Rufen Sie den Endpunkt `/users/me/` auf, Sie erhalten die Response:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="/img/tutorial/security/image09.png">

Wenn Sie die Developer Tools öffnen, können Sie sehen, dass die gesendeten Daten nur den Token enthalten. Das Passwort wird nur bei der ersten Anfrage gesendet, um den Benutzer zu authentisieren und diesen Zugriffstoken zu erhalten, aber nicht mehr danach:

<img src="/img/tutorial/security/image10.png">

!!! note "Hinweis"
    Beachten Sie den Header `Authorization` mit einem Wert, der mit `Bearer` beginnt.

## Fortgeschrittene Verwendung mit `scopes`

OAuth2 hat ein Konzept von <abbr title="Geltungsbereiche">„Scopes“</abbr>.

Sie können diese verwenden, um einem JWT-Token einen bestimmten Satz von Berechtigungen zu übergeben.

Anschließend können Sie diesen Token einem Benutzer direkt oder einem Dritten geben, damit diese mit einer Reihe von Einschränkungen mit Ihrer API interagieren können.

Wie Sie sie verwenden und wie sie in **FastAPI** integriert sind, erfahren Sie später im **Handbuch für fortgeschrittene Benutzer**.

## Zusammenfassung

Mit dem, was Sie bis hier gesehen haben, können Sie eine sichere **FastAPI**-Anwendung mithilfe von Standards wie OAuth2 und JWT einrichten.

In fast jedem Framework wird die Handhabung der Sicherheit recht schnell zu einem ziemlich komplexen Thema.

Viele Packages, die es stark vereinfachen, müssen viele Kompromisse beim Datenmodell, der Datenbank und den verfügbaren Funktionen eingehen. Und einige dieser Pakete, die die Dinge zu sehr vereinfachen, weisen tatsächlich Sicherheitslücken auf.

---

**FastAPI** geht bei keiner Datenbank, keinem Datenmodell oder Tool Kompromisse ein.

Es gibt Ihnen die volle Flexibilität, diejenigen auszuwählen, die am besten zu Ihrem Projekt passen.

Und Sie können viele gut gepflegte und weit verbreitete Packages wie `passlib` und `python-jose` direkt verwenden, da **FastAPI** keine komplexen Mechanismen zur Integration externer Pakete erfordert.

Aber es bietet Ihnen die Werkzeuge, um den Prozess so weit wie möglich zu vereinfachen, ohne Kompromisse bei Flexibilität, Robustheit oder Sicherheit einzugehen.

Und Sie können sichere Standardprotokolle wie OAuth2 auf relativ einfache Weise verwenden und implementieren.

Im **Handbuch für fortgeschrittene Benutzer** erfahren Sie mehr darüber, wie Sie OAuth2-„Scopes“ für ein feingranuliertes Berechtigungssystem verwenden, das denselben Standards folgt. OAuth2 mit Scopes ist der Mechanismus, der von vielen großen Authentifizierungsanbietern wie Facebook, Google, GitHub, Microsoft, Twitter, usw. verwendet wird, um Drittanbieteranwendungen zu autorisieren, im Namen ihrer Benutzer mit ihren APIs zu interagieren.
