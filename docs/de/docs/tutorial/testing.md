# Testen { #testing }

Dank <a href="https://www.starlette.dev/testclient/" class="external-link" target="_blank">Starlette</a> ist das Testen von **FastAPI**-Anwendungen einfach und macht Spaß.

Es basiert auf <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>, welches wiederum auf der Grundlage von Requests konzipiert wurde, es ist also sehr vertraut und intuitiv.

Damit können Sie <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a> direkt mit **FastAPI** verwenden.

## `TestClient` verwenden { #using-testclient }

/// info | Info

Um `TestClient` zu verwenden, installieren Sie zunächst <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a>.

Erstellen Sie eine [virtuelle Umgebung](../virtual-environments.md){.internal-link target=_blank}, aktivieren Sie sie und installieren Sie es dann, z. B.:

```console
$ pip install httpx
```

///

Importieren Sie `TestClient`.

Erstellen Sie einen `TestClient`, indem Sie ihm Ihre **FastAPI**-Anwendung übergeben.

Erstellen Sie Funktionen mit einem Namen, der mit `test_` beginnt (das sind `pytest`-Konventionen).

Verwenden Sie das `TestClient`-Objekt auf die gleiche Weise wie `httpx`.

Schreiben Sie einfache `assert`-Anweisungen mit den Standard-Python-Ausdrücken, die Sie überprüfen müssen (wiederum, Standard-`pytest`).

{* ../../docs_src/app_testing/tutorial001.py hl[2,12,15:18] *}

/// tip | Tipp

Beachten Sie, dass die Testfunktionen normal `def` und nicht `async def` sind.

Und die Anrufe an den Client sind ebenfalls normale Anrufe, die nicht `await` verwenden.

Dadurch können Sie `pytest` ohne Komplikationen direkt nutzen.

///

/// note | Technische Details

Sie könnten auch `from starlette.testclient import TestClient` verwenden.

**FastAPI** stellt denselben `starlette.testclient` auch via `fastapi.testclient` bereit, als Annehmlichkeit für Sie, den Entwickler. Es kommt aber tatsächlich direkt von Starlette.

///

/// tip | Tipp

Wenn Sie in Ihren Tests neben dem Senden von <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Requests</abbr> an Ihre FastAPI-Anwendung auch `async`-Funktionen aufrufen möchten (z. B. asynchrone Datenbankfunktionen), werfen Sie einen Blick auf die [Async-Tests](../advanced/async-tests.md){.internal-link target=_blank} im Handbuch für fortgeschrittene Benutzer.

///

## Tests separieren { #separating-tests }

In einer echten Anwendung würden Sie Ihre Tests wahrscheinlich in einer anderen Datei haben.

Und Ihre **FastAPI**-Anwendung könnte auch aus mehreren Dateien/Modulen, usw. bestehen.

### **FastAPI** Anwendungsdatei { #fastapi-app-file }

Nehmen wir an, Sie haben eine Dateistruktur wie in [Größere Anwendungen](bigger-applications.md){.internal-link target=_blank} beschrieben:

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

In der Datei `main.py` haben Sie Ihre **FastAPI**-Anwendung:


{* ../../docs_src/app_testing/main.py *}


### Testdatei { #testing-file }

Dann könnten Sie eine Datei `test_main.py` mit Ihren Tests haben. Sie könnte sich im selben Python-Package befinden (dasselbe Verzeichnis mit einer `__init__.py`-Datei):

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Da sich diese Datei im selben Package befindet, können Sie relative Importe verwenden, um das Objekt `app` aus dem `main`-Modul (`main.py`) zu importieren:

{* ../../docs_src/app_testing/test_main.py hl[3] *}


... und haben den Code für die Tests wie zuvor.

## Testen: erweitertes Beispiel { #testing-extended-example }

Nun erweitern wir dieses Beispiel und fügen weitere Details hinzu, um zu sehen, wie verschiedene Teile getestet werden.

### Erweiterte **FastAPI**-Anwendungsdatei { #extended-fastapi-app-file }

Fahren wir mit der gleichen Dateistruktur wie zuvor fort:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Nehmen wir an, dass die Datei `main.py` mit Ihrer **FastAPI**-Anwendung jetzt einige andere **Pfadoperationen** hat.

Sie verfügt über eine `GET`-Operation, die einen Fehler zurückgeben könnte.

Sie verfügt über eine `POST`-Operation, die mehrere Fehler zurückgeben könnte.

Beide *Pfadoperationen* erfordern einen `X-Token`-Header.

//// tab | Python 3.10+

```Python
{!> ../../docs_src/app_testing/app_b_an_py310/main.py!}
```

////

//// tab | Python 3.9+

```Python
{!> ../../docs_src/app_testing/app_b_an_py39/main.py!}
```

////

//// tab | Python 3.8+

```Python
{!> ../../docs_src/app_testing/app_b_an/main.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | Tipp

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python
{!> ../../docs_src/app_testing/app_b_py310/main.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | Tipp

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python
{!> ../../docs_src/app_testing/app_b/main.py!}
```

////

### Erweiterte Testdatei { #extended-testing-file }

Anschließend könnten Sie `test_main.py` mit den erweiterten Tests aktualisieren:

{* ../../docs_src/app_testing/app_b/test_main.py *}


Wenn Sie möchten, dass der Client Informationen im Request übergibt und Sie nicht wissen, wie das geht, können Sie suchen (googeln), wie es mit `httpx` gemacht wird, oder sogar, wie es mit `requests` gemacht wird, da das Design von HTTPX auf dem Design von Requests basiert.

Dann machen Sie in Ihren Tests einfach das gleiche.

Z. B.:

* Um einen *Pfad*- oder *Query*-Parameter zu übergeben, fügen Sie ihn der URL selbst hinzu.
* Um einen JSON-Body zu übergeben, übergeben Sie ein Python-Objekt (z. B. ein <abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">`dict`</abbr>) an den Parameter `json`.
* Wenn Sie *Formulardaten* anstelle von JSON senden müssen, verwenden Sie stattdessen den `data`-Parameter.
* Um *Header* zu übergeben, verwenden Sie ein `dict` im `headers`-Parameter.
* Für *Cookies* ein `dict` im `cookies`-Parameter.

Weitere Informationen zum Übergeben von Daten an das Backend (mithilfe von `httpx` oder dem `TestClient`) finden Sie in der <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX-Dokumentation</a>.

/// info | Info

Beachten Sie, dass der `TestClient` Daten empfängt, die nach JSON konvertiert werden können, keine Pydantic-Modelle.

Wenn Sie ein Pydantic-Modell in Ihrem Test haben und dessen Daten während des Testens an die Anwendung senden möchten, können Sie den `jsonable_encoder` verwenden, der in [JSON-kompatibler Encoder](encoder.md){.internal-link target=_blank} beschrieben wird.

///

## Tests ausführen { #run-it }

Danach müssen Sie nur noch `pytest` installieren.

Erstellen Sie eine [virtuelle Umgebung](../virtual-environments.md){.internal-link target=_blank}, aktivieren Sie sie und installieren Sie es dann, z. B.:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

Es erkennt die Dateien und Tests automatisch, führt sie aus und berichtet Ihnen die Ergebnisse.

Führen Sie die Tests aus, mit:

<div class="termy">

```console
$ pytest

================ test session starts ================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/user/code/superawesome-cli/app
plugins: forked-1.1.3, xdist-1.31.0, cov-2.8.1
collected 6 items

---> 100%

test_main.py <span style="color: green; white-space: pre;">......                            [100%]</span>

<span style="color: green;">================= 1 passed in 0.03s =================</span>
```

</div>
