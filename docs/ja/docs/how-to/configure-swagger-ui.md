# Swagger UI の設定 { #configure-swagger-ui }

いくつかの追加の <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">Swagger UI パラメータ</a>を設定できます。

設定するには、`FastAPI()` のアプリオブジェクトを作成するとき、または `get_swagger_ui_html()` 関数に `swagger_ui_parameters` 引数を渡します。

`swagger_ui_parameters` は、Swagger UI に直接渡される設定を含む辞書を受け取ります。

FastAPI はそれらの設定を **JSON** に変換し、JavaScript と互換にします。Swagger UI が必要とするのはこの形式です。

## シンタックスハイライトを無効化 { #disable-syntax-highlighting }

例えば、Swagger UI のシンタックスハイライトを無効化できます。

設定を変更しなければ、シンタックスハイライトはデフォルトで有効です:

<img src="/img/tutorial/extending-openapi/image02.png">

しかし、`syntaxHighlight` を `False` に設定すると無効化できます:

{* ../../docs_src/configure_swagger_ui/tutorial001_py310.py hl[3] *}

...その場合、Swagger UI ではシンタックスハイライトが表示されなくなります:

<img src="/img/tutorial/extending-openapi/image03.png">

## テーマの変更 { #change-the-theme }

同様に、キー `"syntaxHighlight.theme"`（途中にドットが含まれている点に注意）でシンタックスハイライトのテーマを設定できます:

{* ../../docs_src/configure_swagger_ui/tutorial002_py310.py hl[3] *}

この設定により、シンタックスハイライトの配色テーマが変わります:

<img src="/img/tutorial/extending-openapi/image04.png">

## 既定の Swagger UI パラメータの変更 { #change-default-swagger-ui-parameters }

FastAPI には、多くのユースケースに適した既定の設定パラメータが含まれています。

既定では次の設定が含まれます:

{* ../../fastapi/openapi/docs.py ln[9:24] hl[18:24] *}

引数 `swagger_ui_parameters` に別の値を指定することで、これらを上書きできます。

例えば、`deepLinking` を無効化するには、次の設定を `swagger_ui_parameters` に渡します:

{* ../../docs_src/configure_swagger_ui/tutorial003_py310.py hl[3] *}

## その他の Swagger UI パラメータ { #other-swagger-ui-parameters }

利用可能な他のすべての設定については、公式の <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">Swagger UI パラメータのドキュメント</a>を参照してください。

## JavaScript 専用の設定 { #javascript-only-settings }

Swagger UI では、他にも **JavaScript 専用** のオブジェクト（例: JavaScript の関数）による設定が可能です。

FastAPI には、次の JavaScript 専用の `presets` 設定も含まれています:

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

これらは文字列ではなく **JavaScript** のオブジェクトであるため、Python のコードから直接渡すことはできません。

そのような JavaScript 専用の設定を使う必要がある場合は、上記のいずれかの方法を使用し、Swagger UI の path operation をオーバーライドして、必要な JavaScript を手動で記述してください。
