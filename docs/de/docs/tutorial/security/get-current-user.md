# Aktuellen Benutzer abrufen

Im vorherigen Kapitel hat das Sicherheitssystem (das auf dem Dependency Injection System basiert) der *Pfadoperation-Funktion* einen `token` vom Typ `str` überreicht:

//// tab | Python 3.9+

```Python hl_lines="12"
{!> ../../../docs_src/security/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11"
{!> ../../../docs_src/security/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="10"
{!> ../../../docs_src/security/tutorial001.py!}
```

////

Aber das ist immer noch nicht so nützlich.

Lassen wir es uns den aktuellen Benutzer überreichen.

## Ein Benutzermodell erstellen

Erstellen wir zunächst ein Pydantic-Benutzermodell.

So wie wir Pydantic zum Deklarieren von Bodys verwenden, können wir es auch überall sonst verwenden:

//// tab | Python 3.10+

```Python hl_lines="5  12-16"
{!> ../../../docs_src/security/tutorial002_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="5  12-16"
{!> ../../../docs_src/security/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="5  13-17"
{!> ../../../docs_src/security/tutorial002_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="3  10-14"
{!> ../../../docs_src/security/tutorial002_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="5  12-16"
{!> ../../../docs_src/security/tutorial002.py!}
```

////

## Eine `get_current_user`-Abhängigkeit erstellen

Erstellen wir eine Abhängigkeit `get_current_user`.

Erinnern Sie sich, dass Abhängigkeiten Unterabhängigkeiten haben können?

`get_current_user` wird seinerseits von `oauth2_scheme` abhängen, das wir zuvor erstellt haben.

So wie wir es zuvor in der *Pfadoperation* direkt gemacht haben, erhält unsere neue Abhängigkeit `get_current_user` von der Unterabhängigkeit `oauth2_scheme` einen `token` vom Typ `str`:

//// tab | Python 3.10+

```Python hl_lines="25"
{!> ../../../docs_src/security/tutorial002_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="25"
{!> ../../../docs_src/security/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="26"
{!> ../../../docs_src/security/tutorial002_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="23"
{!> ../../../docs_src/security/tutorial002_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="25"
{!> ../../../docs_src/security/tutorial002.py!}
```

////

## Den Benutzer holen

`get_current_user` wird eine von uns erstellte (gefakte) Hilfsfunktion verwenden, welche einen Token vom Typ `str` entgegennimmt und unser Pydantic-`User`-Modell zurückgibt:

//// tab | Python 3.10+

```Python hl_lines="19-22  26-27"
{!> ../../../docs_src/security/tutorial002_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="19-22  26-27"
{!> ../../../docs_src/security/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="20-23  27-28"
{!> ../../../docs_src/security/tutorial002_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="17-20  24-25"
{!> ../../../docs_src/security/tutorial002_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="19-22  26-27"
{!> ../../../docs_src/security/tutorial002.py!}
```

////

## Den aktuellen Benutzer einfügen

Und jetzt können wir wiederum `Depends` mit unserem `get_current_user` in der *Pfadoperation* verwenden:

//// tab | Python 3.10+

```Python hl_lines="31"
{!> ../../../docs_src/security/tutorial002_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="31"
{!> ../../../docs_src/security/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="32"
{!> ../../../docs_src/security/tutorial002_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="29"
{!> ../../../docs_src/security/tutorial002_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="31"
{!> ../../../docs_src/security/tutorial002.py!}
```

////

Beachten Sie, dass wir als Typ von `current_user` das Pydantic-Modell `User` deklarieren.

Das wird uns innerhalb der Funktion bei Codevervollständigung und Typprüfungen helfen.

/// tip | "Tipp"

Sie erinnern sich vielleicht, dass Requestbodys ebenfalls mit Pydantic-Modellen deklariert werden.

Weil Sie `Depends` verwenden, wird **FastAPI** hier aber nicht verwirrt.

///

/// check

Die Art und Weise, wie dieses System von Abhängigkeiten konzipiert ist, ermöglicht es uns, verschiedene Abhängigkeiten (verschiedene „Dependables“) zu haben, die alle ein `User`-Modell zurückgeben.

Wir sind nicht darauf beschränkt, nur eine Abhängigkeit zu haben, die diesen Typ von Daten zurückgeben kann.

///

## Andere Modelle

Sie können jetzt den aktuellen Benutzer direkt in den *Pfadoperation-Funktionen* abrufen und die Sicherheitsmechanismen auf **Dependency Injection** Ebene handhaben, mittels `Depends`.

Und Sie können alle Modelle und Daten für die Sicherheitsanforderungen verwenden (in diesem Fall ein Pydantic-Modell `User`).

Sie sind jedoch nicht auf die Verwendung von bestimmten Datenmodellen, Klassen, oder Typen beschränkt.

Möchten Sie eine `id` und eine `email` und keinen `username` in Ihrem Modell haben? Kein Problem. Sie können dieselben Tools verwenden.

Möchten Sie nur ein `str` haben? Oder nur ein `dict`? Oder direkt eine Instanz eines Modells einer Datenbank-Klasse? Es funktioniert alles auf die gleiche Weise.

Sie haben eigentlich keine Benutzer, die sich bei Ihrer Anwendung anmelden, sondern Roboter, Bots oder andere Systeme, die nur über einen Zugriffstoken verfügen? Auch hier funktioniert alles gleich.

Verwenden Sie einfach jede Art von Modell, jede Art von Klasse, jede Art von Datenbank, die Sie für Ihre Anwendung benötigen. **FastAPI** deckt das alles mit seinem Dependency Injection System ab.

## Codegröße

Dieses Beispiel mag ausführlich erscheinen. Bedenken Sie, dass wir Sicherheit, Datenmodelle, Hilfsfunktionen und *Pfadoperationen* in derselben Datei vermischen.

Aber hier ist der entscheidende Punkt.

Der Code für Sicherheit und Dependency Injection wird einmal geschrieben.

Sie können es so komplex gestalten, wie Sie möchten. Und dennoch haben Sie es nur einmal geschrieben, an einer einzigen Stelle. Mit all der Flexibilität.

Aber Sie können Tausende von Endpunkten (*Pfadoperationen*) haben, die dasselbe Sicherheitssystem verwenden.

Und alle (oder beliebige Teile davon) können Vorteil ziehen aus der Wiederverwendung dieser und anderer von Ihnen erstellter Abhängigkeiten.

Und alle diese Tausenden von *Pfadoperationen* können nur drei Zeilen lang sein:

//// tab | Python 3.10+

```Python hl_lines="30-32"
{!> ../../../docs_src/security/tutorial002_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="30-32"
{!> ../../../docs_src/security/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="31-33"
{!> ../../../docs_src/security/tutorial002_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="28-30"
{!> ../../../docs_src/security/tutorial002_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="30-32"
{!> ../../../docs_src/security/tutorial002.py!}
```

////

## Zusammenfassung

Sie können jetzt den aktuellen Benutzer direkt in Ihrer *Pfadoperation-Funktion* abrufen.

Wir haben bereits die Hälfte geschafft.

Wir müssen jetzt nur noch eine *Pfadoperation* hinzufügen, mittels der der Benutzer/Client tatsächlich seinen `username` und `password` senden kann.

Das kommt als nächstes.
