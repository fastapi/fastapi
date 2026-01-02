# チュートリアル - ユーザーガイド { #tutorial-user-guide }

このチュートリアルでは、**FastAPI**のほとんどの機能を使う方法を段階的に紹介します。

各セクションは前のセクションを踏まえた内容になっています。しかし、トピックごとに分割されているので、特定のAPIのニーズを満たすために、任意の特定のトピックに直接進めるようになっています。

また、将来的にリファレンスとして機能するように構築されているので、後で戻ってきて必要なものを正確に確認できます。

## コードを実行する { #run-the-code }

すべてのコードブロックをコピーして直接使用できます（実際にテストされたPythonファイルです）。

いずれかの例を実行するには、コードを `main.py`ファイルにコピーし、次のように `fastapi dev` を起動します:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

コードを記述またはコピーし、編集してローカルで実行することを**強く推奨します**。

エディターで使用することで、書く必要のあるコードの少なさ、すべての型チェック、自動補完など、FastAPIの利点を本当に実感できます。

---

## FastAPIをインストールする { #install-fastapi }

最初のステップは、FastAPIのインストールです。

[仮想環境](../virtual-environments.md){.internal-link target=_blank} を作成して有効化し、それから **FastAPIをインストール** してください:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note | 備考

`pip install "fastapi[standard]"` でインストールすると、`fastapi-cloud-cli` を含むいくつかのデフォルトのオプション標準依存関係が付属します。これにより、<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a> にデプロイできます。

これらのオプション依存関係が不要な場合は、代わりに `pip install fastapi` をインストールできます。

標準依存関係はインストールしたいが `fastapi-cloud-cli` は不要な場合は、`pip install "fastapi[standard-no-fastapi-cloud-cli]"` でインストールできます。

///

## 高度なユーザーガイド { #advanced-user-guide }

この **チュートリアル - ユーザーガイド** の後で、後から読める **高度なユーザーガイド** もあります。

**高度なユーザーガイド** は本チュートリアルをベースにしており、同じ概念を使用し、いくつかの追加機能を教えます。

ただし、最初に **チュートリアル - ユーザーガイド**（今読んでいる内容）をお読みください。

**チュートリアル - ユーザーガイド** だけで完全なアプリケーションを構築できるように設計されており、その後ニーズに応じて、**高度なユーザーガイド** の追加のアイデアのいくつかを使って、さまざまな方法で拡張できます。
