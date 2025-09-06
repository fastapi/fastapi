# Extramodelle { #extra-models }

Im Anschluss an das vorherige Beispiel ist es üblich, mehr als ein zusammenhängendes Modell zu haben.

Dies gilt insbesondere für Benutzermodelle, denn:

* Das **Eingabemodell** muss ein Passwort enthalten können.
* Das **Ausgabemodell** sollte kein Passwort haben.
* Das **Datenbankmodell** müsste wahrscheinlich ein gehashtes Passwort haben.

/// danger | Gefahr

Speichern Sie niemals das Klartextpasswort eines Benutzers. Speichern Sie immer einen „sicheren Hash“, den Sie dann verifizieren können.

Wenn Sie nicht wissen, was das ist, werden Sie in den [Sicherheitskapiteln](security/simple-oauth2.md#password-hashing){.internal-link target=_blank} lernen, was ein „Passworthash“ ist.

///

## Mehrere Modelle { #multiple-models }

Hier ist eine allgemeine Idee, wie die Modelle mit ihren Passwortfeldern aussehen könnten und an welchen Stellen sie verwendet werden:

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}

/// info | Info

In Pydantic v1 hieß die Methode `.dict()`, in Pydantic v2 wurde sie <abbr title="veraltet, obsolet: Es soll nicht mehr verwendet werden">deprecatet</abbr> (aber weiterhin unterstützt) und in `.model_dump()` umbenannt.

Die Beispiele hier verwenden `.dict()` für die Kompatibilität mit Pydantic v1, aber Sie sollten `.model_dump()` verwenden, wenn Sie Pydantic v2 verwenden können.

///

### Über `**user_in.dict()` { #about-user-in-dict }

#### Die `.dict()`-Methode von Pydantic { #pydantics-dict }

`user_in` ist ein Pydantic-Modell der Klasse `UserIn`.

Pydantic-Modelle haben eine `.dict()`-Methode, die ein <abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">`dict`</abbr> mit den Daten des Modells zurückgibt.

Wenn wir also ein Pydantic-Objekt `user_in` erstellen, etwa so:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

und dann aufrufen:

```Python
user_dict = user_in.dict()
```

haben wir jetzt ein `dict` mit den Daten in der Variablen `user_dict` (es ist ein `dict` statt eines Pydantic-Modellobjekts).

Und wenn wir aufrufen:

```Python
print(user_dict)
```

würden wir ein Python-`dict` erhalten mit:

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### Ein `dict` entpacken { #unpacking-a-dict }

Wenn wir ein `dict` wie `user_dict` nehmen und es einer Funktion (oder Klasse) mit `**user_dict` übergeben, wird Python es „entpacken“. Es wird die Schlüssel und Werte von `user_dict` direkt als Schlüsselwort-Argumente übergeben.

Setzen wir also das `user_dict` von oben ein:

```Python
UserInDB(**user_dict)
```

so ist das äquivalent zu:

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

Oder genauer gesagt, dazu, `user_dict` direkt zu verwenden, mit welchen Inhalten es auch immer in der Zukunft haben mag:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### Ein Pydantic-Modell aus dem Inhalt eines anderen { #a-pydantic-model-from-the-contents-of-another }

Da wir im obigen Beispiel `user_dict` von `user_in.dict()` bekommen haben, wäre dieser Code:

```Python
user_dict = user_in.dict()
UserInDB(**user_dict)
```

gleichwertig zu:

```Python
UserInDB(**user_in.dict())
```

... weil `user_in.dict()` ein `dict` ist, und dann lassen wir Python es „entpacken“, indem wir es an `UserInDB` mit vorangestelltem `**` übergeben.

Auf diese Weise erhalten wir ein Pydantic-Modell aus den Daten eines anderen Pydantic-Modells.

#### Ein `dict` entpacken und zusätzliche Schlüsselwort-Argumente { #unpacking-a-dict-and-extra-keywords }

Und dann fügen wir das zusätzliche Schlüsselwort-Argument `hashed_password=hashed_password` hinzu, wie in:

```Python
UserInDB(**user_in.dict(), hashed_password=hashed_password)
```

... was so ist wie:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

/// warning | Achtung

Die unterstützenden zusätzlichen Funktionen `fake_password_hasher` und `fake_save_user` dienen nur zur Demo eines möglichen Datenflusses, bieten jedoch natürlich keine echte Sicherheit.

///

## Verdopplung vermeiden { #reduce-duplication }

Die Reduzierung von Code-Verdoppelung ist eine der Kernideen von **FastAPI**.

Da die Verdopplung von Code die Wahrscheinlichkeit von Fehlern, Sicherheitsproblemen, Problemen mit der Desynchronisation des Codes (wenn Sie an einer Stelle, aber nicht an der anderen aktualisieren) usw. erhöht.

Und diese Modelle teilen alle eine Menge der Daten und verdoppeln Attributnamen und -typen.

Wir könnten es besser machen.

Wir können ein `UserBase`-Modell deklarieren, das als Basis für unsere anderen Modelle dient. Und dann können wir Unterklassen dieses Modells erstellen, die seine Attribute (Typdeklarationen, Validierung usw.) erben.

Die ganze Datenkonvertierung, -validierung, -dokumentation usw. wird immer noch wie gewohnt funktionieren.

Auf diese Weise können wir nur die Unterschiede zwischen den Modellen (mit Klartext-`password`, mit `hashed_password` und ohne Passwort) deklarieren:

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` oder `anyOf` { #union-or-anyof }

Sie können deklarieren, dass eine <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> eine <abbr title="Union – Verbund, Einheit, Vereinigung: Eines von Mehreren">`Union`</abbr> mehrerer Typen ist, das bedeutet, dass die Response einer von ihnen ist.

Dies wird in OpenAPI mit `anyOf` definiert.

Um das zu tun, verwenden Sie den Standard-Python-Typhinweis <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>:

/// note | Hinweis

Wenn Sie eine <a href="https://docs.pydantic.dev/latest/concepts/types/#unions" class="external-link" target="_blank">`Union`</a> definieren, listen Sie den spezifischeren Typ zuerst auf, gefolgt vom weniger spezifischen Typ. Im Beispiel unten steht `PlaneItem` vor `CarItem` in `Union[PlaneItem, CarItem]`.

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}


### `Union` in Python 3.10 { #union-in-python-3-10 }

In diesem Beispiel übergeben wir `Union[PlaneItem, CarItem]` als Wert des Arguments `response_model`.

Da wir es als **Wert an ein Argument übergeben**, anstatt es in einer **Typannotation** zu verwenden, müssen wir `Union` verwenden, sogar in Python 3.10.

Wäre es eine Typannotation gewesen, hätten wir den vertikalen Strich verwenden können, wie in:

```Python
some_variable: PlaneItem | CarItem
```

Aber wenn wir das in der Zuweisung `response_model=PlaneItem | CarItem` machen, würden wir einen Fehler erhalten, weil Python versuchen würde, eine **ungültige Operation** zwischen `PlaneItem` und `CarItem` auszuführen, anstatt es als Typannotation zu interpretieren.

## Liste von Modellen { #list-of-models }

Auf die gleiche Weise können Sie Responses von Listen von Objekten deklarieren.

Dafür verwenden Sie Pythons Standard-`typing.List` (oder nur `list` in Python 3.9 und höher):

{* ../../docs_src/extra_models/tutorial004_py39.py hl[18] *}


## Response mit beliebigem `dict` { #response-with-arbitrary-dict }

Sie können auch eine Response deklarieren, die ein beliebiges `dict` zurückgibt, indem Sie nur die Typen der Schlüssel und Werte ohne ein Pydantic-Modell deklarieren.

Dies ist nützlich, wenn Sie die gültigen Feld-/Attributnamen nicht im Voraus kennen (die für ein Pydantic-Modell benötigt werden würden).

In diesem Fall können Sie `typing.Dict` verwenden (oder nur `dict` in Python 3.9 und höher):

{* ../../docs_src/extra_models/tutorial005_py39.py hl[6] *}


## Zusammenfassung { #recap }

Verwenden Sie gerne mehrere Pydantic-Modelle und vererben Sie je nach Bedarf.

Sie brauchen kein einzelnes Datenmodell pro Einheit, wenn diese Einheit in der Lage sein muss, verschiedene „Zustände“ zu haben. Wie im Fall der Benutzer-„Einheit“ mit einem Zustand einschließlich `password`, `password_hash` und ohne Passwort.
