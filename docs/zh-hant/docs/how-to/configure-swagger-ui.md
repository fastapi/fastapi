# 設定 Swagger UI { #configure-swagger-ui }

你可以設定一些額外的 <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">Swagger UI 參數</a>。

要設定它們，建立 `FastAPI()` 應用物件時，或呼叫 `get_swagger_ui_html()` 函式時，傳入參數 `swagger_ui_parameters`。

`swagger_ui_parameters` 接受一個 dict，內容會直接傳給 Swagger UI 作為設定。

FastAPI 會把這些設定轉換成 JSON，以便與 JavaScript 相容，因為 Swagger UI 需要的是這種格式。

## 停用語法醒目提示 { #disable-syntax-highlighting }

例如，你可以在 Swagger UI 中停用語法醒目提示（syntax highlighting）。

不更動設定時，語法醒目提示預設為啟用：

<img src="/img/tutorial/extending-openapi/image02.png">

但你可以將 `syntaxHighlight` 設為 `False` 來停用它：

{* ../../docs_src/configure_swagger_ui/tutorial001_py310.py hl[3] *}

...然後 Swagger UI 就不會再顯示語法醒目提示：

<img src="/img/tutorial/extending-openapi/image03.png">

## 更換主題 { #change-the-theme }

同樣地，你可以用鍵 `"syntaxHighlight.theme"` 設定語法醒目提示主題（注意中間有一個點）：

{* ../../docs_src/configure_swagger_ui/tutorial002_py310.py hl[3] *}

這個設定會變更語法醒目提示的配色主題：

<img src="/img/tutorial/extending-openapi/image04.png">

## 更改預設的 Swagger UI 參數 { #change-default-swagger-ui-parameters }

FastAPI 內建一些預設參數，適用於大多數情境。

包含以下預設設定：

{* ../../fastapi/openapi/docs.py ln[9:24] hl[18:24] *}

你可以在 `swagger_ui_parameters` 參數中提供不同的值來覆蓋其中任一項。

例如，要停用 `deepLinking`，可以在 `swagger_ui_parameters` 傳入以下設定：

{* ../../docs_src/configure_swagger_ui/tutorial003_py310.py hl[3] *}

## 其他 Swagger UI 參數 { #other-swagger-ui-parameters }

若要查看所有可用的設定，請參考官方的 <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">Swagger UI 參數文件</a>。

## 僅限 JavaScript 的設定 { #javascript-only-settings }

Swagger UI 也允許某些設定是僅限 JavaScript 的物件（例如 JavaScript 函式）。

FastAPI 也包含以下僅限 JavaScript 的 `presets` 設定：

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

這些是 JavaScript 物件，而不是字串，因此無法直接從 Python 程式碼傳遞。

若需要使用這類僅限 JavaScript 的設定，你可以使用上面介紹的方法：覆寫所有 Swagger UI 的路徑操作（path operation），並手動撰寫所需的 JavaScript。
