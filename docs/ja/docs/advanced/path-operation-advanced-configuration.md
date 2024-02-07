# Path Operationの高度な設定

## OpenAPI operationId

!!! warning "注意"
    あなたがOpenAPIの「エキスパート」でなければ、これは必要ないかもしれません。

*path operation* で `operation_id` パラメータを利用することで、OpenAPIの `operationId` を設定できます。

`operation_id` は各オペレーションで一意にする必要があります。

```Python hl_lines="6"
{!../../../docs_src/path_operation_advanced_configuration/tutorial001.py!}
```

### *path operation関数* の名前をoperationIdとして使用する

APIの関数名を `operationId` として利用したい場合、すべてのAPIの関数をイテレーションし、各 *path operation* の `operationId` を `APIRoute.name` で上書きすれば可能です。

そうする場合は、すべての *path operation* を追加した後に行う必要があります。

```Python hl_lines="2  12-21  24"
{!../../../docs_src/path_operation_advanced_configuration/tutorial002.py!}
```

!!! tip "豆知識"
    `app.openapi()` を手動でコールする場合、その前に`operationId`を更新する必要があります。

!!! warning "注意"
    この方法をとる場合、各 *path operation関数* が一意な名前である必要があります。

    それらが異なるモジュール (Pythonファイル) にあるとしてもです。

## OpenAPIから除外する

生成されるOpenAPIスキーマ (つまり、自動ドキュメント生成の仕組み) から *path operation* を除外するには、 `include_in_schema` パラメータを `False` にします。

```Python hl_lines="6"
{!../../../docs_src/path_operation_advanced_configuration/tutorial003.py!}
```

## docstringによる説明の高度な設定

*path operation関数* のdocstringからOpenAPIに使用する行を制限することができます。

`\f` (「書式送り (Form Feed)」のエスケープ文字) を付与することで、**FastAPI** はOpenAPIに使用される出力をその箇所までに制限します。

ドキュメントには表示されませんが、他のツール (例えばSphinx) では残りの部分を利用できるでしょう。

```Python hl_lines="19-29"
{!../../../docs_src/path_operation_advanced_configuration/tutorial004.py!}
```
