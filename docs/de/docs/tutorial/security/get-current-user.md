# Aktuellen Benutzer abrufen { #get-current-user }

Im vorherigen Kapitel hat das Sicherheitssystem (das auf dem Dependency Injection System basiert) der *Pfadoperation-Funktion* einen `token` vom Typ `str` überreicht:

{* ../../docs_src/security/tutorial001_an_py39.py hl[12] *}

Aber das ist immer noch nicht so nützlich.

Lassen wir es uns den aktuellen Benutzer überreichen.

## Ein Benutzermodell erstellen { #create-a-user-model }

Erstellen wir zunächst ein Pydantic-Benutzermodell.

So wie wir Pydantic zum Deklarieren von Bodys verwenden, können wir es auch überall sonst verwenden:

{* ../../docs_src/security/tutorial002_an_py310.py hl[5,12:6] *}

## Eine `get_current_user`-Abhängigkeit erstellen { #create-a-get-current-user-dependency }

Erstellen wir eine Abhängigkeit `get_current_user`.

Erinnern Sie sich, dass Abhängigkeiten Unterabhängigkeiten haben können?

`get_current_user` wird seinerseits von `oauth2_scheme` abhängen, das wir zuvor erstellt haben.

So wie wir es zuvor in der *Pfadoperation* direkt gemacht haben, erhält unsere neue Abhängigkeit `get_current_user` von der Unterabhängigkeit `oauth2_scheme` einen `token` vom Typ `str`:

{* ../../docs_src/security/tutorial002_an_py310.py hl[25] *}

## Den Benutzer abrufen { #get-the-user }

`get_current_user` wird eine von uns erstellte (gefakte) Hilfsfunktion verwenden, welche einen Token vom Typ `str` entgegennimmt und unser Pydantic-`User`-Modell zurückgibt:

{* ../../docs_src/security/tutorial002_an_py310.py hl[19:22,26:27] *}

## Den aktuellen Benutzer einfügen { #inject-the-current-user }

Und jetzt können wir wiederum `Depends` mit unserem `get_current_user` in der *Pfadoperation* verwenden:

{* ../../docs_src/security/tutorial002_an_py310.py hl[31] *}

Beachten Sie, dass wir als Typ von `current_user` das Pydantic-Modell `User` deklarieren.

Das wird uns innerhalb der Funktion bei Codevervollständigung und Typprüfungen helfen.

/// tip | Tipp

Sie erinnern sich vielleicht, dass <abbr title="Anfragekörper">Requestbodys</abbr> ebenfalls mit Pydantic-Modellen deklariert werden.

Weil Sie `Depends` verwenden, wird **FastAPI** hier aber nicht verwirrt.

///

/// check | Testen

Die Art und Weise, wie dieses System von Abhängigkeiten konzipiert ist, ermöglicht es uns, verschiedene Abhängigkeiten (verschiedene „Dependables“) zu haben, die alle ein `User`-Modell zurückgeben.

Wir sind nicht darauf beschränkt, nur eine Abhängigkeit zu haben, die diesen Typ von Daten zurückgeben kann.

///

## Andere Modelle { #other-models }

Sie können jetzt den aktuellen Benutzer direkt in den *Pfadoperation-Funktionen* abrufen und die Sicherheitsmechanismen auf **Dependency Injection** Ebene handhaben, mittels `Depends`.

Und Sie können alle Modelle und Daten für die Sicherheitsanforderungen verwenden (in diesem Fall ein Pydantic-Modell `User`).

Sie sind jedoch nicht auf die Verwendung von bestimmten Datenmodellen, Klassen, oder Typen beschränkt.

Möchten Sie eine `id` und eine `email` und keinen `username` in Ihrem Modell haben? Kein Problem. Sie können dieselben Tools verwenden.

Möchten Sie nur ein `str` haben? Oder nur ein `dict`? Oder direkt eine Instanz eines Modells einer Datenbank-Klasse? Es funktioniert alles auf die gleiche Weise.

Sie haben eigentlich keine Benutzer, die sich bei Ihrer Anwendung anmelden, sondern Roboter, Bots oder andere Systeme, die nur über einen Zugriffstoken verfügen? Auch hier funktioniert alles gleich.

Verwenden Sie einfach jede Art von Modell, jede Art von Klasse, jede Art von Datenbank, die Sie für Ihre Anwendung benötigen. **FastAPI** deckt das alles mit seinem Dependency Injection System ab.

## Codegröße { #code-size }

Dieses Beispiel mag ausführlich erscheinen. Bedenken Sie, dass wir Sicherheit, Datenmodelle, Hilfsfunktionen und *Pfadoperationen* in derselben Datei vermischen.

Aber hier ist der entscheidende Punkt.

Der Code für Sicherheit und Dependency Injection wird einmal geschrieben.

Sie können es so komplex gestalten, wie Sie möchten. Und dennoch haben Sie es nur einmal geschrieben, an einer einzigen Stelle. Mit all der Flexibilität.

Aber Sie können Tausende von Endpunkten (*Pfadoperationen*) haben, die dasselbe Sicherheitssystem verwenden.

Und alle (oder beliebige Teile davon) können Vorteil ziehen aus der Wiederverwendung dieser und anderer von Ihnen erstellter Abhängigkeiten.

Und alle diese Tausenden von *Pfadoperationen* können nur drei Zeilen lang sein:

{* ../../docs_src/security/tutorial002_an_py310.py hl[30:32] *}

## Zusammenfassung { #recap }

Sie können jetzt den aktuellen Benutzer direkt in Ihrer *Pfadoperation-Funktion* abrufen.

Wir haben bereits die Hälfte geschafft.

Wir müssen jetzt nur noch eine *Pfadoperation* hinzufügen, mittels der der Benutzer/Client tatsächlich seinen `username` und `password` senden kann.

Das kommt als nächstes.
