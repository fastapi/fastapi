# 测试

借助 <a href="https://www.starlette.io/testclient/" class="external-link" target="_blank">Starlette</a>，测试 **FastAPI** 应用这件事变得简单又愉悦。

因为 Starlette 基于 <a href="https://requests.readthedocs.io" class="external-link" target="_blank">Requests</a>，所以测试操作也是非常熟悉和直观。

借助 Starlette，还可以直接使用 <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a> 测试 **FastAPI** 应用。

## 使用 `TestClient`

导入 `TestClient`。

创建 `TestClient`，并把它传递给 **FastAPI**。

创建以 `test_` 开头的函数，这是 `pytest` 的标准惯例。

使用 `TestClient` 对象的方式与执行 `requests` 的方式一样。

使用 python 标准表达式编写简单的，用于校验的 `assert` 语句，这也是 `pytest` 的标准惯例。

```Python hl_lines="2  12  15-18"
{!../../../docs_src/app_testing/tutorial001.py!}
```

!!! tip "提示"

    注意，测试函数是普通函数（`def`），不是异步函数（`async def`）。
    
    并且，对 `client` 也要使用普通调用，不要使用 `await`。
    
    这样，直接使用 `pytest` 就不会变得复杂。

!!! note "技术细节"

    您也可以使用 `from starlette.testclient import TestClient`。
    
    **FastAPI** 的 `fastapi.testclient` 与 `starlette.testclient` 一样，只是为了方便开发者调用，但其实它直接继承自 Starlette。

!!! tip "提示"

    除了使用异步函数向 FastAPI 应用发送请求外（例如，异步数据库函数），如果想在测试中使用 `async` 异步函数，请参阅高级用户指南中的[异步测试](../advanced/async-tests.md){.internal-link target=_blank}。

## 分拆测试

实际应用中，测试会分为多个不同文件。

而且，**FastAPI** 应用可能也是由多个文件/模块组成的。

### **FastAPI** 的 app 文件

假设 **FastAPI** 应用中包含 `app ` 的  `main.py` 如下所示：

```Python
{!../../../docs_src/app_testing/main.py!}
```

### 测试文件

然后，创建测试文件 `test_main.py`，并从 `main` 模块（`mian.py`）中导入 `app`：

```Python
{!../../../docs_src/app_testing/test_main.py!}
```

## 测试：扩展示例

接下来，扩展上述示例，添加更多细节，以介绍如何测试不同组件。

### 扩展 **FastAPI** app 文件

假设 **FastAPI** 应用中包含 `app ` 的  `main_b.py` 如下所示：

此应用的 `GET` 操作会返回错误。

`POST` 操作会返回多个错误。

两个**路径操作**都需要 `X-Token` 请求头。

```Python
{!../../../docs_src/app_testing/main_b.py!}
```

### 扩展测试文件

同上，测试文件 `test_main_b.py`也添加了扩展测试：

```Python
{!../../../docs_src/app_testing/test_main_b.py!}
```



在客户端的请求中传递信息，如果您不知道怎么操作，请（在谷歌）搜索如何在 `requests` 中执行这一操作。

接下来执行同样的测试操作。

例如：

* 传递*路径或查询*参数，把它添加至 URL
* 传递 JSON 请求体时，需要把 `dict` 等 Python 对象传递给参数 `json`
* 如果发送的是*表单数据*，不是 JSON，则要使用参数 `data`
* 传递*请求头*时，在参数 `headers` 中使用 `dict`
* 传递 `cookies` 时，在参数 `cookies` 中使用 `dict`

关于如何（使用 `request` 或 `TestClient`）把数据传递给后端的说明，详见 <a href="https://requests.readthedocs.io" class="external-link" target="_blank">Requests 文档</a>。

!!! info "说明"

    注意，`TestClient` 接收的是可以转换为 JSON 的数据，不是 Pydantic 模型。
    
    如果在测试中使用 Pydantic 模型，并希望在测试中把模型的数据发送给 FastAPI 应用，可以使用 [JSON 编码器](encoder.md){.internal-link target=_blank} 中的 `jsonable_encoder`。

## 运行测试

接下来，安装 `pytest`：

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

`pytest` 会自动检测文件，并进行测试。执行测试文件，生成测试报告。

运行测试：

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

