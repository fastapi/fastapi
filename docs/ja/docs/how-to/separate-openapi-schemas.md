# 入力と出力でOpenAPIのスキーマを分けるかどうか { #separate-openapi-schemas-for-input-and-output-or-not }

**Pydantic v2** のリリース以降、生成される OpenAPI は以前より少し正確で、より正しいものになりました。😎

実際には、場合によっては同じ Pydantic モデルに対して、入力用と出力用で OpenAPI に **2 つの JSON Schema** が含まれることがあります。これは **デフォルト値** の有無に依存します。

その動作と、必要に応じての変更方法を見ていきます。

## 入出力のPydanticモデル { #pydantic-models-for-input-and-output }

次のようにデフォルト値を持つ Pydantic モデルがあるとします。

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:7] hl[7] *}

### 入力用モデル { #model-for-input }

このモデルを次のように入力として使うと:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:15] hl[14] *}

...`description` フィールドは **必須ではありません**。デフォルト値が `None` だからです。

### ドキュメントでの入力モデル { #input-model-in-docs }

ドキュメントで確認すると、`description` フィールドには **赤いアスタリスク** が付いておらず、必須としてはマークされていません:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image01.png">
</div>

### 出力用モデル { #model-for-output }

しかし同じモデルを次のように出力として使う場合:

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py hl[19] *}

...`description` にデフォルト値があるため、そのフィールドに何も返さなくても、その **デフォルト値** が入ります。

### 出力のレスポンスデータ { #model-for-output-response-data }

ドキュメントから試してレスポンスを確認すると、コードでは一方の `description` フィールドに何も追加していないにもかかわらず、JSON レスポンスにはデフォルト値（`null`）が含まれています:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image02.png">
</div>

つまりそのフィールドには **常に値があります**。値が `None`（JSON では `null`）になることがあるだけです。

したがって、この API を使うクライアントは値の有無を確認する必要がなく、フィールドが **常に存在する** と仮定できます。場合によってはデフォルト値の `None` になるだけです。

これを OpenAPI で表現するには、そのフィールドを **必須** としてマークします。常に存在するためです。

このため、モデルの JSON Schema は、**入力か出力か** によって異なる場合があります:

- **入力** では `description` は **必須ではない**
- **出力** では **必須**（値は `None`、JSON では `null` の可能性あり）

### ドキュメントでの出力モデル { #model-for-output-in-docs }

ドキュメントで出力モデルを見ると、`name` と `description` の **両方** が **赤いアスタリスク** で **必須** としてマークされています:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image03.png">
</div>

### ドキュメントでの入力・出力モデル { #model-for-input-and-output-in-docs }

さらに、OpenAPI に含まれる利用可能なスキーマ（JSON Schema）を確認すると、`Item-Input` と `Item-Output` の 2 つがあることが分かります。

`Item-Input` では、`description` は **必須ではありません**（赤いアスタリスクなし）。

一方、`Item-Output` では、`description` は **必須**（赤いアスタリスクあり）です。

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image04.png">
</div>

この **Pydantic v2** の機能により、API ドキュメントはより **正確** になり、自動生成されたクライアントや SDK もより正確になります。これにより、より良い **開発者エクスペリエンス** と一貫性が得られます。🎉

## スキーマを分けない { #do-not-separate-schemas }

一方で、**入力と出力で同じスキーマ** にしたい場合もあります。

主なユースケースは、すでに自動生成されたクライアントコードや SDK があり、まだそれらをすべて更新したくない場合です。いずれは更新したいとしても、今ではないかもしれません。

その場合は、**FastAPI** のパラメータ `separate_input_output_schemas=False` でこの機能を無効化できます。

/// info | 情報

`separate_input_output_schemas` のサポートは FastAPI `0.102.0` で追加されました。🤓

///

{* ../../docs_src/separate_openapi_schemas/tutorial002_py310.py hl[10] *}

### ドキュメントで入力・出力に同一スキーマを使用 { #same-schema-for-input-and-output-models-in-docs }

これでモデルの入力と出力は単一のスキーマ、`Item` のみになり、`description` は **必須ではありません**:

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image05.png">
</div>
