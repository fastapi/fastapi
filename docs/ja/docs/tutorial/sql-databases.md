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

!!! Tip "豆知識"
    **FastAPI** と **PostgreSQL** を使った公式のプロジェクトジェネレータがあります。これはフロントエンドやその他のツールを含んでおり、全て **Docker** を基にしています。 <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

!!! note "備考"
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

!!! Tip "豆知識"
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

!!! Tip "豆知識"

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

!!! info "技術的詳細"

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

!!! Tip "豆知識"
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

!!! Tip "豆知識"
    SQLAlchemyの *モデル* とPydanticの *モデル* の混同を避けるために、SQLAlchemyのモデルを `models.py` に、Pydantic のモデルを `schemas.py` に記述することにします。

    これらのPydanticモデルは、多かれ少なかれ「スキーマ」（有効なデータの形）を定義するものです。

    これにより、両者を使い分ける際の混乱を回避することができます。

### Pydanticの初期モデル/スキーマの作成

`ItemBase` と `UserBase` という Pydantic *モデル* (スキーマ) を作成して、データの作成時や読み込み時に共通の属性を持つようにします。

そして、それらを継承した `ItemCreate` と `UserCreate` を作成し（つまり、同じ属性を持つことになります）、さらに作成に必要な追加データ（属性）を作成します。

そのため、ユーザは作成時に `password` も持つことになります。

しかし、セキュリティのために、`password`は他のPydantic *モデル*には含まれません。例えば、ユーザを読み取るときにAPIから送られることはありません。

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

同じように、ユーザを読み込むときに、 `items` にはこのユーザに属するアイテムが含まれると宣言できるようになりました。

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

!!! Tip "豆知識"
    ユーザを読み込む（APIから返す）ときに使用されるPydantic *モデル*である `User` には、 `password` が含まれていないことに注意してください。

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

!!! Tip "豆知識"
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

では、`sql_app/crud.py` を見てみましょう。

このファイルでは、データベースのデータを操作するための再利用可能な関数を用意します。

**CRUD** はこれに由来します: **C**reate, **R**ead, **U**pdate, and **D**elete.

...ただし、この例では作成と読み込みのみです。

### データの読み込み

`sqlalchemy.orm` から `Session` をインポートします。これにより、 `db` パラメータの型を宣言して、関数内でより良い型チェックと補完を行うことができるようになります。

`models` (SQLAlchemy のモデル) と`schemas` (Pydantic の *モデル* / スキーマ) をインポートします。

以下の操作のためのutility functionsを作成します:

* IDとemailから単一のuserを読み込む。
* 複数のuserを読み込む。
* 複数のitemを読み込む。

```Python hl_lines="1  3  6-7  10-11  14-15  27-28"
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

!!! Tip "豆知識"
    *path operation function*とは別に、データベースとのやり取り（ユーザーやアイテムの取得）だけに特化した関数を作ることで、複数のパーツで再利用しやすくなりますし、その関数に対して<abbr title="コードで書かれた自動テストで、別のコードが正しく動作しているかどうかをチェックします。">ユニットテスト</abbr>を追加することもできます。

### データの作成

次に、データを作成するためのutility functionsを作成します。

The steps are:

* SQLAlchemyのモデル *インスタンス* を、あなたのデータで作成します。
* そのインスタンスオブジェクトをデータベースセッションに `追加` します。
* 変更をデータベースに `commit` します (変更が保存されます)。
* インスタンスを `refresh` します (生成された ID のような、データベースからの新しいデータを含むようにします)。

```Python hl_lines="18-24  31-36"
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

!!! Tip "豆知識"
    SQLAlchemy の `User` のモデルは、 `hashed_password` を含んでいます。これは、安全なハッシュ化されたパスワードを含むべきです。

    しかし、APIクライアントが提供するのはオリジナルのパスワードなので、それを抽出してアプリケーションでハッシュ化したパスワードを生成する必要がある。

    そして、保存する値を `hashed_password` 引数に渡します。

!!! Warning "注意"
    この例では、パスワードがハッシュ化されていないため、安全ではありません。

    実際のアプリケーションでは、パスワードをハッシュ化する必要があり、決して平文で保存することはできません。

    詳しくは、チュートリアルの「セキュリティ」のセクションに戻ってください。

    ここでは、データベースのツールや仕組みにのみ焦点を当てます。

!!! Tip "豆知識"
    `Item` にキーワード引数を渡して、Pydantic *model* からそれぞれを読み込むのではなく、次の関数でPydantic *model* データの `dict` を生成しているのです:

    `item.dict()`

    そして、`dict` の key-value ペアを SQLAlchemy の `Item` へのキーワード引数として渡しています。次のように:

    `Item(**item.dict())`

    さらに、Pydantic *model* が提供しない別のキーワード引数 `owner_id` を、渡します。次のように:

    `Item(**item.dict(), owner_id=user_id)`

## Main **FastAPI** app

そして、`sql_app/main.py`ファイルで、前に作成した他のすべてのパーツを統合して使用するようにしましょう。

### データベーステーブルの作成

非常にシンプルな方法で、データベースのテーブルを作成します:

=== "Python 3.6 and above"

    ```Python hl_lines="9"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="7"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

#### Alembicに関する備考

通常、 <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a> でデータベースを初期化（テーブルの作成など）することが多いと思います。

そして、Alembicを「マイグレーション」にも使うことになります（それが主な仕事です）。

マイグレーション "とは、SQLAlchemy のモデルの構造を変更したり、新しい属性を追加した りするたびに、それらの変更をデータベースに再現し、新しいカラムやテーブルを追加する ために必要な一連のステップのことです。

FastAPI プロジェクトでの Alembic の例は [Project Generation - Template](../project-generation.md){.internal-link target=_blank} のテンプレートで確認できます。具体的には <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/alembic/" class="external-link" target="_blank">ソースコード内の alembic ディレクトリ</a> にあります。

### 依存関係の作成

ここで、`sql_app/database.py` ファイルで作成した `SessionLocal` クラスを使用して、依存関係を作成します。

リクエストごとに独立したデータベースセッション/接続 (`SessionLocal`) を持ち、すべてのリクエストで同じセッションを使用し、リクエストの終了後にそれを閉じる必要があります。

そして、次のリクエストのために新しいセッションが作成されます。

そのために、以前 [Dependencies with `yield`](dependencies/dependencies-with-yield.md){.internal-link target=_blank} の章で説明したように、`yield` で新しい依存関係を作成します。

この依存関係は、一つのリクエストで使われる新しい SQLAlchemy の `SessionLocal` を作成し、リクエストが終了したらそれを閉じます。

=== "Python 3.6 and above"

    ```Python hl_lines="15-20"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="13-18"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

!!! info "情報"
    `SessionLocal()` の生成とリクエストの処理を `try` ブロックに記述しています。

    そして、`finally` ブロックでそれを閉じます。

    このようにして、リクエストの後にデータベースセッションが常に閉じられるようにします。たとえ、リクエストの処理中に例外が発生したとしてもです。

    しかし、終了コード(`yield`の後)からは別の例外を発生させることができません。詳しくは [Dependencies with `yield` and `HTTPException`](./dependencies/dependencies-with-yield.md#dependencies-with-yield-and-httpexception){.internal-link target=_blank} を参照してください。

そして、*path operation function* で依存関係を使うときには、SQLAlchemy から直接インポートした `Session` 型で宣言します。

これにより、エディタは `db` パラメータが `Session` 型であることがわかるので、*path operation function* 内でより良いエディタサポートが得られます:

=== "Python 3.6 and above"

    ```Python hl_lines="24  32  38  47  53"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="22  30  36  45  51"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

!!! info "技術的詳細"
    パラメータ `db` は実際には `SessionLocal` 型ですが、このクラス (`sessionmaker()` で生成) は SQLAlchemy の `Session` の「代理」なので、エディタにはどのメソッドが提供されているのかがよくわかりません。

    しかし、型を `Session` と宣言することで、エディタは利用可能なメソッド (`.add()`, `.query()`, `.commit()` など) を知ることができ、よりよいサポート (補完など) を提供できるようになりました。型宣言は実際のオブジェクトには影響を与えません。

### **FastAPI** の *path operations* の作成

さて、最後に、標準的な **FastAPI** の *path operations* のコードを紹介します。

=== "Python 3.6 and above"

    ```Python hl_lines="23-28  31-34  37-42  45-49  52-55"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="21-26  29-32  35-40  43-47  50-53"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

依存関係にある各リクエストの前に `yield` でデータベースセッションを作成し、終了後にそれを閉じています。

そして、そのセッションを直接取得するために、*path operation function*に必要な依存関係を作成します。

これによって、*path operation function* の内部から直接 `crud.get_user` を呼び出して、そのセッションを使用することができます。

!!! Tip "豆知識"
    返す値は、SQLAlchemy のモデル、あるいは SQLAlchemy のモデルのリストである ことに注意してください。

    しかし、すべての *path operations* は `orm_mode` を使用した Pydantic *モデル* / スキーマによる `response_model` を持っているので、Pydantic モデルで宣言されたデータはそれらから抽出され、通常のフィルタリングや検証を経てクライアントに返されることになります。

!!! Tip "豆知識"
    また、 `List[schemas.Item]` のような Python の標準的な型を持つ `response_models` が存在することに注意してください。

    しかし、その `List` のコンテンツ/パラメータは `orm_mode` を持つ Pydantic *model* であるため、通常通りデータを取得してクライアントに返すことは問題ないはずです。

### `def` と `async def` について

ここでは、*path operation function* の中と依存関係の中で、SQLAlchemy のコードを使っていて、順番に、外部のデータベースと通信していきます。

その分、「待つ」ことが必要かもしれません。

しかし、SQLAlchemy は `await` を直接使う互換性を持っていないので、以下のようにしたいのですが:

```Python
user = await db.query(User).first()
```

...代わりに以下のようにしています:

```Python
user = db.query(User).first()
```

そして、*path operation functions* と依存関係を `async def` を使わずに、通常の `def` で次のように宣言します:

```Python hl_lines="2"
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    ...
```

!!! info "情報"
    リレーショナルデータベースに非同期で接続する必要がある場合は、 [Async SQL (Relational) Databases](../advanced/async-sql-databases.md){.internal-link target=_blank} を参照してください。

!!! note "非常に技術的な詳細"
    この `async def` と `def` がどのように扱われるのか、非常に技術的な詳細は [Async](../async.md#very-technical-details){.internal-link target=_blank} ドキュメントで確認することができますので、興味があり、深い技術的知識をお持ちの方はご覧ください。

## マイグレーション

SQLAlchemyを直接使っていて、**FastAPI**との連携にプラグインの類は必要ないため、<a href="https://alembic.sqlalchemy.org" class="external-link" target="_blank">Alembic</a> と直接データベースの <abbr title="Automatically updating the database to have any new column we define in our models.">マイグレーション</abbr> を連携させることができました。

そして、SQLAlchemyに関連するコードとSQLAlchemyのモデルはそれぞれ独立したファイルに住んでいるので、FastAPIやPydanticなどをインストールしなくても、Alembicでマイグレーションを行うことさえ可能でしょう。

同じように、SQLAlchemy のモデルやユーティリティを、 **FastAPI** とは関係のない、コードの他の部分で使うことができるようになります。

例えば、<a href="https://docs.celeryq.dev" class="external-link" target="_blank">Celery</a>、<a href="https://python-rq.org/" class="external-link" target="_blank">RQ</a>または<a href="https://arq-docs.helpmanual.io/" class="external-link" target="_blank">ARQ</a>を使ったbackground task workerで。

## すべてのファイルを確認する

 my_super_project`というディレクトリがあり、その中に `sql_app` というサブディレクトリがあることを思い出してください。

`sql_app` には以下のファイルが必要です:

* `sql_app/__init__.py`: 空のファイル

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

## 確認する

このコードをコピーして、そのまま使用することができます。

!!! info "情報"

    実際、ここに示したコードはテストの一部です。このドキュメントにあるコードのほとんどのように。

そうすれば、Uvicornで実行できます:


<div class="termy">

```console
$ uvicorn sql_app.main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

そしたら、ブラウザで <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> を開けます。

そして、実際のデータベースからデータを読み出しながら、**FastAPI**アプリケーションと対話することができるようになります:

<img src="/img/tutorial/sql-databases/image01.png">

## データベースと直接対話する

FastAPI とは別に、SQLite データベース（ファイル）を直接探索して、内容のデバッグ、テーブル、カラム、レコードの追加、データの修正などを行いたい場合、<a href="https://sqlitebrowser.org/" class="external-link" target="_blank">DB Browser for SQLite</a>を使用することができます。

このように表示されます:

<img src="/img/tutorial/sql-databases/image02.png">

<a href="https://inloop.github.io/sqlite-viewer/" class="external-link" target="_blank">SQLite Viewer</a>や<a href="https://extendsclass.com/sqlite-browser.html" class="external-link" target="_blank">ExtendsClass</a>のようなオンライン SQLiteブラウザを使用することもできます。

## ミドルウェアによる代替DBセッション

もし `yield` で依存関係を使えない場合 -- たとえば、**Python 3.7** を使っておらず、上記の **Python 3.6** 用の "backports" をインストールできない場合 -- 同じ方法で「ミドルウェア」でセッションをセットアップすることが可能です。

「ミドルウェア」とは、基本的にリクエストごとに必ず実行される関数で、エンドポイント関数の前に実行されるコードと、エンドポイント関数の後に実行されるコードがあります。

### ミドルウェアの作成

これから追加するミドルウェア(単なる関数)は、各リクエストに対して新しい SQLAlchemy `SessionLocal` を作成し、それをリクエストに追加して、リクエストが終了したらそれをクローズします。

=== "Python 3.6 and above"

    ```Python hl_lines="14-22"
    {!> ../../../docs_src/sql_databases/sql_app/alt_main.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="12-20"
    {!> ../../../docs_src/sql_databases/sql_app_py39/alt_main.py!}
    ```

!!! info "情報"
    `SessionLocal()` の生成とリクエストの処理を `try` ブロックに記述しています。

    そして、`finally` ブロックでそれを閉じます。

    このようにして、リクエストの後にデータベースセッションが常に閉じられるようにします。たとえ、リクエストの処理中に例外が発生したとしてもです。

### `request.state` について

`request.state` は、各 `Request` オブジェクトのプロパティである。これは、リクエスト自体に付随する任意のオブジェクト (この場合はデータベースセッション) を格納するためにあります。詳しくは<a href="https://www.starlette.io/requests/#other-state" class="external-link" target="_blank">Starletteの`Request` stateに関するドキュメント</a>を参照してください。

この場合、すべてのリクエストを通じて単一のデータベースセッションが使用され、その後（ミドルウェアで）クローズされることを保証するのに役立ちます。

### yield` やミドルウェアとの依存関係

ここで **middleware** を追加することは、 `yield` による依存関係が行うことと似ていますが、いくつかの違いがあります。

* より多くのコードを必要とし、少し複雑になっています。
* ミドルウェアは `async` 関数である必要があります。
    * その中に、ネットワークを「待つ」必要があるコードがあると、そこでアプリケーションが「ブロック」され、パフォーマンスが少し低下する可能性があります。
    * もっとも、ここでは `SQLAlchemy` の動作にはあまり問題はないでしょうけど。
    * しかし、ミドルウェアに<abbr title="input and output">I/O</abbr>待ちの多いコードを追加した場合、その後、問題が発生する可能性があります。
* ミドルウェアは、リクエスト*ごと*に実行されます。
    * そのため、リクエストごとに接続が作成されます。
    * そのリクエストを処理する*path operation*がDBを必要としていなかったとしても。

!!! Tip "豆知識"
    ユースケースで十分な場合は、`yield`を使った依存関係を使う方がいいかもしれません。

!!! info "情報"
    最近、**FastAPI** に `yield` を含む依存関係が追加されました。

    このチュートリアルの以前のバージョンでは、ミドルウェアを使った例しかありませんでしたが、データベースのセッション管理にミドルウェアを使ったアプリケーションはいくつかあると思われます。
