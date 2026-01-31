# 异步测试 { #async-tests }

你已经了解了如何使用提供的 `TestClient` 测试你的 **FastAPI** 应用程序。到目前为止，你只了解了如何编写同步测试，而没有使用 `async` 函数。

在测试中能够使用异步函数可能会很有用，比如当你需要异步查询数据库的时候。想象一下，你想要测试向 FastAPI 应用程序发送请求，然后验证你的后端是否成功在数据库中写入了正确的数据，同时你使用了一个异步数据库库。

让我们看看如何才能实现这一点。

## pytest.mark.anyio { #pytest-mark-anyio }

如果我们想在测试中调用异步函数，那么我们的测试函数必须是异步的。AnyIO 为此提供了一个简洁的插件，它允许我们指定某些测试函数要以异步方式调用。

## HTTPX { #httpx }

即使你的 **FastAPI** 应用程序使用普通的 `def` 函数而不是 `async def`，它在底层仍然是一个 `async` 应用程序。

`TestClient` 在内部通过一些“魔法”操作，使得你可以在普通的 `def` 测试函数中调用异步的 FastAPI 应用程序，并使用标准的 pytest。但当我们在异步函数中使用它时，这种“魔法”就不再生效了。由于测试以异步方式运行，我们无法在测试函数中继续使用 `TestClient`。

`TestClient` 基于 <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>，幸运的是，我们可以直接使用它来测试 API。

## 示例 { #example }

举个简单的例子，让我们来看一个与 [更大的应用](../tutorial/bigger-applications.md){.internal-link target=_blank} 和 [测试](../tutorial/testing.md){.internal-link target=_blank} 中描述的类似文件结构：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

文件 `main.py` 将包含：

{* ../../docs_src/async_tests/app_a_py39/main.py *}

文件 `test_main.py` 将包含针对 `main.py` 的测试，现在它可能看起来如下：

{* ../../docs_src/async_tests/app_a_py39/test_main.py *}

## 运行 { #run-it }

你可以通过以下方式照常运行测试：

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## 详细说明 { #in-detail }

这个标记 `@pytest.mark.anyio` 会告诉 pytest 该测试函数应该被异步调用：

{* ../../docs_src/async_tests/app_a_py39/test_main.py hl[7] *}

/// tip | 提示

请注意，测试函数现在用的是 `async def`，而不是像以前使用 `TestClient` 时那样只是 `def`。

///

然后我们可以使用应用程序创建一个 `AsyncClient`，并使用 `await` 向其发送异步请求。

{* ../../docs_src/async_tests/app_a_py39/test_main.py hl[9:12] *}

这相当于：

```Python
response = client.get('/')
```

...我们过去使用 `TestClient` 发出请求时用的方式。

/// tip | 提示

请注意，我们正在将 async/await 与新的 `AsyncClient` 一起使用——请求是异步的。

///

/// warning | 警告

如果你的应用程序依赖于 lifespan 事件，`AsyncClient` 将不会触发这些事件。为了确保它们被触发，请使用 <a href="https://github.com/florimondmanca/asgi-lifespan#usage" class="external-link" target="_blank">florimondmanca/asgi-lifespan</a> 中的 `LifespanManager`。

///

## 其他异步函数调用 { #other-asynchronous-function-calls }

由于测试函数现在是异步的，因此除了在测试中向 FastAPI 应用程序发送请求之外，你现在还可以调用（并 `await`）其他 `async` 函数，就和你在代码中的其他任何地方调用它们的方法一样。

/// tip | 提示

如果你在测试中集成异步函数调用的时候遇到 `RuntimeError: Task attached to a different loop`（例如，使用 <a href="https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop" class="external-link" target="_blank">MongoDB's MotorClient</a> 时），请记住，只能在异步函数中实例化需要事件循环的对象，例如在 `@app.on_event("startup")` 回调函数中实例化。

///
