# Body – Aktualisierungen { #body-updates }

## Ersetzendes Aktualisieren mit `PUT` { #update-replacing-with-put }

Um einen Artikel zu aktualisieren, können Sie die <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">HTTP `PUT`</a> Operation verwenden.

Sie können den `jsonable_encoder` verwenden, um die empfangenen Daten in etwas zu konvertieren, das als JSON gespeichert werden kann (z. B. in einer NoSQL-Datenbank). Zum Beispiel, um ein `datetime` in einen `str` zu konvertieren.

{* ../../docs_src/body_updates/tutorial001_py310.py hl[28:33] *}

`PUT` wird verwendet, um Daten zu empfangen, die die existierenden Daten ersetzen sollen.

### Warnung bezüglich des Ersetzens { #warning-about-replacing }

Das bedeutet, dass, wenn Sie den Artikel `bar` aktualisieren wollen, mittels `PUT` und folgendem Body:

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

weil das bereits gespeicherte Attribut `"tax": 20.2` nicht enthalten ist, das Eingabemodell den Defaultwert `"tax": 10.5` erhalten würde.

Und die Daten würden mit diesem „neuen“ `tax` von `10.5` gespeichert werden.

## Teil-Aktualisierungen mit `PATCH` { #partial-updates-with-patch }

Sie können auch die <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">HTTP `PATCH`</a> Operation verwenden, um Daten *teilweise* zu ersetzen.

Das bedeutet, Sie senden nur die Daten, die Sie aktualisieren wollen, der Rest bleibt unverändert.

/// note | Hinweis

`PATCH` wird seltener verwendet und ist weniger bekannt als `PUT`.

Und viele Teams verwenden ausschließlich `PUT`, selbst für nur Teil-Aktualisierungen.

Es steht Ihnen **frei**, das zu verwenden, was Sie möchten, **FastAPI** legt Ihnen keine Einschränkungen auf.

Aber dieser Leitfaden zeigt Ihnen mehr oder weniger, wie die beiden normalerweise verwendet werden.

///

### Pydantics `exclude_unset`-Parameter verwenden { #using-pydantics-exclude-unset-parameter }

Wenn Sie Teil-Aktualisierungen entgegennehmen, ist der `exclude_unset`-Parameter in der `.model_dump()`-Methode von Pydantic-Modellen sehr nützlich.

Wie in `item.model_dump(exclude_unset=True)`.

/// info | Info

In Pydantic v1 hieß diese Methode `.dict()`, in Pydantic v2 wurde sie <abbr title="veraltet, obsolet: Es soll nicht mehr verwendet werden">deprecatet</abbr> (aber immer noch unterstützt) und in `.model_dump()` umbenannt.

Die Beispiele hier verwenden `.dict()` für die Kompatibilität mit Pydantic v1, Sie sollten jedoch stattdessen `.model_dump()` verwenden, wenn Sie Pydantic v2 verwenden können.

///

Das wird ein <abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">`dict`</abbr> erstellen, mit nur den Daten, die gesetzt wurden, als das `item`-Modell erstellt wurde, Defaultwerte ausgeschlossen.

Sie können das verwenden, um ein `dict` zu erstellen, das nur die (im <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr>) gesendeten Daten enthält, ohne Defaultwerte:

{* ../../docs_src/body_updates/tutorial002_py310.py hl[32] *}

### Pydantics `update`-Parameter verwenden { #using-pydantics-update-parameter }

Jetzt können Sie eine Kopie des existierenden Modells mittels `.model_copy()` erstellen, wobei Sie dem `update`-Parameter ein `dict` mit den zu ändernden Daten übergeben.

/// info | Info

In Pydantic v1 hieß diese Methode `.copy()`, in Pydantic v2 wurde sie <abbr title="veraltet, obsolet: Es soll nicht mehr verwendet werden">deprecatet</abbr> (aber immer noch unterstützt) und in `.model_copy()` umbenannt.

Die Beispiele hier verwenden `.copy()` für die Kompatibilität mit Pydantic v1, Sie sollten jedoch stattdessen `.model_copy()` verwenden, wenn Sie Pydantic v2 verwenden können.

///

Wie in `stored_item_model.model_copy(update=update_data)`:

{* ../../docs_src/body_updates/tutorial002_py310.py hl[33] *}

### Rekapitulation zu Teil-Aktualisierungen { #partial-updates-recap }

Zusammengefasst, um Teil-Aktualisierungen vorzunehmen:

* (Optional) verwenden Sie `PATCH` statt `PUT`.
* Lesen Sie die bereits gespeicherten Daten aus.
* Fügen Sie diese in ein Pydantic-Modell ein.
* Erzeugen Sie aus dem empfangenen Modell ein `dict` ohne Defaultwerte (mittels `exclude_unset`).
    * So ersetzen Sie nur die tatsächlich vom Benutzer gesetzten Werte, statt dass bereits gespeicherte Werte mit Defaultwerten des Modells überschrieben werden.
* Erzeugen Sie eine Kopie ihres gespeicherten Modells, wobei Sie die Attribute mit den empfangenen Teil-Ersetzungen aktualisieren (mittels des `update`-Parameters).
* Konvertieren Sie das kopierte Modell zu etwas, das in Ihrer Datenbank gespeichert werden kann (indem Sie beispielsweise `jsonable_encoder` verwenden).
    * Das ist vergleichbar dazu, die `.model_dump()`-Methode des Modells erneut aufzurufen, aber es wird sicherstellen, dass die Werte zu Daten konvertiert werden, die ihrerseits zu JSON konvertiert werden können, zum Beispiel `datetime` zu `str`.
* Speichern Sie die Daten in Ihrer Datenbank.
* Geben Sie das aktualisierte Modell zurück.

{* ../../docs_src/body_updates/tutorial002_py310.py hl[28:35] *}

/// tip | Tipp

Sie können tatsächlich die gleiche Technik mit einer HTTP `PUT` Operation verwenden.

Aber dieses Beispiel verwendet `PATCH`, da dieses für solche Anwendungsfälle geschaffen wurde.

///

/// note | Hinweis

Beachten Sie, dass das hereinkommende Modell immer noch validiert wird.

Wenn Sie also Teil-Aktualisierungen empfangen wollen, die alle Attribute auslassen können, müssen Sie ein Modell haben, dessen Attribute alle als optional gekennzeichnet sind (mit Defaultwerten oder `None`).

Um zu unterscheiden zwischen Modellen für **Aktualisierungen**, mit lauter optionalen Werten, und solchen für die **Erzeugung**, mit benötigten Werten, können Sie die Techniken verwenden, die in [Extramodelle](extra-models.md){.internal-link target=_blank} beschrieben wurden.

///
