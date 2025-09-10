# Header-Parameter { #header-parameters }

Sie können Header-Parameter genauso definieren, wie Sie `Query`-, `Path`- und `Cookie`-Parameter definieren.

## `Header` importieren { #import-header }

Importieren Sie zuerst `Header`:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[3] *}

## `Header`-Parameter deklarieren { #declare-header-parameters }

Deklarieren Sie dann die Header-Parameter mit derselben Struktur wie bei `Path`, `Query` und `Cookie`.

Sie können den Defaultwert sowie alle zusätzlichen Validierungs- oder Annotationsparameter definieren:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[9] *}

/// note | Technische Details

`Header` ist eine „Schwester“-Klasse von `Path`, `Query` und `Cookie`. Sie erbt ebenfalls von der gemeinsamen `Param`-Klasse.

Aber denken Sie daran, dass bei der Nutzung von `Query`, `Path`, `Header` und anderen Importen aus `fastapi`, diese tatsächlich Funktionen sind, die spezielle Klassen zurückgeben.

///

/// info | Info

Um Header zu deklarieren, müssen Sie `Header` verwenden, da die Parameter sonst als Query-Parameter interpretiert werden würden.

///

## Automatische Konvertierung { #automatic-conversion }

`Header` bietet etwas zusätzliche Funktionalität im Vergleich zu `Path`, `Query` und `Cookie`.

Die meisten Standard-Header sind durch ein „Bindestrich“-Zeichen getrennt, auch bekannt als „Minus-Symbol“ (`-`).

Aber eine Variable wie `user-agent` ist in Python ungültig.

Daher wird `Header` standardmäßig die Zeichen des Parameter-Namens von Unterstrich (`_`) zu Bindestrich (`-`) konvertieren, um die Header zu extrahieren und zu dokumentieren.

Außerdem ist Groß-/Klein­schrei­bung in HTTP-Headern nicht relevant, daher können Sie sie im Standard-Python-Stil (auch bekannt als „snake_case“) deklarieren.

Sie können also `user_agent` verwenden, wie Sie es normalerweise im Python-Code tun würden, anstatt die Anfangsbuchstaben wie bei `User_Agent` großzuschreiben oder Ähnliches.

Wenn Sie aus irgendeinem Grund die automatische Konvertierung von Unterstrichen zu Bindestrichen deaktivieren müssen, setzen Sie den Parameter `convert_underscores` von `Header` auf `False`:

{* ../../docs_src/header_params/tutorial002_an_py310.py hl[10] *}

/// warning | Achtung

Bevor Sie `convert_underscores` auf `False` setzen, bedenken Sie, dass manche HTTP-Proxys und Server die Verwendung von Headern mit Unterstrichen nicht erlauben.

///

## Doppelte Header { #duplicate-headers }

Es ist möglich, doppelte Header zu empfangen. Damit ist gemeint, denselben Header mit mehreren Werten.

Sie können solche Fälle definieren, indem Sie in der Typdeklaration eine Liste verwenden.

Sie erhalten dann alle Werte von diesem doppelten Header als Python-`list`.

Um beispielsweise einen `X-Token`-Header zu deklarieren, der mehrmals vorkommen kann, können Sie schreiben:

{* ../../docs_src/header_params/tutorial003_an_py310.py hl[9] *}

Wenn Sie mit dieser *Pfadoperation* kommunizieren und zwei HTTP-Header senden, wie:

```
X-Token: foo
X-Token: bar
```

Dann wäre die <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr>:

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## Zusammenfassung { #recap }

Deklarieren Sie Header mit `Header`, wobei Sie dasselbe gängige Muster wie bei `Query`, `Path` und `Cookie` verwenden.

Und machen Sie sich keine Sorgen um Unterstriche in Ihren Variablen, **FastAPI** wird sich darum kümmern, sie zu konvertieren.
