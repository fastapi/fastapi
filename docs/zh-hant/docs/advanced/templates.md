# 模板 { #templates }

你可以在 **FastAPI** 中使用任意你想要的模板引擎。

常見的選擇是 Jinja2，與 Flask 與其他工具所使用的一樣。

有一些工具可讓你輕鬆設定，並可直接在你的 **FastAPI** 應用程式中使用（由 Starlette 提供）。

## 安裝相依套件 { #install-dependencies }

請先建立一個[虛擬環境](../virtual-environments.md){.internal-link target=_blank}、啟用它，然後安裝 `jinja2`：

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## 使用 `Jinja2Templates` { #using-jinja2templates }

- 匯入 `Jinja2Templates`。
- 建立一個可重複使用的 `templates` 物件。
- 在會回傳模板的「*路徑操作（path operation）*」中宣告一個 `Request` 參數。
- 使用你建立的 `templates` 來渲染並回傳 `TemplateResponse`，傳入模板名稱、`request` 物件，以及在 Jinja2 模板中使用的「context」鍵值對字典。

{* ../../docs_src/templates/tutorial001_py310.py hl[4,11,15:18] *}

/// note

在 FastAPI 0.108.0、Starlette 0.29.0 之前，`name` 是第一個參數。

此外，在更早的版本中，`request` 物件是作為 context 的鍵值對之一傳給 Jinja2 的。

///

/// tip

透過宣告 `response_class=HTMLResponse`，文件 UI 能夠知道回應將會是 HTML。

///

/// note | 技術細節

你也可以使用 `from starlette.templating import Jinja2Templates`。

**FastAPI** 以 `fastapi.templating` 的形式提供與 `starlette.templating` 相同的內容，僅為了方便你（開發者）。但大多數可用的回應類別都直接來自 Starlette，`Request` 與 `StaticFiles` 也是如此。

///

## 撰寫模板 { #writing-templates }

接著你可以在 `templates/item.html` 編寫模板，例如：

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### 模板 context 值 { #template-context-values }

在包含以下內容的 HTML 中：

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...它會顯示你在傳入的 context `dict` 中提供的 `id`：

```Python
{"id": id}
```

例如，若 ID 為 `42`，會渲染為：

```html
Item ID: 42
```

### 模板 `url_for` 參數 { #template-url-for-arguments }

你也可以在模板中使用 `url_for()`，它所接受的參數與你的「*路徑操作函式（path operation function）*」所使用的參數相同。

因此，包含以下內容的區塊：

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...會產生指向與「*路徑操作函式*」`read_item(id=id)` 相同 URL 的連結。

例如，若 ID 為 `42`，會渲染為：

```html
<a href="/items/42">
```

## 模板與靜態檔案 { #templates-and-static-files }

你也可以在模板中使用 `url_for()`，例如搭配你以 `name="static"` 掛載的 `StaticFiles` 使用。

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

在這個例子中，它會連結到 `static/styles.css` 的 CSS 檔案，內容為：

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

而且因為你使用了 `StaticFiles`，該 CSS 檔案會由你的 **FastAPI** 應用程式在 URL `/static/styles.css` 自動提供。

## 更多細節 { #more-details }

想了解更多細節（包含如何測試模板），請參考 <a href="https://www.starlette.dev/templates/" class="external-link" target="_blank">Starlette 的模板說明文件</a>。
