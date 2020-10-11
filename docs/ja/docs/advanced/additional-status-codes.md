# 追加のステータスコード

デフォルトでは、 **FastAPI** は `JSONResponse` を使ってレスポンスを返します。その `JSONResponse` の中には、 *path operation* が返した内容が入ります。

それは、デフォルトのステータスコードか、 *path operation* でセットしたものを利用します。

## 追加のステータスコード

メインのステータスコードとは別に追加のステータスコードを返したい場合は、追加のステータスコードが設定された `JSONResponse` のような `Response` を直接返します。

例えば、itemを更新し、成功した場合は200 "OK"のHTTPステータスコードを返す *path operation* を作りたいとします。

しかし、新しいitemも許可したいです。itemが存在しない場合は、それらを作成して201 "Created"を返します。

これを達成するには、 `JSONResponse` をインポートし、 `status_code` を設定して直接内容を返します。

```Python hl_lines="4  23"
{!../../../docs_src/additional_status_codes/tutorial001.py!}
```

!!! warning "注意"
    上記の例のように `Response` を直接返す場合、それは直接返されます。

    モデルなどはシリアライズされません。

    必要なデータが含まれていることや、値が有効なJSONであること (`JSONResponse` を使う場合) を確認してください。

!!! note "技術詳細"
    `from starlette.responses import JSONResponse` を利用することもできます。

    **FastAPI** は `fastapi.responses` と同じ `starlette.responses` を、開発者の利便性のために提供しています。しかし有効なレスポンスはほとんどStarletteから来ています。 `status` についても同じです。

## OpenAPIとAPIドキュメント

もし追加のステータスコードとレスポンスを直接返す場合、それらはOpenAPIスキーマ (APIドキュメント) には含まれません。なぜなら、FastAPIは何が返されるのか事前に知ることができないからです。

しかし、 [Additional Responses](additional-responses.md){.internal-link target=_blank} を使ってコードの中にドキュメントを書くことができます。
