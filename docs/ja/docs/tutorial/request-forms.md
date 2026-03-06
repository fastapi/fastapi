# フォームデータ { #form-data }

JSONの代わりにフィールドを受け取る場合は、`Form`を使用します。

/// info | 情報

フォームを使うためには、まず<a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>をインストールします。

必ず[仮想環境](../virtual-environments.md){.internal-link target=_blank}を作成して有効化してから、例えば次のようにインストールしてください:

```console
$ pip install python-multipart
```

///

## `Form`のインポート { #import-form }

`fastapi`から`Form`をインポートします:

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[3] *}

## `Form`のパラメータの定義 { #define-form-parameters }

`Body`や`Query`の場合と同じようにフォームパラメータを作成します:

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[9] *}

例えば、OAuth2仕様が使用できる方法の１つ（「パスワードフロー」と呼ばれる）では、フォームフィールドとして`username`と`password`を送信する必要があります。

<dfn title="仕様">仕様</dfn>では、フィールドの名前が正確に`username`と`password`であることと、JSONではなくフォームフィールドとして送信されることを要求しています。

`Form`では`Body`（および`Query`や`Path`、`Cookie`）と同じ設定を宣言することができます。これには、バリデーション、例、エイリアス（例えば`username`の代わりに`user-name`）などが含まれます。

/// info | 情報

`Form`は`Body`を直接継承するクラスです。

///

/// tip | 豆知識

フォームのボディを宣言するには、明示的に`Form`を使用する必要があります。なぜなら、これを使わないと、パラメータはクエリパラメータやボディ（JSON）パラメータとして解釈されるからです。

///

## 「フォームフィールド」について { #about-form-fields }

HTMLフォーム（`<form></form>`）がサーバにデータを送信する方法は、通常、そのデータに「特別な」エンコーディングを使用していますが、これはJSONとは異なります。

**FastAPI** は、JSONの代わりにそのデータを適切な場所から読み込むようにします。

/// note | 技術詳細

フォームからのデータは通常、`application/x-www-form-urlencoded`の「media type」を使用してエンコードされます。

しかし、フォームがファイルを含む場合は、`multipart/form-data`としてエンコードされます。ファイルの扱いについては次の章で説明します。

これらのエンコーディングやフォームフィールドの詳細については、<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network - Mozilla 開発者ネットワーク">MDN</abbr>の<code>POST</code></a>のウェブドキュメントを参照してください。

///

/// warning | 注意

*path operation*で複数の`Form`パラメータを宣言することができますが、JSONとして受け取ることを期待している`Body`フィールドを宣言することはできません。なぜなら、リクエストは`application/x-www-form-urlencoded`の代わりに`application/json`を使ってボディをエンコードするからです。

これは **FastAPI**の制限ではなく、HTTPプロトコルの一部です。

///

## まとめ { #recap }

フォームデータの入力パラメータを宣言するには、`Form`を使用する。
