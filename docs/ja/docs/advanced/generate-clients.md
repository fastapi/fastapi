# SDK の生成 { #generating-sdks }

**FastAPI** は **OpenAPI** 仕様に基づいているため、その API は多くのツールが理解できる標準形式で記述できます。

これにより、最新の**ドキュメント**、複数言語のクライアントライブラリ（<abbr title="Software Development Kits - ソフトウェア開発キット">**SDKs**</abbr>）、そしてコードと同期し続ける**テスト**や**自動化ワークフロー**を容易に生成できます。

本ガイドでは、FastAPI バックエンド向けの **TypeScript SDK** を生成する方法を説明します。

## オープソースの SDK ジェネレータ { #open-source-sdk-generators }

多用途な選択肢として <a href="https://openapi-generator.tech/" class="external-link" target="_blank">OpenAPI Generator</a> があります。これは**多数のプログラミング言語**をサポートし、OpenAPI 仕様から SDK を生成できます。

**TypeScript クライアント**向けには、<a href="https://heyapi.dev/" class="external-link" target="_blank">Hey API</a> が目的特化のソリューションで、TypeScript エコシステムに最適化された体験を提供します。

他の SDK ジェネレータは <a href="https://openapi.tools/#sdk" class="external-link" target="_blank">OpenAPI.Tools</a> でも見つけられます。

/// tip | 豆知識

FastAPI は自動的に **OpenAPI 3.1** の仕様を生成します。したがって、使用するツールはこのバージョンをサポートしている必要があります。

///

## FastAPI スポンサーによる SDK ジェネレータ { #sdk-generators-from-fastapi-sponsors }

このセクションでは、FastAPI をスポンサーしている企業による、**ベンチャー支援**および**企業支援**のソリューションを紹介します。これらの製品は、高品質な生成 SDK に加えて、**追加機能**や**統合**を提供します。

✨ [**FastAPI をスポンサーする**](../help-fastapi.md#sponsor-the-author){.internal-link target=_blank} ✨ ことで、これらの企業はフレームワークとその**エコシステム**の健全性と**持続可能性**を支援しています。

この支援は、FastAPI の**コミュニティ**（皆さん）への強いコミットメントの表明でもあり、**優れたサービス**の提供だけでなく、堅牢で発展するフレームワーク FastAPI を支える姿勢を示しています。🙇

例えば、次のようなものがあります:

* <a href="https://speakeasy.com/editor?utm_source=fastapi+repo&utm_medium=github+sponsorship" class="external-link" target="_blank">Speakeasy</a>
* <a href="https://www.stainless.com/?utm_source=fastapi&utm_medium=referral" class="external-link" target="_blank">Stainless</a>
* <a href="https://developers.liblab.com/tutorials/sdk-for-fastapi?utm_source=fastapi" class="external-link" target="_blank">liblab</a>

これらのソリューションの中にはオープンソースや無料枠を提供するものもあり、金銭的コミットメントなしで試すことができます。他の商用 SDK ジェネレータも存在し、オンラインで見つけられます。🤓

## TypeScript SDK を作成する { #create-a-typescript-sdk }

まずは簡単な FastAPI アプリから始めます:

{* ../../docs_src/generate_clients/tutorial001_py310.py hl[7:9,12:13,16:17,21] *}

ここで、*path operation* はリクエストとレスポンスのペイロードに使用するモデルを定義しており、`Item` と `ResponseMessage` を使っています。

### API ドキュメント { #api-docs }

`/docs` に移動すると、リクエストで送信・レスポンスで受信するデータの**スキーマ**が表示されます:

<img src="/img/tutorial/generate-clients/image01.png">

これらのスキーマは、アプリ内でモデルとして宣言されているため表示されます。

その情報はアプリの **OpenAPI スキーマ**に含まれ、API ドキュメントに表示されます。

OpenAPI に含まれるこれらのモデル情報を使って、**クライアントコードを生成**できます。

### Hey API { #hey-api }

モデルを備えた FastAPI アプリがあれば、Hey API で TypeScript クライアントを生成できます。最も手早い方法は npx を使うことです。

```sh
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

これで TypeScript SDK が `./src/client` に生成されます。

<a href="https://heyapi.dev/openapi-ts/get-started" class="external-link" target="_blank">`@hey-api/openapi-ts` のインストール方法</a>や、<a href="https://heyapi.dev/openapi-ts/output" class="external-link" target="_blank">生成物の詳細</a>は公式サイトを参照してください。

### SDK の利用 { #using-the-sdk }

これでクライアントコードを import して利用できます。例えば次のようになり、メソッドに対して補完が効きます:

<img src="/img/tutorial/generate-clients/image02.png">

送信するペイロードにも補完が適用されます:

<img src="/img/tutorial/generate-clients/image03.png">

/// tip | 豆知識

FastAPI アプリの `Item` モデルで定義した `name` と `price` に補完が効いている点に注目してください。

///

送信データに対するインラインエラーも表示されます:

<img src="/img/tutorial/generate-clients/image04.png">

レスポンスオブジェクトにも補完があります:

<img src="/img/tutorial/generate-clients/image05.png">

## タグ付きの FastAPI アプリ { #fastapi-app-with-tags }

実運用ではアプリは大きくなり、*path operation* のグループ分けにタグを使うことが多いでしょう。

例えば **items** 用と **users** 用のセクションがあり、タグで分けられます:

{* ../../docs_src/generate_clients/tutorial002_py310.py hl[21,26,34] *}

### タグ付き TypeScript クライアントの生成 { #generate-a-typescript-client-with-tags }

タグを用いた FastAPI アプリからクライアントを生成すると、通常クライアント側のコードもタグごとに分割されます。

これにより、クライアントコードも正しく整理・グルーピングされます:

<img src="/img/tutorial/generate-clients/image06.png">

この例では次のようになります:

* `ItemsService`
* `UsersService`

### クライアントのメソッド名 { #client-method-names }

現状では、生成されるメソッド名（`createItemItemsPost` など）はあまりきれいではありません:

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

これは、クライアントジェネレータが各 *path operation* の OpenAPI 内部の **operation ID** を用いるためです。

OpenAPI では operation ID は全ての *path operation* を通して一意である必要があります。そのため FastAPI は**関数名**、**パス**、**HTTP メソッド/オペレーション**を組み合わせて operation ID を生成し、一意性を保証します。

次にこれを改善する方法を示します。🤓

## カスタム operation ID とより良いメソッド名 { #custom-operation-ids-and-better-method-names }

operation ID の**生成方法**を**変更**して簡潔にし、クライアント側の**メソッド名をシンプル**にできます。

この場合でも各 operation ID が**一意**であることは別の方法で保証する必要があります。

例えば、各 *path operation* にタグを付け、**タグ**と *path operation* の**名前**（関数名）から operation ID を生成できます。

### 一意 ID 生成関数のカスタマイズ { #custom-generate-unique-id-function }

FastAPI は各 *path operation* に**一意 ID**を用いており、これは **operation ID** のほか、必要に応じてリクエストやレスポンスのカスタムモデル名にも使われます。

この関数はカスタマイズ可能です。`APIRoute` を受け取り、文字列を返します。

例えばここでは、最初のタグ（通常は 1 つ）と *path operation* 名（関数名）を使います。

そのカスタム関数を **FastAPI** の `generate_unique_id_function` パラメータに渡します:

{* ../../docs_src/generate_clients/tutorial003_py310.py hl[6:7,10] *}

### カスタム operation ID で TypeScript クライアントを生成 { #generate-a-typescript-client-with-custom-operation-ids }

この状態でクライアントを再生成すると、メソッド名が改善されています:

<img src="/img/tutorial/generate-clients/image07.png">

ご覧のとおり、メソッド名はタグ名と関数名のみになり、URL パスや HTTP オペレーションの情報は含まれません。

### クライアント生成向けの OpenAPI 仕様の前処理 { #preprocess-the-openapi-specification-for-the-client-generator }

それでも生成コードには**重複情報**が残っています。

`ItemsService`（タグ由来）から items 関連であることはすでに分かるのに、メソッド名にもタグ名が前置されています。😕

OpenAPI 全体としては operation ID の**一意性**のために、このプレフィックスを維持したい場合があるでしょう。

しかし生成クライアント用には、クライアントを生成する直前に OpenAPI の operation ID を**加工**して、メソッド名をより**見やすく**、**クリーン**にできます。

OpenAPI の JSON を `openapi.json` として保存し、次のようなスクリプトで**そのタグのプレフィックスを除去**できます:

{* ../../docs_src/generate_clients/tutorial004_py310.py *}

//// tab | Node.js

```Javascript
{!> ../../docs_src/generate_clients/tutorial004.js!}
```

////

これにより operation ID は `items-get_items` のような形から単なる `get_items` に置き換わり、クライアントジェネレータはより簡潔なメソッド名を生成できます。

### 前処理済み OpenAPI から TypeScript クライアントを生成 { #generate-a-typescript-client-with-the-preprocessed-openapi }

生成元が `openapi.json` になったので、入力の場所を更新します:

```sh
npx @hey-api/openapi-ts -i ./openapi.json -o src/client
```

新しいクライアントを生成すると、**クリーンなメソッド名**になり、**補完**や**インラインエラー**などもそのまま利用できます:

<img src="/img/tutorial/generate-clients/image08.png">

## 利点 { #benefits }

自動生成されたクライアントを使うと、次のような対象で**補完**が得られます:

* メソッド
* 本体のリクエストペイロード、クエリパラメータ等
* レスポンスのペイロード

また、あらゆる箇所で**インラインエラー**も得られます。

バックエンドコードを更新してフロントエンドを**再生成**すれば、新しい *path operation* はメソッドとして追加され、古いものは削除され、その他の変更も生成コードに反映されます。🤓

つまり、変更があれば自動的にクライアントコードに**反映**されます。クライアントを**ビルド**すれば、使用データに**不整合**があればエラーになります。

その結果、多くのエラーを開発の初期段階で**早期発見**でき、本番で最終ユーザーに不具合が現れてから原因をデバッグする必要がなくなります。✨
