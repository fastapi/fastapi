# Formularmodelle { #form-models }

Sie können **Pydantic-Modelle** verwenden, um **Formularfelder** in FastAPI zu deklarieren.

/// info | Info

Um Formulare zu verwenden, installieren Sie zuerst [`python-multipart`](https://github.com/Kludex/python-multipart).

Stellen Sie sicher, dass Sie eine [Virtuelle Umgebung](../virtual-environments.md) erstellen, sie aktivieren und es dann installieren, zum Beispiel:

```console
$ pip install python-multipart
```

///

/// note | Hinweis

Dies wird seit FastAPI Version `0.113.0` unterstützt. 🤓

///

## Pydantic-Modelle für Formulare { #pydantic-models-for-forms }

Sie müssen nur ein **Pydantic-Modell** mit den Feldern deklarieren, die Sie als **Formularfelder** erhalten möchten, und dann den Parameter als `Form` deklarieren:

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI** wird die Daten für **jedes Feld** aus den **Formulardaten** im <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> **extrahieren** und Ihnen das von Ihnen definierte Pydantic-Modell übergeben.

## Die Dokumentation testen { #check-the-docs }

Sie können dies in der Dokumentations-UI unter `/docs` testen:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Zusätzliche Formularfelder verbieten { #forbid-extra-form-fields }

In einigen speziellen Anwendungsfällen (wahrscheinlich nicht sehr häufig) möchten Sie möglicherweise die Formularfelder auf nur diejenigen beschränken, die im Pydantic-Modell deklariert sind, und jegliche **zusätzlichen** Felder **verbieten**.

/// note | Hinweis

Dies wird seit FastAPI Version `0.114.0` unterstützt. 🤓

///

Sie können die Modellkonfiguration von Pydantic verwenden, um jegliche `extra` Felder zu `verbieten`:

{* ../../docs_src/request_form_models/tutorial002_an_py310.py hl[12] *}

Wenn ein Client versucht, einige zusätzliche Daten zu senden, erhält er eine **Error-<abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr>**.

Zum Beispiel, wenn der Client versucht, folgende Formularfelder zu senden:

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

erhält er eine Error-Response, die ihm mitteilt, dass das Feld `extra` nicht erlaubt ist:

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

## Zusammenfassung { #summary }

Sie können Pydantic-Modelle verwenden, um Formularfelder in FastAPI zu deklarieren. 😎
