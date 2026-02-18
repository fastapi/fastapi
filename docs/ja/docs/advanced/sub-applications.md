# サブアプリケーション - マウント { #sub-applications-mounts }

それぞれ独立した OpenAPI とドキュメント UI を持つ2つの独立した FastAPI アプリケーションが必要な場合、メインアプリに1つ（以上）のサブアプリケーションを「マウント」できます。

## FastAPI アプリケーションのマウント { #mounting-a-fastapi-application }

「マウント」とは、特定のパスに完全に「独立した」アプリケーションを追加し、そのサブアプリケーションで宣言された path operation によって、そのパス以下のすべてを処理させることを意味します。

### トップレベルアプリケーション { #top-level-application }

まず、メインのトップレベル **FastAPI** アプリケーションと、その path operation を作成します:

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[3, 6:8] *}

### サブアプリケーション { #sub-application }

次に、サブアプリケーションとその path operation を作成します。

このサブアプリケーションは通常の FastAPI アプリケーションですが、これを「マウント」します:

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[11, 14:16] *}

### サブアプリケーションをマウント { #mount-the-sub-application }

トップレベルのアプリケーション `app` に、サブアプリケーション `subapi` をマウントします。

この例では、パス `/subapi` にマウントされます:

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[11, 19] *}

### 自動 API ドキュメントの確認 { #check-the-automatic-api-docs }

では、`fastapi` コマンドでこのファイルを実行します:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

そして、<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> を開きます。

メインアプリ用の自動 API ドキュメントが表示され、そのアプリ自身の path operation のみが含まれます:

<img src="/img/tutorial/sub-applications/image01.png">

次に、サブアプリケーションのドキュメント <a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">http://127.0.0.1:8000/subapi/docs</a> を開きます。

サブアプリケーション用の自動 API ドキュメントが表示され、そのアプリ自身の path operation のみが、正しいサブパス接頭辞 `/subapi` の下で表示されます:

<img src="/img/tutorial/sub-applications/image02.png">

どちらの UI でも操作すれば正しく動作します。ブラウザがそれぞれのアプリ／サブアプリと通信できるためです。

### 技術詳細: `root_path` { #technical-details-root-path }

上記のようにサブアプリケーションをマウントすると、FastAPI は ASGI 仕様の `root_path` と呼ばれる仕組みを使って、そのサブアプリケーションへのマウントパスを伝播します。

このため、サブアプリケーションはドキュメント UI でそのパス接頭辞を使用すべきことを認識できます。

さらに、サブアプリケーション自身が別のサブアプリケーションをマウントしていても問題ありません。FastAPI がこれらの `root_path` をすべて自動的に処理するためです。

`root_path` の詳細や明示的な指定方法については、[プロキシの背後で](behind-a-proxy.md){.internal-link target=_blank} の節で学べます。
