# 类作为依赖项 { #classes-as-dependencies }

在深入探究 **依赖注入** 系统之前，让我们升级之前的例子。

## 来自前一个例子的`dict` { #a-dict-from-the-previous-example }

在前面的例子中, 我们从依赖项 ("可依赖对象") 中返回了一个 `dict`:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[9] *}

但是后面我们在*路径操作函数*的参数 `commons` 中得到了一个 `dict`。

我们知道编辑器不能为 `dict` 提供很多支持(比如补全)，因为它们无法知道其键和值类型。

对此，我们可以做的更好...

## 什么构成了依赖项？ { #what-makes-a-dependency }

到目前为止，您看到的依赖项都被声明为函数。

但这并不是声明依赖项的唯一方法(尽管它可能是更常见的方法)。

关键因素是依赖项应该是 "可调用对象"。

Python 中的 "**可调用对象**" 是指任何 Python 可以像函数一样 "调用" 的对象。

所以，如果你有一个对象 `something` (可能_不是_一个函数)，你可以 "调用" 它(执行它)，就像：

```Python
something()
```

或者

```Python
something(some_argument, some_keyword_argument="foo")
```

那么它就是一个 "可调用对象"。

## 类作为依赖项 { #classes-as-dependencies_1 }

您可能会注意到，要创建一个 Python 类的实例，您可以使用相同的语法。

举个例子:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

在这个例子中, `fluffy` 是一个 `Cat` 类的实例。

为了创建 `fluffy`，你在 "调用" `Cat` 。

所以，Python 类也是 **可调用对象**。

因此，在 **FastAPI** 中，你可以使用一个 Python 类作为一个依赖项。

实际上 FastAPI 检查的是它是一个 "可调用对象"（函数，类或其他任何类型）以及定义的参数。

如果您在 **FastAPI** 中传递一个 "可调用对象" 作为依赖项，它将分析该 "可调用对象" 的参数，并以处理*路径操作函数*的参数的方式来处理它们。包括子依赖项。

这也适用于完全没有参数的可调用对象。这与不带参数的*路径操作函数*一样。

所以，我们可以将上面的依赖项 "可依赖对象" `common_parameters` 更改为类 `CommonQueryParams`:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[11:15] *}

注意用于创建类实例的 `__init__` 方法：

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[12] *}

...它与我们以前的 `common_parameters` 具有相同的参数：

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[8] *}

这些参数就是 **FastAPI** 用来 "解决" 依赖项的。

在两个例子下，都有：

* 一个可选的 `q` 查询参数，是 `str` 类型。
* 一个 `skip` 查询参数，是 `int` 类型，默认值为 `0`。
* 一个 `limit` 查询参数，是 `int` 类型，默认值为 `100`。

在两个例子下，数据都将被转换、验证、在 OpenAPI schema 上文档化，等等。

## 使用它 { #use-it }

现在，您可以使用这个类来声明你的依赖项了。

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[19] *}

**FastAPI** 调用 `CommonQueryParams` 类。这将创建该类的一个 "实例"，该实例将作为参数 `commons` 被传递给你的函数。

## 类型注解 vs `Depends` { #type-annotation-vs-depends }

注意，我们在上面的代码中编写了两次`CommonQueryParams`：

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.9+ 非 Annotated

/// tip | 提示

如果可能，优先使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

最后的 `CommonQueryParams`，在：

```Python
... Depends(CommonQueryParams)
```

...实际上是 **FastAPI** 用来知道依赖项是什么的。

FastAPI 将从依赖项中提取声明的参数，这才是 FastAPI 实际调用的。

---

在本例中，第一个 `CommonQueryParams`，在：

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, ...
```

////

//// tab | Python 3.9+ 非 Annotated

/// tip | 提示

如果可能，优先使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams ...
```

////

...对于 **FastAPI** 没有任何特殊的意义。FastAPI 不会使用它进行数据转换、验证等 (因为对于这，它使用 `Depends(CommonQueryParams)`)。

你实际上可以只这样编写:

//// tab | Python 3.9+

```Python
commons: Annotated[Any, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.9+ 非 Annotated

/// tip | 提示

如果可能，优先使用 `Annotated` 版本。

///

```Python
commons = Depends(CommonQueryParams)
```

////

..就像:

{* ../../docs_src/dependencies/tutorial003_an_py310.py hl[19] *}

但是声明类型是被鼓励的，因为那样你的编辑器就会知道将传递什么作为参数 `commons` ，然后它可以帮助你完成代码，类型检查，等等：

<img src="/img/tutorial/dependencies/image02.png">

## 快捷方式 { #shortcut }

但是您可以看到，我们在这里有一些代码重复了，编写了`CommonQueryParams`两次：

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.9+ 非 Annotated

/// tip | 提示

如果可能，优先使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

**FastAPI** 为这些情况提供了一个快捷方式，在这些情况下，依赖项 *明确地* 是一个类，**FastAPI** 将 "调用" 它来创建类本身的一个实例。

对于这些特定的情况，您可以跟随以下操作：

不是写成这样：

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.9+ 非 Annotated

/// tip | 提示

如果可能，优先使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

...而是这样写:

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, Depends()]
```

////

//// tab | Python 3.9+ 非 Annotated

/// tip | 提示

如果可能，优先使用 `Annotated` 版本。

///

```Python
commons: CommonQueryParams = Depends()
```

////

您声明依赖项作为参数的类型，并使用 `Depends()` 作为该函数的参数的 "默认" 值，而在 `Depends()` 中没有任何参数，而不是在 `Depends(CommonQueryParams)` 编写完整的类*再次*。

同样的例子看起来像这样：

{* ../../docs_src/dependencies/tutorial004_an_py310.py hl[19] *}

... **FastAPI** 会知道怎么处理。

/// tip | 提示

如果这看起来更加混乱而不是更加有帮助，那么请忽略它，你不*需要*它。

这只是一个快捷方式。因为 **FastAPI** 关心的是帮助您减少代码重复。

///
