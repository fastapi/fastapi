# Header-Parameter-Modelle

Wenn Sie eine Gruppe von verwandten **Header-Parametern** haben, können Sie ein **Pydantic-Modell** erstellen, um diese zu deklarieren.

Dies ermöglicht es Ihnen, das **Modell wiederzuverwenden** in **mehreren Stellen** und auch Validierungen und Metadaten für alle Parameter auf einmal zu deklarieren. 😎

/// note | Hinweis

Dies wird seit FastAPI-Version `0.115.0` unterstützt. 🤓

///

## Header-Parameter mit einem Pydantic-Modell

Deklarieren Sie die **Header-Parameter**, die Sie benötigen, in einem **Pydantic-Modell** und dann den Parameter als `Header`:

{* ../../docs_src/header_param_models/tutorial001_an_py310.py hl[9:14,18] *}

**FastAPI** wird die Daten für **jedes Feld** aus den **Headers** in der Anfrage **extrahieren** und Ihnen das definierte Pydantic-Modell übergeben.

## Überprüfen Sie die Dokumentation

Sie können die erforderlichen Headers in der Dokumentationsoberfläche unter `/docs` sehen:

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## Zusätzliche Headers verbieten

In einigen speziellen Anwendungsfällen (wahrscheinlich nicht sehr häufig) möchten Sie möglicherweise die **Headers einschränken**, die Sie empfangen möchten.

Sie können die Modellkonfiguration von Pydantic verwenden, um `zusätzliche` Felder zu `verbieten`:

{* ../../docs_src/header_param_models/tutorial002_an_py310.py hl[10] *}

Wenn ein Client versucht, einige **zusätzliche Headers** zu senden, erhalten sie eine **Error-Response**.

Zum Beispiel, wenn der Client versucht, einen `tool`-Header mit dem Wert `plumbus` zu senden, erhalten sie eine **Error-Response**, die ihnen mitteilt, dass der Header-Parameter `tool` nicht erlaubt ist:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## Automatische Konvertierung von Unterstrichen deaktivieren

Genauso wie bei regulären Header-Parametern, werden bei der Verwendung von Unterstrich-Zeichen in den Parameternamen diese **automatisch in Bindestriche umgewandelt**.

Zum Beispiel, wenn Sie einen Header-Parameter `save_data` im Code haben, wird der erwartete HTTP-Header `save-data` sein, und er wird auch so in der Dokumentation erscheinen.

Wenn Sie aus irgendeinem Grund diese automatische Konvertierung deaktivieren müssen, können Sie dies auch für Pydantic-Modelle für Header-Parameter tun.

{* ../../docs_src/header_param_models/tutorial003_an_py310.py hl[19] *}

/// warning | Achtung

Bevor Sie `convert_underscores` auf `False` setzen, bedenken Sie, dass einige HTTP-Proxies und Server die Verwendung von Headers mit Unterstrichen nicht zulassen.

///

## Zusammenfassung

Sie können **Pydantic-Modelle** verwenden, um **Headers** in **FastAPI** zu deklarieren. 😎
