# 機能

## FastAPI の機能

**FastAPI** は以下の機能をもちます:

### オープンスタンダード準拠

- API 作成のための<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a>。これは、<abbr title="also known as: endpoints, routes">path</abbr> <abbr title="also known as HTTP methods, as POST, GET, PUT, DELETE">operations</abbr>の宣言、パラメータ、ボディリクエスト、セキュリティなどを含んでいます。
- <a href="http://json-schema.org/" class="external-link" target="_blank"><strong>JSON スキーマ</strong></a>を使用したデータモデルのドキュメント自動生成（OpenAPI は JSON スキーマに基づいている）。
- 綿密な調査の結果、上層に後付けするのではなく、これらの基準に基づいて設計されました。
- これにより、多くの言語で自動 **クライアントコード生成** が可能です。

### 自動ドキュメント生成

対話的な API ドキュメントと探索的な web ユーザーインターフェースを提供します。フレームワークは OpenAPI を基にしているため、いくつかのオプションがあり、デフォルトで 2 つ含まれています。

- <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>で、インタラクティブな探索をしながら、ブラウザから直接 API を呼び出してテストが行えます。

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

- <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>を使用したもう一つの API ドキュメント生成。

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 現代的な Python

FastAPI の機能はすべて、標準の Python 3.8 型宣言に基づいています（Pydantic の功績）。新しい構文はありません。ただの現代的な標準の Python です。

（FastAPI を使用しない場合でも）Python の型の使用方法について簡単な復習が必要な場合は、短いチュートリアル（[Python Types](python-types.md){.internal-link target=\_blank}）を参照してください。

型を使用した標準的な Python を記述します:

```Python
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

これは以下のように用いられます:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

/// info | 情報

`**second_user_data` は以下を意味します：

`second_user_data`辞書のキーと値を直接、キーと値の引数として渡します。これは、`User(id=4, name="Mary", joined="2018-11-30")`と同等です。

///

### エディタのサポート

すべてのフレームワークは使いやすく直感的に使用できるように設計されており、すべての決定は開発を開始する前でも複数のエディターでテストされ、最高の開発体験が保証されます。

前回の Python 開発者調査では、<a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">最も使用されている機能が「オートコンプリート」であることが明らかになりました。</a>

**FastAPI** フレームワークは、この要求を満たすことを基本としています。オートコンプリートはどこでも機能します。

ドキュメントに戻る必要はほとんどありません。

エディターがどのように役立つかを以下に示します:

- <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>の場合:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

- <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>の場合:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

以前は不可能だと考えていたコードでさえ補完されます。例えば、リクエストからの JSON ボディ（ネストされている可能性がある）内の `price`キーです。

間違ったキー名を入力したり、ドキュメント間を行き来したり、上下にスクロールして`username`と`user_name`のどちらを使用したか調べたりする必要はもうありません。

### 簡潔

すべてに適切な**デフォルト**があり、オプションの構成ができます。必要なことを実行し、必要な API を定義するためにすべてのパラメーターを調整できます。

ただし、デフォルトでもすべて **うまくいきます**。

### 検証

- 以下の様な、ほとんどの（すべての？）Python **データ型**の検証:

  - JSON オブジェクト（`dict`）
  - 項目の型を定義する JSON 配列（`list`）
  - 最小長と最大長のある文字列（`str`）フィールド
  - 最小値と最大値のある数値（`int`、` float`）

- よりエキゾチックな型の検証：
  - URL
  - E メール
  - UUID
  - ...その他

すべての検証は、確立された堅牢な **Pydantic** によって処理されます。

### セキュリティと認証

セキュリティと認証が統合されています。 データベースまたはデータモデルについても妥協していません。

以下の OpenAPI で定義されているすべてのセキュリティスキームを含む:

- HTTP ベーシック
- **OAuth2**（**JWT トークン**も使用）。 JWT を使用した OAuth2 のチュートリアル（[OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=\_blank}）を確認してください。
- API キー：
  - ヘッダー
  - クエリパラメータ
  - クッキー、等

さらに、Starlette のすべてのセキュリティ機能も含みます（**セッション Cookie**を含む）。

これらは、システム、データストア、リレーショナルデータベース、NoSQL データベースなどと簡単に統合できる再利用可能なツールとコンポーネントとして構築されています。

### 依存性の注入（Dependency Injection）

FastAPI には非常に使いやすく、非常に強力な<abbr title='also known as "components", "resources", "services", "providers"'><strong>依存性の注入</strong></abbr>システムを備えています。

- 依存関係でさえも依存関係を持つことができ、階層または **依存関係の"グラフ"** を作成することができます。

- フレームワークによってすべて**自動的に処理**されます。
- すべての依存関係はリクエストからのデータを要請できて、**path operations の制約と自動ドキュメンテーションを拡張できます**。
- 依存関係で定義された _path operation_ パラメータも**自動検証**が可能です。
- 複雑なユーザー認証システム、**データベース接続**などのサポート
- **データベース、フロントエンドなどに対する妥協はありません**。それらすべてと簡単に統合できます。

### 無制限の「プラグイン」

他の方法では、それらを必要とせず、必要なコードをインポートして使用します。

統合は非常に簡単に使用できるように設計されており（依存関係を用いて）、_path operations_ で使用されているのと同じ構造と構文を使用して、2 行のコードでアプリケーションの「プラグイン」を作成できます。

### テスト

- <abbr title = "自動的にテストされるコードの量">テストカバレッジ</abbr> 100%
- <abbr title = "Python型アノテーション。これにより、ユーザーはより良いエディターと外部ツールのサポート受けられる。">型アノテーション</abbr>100%のコードベース
- 本番アプリケーションで使用されます

## Starlette の機能

**FastAPI**は、<a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette </strong></a>と完全に互換性があります（そしてベースになっています）。したがって、追加の Starlette コードがあれば、それも機能します。

`FastAPI`は実際には`Starlette`のサブクラスです。したがって、Starlette をすでに知っているか使用している場合は、ほとんどの機能が同じように機能します。

**FastAPI**を使用すると、以下のような、**Starlette**のすべての機能を利用できます（FastAPI は Starlette を強化したものにすぎないため）:

- 見事なパフォーマンス。<a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank"> **Node.JS**および**Go**に匹敵する、最速の Python フレームワークの 1 つです。</a>

- **WebSocket**のサポート
- **GraphQL**のサポート
- プロセス内バックグラウンドタスク
- 起動およびシャットダウンイベント
- `httpx`に基づいて構築されたテストクライアント
- **CORS**、GZip、静的ファイル、ストリーミング応答
- **セッションと Cookie**のサポート
- テストカバレッジ 100%
- 型アノテーション 100%のコードベース

## Pydantic の特徴

**FastAPI**は<a href="https://docs.pydantic.dev/" class="external-link" target="_blank"><strong>Pydantic </strong></a>と完全に互換性があります（そしてベースになっています）。したがって、追加の Pydantic コードがあれば、それも機能します。

データベースのために<abbr title = "Object-Relational Mapper">ORM</abbr>s や、<abbr title = "Object-Document Mapper">ODM</abbr>s などの、Pydantic に基づく外部ライブラリを備えています。

これは、すべてが自動的に検証されるため、多くの場合、リクエストから取得したオブジェクトを**データベースに直接**渡すことができるということを意味しています。

同じことがその逆にも当てはまり、多くの場合、データベースから取得したオブジェクトを**クライアントに直接**渡すことができます。

**FastAPI**を使用すると、**Pydantic**のすべての機能を利用できます（FastAPI が Pydantic に基づいてすべてのデータ処理を行っているため）。

- **brainfuck なし**：
  - スキーマ定義のためのマイクロ言語を新たに学習する必要はありません。
  - Python の型を知っている場合は、既に Pydantic の使用方法を知っているに等しいです。
- ユーザーの **<abbr title = "コードエディターに似た統合開発環境">IDE</abbr>/<abbr title = "コードエラーをチェックするプログラム">リンター</abbr>/思考 とうまく連携します**：
  - Pydantic のデータ構造は、ユーザーが定義するクラスの単なるインスタンスであるため、オートコンプリート、リンティング、mypy、およびユーザーの直感はすべて、検証済みのデータで適切に機能するはずです。
- **複雑な構造**を検証：
  - 階層的な Pydantic モデルや、Python の「`typing`」の「`list`」と「`dict`」などの利用。
  - バリデーターにより、複雑なデータスキーマを明確かつ簡単に定義、チェックし、JSON スキーマとして文書化できます。
  - 深く**ネストされた JSON**オブジェクトを作成し、それらすべてを検証してアノテーションを付けることができます。
- **拡張可能**：
  - Pydantic では、カスタムデータ型を定義できます。または、バリデーターデコレーターで装飾されたモデルのメソッドを使用して検証を拡張できます。
- テストカバレッジ 100%。
