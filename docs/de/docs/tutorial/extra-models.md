# Extramodelle

Fahren wir beim letzten Beispiel fort. Es gibt normalerweise mehrere zusammengehörende Modelle.

Insbesondere Benutzermodelle, denn:

* Das **hereinkommende Modell** sollte ein Passwort haben können.
* Das **herausgehende Modell** sollte kein Passwort haben.
* Das **Datenbankmodell** sollte wahrscheinlich ein <abbr title='Ein aus scheinbar zufälligen Zeichen bestehender „Fingerabdruck“ eines Textes. Der Inhalt des Textes kann nicht eingesehen werden.'>gehashtes</abbr> Passwort haben.

/// danger | "Gefahr"

Speichern Sie niemals das Klartext-Passwort eines Benutzers. Speichern Sie immer den „sicheren Hash“, den Sie verifizieren können.

Falls Ihnen das nichts sagt, in den [Sicherheits-Kapiteln](security/simple-oauth2.md#passwort-hashing){.internal-link target=_blank} werden Sie lernen, was ein „Passwort-Hash“ ist.

///

## Mehrere Modelle

Hier der generelle Weg, wie die Modelle mit ihren Passwort-Feldern aussehen könnten, und an welchen Orten sie verwendet werden würden.

//// tab | Python 3.10+

```Python hl_lines="7  9  14  20  22  27-28  31-33  38-39"
{!> ../../../docs_src/extra_models/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9  11  16  22  24  29-30  33-35  40-41"
{!> ../../../docs_src/extra_models/tutorial001.py!}
```

////

/// info

In Pydantic v1 hieß diese Methode `.dict()`, in Pydantic v2 wurde sie deprecated (aber immer noch unterstützt) und in `.model_dump()` umbenannt.

Die Beispiele hier verwenden `.dict()` für die Kompatibilität mit Pydantic v1, Sie sollten jedoch stattdessen `.model_dump()` verwenden, wenn Sie Pydantic v2 verwenden können.

///

### Über `**user_in.dict()`

#### Pydantic's `.dict()`

`user_in` ist ein Pydantic-Modell der Klasse `UserIn`.

Pydantic-Modelle haben eine `.dict()`-Methode, die ein `dict` mit den Daten des Modells zurückgibt.

Wenn wir also ein Pydantic-Objekt `user_in` erstellen, etwa so:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

und wir rufen seine `.dict()`-Methode auf:

```Python
user_dict = user_in.dict()
```

dann haben wir jetzt in der Variable `user_dict` ein `dict` mit den gleichen Daten (es ist ein `dict` statt eines Pydantic-Modellobjekts).

Wenn wir es ausgeben:

```Python
print(user_dict)
```

bekommen wir ein Python-`dict`:

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### Ein `dict` entpacken

Wenn wir ein `dict` wie `user_dict` nehmen, und es einer Funktion (oder Klassenmethode) mittels `**user_dict` übergeben, wird Python es „entpacken“. Es wird die Schlüssel und Werte von `user_dict` direkt als Schlüsselwort-Argumente übergeben.

Wenn wir also das `user_dict` von oben nehmen und schreiben:

```Python
UserInDB(**user_dict)
```

dann ist das ungefähr äquivalent zu:

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

Oder, präziser, `user_dict` wird direkt verwendet, welche Werte es auch immer haben mag:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### Ein Pydantic-Modell aus den Inhalten eines anderen erstellen.

Da wir in obigem Beispiel `user_dict` mittels `user_in.dict()` erzeugt haben, ist dieser Code:

```Python
user_dict = user_in.dict()
UserInDB(**user_dict)
```

äquivalent zu:

```Python
UserInDB(**user_in.dict())
```

... weil `user_in.dict()` ein `dict` ist, und dann lassen wir Python es „entpacken“, indem wir es `UserInDB` übergeben, mit vorangestelltem `**`.

Wir erhalten also ein Pydantic-Modell aus den Daten eines anderen Pydantic-Modells.

#### Ein `dict` entpacken und zusätzliche Schlüsselwort-Argumente

Und dann fügen wir ein noch weiteres Schlüsselwort-Argument hinzu, `hashed_password=hashed_password`:

```Python
UserInDB(**user_in.dict(), hashed_password=hashed_password)
```

... was am Ende ergibt:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

/// warning | "Achtung"

Die Hilfsfunktionen `fake_password_hasher` und `fake_save_user` demonstrieren nur den möglichen Fluss der Daten und bieten natürlich keine echte Sicherheit.

///

## Verdopplung vermeiden

Reduzierung von Code-Verdoppelung ist eine der Kern-Ideen von **FastAPI**.

Weil Verdoppelung von Code die Wahrscheinlichkeit von Fehlern, Sicherheitsproblemen, Desynchronisation (Code wird nur an einer Stelle verändert, aber nicht an einer anderen), usw. erhöht.

Unsere Modelle teilen alle eine Menge der Daten und verdoppeln Attribut-Namen und -Typen.

Das können wir besser machen.

Wir deklarieren ein `UserBase`-Modell, das als Basis für unsere anderen Modelle dient. Dann können wir Unterklassen erstellen, die seine Attribute (Typdeklarationen, Validierungen, usw.) erben.

Die ganze Datenkonvertierung, -validierung, -dokumentation, usw. wird immer noch wie gehabt funktionieren.

Auf diese Weise beschreiben wir nur noch die Unterschiede zwischen den Modellen (mit Klartext-`password`, mit `hashed_password`, und ohne Passwort):

//// tab | Python 3.10+

```Python hl_lines="7  13-14  17-18  21-22"
{!> ../../../docs_src/extra_models/tutorial002_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9  15-16  19-20  23-24"
{!> ../../../docs_src/extra_models/tutorial002.py!}
```

////

## `Union`, oder `anyOf`

Sie können deklarieren, dass eine Response eine <abbr title="Union – Verbund, Einheit‚ Vereinigung: Eines von Mehreren">`Union`</abbr> mehrerer Typen ist, sprich, einer dieser Typen.

Das wird in OpenAPI mit `anyOf` angezeigt.

Um das zu tun, verwenden Sie Pythons Standard-Typhinweis <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>:

/// note | "Hinweis"

Listen Sie, wenn Sie eine <a href="https://pydantic-docs.helpmanual.io/usage/types/#unions" class="external-link" target="_blank">`Union`</a> definieren, denjenigen Typ zuerst, der am spezifischsten ist, gefolgt von den weniger spezifischen Typen. Im Beispiel oben, in `Union[PlaneItem, CarItem]` also den spezifischeren `PlaneItem` vor dem weniger spezifischen `CarItem`.

///

//// tab | Python 3.10+

```Python hl_lines="1  14-15  18-20  33"
{!> ../../../docs_src/extra_models/tutorial003_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  14-15  18-20  33"
{!> ../../../docs_src/extra_models/tutorial003.py!}
```

////

### `Union` in Python 3.10

In diesem Beispiel übergeben wir dem Argument `response_model` den Wert `Union[PlaneItem, CarItem]`.

Da wir es als **Wert einem Argument überreichen**, statt es als **Typannotation** zu verwenden, müssen wir `Union` verwenden, selbst in Python 3.10.

Wenn es eine Typannotation gewesen wäre, hätten wir auch den vertikalen Trennstrich verwenden können, wie in:

```Python
some_variable: PlaneItem | CarItem
```

Aber wenn wir das in der Zuweisung `response_model=PlaneItem | CarItem` machen, erhalten wir eine Fehlermeldung, da Python versucht, eine **ungültige Operation** zwischen `PlaneItem` und `CarItem` durchzuführen, statt es als Typannotation zu interpretieren.

## Listen von Modellen

Genauso können Sie eine Response deklarieren, die eine Liste von Objekten ist.

Verwenden Sie dafür Pythons Standard `typing.List` (oder nur `list` in Python 3.9 und darüber):

//// tab | Python 3.9+

```Python hl_lines="18"
{!> ../../../docs_src/extra_models/tutorial004_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  20"
{!> ../../../docs_src/extra_models/tutorial004.py!}
```

////

## Response mit beliebigem `dict`

Sie könne auch eine Response deklarieren, die ein beliebiges `dict` zurückgibt, bei dem nur die Typen der Schlüssel und der Werte bekannt sind, ohne ein Pydantic-Modell zu verwenden.

Das ist nützlich, wenn Sie die gültigen Feld-/Attribut-Namen von vorneherein nicht wissen (was für ein Pydantic-Modell notwendig ist).

In diesem Fall können Sie `typing.Dict` verwenden (oder nur `dict` in Python 3.9 und darüber):

//// tab | Python 3.9+

```Python hl_lines="6"
{!> ../../../docs_src/extra_models/tutorial005_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  8"
{!> ../../../docs_src/extra_models/tutorial005.py!}
```

////

## Zusammenfassung

Verwenden Sie gerne mehrere Pydantic-Modelle und vererben Sie je nach Bedarf.

Sie brauchen kein einzelnes Datenmodell pro Einheit, wenn diese Einheit verschiedene Zustände annehmen kann. So wie unsere Benutzer-„Einheit“, welche einen Zustand mit `password`, einen mit `password_hash` und einen ohne Passwort hatte.
