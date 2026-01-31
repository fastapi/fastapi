# 测试 { #testing }

感谢 <a href="https://www.starlette.dev/testclient/" class="external-link" target="_blank">Starlette</a>，测试 **FastAPI** 应用轻松又愉快。

它基于 <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>，而 HTTPX 又是基于 Requests 设计的，所以非常熟悉且直观。

有了它，你可以直接与 **FastAPI** 一起使用 <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a>。

## 使用 `TestClient` { #using-testclient }

/// info | 信息

要使用 `TestClient`，先安装 <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a>。

请确保你创建一个[虚拟环境](../virtual-environments.md){.internal-link target=_blank}，激活它，然后再安装，例如：

```console
$ pip install httpx
```

///

导入 `TestClient`。

通过传入你的 **FastAPI** 应用来创建一个 `TestClient`。

创建名字以 `test_` 开头的函数（这是标准的 `pytest` 约定）。

像使用 `httpx` 那样使用 `TestClient` 对象。

用你需要检查的标准 Python 表达式写简单的 `assert` 语句（同样是标准的 `pytest`）。

{* ../../docs_src/app_testing/tutorial001_py39.py hl[2,12,15:18] *}

/// tip | 提示

注意测试函数是普通的 `def`，不是 `async def`。

还有对 client 的调用也是普通调用，不需要使用 `await`。

这让你可以直接使用 `pytest` 而不会遇到麻烦。

///

/// note | 技术细节

你也可以用 `from starlette.testclient import TestClient`。

**FastAPI** 提供了与 `starlette.testclient` 相同的 `fastapi.testclient`，只是为了方便你（开发者）。但它直接来自 Starlette。

///

/// tip | 提示

如果你除了向 FastAPI 应用发送请求之外，还想在测试中调用 `async` 函数（例如异步数据库函数），请查看高级教程中的 [Async Tests](../advanced/async-tests.md){.internal-link target=_blank}。

///

## 分离测试 { #separating-tests }

在实际应用中，你可能会把测试放在另一个文件里。

并且你的 **FastAPI** 应用也可能由多个文件/模块等组成。

### **FastAPI** app 文件 { #fastapi-app-file }

假设你有一个如 [更大的应用](bigger-applications.md){.internal-link target=_blank} 中所描述的文件结构：

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

在 `main.py` 文件中你有你的 **FastAPI** app：


{* ../../docs_src/app_testing/app_a_py39/main.py *}

### 测试文件 { #testing-file }

然后你可以有一个包含测试的文件 `test_main.py`。它可以放在同一个 Python 包中（同一个带 `__init__.py` 文件的目录）：

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

因为该文件在同一个包中，你可以使用相对导入，从 `main` 模块（`main.py`）导入对象 `app`：

{* ../../docs_src/app_testing/app_a_py39/test_main.py hl[3] *}


...然后像之前一样编写测试代码。

## 测试：扩展示例 { #testing-extended-example }

现在让我们扩展这个示例，并添加更多细节，看看如何测试不同部分。

### 扩展后的 **FastAPI** app 文件 { #extended-fastapi-app-file }

让我们继续使用之前相同的文件结构：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

假设现在包含你的 **FastAPI** app 的文件 `main.py` 有一些其他的 **路径操作**。

它有一个可能返回错误的 `GET` 操作。

它有一个可能返回多个错误的 `POST` 操作。

两个 *路径操作* 都需要一个 `X-Token` header。

{* ../../docs_src/app_testing/app_b_an_py310/main.py *}

### 扩展后的测试文件 { #extended-testing-file }

然后你可以用扩展后的测试更新 `test_main.py`：

{* ../../docs_src/app_testing/app_b_an_py310/test_main.py *}


每当你需要 client 在请求中传递信息但你不知道怎么做时，你可以搜索（Google）如何在 `httpx` 里做，甚至如何用 `requests` 做，因为 HTTPX 的设计基于 Requests 的设计。

然后你只需要在测试中做同样的事情。

例如：

* 要传一个 *path* 或 *query* 参数，把它加到 URL 上。
* 要传一个 JSON body，把一个 Python 对象（例如 `dict`）传给参数 `json`。
* 如果你需要发送 *Form Data* 而不是 JSON，改用 `data` 参数。
* 要传 *headers*，在 `headers` 参数中使用一个 `dict`。
* 对于 *cookies*，在 `cookies` 参数中使用一个 `dict`。

关于如何向后端传递数据（使用 `httpx` 或 `TestClient`）的更多信息，请查阅 <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX documentation</a>。

/// info | 信息

注意 `TestClient` 接收的是可以被转换为 JSON 的数据，而不是 Pydantic 模型。

如果你在测试中有一个 Pydantic 模型，并且你想在测试期间把它的数据发送给应用，你可以使用在 [JSON Compatible Encoder](encoder.md){.internal-link target=_blank} 中描述的 `jsonable_encoder`。

///

## 运行 { #run-it }

之后，你只需要安装 `pytest`。

请确保你创建一个[虚拟环境](../virtual-environments.md){.internal-link target=_blank}，激活它，然后再安装，例如：

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

它会自动检测文件和测试，执行它们，并将结果报告给你。

用下面命令运行测试：

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
