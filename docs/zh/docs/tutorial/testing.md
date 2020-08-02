# 测试

归因于 <a href="https://www.starlette.io/testclient/" class="external-link" target="_blank">Starlette</a>, 测试 **FastAPI** 应用变得简单而且愉快.

它基于 <a href="http://docs.python-requests.org" class="external-link" target="_blank">Requests</a>, 因此会让你感到非常的熟悉和简便.

有了它， 你可以把 <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a> 直接用于 **FastAPI**.

## 使用 `测试客户端`

导入 `TestClient`。

创建一个 `TestClient` 并传递给你的 **FastAPI**。

创建一个名称以 `test_` 开头的函数 (这是 `pytest` 的约定)。

`TestClient` 对象使用方式与`requests`相同。

使用标准的Python表达式编写assert断言来帮助你检查代码（类似于 `pytest`）。

```Python hl_lines="2  12  15 16 17 18"
{!../../../docs_src/app_testing/tutorial001.py!}
```

!!! tip
    注意测试函数是使用 `def`, 而不是 `async def`。

    并且调用客户端也不使用 `await`。

    这让你无障碍地直接使用 `pytest` 。

!!! note "Technical Details"
    你也可以使用 `from starlette.testclient import TestClient`。

    **FastAPI** 提供的`fastapi.testclient`和 `starlette.testclient` 相同，仅仅是为了开发方便. 但它直接来自于 Starlette。

## 分离测试

在实际的开发中, 你可以会让你的测试放在不同的文件中。

并且你的 **FastAPI** 程序可能由许多文件/模块组成。

### **FastAPI** 应用程序文件

假设你的**FastAPI** 应用程序有一个 `main.py` 文件:

```Python
{!../../../docs_src/app_testing/main.py!}
```

### 测试文件

然后你可以有一个 `test_main.py` 文件作为测试, 从 `main` 模块导入你的 `app`  (`main.py`):

```Python
{!../../../docs_src/app_testing/test_main.py!}
```

## 测试: 扩展示例

现在我们扩展这个示例并添加更多细节以查看如何测试不同的部分。

### 扩展 **FastAPI** 应用程序文件

假设你的**FastAPI** 应用程序有一个 `main_b.py` 文件:

它有一个能够返回错误信息的`GET`操作

它有一个能够返回一些错误信息的`POST`操作

这两个路径操作都需要一个`X-Token`请求头

```Python
{!../../../docs_src/app_testing/main_b.py!}
```

### 扩展测试文件

假设你的**FastAPI** 应用程序中有一个 `test_main_b.py` 文件:

```Python
{!../../../docs_src/app_testing/test_main_b.py!}
```

当你不知道如何在请求中使用客户端传递参数，均可以上网搜索`requests`的使用方式

然后，你可以以同样方式在你的测试中使用

例如：

* 要传递路径或查询参数，请将其添加到URL中。
* 要传递JSON正文，可使用Python`dict`对象将数据传递给json参数。
* 如果您需要发送表单数据而不是JSON，请改用data参数。
* 要传请求头，改用headers参数 。
* 对于*cookies*，改用cookies参数 。

关于更多如何将数据传递给后端 (使用 `requests` 或者 `TestClient`) 请参阅 <a href="http://docs.python-requests.org" class="external-link" target="_blank">Requests documentation</a>。

!!! info
    注意`TestClient`获取的数据可以转换成JSON,而不是Pydantic模型

    如果在你的测试中有一个 Pydantic 模型 并且你想要在测试中发送这个数据到应用程序, 你可以使用 `jsonable_encoder`  [JSON Compatible Encoder](encoder.md){.internal-link target=_blank}。

## 运行代码

你只需要安装 `pytest`:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

它将查找文件并自动执行它们进行测试，并将结果报告给您。

使用以下命令运行测试:

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
