# Body – Aktualisierungen

## Ersetzendes Aktualisieren mit `PUT`

Um einen Artikel zu aktualisieren, können Sie die <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">HTTP `PUT`</a> Operation verwenden.

Sie können den `jsonable_encoder` verwenden, um die empfangenen Daten in etwas zu konvertieren, das als JSON gespeichert werden kann (in z. B. einer NoSQL-Datenbank). Zum Beispiel, um ein `datetime` in einen `str` zu konvertieren.

//// tab | Python 3.10+

```Python hl_lines="28-33"
{!> ../../../docs_src/body_updates/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="30-35"
{!> ../../../docs_src/body_updates/tutorial001_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="30-35"
{!> ../../../docs_src/body_updates/tutorial001.py!}
```

////

`PUT` wird verwendet, um Daten zu empfangen, die die existierenden Daten ersetzen sollen.

### Warnung bezüglich des Ersetzens

Das bedeutet, dass, wenn Sie den Artikel `bar` aktualisieren wollen, mittels `PUT` und folgendem Body:

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

das Eingabemodell nun den Defaultwert `"tax": 10.5` hat, weil Sie das bereits gespeicherte Attribut `"tax": 20.2` nicht mit übergeben haben.

Die Daten werden darum mit einem „neuen“ `tax`-Wert von `10.5` abgespeichert.

## Teilweises Ersetzen mit `PATCH`

Sie können auch die <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">HTTP `PATCH`</a> Operation verwenden, um Daten *teilweise* zu ersetzen.

Das bedeutet, sie senden nur die Daten, die Sie aktualisieren wollen, der Rest bleibt unverändert.

/// note | "Hinweis"

`PATCH` wird seltener verwendet und ist weniger bekannt als `PUT`.

Und viele Teams verwenden ausschließlich `PUT`, selbst für nur Teil-Aktualisierungen.

Es steht Ihnen **frei**, das zu verwenden, was Sie möchten, **FastAPI** legt Ihnen keine Einschränkungen auf.

Aber dieser Leitfaden zeigt Ihnen mehr oder weniger, wie die beiden normalerweise verwendet werden.

///

### Pydantics `exclude_unset`-Parameter verwenden

Wenn Sie Teil-Aktualisierungen entgegennehmen, ist der `exclude_unset`-Parameter in der `.model_dump()`-Methode von Pydantic-Modellen sehr nützlich.

Wie in `item.model_dump(exclude_unset=True)`.

/// info

In Pydantic v1 hieß diese Methode `.dict()`, in Pydantic v2 wurde sie deprecated (aber immer noch unterstützt) und in `.model_dump()` umbenannt.

Die Beispiele hier verwenden `.dict()` für die Kompatibilität mit Pydantic v1, Sie sollten jedoch stattdessen `.model_dump()` verwenden, wenn Sie Pydantic v2 verwenden können.

///

Das wird ein `dict` erstellen, mit nur den Daten, die gesetzt wurden als das `item`-Modell erstellt wurde, Defaultwerte ausgeschlossen.

Sie können das verwenden, um ein `dict` zu erstellen, das nur die (im Request) gesendeten Daten enthält, ohne Defaultwerte:

//// tab | Python 3.10+

```Python hl_lines="32"
{!> ../../../docs_src/body_updates/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="34"
{!> ../../../docs_src/body_updates/tutorial002_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="34"
{!> ../../../docs_src/body_updates/tutorial002.py!}
```

////

### Pydantics `update`-Parameter verwenden

Jetzt können Sie eine Kopie des existierenden Modells mittels `.model_copy()` erstellen, wobei Sie dem `update`-Parameter ein `dict` mit den zu ändernden Daten übergeben.

/// info

In Pydantic v1 hieß diese Methode `.copy()`, in Pydantic v2 wurde sie deprecated (aber immer noch unterstützt) und in `.model_copy()` umbenannt.

Die Beispiele hier verwenden `.copy()` für die Kompatibilität mit Pydantic v1, Sie sollten jedoch stattdessen `.model_copy()` verwenden, wenn Sie Pydantic v2 verwenden können.

///

Wie in `stored_item_model.model_copy(update=update_data)`:

//// tab | Python 3.10+

```Python hl_lines="33"
{!> ../../../docs_src/body_updates/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="35"
{!> ../../../docs_src/body_updates/tutorial002_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="35"
{!> ../../../docs_src/body_updates/tutorial002.py!}
```

////

### Rekapitulation zum teilweisen Ersetzen

Zusammengefasst, um Teil-Ersetzungen vorzunehmen:

* (Optional) verwenden Sie `PATCH` statt `PUT`.
* Lesen Sie die bereits gespeicherten Daten aus.
* Fügen Sie diese in ein Pydantic-Modell ein.
* Erzeugen Sie aus dem empfangenen Modell ein `dict` ohne Defaultwerte (mittels `exclude_unset`).
    * So ersetzen Sie nur die tatsächlich vom Benutzer gesetzten Werte, statt dass bereits gespeicherte Werte mit Defaultwerten des Modells überschrieben werden.
* Erzeugen Sie eine Kopie ihres gespeicherten Modells, wobei Sie die Attribute mit den empfangenen Teil-Ersetzungen aktualisieren (mittels des `update`-Parameters).
* Konvertieren Sie das kopierte Modell zu etwas, das in ihrer Datenbank gespeichert werden kann (indem Sie beispielsweise `jsonable_encoder` verwenden).
    * Das ist vergleichbar dazu, die `.model_dump()`-Methode des Modells erneut aufzurufen, aber es wird sicherstellen, dass die Werte zu Daten konvertiert werden, die ihrerseits zu JSON konvertiert werden können, zum Beispiel `datetime` zu `str`.
* Speichern Sie die Daten in Ihrer Datenbank.
* Geben Sie das aktualisierte Modell zurück.

//// tab | Python 3.10+

```Python hl_lines="28-35"
{!> ../../../docs_src/body_updates/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="30-37"
{!> ../../../docs_src/body_updates/tutorial002_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="30-37"
{!> ../../../docs_src/body_updates/tutorial002.py!}
```

////

/// tip | "Tipp"

Sie können tatsächlich die gleiche Technik mit einer HTTP `PUT` Operation verwenden.

Aber dieses Beispiel verwendet `PATCH`, da dieses für solche Anwendungsfälle geschaffen wurde.

///

/// note | "Hinweis"

Beachten Sie, dass das hereinkommende Modell immer noch validiert wird.

Wenn Sie also Teil-Aktualisierungen empfangen wollen, die alle Attribute auslassen können, müssen Sie ein Modell haben, dessen Attribute alle als optional gekennzeichnet sind (mit Defaultwerten oder `None`).

Um zu unterscheiden zwischen Modellen für **Aktualisierungen**, mit lauter optionalen Werten, und solchen für die **Erzeugung**, mit benötigten Werten, können Sie die Techniken verwenden, die in [Extramodelle](extra-models.md){.internal-link target=_blank} beschrieben wurden.

///
