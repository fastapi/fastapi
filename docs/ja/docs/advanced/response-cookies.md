# クッキーのレスポンス <!-- # Response Cookies -->

<!-- ## Use a `Response` parameter -->
## `Response`パラメータの利用

<!-- You can declare a parameter of type `Response` in your *path operation function*. -->
*path operation関数*の中で`Response`型のパラメータを宣言できます。

<!-- And then you can set cookies in that *temporal* response object. -->
これは、*temporal*なレスポンスオブジェクトにクッキーを設定することになります。

```Python hl_lines="1  8-9"
{!../../../docs_src/response_cookies/tutorial002.py!}
```

<!-- And then you can return any object you need, as you normally would (a `dict`, a database model, etc). -->
必要なオブジェクト(`dict`やデータベースモデルなど)もいつもどおり返せます。

<!-- And if you declared a `response_model`, it will still be used to filter and convert the object you returned. -->
また、`response_model`を宣言した場合も、返されたオブジェクトをフィルタリングして変換します。

<!-- **FastAPI** will use that *temporal* response to extract the cookies (also headers and status code), and will put them in the final response that contains the value you returned, filtered by any `response_model`. -->

**FastAPI**はその*temporal*レスポンスを使用してクッキー(ヘッダとステータスコードも)を取り出し、任意の`response_model`によってフィルタリングされて、返したい値を含む最後のレスポンスに展開します。

<!-- You can also declare the `Response` parameter in dependencies, and set cookies (and headers) in them. -->
依存関係の中で`Response`パラメータを宣言し、その中でクッキー(とヘッダ)設定することもできます。

<!-- ## Return a `Response` directly -->
## `Response`を直接返す

<!-- You can also create cookies when returning a `Response` directly in your code. -->
コード内で直接`Response`を返すときに、クッキーを作成することもできます。

<!-- To do that, you can create a response as described in [Return a Response Directly](response-directly.md){.internal-link target=_blank}. -->
そのためには、[Return a Response Directly](response-directly.md){.internal-link target=_blank}で説明されているように、レスポンスを作成します。

<!-- Then set Cookies in it, and then return it: -->
その中にクッキーをセットして返せます：

```Python hl_lines="10-12"
{!../../../docs_src/response_cookies/tutorial001.py!}
```

!!! tip "豆知識"
    <!-- Keep in mind that if you return a response directly instead of using the `Response` parameter, FastAPI will return it directly. -->
    もし`Response`パラメータを使用せずに直接レスポンスを返すと、 FastAPIは直接レスポンスを返すことに注意してください。

    <!-- So, you will have to make sure your data is of the correct type. E.g. it is compatible with JSON, if you are returning a `JSONResponse`. -->
    そこで、データが正しい型であることを確認する必要があります。例えば、`JSONResponse`を返すのであれば、JSONと互換性がを持たせてください。

    <!-- And also that you are not sending any data that should have been filtered by a `response_model`. -->
    また、`response_model`によってフィルタリングされるべきデータを送信していないことも確認する必要があります。

<!-- ### More info -->
### さらなる情報

<!-- !!! note "Technical Details" -->
!!! note "技術詳細"
    <!-- You could also use `from starlette.responses import Response` or `from starlette.responses import JSONResponse`. -->
    `from starlette.responses import Response`や`from starlette.responses import JSONResponse`を使用することもできます。

    <!-- **FastAPI** provides the same `starlette.responses` as `fastapi.responses` just as a convenience for you, the developer. But most of the available responses come directly from Starlette. -->
    **FastAPI**は、開発者が便利に利用できるように、`FastAPI.responses`と同じ`starlette.responses`を提供しています。しかし、利用可能なレスポンスはほとんどはStarletteが直接処理しています。

    <!-- And as the `Response` can be used frequently to set headers and cookies, **FastAPI** also provides it at `fastapi.Response`. -->
    また、`Response`はヘッダーやクッキーの設定に頻繁に使用されるため、**FastAPI**では`FastAPI.Response`でも提供されています。


<!-- To see all the available parameters and options, check the <a href="https://www.starlette.io/responses/#set-cookie" class="external-link" target="_blank">documentation in Starlette</a>. -->
使用可能なすべてのパラメータとオプションを確認するには、<a href="https://www.starlette.io/responses/#set-cookie" class="external-link" target="_blank">documentation in Starlette</a>を参照してください。
