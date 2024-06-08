# SQL (Relational) Databases

!!! info"情報"
    これらの情報は間もなく更新されます。 🎉

    現在のバージョンは Pydantic v1、SQLAlchemy のバージョンは 2.0 未満を想定しています。

    新しいドキュメントには Pydantic v2 が含まれ、<a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a> (これも SQLAlchemy をベースにしています) が Pydantic v2 を使用するように更新され次第、SQLModel も使用される予定です。 

**FastAPI** はあなたにSQL(relational)を使用することを要求しません。

But you can use any relational database that you want.
しかし、あなたが望むどのSQL(relational)も利用することができます。

ここに <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a>を利用した例があります。

あなたは簡単に以下にあるようなSQLAlchemyによってサポートされたどのデータベースも利用することが可能可能です。

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server, etc.

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

ORM には、コード内の *オブジェクト* とデータベースのテーブル（*リレーション*）間で変換（「*マッピング*」）を行うためのツールがあります。 

ORM を使用すると、通常は SQL データベース内のテーブルを表すクラスを作成します。クラスの各属性は列を表し、名前と型を持ちます。

例えば、`Pet` というクラスは、`pets` という SQL テーブルを表すことができます。 

そして、そのクラスの *インスタンス* オブジェクトはそれぞれ、データベース内の行を表します。 

例えば、`orion_cat` というオブジェクト (`Pet` のインスタンス) は、`type` という列に対応する `orion_cat.type` という属性を持つことができます。そして、その属性の値は、例えば `"cat"` となります。 

これらの ORM には、テーブルやエンティティ間の接続や関係を作成するためのツールも用意されています。 

このように、orion_cat.owner という属性を持つこともできます。そして、owner には、owners テーブルから取得された、このペットの飼い主のデータが含まれます。

つまり、orion_cat.owner.name は、このペットの飼い主の名前 (owners テーブルの name 列から取得) になります。

例えば "Arquilian" という値を持つことができます。

そして、ORM は、ペットオブジェクトからアクセスしようとしたときに、対応するテーブル *owners* から情報を取得するためのすべての処理を行います。 

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
    SQLAlchemy の *モデル* と Pydantic の *モデル* の混 confusion を避けるために、SQLAlchemy モデルを格納するファイル `models.py` と、Pydantic モデルを格納するファイル `schemas.py` を作成します。 

    これらの Pydantic モデルは、多かれ少なかれ「スキーマ」（有効なデータの形状）を定義します。 

    これにより、両方を使い分けるときに混乱を避けることができます。 

### 初期の Pydantic *モデル* / スキーマを作成する 

データの作成や読み取り時に共通の属性を持つように、`ItemBase` と `UserBase` の Pydantic *モデル* (あるいは「スキーマ」と呼ぶことにしましょう) を作成します。 

そして、それらを継承する `ItemCreate` と `UserCreate` を作成します（これにより、同じ属性を持ちます）。さらに、作成に必要な追加のデータ（属性）を追加します。 

したがって、ユーザーを作成するときは、`password` も持ちます。 

ただし、セキュリティ上の理由から、`password` は他の Pydantic *モデル* には含まれません。例えば、API からユーザーを読み取るときに、`password` は送信されません。 


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

SQLAlchemy *モデル* は、`=` を使用して属性を定義し、`Column` にパラメータとして型を渡すことに注意してください

```Python
name = Column(String)
```

一方、Pydantic *モデル* は、新しい型注釈構文/型ヒントを使用して、`:` で型を宣言します。 

```Python
name: str
```
これらを覚えておいてください。そうすれば、= と : を使用するときに混乱することがなくなります。

###　読み取り/返却用の Pydantic モデル / スキーマを作成する

次に、データを読み取るとき、つまり API からデータを返すときに使用される Pydantic *モデル* (スキーマ) を作成します。 

例えば、アイテムを作成する前は、それに割り当てられる ID はわかりませんが、アイテムを読み取るとき (API から返すとき) は、すでにその ID がわかっています。 

同様に、ユーザーを読み取るときに、`items` にはこのユーザーに属するアイテムが含まれることを宣言できます。 

これらのアイテムの ID だけでなく、アイテムを読み取るための Pydantic *モデル* (`Item`) で定義したすべてのデータも含まれます。 

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
    ユーザーを読み取るとき (API から返すとき) に使用される Pydantic *モデル* である `User` には、`password` が含まれていないことに注意してください。 

### Pydantic の `orm_mode` を使用する 

次に、読み取り用の Pydantic *モデル* である `Item` と `User` に、内部の `Config` クラスを追加します。 

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
このようにして、Pydantic *モデル* は ORM と互換性を持つようになり、*パス操作* の `response_model` 引数で宣言するだけで済みます。 

データベースモデルを返すことができ、そこからデータを読み取ることができます。 

#### ORM モードに関する技術的な詳細

SQLAlchemy をはじめとする多くの ORM は、デフォルトで「遅延読み込み」になっています。 

これは、例えば、関係を持つデータを含む属性にアクセスしようとしない限り、データベースからそのデータを取得しないことを意味します。 

例えば、`items` 属性にアクセスするとします。 

```Python
current_user.items
```

すると、SQLAlchemy は `items` テーブルにアクセスして、このユーザーのアイテムを取得します。しかし、それまでは取得しません。 

`orm_mode` を使用しないと、*パス操作* から SQLAlchemy モデルを返しても、関係を持つデータは含まれません。 

Pydantic モデルでそれらの関係を宣言していても、含まれません。 

しかし、ORM モードを使用すると、Pydantic 自体が (`dict` を想定するのではなく) 属性から必要なデータにアクセスしようとするため、返したい特定のデータを宣言することができ、ORM からであっても、そのデータを取得することができます。 

## CRUD ユーティリティ

では、`sql_app/crud.py` ファイルを見てみましょう。 

このファイルには、データベース内のデータを操作するための再利用可能な関数を記述します。 

**CRUD** は、**C**reate (作成)、**R**ead (読み取り)、**U**pdate (更新)、**D**elete (削除) の頭文字をとったものです。 

...ただし、この例では、作成と読み取りのみを行っています。 


### データの読み込み

`sqlalchemy.orm` から `Session` をインポートします。これにより、`db` パラメータの型を宣言し、関数内でより適切な型チェックと補完を行うことができるようになります。 

`models` (SQLAlchemy モデル) と `schemas` (Pydantic *モデル* / スキーマ) をインポートします。 

以下の機能を提供するユーティリティ関数を作成します。 

* ID とメールアドレスで 1 人のユーザーを読み取る。 
* 複数のユーザーを読み取る。 
* 複数のアイテムを読み取る。 

```Python hl_lines="1  3  6-7  10-11  14-15  27-28"
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

!!! tip "豆知識"
    *パス操作関数* から独立して、データベースとの対話 (ユーザーやアイテムの取得) のみを担当する関数を作成することで、複数の場所でより簡単に再利用できるようになり、また、<abbr title="コードで記述された自動化されたテストであり、別のコードが正しく動作するかどうかを確認します。">単体テスト</abbr> を追加しやすくなります。 



### Create data

Now create utility functions to create data.

The steps are:

* Create a SQLAlchemy model *instance* with your data.
* `add` that instance object to your database session.
* `commit` the changes to the database (so that they are saved).
* `refresh` your instance (so that it contains any new data from the database, like the generated ID).

```Python hl_lines="18-24  31-36"
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

!!! info
    In Pydantic v1 the method was called `.dict()`, it was deprecated (but still supported) in Pydantic v2, and renamed to `.model_dump()`.

    The examples here use `.dict()` for compatibility with Pydantic v1, but you should use `.model_dump()` instead if you can use Pydantic v2.

!!! tip
    The SQLAlchemy model for `User` contains a `hashed_password` that should contain a secure hashed version of the password.

    But as what the API client provides is the original password, you need to extract it and generate the hashed password in your application.

    And then pass the `hashed_password` argument with the value to save.

!!! warning
    This example is not secure, the password is not hashed.

    In a real life application you would need to hash the password and never save them in plaintext.

    For more details, go back to the Security section in the tutorial.

    Here we are focusing only on the tools and mechanics of databases.

!!! tip
    Instead of passing each of the keyword arguments to `Item` and reading each one of them from the Pydantic *model*, we are generating a `dict` with the Pydantic *model*'s data with:

    `item.dict()`

    and then we are passing the `dict`'s key-value pairs as the keyword arguments to the SQLAlchemy `Item`, with:

    `Item(**item.dict())`

    And then we pass the extra keyword argument `owner_id` that is not provided by the Pydantic *model*, with:

    `Item(**item.dict(), owner_id=user_id)`

## Main **FastAPI** app

And now in the file `sql_app/main.py` let's integrate and use all the other parts we created before.

### Create the database tables

In a very simplistic way create the database tables:

=== "Python 3.9+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

#### Alembic Note

Normally you would probably initialize your database (create tables, etc) with <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a>.

And you would also use Alembic for "migrations" (that's its main job).

A "migration" is the set of steps needed whenever you change the structure of your SQLAlchemy models, add a new attribute, etc. to replicate those changes in the database, add a new column, a new table, etc.

You can find an example of Alembic in a FastAPI project in the templates from [Project Generation - Template](../project-generation.md){.internal-link target=_blank}. Specifically in <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/src/backend/app/alembic" class="external-link" target="_blank">the `alembic` directory in the source code</a>.

### Create a dependency

Now use the `SessionLocal` class we created in the `sql_app/database.py` file to create a dependency.

We need to have an independent database session/connection (`SessionLocal`) per request, use the same session through all the request and then close it after the request is finished.

And then a new session will be created for the next request.

For that, we will create a new dependency with `yield`, as explained before in the section about [Dependencies with `yield`](dependencies/dependencies-with-yield.md){.internal-link target=_blank}.

Our dependency will create a new SQLAlchemy `SessionLocal` that will be used in a single request, and then close it once the request is finished.

=== "Python 3.9+"

    ```Python hl_lines="13-18"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="15-20"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

!!! info
    We put the creation of the `SessionLocal()` and handling of the requests in a `try` block.

    And then we close it in the `finally` block.

    This way we make sure the database session is always closed after the request. Even if there was an exception while processing the request.

    But you can't raise another exception from the exit code (after `yield`). See more in [Dependencies with `yield` and `HTTPException`](dependencies/dependencies-with-yield.md#dependencies-with-yield-and-httpexception){.internal-link target=_blank}

And then, when using the dependency in a *path operation function*, we declare it with the type `Session` we imported directly from SQLAlchemy.

This will then give us better editor support inside the *path operation function*, because the editor will know that the `db` parameter is of type `Session`:

=== "Python 3.9+"

    ```Python hl_lines="22  30  36  45  51"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="24  32  38  47  53"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

!!! info "Technical Details"
    The parameter `db` is actually of type `SessionLocal`, but this class (created with `sessionmaker()`) is a "proxy" of a SQLAlchemy `Session`, so, the editor doesn't really know what methods are provided.

    But by declaring the type as `Session`, the editor now can know the available methods (`.add()`, `.query()`, `.commit()`, etc) and can provide better support (like completion). The type declaration doesn't affect the actual object.

### Create your **FastAPI** *path operations*

Now, finally, here's the standard **FastAPI** *path operations* code.

=== "Python 3.9+"

    ```Python hl_lines="21-26  29-32  35-40  43-47  50-53"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="23-28  31-34  37-42  45-49  52-55"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

We are creating the database session before each request in the dependency with `yield`, and then closing it afterwards.

And then we can create the required dependency in the *path operation function*, to get that session directly.

With that, we can just call `crud.get_user` directly from inside of the *path operation function* and use that session.

!!! tip
    Notice that the values you return are SQLAlchemy models, or lists of SQLAlchemy models.

    But as all the *path operations* have a `response_model` with Pydantic *models* / schemas using `orm_mode`, the data declared in your Pydantic models will be extracted from them and returned to the client, with all the normal filtering and validation.

!!! tip
    Also notice that there are `response_models` that have standard Python types like `List[schemas.Item]`.

    But as the content/parameter of that `List` is a Pydantic *model* with `orm_mode`, the data will be retrieved and returned to the client as normally, without problems.

### About `def` vs `async def`

Here we are using SQLAlchemy code inside of the *path operation function* and in the dependency, and, in turn, it will go and communicate with an external database.

That could potentially require some "waiting".

But as SQLAlchemy doesn't have compatibility for using `await` directly, as would be with something like:

```Python
user = await db.query(User).first()
```

...and instead we are using:

```Python
user = db.query(User).first()
```

Then we should declare the *path operation functions* and the dependency without `async def`, just with a normal `def`, as:

```Python hl_lines="2"
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    ...
```

!!! info
    If you need to connect to your relational database asynchronously, see [Async SQL (Relational) Databases](../how-to/async-sql-encode-databases.md){.internal-link target=_blank}.

!!! note "Very Technical Details"
    If you are curious and have a deep technical knowledge, you can check the very technical details of how this `async def` vs `def` is handled in the [Async](../async.md#very-technical-details){.internal-link target=_blank} docs.

## Migrations

Because we are using SQLAlchemy directly and we don't require any kind of plug-in for it to work with **FastAPI**, we could integrate database <abbr title="Automatically updating the database to have any new column we define in our models.">migrations</abbr> with <a href="https://alembic.sqlalchemy.org" class="external-link" target="_blank">Alembic</a> directly.

And as the code related to SQLAlchemy and the SQLAlchemy models lives in separate independent files, you would even be able to perform the migrations with Alembic without having to install FastAPI, Pydantic, or anything else.

The same way, you would be able to use the same SQLAlchemy models and utilities in other parts of your code that are not related to **FastAPI**.

For example, in a background task worker with <a href="https://docs.celeryq.dev" class="external-link" target="_blank">Celery</a>, <a href="https://python-rq.org/" class="external-link" target="_blank">RQ</a>, or <a href="https://arq-docs.helpmanual.io/" class="external-link" target="_blank">ARQ</a>.

## Review all the files

 Remember you should have a directory named `my_super_project` that contains a sub-directory called `sql_app`.

`sql_app` should have the following files:

* `sql_app/__init__.py`: is an empty file.

* `sql_app/database.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

* `sql_app/models.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

* `sql_app/schemas.py`:

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

* `sql_app/crud.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

* `sql_app/main.py`:

=== "Python 3.9+"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

=== "Python 3.8+"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

## Check it

You can copy this code and use it as is.

!!! info

    In fact, the code shown here is part of the tests. As most of the code in these docs.

Then you can run it with Uvicorn:


<div class="termy">

```console
$ uvicorn sql_app.main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

And then, you can open your browser at <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

And you will be able to interact with your **FastAPI** application, reading data from a real database:

<img src="/img/tutorial/sql-databases/image01.png">

## Interact with the database directly

If you want to explore the SQLite database (file) directly, independently of FastAPI, to debug its contents, add tables, columns, records, modify data, etc. you can use <a href="https://sqlitebrowser.org/" class="external-link" target="_blank">DB Browser for SQLite</a>.

It will look like this:

<img src="/img/tutorial/sql-databases/image02.png">

You can also use an online SQLite browser like <a href="https://inloop.github.io/sqlite-viewer/" class="external-link" target="_blank">SQLite Viewer</a> or <a href="https://extendsclass.com/sqlite-browser.html" class="external-link" target="_blank">ExtendsClass</a>.

## Alternative DB session with middleware

If you can't use dependencies with `yield` -- for example, if you are not using **Python 3.7** and can't install the "backports" mentioned above for **Python 3.6** -- you can set up the session in a "middleware" in a similar way.

A "middleware" is basically a function that is always executed for each request, with some code executed before, and some code executed after the endpoint function.

### Create a middleware

The middleware we'll add (just a function) will create a new SQLAlchemy `SessionLocal` for each request, add it to the request and then close it once the request is finished.

=== "Python 3.9+"

    ```Python hl_lines="12-20"
    {!> ../../../docs_src/sql_databases/sql_app_py39/alt_main.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="14-22"
    {!> ../../../docs_src/sql_databases/sql_app/alt_main.py!}
    ```

!!! info
    We put the creation of the `SessionLocal()` and handling of the requests in a `try` block.

    And then we close it in the `finally` block.

    This way we make sure the database session is always closed after the request. Even if there was an exception while processing the request.

### About `request.state`

`request.state` is a property of each `Request` object. It is there to store arbitrary objects attached to the request itself, like the database session in this case. You can read more about it in <a href="https://www.starlette.io/requests/#other-state" class="external-link" target="_blank">Starlette's docs about `Request` state</a>.

For us in this case, it helps us ensure a single database session is used through all the request, and then closed afterwards (in the middleware).

### Dependencies with `yield` or middleware

Adding a **middleware** here is similar to what a dependency with `yield` does, with some differences:

* It requires more code and is a bit more complex.
* The middleware has to be an `async` function.
    * If there is code in it that has to "wait" for the network, it could "block" your application there and degrade performance a bit.
    * Although it's probably not very problematic here with the way `SQLAlchemy` works.
    * But if you added more code to the middleware that had a lot of <abbr title="input and output">I/O</abbr> waiting, it could then be problematic.
* A middleware is run for *every* request.
    * So, a connection will be created for every request.
    * Even when the *path operation* that handles that request didn't need the DB.

!!! tip
    It's probably better to use dependencies with `yield` when they are enough for the use case.

!!! info
    Dependencies with `yield` were added recently to **FastAPI**.

    A previous version of this tutorial only had the examples with a middleware and there are probably several applications using the middleware for database session management.
