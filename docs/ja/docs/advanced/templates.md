# テンプレート

お好きなテンプレートエンジンを**FastAPI**と使うことができます。

よく使われるものは Flask などで使われているJinja2です。

Starletteにより提供されている簡単に設定できるユーティリティーがあり、**FastAPI**アプリケーションで直接使用することができます。

## 依存関係のインストール

`jinja2`のインストール:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## `Jinja2Templates`の使用

* `Jinja2Templates`をインポートします。
* あとで再利用可能な`templates`オブジェクトを作ります。
* テンプレートを返す*パスオペレーション*内で`Request`パラメータを宣言します。
* 作成した`templates`を使って`TemplateResponse`をレンダリングし、Jinja2の"context"のキーと値のペアの一つとして`request`を渡します。

```Python hl_lines="4  11  15-16"
{!../../../docs_src/templates/tutorial001.py!}
```

!!! note
`request`をJinja2のコンテキストのキーと値ののペアとして渡さなければいけないことに注意してください。そのため、*パスオペレーション*の中でもそれを宣言しなければなりません。

!!! tip
`response_class=HTMLResponse`を宣言することで、docs UIはレスポンスがHTML形式であると知ることができます。

!!! note "Technical Details"
また、`from starlette.templating import Jinja2Templates`も使用できます。

    **FastAPI** provides the same `starlette.templating` as `fastapi.templating` just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with `Request` and `StaticFiles`.

## テンプレートを書く

次にテンプレートを`templates/item.html`に以下のように書きます。

```jinja hl_lines="7"
{!../../../docs_src/templates/templates/item.html!}
```

渡した`dict`"context"から得られた`id`が表示されます。

```Python
{"request": request, "id": id}
```

## テンプレートと静的ファイル

また、`url_for()`テンプレート内で使用することができます。例えば、マウントした`StaticFiles`とともに使用できます。

```jinja hl_lines="4"
{!../../../docs_src/templates/templates/item.html!}
```

この例では、`static/styles.css`にある以下のようなCSSファイルにリンクすることになります。

```CSS hl_lines="4"
{!../../../docs_src/templates/static/styles.css!}
```

また、`StaticFiles`を使用しているので、CSS fileは**FastAPI**アプリケーションによって自動的に`/static/styles.css`のURLで提供されます。

## More details

テンプレートのテストの方法などの詳細については、<a href="https://www.starlette.io/templates/" class="external-link" target="_blank">Starlette's docs on templates</a>をご覧ください。
