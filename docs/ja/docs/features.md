# 機能 { #features }

## FastAPIの機能 { #fastapi-features }

**FastAPI** は次のものを提供します:

### オープンスタンダード準拠 { #based-on-open-standards }

* API 作成のための <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a>。<dfn title="別名: エンドポイント、ルート">path</dfn> <dfn title="別名: HTTP メソッド（POST、GET、PUT、DELETE など）">operations</dfn>、パラメータ、リクエストボディ、セキュリティなどの宣言を含みます。
* <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> によるデータモデルの自動ドキュメント化（OpenAPI 自体が JSON Schema に基づいています）。
* 入念な調査のうえ、これらの標準を中心に設計されています。後付けのレイヤーではありません。
* これにより、多くの言語で自動 **クライアントコード生成** が可能です。

### 自動ドキュメント { #automatic-docs }

対話的な API ドキュメントと探索的な Web ユーザーインターフェース。フレームワークは OpenAPI に基づいているため、複数のオプションがあり、デフォルトで 2 つ含まれます。

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>。インタラクティブに探索しつつ、ブラウザから直接 API を呼び出してテストできます。

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a> による代替の API ドキュメント。

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 現代的なPythonのみ { #just-modern-python }

すべて標準の **Python の型** 宣言（Pydantic に感謝）に基づいています。新しい構文を学ぶ必要はありません。標準的でモダンな Python だけです。

（FastAPI を使わない場合でも）Python の型の使い方を 2 分で復習したい場合は、短いチュートリアル [Python Types](python-types.md){.internal-link target=_blank} を参照してください。

型を使った標準的な Python を記述します:

```Python
from datetime import date

from pydantic import BaseModel

# 変数を str として宣言
# そして関数内でエディタ支援を受ける
def main(user_id: str):
    return user_id


# Pydantic モデル
class User(BaseModel):
    id: int
    name: str
    joined: date
```

これは次のように使えます:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

/// info

`**second_user_data` は次の意味です:

`second_user_data` 辞書のキーと値を、そのままキーバリュー引数として渡します。これは `User(id=4, name="Mary", joined="2018-11-30")` と同等です。

///

### エディタのサポート { #editor-support }

フレームワーク全体が使いやすく直感的になるよう設計されており、最高の開発体験を確保するため、開発開始前から複数のエディタであらゆる判断が検証されています。

Python 開発者調査では、<a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">最もよく使われる機能の 1 つが「オートコンプリート」であることが明らかです</a>。

**FastAPI** はその要求を満たすことを基盤にしています。オートコンプリートはどこでも機能します。

ドキュメントに戻る必要はほとんどありません。

エディタがどのように役立つかの例です:

* <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a> の場合:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> の場合:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

以前は不可能だと思っていたコードでも補完が得られます。例えば、リクエストから届く（ネストされている可能性のある）JSON ボディ内の `price` キーなどです。

もう間違ったキー名を入力したり、ドキュメントを行き来したり、上下にスクロールして最終的に `username` と `user_name` のどちらを使ったのか探す必要はありません。

### 簡潔 { #short }

すべてに妥当な **デフォルト** があり、どこでもオプションで構成できます。必要に応じてすべてのパラメータを微調整して、求める API を定義できます。

しかしデフォルトのままでも、すべて **うまく動きます**。

### 検証 { #validation }

* ほとんど（あるいはすべて？）の Python の **データ型** に対する検証:
    * JSON オブジェクト（`dict`）。
    * 項目の型を定義する JSON 配列（`list`）。
    * 文字列（`str`）フィールドの最小/最大長。
    * 数値（`int`、`float`）の最小/最大値、など。

* よりエキゾチックな型の検証:
    * URL。
    * Email。
    * UUID。
    * ...その他。

すべての検証は、確立され堅牢な **Pydantic** によって処理されます。

### セキュリティと認証 { #security-and-authentication }

セキュリティと認証が統合されています。データベースやデータモデルとの妥協はありません。

OpenAPI で定義されたすべてのセキュリティスキームをサポートします:

* HTTP Basic。
* **OAuth2**（**JWT トークン** も可）。チュートリアル [JWT を用いた OAuth2](tutorial/security/oauth2-jwt.md){.internal-link target=_blank} を確認してください。
* API キー（以下の場所）:
    * ヘッダー。
    * クエリパラメータ。
    * クッキー、など。

さらに、Starlette のすべてのセキュリティ機能（**セッション Cookie** を含む）も利用できます。

これらはすべて再利用可能なツールやコンポーネントとして構築されており、システム、データストア、リレーショナル/NoSQL データベース等と容易に統合できます。

### 依存性の注入 { #dependency-injection }

FastAPI には、非常に使いやすく、かつ非常に強力な <dfn title='別名: コンポーネント、リソース、サービス、プロバイダー'><strong>依存性の注入</strong></dfn> システムがあります。

* 依存関係は依存関係を持つこともでき、階層または **依存関係の「グラフ」** を作成できます。
* すべてフレームワークによって**自動的に処理**されます。
* すべての依存関係はリクエストからデータを要求でき、*path operation* の制約と自動ドキュメントを**拡張**できます。
* 依存関係で定義された *path operation* のパラメータについても**自動検証**されます。
* 複雑なユーザー認証システム、**データベース接続** などのサポート。
* **データベースやフロントエンド等との妥協は不要**。すべてと簡単に統合できます。

### 無制限の「プラグイン」 { #unlimited-plug-ins }

別の言い方をすれば、プラグインは不要で、必要なコードをインポートして使うだけです。

あらゆる統合は（依存関係を用いて）非常に簡単に使えるよう設計されており、*path operation* で使うのと同じ構造と構文で、2 行のコードでアプリケーション用の「プラグイン」を作れます。

### テスト済み { #tested }

* 100% の <dfn title="自動的にテストされるコードの量">テストカバレッジ</dfn>。
* 100% <dfn title="Python の型アノテーション。これにより、エディタや外部ツールからより良い支援が受けられます">型アノテーション付き</dfn>のコードベース。
* 本番アプリケーションで使用されています。

## Starletteの機能 { #starlette-features }

**FastAPI** は <a href="https://www.starlette.dev/" class="external-link" target="_blank"><strong>Starlette</strong></a> と完全に互換性があり（かつそれに基づいています）。そのため、手元の Starlette の追加コードも動作します。

`FastAPI` は実際には `Starlette` のサブクラスです。すでに Starlette を知っている、あるいは使っているなら、ほとんどの機能は同じように動作します。

**FastAPI** では **Starlette** のすべての機能が利用できます（FastAPI は強化された Starlette にすぎません）:

* 圧倒的なパフォーマンス。<a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">利用可能な最速クラスの Python フレームワークの 1 つで、**NodeJS** や **Go** と同等です</a>。
* **WebSocket** のサポート。
* プロセス内バックグラウンドタスク。
* 起動およびシャットダウンイベント。
* HTTPX に基づくテストクライアント。
* **CORS**、GZip、静的ファイル、ストリーミングレスポンス。
* **セッションと Cookie** のサポート。
* テストカバレッジ 100%。
* 型アノテーション 100% のコードベース。

## Pydanticの機能 { #pydantic-features }

**FastAPI** は <a href="https://docs.pydantic.dev/" class="external-link" target="_blank"><strong>Pydantic</strong></a> と完全に互換性があり（かつそれに基づいています）。そのため、手元の Pydantic の追加コードも動作します。

Pydantic に基づく外部ライブラリ（データベース用の <abbr title="Object-Relational Mapper - オブジェクト関係マッパー">ORM</abbr>、<abbr title="Object-Document Mapper - オブジェクトドキュメントマッパー">ODM</abbr> など）も含まれます。

これは、すべてが自動的に検証されるため、多くの場合、リクエストから取得したオブジェクトを **そのままデータベースに** 渡せることを意味します。

逆方向も同様で、多くの場合、データベースから取得したオブジェクトを **そのままクライアントに** 渡せます。

**FastAPI** では **Pydantic** のすべての機能が利用できます（FastAPI はデータ処理のすべてで Pydantic に基づいています）:

* **brainfuck なし**：
    * スキーマ定義のための新しいマイクロ言語を学ぶ必要はありません。
    * Python の型を知っていれば、Pydantic の使い方もわかります。
* **<abbr title="Integrated Development Environment - 統合開発環境: コードエディタに類似">IDE</abbr>/<dfn title="コードのエラーを検査するプログラム">リンター</dfn>/思考** と気持ちよく連携します：
    * Pydantic のデータ構造は、あなたが定義するクラスの単なるインスタンスなので、オートコンプリート、リンティング、mypy、そしてあなたの直感が、検証済みデータに対して適切に機能します。
* **複雑な構造** を検証：
    * 階層的な Pydantic モデルや、Python の `typing` にある `List` や `Dict` などを利用できます。
    * さらにバリデータにより、複雑なデータスキーマを明確かつ容易に定義・検査でき、JSON Schema として文書化できます。
    * 深く **ネストされた JSON** オブジェクトを扱え、それらすべてを検証してアノテーションを付与できます。
* **拡張可能**：
    * Pydantic ではカスタムデータ型を定義できますし、バリデータデコレーターで装飾したモデルメソッドで検証を拡張できます。
* テストカバレッジ 100%。
