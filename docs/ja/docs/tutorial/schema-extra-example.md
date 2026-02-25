# リクエストのExampleデータの宣言 { #declare-request-example-data }

アプリが受け取れるデータの例を宣言できます。

ここでは、それを行ういくつかの方法を紹介します。

## Pydanticモデルでの追加JSON Schemaデータ { #extra-json-schema-data-in-pydantic-models }

生成されるJSON Schemaに追加されるPydanticモデルの`examples`を宣言できます。

{* ../../docs_src/schema_extra_example/tutorial001_py310.py hl[13:24] *}

その追加情報は、そのモデルの出力**JSON Schema**にそのまま追加され、APIドキュメントで使用されます。

<a href="https://docs.pydantic.dev/latest/api/config/" class="external-link" target="_blank">Pydanticのドキュメント: Configuration</a>で説明されているように、`dict`を受け取る属性`model_config`を使用できます。

生成されるJSON Schemaに表示したい追加データ（`examples`を含む）を含む`dict`を使って、`"json_schema_extra"`を設定できます。

/// tip | 豆知識

同じ手法を使ってJSON Schemaを拡張し、独自のカスタム追加情報を追加できます。

例えば、フロントエンドのユーザーインターフェースのためのメタデータを追加する、などに使えます。

///

/// info | 情報

OpenAPI 3.1.0（FastAPI 0.99.0以降で使用）では、**JSON Schema**標準の一部である`examples`がサポートされました。

それ以前は、単一の例を持つキーワード`example`のみがサポートされていました。これはOpenAPI 3.1.0でも引き続きサポートされていますが、非推奨であり、JSON Schema標準の一部ではありません。そのため、`example`から`examples`への移行が推奨されます。🤓

詳細はこのページの最後で読めます。

///

## `Field`の追加引数 { #field-additional-arguments }

Pydanticモデルで`Field()`を使う場合、追加の`examples`も宣言できます:

{* ../../docs_src/schema_extra_example/tutorial002_py310.py hl[2,8:11] *}

## JSON Schema内の`examples` - OpenAPI { #examples-in-json-schema-openapi }

以下のいずれかを使用する場合:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

追加情報を含む`examples`のグループを宣言でき、それらは**OpenAPI**内のそれぞれの**JSON Schemas**に追加されます。

### `examples`を使う`Body` { #body-with-examples }

ここでは、`Body()`で期待されるデータの例を1つ含む`examples`を渡します:

{* ../../docs_src/schema_extra_example/tutorial003_an_py310.py hl[22:29] *}

### ドキュメントUIでの例 { #example-in-the-docs-ui }

上記のいずれの方法でも、`/docs`の中では以下のようになります:

<img src="/img/tutorial/body-fields/image01.png">

### 複数の`examples`を使う`Body` { #body-with-multiple-examples }

もちろん、複数の`examples`を渡すこともできます:

{* ../../docs_src/schema_extra_example/tutorial004_an_py310.py hl[23:38] *}

この場合、examplesはそのボディデータの内部**JSON Schema**の一部になります。

それでも、<dfn title="2023-08-26">執筆時点</dfn>では、ドキュメントUIの表示を担当するツールであるSwagger UIは、**JSON Schema**内のデータに対して複数の例を表示することをサポートしていません。しかし、回避策については以下を読んでください。

### OpenAPI固有の`examples` { #openapi-specific-examples }

**JSON Schema**が`examples`をサポートする前から、OpenAPIは同じく`examples`という別のフィールドをサポートしていました。

この**OpenAPI固有**の`examples`は、OpenAPI仕様の別のセクションに入ります。各JSON Schemaの中ではなく、**各*path operation*の詳細**に入ります。

そしてSwagger UIは、この特定の`examples`フィールドを以前からサポートしています。そのため、これを使って**ドキュメントUIに異なる例を表示**できます。

このOpenAPI固有フィールド`examples`の形は**複数の例**（`list`ではなく）を持つ`dict`であり、それぞれに追加情報が含まれ、その追加情報は**OpenAPI**にも追加されます。

これはOpenAPIに含まれる各JSON Schemaの中には入らず、外側の、*path operation*に直接入ります。

### `openapi_examples`パラメータの使用 { #using-the-openapi-examples-parameter }

FastAPIでは、以下に対してパラメータ`openapi_examples`を使って、OpenAPI固有の`examples`を宣言できます:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

`dict`のキーは各例を識別し、各値は別の`dict`です。

`examples`内の各特定の例`dict`には、次の内容を含められます:

* `summary`: 例の短い説明。
* `description`: Markdownテキストを含められる長い説明。
* `value`: 実際に表示される例（例: `dict`）。
* `externalValue`: `value`の代替で、例を指すURLです。ただし、`value`ほど多くのツールでサポートされていない可能性があります。

次のように使えます:

{* ../../docs_src/schema_extra_example/tutorial005_an_py310.py hl[23:49] *}

### ドキュメントUIのOpenAPI Examples { #openapi-examples-in-the-docs-ui }

`Body()`に`openapi_examples`を追加すると、`/docs`は次のようになります:

<img src="/img/tutorial/body-fields/image02.png">

## 技術詳細 { #technical-details }

/// tip | 豆知識

すでに**FastAPI**バージョン**0.99.0以上**を使用している場合、おそらくこれらの詳細は**スキップ**できます。

これらは、OpenAPI 3.1.0が利用可能になる前の古いバージョンにより関連します。

これは簡単なOpenAPIとJSON Schemaの**歴史の授業**だと考えられます。🤓

///

/// warning | 注意

ここでは、標準である**JSON Schema**と**OpenAPI**についての非常に技術的な詳細を扱います。

上のアイデアがすでにうまく動いているなら、それで十分かもしれませんし、おそらくこの詳細は不要です。気軽にスキップしてください。

///

OpenAPI 3.1.0より前は、OpenAPIは古く改変されたバージョンの**JSON Schema**を使用していました。

JSON Schemaには`examples`がなかったため、OpenAPIは自身が改変したバージョンに独自の`example`フィールドを追加しました。

OpenAPIは、仕様の他の部分にも`example`と`examples`フィールドを追加しました:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#parameter-object" class="external-link" target="_blank">`Parameter Object`（仕様内）</a>。FastAPIの以下で使用されました:
    * `Path()`
    * `Query()`
    * `Header()`
    * `Cookie()`
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#media-type-object" class="external-link" target="_blank">`Request Body Object`。仕様内の`Media Type Object`の`content`フィールド（仕様内）</a>。FastAPIの以下で使用されました:
    * `Body()`
    * `File()`
    * `Form()`

/// info | 情報

この古いOpenAPI固有の`examples`パラメータは、FastAPI `0.103.0`以降は`openapi_examples`になりました。

///

### JSON Schemaの`examples`フィールド { #json-schemas-examples-field }

しかしその後、JSON Schemaは新しいバージョンの仕様に<a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a>フィールドを追加しました。

そして、新しいOpenAPI 3.1.0は、この新しいフィールド`examples`を含む最新バージョン（JSON Schema 2020-12）に基づくようになりました。

そして現在、この新しい`examples`フィールドは、古い単一（かつカスタム）の`example`フィールドより優先され、`example`は現在非推奨です。

JSON Schemaのこの新しい`examples`フィールドは、OpenAPIの他の場所（上で説明）にあるような追加メタデータを持つdictではなく、**単なる例の`list`**です。

/// info | 情報

OpenAPI 3.1.0がこのJSON Schemaとの新しいよりシンプルな統合とともにリリースされた後も、しばらくの間、自動ドキュメントを提供するツールであるSwagger UIはOpenAPI 3.1.0をサポートしていませんでした（バージョン5.0.0からサポートされています🎉）。

そのため、FastAPI 0.99.0より前のバージョンは、OpenAPI 3.1.0より低いバージョンのOpenAPIをまだ使用していました。

///

### PydanticとFastAPIの`examples` { #pydantic-and-fastapi-examples }

Pydanticモデル内で、`schema_extra`または`Field(examples=["something"])`を使って`examples`を追加すると、その例はそのPydanticモデルの**JSON Schema**に追加されます。

そしてそのPydanticモデルの**JSON Schema**はAPIの**OpenAPI**に含まれ、ドキュメントUIで使用されます。

FastAPI 0.99.0より前のバージョン（0.99.0以上は新しいOpenAPI 3.1.0を使用）では、他のユーティリティ（`Query()`、`Body()`など）で`example`または`examples`を使っても、それらの例はそのデータを説明するJSON Schema（OpenAPI独自版のJSON Schemaでさえ）には追加されず、OpenAPI内の*path operation*宣言に直接追加されていました（JSON Schemaを使用するOpenAPIの部分の外側）。

しかし、FastAPI 0.99.0以上ではOpenAPI 3.1.0を使用し、それはJSON Schema 2020-12とSwagger UI 5.0.0以上を使うため、すべてがより一貫し、例はJSON Schemaに含まれます。

### Swagger UIとOpenAPI固有の`examples` { #swagger-ui-and-openapi-specific-examples }

Swagger UIは複数のJSON Schema examplesをサポートしていなかった（2023-08-26時点）ため、ユーザーはドキュメントで複数の例を表示する手段がありませんでした。

それを解決するため、FastAPI `0.103.0`は、新しいパラメータ`openapi_examples`で、同じ古い**OpenAPI固有**の`examples`フィールドを宣言するための**サポートを追加**しました。🤓

### まとめ { #summary }

昔は歴史があまり好きではないと言っていました...が、今の私は「技術の歴史」の授業をしています。😅

要するに、**FastAPI 0.99.0以上にアップグレード**してください。そうすれば、物事はもっと**シンプルで一貫性があり直感的**になり、これらの歴史的詳細を知る必要もありません。😎
