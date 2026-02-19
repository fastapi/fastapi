# LLM テストファイル { #llm-test-file }

このドキュメントは、ドキュメントを翻訳する <abbr title="Large Language Model - 大規模言語モデル">LLM</abbr> が、`scripts/translate.py` の `general_prompt` と、`docs/{language code}/llm-prompt.md` の言語固有プロンプトを理解しているかをテストします。言語固有プロンプトは `general_prompt` の末尾に追加されます。

ここに追加したテストは、すべての言語固有プロンプトの設計者が参照します。

使い方:

* 言語固有プロンプトを用意します - `docs/{language code}/llm-prompt.md`。
* この文書を希望するターゲット言語に新規で翻訳します（例: `translate.py` の `translate-page` コマンド）。これにより `docs/{language code}/docs/_llm-test.md` に翻訳が作成されます。
* 翻訳が問題ないか確認します。
* 必要であれば、言語固有プロンプト、general プロンプト、または英語ドキュメントを改善します。
* その後、翻訳に残っている問題を手動で修正し、良い翻訳にします。
* 良い翻訳を用意した状態でもう一度翻訳します。理想的な結果は、LLM が翻訳に一切変更を加えないことです。つまり general プロンプトと言語固有プロンプトが最良であることを意味します（時々いくつかランダムに見える変更を行うことがあります。理由は <a href="https://doublespeak.chat/#/handbook#deterministic-output" class="external-link" target="_blank">LLM は決定論的アルゴリズムではない</a> ためです）。

テスト内容:

## コードスニペット { #code-snippets }

//// tab | テスト

これはコードスニペットです: `foo`。そしてこれもコードスニペットです: `bar`。さらにもう一つ: `baz quux`。

////

//// tab | 情報

コードスニペットの内容はそのままにしておく必要があります。

`scripts/translate.py` の general プロンプト内「### Content of code snippets」の節を参照してください。

////

## 引用 { #quotes }

//// tab | テスト

昨日、友人はこう書きました。「incorrectly を正しく綴れば、あなたはそれを間違って綴ったことになる」。それに対して私はこう答えました。「そのとおり。ただし『incorrectly』は誤りで、『"incorrectly"』ではありません」。

/// note | 備考

LLM はおそらくここを誤って翻訳します。重要なのは、再翻訳時に修正済みの翻訳を維持できるかどうかだけです。

///

////

//// tab | 情報

プロンプト設計者は、ストレートクォートをタイポグラフィックな引用符に変換するかどうかを選べます。そのままでも問題ありません。

例として `docs/de/llm-prompt.md` の「### Quotes」の節を参照してください。

////

## コードスニペット内の引用 { #quotes-in-code-snippets }

//// tab | テスト

`pip install "foo[bar]"`

コードスニペット中の文字列リテラルの例: `"this"`, `'that'`.

難しい文字列リテラルの例: `f"I like {'oranges' if orange else "apples"}"`

ハードコア: `Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | 情報

... ただし、コードスニペット内の引用符はそのままにしておく必要があります。

////

## コードブロック { #code-blocks }

//// tab | テスト

Bash のコード例です...

```bash
# 宇宙にあいさつを表示
echo "Hello universe"
```

...そしてコンソールのコード例です...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

...さらに別のコンソールのコード例です...

```console
// ディレクトリ "code" を作成
$ mkdir code
// そのディレクトリに移動
$ cd code
```

...そして Python のコード例です...

```Python
wont_work()  # これは動作しません 😱
works(foo="bar")  # これは動作します 🎉
```

...以上です。

////

//// tab | 情報

コードブロック内のコードは、コメントを除き、変更してはいけません。

`scripts/translate.py` の general プロンプト内「### Content of code blocks」の節を参照してください。

////

## タブと色付きボックス { #tabs-and-colored-boxes }

//// tab | テスト

/// info | 情報
いくつかのテキスト
///

/// note | 備考
いくつかのテキスト
///

/// note | 技術詳細
いくつかのテキスト
///

/// check | 確認
いくつかのテキスト
///

/// tip | 豆知識
いくつかのテキスト
///

/// warning | 注意
いくつかのテキスト
///

/// danger | 警告
いくつかのテキスト
///

////

//// tab | 情報

タブおよび `Info`/`Note`/`Warning` などのブロックには、タイトルの翻訳を縦棒（`|`）の後ろに追加します。

`scripts/translate.py` の general プロンプト内「### Special blocks」と「### Tab blocks」の節を参照してください。

////

## Web リンクと内部リンク { #web-and-internal-links }

//// tab | テスト

リンクのテキストは翻訳し、リンク先のアドレスは変更しないでください:

* [上の見出しへのリンク](#code-snippets)
* [内部リンク](index.md#installation){.internal-link target=_blank}
* <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">外部リンク</a>
* <a href="https://fastapi.tiangolo.com/css/styles.css" class="external-link" target="_blank">スタイルへのリンク</a>
* <a href="https://fastapi.tiangolo.com/js/logic.js" class="external-link" target="_blank">スクリプトへのリンク</a>
* <a href="https://fastapi.tiangolo.com/img/foo.jpg" class="external-link" target="_blank">画像へのリンク</a>

リンクのテキストは翻訳し、リンク先のアドレスは翻訳版を指すようにしてください:

* <a href="https://fastapi.tiangolo.com/ja/" class="external-link" target="_blank">FastAPI リンク</a>

////

//// tab | 情報

リンクのテキストは翻訳し、アドレスは変更しないでください。例外は、FastAPI ドキュメントのページへの絶対 URL です。その場合は翻訳版へのリンクにします。

`scripts/translate.py` の general プロンプト内「### Links」の節を参照してください。

////

## HTML "abbr" 要素 { #html-abbr-elements }

//// tab | テスト

ここでは HTML の "abbr" 要素で包まれたものをいくつか示します（いくつかは架空です）:

### abbr が完全な語句を示す { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done - 仕事を成し遂げること">GTD</abbr>
* <abbr title="less than - より小さい"><code>lt</code></abbr>
* <abbr title="XML Web Token - XML ウェブトークン">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface - 並列サーバーゲートウェイインターフェース">PSGI</abbr>

### abbr が完全な語句と説明を示す { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network - Mozilla 開発者ネットワーク: 開発者向けドキュメント、Firefox の開発元が執筆">MDN</abbr>
* <abbr title="Input/Output - 入出力: ディスクの読み書き、ネットワーク通信。">I/O</abbr>.

////

//// tab | 情報

"abbr" 要素の "title" 属性は特定の指示に従って翻訳します。

翻訳は、英語の語を説明するために独自の "abbr" 要素を追加してもよく、LLM はそれらを削除してはいけません。

`scripts/translate.py` の general プロンプト内「### HTML abbr elements」の節を参照してください。

////

## HTML "dfn" 要素 { #html-dfn-elements }

* <dfn title="ある方法で接続・連携して動作するよう構成された複数のマシンの集合">クラスター</dfn>
* <dfn title="入力層と出力層の間に多数の隠れ層を持つ人工ニューラルネットワークを用いる機械学習の手法で、その内部構造を包括的に形成する">ディープラーニング</dfn>

## 見出し { #headings }

//// tab | テスト

### Web アプリを開発する - チュートリアル { #develop-a-webapp-a-tutorial }

こんにちは。

### 型ヒントとアノテーション { #type-hints-and-annotations }

またこんにちは。

### スーパークラスとサブクラス { #super-and-subclasses }

またこんにちは。

////

//// tab | 情報

見出しに関する唯一の厳格なルールは、リンクが壊れないように、LLM が中括弧内のハッシュ部分を変更しないことです。

`scripts/translate.py` の general プロンプト内「### Headings」の節を参照してください。

言語固有の指示については、例として `docs/de/llm-prompt.md` の「### Headings」の節を参照してください。

////

## ドキュメントで使う用語 { #terms-used-in-the-docs }

//// tab | テスト

* you
* your

* e.g.
* etc.

* `foo` を `int` として
* `bar` を `str` として
* `baz` を `list` として

* チュートリアル - ユーザーガイド
* 上級ユーザーガイド
* SQLModel ドキュメント
* API ドキュメント
* 自動生成ドキュメント

* データサイエンス
* ディープラーニング
* 機械学習
* 依存性注入
* HTTP Basic 認証
* HTTP Digest
* ISO 形式
* JSON Schema 規格
* JSON スキーマ
* スキーマ定義
* Password Flow
* モバイル

* 非推奨
* 設計された
* 無効
* オンザフライ
* 標準
* デフォルト
* 大文字小文字を区別
* 大文字小文字を区別しない

* アプリケーションを提供する
* ページを配信する

* アプリ
* アプリケーション

* リクエスト
* レスポンス
* エラーレスポンス

* path operation
* path operation デコレータ
* path operation 関数

* ボディ
* リクエストボディ
* レスポンスボディ
* JSON ボディ
* フォームボディ
* ファイルボディ
* 関数本体

* パラメータ
* ボディパラメータ
* パスパラメータ
* クエリパラメータ
* Cookie パラメータ
* ヘッダーパラメータ
* フォームパラメータ
* 関数パラメータ

* イベント
* 起動イベント
* サーバーの起動
* シャットダウンイベント
* lifespan イベント

* ハンドラ
* イベントハンドラ
* 例外ハンドラ
* 処理する

* モデル
* Pydantic モデル
* データモデル
* データベースモデル
* フォームモデル
* モデルオブジェクト

* クラス
* 基底クラス
* 親クラス
* サブクラス
* 子クラス
* 兄弟クラス
* クラスメソッド

* ヘッダー
* ヘッダー（複数）
* 認可ヘッダー
* `Authorization` ヘッダー
* Forwarded ヘッダー

* 依存性注入システム
* 依存関係
* dependable
* dependant

* I/O バウンド
* CPU バウンド
* 同時実行性
* 並列性
* マルチプロセッシング

* env var
* 環境変数
* `PATH`
* `PATH` 環境変数

* 認証
* 認証プロバイダ
* 認可
* 認可フォーム
* 認可プロバイダ
* ユーザーが認証する
* システムがユーザーを認証する

* CLI
* コマンドラインインターフェース

* サーバー
* クライアント

* クラウドプロバイダ
* クラウドサービス

* 開発
* 開発段階

* dict
* 辞書
* 列挙型
* Enum
* 列挙メンバー

* エンコーダー
* デコーダー
* エンコードする
* デコードする

* 例外
* 送出する

* 式
* 文

* フロントエンド
* バックエンド

* GitHub ディスカッション
* GitHub Issue

* パフォーマンス
* パフォーマンス最適化

* 戻り値の型
* 戻り値

* セキュリティ
* セキュリティスキーム

* タスク
* バックグラウンドタスク
* タスク関数

* テンプレート
* テンプレートエンジン

* 型アノテーション
* 型ヒント

* サーバーワーカー
* Uvicorn ワーカー
* Gunicorn ワーカー
* ワーカープロセス
* ワーカークラス
* ワークロード

* デプロイ
* デプロイする

* SDK
* ソフトウェア開発キット

* `APIRouter`
* `requirements.txt`
* Bearer Token
* 破壊的変更
* バグ
* ボタン
* 呼び出し可能
* コード
* コミット
* コンテキストマネージャ
* コルーチン
* データベースセッション
* ディスク
* ドメイン
* エンジン
* フェイクの X
* HTTP GET メソッド
* アイテム
* ライブラリ
* ライフスパン
* ロック
* ミドルウェア
* モバイルアプリケーション
* モジュール
* マウント
* ネットワーク
* オリジン
* オーバーライド
* ペイロード
* プロセッサ
* プロパティ
* プロキシ
* プルリクエスト
* クエリ
* RAM
* リモートマシン
* ステータスコード
* 文字列
* タグ
* Web フレームワーク
* ワイルドカード
* 返す
* 検証する

////

//// tab | 情報

これはドキュメントで見られる（主に）技術用語の不完全かつ規範的でない一覧です。プロンプト設計者が、LLM がどの用語で手助けを必要としているかを把握するのに役立つかもしれません。例えば、良い翻訳を最適でない翻訳に戻してしまう場合や、あなたの言語での活用・格変化に問題がある場合などです。

`docs/de/llm-prompt.md` の「### List of English terms and their preferred German translations」の節を参照してください。

////
