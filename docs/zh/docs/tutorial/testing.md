# 测试

感谢 <a href="https://www.starlette.dev/testclient/" class="external-link" target="_blank">Starlette</a>，测试**FastAPI** 应用轻松又愉快。

它基于 <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>， 而HTTPX又是基于Requests设计的，所以很相似且易懂。

有了它，你可以直接与**FastAPI**一起使用 <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a>。

## 使用 `TestClient`

/// info | 信息

要使用 `TestClient`，先要安装 <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a>.

例：`pip install httpx`.

///

导入 `TestClient`.

通过传入你的**FastAPI**应用创建一个 `TestClient` 。

创建名字以 `test_` 开头的函数（这是标准的 `pytest` 约定）。

像使用 `httpx` 那样使用 `TestClient` 对象。

为你需要检查的地方用标准的Python表达式写个简单的 `assert` 语句（重申，标准的`pytest`）。

{* ../../docs_src/app_testing/tutorial001.py hl[2,12,15:18] *}

/// tip | 提示

注意测试函数是普通的 `def`，不是 `async def`。

还有client的调用也是普通的调用，不是用 `await`。

这让你可以直接使用 `pytest` 而不会遇到麻烦。

///

/// note | 技术细节

你也可以用 `from starlette.testclient import TestClient`。

**FastAPI** 提供了和 `starlette.testclient` 一样的 `fastapi.testclient`，只是为了方便开发者。但它直接来自Starlette。

///

/// tip | 提示

除了发送请求之外，如果你还想测试时在FastAPI应用中调用 `async` 函数（例如异步数据库函数）， 可以在高级教程中看下 [Async Tests](../advanced/async-tests.md){.internal-link target=_blank} 。

///

## 分离测试

在实际应用中，你可能会把你的测试放在另一个文件里。

您的**FastAPI**应用程序也可能由一些文件/模块组成等等。

### **FastAPI** app 文件

假设你有一个像 [更大的应用](bigger-applications.md){.internal-link target=_blank} 中所描述的文件结构:

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

在 `main.py` 文件中你有一个 **FastAPI** app:


{* ../../docs_src/app_testing/main.py *}

### 测试文件

然后你会有一个包含测试的文件 `test_main.py` 。app可以像Python包那样存在（一样是目录，但有个 `__init__.py` 文件）：

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

因为这文件在同一个包中，所以你可以通过相对导入从 `main` 模块（`main.py`）导入`app`对象：

{* ../../docs_src/app_testing/test_main.py hl[3] *}

...然后测试代码和之前一样的。

## 测试：扩展示例

现在让我们扩展这个例子，并添加更多细节，看下如何测试不同部分。

### 扩展后的 **FastAPI** app 文件

让我们继续之前的文件结构：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

假设现在包含**FastAPI** app的文件 `main.py`  有些其他**路径操作**。

有个 `GET` 操作会返回错误。

有个 `POST` 操作会返回一些错误。

所有*路径操作* 都需要一个`X-Token` 头。

//// tab | Python 3.10+

```Python
{!> ../../docs_src/app_testing/app_b_an_py310/main.py!}
```

////

//// tab | Python 3.9+

```Python
{!> ../../docs_src/app_testing/app_b_an_py39/main.py!}
```

////

//// tab | Python 3.8+

```Python
{!> ../../docs_src/app_testing/app_b_an/main.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | 提示

Prefer to use the `Annotated` version if possible.

///

```Python
{!> ../../docs_src/app_testing/app_b_py310/main.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | 提示

Prefer to use the `Annotated` version if possible.

///

```Python
{!> ../../docs_src/app_testing/app_b/main.py!}
```

////

### 扩展后的测试文件

然后您可以使用扩展后的测试更新`test_main.py`：

{* ../../docs_src/app_testing/app_b/test_main.py *}

每当你需要客户端在请求中传递信息，但你不知道如何传递时，你可以通过搜索（谷歌）如何用 `httpx`做，或者是用 `requests` 做，毕竟HTTPX的设计是基于Requests的设计的。

接着只需在测试中同样操作。

示例：

* 传一个*路径* 或*查询* 参数，添加到URL上。
* 传一个JSON体，传一个Python对象(例如一个`dict`)到参数 `json`。
* 如果你需要发送 *Form Data* 而不是 JSON，使用 `data` 参数。
* 要发送 *headers*，传 `dict` 给 `headers` 参数。
* 对于 *cookies*，传 `dict` 给 `cookies` 参数。

关于如何传数据给后端的更多信息 (使用`httpx` 或 `TestClient`)，请查阅 <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX 文档</a>.

/// info | 信息

注意 `TestClient` 接收可以被转化为JSON的数据，而不是Pydantic模型。

如果你在测试中有一个Pydantic模型，并且你想在测试时发送它的数据给应用，你可以使用在[JSON Compatible Encoder](encoder.md){.internal-link target=_blank}介绍的`jsonable_encoder` 。

///

## 运行起来

之后，你只需要安装 `pytest`:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

他会自动检测文件和测试，执行测试，然后向你报告结果。

执行测试：

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
