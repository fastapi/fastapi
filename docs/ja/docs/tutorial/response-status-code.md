# レスポンスステータスコード { #response-status-code }

レスポンスモデルを指定するのと同じ方法で、レスポンスに使用されるHTTPステータスコードを以下の*path operations*のいずれかの`status_code`パラメータで宣言することもできます。

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* etc.

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

/// note | 備考

`status_code`は「デコレータ」メソッド（`get`、`post`など）のパラメータであることに注意してください。すべてのパラメータやボディのように、*path operation function*のものではありません。

///

`status_code`パラメータはHTTPステータスコードを含む数値を受け取ります。

/// info | 情報

`status_code`は代わりに、Pythonの<a href="https://docs.python.org/3/library/http.html#http.HTTPStatus" class="external-link" target="_blank">`http.HTTPStatus`</a>のように、`IntEnum`を受け取ることもできます。

///

これは:

* レスポンスでステータスコードを返します。
* OpenAPIスキーマ（およびユーザーインターフェース）に以下のように文書化します:

<img src="/img/tutorial/response-status-code/image01.png">

/// note | 備考

いくつかのレスポンスコード（次のセクションを参照）は、レスポンスにボディがないことを示しています。

FastAPIはこれを知っていて、レスポンスボディがないというOpenAPIドキュメントを生成します。

///

## HTTPステータスコードについて { #about-http-status-codes }

/// note | 備考

すでにHTTPステータスコードが何であるかを知っている場合は、次のセクションにスキップしてください。

///

HTTPでは、レスポンスの一部として3桁の数字のステータスコードを送信します。

これらのステータスコードは、それらを認識するために関連付けられた名前を持っていますが、重要な部分は番号です。

つまり:

* `100 - 199` は「情報」のためのものです。直接使うことはほとんどありません。これらのステータスコードを持つレスポンスはボディを持つことができません。
* **`200 - 299`** は「成功」のレスポンスのためのものです。これらは最も利用するであろうものです。
    * `200`はデフォルトのステータスコードで、すべてが「OK」であったことを意味します。
    * 別の例としては、`201`（Created）があります。これはデータベースに新しいレコードを作成した後によく使用されます。
    * 特殊なケースとして、`204`（No Content）があります。このレスポンスはクライアントに返すコンテンツがない場合に使用されるため、レスポンスはボディを持ってはいけません。
* **`300 - 399`** は「リダイレクト」のためのものです。これらのステータスコードを持つレスポンスは`304`（Not Modified）を除き、ボディを持つことも持たないこともできます。`304`はボディを持ってはいけません。
* **`400 - 499`** は「クライアントエラー」のレスポンスのためのものです。これらは、おそらく最も多用するであろう2番目のタイプです。
    * 例えば、`404`は「Not Found」レスポンスです。
    * クライアントからの一般的なエラーについては、`400`を使用することができます。
* `500 - 599` はサーバーエラーのためのものです。これらを直接使うことはほとんどありません。アプリケーションコードやサーバーのどこかで何か問題が発生した場合、これらのステータスコードのいずれかが自動的に返されます。

/// tip | 豆知識

それぞれのステータスコードとどのコードが何のためのコードなのかについて詳細は<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> documentation about HTTP status codes</a>を参照してください。

///

## 名前を覚えるための近道 { #shortcut-to-remember-the-names }

先ほどの例をもう一度見てみましょう:

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

`201`は「作成完了」のためのステータスコードです。

しかし、それぞれのコードの意味を暗記する必要はありません。

`fastapi.status`の便利な変数を利用することができます。

{* ../../docs_src/response_status_code/tutorial002_py310.py hl[1,6] *}

それらは単なる便利なものであり、同じ番号を保持しています。しかし、その方法ではエディタの自動補完を使用してそれらを見つけることができます。

<img src="/img/tutorial/response-status-code/image02.png">

/// note | 技術詳細

また、`from starlette import status`を使うこともできます。

**FastAPI** は、`開発者の利便性を考慮して、fastapi.status`と同じ`starlette.status`を提供しています。しかし、これはStarletteから直接提供されています。

///

## デフォルトの変更 { #changing-the-default }

後に、[高度なユーザーガイド](../advanced/response-change-status-code.md){.internal-link target=_blank}で、ここで宣言しているデフォルトとは異なるステータスコードを返す方法を見ていきます。
