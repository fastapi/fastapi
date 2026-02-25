# クエリパラメータと文字列の検証 { #query-parameters-and-string-validations }

**FastAPI** ではパラメータの追加情報とバリデーションを宣言することができます。

以下のアプリケーションを例にしてみましょう:

{* ../../docs_src/query_params_str_validations/tutorial001_py310.py hl[7] *}

クエリパラメータ `q` は `str | None` 型で、`str` 型ですが `None` にもなり得ることを意味し、実際にデフォルト値は `None` なので、FastAPIはそれが必須ではないと理解します。

/// note | 備考

FastAPIは、 `q` はデフォルト値が `= None` であるため、必須ではないと理解します。

`str | None` を使うことで、エディターによるより良いサポートとエラー検出を可能にします。

///

## バリデーションの追加 { #additional-validation }

`q`はオプショナルですが、もし値が渡されてきた場合には、**長さが50文字を超えないこと**を強制してみましょう。

### `Query` と `Annotated` のインポート { #import-query-and-annotated }

そのために、まずは以下をインポートします:

* `fastapi` から `Query`
* `typing` から `Annotated`

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[1,3] *}

/// info | 情報

FastAPI はバージョン 0.95.0 で `Annotated` のサポートを追加し（推奨し始め）ました。

古いバージョンの場合、`Annotated` を使おうとするとエラーになります。

`Annotated` を使う前に、FastAPI のバージョンを少なくとも 0.95.1 にするために、[FastAPI のバージョンをアップグレード](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}してください。

///

## `q` パラメータの型で `Annotated` を使う { #use-annotated-in-the-type-for-the-q-parameter }

以前、[Python Types Intro](../python-types.md#type-hints-with-metadata-annotations){.internal-link target=_blank} で `Annotated` を使ってパラメータにメタデータを追加できると説明したことを覚えていますか？

いよいよ FastAPI で使うときです。 🚀

次の型アノテーションがありました:

```Python
q: str | None = None
```

これを `Annotated` で包んで、次のようにします:

```Python
q: Annotated[str | None] = None
```

どちらも同じ意味で、`q` は `str` または `None` になり得るパラメータで、デフォルトでは `None` です。

では、面白いところに進みましょう。 🎉

## `q` パラメータの `Annotated` に `Query` を追加する { #add-query-to-annotated-in-the-q-parameter }

追加情報（この場合は追加のバリデーション）を入れられる `Annotated` ができたので、`Annotated` の中に `Query` を追加し、パラメータ `max_length` を `50` に設定します:

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[9] *}

デフォルト値は引き続き `None` なので、このパラメータは依然としてオプショナルです。

しかし、`Annotated` の中に `Query(max_length=50)` を入れることで、この値に **追加のバリデーション** をしたい、最大 50 文字にしたい、と FastAPI に伝えています。 😎

/// tip | 豆知識

ここでは **クエリパラメータ** なので `Query()` を使っています。後で `Path()`、`Body()`、`Header()`、`Cookie()` など、`Query()` と同じ引数を受け取れるものも見ていきます。

///

FastAPI は次を行います:

* 最大長が 50 文字であることを確かめるようデータを **検証** する
* データが有効でないときに、クライアントに **明確なエラー** を表示する
* OpenAPI スキーマの *path operation* にパラメータを **ドキュメント化** する（その結果、**自動ドキュメント UI** に表示されます）

## 代替（古い方法）: デフォルト値としての `Query` { #alternative-old-query-as-the-default-value }

FastAPI の以前のバージョン（<dfn title="2023-03 より前">0.95.0</dfn> より前）では、パラメータのデフォルト値として `Query` を使う必要があり、`Annotated` の中に入れるのではありませんでした。これを使ったコードを見かける可能性が高いので、説明します。

/// tip | 豆知識

新しいコードでは、可能な限り上で説明したとおり `Annotated` を使ってください。複数の利点（後述）があり、欠点はありません。 🍰

///

関数パラメータのデフォルト値として `Query()` を使い、パラメータ `max_length` を 50 に設定する方法は次のとおりです:

{* ../../docs_src/query_params_str_validations/tutorial002_py310.py hl[7] *}

この場合（`Annotated` を使わない場合）、関数内のデフォルト値 `None` を `Query()` に置き換える必要があるため、`Query(default=None)` のパラメータでデフォルト値を設定する必要があります。これは（少なくとも FastAPI にとっては）そのデフォルト値を定義するのと同じ目的を果たします。

なので:

```Python
q: str | None = Query(default=None)
```

...はデフォルト値 `None` を持つオプショナルなパラメータになり、以下と同じです:


```Python
q: str | None = None
```

ただし `Query` のバージョンでは、クエリパラメータであることを明示的に宣言しています。

そして、さらに多くのパラメータを`Query`に渡すことができます。この場合、文字列に適用される、`max_length`パラメータを指定します。

```Python
q: str | None = Query(default=None, max_length=50)
```

これにより、データを検証し、データが有効でない場合は明確なエラーを表示し、OpenAPIスキーマの　*path operation* にパラメータを記載します。

### デフォルト値としての `Query` または `Annotated` 内の `Query` { #query-as-the-default-value-or-in-annotated }

`Annotated` の中で `Query` を使う場合、`Query` の `default` パラメータは使えないことに注意してください。

その代わりに、関数パラメータの実際のデフォルト値を使います。そうしないと整合性が取れなくなります。

例えば、これは許可されません:

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

...なぜなら、デフォルト値が `"rick"` なのか `"morty"` なのかが不明確だからです。

そのため、（できれば）次のようにします:

```Python
q: Annotated[str, Query()] = "rick"
```

...または、古いコードベースでは次のようなものが見つかるでしょう:

```Python
q: str = Query(default="rick")
```

### `Annotated` の利点 { #advantages-of-annotated }

関数パラメータのデフォルト値スタイルではなく、**`Annotated` を使うことが推奨** されます。複数の理由で **より良い** からです。 🤓

**関数パラメータ** の **デフォルト値** は **実際のデフォルト値** であり、Python 全般としてより直感的です。 😌

FastAPI なしで同じ関数を **別の場所** から **呼び出しても**、**期待どおりに動作** します。**必須** パラメータ（デフォルト値がない）があれば、**エディター** がエラーで知らせてくれますし、**Python** も必須パラメータを渡さずに実行すると文句を言います。

`Annotated` を使わずに **（古い）デフォルト値スタイル** を使う場合、FastAPI なしでその関数を **別の場所** で呼び出すとき、正しく動かすために関数へ引数を渡すことを **覚えておく** 必要があります。そうしないと値が期待と異なります（例えば `str` の代わりに `QueryInfo` か、それに類するものになります）。また、エディターも警告せず、Python もその関数の実行で文句を言いません。内部の処理がエラーになるときに初めて問題が出ます。

`Annotated` は複数のメタデータアノテーションを持てるので、<a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a> のような別ツールと同じ関数を使うこともできます。 🚀

## バリデーションをさらに追加する { #add-more-validations }

パラメータ`min_length`も追加することができます:

{* ../../docs_src/query_params_str_validations/tutorial003_an_py310.py hl[10] *}

## 正規表現の追加 { #add-regular-expressions }

パラメータが一致するべき <dfn title="正規表現、regex、regexp は、文字列に対する検索パターンを定義する文字の並びです。">正規表現</dfn> `pattern` を定義することができます:

{* ../../docs_src/query_params_str_validations/tutorial004_an_py310.py hl[11] *}

この特定の正規表現パターンは受け取ったパラメータの値をチェックします:

* `^`: は、これ以降の文字で始まり、これより以前には文字はありません。
* `fixedquery`: は、正確な`fixedquery`を持っています.
* `$`: で終わる場合、`fixedquery`以降には文字はありません.

もしこれらすべての **「正規表現」** のアイデアについて迷っていても、心配しないでください。多くの人にとって難しい話題です。正規表現を必要としなくても、まだ、多くのことができます。

これで、必要になったときにはいつでも **FastAPI** で使えることが分かりました。

## デフォルト値 { #default-values }

もちろん、`None` 以外のデフォルト値も使えます。

クエリパラメータ `q` の `min_length` を `3` とし、デフォルト値を `"fixedquery"` として宣言したいとします:

{* ../../docs_src/query_params_str_validations/tutorial005_an_py310.py hl[9] *}

/// note | 備考

`None` を含む任意の型のデフォルト値があると、パラメータはオプショナル（必須ではない）になります。

///

## 必須パラメータ { #required-parameters }

これ以上、バリデーションやメタデータを宣言する必要がない場合は、デフォルト値を宣言しないだけでクエリパラメータ `q` を必須にできます。以下のように:

```Python
q: str
```

以下の代わりに:

```Python
q: str | None = None
```

しかし今は、例えば次のように `Query` で宣言しています:

```Python
q: Annotated[str | None, Query(min_length=3)] = None
```

そのため、`Query` を使いながら値を必須として宣言したい場合は、単にデフォルト値を宣言しません:

{* ../../docs_src/query_params_str_validations/tutorial006_an_py310.py hl[9] *}

### 必須、`None` にできる { #required-can-be-none }

パラメータが `None` を受け付けるが、それでも必須である、と宣言できます。これにより、値が `None` であってもクライアントは値を送らなければならなくなります。

そのために、`None` が有効な型であることを宣言しつつ、単にデフォルト値を宣言しません:

{* ../../docs_src/query_params_str_validations/tutorial006c_an_py310.py hl[9] *}

## クエリパラメータのリスト / 複数の値 { #query-parameter-list-multiple-values }

クエリパラメータを明示的に `Query` で定義すると、値のリストを受け取るように宣言したり、言い換えると複数の値を受け取るように宣言したりすることもできます。

例えば、URL内に複数回出現するクエリパラメータ`q`を宣言するには以下のように書きます:

{* ../../docs_src/query_params_str_validations/tutorial011_an_py310.py hl[9] *}

そして、次のような URL なら:

```
http://localhost:8000/items/?q=foo&q=bar
```

*path operation function* 内の *function parameter* `q` で、複数の `q` *query parameters'* 値（`foo` と `bar`）を Python の `list` として受け取ります。

そのため、このURLのレスポンスは以下のようになります:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | 豆知識

上述の例のように、`list`型のクエリパラメータを宣言するには明示的に`Query`を使用する必要があります。そうしない場合、リクエストボディと解釈されます。

///

対話的APIドキュメントは複数の値を許可するために自動的に更新されます。

<img src="/img/tutorial/query-params-str-validations/image02.png">

### デフォルト値を持つ、クエリパラメータのリスト / 複数の値 { #query-parameter-list-multiple-values-with-defaults }

また、値が指定されていない場合はデフォルトの `list` を定義することもできます。

{* ../../docs_src/query_params_str_validations/tutorial012_an_py310.py hl[9] *}

以下にアクセスすると:

```
http://localhost:8000/items/
```

`q`のデフォルトは: `["foo", "bar"]` となり、レスポンスは以下のようになります:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### `list` だけを使う { #using-just-list }

`list[str]` の代わりに直接 `list` を使うこともできます:

{* ../../docs_src/query_params_str_validations/tutorial013_an_py310.py hl[9] *}

/// note | 備考

この場合、FastAPIはリストの内容をチェックしないことを覚えておいてください。

例えば`list[int]`はリストの内容が整数であるかどうかをチェックします(そして、文書化します)。しかし`list`だけではそうしません。

///

## より多くのメタデータを宣言する { #declare-more-metadata }

パラメータに関する情報をさらに追加することができます。

その情報は、生成されたOpenAPIに含まれ、ドキュメントのユーザーインターフェースや外部のツールで使用されます。

/// note | 備考

ツールによってOpenAPIのサポートのレベルが異なる可能性があることを覚えておいてください。

その中には、宣言されたすべての追加情報が表示されていないものもあるかもしれませんが、ほとんどの場合、不足している機能はすでに開発の計画がされています。

///

`title`を追加できます:

{* ../../docs_src/query_params_str_validations/tutorial007_an_py310.py hl[10] *}

`description`を追加できます:

{* ../../docs_src/query_params_str_validations/tutorial008_an_py310.py hl[14] *}

## エイリアスパラメータ { #alias-parameters }

パラメータに`item-query`を指定するとします.

以下のような感じです:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

しかし、`item-query`は有効なPythonの変数名ではありません。

最も近いのは`item_query`でしょう。

しかし、どうしても`item-query`と正確に一致している必要があるとします...

それならば、`alias`を宣言することができます。エイリアスはパラメータの値を見つけるのに使用されます:

{* ../../docs_src/query_params_str_validations/tutorial009_an_py310.py hl[9] *}

## パラメータを非推奨にする { #deprecating-parameters }

さて、このパラメータが気に入らなくなったとしましょう。

それを使っているクライアントがいるので、しばらくは残しておく必要がありますが、ドキュメントには<abbr title="obsolete, recommended not to use it - 廃止予定、使用は推奨されません">deprecated</abbr>と明記しておきたいです。

その場合、`Query`にパラメータ`deprecated=True`を渡します:

{* ../../docs_src/query_params_str_validations/tutorial010_an_py310.py hl[19] *}

ドキュメントは以下のようになります:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## OpenAPI からパラメータを除外する { #exclude-parameters-from-openapi }

生成される OpenAPI スキーマ（つまり自動ドキュメントシステム）からクエリパラメータを除外するには、`Query` のパラメータ `include_in_schema` を `False` に設定します:

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}

## カスタムバリデーション { #custom-validation }

上で示したパラメータではできない **カスタムバリデーション** が必要になる場合があります。

その場合、通常のバリデーション（例: 値が `str` であることの検証）の後に適用される **カスタムバリデータ関数** を使えます。

これを行うには、`Annotated` の中で <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-after-validator" class="external-link" target="_blank">Pydantic の `AfterValidator`</a> を使います。

/// tip | 豆知識

Pydantic には <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-before-validator" class="external-link" target="_blank">`BeforeValidator`</a> などもあります。 🤓

///

例えば、このカスタムバリデータは、<abbr title="International Standard Book Number - 国際標準図書番号">ISBN</abbr> の書籍番号なら item ID が `isbn-` で始まること、<abbr title="Internet Movie Database - インターネット・ムービー・データベース: 映画に関する情報を掲載する Web サイト">IMDB</abbr> の movie URL ID なら `imdb-` で始まることをチェックします:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py hl[5,16:19,24] *}

/// info | 情報

これは Pydantic バージョン 2 以上で利用できます。 😎

///

/// tip | 豆知識

データベースや別の API など、何らかの **外部コンポーネント** との通信が必要なタイプのバリデーションを行う必要がある場合は、代わりに **FastAPI Dependencies** を使うべきです。これについては後で学びます。

これらのカスタムバリデータは、リクエストで提供された **同じデータのみ** でチェックできるもの向けです。

///

### そのコードを理解する { #understand-that-code }

重要なのは、**`Annotated` の中で関数と一緒に `AfterValidator` を使うこと** だけです。この部分は飛ばしても構いません。 🤸

---

ただし、この具体的なコード例が気になっていて、まだ興味が続くなら、追加の詳細を示します。

#### `value.startswith()` を使う文字列 { #string-with-value-startswith }

気づきましたか？`value.startswith()` を使う文字列はタプルを受け取れ、そのタプル内の各値をチェックします:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[16:19] hl[17] *}

#### ランダムなアイテム { #a-random-item }

`data.items()` で、辞書の各アイテムのキーと値を含むタプルを持つ <dfn title="for ループで繰り返し処理できるもの（list、set など）">反復可能オブジェクト</dfn> を取得します。

この反復可能オブジェクトを `list(data.items())` で適切な `list` に変換します。

そして `random.choice()` でその `list` から **ランダムな値** を取得するので、`(id, name)` のタプルを得ます。これは `("imdb-tt0371724", "The Hitchhiker's Guide to the Galaxy")` のようになります。

次に、そのタプルの **2つの値を代入** して、変数 `id` と `name` に入れます。

つまり、ユーザーが item ID を提供しなかった場合でも、ランダムな提案を受け取ります。

...これを **単一のシンプルな1行** で行っています。 🤯 Python が好きになりませんか？ 🐍

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[22:30] hl[29] *}

## まとめ { #recap }

パラメータに追加のバリデーションとメタデータを宣言することができます。

一般的なバリデーションとメタデータ:

* `alias`
* `title`
* `description`
* `deprecated`

文字列に固有のバリデーション:

* `min_length`
* `max_length`
* `pattern`

`AfterValidator` を使ったカスタムバリデーション。

この例では、`str` の値のバリデーションを宣言する方法を見てきました。

数値のような他の型のバリデーションを宣言する方法は次の章を参照してください。
