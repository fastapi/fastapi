# Header-Parameter-Modelle { #header-parameter-models }

Wenn Sie eine Gruppe verwandter **Header-Parameter** haben, können Sie ein **Pydantic-Modell** erstellen, um diese zu deklarieren.

Dadurch können Sie das **Modell an mehreren Stellen wiederverwenden** und auch Validierungen und Metadaten für alle Parameter gleichzeitig deklarieren. 😎

/// note | Hinweis

Dies wird seit FastAPI Version `0.115.0` unterstützt. 🤓

///

## Header-Parameter mit einem Pydantic-Modell { #header-parameters-with-a-pydantic-model }

Deklarieren Sie die erforderlichen **Header-Parameter** in einem **Pydantic-Modell** und dann den Parameter als `Header`:

{* ../../docs_src/header_param_models/tutorial001_an_py310.py hl[9:14,18] *}

**FastAPI** wird die Daten für **jedes Feld** aus den **Headern** des <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> extrahieren und Ihnen das von Ihnen definierte Pydantic-Modell geben.

## Die Dokumentation testen { #check-the-docs }

Sie können die erforderlichen Header in der Dokumentationsoberfläche unter `/docs` sehen:

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## Zusätzliche Header verbieten { #forbid-extra-headers }

In einigen speziellen Anwendungsfällen (wahrscheinlich nicht sehr häufig) möchten Sie möglicherweise die **Header einschränken**, die Sie erhalten möchten.

Sie können Pydantics Modellkonfiguration verwenden, um `extra` Felder zu verbieten (`forbid`):

{* ../../docs_src/header_param_models/tutorial002_an_py310.py hl[10] *}

Wenn ein Client versucht, einige **zusätzliche Header** zu senden, erhält er eine **Error-<abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr>**.

Zum Beispiel, wenn der Client versucht, einen `tool`-Header mit einem Wert von `plumbus` zu senden, erhält er eine **Error-Response**, die ihm mitteilt, dass der Header-Parameter `tool` nicht erlaubt ist:

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

## Automatische Umwandlung von Unterstrichen deaktivieren { #disable-convert-underscores }

Ähnlich wie bei regulären Header-Parametern werden bei der Verwendung von Unterstrichen in den Parameternamen diese **automatisch in Bindestriche umgewandelt**.

Wenn Sie beispielsweise einen Header-Parameter `save_data` im Code haben, wird der erwartete HTTP-Header `save-data` sein, und er wird auch so in der Dokumentation angezeigt.

Falls Sie aus irgendeinem Grund diese automatische Umwandlung deaktivieren müssen, können Sie dies auch für Pydantic-Modelle für Header-Parameter tun.

{* ../../docs_src/header_param_models/tutorial003_an_py310.py hl[19] *}

/// warning | Achtung

Bevor Sie `convert_underscores` auf `False` setzen, bedenken Sie, dass einige HTTP-Proxies und -Server die Verwendung von Headern mit Unterstrichen nicht zulassen.

///

## Parametermodelle kombinieren { #combine-parameter-models }

Sie können mehrere Header-Parameter-Modelle mit einzelnen Header-Parametern und Abhängigkeiten kombinieren. Jedes Modell wird unabhängig extrahiert und validiert, wie für [Query-Parameter-Modelle](query-param-models.md#combine-parameter-models) erklärt.

Die `extra`-Konfiguration jedes Modells gilt für alle Header-Parameter, einschließlich derjenigen, die in anderen Modellen oder Abhängigkeiten deklariert sind. Mit `extra="forbid"` wird jeder Header außerhalb dieses Modells abgelehnt. Mit `extra="allow"` werden diese Header als zusätzliche Felder des Modells aufgenommen.

Jedes Modell verwendet seine eigene Einstellung für `Header(convert_underscores=...)`, sowohl beim Lesen des Requests als auch beim Generieren von OpenAPI. Explizite Feld-Aliasse bleiben unveränderte Headernamen.

## Optionale Header-Parameter-Modelle { #optional-header-parameter-models }

Deklarieren Sie ein Header-Parameter-Modell mit `| None` und einem Defaultwert von `None`, um die Gruppe optional zu machen.

{* ../../docs_src/header_param_models/tutorial004_an_py310.py hl[15] *}

Wenn weder `x-client-name` noch `x-client-version` gesendet wird, ist `client` gleich `None`. Wenn einer von beiden gesendet wird, validiert FastAPI das Modell und erfordert beide Felder.

Es gelten dieselben Regeln für Defaultwerte, zusätzliche Felder und OpenAPI wie für [optionale Query-Parameter-Modelle](query-param-models.md#optional-query-parameter-models).

Header wie `Host` folgen ebenfalls der `extra`-Konfiguration des Modells. Mit `extra="allow"` führen sie dazu, dass das Modell vorhanden ist, selbst wenn keines der beiden deklarierten Felder übermittelt wird.

## Zusammenfassung { #summary }

Sie können **Pydantic-Modelle** verwenden, um **Header** in **FastAPI** zu deklarieren. 😎
