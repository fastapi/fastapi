# Path Operationの設定

*path operationデコレータ*を設定するためのパラメータがいくつかあります。

/// warning | 注意

これらのパラメータは*path operation関数*ではなく、*path operationデコレータ*に直接渡されることに注意してください。

///

## レスポンスステータスコード

*path operation*のレスポンスで使用する（HTTP）`status_code`を定義することができます。

`404`のように`int`のコードを直接渡すことができます。

しかし、それぞれの番号コードが何のためのものか覚えていない場合は、`status`のショートカット定数を使用することができます:

{* ../../docs_src/path_operation_configuration/tutorial001.py hl[3,17] *}

そのステータスコードはレスポンスで使用され、OpenAPIスキーマに追加されます。

/// note | 技術詳細

また、`from starlette import status`を使用することもできます。

**FastAPI** は開発者の利便性を考慮して、`fastapi.status`と同じ`starlette.status`を提供しています。しかし、これはStarletteから直接提供されています。

///

## タグ

`tags`パラメータを`str`の`list`（通常は１つの`str`）と一緒に渡すと、*path operation*にタグを追加できます:

{* ../../docs_src/path_operation_configuration/tutorial002.py hl[17,22,27] *}

これらはOpenAPIスキーマに追加され、自動ドキュメントのインターフェースで使用されます:

<img src="https://fastapi.tiangolo.com/img/tutorial/path-operation-configuration/image01.png">

## 概要と説明

`summary`と`description`を追加できます:

{* ../../docs_src/path_operation_configuration/tutorial003.py hl[20:21] *}

## docstringを用いた説明

説明文は長くて複数行におよぶ傾向があるので、関数<abbr title="ドキュメントに使用される関数内の最初の式（変数に代入されていない）としての複数行の文字列">docstring</abbr>内に*path operation*の説明文を宣言できます。すると、**FastAPI** は説明文を読み込んでくれます。

docstringに<a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a>を記述すれば、正しく解釈されて表示されます。（docstringのインデントを考慮して）

{* ../../docs_src/path_operation_configuration/tutorial004.py hl[19:27] *}

これは対話的ドキュメントで使用されます:

<img src="https://fastapi.tiangolo.com/img/tutorial/path-operation-configuration/image02.png">

## レスポンスの説明

`response_description`パラメータでレスポンスの説明をすることができます。

{* ../../docs_src/path_operation_configuration/tutorial005.py hl[21] *}

/// info | 情報

`respnse_description`は具体的にレスポンスを参照し、`description`は*path operation*全般を参照していることに注意してください。

///

/// check | 確認

OpenAPIは*path operation*ごとにレスポンスの説明を必要としています。

そのため、それを提供しない場合は、**FastAPI** が自動的に「成功のレスポンス」を生成します。

///

<img src="https://fastapi.tiangolo.com/img/tutorial/path-operation-configuration/image03.png">

## 非推奨の*path operation*

*path operation*を<abbr title="非推奨、使わない方がよい">deprecated</abbr>としてマークする必要があるが、それを削除しない場合は、`deprecated`パラメータを渡します:

{* ../../docs_src/path_operation_configuration/tutorial006.py hl[16] *}

対話的ドキュメントでは非推奨と明記されます:

<img src="https://fastapi.tiangolo.com/img/tutorial/path-operation-configuration/image04.png">

*path operations*が非推奨である場合とそうでない場合でどのように見えるかを確認してください:

<img src="https://fastapi.tiangolo.com/img/tutorial/path-operation-configuration/image05.png">

## まとめ

*path operationデコレータ*にパラメータを渡すことで、*path operations*のメタデータを簡単に設定・追加することができます。
