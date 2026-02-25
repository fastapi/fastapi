# 非同步測試 { #async-tests }

你已經看過如何使用提供的 `TestClient` 來測試你的 FastAPI 應用。到目前為止，你只看到如何撰寫同步測試，沒有使用 `async` 函式。

在測試中能使用非同步函式會很有用，例如當你以非同步方式查詢資料庫時。想像你想測試發送請求到 FastAPI 應用，然後在使用非同步資料庫函式庫時，驗證後端是否成功把正確資料寫入資料庫。

來看看怎麼做。

## pytest.mark.anyio { #pytest-mark-anyio }

若要在測試中呼叫非同步函式，測試函式本身也必須是非同步的。AnyIO 為此提供了一個好用的外掛，讓我們可以標示某些測試函式以非同步方式執行。

## HTTPX { #httpx }

即使你的 FastAPI 應用使用一般的 `def` 函式而非 `async def`，它在底層仍然是個 `async` 應用。

`TestClient` 在內部做了一些魔法，讓我們能在一般的 `def` 測試函式中，使用標準 pytest 來呼叫非同步的 FastAPI 應用。但當我們在非同步函式中使用它時，這個魔法就不再奏效了。也就是說，當以非同步方式執行測試時，就不能在測試函式內使用 `TestClient`。

`TestClient` 是建立在 <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> 之上，所幸我們可以直接使用它來測試 API。

## 範例 { #example }

作為簡單範例，讓我們考慮與[更大型的應用](../tutorial/bigger-applications.md){.internal-link target=_blank}與[測試](../tutorial/testing.md){.internal-link target=_blank}中描述的類似檔案結構：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

檔案 `main.py` 會是：

{* ../../docs_src/async_tests/app_a_py310/main.py *}

檔案 `test_main.py` 會包含針對 `main.py` 的測試，現在可能像這樣：

{* ../../docs_src/async_tests/app_a_py310/test_main.py *}

## 執行 { #run-it }

如常執行測試：

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## 詳解 { #in-detail }

標記 `@pytest.mark.anyio` 告訴 pytest 這個測試函式應以非同步方式執行：

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[7] *}

/// tip

注意，測試函式現在是 `async def`，而不是像使用 `TestClient` 時那樣僅用 `def`。

///

接著，我們可以用該應用建立 `AsyncClient`，並以 `await` 發送非同步請求。

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[9:12] *}

這等同於：

```Python
response = client.get('/')
```

也就是先前用 `TestClient` 發送請求時所用的寫法。

/// tip

注意，對新的 `AsyncClient` 需搭配 async/await —— 請求是非同步的。

///

/// warning

如果你的應用仰賴 lifespan 事件，`AsyncClient` 不會觸發這些事件。若要確保它們被觸發，請使用 <a href="https://github.com/florimondmanca/asgi-lifespan#usage" class="external-link" target="_blank">florimondmanca/asgi-lifespan</a> 的 `LifespanManager`。

///

## 其他非同步函式呼叫 { #other-asynchronous-function-calls }

由於測試函式現在是非同步的，你也可以在測試中呼叫（並 `await`）其他 `async` 函式，和在程式碼其他地方一樣。

/// tip

如果在將非同步呼叫整合進測試時遇到 `RuntimeError: Task attached to a different loop`（例如使用 <a href="https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop" class="external-link" target="_blank">MongoDB 的 MotorClient</a> 時），請記得：需要事件迴圈的物件只應在非同步函式內實例化，例如在 `@app.on_event("startup")` 回呼中。

///
