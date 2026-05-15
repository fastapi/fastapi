# ヘッダーのパラメータ { #header-parameters }

ヘッダーのパラメータは、`Query`や`Path`、`Cookie`のパラメータを定義するのと同じように定義できます。

## `Header`をインポート { #import-header }

まず、`Header`をインポートします:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[3] *}

## `Header`のパラメータの宣言 { #declare-header-parameters }

次に、`Path`や`Query`、`Cookie`と同じ構造を用いてヘッダーのパラメータを宣言します。

デフォルト値に加えて、追加の検証パラメータや注釈パラメータをすべて定義できます:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[9] *}

/// note | 技術詳細

`Header`は`Path`や`Query`、`Cookie`の「姉妹」クラスです。また、同じ共通の`Param`クラスを継承しています。

しかし、`fastapi`から`Query`や`Path`、`Header`などをインポートする場合、それらは実際には特殊なクラスを返す関数であることを覚えておいてください。

///

/// info | 情報

ヘッダーを宣言するには、`Header`を使う必要があります。なぜなら、そうしないと、パラメータがクエリのパラメータとして解釈されてしまうからです。

///

## 自動変換 { #automatic-conversion }

`Header`は`Path`や`Query`、`Cookie`が提供する機能に加え、少しだけ追加の機能を持っています。

ほとんどの標準ヘッダーは、「マイナス記号」（`-`）としても知られる「ハイフン」文字で区切られています。

しかし、`user-agent`のような変数はPythonでは無効です。

そのため、デフォルトでは、`Header`はパラメータ名の文字をアンダースコア（`_`）からハイフン（`-`）に変換して、ヘッダーを抽出して文書化します。

また、HTTPヘッダは大文字小文字を区別しないので、Pythonの標準スタイル（別名「スネークケース」）で宣言することができます。

そのため、`User_Agent`などのように最初の文字を大文字にする必要はなく、通常のPythonコードと同じように`user_agent`を使用することができます。

もしなんらかの理由でアンダースコアからハイフンへの自動変換を無効にする必要がある場合は、`Header`のパラメータ`convert_underscores`を`False`に設定してください:

{* ../../docs_src/header_params/tutorial002_an_py310.py hl[10] *}

/// warning | 注意

`convert_underscores`を`False`に設定する前に、HTTPプロキシやサーバの中にはアンダースコアを含むヘッダーの使用を許可していないものがあることに注意してください。

///

## ヘッダーの重複 { #duplicate-headers }

受信したヘッダーが重複することがあります。つまり、同じヘッダーで複数の値を持つということです。

これらの場合、型宣言でリストを使用して定義することができます。

重複したヘッダーのすべての値をPythonの`list`として受け取ることができます。

例えば、複数回出現する可能性のある`X-Token`のヘッダを定義するには、以下のように書くことができます:

{* ../../docs_src/header_params/tutorial003_an_py310.py hl[9] *}

その*path operation*と通信する際に、次のように2つのHTTPヘッダーを送信する場合:

```
X-Token: foo
X-Token: bar
```

レスポンスは以下のようになります:

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## まとめ { #recap }

ヘッダーは`Header`で宣言し、`Query`や`Path`、`Cookie`と同じ共通パターンを使用します。

また、変数のアンダースコアを気にする必要はありません。**FastAPI** がそれらの変換をすべて取り持ってくれます。
