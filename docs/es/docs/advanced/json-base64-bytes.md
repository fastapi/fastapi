# JSON con Bytes como Base64 { #json-with-bytes-as-base64 }

Si tu app necesita recibir y enviar datos JSON, pero necesitas incluir datos binarios en él, puedes codificarlos como base64.

## Base64 vs Archivos { #base64-vs-files }

Considera primero si puedes usar [Archivos en request](../tutorial/request-files.md) para subir datos binarios y [Response personalizada - FileResponse](./custom-response.md#fileresponse--fileresponse-) para enviar datos binarios, en lugar de codificarlos en JSON.

JSON solo puede contener strings codificados en UTF-8, así que no puede contener bytes crudos.

Base64 puede codificar datos binarios en strings, pero para hacerlo necesita usar más caracteres que los datos binarios originales, así que normalmente sería menos eficiente que los archivos normales.

Usa base64 solo si definitivamente necesitas incluir datos binarios en JSON y no puedes usar archivos para eso.

## Pydantic `bytes` { #pydantic-bytes }

Puedes declarar un modelo de Pydantic con campos `bytes`, y luego usar `val_json_bytes` en la configuración del modelo para indicarle que use base64 para validar datos JSON de entrada; como parte de esa validación decodificará el string base64 en bytes.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:9,29:35] hl[9] *}

Si revisas `/docs`, verás que el campo `data` espera bytes codificados en base64:

<div class="screenshot">
<img src="/img/tutorial/json-base64-bytes/image01.png">
</div>

Podrías enviar un request como:

```json
{
    "description": "Some data",
    "data": "aGVsbG8="
}
```

/// tip | Consejo

`aGVsbG8=` es la codificación base64 de `hello`.

///

Y luego Pydantic decodificará el string base64 y te dará los bytes originales en el campo `data` del modelo.

Recibirás una response como:

```json
{
  "description": "Some data",
  "content": "hello"
}
```

## Pydantic `bytes` para datos de salida { #pydantic-bytes-for-output-data }

También puedes usar campos `bytes` con `ser_json_bytes` en la configuración del modelo para datos de salida, y Pydantic serializará los bytes como base64 al generar la response JSON.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,12:16,29,38:41] hl[16] *}

## Pydantic `bytes` para datos de entrada y salida { #pydantic-bytes-for-input-and-output-data }

Y por supuesto, puedes usar el mismo modelo configurado para usar base64 para manejar tanto la entrada (*validate*) con `val_json_bytes` como la salida (*serialize*) con `ser_json_bytes` al recibir y enviar datos JSON.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,19:26,29,44:46] hl[23:26] *}
