# SQL（リレーショナル）データベース { #sql-relational-databases }

FastAPI は SQL（リレーショナル）データベースの使用を必須にはしません。必要であれば、任意のデータベースを使用できます。

ここでは <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a> を使った例を見ていきます。

SQLModel は <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a> と Pydantic の上に構築されています。FastAPI と同じ作者により、SQL データベースを使う必要がある FastAPI アプリに最適になるように作られています。

/// tip | 豆知識

他の任意の SQL あるいは NoSQL のデータベースライブラリ（場合によっては <abbr title="Object Relational Mapper - オブジェクト関係マッパー: いくつかのクラスが SQL テーブルを表し、そのインスタンスがそれらのテーブルの行を表すライブラリを指す専門用語">"ORMs"</abbr> と呼ばれます）を使うこともできます。FastAPI は何も強制しません。😎

///

SQLModel は SQLAlchemy をベースにしているため、SQLAlchemy がサポートする任意のデータベース（SQLModel からもサポートされます）を簡単に使えます。例えば:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server など

この例では、単一ファイルで動作し、Python に統合サポートがあるため、SQLite を使います。つまり、この例をそのままコピーして実行できます。

本番アプリでは、PostgreSQL のようなデータベースサーバーを使いたくなるかもしれません。

/// tip | 豆知識

フロントエンドやその他のツールを含む、FastAPI と PostgreSQL の公式プロジェクトジェネレーターがあります: <a href="https://github.com/fastapi/full-stack-fastapi-template" class="external-link" target="_blank">https://github.com/fastapi/full-stack-fastapi-template</a>

///

これはとてもシンプルで短いチュートリアルです。データベースや SQL、より高度な機能について学びたい場合は、<a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel のドキュメント</a>をご覧ください。

## `SQLModel` のインストール { #install-sqlmodel }

まずは [仮想環境](../virtual-environments.md){.internal-link target=_blank} を作成・有効化し、`sqlmodel` をインストールします:

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## 単一モデルでアプリ作成 { #create-the-app-with-a-single-model }

まずは最も簡単な、単一の SQLModel モデルだけを使うバージョンを作ります。

後で、下記のとおり複数モデルにしてセキュリティと汎用性を高めます。🤓

### モデルの作成 { #create-models }

`SQLModel` をインポートしてデータベースモデルを作成します:

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

`Hero` クラスは Pydantic モデルによく似ています（実際には内部的に Pydantic モデルでもあります）。

いくつかの違いがあります:

* `table=True` は SQLModel に対して「これはテーブルモデルであり、SQL データベースのテーブルを表す。単なるデータモデル（通常の Pydantic クラス）ではない」と伝えます。

* `Field(primary_key=True)` は `id` が SQL データベースのプライマリキーであることを SQLModel に伝えます（SQL のプライマリキーについては SQLModel ドキュメントを参照してください）。

    注: プライマリキーのフィールドには `int | None` を使っています。これは Python コード内で `id=None` のように「`id` なしでオブジェクトを作成」し、保存時にデータベースが生成することを想定するためです。SQLModel はデータベースが `id` を提供することを理解し、スキーマでは「NULL 不可の `INTEGER` 列」を定義します。詳細は <a href="https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#primary-key-id" class="external-link" target="_blank">SQLModel のプライマリキーに関するドキュメント</a> を参照してください。

* `Field(index=True)` は、この列に対して SQL のインデックスを作成するよう SQLModel に指示します。これにより、この列でフィルタしてデータを読む場合に検索が高速になります。

    `str` と宣言されたものは、SQL の `TEXT`（データベースによっては `VARCHAR`）型の列になることを SQLModel は理解します。

### Engine の作成 { #create-an-engine }

SQLModel の `engine`（内部的には SQLAlchemy の `engine`）は、データベースへの接続を保持します。

同じデータベースに接続するために、コード全体で 1 つの `engine` オブジェクトを共有します。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

`check_same_thread=False` を使うと、FastAPI が異なるスレッドで同じ SQLite データベースを使えるようになります。これは、依存関係などにより 1 つのリクエストが複数スレッドを使う可能性があるため、必要です。

心配はいりません。このコードの構成では、後で「1 リクエストにつき 1 つの SQLModel セッション」を確実に使うようにします。実際、`check_same_thread` はそれを実現しようとしています。

### テーブルの作成 { #create-the-tables }

`SQLModel.metadata.create_all(engine)` を使って、すべてのテーブルモデルのテーブルを作成する関数を追加します。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### Session 依存関係の作成 { #create-a-session-dependency }

`Session` は、メモリ上でオブジェクトを保持して変更を追跡し、`engine` を使ってデータベースと通信します。

各リクエストごとに新しい `Session` を提供する、`yield` を使った FastAPI の依存関係を作成します。これにより、1 リクエストにつき 1 つのセッションを使うことが保証されます。🤓

続いて、この依存関係を使うコードを簡潔にするために、`Annotated` による依存関係 `SessionDep` を作成します。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### 起動時にテーブルを作成 { #create-database-tables-on-startup }

アプリケーションの起動時にデータベースのテーブルを作成します。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

ここでは、アプリケーションのスタートアップイベントでテーブルを作成しています。

本番では、アプリを起動する前にマイグレーションスクリプトを実行するのが一般的でしょう。🤓

/// tip | 豆知識

SQLModel は Alembic をラップしたマイグレーションユーティリティを提供予定ですが、現時点では <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a> を直接使えます。

///

### Hero の作成 { #create-a-hero }

各 SQLModel モデルは Pydantic モデルでもあるため、Pydantic モデルと同じように型アノテーションで使えます。

例えば、`Hero` 型のパラメータを宣言すると、JSON ボディから読み込まれます。

同様に、関数の戻り値の型として宣言すると、そのデータ形状が自動 API ドキュメントの UI に表示されます。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

ここでは `SessionDep` 依存関係（`Session`）を使って、新しい `Hero` を `Session` インスタンスに追加し、データベースにコミットし、`hero` のデータをリフレッシュしてから返します。

### Hero の取得 { #read-heroes }

`select()` を使ってデータベースから `Hero` を取得できます。結果のページネーションのために `limit` と `offset` を含められます。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### 単一の Hero を取得 { #read-one-hero }

単一の `Hero` を取得できます。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### Hero の削除 { #delete-a-hero }

`Hero` を削除することもできます。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### アプリの起動 { #run-the-app }

アプリを起動します:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

その後 `/docs` の UI にアクセスすると、FastAPI がこれらのモデルを使って API をドキュメント化し、同時にデータのシリアライズとバリデーションにも使っていることがわかります。

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## 複数モデルでアプリを更新 { #update-the-app-with-multiple-models }

ここで、少しリファクタリングしてセキュリティと汎用性を高めましょう。

前のアプリでは、UI 上でクライアントが作成する `Hero` の `id` を自分で決められてしまいます。😱

それは許可すべきではありません。すでに DB で割り当て済みの `id` を上書きされる可能性があります。`id` の決定はクライアントではなく、バックエンドまたはデータベースが行うべきです。

さらに、`secret_name` を作っていますが、現状ではそれをどこでも返してしまっています。これではあまり「シークレット」ではありません... 😅

これらを、いくつかの追加モデルで修正します。ここで SQLModel の真価が発揮されます。✨

### 複数モデルの作成 { #create-multiple-models }

SQLModel では、`table=True` のあるモデルクラスがテーブルモデルです。

`table=True` のないモデルクラスはデータモデルで、実体は（小さな機能がいくつか追加された）Pydantic モデルです。🤓

SQLModel では継承を使って、あらゆるケースでフィールドの重複を避けられます。

#### `HeroBase` - ベースクラス { #herobase-the-base-class }

まず、すべてのモデルで共有されるフィールドを持つ `HeroBase` モデルを作ります:

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - テーブルモデル { #hero-the-table-model }

次に、実際のテーブルモデルである `Hero` を作ります。他のモデルには常に含まれない追加フィールドを持ちます:

* `id`
* `secret_name`

`Hero` は `HeroBase` を継承しているため、`HeroBase` で宣言されたフィールドも持ちます。つまり、`Hero` の全フィールドは次のとおりです:

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - 公開用データモデル { #heropublic-the-public-data-model }

次に、API のクライアントに返す `HeroPublic` モデルを作ります。

これは `HeroBase` と同じフィールドを持つため、`secret_name` は含みません。

これでヒーローの正体は守られます！🥷

また、`id: int` を再宣言します。これにより、API クライアントとの間で「常に `id` が存在し、`int` である（`None` にはならない）」という契約を結びます。

/// tip | 豆知識

戻り値のモデルで、値が常に存在し常に `int`（`None` ではない）であることを保証すると、API クライアント側のコードははるかにシンプルに書けます。

加えて、自動生成クライアントのインターフェースも簡潔になり、あなたの API とやり取りする開発者体験が向上します。😎

///

`HeroPublic` のフィールドは `HeroBase` と同じで、`id` は `int`（`None` ではない）として宣言されます:

* `id`
* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - 作成用データモデル { #herocreate-the-data-model-to-create-a-hero }

次に、クライアントからのデータをバリデートする `HeroCreate` モデルを作ります。

これは `HeroBase` と同じフィールドに加え、`secret_name` も持ちます。

これで、クライアントが新しいヒーローを作成する際に `secret_name` を送信し、データベースに保存されますが、そのシークレット名は API ではクライアントに返されません。

/// tip | 豆知識

これはパスワードを扱う際の方法と同じです。受け取りますが、API では返しません。

また、保存前にパスワードの値はハッシュ化し、平文のまま保存しないでください。

///

`HeroCreate` のフィールド:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - 更新用データモデル { #heroupdate-the-data-model-to-update-a-hero }

前のバージョンのアプリにはヒーローを更新する方法がありませんでしたが、複数モデルを使えば可能です。🎉

`HeroUpdate` データモデルは少し特殊で、新しいヒーローを作成するのに必要なフィールドと同じフィールドをすべて持ちますが、すべてのフィールドがオプショナル（デフォルト値を持つ）です。これにより、更新時には変更したいフィールドだけを送れます。

すべてのフィールドの型が実質的に変わる（`None` を含み、デフォルト値が `None` になる）ため、フィールドは再宣言する必要があります。

すべてのフィールドを再宣言するので、厳密には `HeroBase` を継承する必要はありません。一貫性のためにここでは継承していますが、必須ではありません。好みの問題です。🤷

`HeroUpdate` のフィールド:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### `HeroCreate` で作成し `HeroPublic` を返す { #create-with-herocreate-and-return-a-heropublic }

複数モデルが用意できたので、それらを使うようにアプリの部分を更新します。

リクエストでは `HeroCreate` データモデルを受け取り、そこから `Hero` テーブルモデルを作成します。

この新しいテーブルモデル `Hero` は、クライアントから送られたフィールドを持ち、データベースによって生成された `id` も持ちます。

関数からはこのテーブルモデル `Hero` をそのまま返します。しかし `response_model` に `HeroPublic` データモデルを指定しているため、FastAPI が `HeroPublic` を使ってデータをバリデート・シリアライズします。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip | 豆知識

今回は返却値の型アノテーション `-> HeroPublic` の代わりに `response_model=HeroPublic` を使います。返している値は実際には `HeroPublic` ではないためです。

もし `-> HeroPublic` と宣言すると、エディタや Linter は（正しく）「`HeroPublic` ではなく `Hero` を返している」と警告します。

`response_model` に指定することで、型アノテーションやエディタ等の補助を崩さずに、FastAPI にシリアライズの仕事を任せられます。

///

### `HeroPublic` で Hero を取得 { #read-heroes-with-heropublic }

前と同様に `Hero` を取得できます。再び `response_model=list[HeroPublic]` を使って、データが正しくバリデート・シリアライズされることを保証します。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### `HeroPublic` で単一の Hero を取得 { #read-one-hero-with-heropublic }

単一のヒーローを取得します:

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### `HeroUpdate` で Hero を更新 { #update-a-hero-with-heroupdate }

ヒーローを更新できます。ここでは HTTP の `PATCH` を使います。

コードでは、クライアントが送ったデータのみ（デフォルト値として入ってくる値は除外）を持つ `dict` を取得します。これには `exclude_unset=True` を使います。これが主なコツです。🪄

その後、`hero_db.sqlmodel_update(hero_data)` を使って、`hero_db` を `hero_data` の内容で更新します。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### 再度 Hero を削除 { #delete-a-hero-again }

ヒーローの削除はほとんど変わりません。

ここはリファクタリング欲求を満たさないままにしておきます。😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### アプリの再起動 { #run-the-app-again }

アプリを再度起動します:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

`/docs` の API UI に行くと、内容が更新されており、ヒーロー作成時にクライアントから `id` を受け取ることは期待されていない、などが確認できます。

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## まとめ { #recap }

<a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a> を使って SQL データベースとやり取りし、データモデルとテーブルモデルでコードを簡潔にできます。

さらに多くを学ぶには SQLModel のドキュメントをご覧ください。<a href="https://sqlmodel.tiangolo.com/tutorial/fastapi/" class="external-link" target="_blank">FastAPI と SQLModel を使うチュートリアル</a> もあります。🚀
