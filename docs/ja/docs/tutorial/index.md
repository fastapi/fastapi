# チュートリアル - ユーザーガイド { #tutorial-user-guide }

このチュートリアルでは、**FastAPI**のほとんどの機能を使う方法を段階的に紹介します。

各セクションは前のセクションを踏まえた内容になっています。しかし、トピックごとに分割されているので、特定のAPIのニーズを満たすために、任意の特定のトピックに直接進めるようになっています。

また、将来的にリファレンスとして機能するように構築されているので、後で戻ってきて必要なものを正確に確認できます。

## コードを実行する { #run-the-code }

すべてのコードブロックをコピーして直接使用できます（実際にテストされたPythonファイルです）。

いずれかの例を実行するには、コードを `main.py`ファイルにコピーし、`uv run` で `fastapi dev` を起動します:

<div class="termy">

```console
$ <font color="#4E9A06">uv run fastapi</font> dev

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

最初のステップは、プロジェクトをセットアップして FastAPI を追加することです。

[`uv`](https://docs.astral.sh/uv/getting-started/installation/) をインストールし、プロジェクトを作成して FastAPI を追加します:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"

---> 100%
```

</div>

`uv add` はプロジェクトの仮想環境を `.venv` に作成し、FastAPI を `pyproject.toml` に追加し、後で同じパッケージバージョンをインストールできるように `uv.lock` を作成します。

/// details | これらのコマンドが行うこと

* `uv init`: 新しい Python プロジェクトを作成します。
* `awesome-project`: この名前の新しいディレクトリにプロジェクトを作成します。
* `--bare`: サンプルの `main.py`、`README.md`、その他のファイルを生成せず、最小限の `pyproject.toml` ファイルだけを作成します。このチュートリアルの次のステップで、アプリケーションファイルは自分で作成します。

その後、FastAPI を追加する前に `cd awesome-project` で新しいプロジェクトディレクトリに入ります。

`uv` は、システムにすでにインストールされている互換性のある Python バージョンを使用するか、必要に応じてダウンロードします。

`uv add` を実行すると、FastAPI と FastAPI が依存するすべてのパッケージの互換性のあるバージョンが選択されます。正確なバージョンは `uv.lock` に記録されるため、後で別のコンピューターやアプリケーションをデプロイするときに同じパッケージバージョンをインストールできます。

このファイルを作成または更新することを、[プロジェクト依存関係を**ロック**すること](https://docs.astral.sh/uv/concepts/projects/sync/)と呼びます。`uv` はパッケージを追加するときにこれを自動的に行います。

///

/// details | FastAPI のインストールオプション

`uv add "fastapi[standard]"` でインストールすると、`fastapi-cloud-cli` を含むいくつかのデフォルトのオプション標準依存関係が付属します。これにより、[FastAPI Cloud](https://fastapicloud.com) にデプロイできます。

これらのオプション依存関係が不要な場合は、代わりに `uv add fastapi` をインストールできます。

標準依存関係はインストールしたいが `fastapi-cloud-cli` は不要な場合は、`uv add "fastapi[standard-no-fastapi-cloud-cli]"` でインストールできます。

///

/// details | 代わりに `pip` を使用する

仮想環境とパッケージを手動で管理したい場合は、仮想環境を作成して有効化し、それから `pip install "fastapi[standard]"` で FastAPI をインストールします。

詳しい手順は [仮想環境ガイド](https://tiangolo.com/guides/virtual-environments/) を読んでください。

///

## AI Agent Skills { #ai-agent-skills }

FastAPI には、AI coding agents 向けの公式スキルが含まれています。これはパッケージに同梱されているため、そのガイダンスはプロジェクトにインストールされている FastAPI のバージョンと一致し、FastAPI を更新すると一緒に更新されます。

プロジェクトに FastAPI をインストールした後、<a href="https://library-skills.io">Library Skills</a> でスキルをインストールできます:

```bash
uvx library-skills
```

/// note | 備考

`uvx` は `uv tool run` のエイリアスです。Library Skills がプロジェクトにインストールされたパッケージをスキャンする間、一時的で分離された環境で Library Skills を実行します。

///

このスキルは Codex、Claude Code、Cursor、GitHub Copilot、Gemini CLI、Pi、OpenCode、およびその他ほとんどの coding agent と互換性があります。Claude Code の場合、スキルのインストール先を尋ねられたら `.claude/skills` を選択してください。

## 高度なユーザーガイド { #advanced-user-guide }

この **チュートリアル - ユーザーガイド** の後で、後から読める **高度なユーザーガイド** もあります。

**高度なユーザーガイド** は本チュートリアルをベースにしており、同じ概念を使用し、いくつかの追加機能を教えます。

ただし、最初に **チュートリアル - ユーザーガイド**（今読んでいる内容）をお読みください。

**チュートリアル - ユーザーガイド** だけで完全なアプリケーションを構築できるように設計されており、その後ニーズに応じて、**高度なユーザーガイド** の追加のアイデアのいくつかを使って、さまざまな方法で拡張できます。
