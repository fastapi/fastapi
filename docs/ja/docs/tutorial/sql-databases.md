# SQL (Relational) Databases

!!! info"情報"
これらの情報は間もなく更新されます。 🎉

    現在のバージョンは Pydantic v1、SQLAlchemy のバージョンは 2.0 未満を想定しています。

    新しいドキュメントには Pydantic v2 が含まれ、<a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a> (これも SQLAlchemy をベースにしています) が Pydantic v2 を使用するように更新され次第、SQLModel も使用される予定です。

**FastAPI** はあなたに SQL(relational)を使用することを要求しません。

But you can use any relational database that you want.
しかし、あなたが望むどの SQL(relational)も利用することができます。

ここに <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a>を利用した例があります。

あなたは簡単に以下にあるような SQLAlchemy によってサポートされたどのデータベースも利用することが可能可能です。

- PostgreSQL
- MySQL
- SQLite
- Oracle
- Microsoft SQL Server, etc.

In this example, we'll use **SQLite**, because it uses a single file and Python has integrated support. So, you can copy this example and run it as is.
この例では、**SQLite** を使用します。**SQLite**は単一のファイルを使用し、Python に統合サポートが組み込まれているためです。 そのため、この例をコピーしてそのまま実行できます。

後ほど、本番環境のアプリケーションでは、**PostgreSQL**のようなデータベースサーバーを使用したくなるかもしれません。

!!! tip "豆知識"
**FastAPI**と**PostgreSQL**を使用した公式プロジェクトジェネレーターがあります。すべて Docker ベースで、フロントエンドやその他のツールも含まれています。 <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

!!! note "備考"
ほとんどのコードは、フレームワークに依存しない標準的な `SQLAlchemy` のコードであることに注意してください。

    **FastAPI**特有のコードは常に最小限です

## ORMs(オブジェクト関係マッピング)

**FastAPI**は、あらゆるデータベース、そしてデータベースと通信するためのあらゆるスタイルのライブラリと連携します。

一般的なパターンは、「ORM」: つまり「オブジェクト関係マッピング」ライブラリを使用することです。

ORM には、コード内の _オブジェクト_ とデータベースのテーブル（_リレーション_）間で変換（「_マッピング_」）を行うためのツールがあります。

ORM を使用すると、通常は SQL データベース内のテーブルを表すクラスを作成します。クラスの各属性は列を表し、名前と型を持ちます。

例えば、`Pet` というクラスは、`pets` という SQL テーブルを表すことができます。

そして、そのクラスの _インスタンス_ オブジェクトはそれぞれ、データベース内の行を表します。

例えば、`orion_cat` というオブジェクト (`Pet` のインスタンス) は、`type` という列に対応する `orion_cat.type` という属性を持つことができます。そして、その属性の値は、例えば `"cat"` となります。

これらの ORM には、テーブルやエンティティ間の接続や関係を作成するためのツールも用意されています。

このように、orion_cat.owner という属性を持つこともできます。そして、owner には、owners テーブルから取得された、このペットの飼い主のデータが含まれます。

つまり、orion_cat.owner.name は、このペットの飼い主の名前 (owners テーブルの name 列から取得) になります。

例えば "Arquilian" という値を持つことができます。

そして、ORM は、ペットオブジェクトからアクセスしようとしたときに、対応するテーブル _owners_ から情報を取得するためのすべての処理を行います。

一般的な ORM には、例えば Django-ORM (Django フレームワークの一部)、SQLAlchemy ORM (SQLAlchemy の一部、フレームワークに依存しない)、Peewee (フレームワークに依存しない) などがあります。

ここでは **SQLAlchemy ORM** の使用方法を見ていきます。

同様の方法で、他の ORM を使用することもできます

!!! tip "豆知識"
Peewee を使用した同様の記事が、このドキュメントにあります。

## ファイル構造

これらの例では、`my_super_project` という名前のディレクトリがあり、その中に `sql_app` という名前のサブディレクトリがあるとします。その構造は次のとおりです。

```
.
└── sql_app
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    ├── models.py
    └── schemas.py
```

`__init__.py` ファイルは空のファイルですが、これにより Python は、（Python ファイルである）すべてのモジュールを含む`sql_app`がパッケージであることを認識します。

では、各ファイル/モジュールが何をするのかを見ていきましょう。

## `SQLAlchemy`をインストールする

最初に`SQLAlchemy`をインストールする必要があります。

<div class="termy">

```console
$ pip install sqlalchemy

---> 100%
```

</div>

## SQLAlchemy のパーツを作成する

このファイルを参照してください。 `sql_app/database.py`.

### SQLAlchemy のパーツをインポートする

```Python hl_lines="1-3"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

### SQLAlchemy 用のデータベース URL を作成する

```Python hl_lines="5-6"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

この例では、SQLite データベースに「接続」しています（SQLite データベースを含むファイルを開いています）。

ファイルは、`sql_app.db` というファイル内の、同じディレクトリにあります。

そのため、最後の部分は `./sql_app.db` となっています。

**PostgreSQL** データベースを使用している場合は、次の行のコメントを外すだけです。

```Python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
```

...そして、データベースのデータと認証情報で適宜変更してください（MySQL、MariaDB、その他のデータベースでも同様です）

!!! tip "豆知識"

    これは、別のデータベースを使用したい場合に変更する必要がある主要な行です。

### SQLAlchemy `engine` を作成する

最初のステップは、SQLAlchemy の「エンジン」を作成することです。

この `engine` は、後で他の場所で使用します。

```Python hl_lines="8-10"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

#### 備考

議論:

```Python
connect_args={"check_same_thread": False}
```

...これは `SQLite`にのみ必要です。ほかのデータベースでは必要ありません。

!!! info "技術的な詳細"

    デフォルトでは、SQLite は 1 つのスレッドのみが自身と通信できるようにします。これは、各スレッドが独立したリクエストを処理すると想定しているためです。

    これは、異なるもの（異なるリクエスト）に対して同じ接続を誤って共有することを防ぐためです。

    しかし、FastAPI では、通常の関数 (`def`) を使用すると、複数のスレッドが同じリクエストに対してデータベースと対話する可能性があるため、
    `connect_args={"check_same_thread": False}` を使用して SQLite にそれを許可するように指示する必要があります。

    また、各リクエストが依存関係の中で独自のデータベース接続セッションを取得するようにするため、このデフォルトのメカニズムは必要ありません。

### `SessionLocal` クラスを作成する

`SessionLocal` クラスの各インスタンスは、データベースセッションになります。クラス自体は、まだデータベースセッションではありません。

しかし、`SessionLocal` クラスのインスタンスを作成すると、このインスタンスが実際のデータベースセッションになります。

SQLAlchemy からインポートした `Session` と区別するために、`SessionLocal` という名前を付けています。

`Session` (SQLAlchemy からインポートしたもの) は後で使用します。

`SessionLocal` クラスを作成するには、`sessionmaker` 関数を使用します。

```Python hl_lines="11"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

### `Base` クラスを作成する

次に、クラスを返す `declarative_base()` 関数を使用します。

後で、このクラスを継承して、データベースモデルまたはクラス（ORM モデル）を作成します。

```Python hl_lines="13"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

## Create the database models

このファイルを見てみましょう！ `sql_app/models.py`

### `Base` クラスから SQLAlchemy モデルを作成する

先ほど作成した `Base` クラスを使用して、SQLAlchemy モデルを作成します。

!!! tip "豆知識"
SQLAlchemy は、「**モデル**」という用語を使用して、データベースと対話するこれらのクラスやインスタンスを参照します。

    しかし、Pydantic も「**モデル**」という用語を使用して、データの検証、変換、およびドキュメントのクラスとインスタンスという、別のものを指します。

`database` (上記の `database.py` ファイル) から `Base` をインポートします。

それを継承するクラスを作成します。

これらのクラスが SQLAlchemy モデルです。

```Python hl_lines="4  7-8  18-19"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

`__tablename__` 属性は、これらの各モデルに対してデータベース内で使用するテーブル名を SQLAlchemy に伝えます。

### モデルの属性/列を作成する

次に、すべてのモデル (クラス) 属性を作成します。

これらの属性はそれぞれ、対応するデータベーステーブル内の列を表します。

デフォルト値として、SQLAlchemy の `Column` を使用します。

そして、データベース内の型を定義する SQLAlchemy クラスの「型」(`Integer`、`String`、`Boolean` など) を引数として渡します。

```Python hl_lines="1  10-13  21-24"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

### 関係(relationship)の作成

次に、リレーションシップを作成します。

これには、SQLAlchemy ORM によって提供される `relationship` を使用します。

これは、多かれ少なかれ、「マジック」属性となり、このテーブルに関連する他のテーブルの値を含みます。

```Python hl_lines="2  15  26"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

`my_user.items` のように `User` 内の `items` 属性にアクセスすると、`users` テーブル内のこのレコードを指す外部キーを持つ `Item` SQLAlchemy モデル (`items` テーブルからの) のリストが格納されます。

`my_user.items` にアクセスすると、SQLAlchemy は実際に `items` テーブル内のデータベースからアイテムを取得し、ここに格納します。

また、`Item` 内の `owner` 属性にアクセスすると、`users` テーブルからの `User` SQLAlchemy モデルが含まれます。`users` テーブルからどのレコードを取得するかを知るために、外部キーを持つ `owner_id` 属性/列を使用します。

## Create the Pydantic models

次にファイルを確認しましょう `sql_app/schemas.py`.

!!! tip "豆知識"
SQLAlchemy の _モデル_ と Pydantic の _モデル_ の混 confusion を避けるために、SQLAlchemy モデルを格納するファイル `models.py` と、Pydantic モデルを格納するファイル `schemas.py` を作成します。

    これらの Pydantic モデルは、多かれ少なかれ「スキーマ」（有効なデータの形状）を定義します。

    これにより、両方を使い分けるときに混乱を避けることができます。

### 初期の Pydantic _モデル_ / スキーマを作成する

データの作成や読み取り時に共通の属性を持つように、`ItemBase` と `UserBase` の Pydantic _モデル_ (あるいは「スキーマ」と呼ぶことにしましょう) を作成します。

そして、それらを継承する `ItemCreate` と `UserCreate` を作成します（これにより、同じ属性を持ちます）。さらに、作成に必要な追加のデータ（属性）を追加します。

したがって、ユーザーを作成するときは、`password` も持ちます。

ただし、セキュリティ上の理由から、`password` は他の Pydantic _モデル_ には含まれません。例えば、API からユーザーを読み取るときに、`password` は送信されません。

=== "Python 3.10+"

    ```Python hl_lines="1  4-6  9-10  21-22  25-26"
    {!> ../../../docs_src/sql_databases/sql_app_py310/schemas.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="3  6-8  11-12  23-24  27-28"
    {!> ../../../docs_src/sql_databases/sql_app_py39/schemas.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="3  6-8  11-12  23-24  27-28"
    {!> ../../../docs_src/sql_databases/sql_app/schemas.py!}
    ```

#### SQLAlchemy スタイルと Pydantic スタイル

SQLAlchemy _モデル_ は、`=` を使用して属性を定義し、`Column` にパラメータとして型を渡すことに注意してください

```Python
name = Column(String)
```

一方、Pydantic _モデル_ は、新しい型注釈構文/型ヒントを使用して、`:` で型を宣言します。

```Python
name: str
```

これらを覚えておいてください。そうすれば、= と : を使用するときに混乱することがなくなります。

###　読み取り/返却用の Pydantic モデル / スキーマを作成する

次に、データを読み取るとき、つまり API からデータを返すときに使用される Pydantic _モデル_ (スキーマ) を作成します。

例えば、アイテムを作成する前は、それに割り当てられる ID はわかりませんが、アイテムを読み取るとき (API から返すとき) は、すでにその ID がわかっています。

同様に、ユーザーを読み取るときに、`items` にはこのユーザーに属するアイテムが含まれることを宣言できます。

これらのアイテムの ID だけでなく、アイテムを読み取るための Pydantic _モデル_ (`Item`) で定義したすべてのデータも含まれます。

=== "Python 3.10+"

    ```Python hl_lines="13-15  29-32"
    {!> ../../../docs_src/sql_databases/sql_app_py310/schemas.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="15-17  31-34"
    {!> ../../../docs_src/sql_databases/sql_app_py39/schemas.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="15-17  31-34"
    {!> ../../../docs_src/sql_databases/sql_app/schemas.py!}
    ```

!!! tip "豆知識"
ユーザーを読み取るとき (API から返すとき) に使用される Pydantic _モデル_ である `User` には、`password` が含まれていないことに注意してください。

### Pydantic の `orm_mode` を使用する

次に、読み取り用の Pydantic _モデル_ である `Item` と `User` に、内部の `Config` クラスを追加します。

この <a href="https://docs.pydantic.dev/latest/api/config/" class="external-link" target="_blank">`Config`</a> クラスは、Pydantic に設定を提供するために使用されます。

`Config` クラスで、属性 `orm_mode = True` を設定します。

=== "Python 3.10+"

    ```Python hl_lines="13  17-18  29  34-35"
    {!> ../../../docs_src/sql_databases/sql_app_py310/schemas.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="15  19-20  31  36-37"
    {!> ../../../docs_src/sql_databases/sql_app_py39/schemas.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="15  19-20  31  36-37"
    {!> ../../../docs_src/sql_databases/sql_app/schemas.py!}
    ```

!!! tip "豆知識"
`orm_mode = True` のように、`=` を使用して値を代入していることに注意してください。

    これは、前の型宣言のように `:` を使用していません。

    これは、型を宣言するのではなく、設定値を設定しています。

    Pydantic の `orm_mode` は、`dict` ではなくても、ORM モデル (または属性を持つ任意のオブジェクト) であっても、Pydantic *モデル* にデータを読み取るように指示します。

    このようにして、次のように、`dict` から `id` 値を取得しようとするだけでなく、

```Python
id = data["id"]
```

次のように、属性からも取得しようとします。

```Python
id = data.id
```

このようにして、Pydantic _モデル_ は ORM と互換性を持つようになり、_パス操作_ の `response_model` 引数で宣言するだけで済みます。

データベースモデルを返すことができ、そこからデータを読み取ることができます。

#### ORM モードに関する技術的な詳細

SQLAlchemy をはじめとする多くの ORM は、デフォルトで「遅延読み込み」になっています。

これは、例えば、関係を持つデータを含む属性にアクセスしようとしない限り、データベースからそのデータを取得しないことを意味します。

例えば、`items` 属性にアクセスするとします。

```Python
current_user.items
```

すると、SQLAlchemy は `items` テーブルにアクセスして、このユーザーのアイテムを取得します。しかし、それまでは取得しません。

`orm_mode` を使用しないと、_パス操作_ から SQLAlchemy モデルを返しても、関係を持つデータは含まれません。

Pydantic モデルでそれらの関係を宣言していても、含まれません。

しかし、ORM モードを使用すると、Pydantic 自体が (`dict` を想定するのではなく) 属性から必要なデータにアクセスしようとするため、返したい特定のデータを宣言することができ、ORM からであっても、そのデータを取得することができます。

## CRUD ユーティリティ

では、`sql_app/crud.py` ファイルを見てみましょう。

このファイルには、データベース内のデータを操作するための再利用可能な関数を記述します。

**CRUD** は、**C**reate (作成)、**R**ead (読み取り)、**U**pdate (更新)、**D**elete (削除) の頭文字をとったものです。

...ただし、この例では、作成と読み取りのみを行っています。

### データの読み込み

`sqlalchemy.orm` から `Session` をインポートします。これにより、`db` パラメータの型を宣言し、関数内でより適切な型チェックと補完を行うことができるようになります。

`models` (SQLAlchemy モデル) と `schemas` (Pydantic _モデル_ / スキーマ) をインポートします。

以下の機能を提供するユーティリティ関数を作成します。

- ID とメールアドレスで 1 人のユーザーを読み取る。
- 複数のユーザーを読み取る。
- 複数のアイテムを読み取る。

```Python hl_lines="1  3  6-7  10-11  14-15  27-28"
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

!!! tip "豆知識"
_パス操作関数_ から独立して、データベースとの対話 (ユーザーやアイテムの取得) のみを担当する関数を作成することで、複数の場所でより簡単に再利用できるようになり、また、<abbr title="コードで記述された自動化されたテストであり、別のコードが正しく動作するかどうかを確認します。">単体テスト</abbr> を追加しやすくなります。

### データの作成

ユーティリティ関数を書いてデータを作成する手順は以下の通りです。

- データを使用して SQLAlchemy モデルの*インスタンス*を作成します。
- インスタンスオブジェクトをデータベースセッションに`追加`します。
- データベースへの変更を`コミット`します（これにより、変更が保存されます）。
- インスタンスを`更新`します（これにより、インスタンスにデータベースからの新しいデータ（生成された ID など）が含まれます）。

```Python hl_lines="18-24  31-36"
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

!!! info "情報"
Pydantic v1 では、このメソッドは`.dict()`と呼ばれていました。Pydantic v2 では非推奨になりました（ただし、引き続きサポートされています）が、`.model_dump()`に名前が変更されました。

これらの例では、Pydantic v1 との互換性のために`.dict()`を使用していますが、Pydantic v2 を使用できる場合は、代わりに`.model_dump()`を使用する必要があります。

!!! tip "豆知識"
`User`の SQLAlchemy モデルには、パスワードの安全なハッシュバージョンを含む`hashed_password`が含まれています。

しかし、API クライアントが提供するのは元のパスワードなので、アプリケーションでそれを抽出してハッシュパスワードを生成する必要があります。

次に、値を含む`hashed_password`引数を渡して保存します。

!!! warning "注意"
この例は安全ではありません。パスワードはハッシュ化されていません。

実際のアプリケーションでは、パスワードをハッシュ化し、プレーンテキストで保存しないようにする必要があります。

詳細については、チュートリアルのセキュリティセクションに戻ってください。

ここでは、データベースのツールとメカニズムのみに焦点を当てています。

!!! tip "豆知識"
Item にキーワード引数を 1 つずつ渡して、各引数を Pydantic *モデル*から読み取るのではなく、Pydantic *モデル*のデータを dict に生成して、以下のようにしています。

    `item.dict()`

    そして以下のように、dictのキーと値のペアを、SQLAlchemyのItemにキーワード引数として渡しています。

    `Item(**item.dict())`

    そして、Pydantic *モデル*によって提供されない追加のキーワード引数`owner_id`を渡します。以下のようにです:

    `Item(**item.dict(), owner_id=user_id)`

## メインの **FastAPI** アプリ

そして、`sql_app/main.py`ファイルで、これまでに作成した他のすべての部分を統合して使用してみましょう。

### データベーステーブルの作成

非常に単純な方法で、データベーステーブルを作成します。

=== "Python 3.9+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

#### Alembic メモ

通常、データベースを初期化する場合（テーブルの作成など）、<a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a>を使用します。

また、Alembic は「マイグレーション」にも使用します（これは Alembic の主な仕事です）。

「マイグレーション」とは、SQLAlchemy モデルの構造を変更したり、新しい属性を追加したりなどした場合に、データベースにそれらの変更を複製したり、新しい列や新しいテーブルを追加したりするために必要な手順のセットです。

FastAPI プロジェクトで Alembic の例を見つけるには、[プロジェクト生成 - テンプレート](../project-generation.md){.internal-link target=\_blank}のテンプレートを使用します。具体的には、<a href="https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/src/backend/app/alembic" class="external-link" target="_blank">ソースコードの`alembic`ディレクトリ</a>をご覧ください。

### 依存関係を作成します

これで、`sql_app/database.py`ファイルで作成した`SessionLocal`クラスを使用して、依存関係を作成します。

各リクエストに対して独立したデータベースセッション/接続(`SessionLocal`)が必要であり、そのセッションをリクエスト全体で使用し、リクエストが完了したらクローズする必要があります。

そして、次のリクエストのために新しいセッションが作成されます。

そのため、[依存関係`yield`](dependencies/dependencies-with-yield.md){.internal-link target=\_blank}に関するセクションで説明したように、`yield`を使用した新しい依存関係を作成します。

私たちの依存関係は、単一のリクエストで使用され、リクエストが終了したらクローズされる新しい SQLAlchemy の`SessionLocal`を作成します。

=== "Python 3.9+"

    ```Python hl_lines="13-18"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="15-20"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

!!! info "情報"
`SessionLocal()`の作成とリクエストの処理を`try`ブロックに入れます。

そして、`finally`ブロックでクローズします。

これにより、リクエスト後にデータベースセッションが常にクローズされるようにします。リクエストの処理中に例外が発生した場合でもです。

    しかし、終了コード（`yield`の後）から別の例外を発生させることはできません。 [依存関係`yield`と`HTTPException`](dependencies/dependencies-with-yield.md#dependencies-with-yield-and-httpexception){.internal-link target=_blank}で詳しく説明されています。

そして、*パスオペレーション関数*で依存関係を使用する場合は、SQLAlchemy から直接インポートした`Session`型で宣言します。

これにより、*パスオペレーション関数*内でより良いエディターサポートが得られます。なぜなら、エディターは`db`パラメーターが`Session`型であることを認識しているからです。

=== "Python 3.9+"

    ```Python hl_lines="22  30  36  45  51"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="24  32  38  47  53"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

!!! info "技術的な詳細"
パラメーター`db`は実際には`SessionLocal`型ですが、このクラス（`sessionmaker()`で作成された）は SQLAlchemy の`Session`の「プロキシ」なので、エディターは実際にはどのメソッドが提供されているかを知りません。

しかし、`Session`として型を宣言することにより、エディターは使用可能なメソッド（`.add()`、`.query()`、`.commit()`など）を認識し、より良いサポート（補完など）を提供できます。型の宣言は、実際のオブジェクトには影響しません。

### **FastAPI**の*パスオペレーション*を作成します

最後に、標準的な**FastAPI**の*パスオペレーション*コードを以下に示します。

=== "Python 3.9+"

    ```Python hl_lines="21-26  29-32  35-40  43-47  50-53"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="23-28  31-34  37-42  45-49  52-55"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

依存関係で`yield`を使用して、各リクエストの前にデータベースセッションを作成し、後でクローズしています。

そして、そのセッションを直接取得するために、*パスオペレーション関数*で必要な依存関係を作成できます。

これにより、*パスオペレーション関数*内から直接`crud.get_user`を呼び出して、そのセッションを使用できます。

!!! tip "豆知識"
返される値は、SQLAlchemy モデルまたは SQLAlchemy モデルのリストであることに注意してください。

しかし、すべての*パスオペレーション*は、`orm_mode`を使用する Pydantic _モデル_ / スキーマで`response_model`を持ち、Pydantic モデルに宣言されたデータがそれらから抽出されてクライアントに返されます。通常のフィルタリングと検証がすべて行われます

!!! tip "豆知識"
また、`List[schemas.Item]`のような標準的な Python 型を持つ`response_models`があることに注意してください。

しかし、その`List`の内容/パラメーターは、`orm_mode`を持つ Pydantic *モデル*なので、データは通常どおり取得されてクライアントに返され、問題はありません。

### `def` vs `async def`について

ここでは、*パスオペレーション関数*と依存関係の中で SQLAlchemy コードを使用しており、それが外部データベースとの通信を行うことになります。

これにより、潜在的に「待機」が必要になる可能性があります。

しかし、SQLAlchemy は、次のようなもので使用される`await`を直接使用するための互換性はありません。

```Python
user = await db.query(User).first()
```

...そして、代わりに以下のものを使用しています。

```Python
user = db.query(User).first()
```

Then we should declare the _path operation functions_ and the dependency without `async def`, just with a normal `def`, as:

```Python hl_lines="2"
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    ...
```

!!! info "情報"
リレーショナルデータベースに非同期的に接続する必要がある場合は、[非同期 SQL（リレーショナル）データベース](../how-to/async-sql-encode-databases.md){.internal-link target=\_blank}を参照してください。

!!! note "非常に技術的な詳細"
興味があり、深い技術知識をお持ちの場合は、この`async def` vs `def`がどのように処理されるかについて、[非同期](../async.md#very-technical-details){.internal-link target=\_blank}ドキュメントの非常に技術的な詳細を確認できます。

## マイグレーション

SQLAlchemy を直接使用しており、**FastAPI**との連携のためにプラグインは必要ないため、<a href="https://alembic.sqlalchemy.org" class="external-link" target="_blank">Alembic</a>を使用してデータベースの<abbr title="モデルに定義した新しい列をすべてデータベースに自動的に更新します。">マイグレーション</abbr>を直接統合できます。

また、SQLAlchemy と SQLAlchemy モデルに関連するコードは、独立した別々のファイルに存在するため、FastAPI、Pydantic、またはその他のものをインストールすることなく、Alembic でマイグレーションを実行することもできます。

同じように、**FastAPI**に関係しないコードの他の部分で、同じ SQLAlchemy モデルとユーティリティを使用できます。

たとえば、<a href="https://docs.celeryq.dev" class="external-link" target="_blank">Celery</a>、<a href="https://python-rq.org/" class="external-link" target="_blank">RQ</a>、または<a href="https://arq-docs.helpmanual.io/" class="external-link" target="_blank">ARQ</a>を使用したバックグラウンドタスクワーカーの場合です

## すべてのファイルの振り返り

`my_super_project`という名前のディレクトリがあり、その中に`sql_app`という名前のサブディレクトリがあることを覚えておいてください。

`sql_app` は以下のファイルを持っているべきです。

- `sql_app/__init__.py`:　空のファイル.

- `sql_app/database.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

- `sql_app/models.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

- `sql_app/schemas.py`:

=== "Python 3.10+"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app_py310/schemas.py!}
    ```

=== "Python 3.9+"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app_py39/schemas.py!}
    ```

=== "Python 3.8+"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app/schemas.py!}
    ```

- `sql_app/crud.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

- `sql_app/main.py`:

=== "Python 3.9+"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

=== "Python 3.8+"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

## 確認してください

このコードをコピーしてそのまま使用できます。

!!! info "情報"

実際、ここで示されているコードはテストの一部です。このドキュメントのほとんどのコードと同じです。

次に、Uvicorn で実行できます。

<div class="termy">

```console
$ uvicorn sql_app.main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

そしてブラウザでこのリンクを開いてください。 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

そして、実際のデータベースからデータを読み込みながら、**FastAPI**アプリケーションとやり取りできるようになります。

<img src="/img/tutorial/sql-databases/image01.png">

## Interact with the database directly

FastAPI とは別に、SQLite データベース（ファイル）を直接操作して、その内容をデバッグしたり、テーブル、列、レコードを追加したり、データを変更したりする場合は、<a href="https://sqlitebrowser.org/" class="external-link" target="_blank">DB Browser for SQLite</a>を使用できます。

以下のような表示になります。

<img src="/img/tutorial/sql-databases/image02.png">

<a href="https://inloop.github.io/sqlite-viewer/" class="external-link" target="_blank">SQLite Viewer</a>や<a href="https://extendsclass.com/sqlite-browser.html" class="external-link" target="_blank">ExtendsClass</a>のようなオンラインの SQLite ブラウザを使用することもできます。

## ミドルウェアを使用した代替 DB セッション

`yield`を使用した依存関係を使用できない場合（たとえば、**Python 3.7**を使用しておらず、**Python 3.6**のバックポートをインストールできない場合）、同様の方法で「ミドルウェア」でセッションを設定できます。

「ミドルウェア」は基本的に、各リクエストに対して常に実行される関数であり、エンドポイント関数の実行前と実行後にいくつかのコードが実行されます。

### Create a middleware

追加するミドルウェア（単なる関数）は、各リクエストに対して新しい SQLAlchemy の`SessionLocal`を作成し、リクエストに追加して、リクエストが完了したらクローズします。

=== "Python 3.9+"

    ```Python hl_lines="12-20"
    {!> ../../../docs_src/sql_databases/sql_app_py39/alt_main.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="14-22"
    {!> ../../../docs_src/sql_databases/sql_app/alt_main.py!}
    ```

!!! info "情報"
`SessionLocal()`の作成とリクエストの処理を`try`ブロックに入れます。

そして、`finally`ブロックでクローズします。

これにより、リクエスト後にデータベースセッションが常にクローズされるようにします。リクエストの処理中に例外が発生した場合でもです。

### `request.state`について

`request.state`は各`Request`オブジェクトのプロパティです。ここでは、この場合のデータベースセッションのように、リクエスト自体に添付された任意のオブジェクトを格納するために使用されます。 <a href="https://www.starlette.io/requests/#other-state" class="external-link" target="_blank">Starlette の`Request`状態に関するドキュメント</a>で詳細を確認できます。

この場合、これはリクエスト全体で単一のデータベースセッションが使用され、後で（ミドルウェアで）クローズされることを保証するのに役立ちます。

### `yield`を使用した依存関係またはミドルウェア

ここで**ミドルウェア**を追加することは、`yield`を使用した依存関係が実行することと似ていますが、以下に示すようないくつかの違いがあります。

- より多くのコードが必要で、少し複雑です。
- ミドルウェアは`async`関数である必要があります。
  - ネットワークを「待つ」必要があるコードが含まれている場合、そこでアプリケーションが「ブロック」され、パフォーマンスが少し低下する可能性があります。
  - `SQLAlchemy`の動作方法では、おそらくそれほど問題ではありません。
  - しかし、ミドルウェアに多くの<abbr title="入出力">I/O</abbr>待機を含むコードを追加した場合、問題になる可能性があります。
- ミドルウェアは*すべての*リクエストに対して実行されます。
  - つまり、すべてのリクエストに対して接続が作成されます。
  - そのリクエストを処理する*パスオペレーション*が DB を必要としなかった場合でもです。

!!! tip 　"豆知識"
ユースケースで十分な場合は、`yield`を使用した依存関係を使用する方がおそらく良いでしょう。

!!! info "情報"
`yield`を使用した依存関係は、最近**FastAPI**に追加されました。

このチュートリアルの以前のバージョンでは、ミドルウェアを使用した例のみが示されており、ミドルウェアを使用してデータベースセッションを管理しているアプリケーションがいくつか存在する可能性があります。
