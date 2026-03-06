# クッキーのパラメータ { #cookie-parameters }

クッキーのパラメータは、`Query`や`Path`のパラメータを定義するのと同じ方法で定義できます。

## `Cookie`をインポート { #import-cookie }

まず、`Cookie`をインポートします:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## `Cookie`のパラメータを宣言 { #declare-cookie-parameters }

次に、`Path`や`Query`と同じ構造を使ってクッキーのパラメータを宣言します。

最初の値がデフォルト値で、追加の検証パラメータや注釈パラメータをすべて渡すことができます:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | 技術詳細

`Cookie`は`Path`と`Query`の「姉妹」クラスです。また、同じ共通の`Param`クラスを継承しています。

しかし、`fastapi`から`Query`や`Path`、`Cookie`などをインポートする場合、それらは実際には特殊なクラスを返す関数であることを覚えておいてください。

///

/// info | 情報

クッキーを宣言するには、`Cookie`を使う必要があります。なぜなら、そうしないとパラメータがクエリのパラメータとして解釈されてしまうからです。

///

/// info | 情報

**ブラウザがクッキーを**特殊な方法で裏側で扱うため、**JavaScript** から簡単には触れられないことを念頭に置いてください。

`/docs` の **API docs UI** に移動すると、*path operation* のクッキーに関する **documentation** を確認できます。

しかし、データを **入力** して「Execute」をクリックしても、docs UI は **JavaScript** で動作するためクッキーは送信されず、値を何も書かなかったかのような **error** メッセージが表示されます。

///

## まとめ { #recap }

クッキーは`Cookie`を使って宣言し、`Query`や`Path`と同じ共通のパターンを使用する。
