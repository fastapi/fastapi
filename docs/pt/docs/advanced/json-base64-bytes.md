# JSON com bytes em Base64 { #json-with-bytes-as-base64 }

Se sua aplicação precisa receber e enviar dados JSON, mas você precisa incluir dados binários nele, você pode codificá-los em base64.

## Base64 vs Arquivos { #base64-vs-files }

Primeiro, considere se você pode usar [Arquivos na request](../tutorial/request-files.md) para fazer upload de dados binários e [Response personalizada - FileResponse](./custom-response.md#fileresponse--fileresponse-) para enviar dados binários, em vez de codificá-los em JSON.

JSON só pode conter strings codificadas em UTF-8, portanto não pode conter bytes puros.

Base64 pode codificar dados binários em strings, mas, para isso, precisa usar mais caracteres do que os dados binários originais; assim, normalmente é menos eficiente do que arquivos comuns.

Use base64 apenas se realmente precisar incluir dados binários em JSON e não puder usar arquivos para isso.

## Pydantic `bytes` { #pydantic-bytes }

Você pode declarar um modelo Pydantic com campos `bytes` e então usar `val_json_bytes` na configuração do modelo para indicar que deve usar base64 para *validar* os dados JSON de entrada; como parte dessa validação, ele decodificará a string base64 em bytes.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:9,29:35] hl[9] *}

Se você verificar a `/docs`, verá que o campo `data` espera bytes codificados em base64:

<div class="screenshot">
<img src="/img/tutorial/json-base64-bytes/image01.png">
</div>

Você poderia enviar uma request assim:

```json
{
    "description": "Some data",
    "data": "aGVsbG8="
}
```

/// tip | Dica

`aGVsbG8=` é a codificação base64 de `hello`.

///

Em seguida, o Pydantic decodificará a string base64 e fornecerá os bytes originais no campo `data` do modelo.

Você receberá uma response assim:

```json
{
  "description": "Some data",
  "content": "hello"
}
```

## Pydantic `bytes` para dados de saída { #pydantic-bytes-for-output-data }

Você também pode usar campos `bytes` com `ser_json_bytes` na configuração do modelo para dados de saída, e o Pydantic irá *serializar* os bytes como base64 ao gerar a response JSON.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,12:16,29,38:41] hl[16] *}

## Pydantic `bytes` para dados de entrada e saída { #pydantic-bytes-for-input-and-output-data }

E, claro, você pode usar o mesmo modelo configurado para usar base64 para lidar tanto com a entrada (*validar*) com `val_json_bytes` quanto com a saída (*serializar*) com `ser_json_bytes` ao receber e enviar dados JSON.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,19:26,29,44:46] hl[23:26] *}
