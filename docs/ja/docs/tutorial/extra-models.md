# モデル - より詳しく

先ほどの例に続き、複数の関連モデルを持つことが一般的です。

これはユーザーモデルの場合は特にそうです。なぜなら:

* **入力モデル** にはパスワードが必要です。
* **出力モデル**はパスワードをもつべきではありません。
* **データベースモデル**はおそらくハッシュ化されたパスワードが必要になるでしょう。

/// danger | 危険

ユーザーの平文のパスワードは絶対に保存しないでください。常に認証に利用可能な「安全なハッシュ」を保存してください。

知らない方は、[セキュリティの章](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}で「パスワードハッシュ」とは何かを学ぶことができます。

///

## 複数のモデル

ここでは、パスワードフィールドをもつモデルがどのように見えるのか、また、どこで使われるのか、大まかなイメージを紹介します:

{* ../../docs_src/extra_models/tutorial001.py hl[9,11,16,22,24,29:30,33:35,40:41] *}

### `**user_in.dict()`について

#### Pydanticの`.dict()`

`user_in`は`UserIn`クラスのPydanticモデルです。

Pydanticモデルには、モデルのデータを含む`dict`を返す`.dict()`メソッドがあります。

そこで、以下のようなPydanticオブジェクト`user_in`を作成すると:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

そして呼び出すと:

```Python
user_dict = user_in.dict()
```

これで変数`user_dict`のデータを持つ`dict`ができました。（これはPydanticモデルのオブジェクトの代わりに`dict`です）。

そして呼び出すと:

```Python
print(user_dict)
```

以下のようなPythonの`dict`を得ることができます:

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### `dict`の展開

`user_dict`のような`dict`を受け取り、それを`**user_dict`を持つ関数（またはクラス）に渡すと、Pythonはそれを「展開」します。これは`user_dict`のキーと値を直接キー・バリューの引数として渡します。

そこで上述の`user_dict`の続きを以下のように書くと:

```Python
UserInDB(**user_dict)
```

以下と同等の結果になります:

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

もっと正確に言えば、`user_dict`を将来的にどんな内容であっても直接使用することになります:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### 別のモデルからつくるPydanticモデル

上述の例では`user_in.dict()`から`user_dict`をこのコードのように取得していますが:

```Python
user_dict = user_in.dict()
UserInDB(**user_dict)
```

これは以下と同等です:

```Python
UserInDB(**user_in.dict())
```

...なぜなら`user_in.dict()`は`dict`であり、`**`を付与して`UserInDB`を渡してPythonに「展開」させているからです。

そこで、別のPydanticモデルのデータからPydanticモデルを取得します。

#### `dict`の展開と追加引数

そして、追加のキーワード引数`hashed_password=hashed_password`を以下のように追加すると:

```Python
UserInDB(**user_in.dict(), hashed_password=hashed_password)
```

...以下のようになります:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

/// warning | 注意

サポートしている追加機能は、データの可能な流れをデモするだけであり、もちろん本当のセキュリティを提供しているわけではありません。

///

## 重複の削減

コードの重複を減らすことは、**FastAPI**の中核的なアイデアの１つです。

コードの重複が増えると、バグやセキュリティの問題、コードの非同期化問題（ある場所では更新しても他の場所では更新されない場合）などが発生する可能性が高くなります。

そして、これらのモデルは全てのデータを共有し、属性名や型を重複させています。

もっと良い方法があります。

他のモデルのベースとなる`UserBase`モデルを宣言することができます。そして、そのモデルの属性（型宣言、検証など）を継承するサブクラスを作ることができます。

データの変換、検証、文書化などはすべて通常通りに動作します。

このようにして、モデル間の違いだけを宣言することができます:

{* ../../docs_src/extra_models/tutorial002.py hl[9,15,16,19,20,23,24] *}

## `Union`または`anyOf`

レスポンスを２つの型の`Union`として宣言することができます。

OpenAPIでは`anyOf`で定義されます。

そのためには、標準的なPythonの型ヒント<a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>を使用します:

{* ../../docs_src/extra_models/tutorial003.py hl[1,14,15,18,19,20,33] *}

## モデルのリスト

同じように、オブジェクトのリストのレスポンスを宣言することができます。

そのためには、標準のPythonの`typing.List`を使用する:

{* ../../docs_src/extra_models/tutorial004.py hl[1,20] *}

## 任意の`dict`を持つレスポンス

また、Pydanticモデルを使用せずに、キーと値の型だけを定義した任意の`dict`を使ってレスポンスを宣言することもできます。

これは、有効なフィールド・属性名（Pydanticモデルに必要なもの）を事前に知らない場合に便利です。

この場合、`typing.Dict`を使用することができます:

{* ../../docs_src/extra_models/tutorial005.py hl[1,8] *}

## まとめ

複数のPydanticモデルを使用し、ケースごとに自由に継承します。

エンティティが異なる「状態」を持たなければならない場合は、エンティティごとに単一のデータモデルを持つ必要はありません。`password` や `password_hash` やパスワードなしなどのいくつかの「状態」をもつユーザー「エンティティ」の場合の様にすれば良いです。
