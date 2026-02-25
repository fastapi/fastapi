# HTTP Basic 認証 { #http-basic-auth }

最もシンプルなケースでは、HTTP Basic 認証を利用できます。

HTTP Basic 認証では、アプリケーションはユーザー名とパスワードを含むヘッダーを期待します。

それを受け取れない場合、HTTP 401 "Unauthorized" エラーを返します。

そして、値が `Basic` のヘッダー `WWW-Authenticate` を、任意の `realm` パラメータとともに返します。

これにより、ブラウザは組み込みのユーザー名とパスワード入力プロンプトを表示します。

その後、そのユーザー名とパスワードを入力すると、ブラウザはそれらをヘッダーに自動的に付与して送信します。

## シンプルな HTTP Basic 認証 { #simple-http-basic-auth }

- `HTTPBasic` と `HTTPBasicCredentials` をインポートします。
- `HTTPBasic` を使って「`security` スキーム」を作成します。
- その `security` を依存関係として path operation に使用します。
- `HTTPBasicCredentials` 型のオブジェクトが返ります:
    - 送信された `username` と `password` を含みます。

{* ../../docs_src/security/tutorial006_an_py310.py hl[4,8,12] *}

URL を最初に開こうとしたとき（またはドキュメントで「Execute」ボタンをクリックしたとき）、ブラウザはユーザー名とパスワードの入力を求めます:

<img src="/img/tutorial/security/image12.png">

## ユーザー名の確認 { #check-the-username }

より完全な例です。

依存関係を使ってユーザー名とパスワードが正しいかを確認します。

これには、Python 標準モジュール <a href="https://docs.python.org/3/library/secrets.html" class="external-link" target="_blank">`secrets`</a> を用いてユーザー名とパスワードを検証します。

`secrets.compare_digest()` は `bytes` か、ASCII 文字（英語の文字）のみを含む `str` を受け取る必要があります。つまり、`Sebastián` のように `á` を含む文字ではそのままでは動作しません。

これに対処するため、まず `username` と `password` を UTF-8 でエンコードして `bytes` に変換します。

そのうえで、`secrets.compare_digest()` を使って、`credentials.username` が `"stanleyjobson"` であり、`credentials.password` が `"swordfish"` であることを確認します。

{* ../../docs_src/security/tutorial007_an_py310.py hl[1,12:24] *}

これは次のようなコードに相当します:

```Python
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # Return some error
    ...
```

しかし `secrets.compare_digest()` を使うことで、「タイミング攻撃」と呼ばれる種類の攻撃に対して安全になります。

### タイミング攻撃 { #timing-attacks }

「タイミング攻撃」とは何でしょうか？

攻撃者がユーザー名とパスワードを推測しようとしていると想像してください。

そして、ユーザー名 `johndoe`、パスワード `love123` を使ってリクエストを送ります。

その場合、アプリケーション内の Python コードは次のようなものと等価になります:

```Python
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

しかし、Python は `johndoe` の最初の `j` と `stanleyjobson` の最初の `s` を比較した時点で、両者の文字列が同じでないと判断してすぐに `False` を返します。つまり「残りの文字を比較して計算資源を無駄にする必要はない」と考えるわけです。そしてアプリケーションは「ユーザー名またはパスワードが正しくありません」と返します。

次に、攻撃者がユーザー名 `stanleyjobsox`、パスワード `love123` で試すとします。

アプリケーションのコードは次のようになります:

```Python
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

この場合、Python は `stanleyjobsox` と `stanleyjobson` の両方で `stanleyjobso` 全体を比較してから、文字列が同じでないと気づきます。したがって、「ユーザー名またはパスワードが正しくありません」と応答するまでに余分に数マイクロ秒かかります。

#### 応答時間が攻撃者を助ける { #the-time-to-answer-helps-the-attackers }

ここで、サーバーが「ユーザー名またはパスワードが正しくありません」というレスポンスを返すまでに、わずかに長い時間がかかったことに気づけば、攻撃者は何かしら正解に近づいた、すなわち先頭のいくつかの文字が正しかったことを知ることができます。

すると、`johndoe` よりも `stanleyjobsox` に近いものを狙って再試行できます。

#### 「プロ」レベルの攻撃 { #a-professional-attack }

もちろん、攻撃者はこれらを手作業では行わず、プログラムを書いて、1 秒間に数千〜数百万回のテストを行うでしょう。そして 1 回に 1 文字ずつ正しい文字を見つけていきます。

そうすることで、数分から数時間のうちに、攻撃者は私たちのアプリケーションの「助け」（応答にかかった時間）だけを利用して、正しいユーザー名とパスワードを推測できてしまいます。

#### `secrets.compare_digest()` で対策 { #fix-it-with-secrets-compare-digest }

しかし、私たちのコードでは実際に `secrets.compare_digest()` を使用しています。

要するに、`stanleyjobsox` と `stanleyjobson` を比較するのにかかる時間は、`johndoe` と `stanleyjobson` を比較するのにかかる時間と同じになります。パスワードでも同様です。

このように、アプリケーションコードで `secrets.compare_digest()` を使うと、この種の一連のセキュリティ攻撃に対して安全になります。

### エラーを返す { #return-the-error }

認証情報が不正であることを検出したら、ステータスコード 401（認証情報が提供されない場合と同じ）で `HTTPException` を返し、ブラウザに再度ログインプロンプトを表示させるためにヘッダー `WWW-Authenticate` を追加します:

{* ../../docs_src/security/tutorial007_an_py310.py hl[26:30] *}
