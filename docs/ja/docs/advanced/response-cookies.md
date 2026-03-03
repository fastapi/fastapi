# レスポンスの Cookie { #response-cookies }

## `Response` パラメータを使う { #use-a-response-parameter }

*path operation 関数*で `Response` 型のパラメータを宣言できます。

そして、その*一時的*なレスポンスオブジェクトに Cookie を設定できます。

{* ../../docs_src/response_cookies/tutorial002_py310.py hl[1, 8:9] *}

その後は通常どおり、必要な任意のオブジェクト（`dict`、データベースモデルなど）を返せます。

`response_model` を宣言している場合でも、返したオブジェクトは引き続きフィルタおよび変換されます。

**FastAPI** はその*一時的*なレスポンスから Cookie（およびヘッダーやステータスコード）を取り出し、`response_model` によってフィルタされた返却値を含む最終的なレスポンスに設定します。

`Response` パラメータは依存関係でも宣言でき、そこで Cookie（やヘッダー）を設定することも可能です。

## `Response` を直接返す { #return-a-response-directly }

コードで `Response` を直接返すときに、Cookie を作成することもできます。

そのためには、[Response を直接返す](response-directly.md){.internal-link target=_blank} で説明されているとおりにレスポンスを作成します。

そのレスポンスに Cookie を設定してから返します:

{* ../../docs_src/response_cookies/tutorial001_py310.py hl[10:12] *}

/// tip | 豆知識

`Response` パラメータを使わずにレスポンスを直接返す場合、FastAPI はそのレスポンスをそのまま返します。

そのため、データの型が正しいことを確認する必要があります。例えば、`JSONResponse` を返すなら、JSON と互換性がある必要があります。

また、`response_model` によってフィルタされるべきデータを送っていないことも確認してください。

///

### 詳細情報 { #more-info }

/// note | 技術詳細

`from starlette.responses import Response` や `from starlette.responses import JSONResponse` を使うこともできます。

**FastAPI** は開発者の利便性のために、`starlette.responses` と同じものを `fastapi.responses` として提供しています。ただし、利用可能なレスポンスの大半は Starlette から直接提供されています。

また、`Response` はヘッダーや Cookie の設定に頻繁に使われるため、`fastapi.Response` としても提供されています。

///

利用可能なすべてのパラメータやオプションについては、<a href="https://www.starlette.dev/responses/#set-cookie" class="external-link" target="_blank">Starlette のドキュメント</a>を参照してください。
