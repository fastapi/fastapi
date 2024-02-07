# フォームデータ

JSONの代わりにフィールドを受け取る場合は、`Form`を使用します。

!!! info "情報"
    フォームを使うためには、まず<a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>をインストールします。

    たとえば、`pip install python-multipart`のように。

## `Form`のインポート

`fastapi`から`Form`をインポートします:

```Python hl_lines="1"
{!../../../docs_src/request_forms/tutorial001.py!}
```

## `Form`のパラメータの定義

`Body`や`Query`の場合と同じようにフォームパラメータを作成します:

```Python hl_lines="7"
{!../../../docs_src/request_forms/tutorial001.py!}
```

例えば、OAuth2仕様が使用できる方法の１つ（「パスワードフロー」と呼ばれる）では、フォームフィールドとして`username`と`password`を送信する必要があります。

<abbr title="仕様">仕様</abbr>では、フィールドの名前が`username`と`password`であることと、JSONではなくフォームフィールドとして送信されることを要求しています。

`Form`では`Body`（および`Query`や`Path`、`Cookie`）と同じメタデータとバリデーションを宣言することができます。

!!! info "情報"
    `Form`は`Body`を直接継承するクラスです。

!!! tip "豆知識"
    フォームのボディを宣言するには、明示的に`Form`を使用する必要があります。なぜなら、これを使わないと、パラメータはクエリパラメータやボディ（JSON）パラメータとして解釈されるからです。

## 「フォームフィールド」について

HTMLフォーム（`<form></form>`）がサーバにデータを送信する方法は、通常、そのデータに「特別な」エンコーディングを使用していますが、これはJSONとは異なります。

**FastAPI** は、JSONの代わりにそのデータを適切な場所から読み込むようにします。

!!! note "技術詳細"
    フォームからのデータは通常、`application/x-www-form-urlencoded`の「media type」を使用してエンコードされます。

    しかし、フォームがファイルを含む場合は、`multipart/form-data`としてエンコードされます。ファイルの扱いについては次の章で説明します。

    これらのエンコーディングやフォームフィールドの詳細については、<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr>の<code>POST</code></a>のウェブドキュメントを参照してください。

!!! warning "注意"
    *path operation*で複数の`Form`パラメータを宣言することができますが、JSONとして受け取ることを期待している`Body`フィールドを宣言することはできません。なぜなら、リクエストは`application/json`の代わりに`application/x-www-form-urlencoded`を使ってボディをエンコードするからです。

    これは **FastAPI**の制限ではなく、HTTPプロトコルの一部です。

## まとめ

フォームデータの入力パラメータを宣言するには、`Form`を使用する。
