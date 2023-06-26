# 类作为依赖项

在深入探究 **依赖注入** 系统之前，让我们升级之前的例子。

## 来自前一个例子的`dict`

在前面的例子中, 我们从依赖项 ("可依赖对象") 中返回了一个 `dict`:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/dependencies/tutorial001_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/dependencies/tutorial001.py!}
    ```

但是后面我们在路径操作函数的参数 `commons` 中得到了一个 `dict`。

我们知道编辑器不能为 `dict` 提供很多支持(比如补全)，因为编辑器不知道 `dict` 的键和值类型。

对此，我们可以做的更好...

## 什么构成了依赖项？

到目前为止，您看到的依赖项都被声明为函数。

但这并不是声明依赖项的唯一方法(尽管它可能是更常见的方法)。

关键因素是依赖项应该是 "可调用对象"。

Python 中的 "**可调用对象**" 是指任何 Python 可以像函数一样 "调用" 的对象。

所以，如果你有一个对象 `something` (可能*不是*一个函数)，你可以 "调用" 它(执行它)，就像：

```Python
something()
```

或者

```Python
something(some_argument, some_keyword_argument="foo")
```

这就是 "可调用对象"。

## 类作为依赖项

您可能会注意到，要创建一个 Python 类的实例，您可以使用相同的语法。

举个例子:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

在这个例子中, `fluffy` 是一个 `Cat` 类的实例。

为了创建 `fluffy`，你调用了 `Cat` 。

所以，Python 类也是 **可调用对象**。

因此，在 **FastAPI** 中，你可以使用一个 Python 类作为一个依赖项。

实际上 FastAPI 检查的是它是一个 "可调用对象"（函数，类或其他任何类型）以及定义的参数。

如果您在 **FastAPI** 中传递一个 "可调用对象" 作为依赖项，它将分析该 "可调用对象" 的参数，并以处理路径操作函数的参数的方式来处理它们。包括子依赖项。

这也适用于完全没有参数的可调用对象。这与不带参数的路径操作函数一样。

所以，我们可以将上面的依赖项 "可依赖对象" `common_parameters` 更改为类 `CommonQueryParams`:

=== "Python 3.10+"

    ```Python hl_lines="9-13"
    {!> ../../../docs_src/dependencies/tutorial002_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="11-15"
    {!> ../../../docs_src/dependencies/tutorial002.py!}
    ```

注意用于创建类实例的 `__init__` 方法：

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/dependencies/tutorial002_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="12"
    {!> ../../../docs_src/dependencies/tutorial002.py!}
    ```

...它与我们以前的 `common_parameters` 具有相同的参数：

=== "Python 3.10+"

    ```Python hl_lines="6"
    {!> ../../../docs_src/dependencies/tutorial001_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/dependencies/tutorial001.py!}
    ```

这些参数就是 **FastAPI** 用来 "处理" 依赖项的。

在两个例子下，都有：

* 一个可选的 `q` 查询参数，是 `str` 类型。
* 一个 `skip` 查询参数，是 `int` 类型，默认值为 `0`。
* 一个 `limit` 查询参数，是 `int` 类型，默认值为 `100`。

在两个例子下，数据都将被转换、验证、在 OpenAPI schema 上文档化，等等。

## 使用它

现在，您可以使用这个类来声明你的依赖项了。

=== "Python 3.10+"

    ```Python hl_lines="17"
    {!> ../../../docs_src/dependencies/tutorial002_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/dependencies/tutorial002.py!}
    ```

**FastAPI** 调用 `CommonQueryParams` 类。这将创建该类的一个 "实例"，该实例将作为参数 `commons` 被传递给你的函数。

## 类型注解 vs `Depends`

注意，我们在上面的代码中编写了两次`CommonQueryParams`：

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

最后的 `CommonQueryParams`:

```Python
... = Depends(CommonQueryParams)
```

...实际上是 **Fastapi** 用来知道依赖项是什么的。

FastAPI 将从依赖项中提取声明的参数，这才是 FastAPI 实际调用的。

---

在本例中，第一个 `CommonQueryParams` ：

```Python
commons: CommonQueryParams ...
```

...对于 **FastAPI** 没有任何特殊的意义。FastAPI 不会使用它进行数据转换、验证等 (因为对于这，它使用 `= Depends(CommonQueryParams)`)。

你实际上可以只这样编写:

```Python
commons = Depends(CommonQueryParams)
```

..就像:

=== "Python 3.10+"

    ```Python hl_lines="17"
    {!> ../../../docs_src/dependencies/tutorial003_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/dependencies/tutorial003.py!}
    ```

但是声明类型是被鼓励的，因为那样你的编辑器就会知道将传递什么作为参数 `commons` ，然后它可以帮助你完成代码，类型检查，等等：

<img src="/img/tutorial/dependencies/image02.png">

## 快捷方式

但是您可以看到，我们在这里有一些代码重复了，编写了`CommonQueryParams`两次：

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

**FastAPI** 为这些情况提供了一个快捷方式，在这些情况下，依赖项 *明确地* 是一个类，**FastAPI** 将 "调用" 它来创建类本身的一个实例。

对于这些特定的情况，您可以跟随以下操作：

不是写成这样：

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

...而是这样写:

```Python
commons: CommonQueryParams = Depends()
```

您声明依赖项作为参数的类型，并使用 `Depends()` 作为该函数的参数的 "默认" 值(在 `=` 之后)，而在 `Depends()` 中没有任何参数，而不是在 `Depends(CommonQueryParams)` 编写完整的类。

同样的例子看起来像这样：

=== "Python 3.10+"

    ```Python hl_lines="17"
    {!> ../../../docs_src/dependencies/tutorial004_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/dependencies/tutorial004.py!}
    ```

... **FastAPI** 会知道怎么处理。

!!! tip
    如果这看起来更加混乱而不是更加有帮助，那么请忽略它，你不*需要*它。

    这只是一个快捷方式。因为 **FastAPI** 关心的是帮助您减少代码重复。
