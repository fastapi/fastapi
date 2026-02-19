# WSGI の組み込み - Flask、Django など { #including-wsgi-flask-django-others }

[サブアプリケーション - マウント](sub-applications.md){.internal-link target=_blank}、[プロキシの背後](behind-a-proxy.md){.internal-link target=_blank} で見たように、WSGI アプリケーションをマウントできます。

そのために `WSGIMiddleware` を使用して、Flask や Django などの WSGI アプリをラップできます。

## `WSGIMiddleware` の使用 { #using-wsgimiddleware }

/// info | 情報

これには `a2wsgi` のインストールが必要です。例: `pip install a2wsgi`。

///

`a2wsgi` から `WSGIMiddleware` をインポートします。

次に、そのミドルウェアで WSGI（例: Flask）アプリをラップします。

そして、それをあるパスの下にマウントします。

{* ../../docs_src/wsgi/tutorial001_py310.py hl[1,3,23] *}

/// note | 備考

以前は `fastapi.middleware.wsgi` の `WSGIMiddleware` を使用することが推奨されていましたが、現在は非推奨です。

代わりに `a2wsgi` パッケージを使用することを推奨します。使い方は同じです。

`a2wsgi` パッケージがインストールされていることを確認し、`a2wsgi` から `WSGIMiddleware` を正しくインポートしてください。

///

## チェック { #check-it }

これで、パス `/v1/` 配下へのすべてのリクエストは Flask アプリケーションが処理します。

それ以外は **FastAPI** が処理します。

実行して <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a> にアクセスすると、Flask からのレスポンスが表示されます:

```txt
Hello, World from Flask!
```

さらに <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a> にアクセスすると、FastAPI からのレスポンスが表示されます:

```JSON
{
    "message": "Hello World"
}
```
