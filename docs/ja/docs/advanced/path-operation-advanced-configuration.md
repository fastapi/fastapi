# Path Operationの高度な設定 { #path-operation-advanced-configuration }

## OpenAPI operationId { #openapi-operationid }

/// warning | 注意

OpenAPIの「エキスパート」でなければ、これはおそらく必要ありません。

///

*path operation* で `operation_id` パラメータを利用することで、OpenAPIの `operationId` を設定できます。

各オペレーションで一意になるようにする必要があります。

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py310.py hl[6] *}

### *path operation関数* の名前をoperationIdとして使用する { #using-the-path-operation-function-name-as-the-operationid }

APIの関数名を `operationId` として利用したい場合、すべてのAPI関数をイテレーションし、各 *path operation* の `operation_id` を `APIRoute.name` で上書きすれば可能です。

すべての *path operation* を追加した後に行うべきです。

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py310.py hl[2, 12:21, 24] *}

/// tip | 豆知識

`app.openapi()` を手動で呼び出す場合、その前に `operationId` を更新するべきです。

///

/// warning | 注意

この方法をとる場合、各 *path operation関数* が一意な名前である必要があります。

異なるモジュール（Pythonファイル）にある場合でも同様です。

///

## OpenAPIから除外する { #exclude-from-openapi }

生成されるOpenAPIスキーマ（つまり、自動ドキュメント生成の仕組み）から *path operation* を除外するには、`include_in_schema` パラメータを使用して `False` に設定します。

{* ../../docs_src/path_operation_advanced_configuration/tutorial003_py310.py hl[6] *}

## docstringによる説明の高度な設定 { #advanced-description-from-docstring }

*path operation関数* のdocstringからOpenAPIに使用する行を制限できます。

`\f`（エスケープされた「書式送り（form feed）」文字）を追加すると、**FastAPI** はその地点でOpenAPIに使用される出力を切り詰めます。

ドキュメントには表示されませんが、他のツール（Sphinxなど）は残りの部分を利用できます。

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## 追加レスポンス { #additional-responses }

*path operation* に対して `response_model` と `status_code` を宣言する方法はすでに見たことがあるでしょう。

それにより、*path operation* のメインのレスポンスに関するメタデータが定義されます。

追加のレスポンスについても、モデルやステータスコードなどとともに宣言できます。

これについてはドキュメントに章全体があります。 [OpenAPIの追加レスポンス](additional-responses.md){.internal-link target=_blank} で読めます。

## OpenAPI Extra { #openapi-extra }

アプリケーションで *path operation* を宣言すると、**FastAPI** はOpenAPIスキーマに含めるために、その *path operation* に関連するメタデータを自動的に生成します。

/// note | 技術詳細

OpenAPI仕様では <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Operation Object</a> と呼ばれています。

///

これには *path operation* に関するすべての情報が含まれ、自動ドキュメントを生成するために使われます。

`tags`、`parameters`、`requestBody`、`responses` などが含まれます。

この *path operation* 固有のOpenAPIスキーマは通常 **FastAPI** により自動生成されますが、拡張することもできます。

/// tip | 豆知識

これは低レベルな拡張ポイントです。

追加レスポンスを宣言するだけなら、より便利な方法として [OpenAPIの追加レスポンス](additional-responses.md){.internal-link target=_blank} を使うことができます。

///

`openapi_extra` パラメータを使って、*path operation* のOpenAPIスキーマを拡張できます。

### OpenAPI Extensions { #openapi-extensions }

この `openapi_extra` は、例えば [OpenAPI Extensions](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions) を宣言するのに役立ちます。

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py310.py hl[6] *}

自動APIドキュメントを開くと、その拡張は特定の *path operation* の下部に表示されます。

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

そして（APIの `/openapi.json` にある）生成されたOpenAPIを見ると、その拡張も特定の *path operation* の一部として確認できます。

```JSON hl_lines="22"
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "x-aperture-labs-portal": "blue"
            }
        }
    }
}
```

### カスタムOpenAPI *path operation* スキーマ { #custom-openapi-path-operation-schema }

`openapi_extra` 内の辞書は、*path operation* 用に自動生成されたOpenAPIスキーマと深くマージされます。

そのため、自動生成されたスキーマに追加データを加えることができます。

例えば、Pydanticを使ったFastAPIの自動機能を使わずに独自のコードでリクエストを読み取り・検証することを選べますが、それでもOpenAPIスキーマでリクエストを定義したい場合があります。

それは `openapi_extra` で行えます。

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py310.py hl[19:36, 39:40] *}

この例では、Pydanticモデルを一切宣言していません。実際、リクエストボディはJSONとして <dfn title="bytes などのプレーンな形式から Python オブジェクトに変換される">パース</dfn> されず、直接 `bytes` として読み取られます。そして `magic_data_reader()` 関数が、何らかの方法でそれをパースする責務を担います。

それでも、リクエストボディに期待されるスキーマを宣言できます。

### カスタムOpenAPI content type { #custom-openapi-content-type }

同じトリックを使って、PydanticモデルでJSON Schemaを定義し、それを *path operation* 用のカスタムOpenAPIスキーマセクションに含めることができます。

また、リクエスト内のデータ型がJSONでない場合でもこれを行えます。

例えばこのアプリケーションでは、PydanticモデルからJSON Schemaを抽出するFastAPIの統合機能や、JSONの自動バリデーションを使っていません。実際、リクエストのcontent typeをJSONではなくYAMLとして宣言しています。

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[15:20, 22] *}

それでも、デフォルトの統合機能を使っていないにもかかわらず、YAMLで受け取りたいデータのために、Pydanticモデルを使って手動でJSON Schemaを生成しています。

そしてリクエストを直接使い、ボディを `bytes` として抽出します。これは、FastAPIがリクエストペイロードをJSONとしてパースしようとすらしないことを意味します。

その後、コード内でそのYAMLコンテンツを直接パースし、さらに同じPydanticモデルを使ってYAMLコンテンツを検証しています。

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[24:31] *}

/// tip | 豆知識

ここでは同じPydanticモデルを再利用しています。

ただし同様に、別の方法で検証することもできます。

///
