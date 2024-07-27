# レスポンス - ステータスコードの変更 <!-- # Response - Change Status Code -->

<!-- You probably read before that you can set a default [Response Status Code](../tutorial/response-status-code.md){.internal-link target=_blank}. -->
デフォルトの[Response Status Code](./tutorial/response-status-code.md){.internal-link target=_blank}の設定方法は以前に読みましたね。

<!-- But in some cases you need to return a different status code than the default. -->
ただ、場合によっては、デフォルトとは異なるステータスコードを返したいことがあります。

<!-- ## Use case -->
## ユースケース

<!-- For example, imagine that you want to return an HTTP status code of "OK" `200` by default. -->
例えば、デフォルトで`200`"OK"のHTTPステータスコードを返したいとします。

<!-- But if the data didn't exist, you want to create it, and return an HTTP status code of "CREATED" `201`. -->
しかし、データが存在しない場合は、そのデータを作成して、`201`"CREATED"のHTTPステータスコードを返したいとします。

<!-- But you still want to be able to filter and convert the data you return with a `response_model`. -->
それに、返されたデータを`response_model`でフィルタリングして変換できるようにしたい場合もあります。

<!-- For those cases, you can use a `Response` parameter. -->
このような場合は、`Response`パラメータを使用しましょう。

<!-- ## Use a `Response` parameter -->
## Responseパラメータの利用

<!-- You can declare a parameter of type `Response` in your *path operation function* (as you can do for cookies and headers). -->
*path operation関数*で`Response`型のパラメータを宣言することができます(クッキーやヘッダの場合と同じです)。

<!-- And then you can set the `status_code` in that *temporal* response object. -->
次に、*temporal*なレスポンスオブジェクトに`status_code`を設定します。

```Python hl_lines="1  9  12"
{!../../../docs_src/response_change_status_code/tutorial001.py!}
```

<!-- And then you can return any object you need, as you normally would (a `dict`, a database model, etc). -->
必要なオブジェクト(`dict`やデータベースモデルなど)もいつもどおり返せます。

<!-- And if you declared a `response_model`, it will still be used to filter and convert the object you returned. -->
また、`response_model`を宣言した場合も、返されたオブジェクトをフィルタリングして変換します。

<!-- **FastAPI** will use that *temporal* response to extract the status code (also cookies and headers), and will put them in the final response that contains the value you returned, filtered by any `response_model`. -->
**FastAPI**はその*temporal*レスポンスを使用してステータスコード(クッキーとヘッダも)を取り出し、任意の`response_model`によってフィルタリングされて、返したい値を含む最後のレスポンスに展開します。

<!-- You can also declare the `Response` parameter in dependencies, and set the status code in them. But keep in mind that the last one to be set will win. -->
`Response`パラメータを依存関係で宣言し、その中にステータスコードを設定することもできます。ただし、最後に設定されたものが優先されることに注意が必要です。
