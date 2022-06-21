# SQL (リレーショナル) データベース

**FastAPI** では、SQL（リレーショナル）データベースを使用する必要はありません。

しかし、使いたいリレーショナルデータベースを使用することができます。

ここでは、 <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a>を使った例を見てみましょう。

以下のような、SQLAlchemyがサポートするどのようなデータベースにも簡単に適応できます:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server, 等

この例では **SQLite** を使用します。なぜなら、SQLiteは単一のファイルを使用し、Pythonが完全にサポートしているからです。そのため、この例をコピーして、そのまま実行することができます。

その後、本番のアプリケーションでは **PostgreSQL** のようなデータベースサーバーを使用したいと思うかもしれません。

!!! 豆知識
    **FastAPI** と **PostgreSQL** を使った公式のプロジェクトジェネレータがあります。これはフロントエンドやその他のツールを含んでおり、全て **Docker** を基にしています。 <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

!!! 備考
    コードのほとんどは、どのフレームワークでも使うような標準的な `SQLAlchemy` のコードであることに注意してください。

    **FastAPI** 固有のコードは、いつもと同じように小さいです。

## ORMs

**FastAPI** は、どんなデータベースでも、どんなスタイルのライブラリでも、データベースと対話することができます。

一般的なパターンは 「ORM」 ("object-relational mapping") ライブラリを使用することです。

ORMは、コード内の *objects* とデータベースのテーブル ("*relations*") を変換 ("*map*") するツールを持っています。

ORMでは、通常はSQLデータベースのテーブルを表すクラスを作成し、クラスの各属性は名前と型を持つカラムを表します。

例えば、 `Pet` クラスはSQLテーブルの `pets` を表現します。

そして、そのクラスの各 *インスタンス* オブジェクトは、データベースの行を表します。

例えば、 `orion_cat` (`Pet` のインスタンス) オブジェクトが `orion_cat.type` という属性を持つなら、そのカラムは `type` であると考えられる。そしてその属性の値は、例えば `"cat"` とすることができる。

これらのORMは、テーブルやエンティティ間の接続やリレーションを作成するツールも備えている。

この方法では、 `orion_cat.owner` という属性も持つことができ、ownerには *owners* テーブルから取得した、このペットの飼い主のデータが格納されます。

つまり、 `orion_cat.owner.name` には、このペットの飼い主の名前 (`owners` テーブルの `name` カラム) を指定することができます。

`"Arquilian"` のような値を持つことができます。

そして、ペットオブジェクトからアクセスしようとすると、対応する *owners* テーブルから情報を取得するために、ORMがすべての作業を行います。

一般的な ORM は、例えば Django-ORM (Django フレームワークの一部), SQLAlchemy ORM (SQLAlchemy の一部、フレームワークとは独立), Peewee (フレームワークとは独立) などです。

ここでは、**SQLAlchemy ORM** を使って、どのように動作するかを見ていきます。

同様の方法で、他のORMを使用することもできます。

!!! 豆知識
    このドキュメントにPeeweeを使った同等の記事があります。

## ファイル構成

これらの例では、`my_super_project` というディレクトリがあり、その中に `sql_app` というサブディレクトリがあり、次のような構造になっているとします:

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

ファイル `__init__.py` はただの空ファイルですが、このファイルは `sql_app` とそのモジュール (Python ファイル) がパッケージであることを Python に知らせます。

では、それぞれのファイル/モジュールが何をするのか見てみましょう。

## SQLAlchemyのパーツを作成する

ファイル `sql_app/database.py` を参照してみましょう。

### SQLAlchemyのパーツをインポートする

```Python hl_lines="1-3"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

### SQLAlchemy用のデータベースURLを作成する

```Python hl_lines="5-6"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

この例では、SQLiteデータベースへの「接続」（SQLiteデータベースでファイルを開くこと）を行っています。

このファイルは同じディレクトリにある `sql_app.db` というファイルに格納されます。

そのため、最後の部分が `./sql_app.db` になっています。

もし、代わりに **PostgreSQL** データベースを使用している場合は、この行をアンコメントする必要があります:

```Python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
```

...そして、あなたのデータベースデータと認証情報（MySQL、MariaDB、その他に相当するもの）を適応させます。

!!! 豆知識

    これは、別のデータベースを使用する場合に修正する必要がある主要な行です。

### SQLAlchemy `エンジン` の作成

最初のステップは、SQLAlchemy の「エンジン」を作ることです。

この `engine` は後で他の場所でも使用することになります。

```Python hl_lines="8-10"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

#### 備考

引数:

```Python
connect_args={"check_same_thread": False}
```

...は `SQLite` でのみ必要です。他のデータベースでは必要ありません。

!!! 情報 「技術的詳細」

    デフォルトでは、SQLite は、各スレッドが独立したリクエストを処理すると仮定して、1つのスレッドのみとの通信を許可します。

    これは、誤って同じ接続を異なるもの（異なる要求）のために共有することを防ぐためです。

    しかし FastAPI では、通常の関数 (`def`) を使うと、同じリクエストに対して複数のスレッドがデータベースとやり取りする可能性があります。そこで、SQLite にそれを許可するように、 `connect_args={"check_same_thread": False}` とします。

    また、各リクエストは依存関係でそれ自身のデータベース接続セッションを取得するようにしますので、そのようなデフォルトのメカニズムは必要ありません。

### `SessionLocal` クラスの作成

SessionLocal` クラスの各インスタンスがデータベースセッションになります。このクラス自身は、まだデータベースセッションではありません。

しかし、一旦 `SessionLocal` クラスのインスタンスを作成すると、このインスタンスが実際のデータベースセッションとなります。

我々はSQLAlchemy からインポートする `Session` と区別するために、 `SessionLocal` と名付けました。

後で `Session` (SQLAlchemyからインポートしたもの) を使うことになります。

`SessionLocal` クラスを作成するには、 `sessionmaker` 関数を使用します。

```Python hl_lines="11"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

### `Base` クラスの作成

では、クラスを返す関数 `declarative_base()` を使ってみましょう。

後で、このクラスを継承して、各データベースモデルやクラス（ORMモデル）を作成します:

```Python hl_lines="13"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

## データベースモデルの作成

それでは、`sql_app/models.py` を見てみましょう。

### `Base` クラスからSQLAlchemyのモデルを作成する

先程作った `Base` クラスを使って、SQLAlchemy のモデルを作成します。

!!! 豆知識
    SQLAlchemy では、データベースとやりとりするこれらのクラスやインスタンスを 「**モデル**」 という用語で呼んでいます。

    しかし、Pydanticは「**モデル**」という言葉を、データの検証、変換、文書化のクラスとインスタンスという異なるものを指すのにも使っています。

`database` (上記の `database.py` ファイル) から `Base` をインポートします。

それを継承したクラスを作成します。

これらのクラスがSQLAlchemyのモデルです。

```Python hl_lines="4  7-8  18-19"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

`__tablename__` 属性は、SQLAlchemyにそれぞれのモデルで使うデータベースのテーブルの名前を教えます。

### モデルの属性/カラムの作成

ここで、全てのモデル（クラス）属性を作成します。

これらの属性は、それぞれ対応するデータベーステーブルのカラムを表しています。

ここでは、SQLAlchemy の `Column` をデフォルト値として使用します。

そして、データベースで型を定義する、 `Integer`, `String`, `Boolean` という SQLAlchemy のクラス 「type」 を引数として渡します。

```Python hl_lines="1  10-13  21-24"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

### リレーションの作成

ここで、リレーションを作成します。

このために、SQLAlchemy ORM が提供する `relationship` を使います。

これは、多かれ少なかれ、このテーブルに関連する他のテーブルからの値を含む「魔法の」属性となります。

```Python hl_lines="2  15  26"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

`my_user.items` のように、`User` の `items` 属性にアクセスすると、`users` テーブルのこのレコードを指す外部キーを持つ、（`items` テーブルの） `Item` のSQLAlchemyモデルのリストが表示されます。

`my_user.items` にアクセスすると、SQLAlchemy は実際にデータベースから `items` テーブルにあるアイテムを取得し、ここに入力します。

そして、`Item` の `owner` 属性にアクセスすると、`users` テーブルの `User` のSQLAlchemy モデルが含まれます。これは、 `users` テーブルからどのレコードを取得するかを知るために、外部キーを持つ `owner_id` 属性/カラムを使用します。

## Pydanticモデルの作成

では、`sql_app/schemas.py`を確認してみましょう。

!!! 豆知識
    SQLAlchemyの *モデル* とPydanticの *モデル* の混同を避けるために、SQLAlchemyのモデルを `models.py` に、Pydantic のモデルを `schemas.py` に記述することにします。

    これらのPydanticモデルは、多かれ少なかれ「スキーマ」（有効なデータの形）を定義するものです。

    これにより、両者を使い分ける際の混乱を回避することができます。

### Pydanticの初期モデル/スキーマの作成

`ItemBase` と `UserBase` という Pydantic *モデル* (スキーマ) を作成して、データの作成時や読み込み時に共通の属性を持つようにします。

そして、それらを継承した `ItemCreate` と `UserCreate` を作成し（つまり、同じ属性を持つことになります）、さらに作成に必要な追加データ（属性）を作成します。

そのため、ユーザは作成時に `password` も持つことになります。

しかし、セキュリティのために、`password`は他のPydantic *モデル*には含まれません。例えば、ユーザーを読み取るときにAPIから送られることはありません。

=== "Python 3.6 and above"

    ```Python hl_lines="3  6-8  11-12  23-24  27-28"
    {!> ../../../docs_src/sql_databases/sql_app/schemas.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="3  6-8  11-12  23-24  27-28"
    {!> ../../../docs_src/sql_databases/sql_app_py39/schemas.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="1  4-6  9-10  21-22  25-26"
    {!> ../../../docs_src/sql_databases/sql_app_py310/schemas.py!}
    ```

#### SQLAlchemy式とPydantic式

SQLAlchemyの *モデル* は、 `=` を使って属性を定義し、次のように `Column` にパラメータとして型を渡していることに注意してください:

```Python
name = Column(String)
```

一方、Pydantic *モデル* は `:` という新しい型注釈シンタックス/型ヒントを用いて型を宣言します:

```Python
name: str
```

これを覚えておくと、`=` や `:` を一緒に使うときに混乱することがありません。

### Pydanticの *モデル* / スキーマ を作成し、 読み込み / 返却を行う

次に、データを読み込むとき、APIからデータを返すときに使用するPydantic *モデル*（スキーマ）を作成します。

例えば、アイテムを作る前には、そのアイテムに割り当てられたIDが何であるかはわかりませんが、それを読むとき（APIから返すとき）には、すでにそのIDが分かっていることになります。

同じように、ユーザーを読み込むときに、 `items` にはこのユーザーに属するアイテムが含まれると宣言できるようになりました。

それらアイテムのIDだけでなく、アイテムを読み取るためのPydantic *モデル* で定義したすべてのデータこそが `Item` です。

=== "Python 3.6 and above"

    ```Python hl_lines="15-17  31-34"
    {!> ../../../docs_src/sql_databases/sql_app/schemas.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="15-17  31-34"
    {!> ../../../docs_src/sql_databases/sql_app_py39/schemas.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="13-15  29-32"
    {!> ../../../docs_src/sql_databases/sql_app_py310/schemas.py!}
    ```

!!! 豆知識
    ユーザーを読み込む（APIから返す）ときに使用されるPydantic *モデル*である `User` には、 `password` が含まれていないことに注意してください。

### Pydanticの `orm_mode` を使用する

さて、Pydantic の読み込み用の *モデル*である `Item` と `User` に、内部クラスの `Config` クラスを追加してください。

この <a href="https://pydantic-docs.helpmanual.io/usage/model_config/" class="external-link" target="_blank">`Config`</a> はPydanticに設定を提供するために使用されます。

`Config` クラスで、`orm_mode = True` という属性を設定してください。

=== "Python 3.6 and above"

    ```Python hl_lines="15  19-20  31  36-37"
    {!> ../../../docs_src/sql_databases/sql_app/schemas.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="15  19-20  31  36-37"
    {!> ../../../docs_src/sql_databases/sql_app_py39/schemas.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="13  17-18  29  34-35"
    {!> ../../../docs_src/sql_databases/sql_app_py310/schemas.py!}
    ```

!!! 豆知識
    このように、`=`で値を代入していることに注目してください:

    `orm_mode = True`

    以前の型宣言のように `:` を使うことはありません。

    これは設定値の設定であり、型の宣言ではありません。

Pydantic の `orm_mode` は、たとえそれが `dict` ではなく ORM モデル (あるいは属性を持つその他の任意のオブジェクト) であっても、Pydantic の *モデル* にデータを読み込むように指示します。

このように、`dict`から`id`の値だけを取得しようとするのではなく:

```Python
id = data["id"]
```

このように、属性から取得しようとすることもあります。

```Python
id = data.id
```

そして、これによってPydanticの*モデル*はORMと互換性を持ち、*path operation* の中の `response_model` 引数で宣言すれば良いのです。

データベースモデルを返すと、そこからデータを読み込んでくれるようになります。

#### ORMモードに関する技術的詳細

SQLAlchemyやその他多くのものは、デフォルトで「遅延ロード」になっています。

つまり、例えば、そのデータを含む属性にアクセスしようとしない限り、データベースからリレーションシップのデータを取得することはできないということです。

例えば、属性 `items` にアクセスする場合:

```Python
current_user.items
```

この場合は、SQLAlchemy が `items` テーブルに移動して、このユーザのアイテムを取得するようにします。

orm_mode` がないと、*path operation* から SQLAlchemy のモデルを返した場合、リレーションシップのデータが含まれないことになります。

Pydanticモデルでそれらの関係を宣言したとしても。

しかしORMモードでは、Pydantic自身が（`dict`を想定するのではなく）属性から必要なデータにアクセスしようとするので、返したい特定のデータを宣言すれば、ORMからでもそれを取得しに行くことができるようになるのです。

## CRUD utils

Now let's see the file `sql_app/crud.py`.

In this file we will have reusable functions to interact with the data in the database.

**CRUD** comes from: **C**reate, **R**ead, **U**pdate, and **D**elete.

...although in this example we are only creating and reading.

### Read data

Import `Session` from `sqlalchemy.orm`, this will allow you to declare the type of the `db` parameters and have better type checks and completion in your functions.

Import `models` (the SQLAlchemy models) and `schemas` (the Pydantic *models* / schemas).

Create utility functions to:

* Read a single user by ID and by email.
* Read multiple users.
* Read multiple items.

```Python hl_lines="1  3  6-7  10-11  14-15  27-28"
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

!!! tip
    By creating functions that are only dedicated to interacting with the database (get a user or an item) independent of your *path operation function*, you can more easily reuse them in multiple parts and also add <abbr title="Automated tests, written in code, that check if another piece of code is working correctly.">unit tests</abbr> for them.

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

=== "Python 3.6 and above"

    ```Python hl_lines="9"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="7"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

#### Alembic Note

Normally you would probably initialize your database (create tables, etc) with <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a>.

And you would also use Alembic for "migrations" (that's its main job).

A "migration" is the set of steps needed whenever you change the structure of your SQLAlchemy models, add a new attribute, etc. to replicate those changes in the database, add a new column, a new table, etc.

You can find an example of Alembic in a FastAPI project in the templates from [Project Generation - Template](../project-generation.md){.internal-link target=_blank}. Specifically in <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/alembic/" class="external-link" target="_blank">the `alembic` directory in the source code</a>.

### Create a dependency

Now use the `SessionLocal` class we created in the `sql_app/database.py` file to create a dependency.

We need to have an independent database session/connection (`SessionLocal`) per request, use the same session through all the request and then close it after the request is finished.

And then a new session will be created for the next request.

For that, we will create a new dependency with `yield`, as explained before in the section about [Dependencies with `yield`](dependencies/dependencies-with-yield.md){.internal-link target=_blank}.

Our dependency will create a new SQLAlchemy `SessionLocal` that will be used in a single request, and then close it once the request is finished.

=== "Python 3.6 and above"

    ```Python hl_lines="15-20"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="13-18"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

!!! info
    We put the creation of the `SessionLocal()` and handling of the requests in a `try` block.

    And then we close it in the `finally` block.

    This way we make sure the database session is always closed after the request. Even if there was an exception while processing the request.

    But you can't raise another exception from the exit code (after `yield`). See more in [Dependencies with `yield` and `HTTPException`](./dependencies/dependencies-with-yield.md#dependencies-with-yield-and-httpexception){.internal-link target=_blank}

And then, when using the dependency in a *path operation function*, we declare it with the type `Session` we imported directly from SQLAlchemy.

This will then give us better editor support inside the *path operation function*, because the editor will know that the `db` parameter is of type `Session`:

=== "Python 3.6 and above"

    ```Python hl_lines="24  32  38  47  53"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="22  30  36  45  51"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

!!! info "Technical Details"
    The parameter `db` is actually of type `SessionLocal`, but this class (created with `sessionmaker()`) is a "proxy" of a SQLAlchemy `Session`, so, the editor doesn't really know what methods are provided.

    But by declaring the type as `Session`, the editor now can know the available methods (`.add()`, `.query()`, `.commit()`, etc) and can provide better support (like completion). The type declaration doesn't affect the actual object.

### Create your **FastAPI** *path operations*

Now, finally, here's the standard **FastAPI** *path operations* code.

=== "Python 3.6 and above"

    ```Python hl_lines="23-28  31-34  37-42  45-49  52-55"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="21-26  29-32  35-40  43-47  50-53"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
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
    If you need to connect to your relational database asynchronously, see [Async SQL (Relational) Databases](../advanced/async-sql-databases.md){.internal-link target=_blank}.

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

=== "Python 3.6 and above"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app/schemas.py!}
    ```

=== "Python 3.9 and above"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app_py39/schemas.py!}
    ```

=== "Python 3.10 and above"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app_py310/schemas.py!}
    ```

* `sql_app/crud.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

* `sql_app/main.py`:

=== "Python 3.6 and above"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

=== "Python 3.9 and above"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
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

=== "Python 3.6 and above"

    ```Python hl_lines="14-22"
    {!> ../../../docs_src/sql_databases/sql_app/alt_main.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="12-20"
    {!> ../../../docs_src/sql_databases/sql_app_py39/alt_main.py!}
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
