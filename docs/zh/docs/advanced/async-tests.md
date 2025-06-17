# 异步测试

您已经了解了如何使用 `TestClient` 测试 **FastAPI** 应用程序。但是到目前为止，您只了解了如何编写同步测试，而没有使用 `async` 异步函数。

在测试中能够使用异步函数可能会很有用，比如当您需要异步查询数据库的时候。想象一下，您想要测试向 FastAPI 应用程序发送请求，然后验证您的后端是否成功在数据库中写入了正确的数据，与此同时您使用了异步的数据库的库。

让我们看看如何才能实现这一点。

## pytest.mark.anyio

如果我们想在测试中调用异步函数，那么我们的测试函数必须是异步的。 AnyIO 为此提供了一个简洁的插件，它允许我们指定一些测试函数要异步调用。

## HTTPX

即使您的 **FastAPI** 应用程序使用普通的 `def` 函数而不是 `async def` ，它本质上仍是一个 `async` 异步应用程序。

`TestClient` 在内部通过一些“魔法”操作，使得您可以在普通的 `def` 测试函数中调用异步的 FastAPI 应用程序，并使用标准的 pytest。但当我们在异步函数中使用它时，这种“魔法”就不再生效了。由于测试以异步方式运行，我们无法在测试函数中继续使用 `TestClient`。

`TestClient` 是基于 <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> 的。幸运的是，我们可以直接使用它来测试API。

## 示例

举个简单的例子，让我们来看一个[更大的应用](../tutorial/bigger-applications.md){.internal-link target=_blank}和[测试](../tutorial/testing.md){.internal-link target=_blank}中描述的类似文件结构：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

文件 `main.py` 将包含:

{* ../../docs_src/async_tests/main.py *}

文件 `test_main.py` 将包含针对 `main.py` 的测试，现在它可能看起来如下：

{* ../../docs_src/async_tests/test_main.py *}

## 运行测试

您可以通过以下方式照常运行测试：

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## 详细说明

这个标记 `@pytest.mark.anyio` 会告诉 pytest 该测试函数应该被异步调用：

{* ../../docs_src/async_tests/test_main.py hl[7] *}

/// tip

请注意，测试函数现在用的是 `async def`，而不是像以前使用 `TestClient` 时那样只是 `def` 。

///

我们现在可以使用应用程序创建一个 `AsyncClient` ，并使用 `await` 向其发送异步请求。

{* ../../docs_src/async_tests/test_main.py hl[9:12] *}

这相当于：

```Python
response = client.get('/')
```

我们曾经通过它向 `TestClient` 发出请求。

/// tip

请注意，我们正在将 async/await 与新的 `AsyncClient` 一起使用——请求是异步的。

///

/// warning

如果您的应用程序依赖于生命周期事件， `AsyncClient` 将不会触发这些事件。为了确保它们被触发，请使用 <a href="https://github.com/florimondmanca/asgi-lifespan#usage" class="external-link" target="_blank">florimondmanca/asgi-lifespan</a> 中的 `LifespanManager` 。

///

## 其他异步函数调用

由于测试函数现在是异步的，因此除了在测试中向 FastAPI 应用程序发送请求之外，您现在还可以调用（和使用 `await` 等待）其他 `async` 异步函数，就和您在代码中的其他任何地方调用它们的方法一样。

/// tip

如果您在测试程序中集成异步函数调用的时候遇到一个 `RuntimeError: Task attached to a different loop` 的报错（例如，使用 <a href="https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop" class="external-link" target="_blank">MongoDB 的 MotorClient</a> 时），请记住，只能在异步函数中实例化需要事件循环的对象，例如通过 `'@app.on_event("startup")` 回调函数进行初始化。

///
