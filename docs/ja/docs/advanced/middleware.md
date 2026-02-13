# 高度なミドルウェア { #advanced-middleware }

メインのチュートリアルでは、アプリケーションに[カスタムミドルウェア](../tutorial/middleware.md){.internal-link target=_blank}を追加する方法を学びました。

そして、[`CORSMiddleware` を使った CORS の扱い方](../tutorial/cors.md){.internal-link target=_blank}も学びました。

このセクションでは、その他のミドルウェアの使い方を見ていきます。

## ASGI ミドルウェアの追加 { #adding-asgi-middlewares }

**FastAPI** は Starlette を基盤としており、<abbr title="Asynchronous Server Gateway Interface - 非同期サーバーゲートウェイインターフェース">ASGI</abbr> 仕様を実装しているため、任意の ASGI ミドルウェアを利用できます。

ミドルウェアは ASGI 仕様に従っていれば、FastAPI や Starlette 専用に作られていなくても動作します。

一般に、ASGI ミドルウェアは最初の引数として ASGI アプリを受け取るクラスです。

そのため、サードパーティの ASGI ミドルウェアのドキュメントでは、おそらく次のように書かれているでしょう:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

しかし FastAPI（正確には Starlette）は、内部ミドルウェアがサーバーエラーを処理し、カスタム例外ハンドラが正しく動作することを保証する、より簡単な方法を提供しています。

そのためには（CORS の例と同様に）`app.add_middleware()` を使います。

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` は、最初の引数にミドルウェアのクラスを取り、それ以外の追加引数はミドルウェアに渡されます。

## 組み込みミドルウェア { #integrated-middlewares }

**FastAPI** は一般的なユースケースに対応するいくつかのミドルウェアを含んでいます。以下でその使い方を見ていきます。

/// note | 技術詳細

以下の例では、`from starlette.middleware.something import SomethingMiddleware` を使うこともできます。

**FastAPI** は開発者であるあなたの便宜のために `fastapi.middleware` にいくつかのミドルウェアを提供しています。しかし、利用可能なミドルウェアの多くは Starlette から直接提供されています。

///

## `HTTPSRedirectMiddleware` { #httpsredirectmiddleware }

すべての受信リクエストが `https` または `wss` でなければならないように強制します。

`http` または `ws` への受信リクエストは、安全なスキームにリダイレクトされます。

{* ../../docs_src/advanced_middleware/tutorial001_py310.py hl[2,6] *}

## `TrustedHostMiddleware` { #trustedhostmiddleware }

HTTP Host Header 攻撃を防ぐため、すべての受信リクエストに正しく設定された `Host` ヘッダーを強制します。

{* ../../docs_src/advanced_middleware/tutorial002_py310.py hl[2,6:8] *}

サポートされる引数は次のとおりです:

- `allowed_hosts` - 許可するホスト名のドメイン名リスト。`*.example.com` のようなワイルドカードドメインでサブドメインのマッチングもサポートします。任意のホスト名を許可するには、`allowed_hosts=["*"]` を使うか、このミドルウェアを省略します。
- `www_redirect` - True に設定すると、許可されたホストの非 www 版へのリクエストを www 版へリダイレクトします。デフォルトは `True` です。

受信リクエストが正しく検証されない場合、`400` のレスポンスが返されます。

## `GZipMiddleware` { #gzipmiddleware }

`Accept-Encoding` ヘッダーに "gzip" を含むリクエストに対して GZip レスポンスを処理します。

このミドルウェアは、通常のレスポンスとストリーミングレスポンスの両方を処理します。

{* ../../docs_src/advanced_middleware/tutorial003_py310.py hl[2,6] *}

サポートされる引数は次のとおりです:

- `minimum_size` - このバイト数の最小サイズ未満のレスポンスは GZip 圧縮しません。デフォルトは `500` です。
- `compresslevel` - GZip 圧縮時に使用します。1 から 9 までの整数です。デフォルトは `9`。値が小さいほど圧縮は速くなりますがファイルサイズは大きくなり、値が大きいほど圧縮は遅くなりますがファイルサイズは小さくなります。

## その他のミドルウェア { #other-middlewares }

他にも多くの ASGI ミドルウェアがあります。

例えば:

- <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">Uvicorn の `ProxyHeadersMiddleware`</a>
- <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">MessagePack</a>

他に利用可能なミドルウェアについては、<a href="https://www.starlette.dev/middleware/" class="external-link" target="_blank">Starlette のミドルウェアドキュメント</a>や <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">ASGI Awesome List</a> を参照してください。
