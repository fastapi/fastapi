# 測試 { #testing }

多虧了 <a href="https://www.starlette.dev/testclient/" class="external-link" target="_blank">Starlette</a>，測試 **FastAPI** 應用既簡單又好用。

它是基於 <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> 打造，而 HTTPX 的設計又參考了 Requests，所以用起來非常熟悉、直覺。

借助它，你可以直接用 <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a> 來測試 **FastAPI**。

## 使用 `TestClient` { #using-testclient }

/// info

要使用 `TestClient`，請先安裝 <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a>。

請先建立並啟用一個[虛擬環境](../virtual-environments.md){.internal-link target=_blank}，然後安裝，例如：

```console
$ pip install httpx
```

///

匯入 `TestClient`。

建立一個 `TestClient`，把你的 **FastAPI** 應用傳入其中。

建立名稱以 `test_` 開頭的函式（這是 `pytest` 的慣例）。

像使用 `httpx` 一樣使用 `TestClient` 物件。

用簡單的 `assert` 敘述搭配標準的 Python 運算式來檢查（同樣是 `pytest` 的標準用法）。

{* ../../docs_src/app_testing/tutorial001_py310.py hl[2,12,15:18] *}

/// tip

注意測試函式是一般的 `def`，不是 `async def`。

而且對 client 的呼叫也都是一般呼叫，不需要使用 `await`。

這讓你可以直接使用 `pytest`，不必費心處理非同步。

///

/// note | 技術細節

你也可以使用 `from starlette.testclient import TestClient`。

**FastAPI** 為了方便開發者，也提供與 `starlette.testclient` 相同的 `fastapi.testclient`。但它其實直接來自 Starlette。

///

/// tip

如果你想在測試中呼叫其他 `async` 函式，而不只是對 FastAPI 應用發送請求（例如非同步的資料庫函式），請參考進階教學中的[非同步測試](../advanced/async-tests.md){.internal-link target=_blank}。

///

## 分離測試 { #separating-tests }

在真實專案中，你大概會把測試放在不同的檔案中。

你的 **FastAPI** 應用也可能由多個檔案/模組組成，等等。

### **FastAPI** 應用檔案 { #fastapi-app-file }

假設你的檔案結構如[更大型的應用](bigger-applications.md){.internal-link target=_blank}所述：

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

在 `main.py` 檔案中有你的 **FastAPI** 應用：


{* ../../docs_src/app_testing/app_a_py310/main.py *}

### 測試檔案 { #testing-file }

然後你可以建立一個 `test_main.py` 放你的測試。它可以與應用位於同一個 Python 套件（同一個包含 `__init__.py` 的目錄）：

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

因為這個檔案在同一個套件中，你可以使用相對匯入，從 `main` 模組（`main.py`）匯入 `app` 這個物件：

{* ../../docs_src/app_testing/app_a_py310/test_main.py hl[3] *}


...然後測試的程式碼就和先前一樣。

## 測試：進階範例 { #testing-extended-example }

現在我們延伸這個範例並加入更多細節，看看如何測試不同部分。

### 擴充的 **FastAPI** 應用檔案 { #extended-fastapi-app-file }

沿用先前相同的檔案結構：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

假設現在你的 **FastAPI** 應用所在的 `main.py` 有一些其他的路徑操作（path operations）。

它有一個可能回傳錯誤的 `GET` 操作。

它有一個可能回傳多種錯誤的 `POST` 操作。

兩個路徑操作都需要一個 `X-Token` 標頭（header）。

{* ../../docs_src/app_testing/app_b_an_py310/main.py *}

### 擴充的測試檔案 { #extended-testing-file }

接著你可以把 `test_main.py` 更新為擴充後的測試：

{* ../../docs_src/app_testing/app_b_an_py310/test_main.py *}


每當你需要在請求中讓 client 帶一些資料，但不確定該怎麼做時，你可以搜尋（Google）在 `httpx` 要如何傳遞，甚至用 Requests 怎麼做，因為 HTTPX 的設計是基於 Requests。

然後在你的測試中做一樣的事即可。

例如：

* 要傳遞路徑或查詢參數，直接把它加在 URL 上。
* 要傳遞 JSON 本文，將 Python 物件（例如 `dict`）傳給 `json` 參數。
* 如果需要送出表單資料（Form Data）而不是 JSON，改用 `data` 參數。
* 要傳遞標頭（headers），在 `headers` 參數中放一個 `dict`。
* 對於 Cookie（cookies），在 `cookies` 參數中放一個 `dict`。

關於如何把資料傳給後端（使用 `httpx` 或 `TestClient`），更多資訊請參考 <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX 文件</a>。

/// info

請注意，`TestClient` 接收的是可轉為 JSON 的資料，而不是 Pydantic models。

如果你的測試裡有一個 Pydantic model，並想在測試時把它的資料送給應用，你可以使用[JSON 相容編碼器](encoder.md){.internal-link target=_blank}中介紹的 `jsonable_encoder`。

///

## 執行 { #run-it }

接下來，你只需要安裝 `pytest`。

請先建立並啟用一個[虛擬環境](../virtual-environments.md){.internal-link target=_blank}，然後安裝，例如：

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

它會自動偵測檔案與測試、執行它們，並把結果回報給你。

用以下指令執行測試：

<div class="termy">

```console
$ pytest

================ test session starts ================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/user/code/superawesome-cli/app
plugins: forked-1.1.3, xdist-1.31.0, cov-2.8.1
collected 6 items

---> 100%

test_main.py <span style="color: green; white-space: pre;">......                            [100%]</span>

<span style="color: green;">================= 1 passed in 0.03s =================</span>
```

</div>
