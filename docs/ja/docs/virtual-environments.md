# 仮想環境 { #virtual-environments }

Pythonプロジェクトで作業する際は、プロジェクトごとにインストールされるパッケージを分離するために**仮想環境**を使用するべきです。

FastAPIプロジェクトでは、プロジェクト、その依存関係、仮想環境を管理するために [uv](https://docs.astral.sh/uv/) を使用することをおすすめします。

## プロジェクトの作成 { #create-a-project }

[公式インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)に従って `uv` をインストールし、プロジェクトを作成します:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"
```

</div>

`uv` はプロジェクトの仮想環境を自動的に作成します。自分で作成したり有効化したりする必要はありません。

プロジェクト環境内でコマンドを実行するには、例えば次のように `uv run` を使用します:

<div class="termy">

```console
$ uv run fastapi dev
```

</div>

## さらに学ぶ { #learn-more }

仮想環境の内部的な仕組み（有効化や、代替となる `python -m venv` と `pip` のワークフローを含む）については、[仮想環境ガイド](https://tiangolo.com/guides/virtual-environments/)を読んでください。
