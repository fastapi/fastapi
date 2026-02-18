# 追加のモデル { #extra-models }

先ほどの例に続き、複数の関連モデルを持つことは一般的です。

これはユーザーモデルの場合は特にそうです。なぜなら:

* **入力モデル** にはパスワードが必要です。
* **出力モデル**はパスワードをもつべきではありません。
* **データベースモデル**はおそらくハッシュ化されたパスワードが必要になるでしょう。

/// danger | 警告

ユーザーの平文のパスワードは絶対に保存しないでください。常に検証できる「安全なハッシュ」を保存してください。

知らない方は、[セキュリティの章](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}で「パスワードハッシュ」とは何かを学ぶことができます。

///

## 複数のモデル { #multiple-models }

ここでは、パスワードフィールドをもつモデルがどのように見えるのか、また、どこで使われるのか、大まかなイメージを紹介します:

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}

### `**user_in.model_dump()` について { #about-user-in-model-dump }

#### Pydanticの`.model_dump()` { #pydantics-model-dump }

`user_in`は`UserIn`クラスのPydanticモデルです。

Pydanticモデルには、モデルのデータを含む`dict`を返す`.model_dump()`メソッドがあります。

そこで、以下のようなPydanticオブジェクト`user_in`を作成すると:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

そして呼び出すと:

```Python
user_dict = user_in.model_dump()
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

#### `dict`の展開 { #unpacking-a-dict }

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

#### 別のモデルの内容からつくるPydanticモデル { #a-pydantic-model-from-the-contents-of-another }

上述の例では`user_in.model_dump()`から`user_dict`をこのコードのように取得していますが:

```Python
user_dict = user_in.model_dump()
UserInDB(**user_dict)
```

これは以下と同等です:

```Python
UserInDB(**user_in.model_dump())
```

...なぜなら`user_in.model_dump()`は`dict`であり、`**`を付与して`UserInDB`を渡してPythonに「展開」させているからです。

そこで、別のPydanticモデルのデータからPydanticモデルを取得します。

#### `dict`の展開と追加キーワード { #unpacking-a-dict-and-extra-keywords }

そして、追加のキーワード引数`hashed_password=hashed_password`を以下のように追加すると:

```Python
UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
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

追加のサポート関数`fake_password_hasher`と`fake_save_user`は、データの可能な流れをデモするだけであり、もちろん本当のセキュリティを提供しているわけではありません。

///

## 重複の削減 { #reduce-duplication }

コードの重複を減らすことは、**FastAPI**の中核的なアイデアの１つです。

コードの重複が増えると、バグやセキュリティの問題、コードの非同期化問題（ある場所では更新しても他の場所では更新されない場合）などが発生する可能性が高くなります。

そして、これらのモデルは全てのデータを共有し、属性名や型を重複させています。

もっと良い方法があります。

他のモデルのベースとなる`UserBase`モデルを宣言することができます。そして、そのモデルの属性（型宣言、検証など）を継承するサブクラスを作ることができます。

データの変換、検証、文書化などはすべて通常通りに動作します。

このようにして、モデル間の違いだけを宣言することができます（平文の`password`、`hashed_password`、パスワードなし）:

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` または `anyOf` { #union-or-anyof }

レスポンスを2つ以上の型の`Union`として宣言できます。つまり、そのレスポンスはそれらのいずれかになります。

OpenAPIでは`anyOf`で定義されます。

そのためには、標準的なPythonの型ヒント<a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>を使用します:

/// note | 備考

<a href="https://docs.pydantic.dev/latest/concepts/types/#unions" class="external-link" target="_blank">`Union`</a>を定義する場合は、最も具体的な型を先に、その後により具体性の低い型を含めてください。以下の例では、より具体的な`PlaneItem`が`Union[PlaneItem, CarItem]`内で`CarItem`より前に来ています。

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}

### Python 3.10の`Union` { #union-in-python-3-10 }

この例では、引数`response_model`の値として`Union[PlaneItem, CarItem]`を渡しています。

**型アノテーション**に書くのではなく、**引数の値**として渡しているため、Python 3.10でも`Union`を使う必要があります。

型アノテーションであれば、次のように縦棒を使用できました:

```Python
some_variable: PlaneItem | CarItem
```

しかし、これを代入で`response_model=PlaneItem | CarItem`のように書くと、Pythonはそれを型アノテーションとして解釈するのではなく、`PlaneItem`と`CarItem`の間で**無効な操作**を行おうとしてしまうため、エラーになります。

## モデルのリスト { #list-of-models }

同じように、オブジェクトのリストのレスポンスを宣言できます。

そのためには、標準のPythonの`list`を使用します:

{* ../../docs_src/extra_models/tutorial004_py310.py hl[18] *}

## 任意の`dict`によるレスポンス { #response-with-arbitrary-dict }

また、Pydanticモデルを使用せずに、キーと値の型だけを定義した任意の`dict`を使ってレスポンスを宣言することもできます。

これは、有効なフィールド・属性名（Pydanticモデルに必要なもの）を事前に知らない場合に便利です。

この場合、`dict`を使用できます:

{* ../../docs_src/extra_models/tutorial005_py310.py hl[6] *}

## まとめ { #recap }

複数のPydanticモデルを使用し、ケースごとに自由に継承します。

エンティティが異なる「状態」を持たなければならない場合は、エンティティごとに単一のデータモデルを持つ必要はありません。`password`、`password_hash`、パスワードなしを含む状態を持つユーザー「エンティティ」の場合と同様です。
