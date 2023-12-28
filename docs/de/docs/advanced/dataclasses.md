# Verwendung von Datenklassen

FastAPI basiert auf **Pydantic** und ich habe Ihnen gezeigt, wie Sie Pydantic-Modelle verwenden können, um Requests und Responses zu deklarieren.

Aber FastAPI unterstützt auf die gleiche Weise auch die Verwendung von <a href="https://docs.python.org/3/library/dataclasses.html" class="external-link" target="_blank">`dataclasses`</a>:

```Python hl_lines="1  7-12  19-20"
{!../../../docs_src/dataclasses/tutorial001.py!}
```

Das ist dank **Pydantic** ebenfalls möglich, da es <a href="https://pydantic-docs.helpmanual.io/usage/dataclasses/#use-of-stdlib-dataclasses-with-basemodel" class="external-link" target="_blank">`dataclasses` intern unterstützt</a>.

Auch wenn im obige Code Pydantic nicht explizit vorkommt, verwendet FastAPI Pydantic, um diese Standard-Datenklassen in Pydantics eigene Variante von Datenklassen zu konvertieren.

Und natürlich wird das gleiche unterstützt:

* Validierung der Daten
* Serialisierung der Daten
* Dokumentation der Daten, usw.

Das funktioniert genauso wie mit Pydantic-Modellen. Und tatsächlich wird es unter der Haube mittels Pydantic auf die gleiche Weise bewerkstelligt.

!!! info
    Bedenken Sie, dass Datenklassen nicht alles können, was Pydantic-Modelle können.

    Daher müssen Sie möglicherweise weiterhin Pydantic-Modelle verwenden.

    Wenn Sie jedoch eine Menge Datenklassen herumliegen haben, ist dies ein guter Trick, um sie für eine Web-API mithilfe von FastAPI zu verwenden. 🤓

## Datenklassen als `response_model`

Sie können `dataclasses` auch im Parameter `response_model` verwenden:

```Python hl_lines="1  7-13  19"
{!../../../docs_src/dataclasses/tutorial002.py!}
```

Die Datenklasse wird automatisch in eine Pydantic-Datenklasse konvertiert.

Auf diese Weise wird deren Schema in der Benutzeroberfläche der API-Dokumentation angezeigt:

<img src="/img/tutorial/dataclasses/image01.png">

## Datenklassen in verschachtelten Datenstrukturen

Sie können `dataclasses` auch mit anderen Typannotationen kombinieren, um verschachtelte Datenstrukturen zu erstellen.

In einigen Fällen müssen Sie möglicherweise immer noch Pydantics Version von `dataclasses` verwenden. Zum Beispiel, wenn Sie Fehler in der automatisch generierten API-Dokumentation haben.

In diesem Fall können Sie einfach die Standard-`dataclasses` durch `pydantic.dataclasses` ersetzen, was einen direkten Ersatz darstellt:

```{ .python .annotate hl_lines="1  5  8-11  14-17  23-25  28" }
{!../../../docs_src/dataclasses/tutorial003.py!}
```

1. Wir importieren `field` weiterhin von Standard-`dataclasses`.

2. `pydantic.dataclasses` ist ein direkter Ersatz für `dataclasses`.

3. Die Datenklasse `Author` enthält eine Liste von `Item`-Datenklassen.

4. Die Datenklasse `Author` wird im `response_model`-Parameter verwendet.

5. Sie können andere Standard-Typannotationen mit Datenklassen als Requestbody verwenden.

    In diesem Fall handelt es sich um eine Liste von `Item`-Datenklassen.

6. Hier geben wir ein Dictionary zurück, das `items` enthält, welches eine Liste von Datenklassen ist.

    FastAPI ist weiterhin in der Lage, die Daten nach JSON zu <abbr title="Konvertieren der Daten in ein übertragbares Format">serialisieren</abbr>.

7. Hier verwendet das `response_model` als Typannotation eine Liste von `Author`-Datenklassen.

    Auch hier können Sie `dataclasses` mit Standard-Typannotationen kombinieren.

8. Beachten Sie, dass diese *Pfadoperation-Funktion* reguläres `def` anstelle von `async def` verwendet.

    Wie immer können Sie in FastAPI `def` und `async def` beliebig kombinieren.

    Wenn Sie eine Auffrischung darüber benötigen, wann welche Anwendung sinnvoll ist, lesen Sie den Abschnitt „In Eile?“ in der Dokumentation zu [`async` und `await`](../async.md#in-eile){.internal-link target=_blank}.

9. Diese *Pfadoperation-Funktion* gibt keine Datenklassen zurück (obwohl dies möglich wäre), sondern eine Liste von Dictionarys mit internen Daten.

    FastAPI verwendet den Parameter `response_model` (der Datenklassen enthält), um die Response zu konvertieren.

Sie können `dataclasses` mit anderen Typannotationen auf vielfältige Weise kombinieren, um komplexe Datenstrukturen zu bilden.

Weitere Einzelheiten finden Sie in den Bemerkungen im Quellcode oben.

## Mehr erfahren

Sie können `dataclasses` auch mit anderen Pydantic-Modellen kombinieren, von ihnen erben, sie in Ihre eigenen Modelle einbinden, usw.

Weitere Informationen finden Sie in der <a href="https://pydantic-docs.helpmanual.io/usage/dataclasses/" class="external-link" target="_blank">Pydantic-Dokumentation zu Datenklassen</a>.

## Version

Dies ist verfügbar seit FastAPI-Version `0.67.0`. 🔖
