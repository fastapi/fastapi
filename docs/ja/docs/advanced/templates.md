# テンプレート { #templates }

**FastAPI** では任意のテンプレートエンジンを使用できます。

Flask などでも使われている Jinja2 が一般的な選択肢です。

Starlette によって提供され、**FastAPI** アプリで直接使える、簡単に設定できるユーティリティがあります。

## 依存関係のインストール { #install-dependencies }

[仮想環境](../virtual-environments.md){.internal-link target=_blank} を作成して有効化し、`jinja2` をインストールします:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## `Jinja2Templates` の使用 { #using-jinja2templates }

* `Jinja2Templates` をインポートします。
* 後で再利用できる `templates` オブジェクトを作成します。
* テンプレートを返す path operation に `Request` パラメータを宣言します。
* 作成した `templates` を使って `TemplateResponse` をレンダリングして返します。テンプレート名、リクエストオブジェクト、Jinja2 テンプレート内で使用するキーと値のペアからなる "context" の辞書を渡します。

{* ../../docs_src/templates/tutorial001_py310.py hl[4,11,15:18] *}

/// note | 備考

FastAPI 0.108.0、Starlette 0.29.0 以前では、`name` は最初のパラメータでした。

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

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...渡した "context" の `dict` から取得した `id` が表示されます:

```Python
{"id": id}
```

例えば、ID が `42` の場合は次のようにレンダリングされます:

```html
Item ID: 42
```

### テンプレートの `url_for` の引数 { #template-url-for-arguments }

テンプレート内でも `url_for()` を使用できます。引数には、対応する path operation 関数で使われるのと同じ引数を取ります。

したがって、次の部分は:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...path operation 関数 `read_item(id=id)` が処理するのと同じ URL へのリンクを生成します。

例えば、ID が `42` の場合は次のようにレンダリングされます:

```html
<a href="/items/42">
```

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

より詳しい内容（テンプレートのテスト方法など）については、<a href="https://www.starlette.dev/templates/" class="external-link" target="_blank">Starlette のテンプレートに関するドキュメント</a>を参照してください。
