# レスポンス - ヘッダ<!-- # Response Headers -->

<!-- ## Use a `Response` parameter -->

## `Response`パラメータの利用

<!-- You can declare a parameter of type `Response` in your *path operation function* (as you can do for cookies). -->

_path operation 関数_ で`Response`型のパラメータを宣言できます(クッキーの場合と同様です)。

<!-- And then you can set headers in that *temporal* response object. -->

これは、_temporal_ なレスポンスオブジェクトにヘッダを設定することになります。

```Python hl_lines="1  7-8"
{!../../../docs_src/response_headers/tutorial002.py!}
```

<!-- And then you can return any object you need, as you normally would (a `dict`, a database model, etc). -->

必要なオブジェクト(`dict`やデータベースのモデルなど)もいつもどおり返せます。

<!-- And if you declared a `response_model`, it will still be used to filter and convert the object you returned. -->

また、`response_model`を宣言した場合も、返されたオブジェクトをフィルタリングして変換します。

<!-- **FastAPI** will use that *temporal* response to extract the headers (also cookies and status code), and will put them in the final response that contains the value you returned, filtered by any `response_model`. -->

**FastAPI** はその _temporal_ レスポンスを使用してクッキー(ヘッダとステータスコードも)を取り出し、任意の`response_model`によってフィルタリングされて、返したい値を含む最後のレスポンスに展開します。

<!-- You can also declare the `Response` parameter in dependencies, and set headers (and cookies) in them. -->

依存関係の中で`Response`パラメータを宣言し、その中でヘッダ(とクッキー)設定することもできます。

<!-- ## Return a `Response` directly -->

## `Response`を直接返す

<!-- You can also add headers when you return a `Response` directly. -->

コード内で直接`Response`を返すときに、ヘッダを作成することもできます。

<!-- Create a response as described in [Return a Response Directly](response-directly.md){.internal-link target=_blank} and pass the headers as an additional parameter: -->

[Return a Response Directly](response-directly.md){.internal-link target=\_blank}の説明どおりにレスポンスを作成し、追加パラメータとしてヘッダを渡します:

```Python hl_lines="10-12"
{!../../../docs_src/response_headers/tutorial001.py!}
```

<!-- !!! note "Technical Details" -->

!!! note "技術詳細"

    <!-- You could also use `from starlette.responses import Response` or `from starlette.responses import JSONResponse`. -->

    `from starlette.responses import Response`や`from starlette.responses import JSONResponse`を使用することもできます。

    <!-- **FastAPI** provides the same `starlette.responses` as `fastapi.responses` just as a convenience for you, the developer. But most of the available responses come directly from Starlette. -->
    **FastAPI** は、開発者が便利に利用できるように、`FastAPI.responses`と同じ`starlette.responses`を提供しています。しかし、利用可能なレスポンスはほとんどはStarletteが直接処理しています。

    <!-- And as the `Response` can be used frequently to set headers and cookies, **FastAPI** also provides it at `fastapi.Response`. -->
    また、`Response`はヘッダやクッキーの設定に頻繁に使用されるため、 **FastAPI** では`FastAPI.Response`でも提供されています。

<!-- ## Custom Headers -->

## カスタムヘッダ

<!-- Keep in mind that custom proprietary headers can be added <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">using the 'X-' prefix</a>. -->

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">"X-"から始まるプレフィックスを使用して</a>、独自のカスタムヘッダを追加できることを覚えておきましょう。

<!-- But if you have custom headers that you want a client in a browser to be able to see, you need to add them to your CORS configurations (read more in [CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md){.internal-link target=_blank}), using the parameter `expose_headers` documented in <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette's CORS docs</a>. -->

しかし、ブラウザにてクライアントに表示させたいカスタムヘッダがある場合、カスタムヘッダを CORS 設定に追加する必要があり(詳細については、[CORS (Cross-Origin Resource Sharing)](./tutorial/cors.md){.internal-link target=\_blank}を参照してください)、<a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette's CORS docs</a>に記載されている`expose_headers`パラメータを使用してください。
