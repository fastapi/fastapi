# FastAPI CLI { #fastapi-cli }

**FastAPI <abbr title="command line interface - コマンドラインインターフェース">CLI</abbr>** は、FastAPI アプリの提供、FastAPI プロジェクトの管理などに使用できるコマンドラインプログラムです。

FastAPI をインストールすると（例: `pip install "fastapi[standard]"`）、ターミナルで実行できるコマンドラインプログラムが付属します。

開発用に FastAPI アプリを起動するには、`fastapi dev` コマンドを使用できます:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

/// tip

本番では `fastapi dev` の代わりに `fastapi run` を使用します。🚀

///

内部的には、**FastAPI CLI** は [Uvicorn](https://www.uvicorn.dev)（高性能で本番運用向けの ASGI サーバー）を使用します。😎

`fastapi` CLI は、実行する FastAPI アプリを自動検出しようとします。既定では、`main.py` の中にある `app` という名前のオブジェクト（ほかにもいくつかの変種）であると仮定します。

ただし、使用するアプリを明示的に設定することもできます。

## `pyproject.toml` でアプリの `entrypoint` を設定 { #configure-the-app-entrypoint-in-pyproject-toml }

`pyproject.toml` に次のように、アプリの場所を設定できます:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

この `entrypoint` により、`fastapi` コマンドは次のようにアプリを import する必要があると認識します:

```python
from main import app
```

もしコード構成が次のような場合:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

`entrypoint` は次のように設定します:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

これは次と同等です:

```python
from backend.main import app
```

### パス指定での `fastapi dev` { #fastapi-dev-with-path }

`fastapi dev` コマンドにファイルパスを渡すこともでき、使用する FastAPI アプリオブジェクトを推測します:

```console
$ fastapi dev main.py
```

ただし、そのたびに `fastapi` コマンドを呼び出す際に正しいパスを渡す必要があります。

さらに、[VS Code 拡張機能](editor-support.md) や [FastAPI Cloud](https://fastapicloud.com) など、ほかのツールがそれを見つけられない場合があります。そのため、`pyproject.toml` の `entrypoint` を使用することを推奨します。

## `fastapi dev` { #fastapi-dev }

`fastapi dev` を実行すると、開発モードが有効になります。

デフォルトでは、**auto-reload** が有効です。コードを変更するとサーバーが自動で再読み込みされます。これはリソースを多く消費し、無効時より安定性が低くなる可能性があります。開発時のみに使用してください。また、IP アドレス `127.0.0.1`（マシン自身のみと通信するための IP、`localhost`）で待ち受けます。

## `fastapi run` { #fastapi-run }

`fastapi run` を実行すると、デフォルトで本番モードで起動します。

デフォルトでは、**auto-reload** は無効です。また、IP アドレス `0.0.0.0`（利用可能なすべての IP アドレスを意味します）で待ち受けるため、そのマシンと通信できる任意のクライアントから公開アクセスが可能になります。これは、たとえばコンテナ内など、本番環境で一般的な実行方法です。

多くの場合（そして推奨されるのは）、上位に HTTPS を終端する「termination proxy」を置きます。これはアプリのデプロイ方法に依存し、プロバイダが代行する場合もあれば、自分で設定する必要がある場合もあります。

/// tip

詳しくは、[デプロイのドキュメント](deployment/index.md)を参照してください。

///
