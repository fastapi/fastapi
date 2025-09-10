# Asynchrone Tests { #async-tests }

Sie haben bereits gesehen, wie Sie Ihre **FastAPI**-Anwendungen mit dem bereitgestellten `TestClient` testen. Bisher haben Sie nur gesehen, wie man synchrone Tests schreibt, ohne `async`-Funktionen zu verwenden.

Die Möglichkeit, in Ihren Tests asynchrone Funktionen zu verwenden, könnte beispielsweise nützlich sein, wenn Sie Ihre Datenbank asynchron abfragen. Stellen Sie sich vor, Sie möchten das Senden von <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Requests</abbr> an Ihre FastAPI-Anwendung testen und dann überprüfen, ob Ihr Backend die richtigen Daten erfolgreich in die Datenbank geschrieben hat, während Sie eine asynchrone Datenbankbibliothek verwenden.

Schauen wir uns an, wie wir das machen können.

## pytest.mark.anyio { #pytest-mark-anyio }

Wenn wir in unseren Tests asynchrone Funktionen aufrufen möchten, müssen unsere Testfunktionen asynchron sein. AnyIO stellt hierfür ein nettes Plugin zur Verfügung, mit dem wir festlegen können, dass einige Testfunktionen asynchron aufgerufen werden sollen.

## HTTPX { #httpx }

Auch wenn Ihre **FastAPI**-Anwendung normale `def`-Funktionen anstelle von `async def` verwendet, handelt es sich darunter immer noch um eine `async`-Anwendung.

Der `TestClient` betreibt unter der Haube etwas Magie, um die asynchrone FastAPI-Anwendung in Ihren normalen `def`-Testfunktionen, mithilfe von Standard-Pytest aufzurufen. Aber diese Magie funktioniert nicht mehr, wenn wir sie in asynchronen Funktionen verwenden. Durch die asynchrone Ausführung unserer Tests können wir den `TestClient` nicht mehr in unseren Testfunktionen verwenden.

Der `TestClient` basiert auf <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> und glücklicherweise können wir es direkt verwenden, um die API zu testen.

## Beispiel { #example }

Betrachten wir als einfaches Beispiel eine Dateistruktur ähnlich der in [Größere Anwendungen](../tutorial/bigger-applications.md){.internal-link target=_blank} und [Testen](../tutorial/testing.md){.internal-link target=_blank}:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Die Datei `main.py` hätte als Inhalt:

{* ../../docs_src/async_tests/main.py *}

Die Datei `test_main.py` hätte die Tests für `main.py`, das könnte jetzt so aussehen:

{* ../../docs_src/async_tests/test_main.py *}

## Es ausführen { #run-it }

Sie können Ihre Tests wie gewohnt ausführen mit:

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## Im Detail { #in-detail }

Der Marker `@pytest.mark.anyio` teilt pytest mit, dass diese Testfunktion asynchron aufgerufen werden soll:

{* ../../docs_src/async_tests/test_main.py hl[7] *}

/// tip | Tipp

Beachten Sie, dass die Testfunktion jetzt `async def` ist und nicht nur `def` wie zuvor, wenn Sie den `TestClient` verwenden.

///

Dann können wir einen `AsyncClient` mit der App erstellen und mit `await` asynchrone Requests an ihn senden.

{* ../../docs_src/async_tests/test_main.py hl[9:12] *}

Das ist das Äquivalent zu:

```Python
response = client.get('/')
```

... welches wir verwendet haben, um unsere Requests mit dem `TestClient` zu machen.

/// tip | Tipp

Beachten Sie, dass wir async/await mit dem neuen `AsyncClient` verwenden – der Request ist asynchron.

///

/// warning | Achtung

Falls Ihre Anwendung auf Lifespan-Events angewiesen ist, der `AsyncClient` löst diese Events nicht aus. Um sicherzustellen, dass sie ausgelöst werden, verwenden Sie `LifespanManager` von <a href="https://github.com/florimondmanca/asgi-lifespan#usage" class="external-link" target="_blank">florimondmanca/asgi-lifespan</a>.

///

## Andere asynchrone Funktionsaufrufe { #other-asynchronous-function-calls }

Da die Testfunktion jetzt asynchron ist, können Sie in Ihren Tests neben dem Senden von Requests an Ihre FastAPI-Anwendung jetzt auch andere `async`-Funktionen aufrufen (und `await`en), genau so, wie Sie diese an anderer Stelle in Ihrem Code aufrufen würden.

/// tip | Tipp

Wenn Sie einen `RuntimeError: Task attached to a different loop` erhalten, wenn Sie asynchrone Funktionsaufrufe in Ihre Tests integrieren (z. B. bei Verwendung von <a href="https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop" class="external-link" target="_blank">MongoDBs MotorClient</a>), dann denken Sie daran, Objekte zu instanziieren, die einen Event Loop nur innerhalb asynchroner Funktionen benötigen, z. B. einen `@app.on_event("startup")`-Callback.

///
