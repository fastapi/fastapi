# パスオペレーションの高度な設定

## OpenAPI operationId

!!! warning "注意"
    あなたがOpenAPIの「エキスパート」でなければ、これは必要ありません。

*パスオペレーション* で `operationId` パラメータを利用することで、OpenAPIの `operationId` を設定できます。

各オペレーションで一意にする必要があります。

```Python hl_lines="6"
{!../../../docs_src/path_operation_advanced_configuration/tutorial001.py!}
```

### *パスオペレーション関数* の名前をoperationIdとして使用する

APIの関数名を `operationId` として利用したい場合、それらをイテレーションし各 *パスオペレーション* の `operationId` を `APIRoute.name` で上書きすれば可能です。

そうする場合は、すべての *パスオペレーション* を追加した後に行う必要があります。

```Python hl_lines="2  12-21  24"
{!../../../docs_src/path_operation_advanced_configuration/tutorial002.py!}
```

!!! tip "豆知識"
    `app.openapi()` を手動でコールする場合、その前に`operationId`を更新する必要があります。

!!! warning "注意"
    この方法をとる場合、各 *パスオペレーション関数* が一意な名前である必要があります。

    それらが異なるモジュール (Pythonファイル) にあるとしてもです。

## OpenAPIから除外する

*パスオペレーション* を、生成されるOpenAPIスキーマ (つまり、自動ドキュメント生成の仕組み) から除外するには、 `include_in_schema` パラメータを `False` にします。

```Python hl_lines="6"
{!../../../docs_src/path_operation_advanced_configuration/tutorial003.py!}
```

## docstringによる高度な説明

*パスオペレーション関数* のdocstringからOpenAPIに使用する行を制限することができます。

`\f` (「フォームフィード」から除外する記号) を付与することで、**FastAPI** はこの時点でOpenAPIに使用される出力を切り捨てます。

ドキュメントには表示されませんが、他のツール (例えばSphinx) では残りの部分を利用することができるでしょう。

```Python hl_lines="19-29"
{!../../../docs_src/path_operation_advanced_configuration/tutorial004.py!}
```
