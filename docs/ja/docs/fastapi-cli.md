# FastAPI CLI { #fastapi-cli }

**FastAPI CLI** は、FastAPI アプリの提供、FastAPI プロジェクトの管理などに使用できるコマンドラインプログラムです。

FastAPI をインストールすると（例: `pip install "fastapi[standard]"`）、`fastapi-cli` というパッケージが含まれます。このパッケージがターミナルで使用する `fastapi` コマンドを提供します。

開発用に FastAPI アプリを起動するには、`fastapi dev` コマンドを使用できます:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

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

`fastapi` というコマンドラインプログラムが **FastAPI CLI** です。

FastAPI CLI は、Python プログラムへのパス（例: `main.py`）を受け取り、`FastAPI` インスタンス（通常は `app`）を自動検出し、適切な import 方法を判断して提供します。

本番環境では代わりに `fastapi run` を使用します。🚀

内部的には、**FastAPI CLI** は <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>（高性能で本番運用向けの ASGI サーバー）を使用します。😎

## `fastapi dev` { #fastapi-dev }

`fastapi dev` を実行すると、開発モードが有効になります。

デフォルトでは、**auto-reload** が有効です。コードを変更するとサーバーが自動で再読み込みされます。これはリソースを多く消費し、無効時より安定性が低くなる可能性があります。開発時のみに使用してください。また、IP アドレス `127.0.0.1`（マシン自身のみと通信するための IP、`localhost`）で待ち受けます。

## `fastapi run` { #fastapi-run }

`fastapi run` を実行すると、デフォルトで本番モードで起動します。

デフォルトでは、**auto-reload** は無効です。また、IP アドレス `0.0.0.0`（利用可能なすべての IP アドレスを意味します）で待ち受けるため、そのマシンと通信できる任意のクライアントから公開アクセスが可能になります。これは、たとえばコンテナ内など、本番環境で一般的な実行方法です。

多くの場合（そして推奨されるのは）、上位に HTTPS を終端する「termination proxy」を置きます。これはアプリのデプロイ方法に依存し、プロバイダが代行する場合もあれば、自分で設定する必要がある場合もあります。

/// tip | 豆知識

詳しくは、[デプロイのドキュメント](deployment/index.md){.internal-link target=_blank}を参照してください。

///
