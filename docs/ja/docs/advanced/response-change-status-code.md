# レスポンス - ステータスコードの変更 { #response-change-status-code }

すでに、デフォルトの[レスポンスのステータスコード](../tutorial/response-status-code.md){.internal-link target=_blank}を設定できることをご存知かもしれません。

しかし場合によっては、デフォルトとは異なるステータスコードを返す必要があります。

## ユースケース { #use-case }

たとえば、デフォルトでは HTTP ステータスコード "OK" `200` を返したいとします。

しかし、データが存在しなければそれを作成し、HTTP ステータスコード "CREATED" `201` を返したい。

それでも、返すデータは `response_model` でフィルタ・変換できるようにしておきたい。

そのような場合は `Response` パラメータを使えます。

## `Response` パラメータを使う { #use-a-response-parameter }

*path operation* 関数で `Response` 型のパラメータを宣言できます（Cookie やヘッダーと同様です）。

そして、その*一時的な*レスポンスオブジェクトに `status_code` を設定できます。

{* ../../docs_src/response_change_status_code/tutorial001_py310.py hl[1,9,12] *}

その後は通常どおり、必要な任意のオブジェクト（`dict`、データベースモデルなど）を返せます。

そして `response_model` を宣言していれば、返したオブジェクトのフィルタと変換には引き続きそれが使われます。

FastAPI はその*一時的な*レスポンスからステータスコード（および Cookie とヘッダー）を取り出し、`response_model` によってフィルタ済みの返却値を含む最終的なレスポンスに反映します。

また、`Response` パラメータは依存関係内に宣言してステータスコードを設定することもできます。ただし、最後に設定されたものが優先される点に注意してください。
