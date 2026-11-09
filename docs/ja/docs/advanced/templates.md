---
render_macros: false
---

# テンプレート { #templates }

**FastAPI** では任意のテンプレートエンジンを使用できます。

Flask などでも使われている Jinja2 が一般的な選択肢です。

Starlette によって提供され、**FastAPI** アプリで直接使える、簡単に設定できるユーティリティがあります。

## 依存関係のインストール { #install-dependencies }

プロジェクトに `jinja2` を追加します:

<div class="termy">

```console
$ uv add jinja2

---> 100%
```

</div>

## `Jinja2Templates` の使用 { #using-jinja2templates }

* `Jinja2Templates` をインポートします。
* 後で再利用できる `templates` オブジェクトを作成します。
* テンプレートを返す *path operation* に `Request` パラメータを宣言します。
* 作成した `templates` を使って `TemplateResponse` をレンダリングして返します。テンプレート名、リクエストオブジェクト、Jinja2 テンプレート内で使用するキーと値のペアからなる「context」の辞書を渡します。

{* ../../docs_src/templates/tutorial001.py hl[4,11,15:18] *}

/// note | 備考

FastAPI 0.108.0、Starlette 0.29.0 より前では、`name` は最初のパラメータでした。

またそれ以前のバージョンでは、`request` オブジェクトは Jinja2 用のコンテキスト内のキーと値のペアの一部として渡されていました。

///

/// tip | 豆知識

`response_class=HTMLResponse` を宣言すると、ドキュメント UI がレスポンスが HTML であることを認識できます。

///

/// note | 技術詳細

`from starlette.templating import Jinja2Templates` を使うこともできます。

**FastAPI** は、開発者であるあなたの利便性のために、`starlette.templating` と同じものを `fastapi.templating` として提供しています。しかし、利用可能なレスポンスのほとんどは Starlette から直接提供されています。`Request` や `StaticFiles` も同様です。

///

## テンプレートの作成 { #writing-templates }

例えば、`templates/item.html` に次のようなテンプレートを書きます:

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### テンプレートのコンテキスト値 { #template-context-values }

次のような HTML 内で:

```jinja
Item ID: {{ id }}
```

...渡した「context」の `dict` から取得した `id` が表示されます:

```Python
{"id": id}
```

例えば、ID が `42` の場合は次のようにレンダリングされます:

```html
Item ID: 42
```

### テンプレートの `url_for` の引数 { #template-url-for-arguments }

テンプレート内でも `url_for()` を使用できます。引数には、対応する *path operation 関数* で使われるのと同じ引数を取ります。

したがって、次の部分は:

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

...*path operation 関数* `read_item(id=id)` が処理するのと同じ URL へのリンクを生成します。

`url_for()` は、現在のリクエストに基づいて、スキームとホストを含む絶対 URL を返します。

例えば、アプリケーションが `https://example.com` で配信されていて、ID が `42` の場合は次のようにレンダリングされます:

```html
<a href="https://example.com/items/42">
```

### テンプレート内の URL パス { #url-paths-in-templates }

同じサイトへのリンクには、`.path` 属性を使って URL パスのみを取得できます。例えば、`templates/item_path.html` では次のようにします:

```jinja hl_lines="4 7"
{!../../docs_src/templates/templates/item_path.html!}
```

テンプレート名を `TemplateResponse` に渡します:

{* ../../docs_src/templates/tutorial002.py ln[14:18] hl[17] *}

同じ例では、アイテムへのリンクは次のようにレンダリングされます:

```html
<a href="/items/42">
```

先頭の `/` により、このパスは現在のサイトのルートからの相対パスになります。

`.path` 属性には、スキーム、ホスト、クエリパラメータ、フラグメントは含まれません。別のホストへのリンクには完全な URL を使用してください。

/// tip | 豆知識

アプリケーションがプロキシの背後にある場合は、[プロキシの背後](behind-a-proxy.md)の説明に従って、転送ヘッダーと `root_path` を設定してください。

///

## テンプレートと静的ファイル { #templates-and-static-files }

テンプレート内で `url_for()` を使用し、例えば `name="static"` でマウントした `StaticFiles` に対して利用できます。

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

この例では、`static/styles.css` の CSS ファイルにリンクします:

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

また、`StaticFiles` を使用しているため、その CSS ファイルは **FastAPI** アプリケーションから URL `/static/styles.css` で自動的に配信されます。

## さらに詳しく { #more-details }

より詳しい内容（テンプレートのテスト方法など）については、[Starlette のテンプレートに関するドキュメント](https://starlette.dev/templates/)を参照してください。
