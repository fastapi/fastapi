# コンテナ内のFastAPI - Docker { #fastapi-in-containers-docker }

FastAPIアプリケーションをデプロイする場合、一般的なアプローチは**Linuxコンテナ・イメージ**をビルドすることです。基本的には <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a>を用いて行われます。生成されたコンテナ・イメージは、いくつかの方法のいずれかでデプロイできます。

Linuxコンテナの使用には、**セキュリティ**、**反復可能性（レプリカビリティ）**、**シンプリシティ**など、いくつかの利点があります。

/// tip | 豆知識

お急ぎで、すでにこれらの情報をご存じですか？ [以下の`Dockerfile`の箇所👇](#build-a-docker-image-for-fastapi)へジャンプしてください。

///

<details>
<summary>Dockerfile Preview 👀</summary>

```Dockerfile
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

</details>

## コンテナとは何か { #what-is-a-container }

コンテナ（主にLinuxコンテナ）は、同じシステム内の他のコンテナ（他のアプリケーションやコンポーネント）から隔離された状態を保ちながら、すべての依存関係や必要なファイルを含むアプリケーションをパッケージ化する非常に**軽量**な方法です。

Linuxコンテナは、ホスト（マシン、仮想マシン、クラウドサーバーなど）の同じLinuxカーネルを使用して実行されます。これは、（OS全体をエミュレートする完全な仮想マシンと比べて）非常に軽量であることを意味します。

このように、コンテナは**リソースをほとんど消費しません**が、プロセスを直接実行するのに匹敵する量です（仮想マシンはもっと消費します）。

コンテナはまた、独自の**分離された**実行プロセス（通常は1つのプロセスのみ）や、ファイルシステム、ネットワークを持ちます。 このことはデプロイ、セキュリティ、開発などを簡素化させます。

## コンテナ・イメージとは何か { #what-is-a-container-image }

**コンテナ**は、**コンテナ・イメージ**から実行されます。

コンテナ・イメージは、コンテナ内に存在すべきすべてのファイルや環境変数、そしてデフォルトのコマンド/プログラムを**静的に**バージョン化したものです。 ここでの**静的**とは、コンテナ**イメージ**は実行されておらず、パッケージ化されたファイルとメタデータのみであることを意味します。

保存された静的コンテンツである「**コンテナイメージ**」とは対照的に、「**コンテナ**」は通常、実行中のインスタンス、つまり**実行**されているものを指します。

**コンテナ**が起動され実行されるとき（**コンテナイメージ**から起動されるとき）、ファイルや環境変数などが作成されたり変更されたりする可能性があります。これらの変更はそのコンテナ内にのみ存在しますが、基盤となるコンテナ・イメージには残りません（ディスクに保存されません）。

コンテナイメージは **プログラム** ファイルやその内容、例えば `python` と `main.py` ファイルに匹敵します。

そして、**コンテナ**自体は（**コンテナイメージ**とは対照的に）イメージをもとにした実際の実行中のインスタンスであり、**プロセス**に匹敵します。実際、コンテナが実行されているのは、**プロセスが実行されている**ときだけです（通常は単一のプロセスだけです）。 コンテナ内で実行中のプロセスがない場合、コンテナは停止します。

## コンテナ・イメージ { #container-images }

Dockerは、**コンテナ・イメージ**と**コンテナ**を作成・管理するための主要なツールの1つです。

そして、多くのツールや環境、データベース、アプリケーションに対応している予め作成された**公式のコンテナ・イメージ**をパブリックに提供している<a href="https://hub.docker.com/" class="external-link" target="_blank">Docker Hub</a>というものがあります。

例えば、公式イメージの1つに<a href="https://hub.docker.com/_/python" class="external-link" target="_blank">Python Image</a>があります。

その他にも、データベースなどさまざまなイメージがあります：

* <a href="https://hub.docker.com/_/postgres" class="external-link" target="_blank">PostgreSQL</a>
* <a href="https://hub.docker.com/_/mysql" class="external-link" target="_blank">MySQL</a>
* <a href="https://hub.docker.com/_/mongo" class="external-link" target="_blank">MongoDB</a>
* <a href="https://hub.docker.com/_/redis" class="external-link" target="_blank">Redis</a>, etc.

予め作成されたコンテナ・イメージを使用することで、異なるツールを**組み合わせて**使用することが非常に簡単になります。例えば、新しいデータベースを試す場合に特に便利です。ほとんどの場合、**公式イメージ**を使い、環境変数で設定するだけで良いです。

そうすれば多くの場合、コンテナとDockerについて学び、その知識をさまざまなツールやコンポーネントによって再利用することができます。

つまり、データベース、Pythonアプリケーション、Reactフロントエンド・アプリケーションを備えたウェブ・サーバーなど、さまざまなものを**複数のコンテナ**で実行し、それらを内部ネットワーク経由で接続します。

すべてのコンテナ管理システム（DockerやKubernetesなど）には、こうしたネットワーキング機能が統合されています。

## コンテナとプロセス { #containers-and-processes }

通常、**コンテナ・イメージ**はそのメタデータに**コンテナ**の起動時に実行されるデフォルトのプログラムまたはコマンドと、そのプログラムに渡されるパラメータを含みます。コマンドラインでの操作とよく似ています。

**コンテナ**が起動されると、そのコマンド/プログラムが実行されます（ただし、別のコマンド/プログラムをオーバーライドして実行させることもできます）。

コンテナは、**メイン・プロセス**（コマンドまたはプログラム）が実行されている限り実行されます。

コンテナは通常**1つのプロセス**を持ちますが、メイン・プロセスからサブ・プロセスを起動することも可能で、そうすれば同じコンテナ内に**複数のプロセス**を持つことになります。

しかし、**少なくとも1つの実行中のプロセス**がなければ、実行中のコンテナを持つことはできないです。メイン・プロセスが停止すれば、コンテナも停止します。

## FastAPI用のDockerイメージをビルドする { #build-a-docker-image-for-fastapi }

ということで、何か作りましょう！🚀

FastAPI用の**Dockerイメージ**を、**公式Python**イメージに基づいて**ゼロから**ビルドする方法をお見せします。

これは**ほとんどの場合**にやりたいことです。例えば：

* **Kubernetes**または同様のツールを使用する場合
* **Raspberry Pi**で実行する場合
* コンテナ・イメージを実行してくれるクラウド・サービスなどを利用する場合

### パッケージ要件 { #package-requirements }

アプリケーションの**パッケージ要件**は通常、何らかのファイルに記述されているはずです。

パッケージ要件は主に**インストール**するために使用するツールに依存するでしょう。

最も一般的な方法は、`requirements.txt` ファイルにパッケージ名とそのバージョンを 1 行ずつ書くことです。

もちろん、[FastAPI バージョンについて](versions.md){.internal-link target=_blank}で読んだのと同じアイデアを使用して、バージョンの範囲を設定します。

例えば、`requirements.txt` は次のようになります：

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

そして通常、例えば `pip` を使ってこれらのパッケージの依存関係をインストールします：

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

</div>

/// info | 情報

パッケージの依存関係を定義しインストールするためのフォーマットやツールは他にもあります。

///

### **FastAPI**コードを作成する { #create-the-fastapi-code }

* `app` ディレクトリを作成し、その中に入ります。
* 空のファイル `__init__.py` を作成します。
* 次の内容で `main.py` ファイルを作成します：

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### Dockerfile { #dockerfile }

同じプロジェクト・ディレクトリに`Dockerfile`というファイルを作成します：

```{ .dockerfile .annotate }
# (1)!
FROM python:3.14

# (2)!
WORKDIR /code

# (3)!
COPY ./requirements.txt /code/requirements.txt

# (4)!
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)!
COPY ./app /code/app

# (6)!
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

1. 公式のPythonベースイメージから始めます

2. 現在の作業ディレクトリを `/code` に設定します

    ここに `requirements.txt` ファイルと `app` ディレクトリを置きます。

3. 要件が書かれたファイルを `/code` ディレクトリにコピーします

    残りのコードではなく、最初に必要なファイルだけをコピーしてください。

    このファイルは**頻繁には変更されない**ので、Dockerはこのステップではそれを検知し**キャッシュ**を使用し、次のステップでもキャッシュを有効にします。

4. 要件ファイルにあるパッケージの依存関係をインストールします

    `--no-cache-dir` オプションはダウンロードしたパッケージをローカルに保存しないように `pip` に指示します。これは、同じパッケージをインストールするために `pip` を再度実行する場合にのみ有効ですが、コンテナで作業する場合はそうではないです。

    /// note | 備考

    `--no-cache-dir`は`pip`に関連しているだけで、Dockerやコンテナとは何の関係もないです。

    ///

    `--upgrade` オプションは、パッケージが既にインストールされている場合、`pip` にアップグレードするように指示します。

    何故ならファイルをコピーする前のステップは**Dockerキャッシュ**によって検出される可能性があるためであり、このステップも利用可能な場合は**Dockerキャッシュ**を使用します。

    このステップでキャッシュを使用すると、開発中にイメージを何度もビルドする際に、**毎回**すべての依存関係を**ダウンロードしてインストールする**代わりに多くの**時間**を**節約**できます。

5. `./app` ディレクトリを `/code` ディレクトリの中にコピーする。

    これには**最も頻繁に変更される**すべてのコードが含まれているため、Dockerの**キャッシュ**は**これ以降のステップ**に簡単に使用されることはありません。

    そのため、コンテナイメージのビルド時間を最適化するために、`Dockerfile`の **最後** にこれを置くことが重要です。

6. 内部でUvicornを使用する `fastapi run` を使うための**コマンド**を設定します

    `CMD` は文字列のリストを取り、それぞれの文字列はスペースで区切られたコマンドラインに入力するものです。

    このコマンドは **現在の作業ディレクトリ**から実行され、上記の `WORKDIR /code` にて設定した `/code` ディレクトリと同じです。

/// tip | 豆知識

コード内の各番号バブルをクリックして、各行が何をするのかをレビューしてください。👆

///

/// warning | 注意

以下で説明する通り、`CMD` 命令は**常に** **exec形式**を使用してください。

///

#### `CMD` を使う - Exec形式 { #use-cmd-exec-form }

Docker命令 <a href="https://docs.docker.com/reference/dockerfile/#cmd" class="external-link" target="_blank">`CMD`</a> は2つの形式で書けます：

✅ **Exec** 形式：

```Dockerfile
# ✅ Do this
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

⛔️ **Shell** 形式：

```Dockerfile
# ⛔️ Don't do this
CMD fastapi run app/main.py --port 80
```

FastAPIが正常にシャットダウンでき、[lifespan events](../advanced/events.md){.internal-link target=_blank}がトリガーされるように、常に **exec** 形式を使用してください。

詳しくは、<a href="https://docs.docker.com/reference/dockerfile/#shell-and-exec-form" class="external-link" target="_blank">shell形式とexec形式に関するDockerドキュメント</a>をご覧ください。

これは `docker compose` を使用する場合にかなり目立つことがあります。より技術的な詳細は、このDocker ComposeのFAQセクションをご覧ください：<a href="https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop" class="external-link" target="_blank">Why do my services take 10 seconds to recreate or stop?</a>。

#### ディレクトリ構造 { #directory-structure }

これで、次のようなディレクトリ構造になるはずです：

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### TLS Termination Proxyの裏側 { #behind-a-tls-termination-proxy }

Nginx や Traefik のような TLS Termination Proxy (ロードバランサ) の後ろでコンテナを動かしている場合は、`--proxy-headers`オプションを追加します。これにより、（FastAPI CLI経由で）Uvicornに対して、そのプロキシから送信されるヘッダを信頼し、アプリケーションがHTTPSの裏で実行されていることなどを示すよう指示します。

```Dockerfile
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

#### Dockerキャッシュ { #docker-cache }

この`Dockerfile`には重要なトリックがあり、まず**依存関係だけのファイル**をコピーします。その理由を説明します。

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

Dockerや他のツールは、これらのコンテナイメージを**段階的に**ビルドし、**1つのレイヤーを他のレイヤーの上に**追加します。`Dockerfile`の先頭から開始し、`Dockerfile`の各命令によって作成されたファイルを追加していきます。

Dockerや同様のツールは、イメージをビルドする際に**内部キャッシュ**も使用します。前回コンテナイメージを構築したときからファイルが変更されていない場合、ファイルを再度コピーしてゼロから新しいレイヤーを作成する代わりに、**前回作成した同じレイヤーを再利用**します。

ただファイルのコピーを避けるだけではあまり改善されませんが、そのステップでキャッシュを利用したため、**次のステップ**でキャッシュを使うことができます。

例えば、依存関係をインストールする命令のためにキャッシュを使うことができます：

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

パッケージ要件のファイルは**頻繁に変更されることはありません**。そのため、そのファイルだけをコピーすることで、Dockerはそのステップでは**キャッシュ**を使用することができます。

そして、Dockerは**次のステップのためにキャッシュ**を使用し、それらの依存関係をダウンロードしてインストールすることができます。そして、ここで**多くの時間を節約**します。✨ ...そして退屈な待ち時間を避けることができます。😪😆

パッケージの依存関係をダウンロードしてインストールするには**数分**かかりますが、**キャッシュ**を使えば**せいぜい数秒**です。

加えて、開発中にコンテナ・イメージを何度もビルドして、コードの変更が機能しているかどうかをチェックすることになるため、多くの時間を節約することができます。

そして`Dockerfile`の最終行の近くですべてのコードをコピーします。この理由は、**最も頻繁に**変更されるものなので、このステップの後にあるものはほとんどキャッシュを使用することができないのためです。

```Dockerfile
COPY ./app /code/app
```

### Dockerイメージをビルドする { #build-the-docker-image }

すべてのファイルが揃ったので、コンテナ・イメージをビルドしましょう。

* プロジェクトディレクトリに移動します（`Dockerfile`がある場所で、`app`ディレクトリがあります）。
* FastAPI イメージをビルドします：

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

/// tip | 豆知識

末尾の `.` に注目してほしいです。これは `./` と同じ意味です。 これはDockerにコンテナイメージのビルドに使用するディレクトリを指示します。

この場合、同じカレント・ディレクトリ(`.`)です。

///

### Dockerコンテナの起動する { #start-the-docker-container }

* イメージに基づいてコンテナを実行します：

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## 確認する { #check-it }

Dockerコンテナの<a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> や <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a> (またはそれに相当するDockerホストを使用したもの）といったURLで確認できるはずです。

アクセスすると以下のようなものが表示されます：

```JSON
{"item_id": 5, "q": "somequery"}
```

## インタラクティブなAPIドキュメント { #interactive-api-docs }

これらのURLにもアクセスできます:  <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> や <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a> (またはそれに相当するDockerホストを使用したもの）

アクセスすると、自動対話型APIドキュメント（<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>が提供）が表示されます：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## 代替のAPIドキュメント { #alternative-api-docs }

また、<a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> や <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a> (またはそれに相当するDockerホストを使用したもの）にもアクセスできます。

代替の自動ドキュメント（<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>によって提供される）が表示されます：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 単一ファイルのFastAPIでDockerイメージをビルドする { #build-a-docker-image-with-a-single-file-fastapi }

FastAPI が単一のファイル、例えば `./app` ディレクトリのない `main.py` の場合、ファイル構造は次のようになります：

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

そうすれば、`Dockerfile`の中にファイルをコピーするために、対応するパスを変更するだけでよいです：

```{ .dockerfile .annotate hl_lines="10  13" }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)!
COPY ./main.py /code/

# (2)!
CMD ["fastapi", "run", "main.py", "--port", "80"]
```

1. `main.py`ファイルを `/code` ディレクトリに直接コピーします（`./app` ディレクトリなし）。

2. 単一ファイル `main.py` 内のアプリケーションを配信するために `fastapi run` を使用します。

`fastapi run` にファイルを渡すと、それがパッケージの一部ではなく単一ファイルであることを自動的に検出し、インポートしてFastAPIアプリを配信する方法を判断します。😎

## デプロイメントのコンセプト { #deployment-concepts }

コンテナという観点から、[デプロイのコンセプト](concepts.md){.internal-link target=_blank}に共通するいくつかについて、もう一度説明しましょう。

コンテナは主に、アプリケーションの**ビルドとデプロイ**のプロセスを簡素化するためのツールですが、これらの**デプロイのコンセプト**を扱うための特定のアプローチを強制するものではなく、いくつかの戦略があります。

**良いニュース**は、それぞれの異なる戦略には、すべてのデプロイメントのコンセプトをカバーする方法があるということです。🎉

これらの**デプロイメントのコンセプト**をコンテナの観点から見直してみましょう：

* HTTPS
* 起動時の実行
* 再起動
* レプリケーション（実行中のプロセス数）
* メモリ
* 開始前の事前ステップ

## HTTPS { #https }

FastAPI アプリケーションの **コンテナ・イメージ**（および後で実行中の **コンテナ**）だけに焦点を当てると、通常、HTTPSは別のツールを用いて**外部で**処理されます。

例えば<a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a>のように、**HTTPS**と**証明書**の**自動**取得を扱う別のコンテナである可能性もあります。

/// tip | 豆知識

TraefikはDockerやKubernetesなどと統合されているので、コンテナ用のHTTPSの設定や構成はとても簡単です。

///

あるいは、（コンテナ内でアプリケーションを実行しながら）クラウド・プロバイダーがサービスの1つとしてHTTPSを処理することもできます。

## 起動時および再起動時の実行 { #running-on-startup-and-restarts }

通常、コンテナの**起動と実行**を担当する別のツールがあります。

それは直接**Docker**であったり、**Docker Compose**であったり、**Kubernetes**であったり、**クラウドサービス**であったりします。

ほとんどの場合（またはすべての場合）、起動時にコンテナを実行し、失敗時に再起動を有効にする簡単なオプションがあります。例えばDockerでは、コマンドラインオプションの`--restart`が該当します。

コンテナを使わなければ、アプリケーションを起動時や再起動時に実行させるのは面倒で難しいかもしれません。しかし、**コンテナ**で作業する場合、ほとんどのケースでその機能はデフォルトで含まれています。✨

## レプリケーション - プロセス数 { #replication-number-of-processes }

**Kubernetes** や Docker Swarm モード、Nomad、あるいは複数のマシン上で分散コンテナを管理するための同様の複雑なシステムを使ってマシンの<dfn title="ある方法で接続され、連携して動作するように構成されたマシンの集まり">クラスタ</dfn>を構成している場合、 各コンテナで（Workerを持つUvicornのような）**プロセスマネージャ**を使用する代わりに、**クラスター・レベル**で**レプリケーション**を処理したいと思うでしょう。

Kubernetesのような分散コンテナ管理システムの1つは通常、入ってくるリクエストの**ロードバランシング**をサポートしながら、**コンテナのレプリケーション**を処理する統合された方法を持っています。このことはすべて**クラスタレベル**にてです。

そのような場合、[上記の説明](#dockerfile)のように**Dockerイメージをゼロから**ビルドし、依存関係をインストールして、**単一のUvicornプロセス**を実行したいでしょう。複数のUvicornワーカーを使う代わりにです。

### ロードバランサー { #load-balancer }

コンテナを使用する場合、通常はメイン・ポート**でリスニング**しているコンポーネントがあるはずです。それはおそらく、**HTTPS**を処理するための**TLS Termination Proxy**でもある別のコンテナであったり、同様のツールであったりするでしょう。

このコンポーネントはリクエストの **負荷** を受け、 (うまくいけば) その負荷を**バランスよく** ワーカーに分配するので、一般に **ロードバランサ** とも呼ばれます。

/// tip | 豆知識

HTTPSに使われるものと同じ**TLS Termination Proxy**コンポーネントは、おそらく**ロードバランサー**にもなるでしょう。

///

そしてコンテナで作業する場合、コンテナの起動と管理に使用する同じシステムには、**ロードバランサー**（**TLS Termination Proxy**の可能性もある）から**ネットワーク通信**（HTTPリクエストなど）をアプリのあるコンテナ（複数可）に送信するための内部ツールが既にあるはずです。

### 1つのロードバランサー - 複数のワーカーコンテナー { #one-load-balancer-multiple-worker-containers }

**Kubernetes**や同様の分散コンテナ管理システムで作業する場合、その内部のネットワーキングのメカニズムを使用することで、メインの**ポート**でリッスンしている単一の**ロードバランサー**が、アプリを実行している可能性のある**複数のコンテナ**に通信（リクエスト）を送信できるようになります。

アプリを実行するこれらのコンテナには、通常**1つのプロセス**（たとえば、FastAPIアプリケーションを実行するUvicornプロセス）があります。これらはすべて**同一のコンテナ**であり同じものを実行しますが、それぞれが独自のプロセスやメモリなどを持ちます。そうすることで、CPUの**異なるコア**、あるいは**異なるマシン**での**並列化**を利用できます。

そして、**ロードバランサー**を備えた分散コンテナシステムは、**順番に**あなたのアプリを含む各コンテナに**リクエストを分配**します。つまり、各リクエストは、あなたのアプリを実行している複数の**レプリケートされたコンテナ**の1つによって処理されます。

そして通常、この**ロードバランサー**は、クラスタ内の*他の*アプリケーション（例えば、異なるドメインや異なるURLパスのプレフィックスの配下）へのリクエストを処理することができ、その通信をクラスタ内で実行されている*他の*アプリケーションのための適切なコンテナに送信します。

### 1コンテナにつき1プロセス { #one-process-per-container }

この種のシナリオでは、すでにクラスタ・レベルでレプリケーションを処理しているため、おそらくコンテナごとに**単一の（Uvicorn）プロセス**を持ちたいでしょう。

この場合、例えばコマンドラインオプションの `--workers` で、コンテナ内に複数のワーカーを持つことは**避けたい**でしょう。**コンテナごとにUvicornのプロセスは1つだけ**にしたいでしょう（おそらく複数のコンテナが必要でしょう）。

（複数のワーカーの場合のように）コンテナ内に別のプロセスマネージャーを持つことは、クラスターシステムですでに対処しているであろう**不要な複雑さ**を追加するだけです。

### 複数プロセスのコンテナと特殊なケース { #containers-with-multiple-processes-and-special-cases }

もちろん、**特殊なケース**として、**コンテナ**内で複数の**Uvicornワーカープロセス**を起動させたい場合があります。

そのような場合、`--workers` コマンドラインオプションを使って、実行したいワーカー数を設定できます：

```{ .dockerfile .annotate }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# (1)!
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

1. ここでは `--workers` コマンドラインオプションを使って、ワーカー数を4に設定しています。

以下は、それが理にかなっている場合の例です：

#### シンプルなアプリ { #a-simple-app }

アプリケーションが、クラスタではなく**単一サーバ**で実行できるほど**シンプル**である場合、コンテナ内にプロセスマネージャが欲しくなることがあります。

#### Docker Compose { #docker-compose }

Docker Composeで**単一サーバ**（クラスタではない）にデプロイすることもできますので、共有ネットワークと**ロードバランシング**を維持しながら（Docker Composeで）コンテナのレプリケーションを管理する簡単な方法はないでしょう。

その場合、**単一のコンテナ**で、**プロセスマネージャ**が内部で**複数のワーカープロセス**を起動するようにします。

---

重要なのは、これらのどれも、盲目的に従わなければならない「**絶対的なルール**」ではないということです。これらのアイデアは、**あなた自身のユースケース**を評価し、あなたのシステムに最適なアプローチを決定するために使用できます。次の概念をどう管理するかを確認してください：

* セキュリティ - HTTPS
* 起動時の実行
* 再起動
* レプリケーション（実行中のプロセス数）
* メモリ
* 開始前の事前ステップ

## メモリ { #memory }

コンテナごとに**単一のプロセスを実行する**と、それらのコンテナ（レプリケートされている場合は1つ以上）によって消費される多かれ少なかれ明確に定義された、安定し制限された量のメモリを持つことになります。

そして、コンテナ管理システム（**Kubernetes**など）の設定で、同じメモリ制限と要件を設定することができます。

そうすれば、コンテナが必要とするメモリ量とクラスタ内のマシンで利用可能なメモリ量を考慮して、**利用可能なマシン**に**コンテナ**をレプリケートできるようになります。

アプリケーションが**シンプル**なものであれば、これはおそらく**問題にはならない**でしょうし、ハードなメモリ制限を指定する必要はないかもしれないです。

しかし、**多くのメモリを使用**している場合（たとえば**機械学習**モデルなど）、どれだけのメモリを消費しているかを確認し、**各マシンで実行するコンテナの数**を調整する必要があります（そしておそらくクラスタにマシンを追加します）。

**コンテナごとに複数のプロセス**を実行する場合、起動するプロセスの数が**利用可能なメモリ以上に消費しない**ようにする必要があります。

## 開始前の事前ステップとコンテナ { #previous-steps-before-starting-and-containers }

コンテナ（DockerやKubernetesなど）を使っている場合、主に2つのアプローチがあります。

### 複数のコンテナ { #multiple-containers }

複数の**コンテナ**があり、おそらくそれぞれが**単一のプロセス**を実行している場合（例えば、**Kubernetes**クラスタなど）、レプリケートされたワーカーコンテナを実行する**前に**、単一のコンテナで**事前のステップ**の作業を行う**別のコンテナ**を持ちたいと思うでしょう。

/// info | 情報

もしKubernetesを使用している場合, これはおそらく<a href="https://kubernetes.io/docs/concepts/workloads/pods/init-containers/" class="external-link" target="_blank">Init Container</a>でしょう。

///

ユースケースが事前のステップを**並列で複数回**実行するのに問題がない場合（例：データベースマイグレーションを実行するのではなく、データベースの準備ができたかをチェックするだけの場合）、メインプロセスを開始する直前に、それらのステップを各コンテナに入れることも可能です。

### 単一コンテナ { #single-container }

単純なセットアップで、**単一のコンテナ**で複数の**ワーカープロセス**（または1つのプロセスのみ）を起動する場合、アプリでプロセスを開始する直前に、同じコンテナで事前のステップを実行できます。

### ベースDockerイメージ { #base-docker-image }

以前は、公式のFastAPI Dockerイメージがありました：<a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>。しかし、現在は非推奨です。⛔️

おそらく、このベースDockerイメージ（またはその他の類似のもの）は**使用しない**方がよいでしょう。

すでに**Kubernetes**（または他のもの）を使用していて、複数の**コンテナ**で、クラスタレベルで**レプリケーション**を設定している場合。そのような場合は、上記で説明したように**ゼロから**イメージを構築する方がよいでしょう：[FastAPI用のDockerイメージをビルドする](#build-a-docker-image-for-fastapi)。

また、複数のワーカーが必要な場合は、単純に `--workers` コマンドラインオプションを使用できます。

/// note | 技術詳細

このDockerイメージは、Uvicornが停止したワーカーの管理と再起動をサポートしていなかった頃に作成されたため、Uvicornと一緒にGunicornを使う必要がありました。これは、GunicornにUvicornワーカープロセスの管理と再起動をさせるだけのために、かなりの複雑さを追加していました。

しかし現在は、Uvicorn（および `fastapi` コマンド）が `--workers` をサポートしているため、自分でビルドする代わりにベースDockerイメージを使う理由はありません（コード量もだいたい同じです 😅）。

///

## コンテナ・イメージのデプロイ { #deploy-the-container-image }

コンテナ（Docker）イメージを手に入れた後、それをデプロイするにはいくつかの方法があります。

例えば以下のリストの方法です:

* 単一サーバーの**Docker Compose**
* **Kubernetes**クラスタ
* Docker Swarmモードのクラスター
* Nomadのような別のツール
* コンテナ・イメージをデプロイするクラウド・サービス

## `uv` を使ったDockerイメージ { #docker-image-with-uv }

<a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">uv</a> を使ってプロジェクトのインストールと管理をしている場合は、<a href="https://docs.astral.sh/uv/guides/integration/docker/" class="external-link" target="_blank">uv Docker guide</a>に従ってください。

## まとめ { #recap }

コンテナ・システム（例えば**Docker**や**Kubernetes**など）を使えば、すべての**デプロイメントのコンセプト**を扱うのがかなり簡単になります：

* HTTPS
* 起動時の実行
* 再起動
* レプリケーション（実行中のプロセス数）
* メモリ
* 開始前の事前ステップ

ほとんどの場合、ベースとなるイメージは使用せず、公式のPython Dockerイメージをベースにした**コンテナイメージをゼロからビルド**します。

`Dockerfile`と**Dockerキャッシュ**内の命令の**順番**に注意することで、**ビルド時間を最小化**し、生産性を最大化できます（そして退屈を避けることができます）。😎
