# レスポンスヘッダー { #response-headers }

## `Response` パラメータを使う { #use-a-response-parameter }

（Cookie と同様に）*path operation 関数*で `Response` 型のパラメータを宣言できます。

そして、その*一時的*なレスポンスオブジェクトにヘッダーを設定できます。

{* ../../docs_src/response_headers/tutorial002_py310.py hl[1, 7:8] *}

その後は通常どおり、必要な任意のオブジェクト（`dict`、データベースモデルなど）を返せます。

`response_model` を宣言している場合は、返したオブジェクトのフィルタと変換に引き続き使用されます。

**FastAPI** はその*一時的*なレスポンスからヘッダー（Cookie やステータスコードも含む）を取り出し、`response_model` によってフィルタされた返却値を含む最終的なレスポンスに反映します。

また、依存関係の中で `Response` パラメータを宣言し、その中でヘッダー（や Cookie）を設定することもできます。

## `Response` を直接返す { #return-a-response-directly }

`Response` を直接返す場合にもヘッダーを追加できます。

[Response を直接返す](response-directly.md){.internal-link target=_blank} で説明したようにレスポンスを作成し、ヘッダーを追加のパラメータとして渡します:

{* ../../docs_src/response_headers/tutorial001_py310.py hl[10:12] *}

/// note | 技術詳細

`from starlette.responses import Response` や `from starlette.responses import JSONResponse` を使うこともできます。

**FastAPI** は、開発者であるあなたへの便宜として、`starlette.responses` と同じものを `fastapi.responses` として提供しています。しかし、利用可能なレスポンスの大半は直接 Starlette から来ています。

また、`Response` はヘッダーや Cookie を設定するのによく使われるため、**FastAPI** は `fastapi.Response` でも提供しています。

///

## カスタムヘッダー { #custom-headers }

独自のカスタムヘッダーは、<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">`X-` プレフィックスを使って</a>追加できることに注意してください。

ただし、ブラウザのクライアントに見えるようにしたいカスタムヘッダーがある場合は、CORS 設定にそれらを追加する必要があります（[CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md){.internal-link target=_blank} を参照）。このとき、<a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette の CORS ドキュメント</a>に記載の `expose_headers` パラメータを使用します。
