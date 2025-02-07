# スキーマの追加 - 例

JSON Schemaに追加する情報を定義することができます。

一般的なユースケースはこのドキュメントで示されているように`example`を追加することです。

JSON Schemaの追加情報を宣言する方法はいくつかあります。

## Pydanticの`schema_extra`

<a href="https://docs.pydantic.dev/latest/concepts/json_schema/#schema-customization" class="external-link" target="_blank">Pydanticのドキュメント: スキーマのカスタマイズ</a>で説明されているように、`Config`と`schema_extra`を使ってPydanticモデルの例を宣言することができます:

{* ../../docs_src/schema_extra_example/tutorial001.py hl[15,16,17,18,19,20,21,22,23] *}

その追加情報はそのまま出力され、JSON Schemaに追加されます。

## `Field`の追加引数

後述する`Field`、`Path`、`Query`、`Body`などでは、任意の引数を関数に渡すことでJSON Schemaの追加情報を宣言することもできます:

{* ../../docs_src/schema_extra_example/tutorial002.py hl[4,10,11,12,13] *}

/// warning | 注意

これらの追加引数が渡されても、文書化のためのバリデーションは追加されず、注釈だけが追加されることを覚えておいてください。

///

## `Body`の追加引数

追加情報を`Field`に渡すのと同じように、`Path`、`Query`、`Body`などでも同じことができます。

例えば、`Body`にボディリクエストの`example`を渡すことができます:

{* ../../docs_src/schema_extra_example/tutorial003.py hl[21,22,23,24,25,26] *}

## ドキュメントのUIの例

上記のいずれの方法でも、`/docs`の中では以下のようになります:

<img src="https://fastapi.tiangolo.com/img/tutorial/body-fields/image01.png">

## 技術詳細

`example` と `examples`について...

JSON Schemaの最新バージョンでは<a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a>というフィールドを定義していますが、OpenAPIは`examples`を持たない古いバージョンのJSON Schemaをベースにしています。

そのため、OpenAPIでは同じ目的のために<a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#fixed-fields-20" class="external-link" target="_blank">`example`</a>を独自に定義しており（`examples`ではなく`example`として）、それがdocs UI（Swagger UIを使用）で使用されています。

つまり、`example`はJSON Schemaの一部ではありませんが、OpenAPIの一部であり、それがdocs UIで使用されることになります。

## その他の情報

同じように、フロントエンドのユーザーインターフェースなどをカスタマイズするために、各モデルのJSON Schemaに追加される独自の追加情報を追加することができます。
