# パスワードとBearerによるシンプルなOAuth2 { #simple-oauth2-with-password-and-bearer }

前章から発展させて、完全なセキュリティフローに必要な不足部分を追加していきます。

## `username` と `password` を取得する { #get-the-username-and-password }

`username` と `password` を取得するために **FastAPI** のセキュリティユーティリティを使います。

OAuth2 では、「password flow」（ここで使用するフロー）を使う場合、クライアント/ユーザーはフォームデータとして `username` と `password` フィールドを送信する必要があります。

しかも、フィールド名はこの通りでなければなりません。つまり、`user-name` や `email` では動作しません。

ただし、フロントエンドで最終ユーザーにどう表示するかは自由です。

また、データベースのモデルでは任意の別名を使って構いません。

しかし、ログイン用の path operation では、仕様との互換性を保つ（たとえば組み込みのAPIドキュメントシステムを使えるようにする）ために、これらの名前を使う必要があります。

また、仕様では `username` と `password` はフォームデータとして送らなければならない（つまり、ここではJSONは使わない）ことも定められています。

### `scope` { #scope }

仕様では、クライアントは追加のフォームフィールド「`scope`」を送ることができるとも書かれています。

フォームフィールド名は `scope`（単数形）ですが、実態はスペース区切りの「スコープ」文字列を並べた長い文字列です。

各「スコープ」は（スペースを含まない）単なる文字列です。

通常、特定のセキュリティ権限を宣言するために使われます。例えば:

- `users:read` や `users:write` はよくある例です。
- `instagram_basic` は Facebook / Instagram で使われます。
- `https://www.googleapis.com/auth/drive` は Google で使われます。

/// info | 情報

OAuth2 における「スコープ」は、要求される特定の権限を表す単なる文字列です。

`:` のような他の文字を含んでいても、URL であっても構いません。

それらの詳細は実装依存です。

OAuth2 にとっては単なる文字列です。

///

## `username` と `password` を取得するコード { #code-to-get-the-username-and-password }

では、これを処理するために **FastAPI** が提供するユーティリティを使いましょう。

### `OAuth2PasswordRequestForm` { #oauth2passwordrequestform }

まず、`OAuth2PasswordRequestForm` をインポートし、`/token` の path operation に `Depends` で依存関係として使います:

{* ../../docs_src/security/tutorial003_an_py310.py hl[4,78] *}

`OAuth2PasswordRequestForm` は次のフォームボディを宣言するクラス依存関係です:

- `username`
- `password`
- スペース区切りの文字列で構成される、オプションの `scope` フィールド
- オプションの `grant_type`

/// tip | 豆知識

OAuth2 の仕様では、固定値 `password` を持つフィールド `grant_type` が実際には必須ですが、`OAuth2PasswordRequestForm` はそれを強制しません。

強制したい場合は、`OAuth2PasswordRequestForm` の代わりに `OAuth2PasswordRequestFormStrict` を使ってください。

///

- オプションの `client_id`（この例では不要）
- オプションの `client_secret`（この例では不要）

/// info | 情報

`OAuth2PasswordRequestForm` は、`OAuth2PasswordBearer` のように **FastAPI** にとって特別なクラスではありません。

`OAuth2PasswordBearer` は **FastAPI** にセキュリティスキームであることを認識させます。そのため OpenAPI にそのように追加されます。

一方、`OAuth2PasswordRequestForm` は、あなた自身でも書けるような単なるクラス依存関係であり、直接 `Form` パラメータを宣言することもできます。

ただし一般的なユースケースなので、簡単に使えるよう **FastAPI** が直接提供しています。

///

### フォームデータの利用 { #use-the-form-data }

/// tip | 豆知識

依存関係クラス `OAuth2PasswordRequestForm` のインスタンスは、スペース区切りの長い文字列を持つ `scope` 属性は持ちません。代わりに、送られてきた各スコープの実際の文字列リストを格納する `scopes` 属性を持ちます。

この例では `scopes` は使いませんが、必要ならその機能が利用できます。

///

次に、フォームフィールドの `username` を使って（疑似の）データベースからユーザーデータを取得します。

そのユーザーが存在しない場合は、「Incorrect username or password」というエラーを返します。

エラーには `HTTPException` 例外を使います:

{* ../../docs_src/security/tutorial003_an_py310.py hl[3,79:81] *}

### パスワードのチェック { #check-the-password }

この時点でデータベースからユーザーデータは取得できましたが、まだパスワードを確認していません。

まず、そのデータを Pydantic の `UserInDB` モデルに入れます。

プレーンテキストのパスワードを保存してはいけないので、（疑似の）パスワードハッシュ化システムを使います。

パスワードが一致しなければ、同じエラーを返します。

#### パスワードハッシュ化 { #password-hashing }

「ハッシュ化」とは、ある内容（ここではパスワード）を、乱雑に見えるバイト列（単なる文字列）に変換することを指します。

まったく同じ内容（まったく同じパスワード）を渡すと、毎回まったく同じ乱雑な文字列が得られます。

しかし、その乱雑な文字列から元のパスワードに戻すことはできません。

##### なぜパスワードをハッシュ化するのか { #why-use-password-hashing }

もしデータベースが盗まれても、盗んだ側が手にするのはユーザーのプレーンテキストのパスワードではなく、ハッシュだけです。

したがって、盗んだ側は同じパスワードを別のシステムで試すことができません（多くのユーザーがあらゆる場所で同じパスワードを使っているため、これは危険になり得ます）。

{* ../../docs_src/security/tutorial003_an_py310.py hl[82:85] *}

#### `**user_dict` について { #about-user-dict }

`UserInDB(**user_dict)` は次を意味します:

`user_dict` のキーと値を、そのままキーワード引数として渡します。つまり次と同等です:

```Python
UserInDB(
    username = user_dict["username"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    disabled = user_dict["disabled"],
    hashed_password = user_dict["hashed_password"],
)
```

/// info | 情報

`**user_dict` のより完全な解説は、[**追加モデル**のドキュメント](../extra-models.md#about-user-in-dict){.internal-link target=_blank}を参照してください。

///

## トークンを返す { #return-the-token }

`token` エンドポイントのレスポンスは JSON オブジェクトでなければなりません。

`token_type` を含める必要があります。ここでは「Bearer」トークンを使うので、トークンタイプは「`bearer`」です。

そして `access_token` を含め、その中にアクセストークンの文字列を入れます。

この単純な例では、完全に安全ではありませんが、トークンとして同じ `username` をそのまま返します。

/// tip | 豆知識

次の章では、パスワードハッシュ化と <abbr title="JSON Web Tokens - JSON Web Token">JWT</abbr> トークンを使った本当に安全な実装を見ます。

しかし今は、必要な特定の詳細に集中しましょう。

///

{* ../../docs_src/security/tutorial003_an_py310.py hl[87] *}

/// tip | 豆知識

仕様に従うと、この例と同じく `access_token` と `token_type` を含む JSON を返す必要があります。

これはあなた自身のコードで実装する必要があり、これらのJSONキーを使っていることを確認してください。

仕様に準拠するために、あなた自身が正しく覚えて実装すべきことは、ほぼこれだけです。

それ以外は **FastAPI** が面倒を見てくれます。

///

## 依存関係の更新 { #update-the-dependencies }

ここで依存関係を更新します。

アクティブなユーザーの場合にのみ `current_user` を取得したいとします。

そこで、`get_current_user` を依存関係として利用する追加の依存関係 `get_current_active_user` を作成します。

これら2つの依存関係は、ユーザーが存在しない、または非アクティブである場合に、HTTPエラーを返すだけです。

したがって、エンドポイントでは、ユーザーが存在し、正しく認証され、かつアクティブである場合にのみ、ユーザーを取得します:

{* ../../docs_src/security/tutorial003_an_py310.py hl[58:66,69:74,94] *}

/// info | 情報

ここで返している値が `Bearer` の追加ヘッダー `WWW-Authenticate` も仕様の一部です。

HTTP（エラー）ステータスコード 401「UNAUTHORIZED」は、`WWW-Authenticate` ヘッダーも返すことになっています。

ベアラートークン（今回のケース）の場合、そのヘッダーの値は `Bearer` であるべきです。

実際のところ、この追加ヘッダーを省略しても動作はします。

しかし、仕様に準拠するためにここでは付与しています。

また、（今または将来）それを想定して利用するツールがあるかもしれず、あなたやユーザーにとって有用になる可能性があります。

これが標準の利点です…。

///

## 動作確認 { #see-it-in-action }

インタラクティブドキュメントを開きます: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

### 認証 { #authenticate }

「Authorize」ボタンをクリックします。

次の認証情報を使います:

User: `johndoe`

Password: `secret`

<img src="/img/tutorial/security/image04.png">

システムで認証されると、次のように表示されます:

<img src="/img/tutorial/security/image05.png">

### 自分のユーザーデータを取得 { #get-your-own-user-data }

`GET` の path `/users/me` を使います。

次のようなユーザーデータが取得できます:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false,
  "hashed_password": "fakehashedsecret"
}
```

<img src="/img/tutorial/security/image06.png">

錠前アイコンをクリックしてログアウトし、同じ操作を再度試すと、次のような HTTP 401 エラーになります:

```JSON
{
  "detail": "Not authenticated"
}
```

### 非アクティブユーザー { #inactive-user }

今度は非アクティブなユーザーで試してみます。次で認証してください:

User: `alice`

Password: `secret2`

そして `GET` の path `/users/me` を使います。

次のような「Inactive user」エラーになります:

```JSON
{
  "detail": "Inactive user"
}
```

## まとめ { #recap }

これで、API のために `username` と `password` に基づく完全なセキュリティシステムを実装するための道具が揃いました。

これらの道具を使えば、任意のデータベース、任意のユーザー/データモデルと互換性のあるセキュリティシステムを構築できます。

ただし、実際にはまだ「安全」ではありません。

次の章では、安全なパスワードハッシュライブラリと <abbr title="JSON Web Tokens - JSON Web Token">JWT</abbr> トークンの使い方を見ていきます。
