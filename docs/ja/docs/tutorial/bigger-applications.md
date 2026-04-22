# 大規模アプリケーション - 複数ファイル { #bigger-applications-multiple-files }

アプリケーションや Web API を作る場合、すべてを1つのファイルに収められることはほとんどありません。

**FastAPI** は、柔軟性を保ったままアプリケーションを構造化できる便利なツールを提供します。

/// info | 情報

Flask 出身であれば、Flask の Blueprint に相当します。

///

## 例のファイル構成 { #an-example-file-structure }

次のようなファイル構成があるとします:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

/// tip | 豆知識

複数の `__init__.py` ファイルがあります: 各ディレクトリやサブディレクトリに1つずつです。

これにより、あるファイルから別のファイルへコードをインポートできます。

例えば、`app/main.py` では次のように書けます:

```
from app.routers import items
```

///

* `app` ディレクトリはすべてを含みます。そして空のファイル `app/__init__.py` があり、「Python パッケージ」（「Python モジュール」の集合）: `app` です。
* `app/main.py` ファイルがあります。Python パッケージ（`__init__.py` のあるディレクトリ）の中にあるため、そのパッケージの「モジュール」: `app.main` です。
* `app/dependencies.py` ファイルもあり、`app/main.py` と同様に「モジュール」: `app.dependencies` です。
* `app/routers/` サブディレクトリに別の `__init__.py` があるので、「Python サブパッケージ」: `app.routers` です。
* `app/routers/items.py` はパッケージ `app/routers/` 内のファイルなので、サブモジュール: `app.routers.items` です。
* `app/routers/users.py` も同様で、別のサブモジュール: `app.routers.users` です。
* `app/internal/` サブディレクトリにも `__init__.py` があるので、別の「Python サブパッケージ」: `app.internal` です。
* `app/internal/admin.py` は別のサブモジュール: `app.internal.admin` です。

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

同じファイル構成にコメントを付けると次のとおりです:

```bash
.
├── app                  # "app" は Python パッケージ
│   ├── __init__.py      # このファイルにより "app" は「Python パッケージ」になる
│   ├── main.py          # "main" モジュール（例: import app.main）
│   ├── dependencies.py  # "dependencies" モジュール（例: import app.dependencies）
│   └── routers          # "routers" は「Python サブパッケージ」
│   │   ├── __init__.py  # このファイルにより "routers" は「Python サブパッケージ」になる
│   │   ├── items.py     # "items" サブモジュール（例: import app.routers.items）
│   │   └── users.py     # "users" サブモジュール（例: import app.routers.users）
│   └── internal         # "internal" は「Python サブパッケージ」
│       ├── __init__.py  # このファイルにより "internal" は「Python サブパッケージ」になる
│       └── admin.py     # "admin" サブモジュール（例: import app.internal.admin）
```

## `APIRouter` { #apirouter }

ユーザーだけを扱うファイルが `/app/routers/users.py` のサブモジュールだとします。

ユーザーに関連する *path operations* をほかのコードから分離して整理したいはずです。

ただし、同じ **FastAPI** アプリケーション / Web API（同じ「Python パッケージ」の一部）である点は変わりません。

そのモジュールで `APIRouter` を使って *path operations* を作成できます。

### `APIRouter` のインポート { #import-apirouter }

クラス `FastAPI` と同様にインポートし、「インスタンス」を作成します:

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[1,3] title["app/routers/users.py"] *}

### `APIRouter` での *path operations* { #path-operations-with-apirouter }

これを使って *path operations* を宣言します。

使い方は `FastAPI` クラスと同じです:

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[6,11,16] title["app/routers/users.py"] *}

`APIRouter` は「ミニ `FastAPI`」のようなクラスと考えられます。

同じオプションがすべてサポートされています。

同じ `parameters`、`responses`、`dependencies`、`tags` などが使えます。

/// tip | 豆知識

この例では変数名は `router` ですが、任意の名前を付けられます。

///

この `APIRouter` をメインの `FastAPI` アプリに取り込みますが、その前に依存関係と別の `APIRouter` を確認します。

## 依存関係 { #dependencies }

アプリケーションの複数箇所で使う依存関係が必要になります。

そのため、専用の `dependencies` モジュール（`app/dependencies.py`）に置きます。

ここではカスタムヘッダー `X-Token` を読む簡単な依存関係を使います:

{* ../../docs_src/bigger_applications/app_an_py310/dependencies.py hl[3,6:8] title["app/dependencies.py"] *}

/// tip | 豆知識

この例を簡単にするために架空のヘッダーを使っています。

しかし実際には、組み込みの [Security utilities](security/index.md) を使う方が良い結果になります。

///

## 別モジュールでの `APIRouter` { #another-module-with-apirouter }

アプリケーションの「items」を扱うエンドポイントが `app/routers/items.py` のモジュールにあるとします。

次の *path operations* があります:

* `/items/`
* `/items/{item_id}`

構造は `app/routers/users.py` と同じです。

しかし、もう少し賢くしてコードを少し簡潔にしたいところです。

このモジュールのすべての *path operations* には同じものがあると分かっています:

* パスの `prefix`: `/items`
* `tags`（1つのタグ: `items`）
* 追加の `responses`
* `dependencies`: 先ほど作成した `X-Token` の依存関係が必要

そこで、各 *path operation* に個別に追加する代わりに、これらを `APIRouter` に追加できます。

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[5:10,16,21] title["app/routers/items.py"] *}

各 *path operation* のパスは次のように `/` で始める必要があるため:

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...prefix の末尾に `/` を含めてはいけません。

この場合の prefix は `/items` です。

また、`tags` のリストや追加の `responses` を、このルーターに含まれるすべての *path operations* に適用するよう追加できます。

さらに `dependencies` のリストを追加できます。これはこのルーター内のすべての *path operations* に追加され、それらへの各リクエストごとに実行・解決されます。

/// tip | 豆知識

[*path operation デコレータ*の依存関係](dependencies/dependencies-in-path-operation-decorators.md) と同様に、*path operation 関数*には値は渡されない点に注意してください。

///

最終的に、item のパスは次のとおりになります:

* `/items/`
* `/items/{item_id}`

...意図したとおりです。

* これらには、文字列 `"items"` を1つ含むタグのリストが付きます。
    * これらの「タグ」は、（OpenAPI を使う）自動インタラクティブドキュメントで特に有用です。
* すべてに事前定義した `responses` が含まれます。
* これらすべての *path operations* では、実行前に `dependencies` のリストが評価・実行されます。
    * 特定の *path operation* に依存関係を宣言した場合は、**それらも実行されます**。
    * ルーターの依存関係が先に実行され、その後に[デコレータ内の `dependencies`](dependencies/dependencies-in-path-operation-decorators.md)、次に通常のパラメータ依存関係が続きます。
    * [`scopes` を伴う `Security` 依存関係](../advanced/security/oauth2-scopes.md) を追加することもできます。

/// tip | 豆知識

`APIRouter` に `dependencies` を置くことで、*path operations* のグループ全体に認証を要求する、といった用途に使えます。個々の *path operation* に依存関係を追加していなくても構いません。

///

/// check | 確認

`prefix`、`tags`、`responses`、`dependencies` の各パラメータは（ほかの多くのケースと同様に）コード重複を避けるための **FastAPI** の機能です。

///

### 依存関係をインポート { #import-the-dependencies }

このコードはモジュール `app.routers.items`（ファイル `app/routers/items.py`）内にあります。

そして依存関係の関数はモジュール `app.dependencies`（ファイル `app/dependencies.py`）から取得する必要があります。

そこで、依存関係には `..` を使った相対インポートを使います:

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[3] title["app/routers/items.py"] *}

#### 相対インポートの仕組み { #how-relative-imports-work }

/// tip | 豆知識

インポートの仕組みを十分理解している場合は、次の節に進んでください。

///

ドット1つ `.` を使うと、次のような意味になります:

```Python
from .dependencies import get_token_header
```

意味:

* このモジュール（`app/routers/items.py`）が存在する同じパッケージ（ディレクトリ `app/routers/`）から開始し...
* モジュール `dependencies`（仮想的には `app/routers/dependencies.py`）を探し...
* そこから関数 `get_token_header` をインポートする。

しかしそのファイルは存在せず、実際の依存関係は `app/dependencies.py` にあります。

アプリ／ファイル構成がどうなっていたかを思い出してください:

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

---

ドット2つ `..` を使うと、次のようになります:

```Python
from ..dependencies import get_token_header
```

意味:

* このモジュール（`app/routers/items.py`）が存在する同じパッケージ（ディレクトリ `app/routers/`）から開始し...
* 親パッケージ（ディレクトリ `app/`）に移動し...
* そこでモジュール `dependencies`（ファイル `app/dependencies.py`）を探し...
* そこから関数 `get_token_header` をインポートする。

これは正しく動作します！ 🎉

---

同様に、ドット3つ `...` を使うと:

```Python
from ...dependencies import get_token_header
```

意味:

* このモジュール（`app/routers/items.py`）が存在する同じパッケージ（ディレクトリ `app/routers/`）から開始し...
* 親パッケージ（ディレクトリ `app/`）に移動し...
* さらにその親パッケージに移動しようとします（`app` は最上位なので親パッケージはありません 😱）...
* そこでモジュール `dependencies`（ファイル `app/dependencies.py`）を探し...
* そこから関数 `get_token_header` をインポートする。

これは `app/` より上位のパッケージ（独自の `__init__.py` を持つ）を参照することになります。しかしそのようなものはありません。そのため、この例ではエラーになります。🚨

これで仕組みが分かったので、どれほど複雑でも自分のアプリで相対インポートを使えます。🤓

### カスタムの `tags`、`responses`、`dependencies` を追加 { #add-some-custom-tags-responses-and-dependencies }

`APIRouter` に追加済みなので、各 *path operation* に `/items` の prefix や `tags=["items"]` を付けていません。

しかし、特定の *path operation* に適用される _追加の_ `tags` や、その *path operation* 固有の追加の `responses` を加えることはできます:

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[30:31] title["app/routers/items.py"] *}

/// tip | 豆知識

この最後の *path operation* は、`["items", "custom"]` のタグの組み合わせを持ちます。

またドキュメントには `404` と `403` の両方のレスポンスが表示されます。

///

## メインの `FastAPI` { #the-main-fastapi }

次に、`app/main.py` のモジュールを見ていきます。

ここでクラス `FastAPI` をインポートして使用します。

これはすべてをまとめるアプリケーションのメインファイルになります。

そして大部分のロジックはそれぞれの専用モジュールに置かれるため、メインファイルはかなりシンプルになります。

### `FastAPI` のインポート { #import-fastapi }

通常どおり `FastAPI` クラスをインポートして作成します。

さらに、各 `APIRouter` の依存関係と組み合わされる[グローバル依存関係](dependencies/global-dependencies.md)も宣言できます:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[1,3,7] title["app/main.py"] *}

### `APIRouter` のインポート { #import-the-apirouter }

次に、`APIRouter` を持つ他のサブモジュールをインポートします:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[4:5] title["app/main.py"] *}

`app/routers/users.py` と `app/routers/items.py` は同じ Python パッケージ `app` のサブモジュールなので、1つのドット `.` を使った「相対インポート」でインポートできます。

### インポートの動作 { #how-the-importing-works }

次の部分:

```Python
from .routers import items, users
```

は次の意味です:

* このモジュール（`app/main.py`）が存在する同じパッケージ（ディレクトリ `app/`）から開始し...
* サブパッケージ `routers`（ディレクトリ `app/routers/`）を探し...
* そこからサブモジュール `items`（ファイル `app/routers/items.py`）と `users`（ファイル `app/routers/users.py`）をインポートする...

モジュール `items` には変数 `router`（`items.router`）があります。これは `app/routers/items.py` で作成した `APIRouter` オブジェクトと同じものです。

モジュール `users` についても同様です。

次のようにインポートすることもできます:

```Python
from app.routers import items, users
```

/// info | 情報

最初のバージョンは「相対インポート」です:

```Python
from .routers import items, users
```

2つ目のバージョンは「絶対インポート」です:

```Python
from app.routers import items, users
```

Python のパッケージとモジュールについて詳しくは、[公式の Python モジュールに関するドキュメント](https://docs.python.org/3/tutorial/modules.html)をご覧ください。

///

### 名前衝突の回避 { #avoid-name-collisions }

サブモジュール `items` の変数 `router` だけをインポートするのではなく、サブモジュール自体を直接インポートしています。

これは、サブモジュール `users` にも `router` という変数があるためです。

もし次のように続けてインポートした場合:

```Python
from .routers.items import router
from .routers.users import router
```

`users` の `router` が `items` のものを上書きしてしまい、同時に両方を使えなくなります。

同じファイルで両方を使えるようにするため、サブモジュールを直接インポートします:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[5] title["app/main.py"] *}

### `users` と `items` の `APIRouter` を取り込む { #include-the-apirouters-for-users-and-items }

では、サブモジュール `users` と `items` から `router` を取り込みます:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[10:11] title["app/main.py"] *}

/// info | 情報

`users.router` は、ファイル `app/routers/users.py` 内の `APIRouter` を含みます。

`items.router` は、ファイル `app/routers/items.py` 内の `APIRouter` を含みます。

///

`app.include_router()` を使って、各 `APIRouter` をメインの `FastAPI` アプリケーションに追加できます。

そのルーターのすべてのルートがアプリに含まれます。

/// note | 技術詳細

実際には、`APIRouter` で宣言された各 *path operation* ごとに内部的に *path operation* が作成されます。

つまり裏側では、すべてが同じ単一のアプリであるかのように動作します。

///

/// check | 確認

ルーターを取り込んでもパフォーマンスを心配する必要はありません。

これは起動時にマイクロ秒で行われます。

したがってパフォーマンスには影響しません。⚡

///

### カスタムの `prefix`、`tags`、`responses`、`dependencies` 付きで `APIRouter` を取り込む { #include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies }

あなたの組織から `app/internal/admin.py` ファイルが提供されたとしましょう。

そこには、組織が複数プロジェクトで共有している管理用の *path operations* を持つ `APIRouter` が含まれています。

この例ではとてもシンプルですが、組織内の他プロジェクトと共有しているため、`APIRouter` 自体を直接変更して `prefix`、`dependencies`、`tags` などを追加できないとします:

{* ../../docs_src/bigger_applications/app_an_py310/internal/admin.py hl[3] title["app/internal/admin.py"] *}

それでも、`APIRouter` を取り込む際にカスタムの `prefix` を設定してすべての *path operations* を `/admin` で始めたい、既存の `dependencies` で保護したい、さらに `tags` と `responses` も含めたいとします。

元の `APIRouter` を変更することなく、`app.include_router()` にこれらのパラメータを渡すことで宣言できます:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[14:17] title["app/main.py"] *}

このようにすると、元の `APIRouter` は未変更のままなので、同じ `app/internal/admin.py` ファイルを組織内の他プロジェクトとも引き続き共有できます。

結果として、このアプリ内では `admin` モジュールの各 *path operation* が次のようになります:

* prefix は `/admin`
* タグは `admin`
* 依存関係は `get_token_header`
* レスポンスは `418` 🍵

ただし、これはこのアプリ内のその `APIRouter` にのみ影響し、それを使用する他のコードには影響しません。

例えば、他のプロジェクトでは同じ `APIRouter` を別の認証方式で使うこともできます。

### *path operation* を追加 { #include-a-path-operation }

`FastAPI` アプリに *path operations* を直接追加することもできます。

ここでは（できることを示すためだけに）追加します 🤷:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[21:23] title["app/main.py"] *}

そして、`app.include_router()` で追加したほかの *path operations* と一緒に正しく動作します。

/// info | 非常に技術的な詳細

注記: これは非常に技術的な詳細で、**読み飛ばして構いません**。

---

`APIRouter` は「マウント」されておらず、アプリケーションの他部分から分離されていません。

これは、それらの *path operations* を OpenAPI スキーマやユーザーインターフェースに含めたいからです。

完全に分離して独立に「マウント」できないため、*path operations* は直接取り込まれるのではなく「クローン（再作成）」されます。

///

## `pyproject.toml` の `entrypoint` を設定 { #configure-the-entrypoint-in-pyproject-toml }

FastAPI の `app` オブジェクトは `app/main.py` にあるので、`pyproject.toml` で `entrypoint` を次のように設定できます:

```toml
[tool.fastapi]
entrypoint = "app.main:app"
```

これは次のようにインポートするのと同等です:

```python
from app.main import app
```

このようにすると、`fastapi` コマンドがアプリの場所を把握できます。

/// Note | 備考

コマンドにパスを渡すこともできます。例えば:

```console
$ fastapi dev app/main.py
```

しかし、そのたびに `fastapi` コマンドを呼ぶ際、正しいパスを渡すのを忘れないようにする必要があります。

さらに、[VS Code Extension](../editor-support.md) や [FastAPI Cloud](https://fastapicloud.com) など、他のツールが見つけられない場合があります。そのため、`pyproject.toml` の `entrypoint` を使うことを推奨します。

///

## 自動APIドキュメントの確認 { #check-the-automatic-api-docs }

アプリを実行します:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

そして [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) を開きます。

すべてのサブモジュール由来のパスを含む自動 API ドキュメントが表示され、正しいパス（および prefix）と正しいタグが使われているのが分かります:

<img src="/img/tutorial/bigger-applications/image01.png">

## 同じルーターを異なる `prefix` で複数回取り込む { #include-the-same-router-multiple-times-with-different-prefix }

同じルーターに対して、異なる prefix で `.include_router()` を複数回使うこともできます。

例えば、同じ API を `/api/v1` と `/api/latest` のように異なる prefix で公開する場合に役立ちます。

高度な使い方なので不要かもしれませんが、必要な場合に備えて用意されています。

## `APIRouter` を別の `APIRouter` に取り込む { #include-an-apirouter-in-another }

`APIRouter` を `FastAPI` アプリケーションに取り込めるのと同じように、`APIRouter` を別の `APIRouter` に取り込むこともできます:

```Python
router.include_router(other_router)
```

`router` を `FastAPI` アプリに取り込む前にこれを実行して、`other_router` の *path operations* も含まれるようにしてください。
