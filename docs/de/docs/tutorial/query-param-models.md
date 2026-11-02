# Query-Parameter-Modelle { #query-parameter-models }

Wenn Sie eine Gruppe von **Query-Parametern** haben, die miteinander in Beziehung stehen, können Sie ein **Pydantic-Modell** erstellen, um diese zu deklarieren.

Dadurch können Sie das **Modell an mehreren Stellen wiederverwenden** und gleichzeitig Validierungen und Metadaten für alle Parameter auf einmal deklarieren. 😎

/// note | Hinweis

Dies wird seit FastAPI Version `0.115.0` unterstützt. 🤓

///

## Query-Parameter mit einem Pydantic-Modell { #query-parameters-with-a-pydantic-model }

Deklarieren Sie die benötigten **Query-Parameter** in einem **Pydantic-Modell** und dann den Parameter als `Query`:

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI** wird die Daten für **jedes Feld** aus den **Query-Parametern** des <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> extrahieren und Ihnen das definierte Pydantic-Modell bereitstellen.

## Die Dokumentation testen { #check-the-docs }

Sie können die Query-Parameter in der Dokumentations-Oberfläche unter `/docs` einsehen:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## Zusätzliche Query-Parameter verbieten { #forbid-extra-query-parameters }

In einigen speziellen Anwendungsfällen (wahrscheinlich nicht sehr häufig) möchten Sie möglicherweise die Query-Parameter, die Sie empfangen möchten, **beschränken**.

Sie können die Modellkonfiguration von Pydantic verwenden, um jegliche `extra` Felder mit `forbid` zu verbieten:

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

Wenn ein Client versucht, einige **zusätzliche** Daten in den **Query-Parametern** zu senden, erhält er eine **Error-<abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr>**.

Wenn der Client beispielsweise versucht, einen `tool` Query-Parameter mit dem Wert `plumbus` zu senden, wie:

```http
https://example.com/items/?limit=10&tool=plumbus
```

erhält er eine **Error-Response**, die ihm mitteilt, dass der Query-Parameter `tool` nicht erlaubt ist:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## Parametermodelle kombinieren { #combine-parameter-models }

Sie können mehrere Query-Parameter-Modelle deklarieren und sie mit einzelnen Query-Parametern oder Abhängigkeiten kombinieren.

{* ../../docs_src/query_param_models/tutorial003_an_py310.py hl[9:15,20:22] *}

Die Requestparameter bleiben auf derselben Ebene.

```http
https://example.com/items/?limit=5&offset=10&tags=red&tags=blue&search=shirt
```

Es gibt keine Schlüssel `pagination` oder `filters` im Query-String. Jedes Modell validiert die Query-Parameter unabhängig, mit seinen eigenen Defaultwerten, Feldvalidatoren und Modellvalidatoren. Dasselbe gilt, wenn die Modelle oder einzelnen Parameter in Abhängigkeiten deklariert werden.

Wenn Modelle einen Parameternamen oder Alias gemeinsam nutzen, validiert jedes Modell diesen Requestparameter unabhängig. Verwenden Sie unterschiedliche Namen oder Aliase für unabhängige Werte. OpenAPI listet einen gemeinsam genutzten Parameter nur einmal auf, wie auch bei Parametern, die mit Abhängigkeiten gemeinsam genutzt werden. Daher sollten gemeinsame Deklarationen denselben Typ und dieselben Einschränkungen beschreiben.

Die `extra`-Konfiguration jedes Modells gilt für alle Query-Parameter, einschließlich derjenigen, die in anderen Modellen oder Abhängigkeiten deklariert sind. Mit `extra="forbid"` wird jeder Parameter außerhalb dieses Modells abgelehnt. Mit `extra="allow"` werden diese Parameter als zusätzliche Felder in das Modell aufgenommen.

Dies funktioniert auch für `Header`- und `Cookie`-Modelle.

## Optionale Query-Parameter-Modelle { #optional-query-parameter-models }

Deklarieren Sie ein Query-Parameter-Modell mit `| None` und einem Defaultwert von `None`, um die Gruppe optional zu machen.

{* ../../docs_src/query_param_models/tutorial004_an_py310.py hl[18] *}

Wenn weder `start` noch `end` gesendet wird, ist `date_range` gleich `None`. Wenn eines davon gesendet wird, validiert FastAPI das Modell und erfordert beide Felder.

Bei Verwendung von `| None` ohne Defaultwert bleibt der Parameter erforderlich.

Zusätzliche Parameter folgen der `extra`-Konfiguration des Modells. Ignorierte zusätzliche Parameter bewirken nicht, dass das Modell als vorhanden gilt.

OpenAPI listet die Felder der Gruppe einzeln auf und markiert sie als optional.

Sie können auch optionale [Header-Parameter-Modelle](header-param-models.md#optional-header-parameter-models) und [Cookie-Parameter-Modelle](cookie-param-models.md#optional-cookie-parameter-models) deklarieren.

## Zusammenfassung { #summary }

Sie können **Pydantic-Modelle** verwenden, um **Query-Parameter** in **FastAPI** zu deklarieren. 😎

/// tip | Tipp

Spoiler-Alarm: Sie können auch Pydantic-Modelle verwenden, um Cookies und Header zu deklarieren, aber darüber werden Sie später im Tutorial lesen. 🤫

///
