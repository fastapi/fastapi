# 作为依赖项的类

在深入研究 **依赖项注入** 系统之前，让我们先升级前面的示例。

## 前面示例中的 `dict`

在前面的例子中，我们从依赖项 ("可依赖项") 中返回一个 `dict` ：

```Python hl_lines="9"
{!../../../docs_src/dependencies/tutorial001.py!}
```

之后我们在 *路径操作函数* 的参数 `commons` 中得到一个 `dict` 。

我们知道编辑器不能为 `dict` 提供很多支持(比如补全)，因为它们不能知道它们的键和值类型。

我们可以做得更好……

## 什么可以是依赖项

到目前为止，您已经看到过将依赖项声明为函数的情况。

但这并不是声明依赖关系的唯一方法(尽管它可能是更常见的方法)。

关键因素是依赖项应该是 "可调用的" 。

Python中的 "**可调用的**" 是Python可以像函数一样 "调用" 的任何东西。

所以，如果你有一个对象 `something` (那可能_不_是一个函数)，你可以 "调用" 它 (执行它) 像:

```Python
something()
```

或

```Python
something(some_argument, some_keyword_argument="foo")
```

那么它就是一个"可调用的"。

## 类作为依赖项

您可能会注意到，要创建Python类的实例，需要使用相同的语法。

例如:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

在这种情况下，`fluffy` 是类 `Cat` 的一个实例。

而要创建 `fluffy`，你需要 "调用" `Cat` 。

所以，Python类也是 **可调用的** 。

然后，在 **FastAPI** 中，可以使用Python类作为依赖项。

FastAPI实际检查的是它是否是 "可调用的" (函数、类或任何其他东西)和所定义的参数。

如果您在 **FastAPI** 中传递一个 "可调用的" 作为依赖项，它将分析该 "可调用的" 的参数，并以与 *路径操作函数* 的参数相同的方式处理它们。包括子依赖项。

这也适用于没有任何参数的调用。与没有参数的 *路径操作函数* 相同。

然后，我们可以将上面例子中的依赖关系 "可依赖的" `common_parameters` 改为类 `CommonQueryParams`:

```Python hl_lines="11-15"
{!../../../docs_src/dependencies/tutorial002.py!}
```

注意用于创建类实例的 `__init__` 方法:

```Python hl_lines="12"
{!../../../docs_src/dependencies/tutorial002.py!}
```

...它的参数与之前的 `common_parameters` 相同:

```Python hl_lines="8"
{!../../../docs_src/dependencies/tutorial001.py!}
```

这些参数是 **FastAPI** 用来 "解决" 依赖关系的。

这两种例子里，它包括:

* 一个可选的查询参数 `q` 。
* 一个查询参数 `skip` , 拥有默认值 `0` 。
* 一个查询参数 `limit` , 拥有默认值 `100` 。

在这两种情况下，数据都将被转换、验证、在OpenAPI模式中生成文档，等等。

## 使用它

现在可以使用这个类声明依赖项了。

```Python hl_lines="19"
{!../../../docs_src/dependencies/tutorial002.py!}
```

**FastAPI** 调用 `CommonQueryParams` 类。浙江创建该类的一个 "实例" ，这个实例将会传递给你的函数的 `commons` 参数。

## 类型注释和 `Depends`

注意我们是如何在上面的代码中两次编写 `CommonQueryParams` :

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

后一个 `CommonQueryParams` 在:

```Python
... = Depends(CommonQueryParams)
```

…**FastAPI**实际通过这个知道依赖项是什么。

FastAPI 将从中提取声明的参数，这就是 FastAPI 实际调用的内容。

---

在这个例子里，第一个 `CommonQueryParams` 在:

```Python
commons: CommonQueryParams ...
```

...对于**FastAPI**没有任何特殊的意义。FastAPI不会将它用于数据转换、验证等。(因为它使用了 `= Depends(CommonQueryParams)` 为了这些目的)。

你可以这样写:

```Python
commons = Depends(CommonQueryParams)
```

..如:

```Python hl_lines="19"
{!../../../docs_src/dependencies/tutorial003.py!}
```

但是声明类型是被鼓励的，因为这样你的编辑器会知道什么会作为参数 `commons` 被传递，然后它可以帮助你进行代码补全，类型检查，等等:

<img src="/img/tutorial/dependencies/image02.png">

## 快捷方式

但是你看到我们这里有一些代码重复，写了两次 `CommonQueryParams` :

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

**FastAPI** 为这些情况提供了一个快捷方式，其中依赖项是一个*特别地* 类，**FastAPI**将 "调用" 这个类来创建类本身的实例。

对于这些特定的情况，您可以执行以下操作:

不用这么写:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

...你可以写:

```Python
commons: CommonQueryParams = Depends()
```

您将依赖项声明为参数的类型，并使用 `Depends()` 作为该函数的参数的 "默认" 值(在 `=` 之后)，在 `Depends()` 中没有任何参数，而不必在 `Depends(CommonQueryParams)` 中*再次*写出完整的类。

同样的例子看起来是这样的:

```Python hl_lines="19"
{!../../../docs_src/dependencies/tutorial004.py!}
```

...**FastAPI** 会知道该做什么。

!!! tip
    如果这看起来更令人困惑而不是有用，忽略它，你 *不需要* 它。

    这只是一个快捷方式。因为 **FastAPI** 关心帮助您最小化代码重复。
