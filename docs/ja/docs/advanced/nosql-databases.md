# NoSQL (分散 / ビッグデータ) Databases

**FastAPI** はあらゆる <abbr title="分散データベース (Big Data)や 'Not Only SQL'">NoSQL</abbr>と統合することもできます。

ここでは<abbr title="ここでのドキュメントとは、キーと値を持つJSONオブジェクト（ディクショナリー）をあらわし、これらの値は他のJSONオブジェクトや配列（リスト）、数値、文字列、真偽値などにすることができます。">ドキュメント</abbr>ベースのNoSQLデータベースである**<a href="https://www.couchbase.com/" class="external-link" target="_blank">Couchbase</a>**を使用した例を見てみましょう。

他にもこれらのNoSQLデータベースを利用することが出来ます:

* **MongoDB**
* **Cassandra**
* **CouchDB**
* **ArangoDB**
* **ElasticSearch** など。

!!! tip "豆知識"
    **FastAPI**と**Couchbase**を使った公式プロジェクト・ジェネレータがあります。すべて**Docker**ベースで、フロントエンドやその他のツールも含まれています: <a href="https://github.com/tiangolo/full-stack-fastapi-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-couchbase</a>

## Couchbase コンポーネントの Import

まずはImportしましょう。今はその他のソースコードに注意を払う必要はありません。

```Python hl_lines="3-5"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

## "document type" として利用する定数の定義

documentで利用する固定の`type`フィールドを用意しておきます。

これはCouchbaseで必須ではありませんが、後々の助けになるベストプラクティスです。

```Python hl_lines="9"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

## `Bucket` を取得する関数の追加

**Couchbase**では、bucketはdocumentのセットで、様々な種類のものがあります。

Bucketは通常、同一のアプリケーション内で互いに関係を持っています。

リレーショナルデータベースの世界でいう"database"(データベースサーバではなく特定のdatabase)と類似しています。

**MongoDB** で例えると"collection"と似た概念です。

次のコードでは主に `Bucket` を利用してCouchbaseを操作します。

この関数では以下の処理を行います:

* **Couchbase** クラスタ(1台の場合もあるでしょう)に接続
    * タイムアウトのデフォルト値を設定
* クラスタで認証を取得
* `Bucket` インスタンスを取得
    * タイムアウトのデフォルト値を設定
* 作成した`Bucket`インスタンスを返却

```Python hl_lines="12-21"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

## Pydantic モデルの作成

**Couchbase**のdocumentは実際には単にJSONオブジェクトなのでPydanticを利用してモデルに出来ます。

### `User` モデル

まずは`User`モデルを作成してみましょう:

```Python hl_lines="24-28"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

このモデルは*path operation*に使用するので`hashed_password`は含めません。

### `UserInDB` モデル

それでは`UserInDB`モデルを作成しましょう。

こちらは実際にデータベースに保存されるデータを保持します。

`User`モデルの持つ全ての属性に加えていくつかの属性を追加するのでPydanticの`BaseModel`を継承せずに`User`のサブクラスとして定義します:

```Python hl_lines="31-33"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

!!! note "備考"
    データベースに保存される`hashed_password`と`type`フィールドを`UserInDB`モデルに保持させていることに注意してください。

    しかしこれらは(*path operation*で返却する)一般的な`User`モデルには含まれません

## user の取得

それでは次の関数を作成しましょう:

* username を取得する
* username を利用してdocumentのIDを生成する
* 作成したIDでdocumentを取得する
* documentの内容を`UserInDB`モデルに設定する

*path operation関数*とは別に、`username`(またはその他のパラメータ)からuserを取得することだけに特化した関数を作成することで、より簡単に複数の部分で再利用したり<abbr title="コードで書かれた自動テストで、他のコードが正しく動作しているかどうかをチェックするもの。">ユニットテスト</abbr>を追加することができます。

```Python hl_lines="36-42"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

### f-strings

`f"userprofile::{username}"` という記載に馴染みがありませんか？これは Python の"<a href="https://docs.python.org/3/glossary.html#term-f-string" class="external-link" target="_blank">f-string</a>"と呼ばれるものです。

f-stringの`{}`の中に入れられた変数は、文字列の中に展開/注入されます。

### `dict` アンパック

`UserInDB(**result.value)`という記載に馴染みがありませんか？<a href="https://docs.python.org/3/glossary.html#term-argument" class="external-link" target="_blank">これは`dict`の"アンパック"</a>と呼ばれるものです。

これは`result.value`の`dict`からそのキーと値をそれぞれ取りキーワード引数として`UserInDB`に渡します。

例えば`dict`が下記のようになっていた場合:

```Python
{
    "username": "johndoe",
    "hashed_password": "some_hash",
}
```

`UserInDB`には次のように渡されます:

```Python
UserInDB(username="johndoe", hashed_password="some_hash")
```

## **FastAPI** コードの実装

### `FastAPI` app の作成

```Python hl_lines="46"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

### *path operation関数*の作成

私たちのコードはCouchbaseを呼び出しており、<a href="https://docs.couchbase.com/python-sdk/2.5/async-programming.html#asyncio-python-3-5" class="external-link" target="_blank">実験的なPython <code>await</code></a>を使用していないので、私たちは`async def`ではなく通常の`def`で関数を宣言する必要があります。

また、Couchbaseは単一の`Bucket`オブジェクトを複数の<abbr title="プログラムによって実行される一連のコードのことで、同時に、または間隔をおいて他のコードも実行されることがあります。">スレッド</abbr>で使用しないことを推奨していますので、単に直接Bucketを取得して関数に渡すことが出来ます。

```Python hl_lines="49-53"
{!../../../docs_src/nosql_databases/tutorial001.py!}
```

## まとめ

他のサードパーティ製のNoSQLデータベースを利用する場合でも、そのデータベースの標準ライブラリを利用するだけで利用できます。

他の外部ツール、システム、APIについても同じことが言えます。
