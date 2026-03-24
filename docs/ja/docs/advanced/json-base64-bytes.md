# Base64 にしたバイトを含む JSON { #json-with-bytes-as-base64 }

アプリで JSON データの受信・送信が必要だが、その中にバイナリデータを含める必要がある場合は、base64 にエンコードできます。

## Base64 とファイル { #base64-vs-files }

バイナリデータのアップロードにはまず、JSON にエンコードする代わりに [Request Files](../tutorial/request-files.md) を、バイナリデータの送信には [カスタムレスポンス - FileResponse](./custom-response.md#fileresponse--fileresponse-) を使えるか検討してください。

JSON は UTF-8 でエンコードされた文字列のみを含められるため、生のバイト列は含められません。

Base64 はバイナリデータを文字列にエンコードできますが、そのために元のバイナリより多くの文字を使用する必要があり、通常は通常のファイルより非効率です。

JSON にバイナリデータをどうしても含める必要があり、ファイルを使えない場合にのみ base64 を使用してください。

## Pydantic `bytes` { #pydantic-bytes }

Pydantic モデルで `bytes` 型のフィールドを宣言し、モデル設定で `val_json_bytes` を使うと、入力 JSON データの検証時に base64 を用いるよう指示できます。この検証の一環として、base64 文字列はバイト列へデコードされます。

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:9,29:35] hl[9] *}

「/docs」を確認すると、`data` フィールドが base64 でエンコードされたバイト列を期待していることが表示されます。

<div class="screenshot">
<img src="/img/tutorial/json-base64-bytes/image01.png">
</div>

次のようなリクエストを送れます:

```json
{
    "description": "Some data",
    "data": "aGVsbG8="
}
```

/// tip | 豆知識

`aGVsbG8=` は `hello` の base64 エンコードです。

///

その後、Pydantic は base64 文字列をデコードし、モデルの `data` フィールドに元のバイト列を渡します。

次のようなレスポンスを受け取ります:

```json
{
  "description": "Some data",
  "content": "hello"
}
```

## 出力データ向けの Pydantic `bytes` { #pydantic-bytes-for-output-data }

出力データ用にモデル設定で `ser_json_bytes` とともに `bytes` フィールドを使用することもでき、Pydantic は JSON レスポンスを生成するときにバイト列を base64 でシリアライズします。

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,12:16,29,38:41] hl[16] *}

## 入力・出力データ向けの Pydantic `bytes` { #pydantic-bytes-for-input-and-output-data }

もちろん、同じモデルを base64 を使うように設定しておけば、JSON データの受信時は `val_json_bytes` で入力を「検証」し、送信時は `ser_json_bytes` で出力を「シリアライズ」する、といった具合に、入力と出力の両方を扱えます。

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,19:26,29,44:46] hl[23:26] *}
