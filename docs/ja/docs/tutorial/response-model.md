# レスポンスモデル - 戻り値の型 { #response-model-return-type }

*path operation 関数*の**戻り値の型**にアノテーションを付けることで、レスポンスに使用される型を宣言できます。

関数**パラメータ**の入力データと同じように **型アノテーション** を使用できます。Pydanticモデル、リスト、辞書、整数や真偽値などのスカラー値を使用できます。

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

FastAPIはこの戻り値の型を使って以下を行います:

* 返却データを**検証**します。
    * データが不正（例: フィールドが欠けている）であれば、それは*あなた*のアプリコードが壊れていて、返すべきものを返していないことを意味し、不正なデータを返す代わりにサーバーエラーを返します。これにより、あなたとクライアントは、期待されるデータとデータ形状を受け取れることを確実にできます。
* OpenAPIの *path operation* に、レスポンス用の **JSON Schema** を追加します。
    * これは**自動ドキュメント**で使用されます。
    * 自動クライアントコード生成ツールでも使用されます。

しかし、最も重要なのは:

* 戻り値の型で定義された内容に合わせて、出力データを**制限しフィルタリング**します。
    * これは**セキュリティ**の観点で特に重要です。以下で詳しく見ていきます。

## `response_model`パラメータ { #response-model-parameter }

型が宣言している内容とまったく同じではないデータを返す必要がある、またはそうしたいケースがあります。

例えば、**辞書を返す**、またはデータベースオブジェクトを返したいが、**Pydanticモデルとして宣言**したい場合があります。こうすることで、Pydanticモデルが返したオブジェクト（例: 辞書やデータベースオブジェクト）のドキュメント化、バリデーションなどをすべて行ってくれます。

戻り値の型アノテーションを追加すると、ツールやエディタが（正しく）エラーとして、関数が宣言した型（例: Pydanticモデル）とは異なる型（例: dict）を返していると警告します。

そのような場合、戻り値の型の代わりに、*path operation デコレータ*のパラメータ `response_model` を使用できます。

`response_model`パラメータは、いずれの *path operation* でも使用できます:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* など。

{* ../../docs_src/response_model/tutorial001_py310.py hl[17,22,24:27] *}

/// note | 備考

`response_model`は「デコレータ」メソッド（`get`、`post`など）のパラメータです。関数のパラメータやボディなどとは違い、*path operation 関数*のパラメータではありません。

///

`response_model`は、Pydanticモデルのフィールドで宣言するのと同じ型を受け取ります。そのため、Pydanticモデルにもできますし、例えば `List[Item]` のように、Pydanticモデルの `list` にもできます。

FastAPIはこの `response_model` を使って、データのドキュメント化や検証などを行い、さらに出力データを型宣言に合わせて**変換・フィルタリング**します。

/// tip | 豆知識

エディタやmypyなどで厳密な型チェックをしている場合、関数の戻り値の型を `Any` として宣言できます。

そうすると、意図的に何でも返していることをエディタに伝えられます。それでもFastAPIは `response_model` を使って、データのドキュメント化、検証、フィルタリングなどを行います。

///

### `response_model`の優先順位 { #response-model-priority }

戻り値の型と `response_model` の両方を宣言した場合、`response_model` が優先され、FastAPIで使用されます。

これにより、レスポンスモデルとは異なる型を返している場合でも、エディタやmypyなどのツールで使用するために関数へ正しい型アノテーションを追加できます。それでもFastAPIは `response_model` を使用してデータの検証やドキュメント化などを実行できます。

また `response_model=None` を使用して、その*path operation*のレスポンスモデル生成を無効化することもできます。これは、Pydanticのフィールドとして有効ではないものに対して型アノテーションを追加する場合に必要になることがあります。以下のセクションのいずれかで例を示します。

## 同じ入力データの返却 { #return-the-same-input-data }

ここでは `UserIn` モデルを宣言しています。これには平文のパスワードが含まれます:

{* ../../docs_src/response_model/tutorial002_py310.py hl[7,9] *}

/// info | 情報

`EmailStr` を使用するには、最初に <a href="https://github.com/JoshData/python-email-validator" class="external-link" target="_blank">`email-validator`</a> をインストールしてください。

[仮想環境](../virtual-environments.md){.internal-link target=_blank}を作成して有効化してから、例えば次のようにインストールしてください:

```console
$ pip install email-validator
```

または次のようにします:

```console
$ pip install "pydantic[email]"
```

///

そして、このモデルを使用して入力を宣言し、同じモデルを使って出力を宣言しています:

{* ../../docs_src/response_model/tutorial002_py310.py hl[16] *}

これで、ブラウザがパスワードを使ってユーザーを作成する際に、APIがレスポンスで同じパスワードを返すようになりました。

この場合、同じユーザーがパスワードを送信しているので問題ないかもしれません。

しかし、同じモデルを別の*path operation*に使用すると、すべてのクライアントにユーザーのパスワードを送信してしまう可能性があります。

/// danger | 警告

すべての注意点を理解していて、自分が何をしているか分かっている場合を除き、ユーザーの平文のパスワードを保存したり、このようにレスポンスで送信したりしないでください。

///

## 出力モデルの追加 { #add-an-output-model }

代わりに、平文のパスワードを持つ入力モデルと、パスワードを持たない出力モデルを作成できます:

{* ../../docs_src/response_model/tutorial003_py310.py hl[9,11,16] *}

ここでは、*path operation 関数*がパスワードを含む同じ入力ユーザーを返しているにもかかわらず:

{* ../../docs_src/response_model/tutorial003_py310.py hl[24] *}

...`response_model`を、パスワードを含まない `UserOut` モデルとして宣言しました:

{* ../../docs_src/response_model/tutorial003_py310.py hl[22] *}

そのため、**FastAPI** は出力モデルで宣言されていないすべてのデータをフィルタリングしてくれます（Pydanticを使用）。

### `response_model`または戻り値の型 { #response-model-or-return-type }

このケースでは2つのモデルが異なるため、関数の戻り値の型を `UserOut` としてアノテーションすると、エディタやツールは、異なるクラスなので不正な型を返していると警告します。

そのため、この例では `response_model` パラメータで宣言する必要があります。

...しかし、これを解決する方法を以下で確認しましょう。

## 戻り値の型とデータフィルタリング { #return-type-and-data-filtering }

前の例から続けます。**関数に1つの型をアノテーション**したい一方で、関数からは実際には**より多くのデータ**を含むものを返せるようにしたいとします。

FastAPIにはレスポンスモデルを使用してデータを**フィルタリング**し続けてほしいです。つまり、関数がより多くのデータを返しても、レスポンスにはレスポンスモデルで宣言されたフィールドのみが含まれます。

前の例ではクラスが異なるため `response_model` パラメータを使う必要がありました。しかしそれは、エディタやツールによる関数の戻り値の型チェックのサポートを受けられないことも意味します。

しかし、このようなことが必要になる多くのケースでは、この例のようにモデルでデータの一部を**フィルタ/削除**したいだけです。

そのような場合、クラスと継承を利用して関数の**型アノテーション**を活用し、エディタやツールのサポートを改善しつつ、FastAPIの**データフィルタリング**も得られます。

{* ../../docs_src/response_model/tutorial003_01_py310.py hl[7:10,13:14,18] *}

これにより、このコードは型として正しいためエディタやmypyからのツール支援を得られますし、FastAPIによるデータフィルタリングも得られます。

これはどのように動作するのでしょうか？確認してみましょう。🤓

### 型アノテーションとツール支援 { #type-annotations-and-tooling }

まず、エディタ、mypy、その他のツールがこれをどう見るかを見てみます。

`BaseUser` には基本フィールドがあります。次に `UserIn` が `BaseUser` を継承して `password` フィールドを追加するため、両方のモデルのフィールドがすべて含まれます。

関数の戻り値の型を `BaseUser` としてアノテーションしますが、実際には `UserIn` インスタンスを返しています。

エディタやmypyなどのツールはこれに文句を言いません。typingの観点では、`UserIn` は `BaseUser` のサブクラスであり、期待されるものが `BaseUser` であれば `UserIn` は*有効*な型だからです。

### FastAPIのデータフィルタリング { #fastapi-data-filtering }

一方FastAPIでは、戻り値の型を見て、返す内容にその型で宣言されたフィールド**だけ**が含まれることを確認します。

FastAPIは、返却データのフィルタリングにクラス継承の同じルールが使われてしまわないようにするため、内部でPydanticを使っていくつかの処理を行っています。そうでないと、期待以上に多くのデータを返してしまう可能性があります。

この方法で、**ツール支援**付きの型アノテーションと**データフィルタリング**の両方という、いいとこ取りができます。

## ドキュメントを見る { #see-it-in-the-docs }

自動ドキュメントを見ると、入力モデルと出力モデルがそれぞれ独自のJSON Schemaを持っていることが確認できます:

<img src="/img/tutorial/response-model/image01.png">

そして、両方のモデルは対話型のAPIドキュメントに使用されます:

<img src="/img/tutorial/response-model/image02.png">

## その他の戻り値の型アノテーション { #other-return-type-annotations }

Pydanticフィールドとして有効ではないものを返し、ツール（エディタやmypyなど）が提供するサポートを得るためだけに、関数でそれをアノテーションするケースがあるかもしれません。

### レスポンスを直接返す { #return-a-response-directly }

最も一般的なケースは、[高度なドキュメントで後述する「Responseを直接返す」](../advanced/response-directly.md){.internal-link target=_blank}場合です。

{* ../../docs_src/response_model/tutorial003_02_py310.py hl[8,10:11] *}

このシンプルなケースは、戻り値の型アノテーションが `Response` のクラス（またはサブクラス）であるため、FastAPIが自動的に処理します。

また `RedirectResponse` と `JSONResponse` の両方は `Response` のサブクラスなので、ツールも型アノテーションが正しいとして問題にしません。

### `Response`のサブクラスをアノテーションする { #annotate-a-response-subclass }

型アノテーションで `Response` のサブクラスを使うこともできます:

{* ../../docs_src/response_model/tutorial003_03_py310.py hl[8:9] *}

これは `RedirectResponse` が `Response` のサブクラスであり、FastAPIがこのシンプルなケースを自動処理するため、同様に動作します。

### 無効な戻り値の型アノテーション { #invalid-return-type-annotations }

しかし、Pydantic型として有効ではない別の任意のオブジェクト（例: データベースオブジェクト）を返し、関数でそのようにアノテーションすると、FastAPIはその型アノテーションからPydanticレスポンスモデルを作成しようとして失敗します。

同様に、<dfn title="複数の型のユニオンは「これらの型のいずれか」を意味します。">ユニオン</dfn>のように、複数の型のうち1つ以上がPydantic型として有効でないものを含む場合も起こります。例えば次は失敗します 💥:

{* ../../docs_src/response_model/tutorial003_04_py310.py hl[8] *}

...これは、型アノテーションがPydantic型ではなく、単一の `Response` クラス（またはサブクラス）でもないために失敗します。`Response` と `dict` の間のunion（どちらか）になっているからです。

### レスポンスモデルを無効化する { #disable-response-model }

上の例を続けると、FastAPIが実行するデフォルトのデータ検証、ドキュメント化、フィルタリングなどを行いたくないこともあるでしょう。

しかし、エディタや型チェッカー（例: mypy）などのツール支援を得るために、関数の戻り値の型アノテーションは残したいかもしれません。

その場合、`response_model=None` を設定することでレスポンスモデルの生成を無効にできます:

{* ../../docs_src/response_model/tutorial003_05_py310.py hl[7] *}

これによりFastAPIはレスポンスモデル生成をスキップし、FastAPIアプリケーションに影響させずに必要な戻り値の型アノテーションを付けられます。🤓

## レスポンスモデルのエンコーディングパラメータ { #response-model-encoding-parameters }

レスポンスモデルには次のようにデフォルト値を設定できます:

{* ../../docs_src/response_model/tutorial004_py310.py hl[9,11:12] *}

* `description: Union[str, None] = None`（またはPython 3.10では `str | None = None`）はデフォルトが `None` です。
* `tax: float = 10.5` はデフォルトが `10.5` です。
* `tags: List[str] = []` はデフォルトが空のリスト `[]` です。

ただし、それらが実際には保存されていない場合、結果から省略したいことがあります。

例えば、NoSQLデータベースに多くのオプション属性を持つモデルがあるが、デフォルト値でいっぱいの非常に長いJSONレスポンスを送信したくない場合です。

### `response_model_exclude_unset`パラメータの使用 { #use-the-response-model-exclude-unset-parameter }

*path operation デコレータ*のパラメータ `response_model_exclude_unset=True` を設定できます:

{* ../../docs_src/response_model/tutorial004_py310.py hl[22] *}

そうすると、デフォルト値はレスポンスに含まれず、実際に設定された値のみが含まれます。

そのため、ID `foo` のitemに対してその *path operation* へリクエストを送ると、レスポンスは以下のようになります（デフォルト値を含まない）:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// info | 情報

以下も使用できます:

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

`exclude_defaults` と `exclude_none` については、<a href="https://docs.pydantic.dev/1.10/usage/exporting_models/#modeldict" class="external-link" target="_blank">Pydanticのドキュメント</a>で説明されている通りです。

///

#### デフォルト値を持つフィールドに値があるデータ { #data-with-values-for-fields-with-defaults }

しかし、ID `bar` のitemのように、デフォルト値が設定されているモデルのフィールドに値が設定されている場合:

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

それらはレスポンスに含まれます。

#### デフォルト値と同じ値を持つデータ { #data-with-the-same-values-as-the-defaults }

ID `baz` のitemのようにデフォルト値と同じ値を持つデータの場合:

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

FastAPIは十分に賢いので（実際には、Pydanticが十分に賢い）、`description` や `tax`、`tags` がデフォルト値と同じ値であっても、明示的に設定された（デフォルトから取得されたのではない）ことを理解します。

そのため、それらはJSONレスポンスに含まれます。

/// tip | 豆知識

デフォルト値は `None` だけではないことに注意してください。

リスト（`[]`）や `10.5` の `float` などでも構いません。

///

### `response_model_include`と`response_model_exclude` { #response-model-include-and-response-model-exclude }

*path operation デコレータ*のパラメータ `response_model_include` と `response_model_exclude` も使用できます。

これらは、含める（残りを省略する）または除外する（残りを含む）属性名を持つ `str` の `set` を受け取ります。

これは、Pydanticモデルが1つしかなく、出力からいくつかのデータを削除したい場合のクイックショートカットとして使用できます。

/// tip | 豆知識

それでも、これらのパラメータではなく、上で示したアイデアのように複数のクラスを使うことが推奨されます。

これは、`response_model_include` や `response_model_exclude` を使っていくつかの属性を省略しても、アプリのOpenAPI（とドキュメント）で生成されるJSON Schemaが完全なモデルのままになるためです。

同様に動作する `response_model_by_alias` にも当てはまります。

///

{* ../../docs_src/response_model/tutorial005_py310.py hl[29,35] *}

/// tip | 豆知識

`{"name", "description"}` の構文は、それら2つの値を持つ `set` を作成します。

これは `set(["name", "description"])` と同等です。

///

#### `set`の代わりに`list`を使用する { #using-lists-instead-of-sets }

もし `set` を使用することを忘れて、代わりに `list` や `tuple` を使用しても、FastAPIはそれを `set` に変換して正しく動作します:

{* ../../docs_src/response_model/tutorial006_py310.py hl[29,35] *}

## まとめ { #recap }

*path operation デコレータ*のパラメータ `response_model` を使用してレスポンスモデルを定義し、とくにプライベートデータがフィルタリングされることを保証します。

明示的に設定された値のみを返すには、`response_model_exclude_unset` を使用します。
