# Response – Statuscode ändern

Sie haben wahrscheinlich schon vorher gelesen, dass Sie einen Standard-[Response-Statuscode](../tutorial/response-status-code.md){.internal-link target=_blank} festlegen können.

In manchen Fällen müssen Sie jedoch einen anderen als den Standard-Statuscode zurückgeben.

## Anwendungsfall

Stellen Sie sich zum Beispiel vor, Sie möchten standardmäßig den HTTP-Statuscode „OK“ `200` zurückgeben.

Wenn die Daten jedoch nicht vorhanden waren, möchten Sie diese erstellen und den HTTP-Statuscode „CREATED“ `201` zurückgeben.

Sie möchten aber dennoch in der Lage sein, die von Ihnen zurückgegebenen Daten mit einem `response_model` zu filtern und zu konvertieren.

In diesen Fällen können Sie einen `Response`-Parameter verwenden.

## Einen `Response`-Parameter verwenden

Sie können einen Parameter vom Typ `Response` in Ihrer *Pfadoperation-Funktion* deklarieren (wie Sie es auch für Cookies und Header tun können).

Anschließend können Sie den `status_code` in diesem *vorübergehenden* Response-Objekt festlegen.

```Python hl_lines="1  9  12"
{!../../../docs_src/response_change_status_code/tutorial001.py!}
```

Und dann können Sie wie gewohnt jedes benötigte Objekt zurückgeben (ein `dict`, ein Datenbankmodell usw.).

Und wenn Sie ein `response_model` deklariert haben, wird es weiterhin zum Filtern und Konvertieren des von Ihnen zurückgegebenen Objekts verwendet.

**FastAPI** verwendet diese *vorübergehende* Response, um den Statuscode (auch Cookies und Header) zu extrahieren und fügt diese in die endgültige Response ein, die den von Ihnen zurückgegebenen Wert enthält, gefiltert nach einem beliebigen `response_model`.

Sie können den Parameter `Response` auch in Abhängigkeiten deklarieren und den Statuscode darin festlegen. Bedenken Sie jedoch, dass der gewinnt, welcher zuletzt gesetzt wird.
