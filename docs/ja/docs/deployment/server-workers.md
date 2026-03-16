# Server Workers - ワーカー付きUvicorn { #server-workers-uvicorn-with-workers }

前回のデプロイメントのコンセプトを振り返ってみましょう：

* セキュリティ - HTTPS
* 起動時の実行
* 再起動
* **レプリケーション（実行中のプロセス数）**
* メモリ
* 開始前の事前ステップ

ここまでのドキュメントのチュートリアルでは、おそらく `fastapi` コマンドなど（Uvicornを実行するもの）を使って、**単一のプロセス**として動作する**サーバープログラム**を実行してきたはずです。

アプリケーションをデプロイする際には、**複数のコア**を利用し、そしてより多くのリクエストを処理できるようにするために、プロセスの**レプリケーション**を持つことを望むでしょう。

前のチャプターである[デプロイメントのコンセプト](concepts.md){.internal-link target=_blank}にて見てきたように、有効な戦略がいくつかあります。

ここでは、`fastapi` コマンド、または `uvicorn` コマンドを直接使って、**ワーカープロセス**付きの **Uvicorn** を使う方法を紹介します。

/// info | 情報

DockerやKubernetesなどのコンテナを使用している場合は、次の章で詳しく説明します： [コンテナ内のFastAPI - Docker](docker.md){.internal-link target=_blank}。

特に**Kubernetes**上で実行する場合は、おそらくワーカーは使わず、代わりに**コンテナごとに単一のUvicornプロセス**を実行したいはずですが、それについてはその章の後半で説明します。

///

## 複数ワーカー { #multiple-workers }

`--workers` コマンドラインオプションで複数のワーカーを起動できます。

//// tab | `fastapi`

`fastapi` コマンドを使う場合：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run --workers 4 <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started parent process <b>[</b><font color="#34E2E2"><b>27365</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27368</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27369</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27370</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27367</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

////

//// tab | `uvicorn`

`uvicorn` コマンドを直接使いたい場合：

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
<font color="#A6E22E">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8080</b> (Press CTRL+C to quit)
<font color="#A6E22E">INFO</font>:     Started parent process [<font color="#A1EFE4"><b>27365</b></font>]
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27368</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27369</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27370</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27367</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
```

</div>

////

ここで唯一の新しいオプションは `--workers` で、Uvicornに4つのワーカープロセスを起動するように指示しています。

各プロセスの **PID** も表示されていて、親プロセス（これは**プロセスマネージャー**）が `27365`、各ワーカープロセスがそれぞれ `27368`、`27369`、`27370`、`27367` です。

## デプロイメントのコンセプト { #deployment-concepts }

ここでは、複数の **ワーカー** を使ってアプリケーションの実行を**並列化**し、CPUの**複数コア**を活用して、**より多くのリクエスト**を処理できるようにする方法を見てきました。

上のデプロイメントのコンセプトのリストから、ワーカーを使うことは主に**レプリケーション**の部分と、**再起動**を少し助けてくれますが、それ以外については引き続き対処が必要です：

* **セキュリティ - HTTPS**
* **起動時の実行**
* ***再起動***
* レプリケーション（実行中のプロセス数）
* **メモリ**
* **開始前の事前ステップ**

## コンテナとDocker { #containers-and-docker }

次章の[コンテナ内のFastAPI - Docker](docker.md){.internal-link target=_blank}では、その他の**デプロイメントのコンセプト**を扱うために使える戦略をいくつか説明します。

単一のUvicornプロセスを実行するために、**ゼロから独自のイメージを構築する**方法も紹介します。これは簡単なプロセスで、**Kubernetes**のような分散コンテナ管理システムを使う場合に、おそらくやりたいことでしょう。

## まとめ { #recap }

`fastapi` または `uvicorn` コマンドで `--workers` CLIオプションを使うことで、**マルチコアCPU**を活用し、**複数のプロセスを並列実行**できるように複数のワーカープロセスを利用できます。

他のデプロイメントのコンセプトを自分で対応しながら、**独自のデプロイシステム**を構築している場合にも、これらのツールやアイデアを使えます。

次の章で、コンテナ（例：DockerやKubernetes）を使った **FastAPI** について学びましょう。これらのツールにも、他の**デプロイメントのコンセプト**を解決する簡単な方法があることがわかります。✨
