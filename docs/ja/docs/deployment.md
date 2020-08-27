# デプロイ

**FastAPI** 製のアプリケーションは比較的容易にデプロイできます。

ユースケースや使用しているツールに依っていくつかの方法に分かれます。

次のセクションでいくつかの方法についてより詳しく説明します。

## FastAPIのバージョン

**FastAPI** は既に多くのアプリケーションやシステムに本番環境で使われています。また、100%のテストカバレッジを維持しています。しかし、活発な開発が続いています。

高頻度で新機能が追加され、定期的にバグが修正され、実装は継続的に改善されています。

これが現在のバージョンがいまだに `0.x.x` な理由であり、それぞれのバージョンは破壊的な変更がなされる可能性があります。<a href="https://semver.org/" class="external-link" target="_blank">セマンティック バージョニング</a>の規則に則っています。

**FastAPI** で本番用アプリケーションを今すぐに作成したら (すでに何度も経験しているかもしれませんが)、残りのコードが正しく動作するバージョンなのか確認しなければいけません。

### `fastapi` のバージョンを固定

最初にすべきことは、アプリケーションが正しく動作する **FastAPI** のバージョンを固定することです。

例えば、バージョン `0.45.0` を使っているとしましょう。

`requirements.txt` を使っているなら、以下の様にバージョンを指定できます:

```txt
fastapi==0.45.0
```

これは、バージョン `0.45.0` だけを使うことを意味します。

または、以下の様に固定することもできます:

```txt
fastapi>=0.45.0,<0.46.0
```

これは `0.45.0` 以上、`0.46.0` 未満のバージョンを使うことを意味します。例えば、バージョン `0.45.2` は使用可能です。

PoetryやPipenvなど、他のインストール管理ツールを使用している場合でも、それぞれパッケージのバージョンを指定する機能があります。

### 利用可能なバージョン

[Release Notes](release-notes.md){.internal-link target=_blank}で利用可能なバージョンが確認できます (最新版の確認などのため)。

### バージョンについて

Semantic Versioningの規約に従って、`1.0.0` 未満の全てのバージョンは破壊的な変更が加わる可能性があります。

FastAPIでは「パッチ」バージョンはバグ修正と非破壊的な変更に留めるという規約に従っています。

!!! tip "豆知識"
    「パッチ」は最後の数字を指します。例えば、`0.2.3` ではパッチバージョンは `3` です。

従って、以下の様なバージョンの固定が望ましいです:

```txt
fastapi>=0.45.0,<0.46.0
```

破壊的な変更と新機能実装は「マイナー」バージョンで加えられます。

!!! tip "豆知識"
    「マイナー」は真ん中の数字です。例えば、`0.2.3` ではマイナーバージョンは `2` です。

### FastAPIのバージョンのアップグレード

アプリケーションにテストを加えるべきです。

**FastAPI** では非常に簡単に実現できます (Starletteのおかげで)。ドキュメントを確認して下さい: [テスト](tutorial/testing.md){.internal-link target=_blank}

テストを加えた後で、**FastAPI** のバージョンをより最新のものにアップグレードし、テストを実行することで全てのコードが正常に動作するか確認できます。

全てが動作するか、修正を行った上で全てのテストを通過した場合、使用している`fastapi` のバージョンをより最新のバージョンに固定できます。

### Starletteについて

`Starlette` のバージョンは固定すべきではありません。

**FastAPI** は、バージョン毎にStarletteのより新しいバージョンを使用します。

よって、最適なStarletteのバージョン選択を**FastAPI** に任せることができます。

### Pydanticについて

Pydanticは自身のテストだけでなく**FastAPI** のためのテストを含んでいます。なので、Pydanticの新たなバージョン (`1.0.0` 以降)は全てFastAPIと整合性があります。

Pydanticのバージョンを、動作が保証できる`1.0.0`以降のいずれかのバージョンから`2.0.0` 未満の間に固定できます。

例えば:

```txt
pydantic>=1.2.0,<2.0.0
```

## Docker

このセクションでは以下の使い方の紹介とガイドへのリンクが確認できます:

* **5分**程度で、**FastAPI** のアプリケーションを、パフォーマンスを最大限に発揮するようなDokcerイメージ (コンテナ)にする。
* (オプション) 開発者として必要な範囲でHTTPSを理解する。
* **20分**程度で、自動的なHTTPS生成とともにDockerのSwarmモード クラスタをセットアップする (月5ドルのシンプルなサーバー上で)。
* **10分**程度で、DockerのSwarmモード クラスタを使って、HTTPSなどを使用した完全な**FastAPI** アプリケーションの作成とデプロイ。

デプロイのために、<a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a> を利用できます。セキュリティ、再現性、開発のシンプルさなどに利点があります。

Dockerを使う場合、公式のDokcerイメージが利用可能です:

### <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>

このイメージは「自動チューニング」機構を含んでいます。犠牲を払うことなく、ただコードを加えるだけで自動的に高パフォーマンスを実現できます。

ただし、環境変数や設定ファイルを使って全ての設定の変更や更新を行えます。

!!! tip "豆知識"
    全ての設定とオプションを確認するには、Dockerイメージページを開いて下さい: <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>.

### `Dockerfile` の作成

* プロジェクトディレクトリへ移動。
* 以下の`Dockerfile` を作成:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app
```

#### より大きなアプリケーション

[Bigger Applications with Multiple Files](tutorial/bigger-applications.md){.internal-link target=_blank} セクションを倣う場合は、`Dockerfile` は以下の様になるかもしれません:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app/app
```

#### Raspberry Piなどのアーキテクチャ

Raspberry Pi (ARMプロセッサ搭載)やそれ以外のアーキテクチャでDockerが作動している場合、(マルチアーキテクチャである) Pythonベースイメージを使って、一から`Dockerfile`を作成し、Uvicornを使用できます。

この場合、`Dockerfile` は以下の様になるかもしれません:

```Dockerfile
FROM python:3.7

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

### **FastAPI** コードの作成

* `app` ディレクトリを作成し、移動。
* 以下の`main.py` ファイルを作成:

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

* ここでは、以下の様なディレクトリ構造になっているべきです:

```
.
├── app
│   └── main.py
└── Dockerfile
```

### Dockerイメージをビルド

* プロジェクトディレクトリ (`app` ディレクトリを含んだ、`Dockerfile` のある場所) へ移動
* FastAPIイメージのビルド:

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

### Dockerコンテナを起動

* 用意したイメージを基にしたコンテナの起動:

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

これで、Dockerコンテナ内に最適化されたFastAPIサーバが動作しています。使用しているサーバ (そしてCPUコア数) に沿った自動チューニングが行われています。

### 確認

DockerコンテナのURLで確認できるはずです。例えば: <a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> や <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a> (もしくはDockerホストを使用したこれらと同等のもの)。

以下の様なものが返されます:

```JSON
{"item_id": 5, "q": "somequery"}
```

### 対話的APIドキュメント

ここで、<a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> や <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a> (もしくはDockerホストを使用したこれらと同等のもの) を開いて下さい。

自動生成された対話的APIドキュメントが確認できます (<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>によって提供される):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### その他のAPIドキュメント

また同様に、<a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> や <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a> (もしくはDockerホストを使用したこれらと同等のもの) を開いて下さい。

他の自動生成された対話的なAPIドキュメントが確認できます (<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>によって提供される):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## HTTPS

### HTTPSについて

HTTPSを、「有効」か「無効」にされるだけの何かだと考えることは簡単です。

しかし実態は、より複雑です。

!!! tip "豆知識"
    もし急いでいたり、気にならない場合は、次のセクションに進んで構築手順を確認して下さい。

コンシューマの観点からHTTPSの基本を学びたい場合は、<a href="https://howhttps.works/" class="external-link" target="_blank">https://howhttps.works/</a>を確認して下さい。

ここで、開発者の観点からHTTPSについて考える際に、覚えておくべきことがいくつかあります:

* サーバーはHTTPSのために、サードパーティによって生成された「証明書」が必要です。
    * それらの証明書は、実際には「生成」されるものではなく、サードパーティから取得するものです。
* 証明書は有効期限があります。
    * 期限切れを起こします。
    * そうなった場合、サードパーティから再取得する必要があります。
* 接続の暗号化はTCPレベルで行われます。
    * HTTPよりも1つ下のレイヤーです。
    * よって、証明と暗号化はHTTPの前に行われます。
* TCPは「ドメイン」を認識しません。IPアドレスについてのみ認識します。
    * リクエストされた特定のドメインに関する情報はHTTPデータの中に入ります。
* HTTPS証明書は特定のドメインであることを「証明」します。しかし、どのドメインで扱われるか知る前にプロトコルと暗号化はTCPレベルで行われます。
* デフォルトでは、これはIPアドレス毎に一つのHTTPS証明書しか持てないことを意味します。
    * サーバの大きさやその中にあるそれぞれのアプリケーションの大きさに依りません。
    * しかし、解決方法はあります。
* <a href="https://en.wikipedia.org/wiki/Server_Name_Indication" class="external-link" target="_blank"><abbr title="Server Name Indication">SNI</abbr></a>と呼ばれるTLSプロトコル (HTTPの前にTCPレベルで暗号化を行う) への拡張機能が存在します。
    * このSNI拡張機能により、ひとつのサーバ (一つのIPアドレスをもつ) に複数のHTTPS証明書を持たせることができて、複数のHTTPSドメイン/アプリケーションにサービスを提供できるようになります。
    * これを動作させるためには、サーバ上でパブリックIPアドレスを持ってアクセスを待ち受けている一つのコンポーネント (プログラム) にサーバ内の全てのHTTPS証明書をもたせなければなりません。
* 安全な接続を実現した後でも、通信プロトコルはHTTPのままです。
    * コンテンツはHTTPプロトコルで送信されているにも関わらず暗号化されます。

サーバー（マシン、ホストなど）で1つのプログラム/ HTTPサーバーを実行し、すべてのHTTPSの処理を管理することは一般的な方法です : 同じサーバーで実行されている実際のHTTPアプリケーション (この場合、**FastAPI**) に復号化されたHTTPリクエストを送信し、アプリケーションからHTTPレスポンスを取得し、適切な証明書を使用して暗号化し、HTTPSを使用してクライアントに送り返します。このサーバーは、しばしば<a href="https://en.wikipedia.org/wiki/TLS_termination_proxy" class="external-link" target="_blank"> TLSターミネーションプロキシ</a>と呼ばれます。

### Let's Encrypt

Let's Encryptがない頃、HTTPS証明書は信頼できるサードパーティから販売されていました。

証明書を取得するプロセスは面倒であり、かなりの事務処理を必要とし、証明書は非常に高価でした。

しかしその後、<a href="https://letsencrypt.org/" class="external-link" target="_blank">Let's Encrypt</a>が作成されました。

これはLinux Foundationのプロジェクトです。自動化された方法で、HTTPS証明書を無料で提供します。これらの証明書はすべての標準的な暗号化セキュリティを使用しており、有効期間が短い（約3か月）です。寿命が短くなるため、セキュリティは優れています。

ドメインは安全に検証され、証明書は自動的に生成されます。証明書の更新を自動化することもできます。

このアイデアは、証明書の取得と更新を自動化して、安全なHTTPSを無料で永久に使用できるようにするためのものです。

### Traefik

<a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a>は、高性能なリバースプロキシ/ロードバランサーです。「TLSターミネーションプロキシ」ジョブを実行できます（他の機能と切り離して）。

Let's Encryptと統合されています。そのため、証明書の取得と更新を含むHTTPSに関するすべての処理を実行できます。

また、Dockerとも統合されています。したがって、各アプリケーション構成でドメインを宣言し、それらの構成を読み取って、HTTPS証明書を生成し、構成に変更を加えることなく、アプリケーションにHTTPSを自動的に提供できます。

---

次のセクションに進み、この情報とツールを使用して、すべてを組み合わせます。

## TraefikとHTTPSを使用したDocker Swarmモードのクラスタ

HTTPSを処理する（証明書の取得と更新を含む）Traefikを使用して、Docker Swarmモードのクラスタを数分（20分程度）でセットアップできます。

Docker Swarmモードを使用することで、1台のマシンの「クラスタ」から開始でき（1か月あたり5ドルのサーバーでもできます）、後から必要なだけサーバーを拡張できます。

TraefikおよびHTTPS処理を備えたDocker Swarm Modeクラスターをセットアップするには、次のガイドに従います:

### <a href="https://medium.com/@tiangolo/docker-swarm-mode-and-traefik-for-a-https-cluster-20328dba6232" class="external-link" target="_blank">Docker Swarm Mode and Traefik for an HTTPS cluster</a>

### FastAPIアプリケーションのデプロイ

すべてを設定するための最も簡単な方法は、[**FastAPI** Project Generators](project-generation.md){.internal-link target=_blank}を使用することでしょう。

上述したTraefikとHTTPSを備えたDocker Swarm クラスタが統合されるように設計されています。

2分程度でプロジェクトが生成されます。

生成されたプロジェクトはデプロイの指示がありますが、それを実行するとさらに2分かかります。

## Dockerを使用しない**FastAPI**のデプロイ

Dockerを使用せずに**FastAPI** を直接デプロイすることもできます。

以下の様なASGI対応のサーバだけインストールする必要があります:

=== "Uvicorn"

    * <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>, uvloopとhttptoolsを基にした高速なASGIサーバ。

    <div class="termy">

    ```console
    $ pip install uvicorn

    ---> 100%
    ```

    </div>

=== "Hypercorn"

    * <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>, HTTP/2にも対応しているASGIサーバ。

    <div class="termy">

    ```console
    $ pip install hypercorn

    ---> 100%
    ```

    </div>

    ...または、これら以外のASGIサーバ。

そして、チュートリアルと同様な方法でアプリケーションを起動して下さい。ただし、以下の様に`--reload` オプションは使用しないで下さい:

=== "Uvicorn"

    <div class="termy">

    ```console
    $ uvicorn main:app --host 0.0.0.0 --port 80

    <span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
    ```

    </div>

=== "Hypercorn"

    <div class="termy">

    ```console
    $ hypercorn main:app --bind 0.0.0.0:80

    Running on 0.0.0.0:8080 over http (CTRL + C to quit)
    ```

    </div>


停止した場合に自動的に再起動させるツールを設定したいかも知れません。

さらに、<a href="https://gunicorn.org/" class="external-link" target="_blank">Gunicorn</a>をインストールして<a href="https://www.uvicorn.org/#running-with-gunicorn" class="external-link" target="_blank">Uvicornのマネージャーとして使用したり</a>、複数のワーカーでHypercornを使用したいかも知れません。

ワーカー数などの微調整も行いたいかもしれません。

しかしこれら全てをやろうとすると、自動的にこれらを行うDockerイメージを使えばよいだけかも知れません。
