# 手動デプロイ

**FastAPI** を手動でデプロイすることもできます。

以下の様なASGI対応のサーバをインストールする必要があります:

=== "Uvicorn"

    * <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>, uvloopとhttptoolsを基にした高速なASGIサーバ。

    <div class="termy">

    ```console
    $ pip install uvicorn[standard]

    ---> 100%
    ```

    </div>

!!! tip "豆知識"
    `standard` を加えることで、Uvicornがインストールされ、いくつかの推奨される依存関係を利用するようになります。

    これには、`asyncio` の高性能な完全互換品である `uvloop` が含まれ、並行処理のパフォーマンスが大幅に向上します。

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

停止した場合に自動的に再起動させるツールを設定したいかもしれません。

さらに、<a href="https://gunicorn.org/" class="external-link" target="_blank">Gunicorn</a>をインストールして<a href="https://www.uvicorn.org/#running-with-gunicorn" class="external-link" target="_blank">Uvicornのマネージャーとして使用したり</a>、複数のワーカーでHypercornを使用したいかもしれません。

ワーカー数などの微調整も行いたいかもしれません。

しかしこれら全てをやろうとすると、自動的にこれらを行うDockerイメージを使う方が楽かもしれません。
