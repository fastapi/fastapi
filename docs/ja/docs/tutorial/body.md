# リクエストボディ { #request-body }

クライアント（例えばブラウザ）からAPIにデータを送信する必要がある場合、**リクエストボディ**として送信します。

**リクエスト**ボディは、クライアントからAPIへ送信されるデータです。**レスポンス**ボディは、APIがクライアントに送信するデータです。

APIはほとんどの場合 **レスポンス** ボディを送信する必要があります。しかしクライアントは、常に **リクエストボディ** を送信する必要があるとは限りません。場合によっては、クエリパラメータ付きのパスだけをリクエストして、ボディを送信しないこともあります。

**リクエスト**ボディを宣言するには、<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> モデルを使用し、その強力な機能とメリットをすべて利用します。

/// info | 情報

データを送信するには、`POST`（より一般的）、`PUT`、`DELETE`、`PATCH` のいずれかを使用すべきです。

`GET` リクエストでボディを送信することは仕様上は未定義の動作ですが、それでもFastAPIではサポートされています。ただし、非常に複雑／極端なユースケースのためだけです。

推奨されないため、Swagger UIによる対話的ドキュメントでは `GET` 使用時のボディのドキュメントは表示されず、途中のプロキシが対応していない可能性もあります。

///

## Pydanticの `BaseModel` をインポート { #import-pydantics-basemodel }

まず、`pydantic` から `BaseModel` をインポートする必要があります:

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## データモデルの作成 { #create-your-data-model }

次に、`BaseModel` を継承するクラスとしてデータモデルを宣言します。

すべての属性に標準のPython型を使用します:

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}


クエリパラメータの宣言と同様に、モデル属性がデフォルト値を持つ場合は必須ではありません。そうでなければ必須です。単にオプションにするには `None` を使用してください。

例えば、上記のモデルは次のようなJSON「`object`」（またはPythonの `dict`）を宣言します:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...`description` と `tax` はオプション（デフォルト値が `None`）なので、このJSON「`object`」も有効です:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## パラメータとして宣言 { #declare-it-as-a-parameter }

*path operation* に追加するには、パスパラメータやクエリパラメータを宣言したのと同じ方法で宣言します:

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

...そして、作成したモデル `Item` を型として宣言します。

## 結果 { #results }

そのPythonの型宣言だけで **FastAPI** は以下を行います:

* リクエストのボディをJSONとして読み取ります。
* 対応する型に変換します（必要な場合）。
* データを検証します。
    * データが無効な場合は、どこで何が不正なデータだったのかを正確に示す、分かりやすい明確なエラーを返します。
* 受け取ったデータをパラメータ `item` に渡します。
    * 関数内で `Item` 型として宣言したため、すべての属性とその型について、エディタサポート（補完など）も利用できます。
* モデル向けの <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> 定義を生成します。プロジェクトにとって意味があるなら、他の場所でも好きなように利用できます。
* それらのスキーマは生成されるOpenAPIスキーマの一部となり、自動ドキュメントの <abbr title="User Interfaces - ユーザーインターフェース">UIs</abbr> で使用されます。

## 自動ドキュメント { #automatic-docs }

モデルのJSON Schemaは、OpenAPIで生成されたスキーマの一部になり、対話的なAPIドキュメントに表示されます:

<img src="/img/tutorial/body/image01.png">

また、それらが必要な各 *path operation* 内のAPIドキュメントでも使用されます:

<img src="/img/tutorial/body/image02.png">

## エディタサポート { #editor-support }

エディタ上で、関数内のあらゆる場所で型ヒントと補完が得られます（Pydanticモデルの代わりに `dict` を受け取った場合は起きません）:

<img src="/img/tutorial/body/image03.png">

不正な型操作に対するエラーチェックも得られます:

<img src="/img/tutorial/body/image04.png">

これは偶然ではなく、フレームワーク全体がその設計を中心に構築されています。

そして、すべてのエディタで動作することを確実にするために、実装前の設計フェーズで徹底的にテストされました。

これをサポートするために、Pydantic自体にもいくつかの変更が加えられました。

前述のスクリーンショットは <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a> で撮影されたものです。

ただし、<a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> や、他のほとんどのPythonエディタでも同じエディタサポートを得られます:

<img src="/img/tutorial/body/image05.png">

/// tip | 豆知識

エディタとして <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> を使用している場合、<a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a> を使用できます。

以下により、Pydanticモデルに対するエディタサポートが改善されます:

* auto-completion
* type checks
* refactoring
* searching
* inspections

///

## モデルを使用する { #use-the-model }

関数内では、モデルオブジェクトのすべての属性に直接アクセスできます:

{* ../../docs_src/body/tutorial002_py310.py *}

## リクエストボディ + パスパラメータ { #request-body-path-parameters }

パスパラメータとリクエストボディを同時に宣言できます。

**FastAPI** は、パスパラメータに一致する関数パラメータは **パスから取得** し、Pydanticモデルとして宣言された関数パラメータは **リクエストボディから取得** すべきだと認識します。

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}


## リクエストボディ + パス + クエリパラメータ { #request-body-path-query-parameters }

**body**、**path**、**query** パラメータもすべて同時に宣言できます。

**FastAPI** はそれぞれを認識し、正しい場所からデータを取得します。

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

関数パラメータは以下のように認識されます:

* パラメータが **path** でも宣言されている場合、パスパラメータとして使用されます。
* パラメータが **単数型**（`int`、`float`、`str`、`bool` など）の場合、**query** パラメータとして解釈されます。
* パラメータが **Pydanticモデル** の型として宣言されている場合、リクエスト **body** として解釈されます。

/// note | 備考

FastAPIは、デフォルト値 `= None` があるため、`q` の値が必須ではないことを認識します。

`str | None` は、値が必須ではないことを判断するためにFastAPIでは使用されません。`= None` というデフォルト値があるため、必須ではないことを認識します。

しかし、型アノテーションを追加すると、エディタがより良いサポートを提供し、エラーを検出できるようになります。

///

## Pydanticを使わない方法 { #without-pydantic }

Pydanticモデルを使いたくない場合は、**Body** パラメータも使用できます。[Body - Multiple Parameters: Singular values in body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank} のドキュメントを参照してください。
