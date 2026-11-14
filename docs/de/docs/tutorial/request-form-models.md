# Formularmodelle { #form-models }

Sie können **Pydantic-Modelle** verwenden, um **Formularfelder** in FastAPI zu deklarieren.

/// note | Hinweis

Um Formulare zu verwenden, installieren Sie zuerst [`python-multipart`](https://github.com/Kludex/python-multipart).

Fügen Sie es zu Ihrem Projekt hinzu:

```console
$ uv add python-multipart
```

///

/// note | Hinweis

Dies wird seit FastAPI Version `0.113.0` unterstützt. 🤓

///

## Pydantic-Modelle für Formulare { #pydantic-models-for-forms }

Sie müssen nur ein **Pydantic-Modell** mit den Feldern deklarieren, die Sie als **Formularfelder** erhalten möchten, und dann den Parameter als `Form` deklarieren:

{* ../../docs_src/request_form_models/tutorial001.py hl[9:11,15] *}

**FastAPI** wird die Daten für **jedes Feld** aus den **Formulardaten** im <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> **extrahieren** und Ihnen das von Ihnen definierte Pydantic-Modell übergeben.

Deklarieren Sie für [HTML-Checkboxen](request-forms.md#boolean-form-fields) boolesche Felder mit dem Defaultwert `False`.

## Die Dokumentation testen { #check-the-docs }

Sie können dies in der Dokumentations-UI unter `/docs` testen:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Zusätzliche Formularfelder verbieten { #forbid-extra-form-fields }

In einigen speziellen Anwendungsfällen (wahrscheinlich nicht sehr häufig) möchten Sie möglicherweise die Formularfelder auf nur diejenigen **beschränken**, die im Pydantic-Modell deklariert sind. Und jegliche **zusätzlichen** Felder **verbieten**.

/// note | Hinweis

Dies wird seit FastAPI Version `0.114.0` unterstützt. 🤓

///

Sie können Pydantics Modellkonfiguration verwenden, um jegliche `extra`-Felder auf `forbid` zu setzen:

{* ../../docs_src/request_form_models/tutorial002.py hl[12] *}

Wenn ein Client versucht, einige zusätzliche Daten zu senden, erhält er eine **Error**-<abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr>.

Zum Beispiel, wenn der Client versucht, folgende Formularfelder zu senden:

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

Er erhält eine Error-Response, die ihm mitteilt, dass das Feld `extra` nicht erlaubt ist:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## Formularmodelle kombinieren { #combine-form-models }

Sie können mehrere Formularmodelle mit einzelnen `Form`-Parametern kombinieren.

{* ../../docs_src/request_form_models/tutorial003.py hl[9:14,19:21] *}

Der Client sendet `name`, `tags` und `token` als Formularfelder. Jedes Modell validiert die Formularfelder unabhängig.

Die `extra`-Konfiguration jedes Modells gilt für alle Formularfelder, einschließlich der Felder und Dateien, die in anderen Parametern oder Abhängigkeiten deklariert sind. Mit `extra="forbid"` wird jedes Feld außerhalb dieses Modells abgelehnt. Mit `extra="allow"` werden diese Felder als zusätzliche Felder im Modell aufgenommen.

Wenn mehrere Deklarationen denselben Formularfeldnamen verwenden, validiert jede den Wert dieses Feldes. Verwenden Sie kompatible Typen und Einschränkungen für gemeinsam genutzte Felder, damit das OpenAPI-Schema sie konsistent beschreiben kann.

## Optionale Formularmodelle { #optional-form-models }

Deklarieren Sie ein Formularmodell mit `| None` und dem Defaultwert `None`, um die Gruppe optional zu machen.

{* ../../docs_src/request_form_models/tutorial005.py hl[17] *}

Wenn weder `name` noch `age` gesendet wird, ist `profile` gleich `None`. Wenn eines der beiden gesendet wird, validiert FastAPI das Modell und erfordert beide Felder. Auch ein übermittelter leerer Wert zählt als Angabe eines Feldes.

Die Verwendung von `| None` ohne Defaultwert macht den Parameter weiterhin erforderlich.

Zusätzliche Felder folgen der `extra`-Konfiguration des Modells. Ignorierte zusätzliche Felder führen nicht dazu, dass das Modell als vorhanden gilt.

Ein optionales Modell, das nur nicht aktivierte Checkboxen enthält, wird weggelassen. Senden Sie einen Wert wie `enabled=false`, um es explizit anzugeben.

## Optionale Unions von Formularmodellen { #optional-unions-of-form-models }

Sie können auch eine optionale Union von Modellen verwenden.

{* ../../docs_src/request_form_models/tutorial006.py hl[9:16,21] *}

Wenn keine Formularfelder gesendet werden, ist `contact` gleich `None`. Senden Sie `kind=person` mit `name` oder `kind=company` mit `company_name`. Der Diskriminator wählt aus, welches Modell validiert werden soll.

## Unions von Formularmodellen kombinieren { #combine-unions-of-form-models }

Sie können Unions mit anderen Formularmodellen, einzelnen `Form`-Parametern und `File`-Parametern kombinieren. Jede Union wird unabhängig validiert.

{* ../../docs_src/request_form_models/tutorial007.py hl[31:35] *}

Senden Sie alle Felder im selben Formular. Senden Sie beispielsweise `contact_type=person`, `name=Rick`, `notification_type=email`, `email=rick@example.com` und `token=secret`.

Lassen Sie die Benachrichtigungsfelder weg, damit `notification` gleich `None` bleibt.

## Formularmodelle und Dateien { #form-models-and-files }

Sie können ein Formularmodell auch mit [Dateiparametern](request-files.md) kombinieren.

{* ../../docs_src/request_form_models/tutorial004.py hl[14] *}

Hier sendet der Client das Feld `name` und die Datei `avatar` mittels `multipart/form-data`.

## Zusammenfassung { #summary }

Sie können Pydantic-Modelle verwenden, um Formularfelder in FastAPI zu deklarieren. 😎
