# SQL（リレーショナル）データベース { #sql-relational-databases }

**FastAPI** は SQL（リレーショナル）データベースの使用を必須にはしません。必要であれば、**任意のデータベース**を使用できます。

ここでは [SQLModel](https://sqlmodel.tiangolo.com/) を使った例を見ていきます。

**SQLModel** は [SQLAlchemy](https://www.sqlalchemy.org/) と Pydantic の上に構築されています。**FastAPI** と同じ作者により、**SQL データベース**を使う必要がある FastAPI アプリに最適になるように作られています。

/// tip | 豆知識

他の任意の SQL あるいは NoSQL のデータベースライブラリ（場合によっては <abbr title="Object Relational Mapper - オブジェクト関係マッパー: いくつかのクラスが SQL テーブルを表し、そのインスタンスがそれらのテーブルの行を表すライブラリを指す専門用語">"ORMs"</abbr> と呼ばれます）を使うこともできます。FastAPI は何も強制しません。😎

///

SQLModel は SQLAlchemy をベースにしているため、SQLAlchemy が**サポートする任意のデータベース**（SQLModel からもサポートされます）を簡単に使えます。例えば:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server など

この例では、単一ファイルで動作し、Python に統合サポートがあるため、**SQLite** を使います。つまり、この例をそのままコピーして実行できます。

本番アプリでは、**PostgreSQL** のようなデータベースサーバーを使いたくなるかもしれません。

/// tip | 豆知識

フロントエンドやその他のツールを含む、**FastAPI** と **PostgreSQL** の公式プロジェクトジェネレーターがあります: [https://github.com/fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)

///

これはとてもシンプルで短いチュートリアルです。データベース一般や SQL、より高度な機能について学びたい場合は、[SQLModel のドキュメント](https://sqlmodel.tiangolo.com/)をご覧ください。

## `SQLModel` のインストール { #install-sqlmodel }

`sqlmodel` をプロジェクトに追加します:

<div class="termy">

```console
$ uv add sqlmodel
---> 100%
```

</div>

## 単一モデルでアプリ作成 { #create-the-app-with-a-single-model }

まずは最も簡単な、単一の **SQLModel** モデルだけを使うバージョンを作ります。

後で、下記のとおり**複数モデル**にしてセキュリティと汎用性を高めます。🤓

### モデルの作成 { #create-models }

`SQLModel` をインポートしてデータベースモデルを作成します:

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

`Hero` クラスは Pydantic モデルによく似ています（実際には内部的に*Pydantic モデルでもあります*）。

いくつかの違いがあります:

* `table=True` は SQLModel に対して「これは*テーブルモデル*であり、SQL データベースの**テーブル**を表す。単なる*データモデル*（通常の Pydantic クラス）ではない」と伝えます。

* `Field(primary_key=True)` は `id` が SQL データベースの**プライマリキー**であることを SQLModel に伝えます（SQL のプライマリキーについては SQLModel ドキュメントを参照してください）。

    **注:** プライマリキーのフィールドには `int | None` を使っています。これは Python コード内で `id=None` のように「`id` なしでオブジェクトを作成」し、保存時にデータベースが生成することを想定するためです。SQLModel はデータベースが `id` を提供することを理解し、スキーマでは「NULL 不可の `INTEGER` 列」を定義します。詳細は [SQLModel のプライマリキーに関するドキュメント](https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#primary-key-id) を参照してください。

* `Field(index=True)` は、この列に対して **SQL インデックス**を作成するよう SQLModel に指示します。これにより、この列でフィルタしてデータを読む場合に検索が高速になります。

    `str` と宣言されたものは、SQL の `TEXT`（データベースによっては `VARCHAR`）型の列になることを SQLModel は理解します。

### Engine の作成 { #create-an-engine }

SQLModel の `engine`（内部的には SQLAlchemy の `engine`）は、データベースへの**接続を保持**します。

同じデータベースに接続するために、コード全体で**単一の `engine` オブジェクト**を共有します。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

`check_same_thread=False` を使うと、FastAPI が異なるスレッドで同じ SQLite データベースを使えるようになります。これは、**1 つのリクエスト**が**複数スレッド**を使う可能性があるため（例えば依存関係で）、必要です。

心配はいりません。このコードの構成では、後で**1 リクエストにつき 1 つの SQLModel *session***を確実に使うようにします。実際、`check_same_thread` はそれを実現しようとしています。

### テーブルの作成 { #create-the-tables }

`SQLModel.metadata.create_all(engine)` を使って、すべての*テーブルモデル*の**テーブルを作成**する関数を追加します。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### Session 依存関係の作成 { #create-a-session-dependency }

**`Session`** は、**メモリ上でオブジェクトを保持**してデータに必要な変更を追跡し、`engine` を使ってデータベースと通信します。

各リクエストごとに新しい `Session` を提供する、`yield` を使った FastAPI の**依存関係**を作成します。これにより、1 リクエストにつき 1 つのセッションを使うことが保証されます。🤓

続いて、この依存関係を使うコードを簡潔にするために、`Annotated` による依存関係 `SessionDep` を作成します。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### 起動時にテーブルを作成 { #create-database-tables-on-startup }

アプリケーションの起動時にデータベースのテーブルを作成します。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

ここでは、アプリケーションのスタートアップイベントでテーブルを作成しています。

本番では、アプリを起動する前にマイグレーションスクリプトを実行するのが一般的でしょう。🤓

/// tip | 豆知識

SQLModel は Alembic をラップしたマイグレーションユーティリティを提供予定ですが、現時点では [Alembic](https://alembic.sqlalchemy.org/en/latest/) を直接使えます。

///

### Hero の作成 { #create-a-hero }

各 SQLModel モデルは Pydantic モデルでもあるため、Pydantic モデルと同じ**型アノテーション**で使えます。

例えば、`Hero` 型のパラメータを宣言すると、**JSON ボディ**から読み込まれます。

同様に、関数の**戻り値の型**として宣言すると、そのデータ形状が自動 API ドキュメントの UI に表示されます。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

ここでは `SessionDep` 依存関係（`Session`）を使って、新しい `Hero` を `Session` インスタンスに追加し、データベースにコミットし、`hero` のデータをリフレッシュしてから返します。

### Hero の取得 { #read-heroes }

`select()` を使ってデータベースから `Hero` を**取得**できます。結果のページネーションのために `limit` と `offset` を含められます。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### 単一の Hero を取得 { #read-one-hero }

単一の `Hero` を**取得**できます。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### Hero の削除 { #delete-a-hero }

`Hero` を**削除**することもできます。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### アプリの起動 { #run-the-app }

アプリを起動できます:

<div class="termy">

```console
$ uv run fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

その後 `/docs` の UI にアクセスすると、**FastAPI** がこれらの**モデル**を使って API を**ドキュメント化**し、同時にデータの**シリアライズ**と**バリデーション**にも使っていることがわかります。

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## 複数モデルでアプリを更新 { #update-the-app-with-multiple-models }

ここで、少し**リファクタリング**して**セキュリティ**と**汎用性**を高めましょう。

前のアプリを確認すると、UI 上で、現時点ではクライアントが作成する `Hero` の `id` を自分で決められてしまうことがわかります。😱

それは許可すべきではありません。すでに DB で割り当て済みの `id` を上書きされる可能性があります。`id` の決定は**クライアントではなく**、**バックエンド**または**データベース**が行うべきです。

さらに、ヒーローの `secret_name` を作っていますが、現状ではそれをどこでも返してしまっています。これではあまり**シークレット**ではありません... 😅

これらを、いくつかの**追加モデル**で修正します。ここで SQLModel の真価が発揮されます。✨

### 複数モデルの作成 { #create-multiple-models }

**SQLModel** では、`table=True` のあるモデルクラスが**テーブルモデル**です。

`table=True` のないモデルクラスは**データモデル**で、実体は（小さな機能がいくつか追加された）Pydantic モデルです。🤓

SQLModel では**継承**を使って、あらゆるケースでフィールドの**重複を避けられます**。

#### `HeroBase` - ベースクラス { #herobase-the-base-class }

まず、すべてのモデルで**共有されるフィールド**を持つ `HeroBase` モデルを作ります:

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - *テーブルモデル* { #hero-the-table-model }

次に、実際の*テーブルモデル*である `Hero` を作ります。他のモデルには常に含まれない**追加フィールド**を持ちます:

* `id`
* `secret_name`

`Hero` は `HeroBase` を継承しているため、`HeroBase` で宣言された**フィールド**も持ちます。つまり、`Hero` の全フィールドは次のとおりです:

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - 公開用*データモデル* { #heropublic-the-public-data-model }

次に、API のクライアントに**返す** `HeroPublic` モデルを作ります。

これは `HeroBase` と同じフィールドを持つため、`secret_name` は含みません。

これでヒーローの正体は守られます！🥷

また、`id: int` を再宣言します。これにより、API クライアントとの間で「常に `id` が存在し、`int` である（`None` にはならない）」という**契約**を結びます。

/// tip | 豆知識

戻り値のモデルで、値が常に存在し常に `int`（`None` ではない）であることを保証すると、API クライアント側のコードははるかにシンプルに書けます。

加えて、**自動生成クライアント**のインターフェースも簡潔になり、あなたの API とやり取りする開発者体験が向上します。😎

///

`HeroPublic` のフィールドは `HeroBase` と同じで、`id` は `int`（`None` ではない）として宣言されます:

* `id`
* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - 作成用*データモデル* { #herocreate-the-data-model-to-create-a-hero }

次に、クライアントからのデータを**バリデート**する `HeroCreate` モデルを作ります。

これは `HeroBase` と同じフィールドに加え、`secret_name` も持ちます。

これで、クライアントが**新しいヒーローを作成**する際に `secret_name` を送信し、データベースに保存されますが、そのシークレット名は API ではクライアントに返されません。

/// tip | 豆知識

これは**パスワード**を扱う際の方法と同じです。受け取りますが、API では返しません。

また、保存前にパスワードの値は**ハッシュ化**し、**平文のまま保存しないでください**。

///

`HeroCreate` のフィールド:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - 更新用*データモデル* { #heroupdate-the-data-model-to-update-a-hero }

前のバージョンのアプリには**ヒーローを更新する**方法がありませんでしたが、**複数モデル**を使えば可能です。🎉

`HeroUpdate` *データモデル*は少し特殊で、新しいヒーローを作成するのに必要なフィールドと**同じフィールドをすべて**持ちますが、すべてのフィールドが**オプショナル**（デフォルト値を持つ）です。これにより、更新時には変更したいフィールドだけを送れます。

すべての**フィールドが実質的に変わる**（`None` を含み、デフォルト値が `None` になる）ため、フィールドは**再宣言**する必要があります。

すべてのフィールドを再宣言するので、厳密には `HeroBase` を継承する必要はありません。一貫性のためにここでは継承していますが、必須ではありません。好みの問題です。🤷

`HeroUpdate` のフィールド:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### `HeroCreate` で作成し `HeroPublic` を返す { #create-with-herocreate-and-return-a-heropublic }

複数モデルが用意できたので、それらを使うようにアプリの部分を更新します。

リクエストでは `HeroCreate` *データモデル*を受け取り、そこから `Hero` *テーブルモデル*を作成します。

この新しい*テーブルモデル* `Hero` は、クライアントから送られたフィールドを持ち、データベースによって生成された `id` も持ちます。

関数からはこの*テーブルモデル* `Hero` をそのまま返します。しかし `response_model` に `HeroPublic` *データモデル*を指定しているため、**FastAPI** が `HeroPublic` を使ってデータをバリデート・シリアライズします。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip | 豆知識

今回は**返却値の型アノテーション** `-> HeroPublic` の代わりに `response_model=HeroPublic` を使います。返している値は実際には `HeroPublic` ではないためです。

もし `-> HeroPublic` と宣言すると、エディタや Linter は（正しく）「`HeroPublic` ではなく `Hero` を返している」と警告します。

`response_model` に指定することで、型アノテーションやエディタ等の補助を崩さずに、**FastAPI** にシリアライズの仕事を任せられます。

///

### `HeroPublic` で Hero を取得 { #read-heroes-with-heropublic }

前と同様に `Hero` を**取得**できます。再び `response_model=list[HeroPublic]` を使って、データが正しくバリデート・シリアライズされることを保証します。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### `HeroPublic` で単一の Hero を取得 { #read-one-hero-with-heropublic }

単一のヒーローを**取得**します:

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### `HeroUpdate` で Hero を更新 { #update-a-hero-with-heroupdate }

ヒーローを**更新**できます。ここでは HTTP の `PATCH` operation を使います。

コードでは、クライアントが送ったすべてのデータ、つまり**クライアントが送ったデータのみ**（デフォルト値として入ってくる値は除外）を持つ `dict` を取得します。これには `exclude_unset=True` を使います。これが主なコツです。🪄

その後、`hero_db.sqlmodel_update(hero_data)` を使って、`hero_db` を `hero_data` の内容で更新します。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### 再度 Hero を削除 { #delete-a-hero-again }

ヒーローの**削除**はほとんど変わりません。

ここはリファクタリング欲求を満たさないままにしておきます。😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### アプリの再起動 { #run-the-app-again }

アプリを再度起動できます:

<div class="termy">

```console
$ uv run fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

`/docs` の API UI に行くと、内容が更新されており、ヒーロー作成時にクライアントから `id` を受け取ることは期待されていない、などが確認できます。

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## まとめ { #recap }

[**SQLModel**](https://sqlmodel.tiangolo.com/) を使って SQL データベースとやり取りし、*データモデル*と*テーブルモデル*でコードを簡潔にできます。

さらに多くを学ぶには **SQLModel** のドキュメントをご覧ください。[**FastAPI** と SQLModel を使うチュートリアル](https://sqlmodel.tiangolo.com/tutorial/fastapi/) もあります。🚀
