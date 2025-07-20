# チュートリアル - ユーザーガイド

このチュートリアルは**FastAPI**のほぼすべての機能の使い方を段階的に紹介します。

各セクションは前のセクションを踏まえた内容になっています。しかし、トピックごとに分割されているので、特定のAPIの要求を満たすようなトピックに直接たどり着けるようになっています。

また、将来的にリファレンスとして機能するように構築されています。

従って、後でこのチュートリアルに戻ってきて必要なものを確認できます。

## コードを実行する

すべてのコードブロックをコピーして直接使用できます（実際にテストされたPythonファイルです）。

いずれかの例を実行するには、コードを `main.py`ファイルにコピーし、` uvicorn`を次のように起動します:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

コードを記述またはコピーし、編集してローカルで実行することを**強くお勧めします**。

また、エディターで使用することで、書く必要のあるコードの少なさ、すべての型チェック、自動補完などのFastAPIの利点を実感できます。

---

## FastAPIをインストールする

最初のステップは、FastAPIのインストールです。

チュートリアルのために、すべてのオプションの依存関係と機能をインストールしたいとき:

<div class="termy">

```console
$ pip install "fastapi[all]"

---> 100%
```

</div>

...これには、コードを実行するサーバーとして使用できる `uvicorn`も含まれます。

/// note | 備考

パーツ毎にインストールすることも可能です。

以下は、アプリケーションを本番環境にデプロイする際に行うであろうものです:

```
pip install fastapi
```

また、サーバーとして動作するように`uvicorn` をインストールします:

```
pip install "uvicorn[standard]"
```

そして、使用したい依存関係をそれぞれ同様にインストールします。

///

## 高度なユーザーガイド

**高度なユーザーガイド**もあり、**チュートリアル - ユーザーガイド**の後で読むことができます。

**高度なユーザーガイド**は**チュートリアル - ユーザーガイド**に基づいており、同じ概念を使用し、いくつかの追加機能を紹介しています。

ただし、最初に**チュートリアル - ユーザーガイド**（現在読んでいる内容）をお読みください。

**チュートリアル-ユーザーガイド**だけで完全なアプリケーションを構築できるように設計されています。加えて、**高度なユーザーガイド**の中からニーズに応じたアイデアを使用して、様々な拡張が可能です。
