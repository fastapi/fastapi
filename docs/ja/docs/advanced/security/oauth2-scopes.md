# OAuth2 のスコープ { #oauth2-scopes }

OAuth2 のスコープは **FastAPI** で直接利用でき、シームレスに統合されています。

これにより、OAuth2 標準に従った、よりきめ細かな権限システムを、OpenAPI 対応アプリケーション（および API ドキュメント）に統合できます。

スコープ付きの OAuth2 は、Facebook、Google、GitHub、Microsoft、X (Twitter) など、多くの大手認証プロバイダで使われている仕組みです。ユーザーやアプリケーションに特定の権限を付与するために利用されます。

「Facebook でログイン」「Google でログイン」「GitHub でログイン」「Microsoft でログイン」「X (Twitter) でログイン」するたびに、そのアプリケーションはスコープ付きの OAuth2 を使っています。

この節では、同じスコープ付き OAuth2 を使って、**FastAPI** アプリケーションで認証と認可を管理する方法を見ていきます。

/// warning | 注意

これはやや高度な内容です。はじめたばかりであれば読み飛ばしても構いません。

OAuth2 のスコープは必ずしも必要ではなく、認証と認可は好きなやり方で実装できます。

ただし、スコープ付きの OAuth2 は、API（OpenAPI）や API ドキュメントにきれいに統合できます。

とはいえ、これらのスコープやその他のセキュリティ／認可要件の適用は、必要に応じてコードの中で行う必要があります。

多くの場合、スコープ付き OAuth2 はオーバースペックになりえます。

それでも必要だと分かっている場合や、興味がある場合は、このまま読み進めてください。

///

## OAuth2 のスコープと OpenAPI { #oauth2-scopes-and-openapi }

OAuth2 仕様では、「スコープ」は空白で区切られた文字列の一覧として定義されています。

各文字列の内容は任意ですが、空白は含められません。

これらのスコープは「権限」を表します。

OpenAPI（例: API ドキュメント）では、「セキュリティスキーム」を定義できます。

これらのセキュリティスキームの一つが OAuth2 を使う場合、スコープを宣言して利用できます。

各「スコープ」は、ただの文字列（空白なし）です。

通常、特定のセキュリティ権限を宣言するために使われます。例えば:

- `users:read` や `users:write` は一般的な例です。
- `instagram_basic` は Facebook / Instagram で使われています。
- `https://www.googleapis.com/auth/drive` は Google で使われています。

/// info | 情報

OAuth2 において「スコープ」は、必要な特定の権限を宣言する単なる文字列です。

`:` のような他の文字が含まれていても、URL であっても問題ありません。

それらの詳細は実装依存です。

OAuth2 にとっては、単に文字列に過ぎません。

///

## 全体像 { #global-view }

まず、メインの**チュートリアル - ユーザーガイド**にある [OAuth2（パスワード［ハッシュ化あり］）、Bearer と JWT トークン](../../tutorial/security/oauth2-jwt.md){.internal-link target=_blank} の例から変更される部分を、スコープ付き OAuth2 を使って手早く見てみましょう。

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,9,13,47,65,106,108:116,122:126,130:136,141,157] *}

では、これらの変更を一つずつ確認していきます。

## OAuth2 のセキュリティスキーム { #oauth2-security-scheme }

最初の変更点は、`me` と `items` の 2 つのスコープを持つ OAuth2 セキュリティスキームを宣言していることです。

`scopes` パラメータは、各スコープをキー、その説明を値とする `dict` を受け取ります:

{* ../../docs_src/security/tutorial005_an_py310.py hl[63:66] *}

これらのスコープを宣言しているため、ログイン／認可時に API ドキュメントに表示されます。

そして、付与するスコープ（`me`、`items`）を選択できます。

これは、Facebook、Google、GitHub などでログイン時に権限を付与する際と同じ仕組みです:

<img src="/img/tutorial/security/image11.png">

## スコープ付きの JWT トークン { #jwt-token-with-scopes }

次に、トークンの path operation を修正して、要求されたスコープを返すようにします。

引き続き同じ `OAuth2PasswordRequestForm` を使用します。これには、リクエストで受け取った各スコープを含む、`str` の `list` である `scopes` プロパティが含まれます。

そして、そのスコープを JWT トークンの一部として返します。

/// danger | 警告

簡単のため、ここでは受け取ったスコープをそのままトークンに追加しています。

しかし、本番アプリケーションではセキュリティのため、ユーザーが実際に持つことができるスコープ、または事前に定義したスコープだけを追加するようにしてください。

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[157] *}

## path operation と依存関係でスコープを宣言 { #declare-scopes-in-path-operations-and-dependencies }

ここでは、`/users/me/items/` の path operation が `items` スコープを必要とするように宣言します。

そのために、`fastapi` から `Security` をインポートして使います。

`Security` は（`Depends` と同様に）依存関係を宣言できますが、さらにスコープ（文字列）のリストを受け取る `scopes` パラメータも持ちます。

この場合、`Security` に依存関数 `get_current_active_user` を渡します（`Depends` と同様です）。

加えて、`items` という 1 つのスコープ（複数でも可）を含む `list` も渡します。

依存関数 `get_current_active_user` は、`Depends` だけでなく `Security` でもサブ依存関係を宣言できます。自身のサブ依存関数（`get_current_user`）を宣言し、さらにスコープ要件を追加します。

この場合、`me` スコープを要求します（複数のスコープも可）。

/// note | 備考

異なる場所で異なるスコープを追加する必要は必ずしもありません。

ここでは、**FastAPI** が異なるレベルで宣言されたスコープをどのように扱うかを示すためにそうしています。

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,141,172] *}

/// info | 技術詳細

`Security` は実際には `Depends` のサブクラスで、後述する追加パラメータが 1 つあるだけです。

しかし `Depends` の代わりに `Security` を使うことで、**FastAPI** はセキュリティスコープを宣言・内部利用でき、OpenAPI で API をドキュメント化できると判断します。

なお、`fastapi` から `Query`、`Path`、`Depends`、`Security` などをインポートする際、それらは実際には特殊なクラスを返す関数です。

///

## `SecurityScopes` を使う { #use-securityscopes }

次に、依存関数 `get_current_user` を更新します。

これは上記の依存関係から使用されます。

ここで、先ほど作成した同じ OAuth2 スキームを依存関係（`oauth2_scheme`）として宣言して使います。

この依存関数自体はスコープ要件を持たないため、`oauth2_scheme` には `Depends` を使えます。セキュリティスコープを指定する必要がない場合は `Security` を使う必要はありません。

さらに、`fastapi.security` からインポートする特別な型 `SecurityScopes` のパラメータを宣言します。

この `SecurityScopes` クラスは `Request` に似ています（`Request` はリクエストオブジェクトを直接取得するために使いました）。

{* ../../docs_src/security/tutorial005_an_py310.py hl[9,106] *}

## `scopes` を使う { #use-the-scopes }

パラメータ `security_scopes` は `SecurityScopes` 型になります。

このオブジェクトは、自身およびこれをサブ依存として使うすべての依存関係で要求されるスコープを含む `scopes` プロパティ（リスト）を持ちます。つまり、すべての「依存元」... 少し分かりにくいかもしれませんが、後で再度説明します。

`security_scopes`（`SecurityScopes` クラスのインスタンス）は、要求されたスコープを空白で連結した 1 つの文字列を返す `scope_str` も提供します（これを使います）。

後で複数箇所で再利用（raise）できるように、`HTTPException` を 1 つ作成します。

この例外には、要求されたスコープがあればそれらを空白区切りの文字列（`scope_str` を使用）として含めます。このスコープ文字列は `WWW-Authenticate` ヘッダに入れます（仕様の一部です）。

{* ../../docs_src/security/tutorial005_an_py310.py hl[106,108:116] *}

## `username` とデータ構造の検証 { #verify-the-username-and-data-shape }

`username` を取得できていることを確認し、スコープを取り出します。

そして、そのデータを Pydantic モデルで検証します（`ValidationError` 例外を捕捉）。JWT トークンの読み取りや Pydantic によるデータ検証でエラーが発生した場合は、先ほど作成した `HTTPException` を送出します。

そのために、Pydantic モデル `TokenData` に新しいプロパティ `scopes` を追加します。

Pydantic でデータを検証することで、例えばスコープは `str` の `list`、`username` は `str` といった、正確な型になっていることを保証できます。

そうしておけば、例えば誤って `dict` などが入って後でアプリケーションを破壊してしまい、セキュリティリスクになる、といった事態を避けられます。

また、その `username` を持つユーザーが存在することも確認し、存在しなければ、やはり先ほどの例外を送出します。

{* ../../docs_src/security/tutorial005_an_py310.py hl[47,117:129] *}

## `scopes` の検証 { #verify-the-scopes }

この依存関数およびすべての依存元（path operation を含む）が要求するすべてのスコープが、受け取ったトークンに含まれていることを検証し、含まれていなければ `HTTPException` を送出します。

そのために、これらすべてのスコープを `str` の `list` として含む `security_scopes.scopes` を使います。

{* ../../docs_src/security/tutorial005_an_py310.py hl[130:136] *}

## 依存関係ツリーとスコープ { #dependency-tree-and-scopes }

依存関係ツリーとスコープをもう一度見てみましょう。

`get_current_active_user` 依存関係は `get_current_user` をサブ依存として持つため、`get_current_active_user` で宣言された `"me"` スコープは、`get_current_user` に渡される `security_scopes.scopes` の必須スコープ一覧に含まれます。

path operation 自体も `"items"` スコープを宣言するため、これも `get_current_user` に渡される `security_scopes.scopes` に含まれます。

依存関係とスコープの階層は次のようになります:

- *path operation* `read_own_items` には:
    - 依存関係に対して必須スコープ `["items"]` がある:
    - `get_current_active_user`:
        - 依存関数 `get_current_active_user` には:
            - 依存関係に対して必須スコープ `["me"]` がある:
            - `get_current_user`:
                - 依存関数 `get_current_user` には:
                    - 自身に必須スコープはない。
                    - `oauth2_scheme` を使う依存関係がある。
                    - `SecurityScopes` 型の `security_scopes` パラメータがある:
                        - この `security_scopes` パラメータは、上で宣言されたすべてのスコープを含む `list` を持つ `scopes` プロパティを持つ。したがって:
                            - *path operation* `read_own_items` では、`security_scopes.scopes` は `["me", "items"]` を含む。
                            - *path operation* `read_users_me` では、`security_scopes.scopes` は `["me"]` を含む。これは依存関係 `get_current_active_user` に宣言されているため。
                            - *path operation* `read_system_status` では、`security_scopes.scopes` は `[]`（空）になる。`scopes` を持つ `Security` を宣言しておらず、その依存関係 `get_current_user` も `scopes` を宣言していないため。

/// tip | 豆知識

重要で「魔法のよう」な点は、`get_current_user` が path operation ごとに異なる `scopes` のリストをチェックすることになる、ということです。

それは、それぞれの path operation と、その path operation の依存関係ツリー内の各依存関係で宣言された `scopes` によって決まります。

///

## `SecurityScopes` の詳細 { #more-details-about-securityscopes }

`SecurityScopes` はどの地点でも、複数箇所でも使えます。「ルート」の依存関係である必要はありません。

常に、その時点の `Security` 依存関係と、**その特定の** path operation と **その特定の** 依存関係ツリーにおける、すべての依存元で宣言されたセキュリティスコープを持ちます。

`SecurityScopes` には依存元で宣言されたすべてのスコープが入るため、トークンが必要なスコープを持っているかどうかを中央の依存関数で検証し、path operation ごとに異なるスコープ要件を宣言する、といった使い方ができます。

これらは path operation ごとに独立して検証されます。

## チェック { #check-it }

API ドキュメントを開くと、認証して、許可するスコープを指定できます。

<img src="/img/tutorial/security/image11.png">

どのスコープも選択しない場合は「認証済み」にはなりますが、`/users/me/` や `/users/me/items/` にアクセスしようとすると、権限が不足しているというエラーになります。`/status/` には引き続きアクセスできます。

`me` スコープだけを選択し、`items` スコープを選択しない場合は、`/users/me/` にはアクセスできますが、`/users/me/items/` にはアクセスできません。

これは、ユーザーがアプリケーションに与えた権限の範囲に応じて、サードパーティアプリケーションがこれらの path operation のいずれかに、ユーザーから提供されたトークンでアクセスしようとしたときに起こる動作です。

## サードパーティ統合について { #about-third-party-integrations }

この例では、OAuth2 の「password」フローを使用しています。

これは、（おそらく自前のフロントエンドで）自分たちのアプリケーションにログインする場合に適しています。

自分たちで管理しているため、`username` と `password` を受け取る相手を信頼できるからです。

しかし、他者が接続する OAuth2 アプリケーション（Facebook、Google、GitHub などに相当する認証プロバイダ）を構築する場合は、他のいずれかのフローを使用すべきです。

最も一般的なのは implicit フローです。

最も安全なのは code フローですが、手順が多く実装がより複雑です。複雑なため、多くのプロバイダは結局 implicit フローを推奨することがあります。

/// note | 備考

各認証プロバイダがフローに独自の名称を付け、自社のブランドの一部にするのは一般的です。

しかし、最終的には同じ OAuth2 標準を実装しています。

///

**FastAPI** には、これらすべての OAuth2 認証フロー向けのユーティリティが `fastapi.security.oauth2` に含まれています。

## デコレータ `dependencies` での `Security` { #security-in-decorator-dependencies }

デコレータの `dependencies` パラメータに `Depends` の `list` を定義できるのと同様（[path operation デコレータでの依存関係](../../tutorial/dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank} 参照）、ここで `scopes` を指定した `Security` も使用できます。
