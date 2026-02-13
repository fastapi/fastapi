# サーバーを手動で実行する { #run-a-server-manually }

## fastapi run コマンドを使う { #use-the-fastapi-run-command }

結論として、FastAPI アプリケーションを提供するには `fastapi run` を使います:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>2306215</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
```

</div>

これでほとんどのケースは動作します。😎

このコマンドは、たとえばコンテナやサーバー内で **FastAPI** アプリを起動するのに使えます。

## ASGIサーバー { #asgi-servers }

少し詳しく見ていきます。

FastAPI は、Python の Web フレームワークとサーバーのための標準である <abbr title="Asynchronous Server Gateway Interface - 非同期サーバーゲートウェイインターフェース">ASGI</abbr> を使います。FastAPI は ASGI Web フレームワークです。

リモートのサーバーマシンで **FastAPI** アプリケーション（や他の ASGI アプリケーション）を実行するのに主に必要なのは **Uvicorn** のような ASGI サーバープログラムです。これは `fastapi` コマンドにデフォルトで含まれています。

他にもいくつかの選択肢があります:

* <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a>: 高性能な ASGI サーバー。
* <a href="https://hypercorn.readthedocs.io/" class="external-link" target="_blank">Hypercorn</a>: HTTP/2 や Trio に対応する ASGI サーバーなど。
* <a href="https://github.com/django/daphne" class="external-link" target="_blank">Daphne</a>: Django Channels のために作られた ASGI サーバー。
* <a href="https://github.com/emmett-framework/granian" class="external-link" target="_blank">Granian</a>: Python アプリケーション向けの Rust 製 HTTP サーバー。
* <a href="https://unit.nginx.org/howto/fastapi/" class="external-link" target="_blank">NGINX Unit</a>: 軽量で多用途な Web アプリケーションランタイム。

## サーバーマシンとサーバープログラム { #server-machine-and-server-program }

名称に関する小さな注意点があります。💡

「サーバー」という言葉は、リモート/クラウド上のコンピュータ（物理/仮想マシン）と、そのマシン上で動作しているプログラム（例: Uvicorn）の両方を指すのに一般的に使われます。

一般に「サーバー」と書かれているときは、そのどちらかを指している可能性があることを覚えておいてください。

リモートマシンを指す場合、「サーバー」のほか「マシン」「VM（仮想マシン）」「ノード」などとも呼ばれます。いずれも通常 Linux を実行し、そこでプログラムを動かすリモートマシンを指します。

## サーバープログラムをインストール { #install-the-server-program }

FastAPI をインストールすると、本番サーバーの Uvicorn が同梱されており、`fastapi run` コマンドで起動できます。

ただし、ASGI サーバーを手動でインストールすることもできます。

[仮想環境](../virtual-environments.md){.internal-link target=_blank}を作成して有効化し、サーバーアプリケーションをインストールしてください。

例として、Uvicorn をインストールするには:

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

他の ASGI サーバープログラムでも同様の手順です。

/// tip | 豆知識

`standard` を付けると、Uvicorn は推奨の追加依存関係もインストールして使用します。

その中には、`asyncio` の高性能なドロップイン代替であり、大きな並行実行性能の向上をもたらす `uvloop` も含まれます。

`pip install "fastapi[standard]"` のように FastAPI をインストールした場合は、すでに `uvicorn[standard]` も含まれます。

///

## サーバープログラムを起動 { #run-the-server-program }

ASGI サーバーを手動でインストールした場合、通常は FastAPI アプリケーションをインポートさせるために、特別な形式のインポート文字列を渡す必要があります:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note | 備考

`uvicorn main:app` というコマンドは次を指します:

* `main`: ファイル `main.py`（Python の「モジュール」）。
* `app`: `main.py` 内で `app = FastAPI()` により作成されたオブジェクト。

これは次と等価です:

```Python
from main import app
```

///

他の ASGI サーバープログラムでも同様のコマンドがあり、詳細はそれぞれのドキュメントを参照してください。

/// warning | 注意

Uvicorn などのサーバーは、開発時に便利な `--reload` オプションをサポートしています。

しかし `--reload` は多くのリソースを消費し、不安定になるなどの性質があります。

開発中には非常に役立ちますが、 本番環境では使用すべきではありません。

///

## デプロイの概念 { #deployment-concepts }

これらの例は、サーバープログラム（例: Uvicorn）を実行し、事前に決めたポート（例: `80`）で、すべての IP（`0.0.0.0`）をリッスンする「単一プロセス」を起動します。

これが基本的な考え方です。ただし、次のような追加事項にも対応したくなるでしょう:

* セキュリティ - HTTPS
* 起動時に実行
* 再起動
* レプリケーション（実行プロセス数）
* メモリ
* 起動前の事前ステップ

これらの各概念についての考え方や、対処するための具体例・戦略を次の章で説明します。🚀
