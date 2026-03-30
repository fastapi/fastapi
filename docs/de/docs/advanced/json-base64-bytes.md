# JSON mit Bytes als base64 { #json-with-bytes-as-base64 }

Wenn Ihre App JSON-Daten empfangen und senden muss, Sie darin aber Binärdaten einschließen müssen, können Sie diese als base64 kodieren.

## Base64 vs Dateien { #base64-vs-files }

Prüfen Sie zunächst, ob Sie [Request Files](../tutorial/request-files.md) zum Hochladen von Binärdaten und [Benutzerdefinierte Response – FileResponse](./custom-response.md#fileresponse--fileresponse-) zum Senden von Binärdaten verwenden können, anstatt sie in JSON zu kodieren.

JSON kann nur UTF-8-kodierte Strings enthalten, es kann daher keine rohen Bytes enthalten.

Base64 kann Binärdaten in Strings kodieren, dafür werden jedoch mehr Zeichen benötigt als in den ursprünglichen Binärdaten; es ist daher in der Regel weniger effizient als der Umgang mit normalen Dateien.

Verwenden Sie base64 nur, wenn Sie Binärdaten unbedingt in JSON einbetten müssen und dafür keine Dateien verwenden können.

## Pydantic `bytes` { #pydantic-bytes }

Sie können ein Pydantic-Modell mit `bytes`-Feldern deklarieren und dann in der Modellkonfiguration `val_json_bytes` verwenden, um anzugeben, dass zur *Validierung* von eingehenden JSON-Daten base64 genutzt werden soll; im Rahmen dieser Validierung wird der base64-String in Bytes dekodiert.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:9,29:35] hl[9] *}

Wenn Sie die `/docs` aufrufen, zeigt die Dokumentation, dass das Feld `data` base64-kodierte Bytes erwartet:

<div class="screenshot">
<img src="/img/tutorial/json-base64-bytes/image01.png">
</div>

Sie könnten einen Request wie folgt senden:

```json
{
    "description": "Some data",
    "data": "aGVsbG8="
}
```

/// tip | Tipp

`aGVsbG8=` ist die base64-Kodierung von `hello`.

///

Anschließend dekodiert Pydantic den base64-String und stellt Ihnen die ursprünglichen Bytes im Feld `data` des Modells bereit.

Sie erhalten eine Response wie:

```json
{
  "description": "Some data",
  "content": "hello"
}
```

## Pydantic `bytes` für Ausgabedaten { #pydantic-bytes-for-output-data }

Sie können in der Modellkonfiguration für Ausgabedaten auch `bytes`-Felder mit `ser_json_bytes` verwenden; Pydantic wird die Bytes bei der Erzeugung der JSON-Response als base64 *serialisieren*.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,12:16,29,38:41] hl[16] *}

## Pydantic `bytes` für Eingabe- und Ausgabedaten { #pydantic-bytes-for-input-and-output-data }

Und selbstverständlich können Sie dasselbe Modell so konfigurieren, dass base64 sowohl für Eingaben (*validieren*) mit `val_json_bytes` als auch für Ausgaben (*serialisieren*) mit `ser_json_bytes` verwendet wird, wenn JSON-Daten empfangen und gesendet werden.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,19:26,29,44:46] hl[23:26] *}
