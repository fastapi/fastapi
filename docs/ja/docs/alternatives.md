# 代替ツールから受けたインスピレーションと比較

何が**FastAPI**にインスピレーションを与えたのか、他の代替ツールと比較してどうか、そしてそこから何を学んだのかについて。

## はじめに

**FastAPI**は、代替ツールのこれまでの働きがなければ存在しなかったでしょう。

以前に作られた多くのツールが、作成における刺激として役立ってきました。

私は数年前から新しいフレームワークの作成を避けてきました。まず、**FastAPI**でカバーされているすべての機能を、さまざまなフレームワーク、プラグイン、ツールを使って解決しようとしました。

しかし、その時点では、これらの機能をすべて提供し、以前のツールから優れたアイデアを取り入れ、可能な限り最高の方法でそれらを組み合わせ、それまで利用できなかった言語機能 (Python 3.6 以降の型ヒント) を利用したものを作る以外に選択肢はありませんでした。

## 以前のツール

### <a href="https://www.djangoproject.com/" class="external-link" target="_blank">Django</a>

Python のフレームワークの中で最もポピュラーで、広く信頼されています。Instagram のようなシステムの構築に使われています。

リレーショナルデータベース (MySQL や PostgreSQL など) と比較的強固に結合されているので、NoSQL データベース (Couchbase、MongoDB、Cassandra など) をメインに利用することは簡単ではありません。

バックエンドで HTML を生成するために作られたものであり、現代的なフロントエンド (React や Vue.js、Angular など) や、他のシステム (IoT デバイスなど) と通信する API を構築するために作られたものではありません。

### <a href="https://www.django-rest-framework.org/" class="external-link" target="_blank">Django REST Framework</a>

Django REST Framework は、Django を下敷きにして Web API を構築する柔軟なツールキットとして、API の機能を向上させるために作られました。

Mozilla、Red Hat、Eventbrite など多くの企業で利用されています。

これは**自動的な API ドキュメント生成**の最初の例であり、これは**FastAPI**に向けた「調査」を触発した最初のアイデアの一つでした。

/// note | 備考

Django REST Framework は Tom Christie によって作成されました。Starlette と Uvicorn の生みの親であり、**FastAPI**のベースとなっています。

///

/// check | **FastAPI**へ与えたインスピレーション

自動で API ドキュメントを生成する Web ユーザーインターフェースを持っている点。

///

### <a href="http://flask.pocoo.org/" class="external-link" target="_blank">Flask</a>

Flask は「マイクロフレームワーク」であり、データベースとの統合のような Django がデフォルトで持つ多くの機能は含まれていません。

このシンプルさと柔軟性により、メインのデータストレージシステムとして NoSQL データベースを使用するといったようなことが可能になります。

非常にシンプルなので、ドキュメントはいくつかの点でやや技術的でありますが、比較的直感的に学ぶことができます。

また、データベースやユーザ管理、あるいは Django にあらかじめ組み込まれている多くの機能を必ずしも必要としないアプリケーションにもよく使われています。これらの機能の多くはプラグインで追加することができます。

このようにパーツを分離し、必要なものを正確にカバーするために拡張できる「マイクロフレームワーク」であることは、私が残しておきたかった重要な機能でした。

Flask のシンプルさを考えると、API を構築するのに適しているように思えました。次に見つけるべきは、Flask 用の「Django REST Framework」でした。

/// check | **FastAPI**へ与えたインスピレーション

マイクロフレームワークであること。ツールやパーツを目的に合うように簡単に組み合わせられる点。

シンプルで簡単なルーティングの仕組みを持っている点。

///

### <a href="http://docs.python-requests.org" class="external-link" target="_blank">Requests</a>

**FastAPI**は実際には**Requests**の代替ではありません。それらのスコープは大きく異なります。

実際には FastAPI アプリケーションの*内部*で Requests を使用するのが一般的です。

しかし、FastAPI は Requests からかなりのインスピレーションを得ています。

**Requests**は (クライアントとして) API と*通信*するためのライブラリであり、**FastAPI**は (サーバーとして) API を*構築*するためのライブラリです。

これらは多かれ少なかれ両端にあり、お互いを補完し合っています。

Requests は非常にシンプルかつ直感的なデザインで使いやすく、適切なデフォルト値を設定しています。しかし同時に、非常に強力でカスタマイズも可能です。

公式サイトで以下のように言われているのは、それが理由です。

> Requests は今までで最もダウンロードされた Python パッケージである

使い方はとても簡単です。例えば、`GET`リクエストを実行するには、このように書けば良いです:

```Python
response = requests.get("http://example.com/some/url")
```

対応する FastAPI のパスオペレーションはこのようになります:

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

`requests.get(...)` と`@app.get(...)` には類似点が見受けられます。

/// check | **FastAPI**へ与えたインスピレーション

- シンプルで直感的な API を持っている点。
- HTTP メソッド名を直接利用し、単純で直感的である。
- 適切なデフォルト値を持ちつつ、強力なカスタマイズ性を持っている。

///

### <a href="https://swagger.io/" class="external-link" target="_blank">Swagger</a> / <a href="https://github.com/OAI/OpenAPI-Specification/" class="external-link" target="_blank">OpenAPI</a>

私が Django REST Framework に求めていた主な機能は、API の自動的なドキュメント生成でした。

そして、Swagger と呼ばれる、 JSON (または YAML、JSON の拡張版) を使って API をドキュメント化するための標準があることを知りました。

そして、Swagger API 用の Web ユーザーインターフェースが既に作成されていました。つまり、API 用の Swagger ドキュメントを生成することができれば、この Web ユーザーインターフェースを自動的に使用することができるようになります。

ある時点で、Swagger は Linux Foundation に寄贈され、OpenAPI に改名されました。

そのため、バージョン 2.0 では「Swagger」、バージョン 3 以上では「OpenAPI」と表記するのが一般的です。

/// check | **FastAPI**へ与えたインスピレーション

独自のスキーマの代わりに、API 仕様のオープンな標準を採用しました。

そして、標準に基づくユーザーインターフェースツールを統合しています。

- <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>
- <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>

この二つは人気で安定したものとして選択されましたが、少し検索してみると、 (**FastAPI**と同時に使用できる) OpenAPI のための多くの代替となるツールを見つけることができます。

///

### Flask REST フレームワーク

いくつかの Flask REST フレームワークがありますが、それらを調査してみたところ、多くのものが不適切な問題が残ったまま、中断されたり放置されていることがわかりました。

### <a href="https://marshmallow.readthedocs.io/en/3.0/" class="external-link" target="_blank">Marshmallow</a>

API システムで必要とされる主な機能の一つに、コード (Python) からデータを取り出して、ネットワークを介して送れるものに変換するデータの「<abbr title="marshalling, conversion">シリアライゼーション</abbr>」があります。例えば、データベースのデータを含むオブジェクトを JSON オブジェクトに変換したり、`datetime` オブジェクトを文字列に変換するなどです。

API が必要とするもう一つの大きな機能はデータのバリデーションであり、特定のパラメータが与えられた場合にデータが有効であることを確認することです。例えば、あるフィールドがランダムな文字列ではなく `int` であることなどです。これは特に受信するデータに対して便利です。

データバリデーションの仕組みがなければ、すべてのチェックを手作業でコードに実装しなければなりません。

これらの機能は、Marshmallow が提供するものです。Marshmallow は素晴らしいライブラリで、私も以前に何度も使ったことがあります。

しかし、それは Python の型ヒントが存在する前に作られたものです。そのため、すべての<abbr title="データがどのように形成されるべきかの定義">スキーマ</abbr>を定義するためには、Marshmallow が提供する特定のユーティリティやクラスを使用する必要があります。

/// check | **FastAPI**へ与えたインスピレーション

コードで「スキーマ」を定義し、データの型やバリデーションを自動で提供する点。

///

### <a href="https://webargs.readthedocs.io/en/latest/" class="external-link" target="_blank">Webargs</a>

API に求められる他の大きな機能として、<abbr title="Pythonデータの読み込みと変換">受信したリクエストデータのパース</abbr>があります。

Webargs は Flask をはじめとするいくつかのフレームワークの上にそれを提供するために作られたツールです。

データのバリデーションを行うために内部では Marshmallow を使用しており、同じ開発者によって作られました。

素晴らしいツールで、私も**FastAPI**を持つ前はよく使っていました。

/// info | 情報

Webargs は、Marshmallow と同じ開発者により作られました。

///

/// check | **FastAPI**へ与えたインスピレーション

受信したデータに対する自動的なバリデーションを持っている点。

///

### <a href="https://apispec.readthedocs.io/en/stable/" class="external-link" target="_blank">APISpec</a>

Marshmallow と Webargs はバリデーション、パース、シリアライゼーションをプラグインとして提供しています。

しかし、ドキュメントはまだ不足しています。そこで APISpec が作られました。

これは多くのフレームワーク用のプラグインです (Starlette 用のプラグインもあります) 。

仕組みとしては、各ルーティング関数の docstring に YAML 形式でスキーマの定義を記述します。

そして、OpenAPI スキーマを生成してくれます。

Flask, Starlette, Responder などにおいてはそのように動作します。

しかし、Python の文字列 (大きな YAML) の中に、小さな構文があるという問題があります。

エディタでは、この問題を解決することはできません。また、パラメータや Marshmallow スキーマを変更したときに、YAML の docstring を変更するのを忘れてしまうと、生成されたスキーマが古くなってしまいます。

/// info | 情報

APISpec は、Marshmallow と同じ開発者により作成されました。

///

/// check | **FastAPI**へ与えたインスピレーション

OpenAPI という、API についてのオープンな標準をサポートしている点。

///

### <a href="https://flask-apispec.readthedocs.io/en/latest/" class="external-link" target="_blank">Flask-apispec</a>

Webargs、Marshmallow、APISpec を連携させた Flask プラグインです。

Webargs と Marshmallow の情報から、APISpec を使用して OpenAPI スキーマを自動的に生成します。

これは素晴らしいツールで、非常に過小評価されています。多くの Flask プラグインよりもずっと人気があるべきです。ドキュメントがあまりにも簡潔で抽象的であるからかもしれません。

これにより、Python の docstring に YAML (別の構文) を書く必要がなくなりました。

Flask、Flask-apispec、Marshmallow、Webargs の組み合わせは、**FastAPI**を構築するまで私のお気に入りのバックエンドスタックでした。

これを使うことで、いくつかの Flask フルスタックジェネレータを作成することになりました。これらは私 (といくつかの外部のチーム) が今まで使ってきたメインのスタックです。

- <a href="https://github.com/tiangolo/full-stack" class="external-link" target="_blank">https://github.com/tiangolo/full-stack</a>
- <a href="https://github.com/tiangolo/full-stack-flask-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchbase</a>
- <a href="https://github.com/tiangolo/full-stack-flask-couchdb" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchdb</a>

そして、これらのフルスタックジェネレーターは、[**FastAPI** Project Generators](project-generation.md){.internal-link target=\_blank}の元となっていました。

/// info | 情報

Flask-apispec は Marshmallow と同じ開発者により作成されました。

///

/// check | **FastAPI**へ与えたインスピレーション

シリアライゼーションとバリデーションを定義したコードから、OpenAPI スキーマを自動的に生成する点。

///

### <a href="https://nestjs.com/" class="external-link" target="_blank">NestJS</a> (と<a href="https://angular.io/" class="external-link" target="_blank">Angular</a>)

NestJS は Angular にインスパイアされた JavaScript (TypeScript) Node.JS フレームワークで、Python ですらありません。

Flask-apispec でできることと多少似たようなことを実現しています。

Angular 2 にインスピレーションを受けた、統合された依存性注入の仕組みを持っています。(私が知っている他の依存性注入の仕組みと同様に) 「injectable」を事前に登録しておく必要があるため、冗長性とコードの繰り返しが発生します。

パラメータは TypeScript の型で記述されるので (Python の型ヒントに似ています) 、エディタのサポートはとても良いです。

しかし、TypeScript のデータは JavaScript へのコンパイル後には残されないため、バリデーション、シリアライゼーション、ドキュメント化を同時に定義するのに型に頼ることはできません。そのため、バリデーション、シリアライゼーション、スキーマの自動生成を行うためには、多くの場所でデコレータを追加する必要があり、非常に冗長になります。

入れ子になったモデルをうまく扱えません。そのため、リクエストの JSON ボディが内部フィールドを持つ JSON オブジェクトで、それが順番にネストされた JSON オブジェクトになっている場合、適切にドキュメント化やバリデーションをすることができません。

/// check | **FastAPI**へ与えたインスピレーション

素晴らしいエディターの補助を得るために、Python の型ヒントを利用している点。

強力な依存性注入の仕組みを持ち、コードの繰り返しを最小化する方法を見つけた点。

///

### <a href="https://sanic.readthedocs.io/en/latest/" class="external-link" target="_blank">Sanic</a>

`asyncio`に基づいた、Python のフレームワークの中でも非常に高速なものの一つです。Flask と非常に似た作りになっています。

/// note | 技術詳細

Python の`asyncio`ループの代わりに、`uvloop`が利用されています。それにより、非常に高速です。

`Uvicorn`と`Starlette`に明らかなインスピレーションを与えており、それらは現在オープンなベンチマークにおいて Sanic より高速です。

///

/// check | **FastAPI**へ与えたインスピレーション

物凄い性能を出す方法を見つけた点。

**FastAPI**が、(サードパーティのベンチマークによりテストされた) 最も高速なフレームワークである Starlette に基づいている理由です。

///

### <a href="https://falconframework.org/" class="external-link" target="_blank">Falcon</a>

Falcon はもう一つの高性能 Python フレームワークで、ミニマムに設計されており、Hug のような他のフレームワークの基盤として動作します。

Python のウェブフレームワーク標準規格 (WSGI) を使用していますが、それは同期的であるため WebSocket などの利用には対応していません。とはいえ、それでも非常に高い性能を持っています。

これは、「リクエスト」と「レスポンス」の 2 つのパラメータを受け取る関数を持つように設計されています。そして、リクエストからデータを「読み込み」、レスポンスにデータを「書き込み」ます。この設計のため、Python 標準の型ヒントでリクエストのパラメータやボディを関数の引数として宣言することはできません。

そのため、データのバリデーション、シリアライゼーション、ドキュメント化は、自動的にできずコードの中で行わなければなりません。あるいは、Hug のように Falcon の上にフレームワークとして実装されなければなりません。このような分断は、パラメータとして 1 つのリクエストオブジェクトと 1 つのレスポンスオブジェクトを持つという Falcon のデザインにインスピレーションを受けた他のフレームワークでも起こります。

/// check | **FastAPI**へ与えたインスピレーション

素晴らしい性能を得るための方法を見つけた点。

Hug (Hug は Falcon をベースにしています) と一緒に、**FastAPI**が`response`引数を関数に持つことにインスピレーションを与えました。

**FastAPI**では任意ですが、ヘッダーや Cookie やステータスコードを設定するために利用されています。

///

### <a href="https://moltenframework.com/" class="external-link" target="_blank">Molten</a>

**FastAPI**を構築する最初の段階で Molten を発見しました。そして、それは非常に似たようなアイデアを持っています。

- Python の型ヒントに基づいている
- これらの型から行われるバリデーションとドキュメント化
- 依存性注入の仕組み

Pydantic のようなデータのバリデーション、シリアライゼーション、ドキュメント化をするサードパーティライブラリを使用せず、独自のものを持っています。そのため、これらのデータ型の定義は簡単には再利用できません。

もう少し冗長な設定が必要になります。また、 (ASGI ではなく) WSGI に基づいているので、Uvicorn や Starlette や Sanic のようなツールが提供する高性能を得られるようには設計されていません。

依存性注入の仕組みは依存性の事前登録が必要で、宣言された型に基づいて依存性が解決されます。そのため、特定の型を提供する「コンポーネント」を複数宣言することはできません。

ルーティングは一つの場所で宣言され、他の場所で宣言された関数を使用します (エンドポイントを扱う関数のすぐ上に配置できるデコレータを使用するのではなく) 。これは Flask (や Starlette) よりも、Django に近いです。これは、比較的緊密に結合されているものをコードの中で分離しています。

/// check | **FastAPI**へ与えたインスピレーション

モデルの属性の「デフォルト」値を使用したデータ型の追加バリデーションを定義します。これはエディタの補助を改善するもので、以前は Pydantic では利用できませんでした。

同様の方法でのバリデーションの宣言をサポートするよう、Pydantic を部分的にアップデートするインスピーレションを与えました。(現在はこれらの機能は全て Pydantic で可能となっています。)

///

### <a href="http://www.hug.rest/" class="external-link" target="_blank">Hug</a>

Hug は、Python の型ヒントを利用して API パラメータの型宣言を実装した最初のフレームワークの 1 つです。これは素晴らしいアイデアで、他のツールが同じことをするきっかけとなりました。

Hug は標準の Python 型の代わりにカスタム型を宣言に使用していましたが、それでも大きな進歩でした。

また、JSON で API 全体を宣言するカスタムスキーマを生成した最初のフレームワークの 1 つでもあります。

OpenAPI や JSON Schema のような標準に基づいたものではありませんでした。そのため、Swagger UI のような他のツールと統合するのは簡単ではありませんでした。しかし、繰り返しになりますが、これは非常に革新的なアイデアでした。

同じフレームワークを使って API と CLI を作成できる、面白く珍しい機能を持っています。

以前の Python の同期型 Web フレームワーク標準 (WSGI) をベースにしているため、Websocket などは扱えませんが、それでも高性能です。

/// info | 情報

Hug は Timothy Crosley により作成されました。彼は<a href="https://github.com/timothycrosley/isort" class="external-link" target="_blank">`isort`</a>など、Python のファイル内のインポートの並び替えを自動的におこうなう素晴らしいツールの開発者です。

///

/// check | **FastAPI**へ与えたインスピレーション

Hug は APIStar に部分的なインスピレーションを与えており、私が発見した中では APIStar と同様に最も期待の持てるツールの一つでした。

Hug は、**FastAPI**が Python の型ヒントを用いてパラメータを宣言し自動的に API を定義するスキーマを生成することを触発しました。

Hug は、**FastAPI**がヘッダーやクッキーを設定するために関数に `response`引数を宣言することにインスピレーションを与えました。

///

### <a href="https://github.com/encode/apistar" class="external-link" target="_blank">APIStar</a> (<= 0.5)

**FastAPI**を構築することを決める直前に、**APIStar**サーバーを見つけました。それは私が探していたものがほぼすべて含まれており、素晴らしいデザインでした。

これは、私がこれまでに見た中で (NestJS や Molten の前に) Python の型ヒントを使ってパラメータやリクエストを宣言するフレームワークの最初の実装の一つでした。Hug と多かれ少なかれ同時期に見つけました。ただ、APIStar は OpenAPI 標準を使っていました。

いくつかの場所で同じ型ヒントを元に、データの自動バリデーション、データのシリアライゼーション、OpenAPI スキーマの生成を行っていました。

ボディのスキーマ定義には Pydantic のような Python の型ヒントは使われておらず、もう少し Marshmallow に似ていたので、エディタの補助はあまり良くないかもしれませんが、それでも APIStar は利用可能な最良の選択肢でした。

当時のベンチマークでは最高のパフォーマンスを発揮していました (Starlette のみが上回っていました) 。

最初は自動的な API のドキュメント化の Web UI を持っていませんでしたが、Swagger UI を追加できることはわかっていました。

依存性注入の仕組みを持っていました。上記で説明した他のツールのようにコンポーネントの事前登録が必要でした。しかし、それでも素晴らしい機能でした。

セキュリティの統合がなかったので、Flask-apispec を元にしたフルスタックジェネレータにあるすべての機能を置き換えることはできませんでした。私はその機能を追加するプルリクエストを作成するというプロジェクトのバックログを持っていました。

しかし、その後、プロジェクトの焦点が変わりました。

制作者は Starlette に集中する必要があったため、API ウェブフレームワークではなくなりました。

今では APIStar は OpenAPI 仕様を検証するためのツールセットであり、ウェブフレームワークではありません。

/// info | 情報

APIStar は Tom Christie により開発されました。以下の開発者でもあります:

- Django REST Framework
- Starlette (**FastAPI**のベースになっています)
- Uvicorn (Starlette や**FastAPI**で利用されています)

///

/// check | **FastAPI**へ与えたインスピレーション

存在そのもの。

複数の機能 (データのバリデーション、シリアライゼーション、ドキュメント化) を同じ Python 型で宣言し、同時に優れたエディタの補助を提供するというアイデアは、私にとって素晴らしいアイデアでした。

そして、長い間同じようなフレームワークを探し、多くの異なる代替ツールをテストした結果、APIStar が最良の選択肢となりました。

その後、APIStar はサーバーとして存在しなくなり、Starlette が作られ、そのようなシステムのための新しくより良い基盤となりました。これが**FastAPI**を構築するための最終的なインスピレーションでした。

私は、これまでのツールから学んだことをもとに、機能や型システムなどの部分を改善・拡充しながら、**FastAPI**を APIStar の「精神的な後継者」と考えています。

///

## **FastAPI**が利用しているもの

### <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>

Pydantic は、Python の型ヒントを元にデータのバリデーション、シリアライゼーション、 (JSON Schema を使用した) ドキュメントを定義するライブラリです。

そのため、非常に直感的です。

Marshmallow に匹敵しますが、ベンチマークでは Marshmallow よりも高速です。また、Python の型ヒントを元にしているので、エディタの補助が素晴らしいです。

/// check | **FastAPI**での使用用途

データのバリデーション、データのシリアライゼーション、自動的なモデルの (JSON Schema に基づいた) ドキュメント化の全てを扱えます。

**FastAPI**は JSON Schema のデータを OpenAPI に利用します。

///

### <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a>

Starlette は、軽量な<abbr title="非同期Python webを構築するための新標準">ASGI</abbr>フレームワーク/ツールキットで、高性能な非同期サービスの構築に最適です。

非常にシンプルで直感的です。簡単に拡張できるように設計されており、モジュール化されたコンポーネントを持っています。

以下のような特徴があります。

- 非常に感動的な性能。
- WebSocket のサポート。
- GraphQL のサポート。
- インプロセスのバックグラウンドタスク。
- 起動およびシャットダウンイベント。
- requests に基づいて構築されたテストクライアント。
- CORS、GZip、静的ファイル、ストリーミング応答。
- セッションとクッキーのサポート。
- 100%のテストカバレッジ。
- 100%の型注釈付きコードベース。
- ハードな依存関係はない。

Starlette は、現在テストされている Python フレームワークの中で最も速いフレームワークです。フレームワークではなくサーバーである Uvicorn だけが上回っています。

Starlette は基本的な Web マイクロフレームワークの機能をすべて提供します。

しかし、自動的なデータバリデーション、シリアライゼーション、ドキュメント化は提供していません。

これは **FastAPI** が追加する主な機能の一つで、すべての機能は Python の型ヒントに基づいています (Pydantic を使用しています) 。これに加えて、依存性注入の仕組み、セキュリティユーティリティ、OpenAPI スキーマ生成などがあります。

/// note | 技術詳細

ASGI は Django のコアチームメンバーにより開発された新しい「標準」です。まだ「Python の標準 (PEP) 」ではありませんが、現在そうなるように進めています。

しかしながら、いくつかのツールにおいてすでに「標準」として利用されています。このことは互換性を大きく改善するもので、Uvicorn から他の ASGI サーバー (Daphne や Hypercorn) に乗り換えることができたり、あなたが`python-socketio`のような ASGI 互換のツールを追加することもできます。

///

/// check | **FastAPI**での使用用途

web に関するコアな部分を全て扱います。その上に機能を追加します。

`FastAPI`クラスそのものは、`Starlette`クラスを直接継承しています。

基本的には Starlette の強化版であるため、Starlette で可能なことは**FastAPI**で直接可能です。

///

### <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>

Uvicorn は非常に高速な ASGI サーバーで、uvloop と httptools により構成されています。

ウェブフレームワークではなくサーバーです。例えば、パスルーティングのツールは提供していません。それらは、Starlette (や**FastAPI**) のようなフレームワークがその上で提供するものです。

Starlette や**FastAPI**のサーバーとして推奨されています。

/// check | **FastAPI**が推奨する理由

**FastAPI**アプリケーションを実行するメインのウェブサーバーである点。

Gunicorn と組み合わせることで、非同期でマルチプロセスなサーバーを持つことがきます。

詳細は[デプロイ](deployment/index.md){.internal-link target=\_blank}の項目で確認してください。

///

## ベンチマーク と スピード

Uvicorn、Starlette、FastAPI の違いを理解、比較、確認するには、[ベンチマーク](benchmarks.md){.internal-link target=\_blank}を確認してください。
