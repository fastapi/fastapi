# 依赖文件的分类

在我们更深入了解 **依赖文件注入** 系统之前, 让我们先升级一下先前的例子。

## 来自于前一个例子的`dict`

在之前的例子里, 我们从依赖文件（“可依赖文件”）中得到了`dict`文件:

```Python hl_lines="9"
{!../../../docs_src/dependencies/tutorial001.py!}
```

但这次我们从*路径操作函数*的`commons`参数中得到了一个`dict`

而且我们知道编辑器无法为`dict`提供很多帮助(如完善), 因它们不知道它们的密钥与数据类型.

我们可以做的更好...

## 依赖文件的构成

目前你已经见识过了定义成函数的依赖文件.

但那并不是定义依赖文件的唯一方式 (即使这一定义方式十分普遍).

关键的要素是：依赖项应该是「可调用项」.

Python中的“**可调用项**”是所有Python可像函数一样调用的项

所有，如果你有一个项目`something` (那可能 _不是_ 一个函数) 然后你可以像这样“调用”（执行）它:

```Python
something()
```

or

```Python
something(some_argument, some_keyword_argument="foo")
```

那么这就是一个“可调用项”.

## 依赖项的分类

您也许会注意到当你创建一个Python实例时语法与调用函数相同.

举个例子:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

在这个例子里, `fluffy` is an instance of the class `Cat`.

And to create `fluffy`, you are "calling" `Cat`.

So, a Python class is also a **callable**.

Then, in **FastAPI**, you could use a Python class as a dependency.

What FastAPI actually checks is that it is a "callable" (function, class or anything else) and the parameters defined.

If you pass a "callable" as a dependency in **FastAPI**, it will analyze the parameters for that "callable", and process them in the same way as the parameters for a *path operation function*. Including sub-dependencies.

That also applies to callables with no parameters at all. The same as it would be for *path operation functions* with no parameters.

Then, we can change the dependency "dependable" `common_parameters` from above to the class `CommonQueryParams`:

```Python hl_lines="11-15"
{!../../../docs_src/dependencies/tutorial002.py!}
```

Pay attention to the `__init__` method used to create the instance of the class:

```Python hl_lines="12"
{!../../../docs_src/dependencies/tutorial002.py!}
```

...it has the same parameters as our previous `common_parameters`:

```Python hl_lines="8"
{!../../../docs_src/dependencies/tutorial001.py!}
```

Those parameters are what **FastAPI** will use to "solve" the dependency.

In both cases, it will have:

* an optional `q` query parameter.
* a `skip` query parameter, with a default of `0`.
* a `limit` query parameter, with a default of `100`.

In both cases the data will be converted, validated, documented on the OpenAPI schema, etc.

## Use it

Now you can declare your dependency using this class.

```Python hl_lines="19"
{!../../../docs_src/dependencies/tutorial002.py!}
```

**FastAPI** calls the `CommonQueryParams` class. This creates an "instance" of that class and the instance will be passed as the parameter `commons` to your function.

## Type annotation vs `Depends`

Notice how we write `CommonQueryParams` twice in the above code:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

The last `CommonQueryParams`, in:

```Python
... = Depends(CommonQueryParams)
```

...is what **FastAPI** will actually use to know what is the dependency.

From it is that FastAPI will extract the declared parameters and that is what FastAPI will actually call.

---

In this case, the first `CommonQueryParams`, in:

```Python
commons: CommonQueryParams ...
```

...doesn't have any special meaning for **FastAPI**. FastAPI won't use it for data conversion, validation, etc. (as it is using the `= Depends(CommonQueryParams)` for that).

You could actually write just:

```Python
commons = Depends(CommonQueryParams)
```

..as in:

```Python hl_lines="19"
{!../../../docs_src/dependencies/tutorial003.py!}
```

But declaring the type is encouraged as that way your editor will know what will be passed as the parameter `commons`, and then it can help you with code completion, type checks, etc:

<img src="/img/tutorial/dependencies/image02.png">

## Shortcut

But you see that we are having some code repetition here, writing `CommonQueryParams` twice:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

**FastAPI** provides a shortcut for these cases, in where the dependency is *specifically* a class that **FastAPI** will "call" to create an instance of the class itself.

For those specific cases, you can do the following:

Instead of writing:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

...you write:

```Python
commons: CommonQueryParams = Depends()
```

You declare the dependency as the type of the parameter, and you use `Depends()` as its "default" value (that after the `=`) for that function's parameter, without any parameter in `Depends()`, instead of having to write the full class *again* inside of `Depends(CommonQueryParams)`.

The same example would then look like:

```Python hl_lines="19"
{!../../../docs_src/dependencies/tutorial004.py!}
```

...and **FastAPI** will know what to do.

!!! tip
    If that seems more confusing than helpful, disregard it, you don't *need* it.

    It is just a shortcut. Because **FastAPI** cares about helping you minimize code repetition.
