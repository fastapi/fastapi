# より大きなアプリケーションの構造 <!-- # Bigger Applications - Multiple Files -->

<!-- If you are building an application or a web API, it's rarely the case that you can put everything on a single file. -->
アプリケーションやWeb APIを構築するとき、コードを1つのファイルにまとめることはまずありません。

<!-- **FastAPI** provides a convenience tool to structure your application while keeping all the flexibility. -->
**FastAPI**は、柔軟性を保ちつつ、アプリケーションを構築できる便利なツールです。

!!! info "情報"
    <!-- If you come from Flask, this would be the equivalent of Flask's Blueprints. -->
    Flaskを知っているなら、これはFlaskのBlueprintに相当するものです。

<!-- ## An example file structure -->
## ファイル構成例

<!-- Let's say you have a file structure like this: -->
例えば、以下のようなファイル構成があるとします:

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

!!! tip "豆知識"
    <!-- There are several `__init__.py` files: one in each directory or subdirectory. -->
    `__init__.py`ファイルが、各ディレクトリ、サブディレクトリに1つずつ配置されています。

    <!-- This is what allows importing code from one file into another. -->
    こうすることで、ほかのファイルからファイルをインポートすることができるようになります。

    <!-- For example, in `app/main.py` you could have a line like: -->
    例えば、`app/main.py`に、以下のようにファイルをインポートすることができます。

    ```
    from app.routers import items
    ```

<!--
* It contains an `app/main.py` file. As it is inside a Python package (a directory with a file `__init__.py`), it is a "module" of that package: `app.main`.
* There's also an `app/dependencies.py` file, just like `app/main.py`, it is a "module": `app.dependencies`.
* There's a subdirectory `app/routers/` with another file `__init__.py`, so it's a "Python subpackage": `app.routers`.
* The file `app/routers/items.py` is inside a package, `app/routers/`, so, it's a submodule: `app.routers.items`.
* The same with `app/routers/users.py`, it's another submodule: `app.routers.users`.
* There's also a subdirectory `app/internal/` with another file `__init__.py`, so it's another "Python subpackage": `app.internal`.
* And the file `app/internal/admin.py` is another submodule: `app.internal.admin`.
-->

* `app/main.py`ファイルは、Pythonパッケージ( `__init__.py`ファイルがあるディレクトリ)の中にあり、`app.main`という "モジュール" になります。
* `app/main.py`と同じように、`app/dependencies.py`ファイルがあり、`app.dependencies`という "モジュール" になります。
* `app/routers/`サブディレクトリには、`__init__.py`ファイルがあり、`app.routers`という "Python サブパッケージ" になります。
* `app/routers/items.py`ファイルは、`app/routers/`パッケージの中にあるので、`app.routers.items`というサブモジュールになります。
* `app/outers/users.py`ファイルも、`app/routers/`パッケージの中にあるので、`app.routers.items`というサブモジュールになります。
* `app/internal/`サブディレクトリにも`__init__.py`というファイルがあるので、これも`app.internal`という "Python サブパッケージ" になります。
* `app/internal/admin.py`と`app.internal.admin`もサブモジュールになります。

<img src="/img/tutorial/bigger-applications/package.svg">

<!-- Let's say you have a file structure like this: -->
ファイル構成をコメント付きで表すと、以下のようになります:

```
.
├── app                  # "app"はPythonパッケージ
│   ├── __init__.py      # "app"を"Pythonパッケージにするファイル
│   ├── main.py          # "main"モジュール 例. import app.main
│   ├── dependencies.py  # "dependencies"モジュール。 例. import app.dependencies
│   └── routers          # "routers"は"Pythonサブパッケージ"
│   │   ├── __init__.py  # "routers"を"Pythonサブパッケージ"にするファイル
│   │   ├── items.py     # "items"サブモジュール 例. import app.routers.items
│   │   └── users.py     # "users"サブモジュール 例. import app.routers.users
│   └── internal         # "internal"は"Pythonサブパッケージ"
│       ├── __init__.py  # "internal"を"Pythonサブパッケージ"にするファイル
│       └── admin.py     # "admin"サブモジュール 例. import app.internal.admin
```

## `APIRouter`

<!-- Let's say the file dedicated to handling just users is the submodule at `/app/routers/users.py`. -->
`/app/routers/users.py`サブモジュールは、ユーザーだけを扱う専用のファイルにするとします。

<!-- You want to have the *path operations* related to your users separated from the rest of the code, to keep it organized. -->
ユーザーに関する*path operation*を、他のコードから分離して整理した状態にしたいのです。

<!-- But it's still part of the same **FastAPI** application/web API (it's part of the same "Python Package"). -->
しかし、分離したとしても、この部分はいまだ**FastAPI**アプリケーション/Web APIの一部のままとなるのです(同じ「Pythonパッケージ」の一部となります)。

<!-- You can create the *path operations* for that module using `APIRouter`. -->
`APIRouter`を使用して、このモジュールを*path operation*として作成します。

<!-- ### Import `APIRouter` -->
### `APIRouter`のインポート

<!-- You import it and create an "instance" the same way you would with the class `FastAPI`: -->
APIRouterをインポートして、`FastAPI`クラスと同じように"インスタンス"化します:

```Python hl_lines="1  3" title="app/routers/users.py"
{!../../../docs_src/bigger_applications/app/routers/users.py!}
```

<!-- ### *Path operations* with `APIRouter` -->
### `APIRouter`と*path operation*

<!-- And then you use it to declare your *path operations*. -->
APIRouterを使用して*path operation*を宣言します。

<!-- Use it the same way you would use the `FastAPI` class: -->
これは`FastAPI`クラスの使い方と同じ使い方になります:

```Python hl_lines="6  11  16" title="app/routers/users.py"
{!../../../docs_src/bigger_applications/app/routers/users.py!}
```

<!-- You can think of `APIRouter` as a "mini `FastAPI`" class. -->
`APIRouter`を"小さな`FastAPI`"クラスと考えることができます。

<!-- All the same options are supported. -->
すべて同じオプションがサポートされます。

<!-- All the same `parameters`, `responses`, `dependencies`, `tags`, etc. -->
`parameters`、`responses`、`dependencies`、`tags`など、すべて同じオプションになります。

!!! tip "豆知識"
    <!-- In this example, the variable is called `router`, but you can name it however you want. -->
    この例では、`router`という変数名にしていますが、好きな名前をつけることができます。

<!-- We are going to include this `APIRouter` in the main `FastAPI` app, but first, let's check the dependencies and another `APIRouter`. -->
この`APIRouter`をメインの`FastAPI`アプリに組み込む前に、依存関係と他の`APIRouter`を確認してみましょう。

<!-- ## Dependencies -->
## 依存関係

<!-- We see that we are going to need some dependencies used in several places of the application. -->
アプリケーションのいくつかの場所では、依存関係が必要となることがあります。

<!-- So we put them in their own `dependencies` module (`app/dependencies.py`). -->
そこで、依存関係を`dependencies`モジュール(`app/dependencies.py`)にまとめてみました。

<!-- We will now use a simple dependency to read a custom `X-Token` header: -->
ここでは、カスタムの`X-Token`ヘッダーを読み込むために、シンプルな依存関係を使用してみましょう：

=== "Python 3.9+"

    ```Python hl_lines="3  6-8" title="app/dependencies.py"
    {!> ../../../docs_src/bigger_applications/app_an_py39/dependencies.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="1  5-7" title="app/dependencies.py"
    {!> ../../../docs_src/bigger_applications/app_an/dependencies.py!}
    ```

=== "Python 3.8+ non-Annotated"

    !!! tip "豆知識"
        <!-- Prefer to use the `Annotated` version if possible. -->
        できれば`Annotated`バージョンを使いたいです。

    ```Python hl_lines="1  4-6" title="app/dependencies.py"
    {!> ../../../docs_src/bigger_applications/app/dependencies.py!}
    ```

!!! tip "豆知識"
    <!-- We are using an invented header to simplify this example. -->
    この例をシンプルにするために、ヘッダーを作っています。

    <!-- But in real cases you will get better results using the integrated [Security utilities](security/index.md){.internal-link target=_blank}. -->
    しかし、実際のケースでは、統合された[セキュリティ入門](security/index.md){.internal-link target=_blank}にて説明している方法を利用したほうが良いでしょう。

<!-- ## Another module with `APIRouter` -->
## `APIRouter`で別モジュールの作成

<!-- Let's say you also have the endpoints dedicated to handling "items" from your application in the module at `app/routers/items.py`. -->
`app/routers/items.py`モジュールに、"アイテム"を処理するためのエンドポイントもあるとします。

<!-- You have *path operations* for: -->
このエンドポイントの*path operation*を以下とします：

* `/items/`
* `/items/{item_id}`

<!-- It's all the same structure as with `app/routers/users.py`. -->
`app/routers/users.py`とすべて同じ構造になります。

<!-- But we want to be smarter and simplify the code a bit. -->
しかし、よりスマートでシンプルなコードにしたいところです。

<!-- We know all the *path operations* in this module have the same: -->
このモジュールの*path operation*がすべて同じものになります：

<!--
* Path `prefix`: `/items`.
* tags: (just one tag: `items`).
* Extra responses.
* dependencies: they all need that X-Token dependency we created.
-->

* `/items`パス`プレフィックス`
* `tags`: (`items`のタグ)
* 追加の`responses`
* 作成した`X-Token`に依存するすべてのdependencies

<!-- So, instead of adding all that to each *path operation*, we can add it to the `APIRouter`. -->
各*path operation*すべてにこれらを追加する代わりに、`APIRouter`に追加することができます。

```Python hl_lines="5-10  16  21" title="app/routers/items.py"
{!../../../docs_src/bigger_applications/app/routers/items.py!}
```

<!-- As the path of each *path operation* has to start with `/`, like in: -->
各*path operation*のパスは`/`で始めなければなりません：

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

<!-- ...the prefix must not include a final `/`. -->
...プレフィックスには、は最後の`/`を含めてはいけません。

<!-- So, the prefix in this case is `/items`. -->
つまり、この場合のプレフィックスは`/items`となります。

<!-- We can also add a list of `tags` and extra `responses` that will be applied to all the *path operations* included in this router. -->
また、このルーターに含まれるすべての*path operation*に適用される`tags`と追加の`responses`のリストを追加することもできます。

<!-- And we can add a list of `dependencies` that will be added to all the *path operations* in the router and will be executed/solved for each request made to them. -->
そして、ルーター内のすべての*path operation*に、各リクエストに対して実行/解決される`依存関係`のリストを追加することができます。

!!! tip "豆知識"
    <!-- Note that, much like [dependencies in *path operation decorators*](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, no value will be passed to your *path operation function*. -->
    [*path operation*デコレータの依存関係](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}のように、*path operationの関数*には値が渡されないことに注意してください。

<!-- The end result is that the item paths are now: -->
これで、アイテムへのパスができました：

* `/items/`
* `/items/{item_id}`

<!-- ...as we intended. -->
...意図した通りです。

<!-- * They will be marked with a list of tags that contain a single string `"items"`.
    * These "tags" are especially useful for the automatic interactive documentation systems (using OpenAPI).
* All of them will include the predefined `responses`.
* All these *path operations* will have the list of `dependencies` evaluated/executed before them.
    * If you also declare dependencies in a specific *path operation*, **they will be executed too**.
    * The router dependencies are executed first, then the [`dependencies` in the decorator](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, and then the normal parameter dependencies.
    * You can also add [`Security` dependencies with `scopes`](../advanced/security/oauth2-scopes.md){.internal-link target=_blank}. -->

* 文字列`"items"`を含むタグのリストでマークされます。
    * これらの"tags"は、(OpenAPIを使用した)インタラクティブにドキュメントの自動生成を行うシステムにとって特に有用です。
* これらのすべてに、あらかじめ定義された`レスポンス`が含まれます。
* これらの *path operation* はすべて、実行前に`依存関係`のリストが評価/実行されます。
    * 特定の*path operation*で依存関係も宣言すると、**それらも実行されます**。
    * 最初にルーターの依存関係が実行され、次に[path operationデコレータの`依存関係`](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}、そして通常のパラメーターの依存関係が実行されます。
    * また、[`Security` dependencies with `scopes`](../advanced/security/oauth2-scopes.md){.internal-link target=_blank}を追加することもできます。

!!! tip "豆知識"
    `APIRouter`に`依存関係`を持つことで、例えば、*path operation*のグループ全体に認証を要求することができます。たとえ依存関係がそれぞれ個別に追加されなくても、です。

!!! check "チェック"
    <!-- The `prefix`, `tags`, `responses`, and `dependencies` parameters are (as in many other cases) just a feature from **FastAPI** to help you avoid code duplication. -->
    `prefix`、`tags`、`responses`、`dependencies` パラメータは、(他の多くの場合と同様に)コードの重複を避けるための**FastAPI**の機能になります。

<!-- ### Import the dependencies -->
### 依存関係のインポート

<!-- This code lives in the module `app.routers.items`, the file `app/routers/items.py`. -->
このコードは`app.routers.items`モジュールの`app/routers/items.py`にあります。

<!-- And we need to get the dependency function from the module `app.dependencies`, the file `app/dependencies.py`. -->
そして、`app.dependencies`モジュール、`app/dependencies.py`ファイルから依存関数を取得する必要があります。

<!-- So we use a relative import with `..` for the dependencies: -->
そこで、依存関係に`..`を使った相対インポートを使います：

```Python hl_lines="3" title="app/routers/items.py"
{!../../../docs_src/bigger_applications/app/routers/items.py!}
```

<!-- #### How relative imports work -->
#### 相対インポートのしくみ

!!! tip "豆知識"
    <!-- If you know perfectly how imports work, continue to the next section below. -->
    インポートの仕組みを完全に分かっているのであれば、次のセクションに進んでください。

<!-- A single dot `.`, like in: -->
ドット`.`1つ：

```Python
from .dependencies import get_token_header
```

<!-- would mean: -->
どういうことかというと：

<!--
* Starting in the same package that this module (the file `app/routers/items.py`) lives in (the directory `app/routers/`)...
* find the module `dependencies` (an imaginary file at `app/routers/dependencies.py`)...
* and from it, import the function `get_token_header`.
-->

* このモジュール(ファイル`app/routers/items.py`)は同じパッケージ(ディレクトリ`app/routers/`)から始めて...
* モジュール`dependencies`(`app/routers/dependencies.py`であろうファイル) を参照して...
* そして、そこから関数`get_token_header`をインポートしようとしてしまいます。

<!-- But that file doesn't exist, our dependencies are in a file at `app/dependencies.py`. -->
しかし、app/routers/dependencies.pyというファイルはありませんし、依存関係は`app/dependencies.py`ファイルに記載されています。

<!-- Remember how our app/file structure looks like: -->
アプリとファイルの構造を思い出してみましょう：

<img src="/img/tutorial/bigger-applications/package.svg">

---

<!-- The two dots `..`, like in: -->
ドット`..`2つ：

```Python
from ..dependencies import get_token_header
```

どういうことかというと:

<!--
* Starting in the same package that this module (the file `app/routers/items.py`) lives in (the directory `app/routers/`)...
* go to the parent package (the directory `app/`)...
* and in there, find the module `dependencies` (the file at `app/dependencies.py`)...
* and from it, import the function `get_token_header`.
-->

* このモジュール(ファイル`app/routers/items.py`)と同じパッケージ(ディレクトリ`app/routers/`)から始めて...
* 親パッケージ(`app/`ディレクトリ)に移動して...
* 移動先からモジュール`dependencies`(`app/dependencies.py`にあるファイル)を見つけて...
* そして、そこから関数`get_token_header`をインポートします。


正しく動きました!🎉

---

<!-- The same way, if we had used three dots `...`, like in: -->
同じように、`...`のように3つのドットを使ったとします：

```Python
from ...dependencies import get_token_header
```

<!-- that would mean: -->
どういうことかというと:

<!--
* Starting in the same package that this module (the file `app/routers/items.py`) lives in (the directory `app/routers/`)...
* go to the parent package (the directory `app/`)...
* then go to the parent of that package (there's no parent package, `app` is the top level 😱)...
* and in there, find the module `dependencies` (the file at `app/dependencies.py`)...
* and from it, import the function `get_token_header`.
-->

* このモジュール(ファイル`app/routers/items.py`)と同じパッケージ(ディレクトリ`app/routers/`)から始めて...
* 親パッケージ(`app/`ディレクトリ)に移動して...
* そして、そのパッケージの親パッケージ(親パッケージはなくて、`app`がトップレベルでした😱)に移動して...
* 移動先にあるであろうモジュール`dependencies`(`app/dependencies.py`としたファイル)を参照しようとして...
* そして、そこから関数`get_token_header`をインポートしようとします。

<!-- That would refer to some package above `app/`, with its own file `__init__.py`, etc. But we don't have that. So, that would throw an error in our example. 🚨 -->
`app/`の上にある、独自のファイル`__init__.py`などを持つパッケージを指すことになりますが、ここではそのパッケージがありません。そのため、この例ではエラーとなってしまいます🚨

<!-- But now you know how it works, so you can use relative imports in your own apps no matter how complex they are. 🤓 -->
しかし、これで相対インポートのしくみがわかったので、どんなに複雑なアプリでも相対インポートのしくみを使えるようになりましたね🤓

<!-- ### Add some custom `tags`, `responses`, and `dependencies` -->
### カスタムの`tags`、`responses`、`dependencies`の追加

<!-- We are not adding the prefix `/items` nor the `tags=["items"]` to each *path operation* because we added them to the `APIRouter`. -->
プレフィックス`/items`と`tags=["items"]`も`APIRouter`に追加したので、各*path operation*には追加していません。

<!-- But we can still add _more_ `tags` that will be applied to a specific *path operation*, and also some extra `responses` specific to that *path operation*: -->
しかし、特定の*path operation*に適用される`tags`や、その*path operation*に固有の`responses`を追加することができます：

```Python hl_lines="30-31" title="app/routers/items.py"
{!../../../docs_src/bigger_applications/app/routers/items.py!}
```

!!! tip "豆知識"
    <!-- This last path operation will have the combination of tags: `["items", "custom"]`. -->
    この最後のパスオペレーションは、タグの組み合わせを持つことになります：`["items", "custom"]`.

    <!-- And it will also have both responses in the documentation, one for `404` and one for `403`. -->
    また、ドキュメントには`404`と`403`の両方のレスポンスが記載されます。

<!-- ## The main `FastAPI` -->
## メインとなる `FastAPI`
<!-- Now, let's see the module at `app/main.py`. -->
では、`app/main.py`モジュールを見てみましょう。

<!-- Here's where you import and use the class `FastAPI`. -->
ここで`FastAPI`クラスをインポートします。

<!-- This will be the main file in your application that ties everything together. -->
これは、すべてを結びつけるアプリケーションのメインファイルとなります。

<!-- And as most of your logic will now live in its own specific module, the main file will be quite simple. -->
また、ロジックの大半は専用のモジュールに格納されるため、メインファイルは非常にシンプルになります。

<!-- ### Import `FastAPI` -->
### `FastAPI`のインポート
<!-- You import and create a `FastAPI` class as normally. -->
いつものように`FastAPI`クラスをインポートして作成します。

<!-- And we can even declare [global dependencies](dependencies/global-dependencies.md){.internal-link target=_blank} that will be combined with the dependencies for each `APIRouter`: -->
さらに、[グローバルな依存関係](dependencies/global-dependencies.md){.internal-link target=_blank}を宣言して、各`APIRouter`の依存関係と組み合わせることもできます：

```Python hl_lines="1  3  7" title="app/main.py"
{!../../../docs_src/bigger_applications/app/main.py!}
```

<!-- ### Import the `APIRouter` -->
### `APIRouter`のインポート

<!-- Now we import the other submodules that have `APIRouter`s: -->
次に、`APIRouter`を持つ他のサブモジュールをインポートします：

```Python hl_lines="4-5" title="app/main.py"
{!../../../docs_src/bigger_applications/app/main.py!}
```

<!-- As the files `app/routers/users.py` and `app/routers/items.py` are submodules that are part of the same Python package `app`, we can use a single dot `.` to import them using "relative imports". -->
`app/routers/users.py` と `app/routers/items.py`は同じPythonパッケージ`app`に含まれるサブモジュールなので、"相対インポート"を使ってドット`.`でインポートすることができます。

<!-- ### How the importing works -->
### インポートのしくみ

<!-- The section: -->
この:

```Python
from .routers import items, users
```

<!-- means: -->
は、

<!-- * Starting in the same package that this module (the file `app/main.py`) lives in (the directory `app/`)...
* look for the subpackage `routers` (the directory at `app/routers/`)...
* and from it, import the submodule `items` (the file at `app/routers/items.py`) and `users` (the file at `app/routers/users.py`)... -->

* このモジュール(ファイル`app/main.py`)と同じパッケージ(ディレクトリ`app/`)から始めまして...
* サブパッケージ`routers`(`app/routers/`ディレクトリ)を探しまして...
* そして、サブモジュール`items`(ファイル`app/routers/items.py`)と`users`(ファイル`app/routers/users.py`)をインポートします...

<!-- The module `items` will have a variable `router` (`items.router`). This is the same one we created in the file `app/routers/items.py`, it's an `APIRouter` object. -->
モジュール`items`は変数`router`(`items.router`)が定義されています。これは`app/routers/items.py`で作成したものと同じで、`APIRouter`オブジェクトとなります。

<!-- And then we do the same for the module `users`. -->
そして、モジュール`users`についても同じことをします。

<!-- We could also import them like: -->
以下のようにインポートすることもできます：

```Python
from app.routers import items, users
```

!!! info "情報"
    <!-- The first version is a "relative import": -->
    最初のバージョンは"相対インポート"です：

    ```Python
    from .routers import items, users
    ```

    <!-- The second version is an "absolute import": -->
    2つ目のバージョンは"相対インポート"です：

    ```Python
    from app.routers import items, users
    ```

    <!-- To learn more about Python Packages and Modules, read <a href="https://docs.python.org/3/tutorial/modules.html" class="external-link" target="_blank">the official Python documentation about Modules</a>. -->
    Pythonのパッケージとモジュールについてもっと学ぶには、<a href="https://docs.python.org/3/tutorial/modules.html" class="external-link" target="_blank">the official Python documentation about Modules</a>を読んでください。

<!-- ### Avoid name collisions -->
### 名前の衝突を避ける

<!-- We are importing the submodule `items` directly, instead of importing just its variable `router`. -->
`router`変数だけをインポートするのではなく、`items`サブモジュールを直接インポートしています。

<!-- This is because we also have another variable named `router` in the submodule `users`. -->
これは、サブモジュール`users`に`router`という別の変数があるからです。

<!-- If we had imported one after the other, like: -->
もし、以下のように次から次へとインポートしてしまうと：

```Python
from .routers.items import router
from .routers.users import router
```

<!-- the `router` from `users` would overwrite the one from `items` and we wouldn't be able to use them at the same time. -->
`users`の`router`が`items`のrouterを上書きしてしまうので、同時に使うことはできないのです。

<!-- So, to be able to use both of them in the same file, we import the submodules directly: -->
そこで、同じファイル内でその両方を使えるように、サブモジュールを直接インポートします：

```Python hl_lines="5" title="app/main.py"
{!../../../docs_src/bigger_applications/app/main.py!}
```

<!-- ### Include the `APIRouter`s for `users` and `items` -->
### `users`と`items`への`APIRouter`のインポート

<!-- Now, let's include the `router`s from the submodules `users` and `items`: -->
それでは、サブモジュール`users`と`items`の`router`を導入してみましょう：

```Python hl_lines="10-11" title="app/main.py"
{!../../../docs_src/bigger_applications/app/main.py!}
```

!!! info "情報"
    <!-- `users.router` contains the `APIRouter` inside of the file `app/routers/users.py`. -->
    `users.router`は`app/routers/users.py`ファイルの中に`APIRouter`定義しています。

    <!-- And `items.router` contains the `APIRouter` inside of the file `app/routers/items.py`. -->
    そして、`items.router`は`app/routers/items.py`ファイルの中に`APIRouter`を定義しています。

<!-- With `app.include_router()` we can add each `APIRouter` to the main `FastAPI` application. -->
`app.include_router()`を使えば、メインの`FastAPI`アプリケーションに`APIRouter`を追加することができます。

<!-- It will include all the routes from that router as part of it. -->
このルーターからのすべてのルートがその一部分として含まれます。

!!! note "技術詳細"
    <!-- It will actually internally create a *path operation* for each *path operation* that was declared in the `APIRouter`. -->
    実際には、`APIRouter`で宣言されたそれぞれの*path operation*に対して、内部的に*path operation*を作成しています。

    <!-- So, behind the scenes, it will actually work as if everything was the same single app. -->
    つまり、舞台裏では、あたかもすべてが同じひとつのアプリであるかのように動作するのです。

!!! check "チェック"
    <!-- You don't have to worry about performance when including routers. -->
    ルーターを含めれば、パフォーマンスを心配する必要はありません。

    This will take microseconds and will only happen at startup.
    これはマイクロ秒かかりますが、起動時のみのことです。

    So it won't affect performance. ⚡
    そのため、パフォーマンスには影響することはありません⚡

<!-- ### Include an `APIRouter` with a custom `prefix`, `tags`, `responses`, and `dependencies` -->
### カスタムの `prefix`、`tags`、`responses`、`dependencies` を持つ `APIRouter` の導入

<!-- Now, let's imagine your organization gave you the `app/internal/admin.py` file. -->
ところで、あなたの組織から`app/internal/admin.py`ファイルを渡されたとしましょう。

<!-- It contains an `APIRouter` with some admin *path operations* that your organization shares between several projects. -->
このファイルには、組織が複数のプロジェクト間で共有する、いくつか管理用の*path operation*を持つ`APIRouter`が含まれています。

<!-- For this example it will be super simple. But let's say that because it is shared with other projects in the organization, we cannot modify it and add a `prefix`, `dependencies`, `tags`, etc. directly to the `APIRouter`: -->
この例はとてもシンプルにしています。しかし、組織内の他のプロジェクトと共有しているため、`prefix`、`dependencies`、`tags`などを直接`APIRouter`に変更して追加することはできないとします：

```Python hl_lines="3" title="app/internal/admin.py"
{!../../../docs_src/bigger_applications/app/internal/admin.py!}
```

<!-- But we still want to set a custom `prefix` when including the `APIRouter` so that all its *path operations* start with `/admin`, we want to secure it with the `dependencies` we already have for this project, and we want to include `tags` and `responses`. -->

しかし、`APIRouter`を導入する際にカスタム`プレフィックス`を設定し、すべての*path operation*が`/admin`で始まるようにしたいとします。

<!-- We can declare all that without having to modify the original `APIRouter` by passing those parameters to `app.include_router()`: -->
これらのパラメータを`app.include_router()`に渡すことで、オリジナルの`APIRouter`を修正することなく、すべてを宣言することができます：

```Python hl_lines="14-17" title="app/main.py"
{!../../../docs_src/bigger_applications/app/main.py!}
```

<!-- That way, the original `APIRouter` will keep unmodified, so we can still share that same `app/internal/admin.py` file with other projects in the organization. -->
こうすると、オリジナルの`APIRouter`は変更されないので、同じ`app/internal/admin.py`ファイルを組織内の他のプロジェクトと共有することができます。

<!-- The result is that in our app, each of the *path operations* from the `admin` module will have: -->
その結果、私たちのアプリでは、`admin`モジュールのそれぞれの*path operation*が、以下のようになります：

<!-- * The prefix `/admin`.
* The tag `admin`.
* The dependency `get_token_header`.
* The response `418`. 🍵 -->

* プレフィックスは`/admin`.
* タグは`admin`.
* 依存関係は`get_token_header`.
* レスポンスは`418`.🍵

<!-- But that will only affect that `APIRouter` in our app, not in any other code that uses it.  -->
しかし、私たちののアプリ内の`APIRouter`に影響するだけで、それを使う他のコードには影響しません。

<!-- So, for example, other projects could use the same `APIRouter` with a different authentication method. -->
そのため、例えば他のプロジェクトが同じ`APIRouter`を異なる認証方法で使用することもできるようになります。

<!-- ### Include a *path operation* -->
### *path operation* を含む

<!-- We can also add *path operations* directly to the `FastAPI` app. -->
`FastAPI`アプリに直接*path operation*を追加することもできます。

<!-- Here we do it... just to show that we can 🤷: -->
ではやってみましょう🤷：

```Python hl_lines="21-23" title="app/main.py"
{!../../../docs_src/bigger_applications/app/main.py!}
```

<!-- and it will work correctly, together with all the other *path operations* added with `app.include_router()`. -->
`app.include_router()`で追加された他のすべての*path operation*と一緒に、正しく動作します。

!!! info "とても技術的な詳細"
    <!-- **Note**: this is a very technical detail that you probably can **just skip**. -->
    **注**: これは非常に技術的なことなので、おそらく**読み飛ばしていただいて問題ないです**。

    ---

    <!-- The `APIRouter`s are not "mounted", they are not isolated from the rest of the application. -->
    `APIRouter`は"マウント"されておらず、アプリケーションの他の部分から隔離されていません。

    <!-- This is because we want to include their *path operations* in the OpenAPI schema and the user interfaces. -->
    これは、OpenAPIスキーマとユーザインターフェースに*path operation*を含めたいという理由からです。

    <!-- As we cannot just isolate them and "mount" them independently of the rest, the *path operations* are "cloned" (re-created), not included directly. -->
    それらを切り離して、他の部分から独立して"マウント"することはできないので、*path operation*は直接導入されず、"クローン"(再作成)されます。

<!-- ## Check the automatic API docs -->
## 自動生成されたAPIのドキュメントの確認

<!-- Now, run `uvicorn`, using the module `app.main` and the variable `app`: -->
`app.main`モジュールと`app`変数を使って`uvicorn`を実行してみましょう：

<div class="termy">

```console
$ uvicorn app.main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

<!-- And open the docs at <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>. -->
APIドキュメントを開いてみましょう。<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>

<!-- You will see the automatic API docs, including the paths from all the submodules, using the correct paths (and prefixes) and the correct tags: -->
正しいパス(とプレフィックス)と正しいタグを使って、すべてのサブモジュールからのパスを含む自動生成されたAPIドキュメントが表示されます：

<img src="/img/tutorial/bigger-applications/image01.png">

<!-- ## Include the same router multiple times with different `prefix` -->
## 同じルーターを異なる`プレフィックス`で複数回導入

<!-- You can also use `.include_router()` multiple times with the *same* router using different prefixes. -->
`include_router()`は、*同じ*ルーターで異なるプレフィックスを使って複数回使うこともできます。

<!-- This could be useful, for example, to expose the same API under different prefixes, e.g. `/api/v1` and `/api/latest`. -->
例えば、`/api/v1`と`/api/latest`のように、同じAPIを異なるプレフィックスで公開するときに便利です。

<!-- This is an advanced usage that you might not really need, but it's there in case you do. -->
これは高度な使い方で、実際には必要ないかもしれませんが、万が一のために用意されています。

<!-- ## Include an `APIRouter` in another -->
## `APIRouter`を別のルーターへ導入

<!-- The same way you can include an `APIRouter` in a `FastAPI` application, you can include an `APIRouter` in another `APIRouter` using: -->
FastAPIアプリケーションに`APIRouter`を導入するのと同じように、`APIRouter`を別の`APIRouter`に導入することもできます：

```Python
router.include_router(other_router)
```

<!-- Make sure you do it before including `router` in the `FastAPI` app, so that the *path operations* from `other_router` are also included. -->
`other_router`からの*path operation*も含まれるように、`FastAPI`アプリに`router`を導入する前に行うことを確認してみましょう。
