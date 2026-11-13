# フォームデータ { #form-data }

JSONの代わりにフォームフィールドを受け取る場合は、`Form`を使用します。

/// note | 備考

フォームを使うためには、まず[`python-multipart`](https://github.com/Kludex/python-multipart)をインストールします。

プロジェクトに追加します:

```console
$ uv add python-multipart
```

///

## `Form`のインポート { #import-form }

`fastapi`から`Form`をインポートします:

{* ../../docs_src/request_forms/tutorial001.py hl[3] *}

## `Form`のパラメータの定義 { #define-form-parameters }

`Body`や`Query`の場合と同じようにフォームパラメータを作成します:

{* ../../docs_src/request_forms/tutorial001.py hl[9] *}

例えば、OAuth2仕様が使用できる方法の１つ（「パスワードフロー」と呼ばれる）では、フォームフィールドとして`username`と`password`を送信する必要があります。

<dfn title="仕様">仕様</dfn>では、フィールドの名前が正確に`username`と`password`であることと、JSONではなくフォームフィールドとして送信されることを要求しています。

`Form`では`Body`（および`Query`や`Path`、`Cookie`）と同じ設定を宣言することができます。これには、バリデーション、例、エイリアス（例えば`username`の代わりに`user-name`）などが含まれます。

/// note | 備考

`Form`は`Body`を直接継承するクラスです。

///

/// tip | 豆知識

フォームのボディを宣言するには、明示的に`Form`を使用する必要があります。なぜなら、これを使わないと、パラメータはクエリパラメータやボディ（JSON）パラメータとして解釈されるからです。

///

## ブール型のフォームフィールド { #boolean-form-fields }

ブラウザはHTMLフォームを送信する際、チェックされていないチェックボックスを省略します。チェックされていない場合に`False`を受け取るには、デフォルト値を`False`にしたブール型のフォームパラメータを宣言します:

{* ../../docs_src/request_forms/tutorial002.py hl[9] *}

チェックされたチェックボックスはその値を送信し、デフォルトの値は`"on"`です。**FastAPI**は`"on"`を`True`として受け付けます。

## 「フォームフィールド」について { #about-form-fields }

HTMLフォーム（`<form></form>`）がサーバにデータを送信する方法は、通常、そのデータに「特別な」エンコーディングを使用していますが、これはJSONとは異なります。

**FastAPI** は、JSONの代わりにそのデータを適切な場所から読み込むようにします。

/// note | 技術詳細

フォームからのデータは通常、`application/x-www-form-urlencoded`の「media type」を使用してエンコードされます。

しかし、フォームがファイルを含む場合は、`multipart/form-data`としてエンコードされます。ファイルの扱いについては次の章で説明します。

`Form(media_type="multipart/form-data")`を使用すると、OpenAPIでマルチパートフォームを記述できます。フォームパラメータやモデルを組み合わせる場合は、１つのパラメータに設定するだけで十分です。

これらのエンコーディングやフォームフィールドの詳細については、[<abbr title="Mozilla Developer Network - Mozilla 開発者ネットワーク">MDN</abbr> の `POST` のウェブドキュメント](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST)を参照してください。

///

/// warning | 注意

*path operation*で複数の`Form`パラメータを宣言することができますが、JSONとして受け取ることを期待している`Body`フィールドを宣言することはできません。なぜなら、リクエストは`application/json`の代わりに`application/x-www-form-urlencoded`を使ってボディをエンコードするからです。

これは **FastAPI**の制限ではなく、HTTPプロトコルの一部です。

///

## まとめ { #recap }

フォームデータの入力パラメータを宣言するには、`Form`を使用します。
