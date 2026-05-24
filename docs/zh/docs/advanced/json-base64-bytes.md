# 在 JSON 中使用 Base64 表示字节 { #json-with-bytes-as-base64 }

如果你的应用需要接收和发送 JSON 数据，但其中需要包含二进制数据，可以将其编码为 base64。

## Base64 与文件 { #base64-vs-files }

请先考虑是否可以使用 [请求文件](../tutorial/request-files.md) 来上传二进制数据，并使用 [自定义响应 - FileResponse](./custom-response.md#fileresponse--fileresponse-) 来发送二进制数据，而不是把它编码进 JSON。

JSON 只能包含 UTF-8 编码的字符串，因此无法直接包含原始字节。

Base64 可以把二进制数据编码为字符串，但为此会使用比原始二进制更多的字符，因此通常比直接使用文件的效率更低。

仅当你确实需要在 JSON 中包含二进制数据且无法使用文件时，才使用 base64。

## Pydantic `bytes` { #pydantic-bytes }

你可以声明带有 `bytes` 字段的 Pydantic 模型，然后在模型配置中使用 `val_json_bytes` 指定用 base64 来验证输入的 JSON 数据；作为验证的一部分，它会将该 base64 字符串解码为字节。

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:9,29:35] hl[9] *}

查看 `/docs` 时，你会看到字段 `data` 期望接收 base64 编码的字节：

<div class="screenshot">
<img src="/img/tutorial/json-base64-bytes/image01.png">
</div>

你可以发送如下请求：

```json
{
    "description": "Some data",
    "data": "aGVsbG8="
}
```

/// tip | 提示

`aGVsbG8=` 是 `hello` 的 base64 编码。

///

随后 Pydantic 会解码该 base64 字符串，并在模型的 `data` 字段中提供原始字节。

你将会收到类似的响应：

```json
{
  "description": "Some data",
  "content": "hello"
}
```

## 用于输出数据的 Pydantic `bytes` { #pydantic-bytes-for-output-data }

对于输出数据，你也可以在模型配置中为 `bytes` 字段使用 `ser_json_bytes`，Pydantic 会在生成 JSON 响应时将字节以 base64 进行序列化。

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,12:16,29,38:41] hl[16] *}

## 用于输入和输出数据的 Pydantic `bytes` { #pydantic-bytes-for-input-and-output-data }

当然，你也可以使用同一个配置了 base64 的模型，在接收和发送 JSON 数据时，同时处理输入（使用 `val_json_bytes` 进行验证）和输出（使用 `ser_json_bytes` 进行序列化）。

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,19:26,29,44:46] hl[23:26] *}
