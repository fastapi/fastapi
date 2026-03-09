# Path Operationの設定 { #path-operation-configuration }

*path operationデコレータ*を設定するためのパラメータがいくつかあります。

/// warning | 注意

これらのパラメータは*path operationデコレータ*に直接渡され、*path operation関数*に渡されないことに注意してください。

///

## レスポンスステータスコード { #response-status-code }

*path operation*のレスポンスで使用する（HTTP）`status_code`を定義することができます。

`404`のように`int`のコードを直接渡すことができます。

しかし、それぞれの番号コードが何のためのものか覚えていない場合は、`status`のショートカット定数を使用することができます:

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

そのステータスコードはレスポンスで使用され、OpenAPIスキーマに追加されます。

/// note | 技術詳細

`from starlette import status`を使用することもできます。

**FastAPI** は開発者の利便性を考慮して、`fastapi.status`と同じ`starlette.status`を提供しています。しかし、これはStarletteから直接提供されています。

///

## タグ { #tags }

`tags`パラメータを`str`の`list`（通常は１つの`str`）と一緒に渡すと、*path operation*にタグを追加できます:

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

これらはOpenAPIスキーマに追加され、自動ドキュメントのインターフェースで使用されます:

<img src="/img/tutorial/path-operation-configuration/image01.png">

### Enumを使ったタグ { #tags-with-enums }

大きなアプリケーションの場合、**複数のタグ**が蓄積されていき、関連する*path operations*に対して常に**同じタグ**を使っていることを確認したくなるかもしれません。

このような場合、タグを`Enum`に格納すると理にかなっています。

**FastAPI** は、プレーンな文字列の場合と同じ方法でそれをサポートしています:

{* ../../docs_src/path_operation_configuration/tutorial002b_py310.py hl[1,8:10,13,18] *}

## 概要と説明 { #summary-and-description }

`summary`と`description`を追加できます:

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[17:18] *}

## docstringを用いた説明 { #description-from-docstring }

説明文は長くて複数行におよぶ傾向があるので、関数<dfn title="関数内の最初の式（どの変数にも代入されない）として記述される、ドキュメント用の複数行の文字列">docstring</dfn>内に*path operation*の説明文を宣言できます。すると、**FastAPI** は説明文を読み込んでくれます。

docstringに<a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a>を記述すれば、正しく解釈されて表示されます。（docstringのインデントを考慮して）

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

これは対話的ドキュメントで使用されます:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## レスポンスの説明 { #response-description }

`response_description`パラメータでレスポンスの説明をすることができます。

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[18] *}

/// info | 情報

`response_description`は具体的にレスポンスを参照し、`description`は*path operation*全般を参照していることに注意してください。

///

/// check | 確認

OpenAPIは*path operation*ごとにレスポンスの説明を必要としています。

そのため、それを提供しない場合は、**FastAPI** が自動的に「成功のレスポンス」を生成します。

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## *path operation*を非推奨にする { #deprecate-a-path-operation }

*path operation*を<dfn title="非推奨、使用しないことを推奨">deprecated</dfn>としてマークする必要があるが、それを削除しない場合は、`deprecated`パラメータを渡します:

{* ../../docs_src/path_operation_configuration/tutorial006_py310.py hl[16] *}

対話的ドキュメントでは非推奨と明記されます:

<img src="/img/tutorial/path-operation-configuration/image04.png">

*path operations*が非推奨である場合とそうでない場合でどのように見えるかを確認してください:

<img src="/img/tutorial/path-operation-configuration/image05.png">

## まとめ { #recap }

*path operationデコレータ*にパラメータを渡すことで、*path operations*のメタデータを簡単に設定・追加することができます。
